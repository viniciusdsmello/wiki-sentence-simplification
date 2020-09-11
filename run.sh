#!/bin/bash

if [ "$1" = "train" ]; then
	CUDA_VISIBLE_DEVICES=0 python run.py train --train-src=./data/normal.train --train-tgt=./data/simple.train --dev-src=./data/normal.dev --dev-tgt=./data/simple.dev --vocab=vocab.json --cuda --cuda-device=0
elif [ "$1" = "decode_test" ]; then
        CUDA_VISIBLE_DEVICES=0 python run.py decode model.bin ./data/normal.test ./data/simple.test outputs/test_outputs.txt --cuda --cuda-device=0
elif [ "$1" = "decode_dev" ]; then
        CUDA_VISIBLE_DEVICES=0 python run.py decode model.bin ./data/normal.dev ./data/simple.dev outputs/dev_outputs.txt --cuda --cuda-device=0
elif [ "$1" = "train_local" ]; then
	python run.py train --train-src=./data/normal.train --train-tgt=./data/simple.train --dev-src=./data/normal.test --dev-tgt=./data/simple.test --vocab=vocab.json
elif [ "$1" = "test_local" ]; then
    python run.py decode model.bin ./data/normal.dev ./data/simple.dev outputs/test_outputs.txt
elif [ "$1" = "vocab" ]; then
	python vocab.py --train-src=./data/normal.train --train-tgt=./data/simple.train vocab.json
elif [ "$1" = "split_data" ]; then
	python utils/split_data.py
else
	echo "Invalid Option Selected"
fi
