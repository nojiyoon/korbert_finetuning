# KorBERT_QA
1. fine-tuning 데이터 만들기
    - `python csv2json {input_file} {output_file}`
    - 예시 : `!python csv2json /content/drive/MyDrive/공룡_취합.csv /content/drive/MyDrive/KDinoQuAD`

2. fine-tuning 진행
    - FLAGS 참고해 `!python run_squad.py` 옵션 작성 후 실행

3. 모델 평가
    - `python evaluate.py {input_file} {predict_file}`

4. 결과 확인
