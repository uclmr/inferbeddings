# -*- coding: utf-8 -*-

import pytest
import subprocess

import sys
sys.setrecursionlimit(65535)


@pytest.mark.light
def test_symmetric_tiny_cli():
    # Checking if results are still not nice when not using adversarial training,
    # i.e. by using the parameters --adv-weight 0
    cmd = ['./bin/kbp-cli.py',
           '--train', 'data/synth/symmetric-tiny/data.tsv',
           '--test', 'data/synth/symmetric-tiny/data-inverse-test.tsv',
           '--lr', '0.1',
           '--model', 'ComplEx',
           '--similarity', 'dot',
           '--margin', '1',
           '--embedding-size', '50',
           '--nb-epochs', '100',
           '--clauses', 'data/synth/symmetric-tiny/clauses_inverse.pl',
           '--adv-lr', '0.1',
           '--adv-batch-size', '100',
           '--adv-weight', '0',
           '--adversary-epochs', '10',
           '--loss', 'hinge']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    # Hits@10 should be around 0% at first
    assert float(err.split()[-1][:-1]) < 10.0

    cmd = ['./bin/kbp-cli.py',
           '--train', 'data/synth/symmetric-tiny/data.tsv',
           '--test', 'data/synth/symmetric-tiny/data-inverse-test.tsv',
           '--lr', '0.1',
           '--model', 'ComplEx',
           '--similarity', 'dot',
           '--margin', '1',
           '--embedding-size', '50',
           '--nb-epochs', '100',
           '--clauses', 'data/synth/symmetric-tiny/clauses_inverse.pl',
           '--adv-lr', '0.1',
           '--adv-batch-size', '100',
           '--adv-weight', '0',
           '--adversary-epochs', '10',
           '--loss', 'hinge',
           '--materialize']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    # Hits@10 should be at least 90% even after a limited number of epochs
    assert float(err.split()[-1][:-1]) > 99.0

    # Checking if results are still nice
    cmd = ['./bin/kbp-cli.py',
           '--train', 'data/synth/symmetric-tiny/data.tsv',
           '--test', 'data/synth/symmetric-tiny/data-inverse-test.tsv',
           '--lr', '0.1',
           '--model', 'ComplEx',
           '--similarity', 'dot',
           '--margin', '1',
           '--embedding-size', '50',
           '--nb-epochs', '100',
           '--clauses', 'data/synth/symmetric-tiny/clauses_inverse.pl',
           '--adv-lr', '0.1',
           '--adv-batch-size', '100',
           '--adv-weight', '100',
           '--adversary-epochs', '10',
           '--loss', 'hinge']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    # Hits@10 should be at least 90% even after a limited number of epochs
    assert float(err.split()[-1][:-1]) > 99.0

    # Checking if results are still nice
    cmd = ['./bin/kbp-cli.py',
           '--train', 'data/synth/symmetric-tiny/data.tsv',
           '--test', 'data/synth/symmetric-tiny/data-inverse-test.tsv',
           '--lr', '0.1',
           '--model', 'ComplEx',
           '--similarity', 'dot',
           '--margin', '1',
           '--embedding-size', '50',
           '--nb-epochs', '100',
           '--clauses', 'data/synth/symmetric-tiny/clauses_inverse.pl',
           # '--adv-lr', '0.1',
           '--adv-closed-form',
           '--adv-batch-size', '100',
           '--adv-weight', '100',
           '--adversary-epochs', '10',
           '--loss', 'hinge']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    # Hits@10 should be at least 90% even after a limited number of epochs
    assert float(err.split()[-1][:-1]) > 99.0

    cmd = ['./bin/kbp-cli.py',
           '--train', 'data/synth/symmetric-tiny/data.tsv',
           '--test', 'data/synth/symmetric-tiny/data-inverse-test.tsv',
           '--lr', '0.1',
           '--model', 'TransE',
           '--similarity', 'dot',
           '--margin', '1',
           '--embedding-size', '50',
           '--nb-epochs', '100',
           '--clauses', 'data/synth/symmetric-tiny/clauses_inverse.pl',
           '--adv-lr', '0.1',
           '--adv-batch-size', '100',
           '--adv-weight', '100',
           '--adversary-epochs', '10',
           '--loss', 'hinge']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    # Hits@10 should be at least 90% even after a limited number of epochs
    assert float(err.split()[-1][:-1]) > 99.0

    cmd = ['./bin/kbp-cli.py',
           '--train', 'data/synth/symmetric-tiny/data.tsv',
           '--test', 'data/synth/symmetric-tiny/data-inverse-test.tsv',
           '--lr', '0.1',
           '--model', 'ComplEx',
           '--similarity', 'dot',
           '--margin', '1',
           '--embedding-size', '50',
           '--nb-epochs', '100',
           '--clauses', 'data/synth/symmetric-tiny/clauses_inverse.pl',
           '--adv-lr', '0.1',
           '--adv-batch-size', '100',
           '--adv-weight', '0',
           '--adversary-epochs', '10',
           '--loss', 'hinge']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    # Hits@10 should be at least 90% even after a limited number of epochs
    assert float(err.split()[-1][:-1]) < 5.0

if __name__ == '__main__':
    pytest.main([__file__])
