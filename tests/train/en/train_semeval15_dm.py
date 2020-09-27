# -*- coding:utf-8 -*-
# Author: hankcs
# Date: 2020-01-01 18:26
from hanlp.components.parsers.biaffine_parser import BiaffineSemanticDependencyParser
from hanlp.pretrained.glove import GLOVE_6B_100D
from tests import cdroot

cdroot()
save_dir = 'data/model/sdp/semeval15_biaffine_dm'
parser = BiaffineSemanticDependencyParser()
parser.fit('data/semeval15/en.dm.train.conll', 'data/semeval15/en.dm.dev.conll', save_dir,
           pretrained_embed={'class_name': 'HanLP>Word2VecEmbedding',
                             'config': {
                                 'trainable': False,
                                 'embeddings_initializer': 'zero',
                                 'filepath': GLOVE_6B_100D,
                                 'expand_vocab': True,
                                 'lowercase': True,
                                 'normalize': True,
                             }},
           )
parser.load(save_dir)  # disable variational dropout during evaluation so as to use CudaLSTM
sentence = [('Is', 'VBZ'), ('this', 'DT'), ('the', 'DT'), ('future', 'NN'), ('of', 'IN'), ('chamber', 'NN'),
            ('music', 'NN'), ('?', '.')]
print(parser.predict(sentence))
parser.evaluate('data/semeval15/en.id.dm.auto.conllu', save_dir)
parser.evaluate('data/semeval15/en.ood.dm.auto.conllu', save_dir)
