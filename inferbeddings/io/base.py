# -*- coding: utf-8 -*-

import gzip
import bz2
import pickle

import logging

logger = logging.getLogger(__name__)


def iopen(file, *args, **kwargs):
    _open = open
    if file.endswith('.gz'):
        _open = gzip.open
    elif file.endswith('.bz2'):
        _open = bz2.open
    return _open(file, *args, **kwargs)


def read_triples(path):
    logger.debug('Acquiring %s ..' % path)
    pos_triples, neg_triples = [], None

    with iopen(path, 'rt') as f:
        lines = f.readlines()

    if len(lines) > 0:
        if len(lines[0].split()) == 3:
            has_negatives = False
        elif len(lines[0].split()) == 4:
            has_negatives = True
            neg_triples = []
        else:
            raise ValueError('Invalid file format')

        for line in lines:
            if has_negatives:
                if len(line.strip()) > 0:
                    s, p, o, label = line.split()
                    if int(label.strip()) == 1:
                        pos_triples += [(s.strip(), p.strip(), o.strip())]
                    else:
                        neg_triples += [(s.strip(), p.strip(), o.strip())]
            else:
                line_strip = line.strip()
                if len(line_strip) > 0:
                    line_split = line.split()
                    if len(line_split) != 3:
                        logger.error(line_split)
                    s, p, o = line_split
                    pos_triples += [(s.strip(), p.strip(), o.strip())]

    return pos_triples, neg_triples


def save(path, obj):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)
    logger.info('Object {} saved in {}.pkl'.format(type(obj), path))
