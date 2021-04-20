# 실행 코드를 완성해주세요.
python -m korbert.run_squad \
  --vocab_file=\
  --bert_config_file=\
  --init_checkpoint=\
  --do_train=True \
  --train_file=\
  --do_predict=True \
  --predict_file=\
  --train_batch_size=8 \
  --learning_rate=3e-5 \
  --use_tpu=False \
  --num_train_epochs=2 \
  --max_seq_length=384 \
  --doc_stride=128 \
  --do_lower_case=False \
  --output_dir=./output_dir/KDinoQuAD_v1
