"""
Copyright (c) Facebook, Inc. and its affiliates.
All rights reserved.
This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
----------
Downloading and preparation of official Librispeech 4-gram language model.
Please install `kenlm` on your own - https://github.com/kpu/kenlm
Command : python3 prepare_librispeech_official_lm.py --dst [...] --kenlm [...]/kenlm/
Replace [...] with appropriate paths
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
import re


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Librispeech official lm creation.")
    parser.add_argument(
        "--dst", help="data destination directory", default="./decoder"
    )

    parser.add_argument(
        "--lm", help="arpa"
    )

    args = parser.parse_args()
    decoder_path = args.dst
    os.makedirs(decoder_path, exist_ok=True)


    arpa_file = args.lm

    # prepare lexicon word -> tokens spelling
    # write words to lexicon.txt file
    lex_file = os.path.join(decoder_path, "lexicon.txt")
    print("Writing Lexicon file - {}...".format(lex_file))
    with open(lex_file, "w") as f:
        # get all the words in the arpa file
        with open(arpa_file, "r") as arpa:
            for line in arpa:
                # verify if the line corresponds to unigram
                if not re.match(r"[-]*[0-9\.]+\t\S+\t*[-]*[0-9\.]*$", line):
                    continue
                word = line.split("\t")[1]
                word = word.strip().lower()
                if word == "<unk>" or word == "<s>" or word == "</s>":
                    continue
                assert re.match("^[a-z']+$", word), "invalid word - {w}".format(w=word)
                f.write("{w}\t{s} |\n".format(w=word, s=" ".join(word)))

    print("Done!", flush=True)