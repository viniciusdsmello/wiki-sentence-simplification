#!/bin/bash

if [ "$1" = "train" ]; then
	CUDA_VISIBLE_DEVICES=0 python run.py train --train-src=./data/normal.train --train-tgt=./data/simple.train --dev-src=./data/normal.dev --dev-tgt=./data/simple.dev --vocab=vocab.json --cuda
elif [ "$1" = "test" ]; then
        CUDA_VISIBLE_DEVICES=0 python run.py decode model.bin ./data/normal.test ./data/simple.test outputs/test_outputs.txt --cuda
elif [ "$1" = "train_local" ]; then
	python run.py train --train-src=./data/normal.train --train-tgt=./data/simple.train --dev-src=./data/normal.dev --dev-tgt=./data/simple.dev --vocab=vocab.json
elif [ "$1" = "test_local" ]; then
    python run.py decode model.bin ./data/normal.test ./data/simple.test outputs/test_outputs.txt
elif [ "$1" = "vocab" ]; then
	python vocab.py --train-src=./data/normal.train --train-tgt=./data/simple.train vocab.json
else
	echo "Invalid Option Selected"
fi
