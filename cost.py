#! /usr/bin/env python3

# Copyright 2016 Toyota Research Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Parse structure text files and emit various reports describing how
much effort or cost would be involved."""


import argparse

from model.from_html import from_html


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
                        
    result = parser.parse_args()

    root = from_html(open(result.input).read())

    def dump_quantiles(indent, node):
        print(' ' * indent,
              " : ".join("%d" % node.cost().quantile(q / 100)
                       for q in (10, 25, 50, 75, 90)))

    # Print out the tree.
    def dump_node(indent, node):
        print(' ' * indent, node.tag, ':',
              node.format_distribution(),
              node.data)
        dump_quantiles(indent + 1, node)
        for child in node.children:
            dump_node(indent + 2, child)

    dump_node(0, root)
    print("TOTAL:")
    dump_quantiles(0, root)

if __name__ == '__main__':
    main()