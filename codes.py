#!/usr/bin/env python

from yaml import load

with open("status-codes.yml") as codes:
    codes = load(codes)
    for code, detail in codes.iteritems():
        print code
        print detail['category']
        print detail['reason']
        print detail['explanation']
