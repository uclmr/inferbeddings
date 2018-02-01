#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

import argparse
import requests

import pickle
import atexit

import numpy as np

import gzip
import json

import logging

logger = logging.getLogger(os.path.basename(sys.argv[0]))


def contradiction_loss(sentence1, sentence2):
    p1 = call(sentence1, sentence2)['contradiction']
    p2 = call(sentence2, sentence1)['contradiction']
    p1, p2 = float(p1), float(p2)
    return max(p1 - p2, 0) + max(p2 - p1, 0)


def persist(path):
    def decorator(fun):
        cache = {}
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                cache = pickle.load(f)

        def write():
            with open(path, 'wb') as f:
                pickle.dump(cache, f)
        atexit.register(lambda: write())

        def new_f(*args):
            if tuple(args) not in cache:
                cache[tuple(args)] = fun(*args)
            return cache[args]
        return new_f
    return decorator


@persist('dam_cache.p')
def call(sentence1, sentence2, url='http://127.0.0.1:8889/v1/nli'):
    data = {'sentence1': sentence1, 'sentence2': sentence2}
    ans = requests.post(url, data=data)
    ans_json = ans.json()
    return ans_json


def main(argv):
    def fmt(prog):
        return argparse.HelpFormatter(prog, max_help_position=100, width=200)

    argparser = argparse.ArgumentParser('SNLI Adversarial Candidate Generator', formatter_class=fmt)

    argparser.add_argument('--path', '-p', action='store', type=str, default='snli_1.0_train.jsonl.gz')
    argparser.add_argument('--seed', '-s', action='store', type=int, default=0)
    argparser.add_argument('--fraction', '-f', action='store', type=float, default=None)

    args = argparser.parse_args(argv)

    path = args.path
    seed = args.seed
    fraction = args.fraction

    obj_lst = []
    with gzip.open(path, 'rb') as f:
        for line in f:
            dl = line.decode('utf-8')
            obj_lst += [json.loads(dl)]

    if fraction is not None:
        rs = np.random.RandomState(seed)
        nb_obj = len(obj_lst)
        # Round to the closest integer
        nb_samples = int(round(nb_obj * fraction))

        sample_idxs = rs.choice(nb_obj, nb_samples, replace=False)
        sample_obj_lst = [obj_lst[i] for i in sample_idxs]
    else:
        sample_obj_lst = obj_lst

    for obj in sample_obj_lst:
        s1, s2 = obj['sentence1'], obj['sentence2']
        print(s1)
        print(s2)
        print(contradiction_loss(s1, s2))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main(sys.argv[1:])
