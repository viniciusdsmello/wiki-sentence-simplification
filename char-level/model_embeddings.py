#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import torch.nn as nn

from cnn import CNN
from highway import Highway

class ModelEmbeddings(nn.Module): 
    """
    Class that converts input words to their CNN-based embeddings.
    """
    def __init__(self, embed_size, vocab):
        """
        Init the Embedding layer for one language
        @param embed_size (int): Embedding size (dimensionality) for the output 
        @param vocab (VocabEntry): VocabEntry object. See vocab.py for documentation.
        """
        super(ModelEmbeddings, self).__init__()      

        pad_token_idx = vocab.char2id['<pad>']
        char_embed_size, window_size, p_dropout = 50, 5, 0.3

        self.char_embed = nn.Embedding(len(vocab.char2id), char_embed_size, pad_token_idx)
        self.cnn = CNN(char_embed_size, embed_size, window_size)
        self.highway = Highway(embed_size, p_dropout)

        self.embed_size = embed_size

        

    def forward(self, input):
        """
        Looks up character-based CNN embeddings for the words in a batch of sentences.
        @param input: Tensor of integers of shape (sentence_length, batch_size, max_word_length) where
            each integer is an index into the character vocabulary

        @param output: Tensor of shape (sentence_length, batch_size, embed_size), containing the 
            CNN-based embeddings for each word of the sentences in the batch
        """        

        x_embed = self.char_embed.forward(input)

        max_sent, batch_size, max_word, char_embed_size = x_embed.shape
        x_embed_conv = x_embed.view(max_sent * batch_size, max_word, char_embed_size)
        x_embed_conv = x_embed_conv.transpose(1, 2)
        x_conv_out = self.cnn.forward(x_embed_conv)
        x_word_emb = self.highway.forward(x_conv_out)
        x_word_emb = x_word_emb.view(max_sent, batch_size, -1)

        return x_word_emb

        

