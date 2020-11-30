#!/usr/bin/env python

"""

This script walks in a folder tree containing blockchain blocks and parse it in
order to return structured data about divergent blocks containing blocks id,
hash, nodes & timestamp of block file creation.

Input: root tree directory must contain one folder per node containing blocks.
Block file must be named like `<block_id>.json`

.
├── shk01
│   ├── 0.json
│   ├── 1.json
│   ├── 2.json
│   └── 3.json
├── shk02
│   ├── 0.json
│   ├── 1.json
│   ├── 2.json
│   └── 3.json
└── ....

WARNING:
    * You need to preserve originial timestamp in files attributes if you want to get relevant timestamp in result.
    * You need to have ONLY blocks folder in your tree

Output example:

{
  "4590": [
    [
      "shk02",
      4590,
      1566835285.0830116,
      "f6ae590f066b6b5d09ffa2501873cef5"
    ],
    [
      "shk01",
      4590,
      1566835284.9863448,
      "f6ae590f066b6b5d09ffa2501873cef5"
    ],
      "shk03",
      4590,
      1566835285.269678,
      "8bb41f12d4a1d9f4811655f6b8b54863"
    ]
  ],
  "4891": [
    [
      "shk01",
      4891,
      1566835285.086345,
      "69843d59b6ac5e9d830b9b91ab3aba06"
    ],
    [
      "shk02",
      4891,
      1566835285.086345,
      "69843d59b6ac5e9d830b9b91ab3aba06"
    ],
    [
      "shk03",
      4891,
      1566835285.6030116,
      "2cf8cf6dea666b0a9eaf3e3d9a375859"
    ],
  ]
}

"""

import argparse
import hashlib
import json
import logging
import os

def parse_cli():
    """ parser """
    parser = argparse.ArgumentParser(description='Return divergent block in blockchain')
    parser.add_argument('--path', '-p',
                        required=True,
                        help='root path of the directory tree')
    parser.add_argument('-v', '--verbose',
                        action='store_const',
                        dest='loglevel',
                        const=logging.INFO,
                        default=logging.WARNING,
                        help='display INFO logging messages')
    parser.add_argument('-d', '--debug',
                        action='store_const',
                        dest='loglevel',
                        const=logging.DEBUG,
                        help='display DEBUG logging messages')

    return parser


def main():
    """ main """

    args = parse_cli().parse_args()
    logging.basicConfig(level=args.loglevel)

    raw = []
    nodes = []
    blocks = []
    divergence = {}

    # Retrieve nodes list
    try:
        nodes = os.listdir(args.path)
    except FileNotFoundError:
        logging.error('Path {} not found', args.path)
    except NotADirectoryError:
        logging.error('"{}" isn\'t a directory'.format(args.path))

    # Get blocks for each node
    logging.info('begin the parsing')
    for node in nodes:
        logging.debug('begin parsing on node "{}"'.format(node))
        node_path = "{}/{}".format(args.path, node)
        for block in os.scandir(node_path):
            block_id = block.name.replace('.json', '')
            block_time = os.path.getctime(block.path)
            block_hash = ''
            with open(block.path, "rb") as file:
                block_hash = hashlib.md5(file.read()).hexdigest()
            raw.append((node, int(block_id), block_time, block_hash))

    # Order raw data in a list with block_id as list "key"
    logging.info('begin the raw ordering')
    block_id = 0
    while True:
        blocks.append([block for block in raw if block[1] == block_id])
        if not blocks[block_id]:
            logging.info('end of blocks ordering. Last was number "{}"'.format(block_id - 1))
            break
        block_id += 1

    # Detect nodes divergences
    logging.info('begin the divergence detection')

    # Input block list example:
    #      node   id      timestamp                     hash
    # [
    #   [
    #    ('shk02', 0, 1566835285.029678,  '21ffb74314bb084347b612d14169245b'),
    #    ('shk01', 0, 1566835284.9396782, '21ffb74314bb084347b612d14169245b'),
    #    ('shk03', 0, 1566835284.9396782, '21ffb74314bb084347b612d14169245b'),
    #   ],
    #   [
    #    ('shk02', 1, 1566835285.0430114, '3762d2ff5d01cf3172b8e4bf969b2b31'),
    #    ('shk01', 1, 1566835284.9530115, '3762d2ff5d01cf3172b8e4bf969b2b31'),
    #    ('shk03', 1, 1566835284.9396782, '4567hbjuhj3456787uihn8415zef5411'),
    #   ]
    # ]

    for block in blocks:
        block_id = int()
        try:
            block_id = block[0][1]
        except IndexError:
            logging.warning('Skip empty block')
            continue
        hash = set([node_block[3] for node_block in block])
        if len(hash) > 1:  # if it contains more than one hash
            logging.debug('divergence in block number "{}"'.format(block_id))
            divergence[block_id] = block

    print(json.dumps(divergence, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
