# -*- coding: utf-8 -*-
"""csv2json.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_9_IUUqQ1n15gY-cWwmSXWPITbgupnxv

# CSV to JSON
## 과정
1. json으로 바꾼다.
2. 제공된 dev data와 합친다.

- train data로는 *KorQuAD1.0* 버전의 데이터를 사용하도록 하겠습니다.

- colab의 자원적 한계로 인해 *KorQuAD1.0 dev* 데이터를 사용합니다.

"""

# 필요한 모듈 import
import os
import re
import glob
import wget
import sys
import csv
import pandas as pd


"""## CSV 정제"""

print("#########START MAKING TRAIN, DEV, TEST FILES##########")
# 공룡_취합.csv 파일을 전처리하는 과정입니다.
# 최종 파일이 만들어지는 과정에서 만들어질 중간 파일들이 저장될 경로를 설정해줍니다.
############################경로설정##################################
output_path = "./data"
######################################################################

# 파일 경로를 입력받은 경로로 설정합니다.
input_file = sys.argv[1]
output_file = sys.argv[2]

# csv.reader로 읽어옵니다.
combine = csv.reader(open(input_file))

# 편집하기 쉽게 리스트로 만듭니다.
lines = list(combine)
print(lines[:10])

# context 중에 '\n'가 포함된 경우가 있어 해당 부분을 제거하고, 그에 맞는 start_position 을 새로 부여해주는 작업을 진행합니다.
new = []
q_num = 1
id_num = 0
new.append(lines[0])

for index, line in enumerate(lines[1:]):
  q_num += 1
  if line[1] != "":
    id_num += 1
    q_num = 1
    context = line[1]
  else:
    if lines[index-1][1] != '':
      context = lines[index-1][1]
    elif lines[index-2][1] != '':
      context = lines[index-2][1]
    elif lines[index-3][1] != '':
      context = lines[index-3][1]
  if '\n' in context:
    new_line_num = len(re.findall("\n", context[:int(line[4])]))
  else:
    new_line_num = 0
  line[0] = "dino_{}_{}".format(str(id_num), str(q_num))
  context = re.sub("\n", "", context)
  original_num = int(re.sub(" ", "", line[4]).strip())
  new_num = original_num - new_line_num
  line[4] = str(new_num)
  line[1] = context
  # 만약 새로 설정한 position의 context에서의 정답과 answer_text가 불일치할 경우 제외합니다. 
  if context[new_num:new_num+len(line[3])] != line[3]:
    pass
  else:
    new.append(line)

# 만들어진 csv 파일을 'dino.csv'이름으로 저장합니다.
writer = csv.writer(open(os.path.join(output_path, 'dino.csv'), 'w'))
writer.writerows(new)
print("dino.csv saved in {}".format(output_path))

"""## train data

download  dev data

"""
# download KorQuAD 1.0 dev data
###################################경로설정#########################
url = "https://korquad.github.io/dataset/KorQuAD_v1.0_dev.json" ####
down_path = "./data"                                                  ####
####################################################################
if not os.path.isfile(os.path.join(down_path, "KorQuAD_v1.0_dev.json")):
    wget.download(url, out=down_path)                               

"""load train or dev data

**dev가 아닌 train을 load 해서 사용해주세요.**
"""

# import json module
import json

# load dev data
with open(os.path.join(output_path, "KorQuAD_v1.0_dev.json")) as json_file:
  korquad_data = json.load(json_file)

"""convert csv to json and merge"""

# 만든 csv load
df_combine = pd.read_csv(os.path.join(output_path, "dino.csv"))

new_dict = {"version": "dinosaure_squad_v1", "data": []} # 데이터를 담을 dictionary

# row 를 돌면서 dictionary 만들기
id_dict = dict()
num = 0
for index, row in df_combine.iterrows():
  id_ = row['id']
  id_num = id_[:-2]
  if id_num not in id_dict:
    id_dict[id_num] = row['context']
    new_dict["data"].append({"paragraphs": [{"qas": [], "context":row['context']}]})
  new_dict["data"][-1]["paragraphs"][-1]["qas"].append({"answers": [{"text": "", "answer_start": ""}],
                                                          "id": id_,
                                                        "question": row["question"]})
  
  new_dict["data"][-1]["paragraphs"][-1]["qas"][-1]["answers"][-1]["text"] = row["answer_text"]
  new_dict["data"][-1]["paragraphs"][-1]["qas"][-1]["answers"][-1]["answer_start"] = int(row["start_position"])

# json 파일로 저장해 확인해 봅시다.
with open(os.path.join(output_path, "DinoQuAD_v1.json"), "w") as outputfile:
  json.dump(new_dict, outputfile)

print("DinoQuAD_v1.json saved in {}".format(output_path))

"""만들어진 파일 확인"""
# 저장한 파일 load
with open(os.path.join(output_path, "DinoQuAD_v1.json")) as f:
  dino_data = json.load(f)

# 잘못 저장된 파일 확인하기
wrong_list = dict()

for example in dino_data['data']:
  paragraphs = example['paragraphs']
  for paragraph in paragraphs:
    qas = paragraph['qas']
    context = paragraph['context']
    for qa in qas:
      answer_text = qa['answers'][0]['text']
      answer_start = qa['answers'][0]['answer_start']
      answer_len = len(answer_text)
      if context[answer_start:answer_start+answer_len] != answer_text:
        wrong_list[qa["id"]] = {}
        wrong_list[qa["id"]]["original"] = answer_text
        wrong_list[qa["id"]]["changed"] = context[answer_start:answer_start+answer_len]

print("wrong list : ")
print(wrong_list)

print("START MAKING JSON FILES")
# train data와 합치기
merge_train_dict = {"version": "KDinoQuAD_v1_train", "data": []}
merge_dev_dict = {"version": "KDinoQuAD_v1_dev", "data": []}
merge_test_dict = {"version": "KDinoQuAD_v1_test", "data": []}

# train, dev, test 8 : 1 : 1 비율로 나누기
korquad_train_num = int(len(korquad_data["data"]) * 0.8)
dino_train_num = int(len(dino_data["data"]) * 0.8)

korquad_dev_num = korquad_train_num + int(korquad_train_num/2)
dino_dev_num = dino_train_num + int(dino_train_num/2)

# merge
merge_train_dict["data"].extend(korquad_data["data"][:korquad_train_num]) # korquad 추가
merge_train_dict["data"].extend(dino_data["data"][:dino_train_num]) # dino 추가

merge_dev_dict["data"].extend(korquad_data["data"][korquad_train_num:korquad_dev_num]) # korquad 추가
merge_dev_dict["data"].extend(dino_data["data"][dino_train_num:dino_dev_num]) # dino 추가

merge_test_dict["data"].extend(korquad_data["data"][korquad_dev_num:]) # korquad 추가
merge_test_dict["data"].extend(dino_data["data"][dino_dev_num:]) # dino 추가

# 저장
with open(output_file + "_train.json", "w") as f:
  json.dump(merge_train_dict, f)

with open(output_file + "_dev.json", "w") as f:
  json.dump(merge_dev_dict, f)

with open(output_file + "_test.json", "w") as f:
  json.dump(merge_test_dict, f)

# evaluate 위한 데이터 만들기
# lod KDinoQuAD_v1_test.json
with open(output_file + "_dev.json") as f:
    dev_data = json.load(f)

dev_dict = {}

for example in dev_data['data']:
  paragraphs = example['paragraphs']
  for paragraph in paragraphs:
    qas = paragraph['qas']
    for qa in qas:
      answer_text = qa['answers'][0]['text']
      id_ = qa['id']
      dev_dict[id_] = answer_text

with open(output_file + "_dev_answer.json", "w") as f:
    json.dump(dev_dict, f, indent=4)

print("DONE")