#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018 seamus tuohy, <code@seamustuohy.com>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the included LICENSE file for details.
#
#
#
# Draw.io libraries contain compressed xml. I don't like using things I can't inspect first.
# This simple snippet let's me inspect that compressed xml and display it
#
# Here is an example object in a draw.io library
# {"xml":"jZHPbsMgDMafhnsK0pTrlnQ9rZc+AQ1OQSNx5HhN+vZzAv13qNQDkv37/IGNlam6eUd28D/oICqzVaYiRE5RN1cQo9JFcMrUSutCjtLfL9TNqhaDJej5HYNOhrONf5DI575ObORLzGz0dlhCJGW+Jh8YDoNtFjJJ58I8d9J6vZHQBYKGA/aS90jshbUhxgrjYpfrjLNQto3wkQl/4UH5aEo4tqLktoAY5pejrSjPtQPsgOkiJVNwy6trRR6/8BBOPtvKzOyY8tPNev8oCfJfXdP7TlbtaWX/","w":120,"h":80,"aspect":"fixed","title":"AND Gate"}
#
# ALTERNATIVES
#
# You can do this by hand with the drawio tools page:
#   - https://jgraph.github.io/drawio-tools/tools/convert.html?
#
# You can use this cyberchef recipe : https://gchq.github.io/CyberChef/
#
# From_Base64('A-Za-z0-9+/=',false)
# Raw_Inflate(0,0,'Adaptive',false,false)
# URL_Decode()

import argparse
import zlib
import base64
import re
from urllib import parse

import logging
logging.basicConfig(level=logging.ERROR)
log = logging.getLogger(__name__)

def main():
    args = parse_arguments()
    set_logging(args.verbose, args.debug)
    with open(args.input_file, 'r') as fp:
        extract_mxlibrary(fp.read())

def extract_mxlibrary(data):
    """
    'parse' and extract the xml objects from the mxlibrary to check.

    Doesn't actually parse the xml because I don't need the vulnerabilities
    that come with that noise.
    """
    raw_items = re.sub("({\"xml\":\")([^\"]+)(\").*?title\":\"([^\"]+)\"},*", get_decoded, data)
    clean_items = re.sub("[\]]*</*mxlibrary>[\[]*", "", raw_items)
    print(clean_items)

def get_decoded(data):
    decoded = decode_base64_and_inflate(data.group(2))
    title = data.group(4)
    return "\n{0} : {1}\n".format(title, decoded)

def decode_base64_and_inflate(b64string):
    decoded_data = base64.b64decode(b64string)
    decompressed_data = zlib.decompress(decoded_data, -15)
    return parse.unquote(decompressed_data.decode())

def deflate_and_base64_encode(string_val):
    quoted_string = parse.quote(string_val).encode()
    zlibbed_str = zlib.compress(quoted_string)
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode(compressed_string)

# Command Line Functions below this point

def set_logging(verbose=False, debug=False):
    if debug == True:
        log.setLevel("DEBUG")
    elif verbose == True:
        log.setLevel("INFO")

def parse_arguments():
    parser = argparse.ArgumentParser("package name")
    parser.add_argument("--verbose", "-v",
                        help="Turn verbosity on",
                        action='store_true')
    parser.add_argument("--debug", "-d",
                        help="Turn debugging on",
                        action='store_true')
    parser.add_argument("--input_file", "-i",
                        help="Drawio library to parse",
                        required=True)
    args = parser.parse_args()
    return args

def usage():
    print("TODO: usage needed")

if __name__ == '__main__':
    main()
