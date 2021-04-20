# KorBERT_QA
1. fine-tuning 데이터 만들기
    - `python csv2json.py {input_file} {output_file}`
    - 예시 : `!python csv2json.py data/dino_combined_final.csv data/KDinoQuAD_v1`

2. fine-tuning 진행
    - FLAGS를 참고하셔서 TO-DO 부분을 완성해 주세요. 
    - run.sh 역시 빈 부분을 채워주세요.
    - `!sh run.sh` 실행해 주시면 finetuning이 시작됩니다.

3. 모델 평가
    - 지정한 output_dir에 저장된 모델 체크포인트를 이용해 모델을 평가합니다.
    - 평가를 위해 evaluate-v1.0.py를 이용합니다. 
    - 다음과 같이 사용할 수 있습니다.
    - `!python evaluate-v1.0.py {input_file} {predict_file}`
    - 예시 : `!python evaluate-v1.0.py data/KDinoQuAD_v1_dev.json output_dir/prediction.json`

4. 결과 확인
    - 화면에 출력된 EM, F1 score 가 모델을 평가할 수 있는 지표가 됩니다.
