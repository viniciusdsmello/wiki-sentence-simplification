#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import unittest
import torch
import torch.nn as nn


class Highway(nn.Module):

    def __init__(self, word_embed_size: int, p_dropout: float):
        super().__init__()
        self.proj = nn.Linear(word_embed_size, word_embed_size, bias=True)
        self.gate = nn.Linear(word_embed_size, word_embed_size, bias=True)
        self.dropout = nn.Dropout(p=p_dropout)

    def forward(self, x_conv_out: torch.Tensor) -> torch.Tensor:
        x_gate = torch.sigmoid(self.gate.forward(x_conv_out))
        x_proj = torch.relu(self.proj.forward(x_conv_out))

        x_highway = x_gate * x_proj + (1 - x_gate) * x_conv_out
        x_word_emb = self.dropout.forward(x_highway)
        return x_word_emb


class HighwaySanityChecks(unittest.TestCase):

    def test_shape(self):
        batch_size, word_embed_size = 64, 40
        highway = Highway(word_embed_size, 0.5)

        x_conv_out = torch.randn([batch_size, word_embed_size])
        x_word_emb = highway.forward(x_conv_out)

        self.assertEqual(x_word_emb.shape, (batch_size, word_embed_size))
        self.assertEqual(x_word_emb.shape, x_conv_out.shape)

    def test_gate_bypass(self):
        batch_size, word_embed_size = 64, 40
        highway = Highway(word_embed_size, 0.0)
        highway.gate.weight.data[:, :] = 0.0
        highway.gate.bias.data[:] = -math.inf

        x_conv_out = torch.randn([batch_size, word_embed_size])
        x_word_emb = highway.forward(x_conv_out)

        self.assertTrue(torch.allclose(x_conv_out, x_word_emb))

    def test_gate_projection(self):
        batch_size, word_embed_size = 64, 40
        highway = Highway(word_embed_size, 0.0)
        highway.proj.weight.data = torch.eye(word_embed_size)
        highway.proj.bias.data[:] = 0.0
        highway.gate.weight.data[:, :] = 0.0
        highway.gate.bias.data[:] = +math.inf

        x_conv_out = torch.rand([batch_size, word_embed_size])
        x_word_emb = highway.forward(x_conv_out)

        self.assertTrue(torch.allclose(x_conv_out, x_word_emb))

 

