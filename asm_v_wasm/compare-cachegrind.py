#!/usr/bin/env python

import math
import sys
import collections

def diff(a, b):
    r = 100. * (float(a) - float(b)) / float(a)
    if math.abs(r) < 0.01:
        return 0
    return math.ceil(r*100) /100.

results = collections.OrderedDict()
file_name = sys.argv[1]
with open(file_name, 'r') as f:
    for line in f.readlines():
        sp = [l.replace(',','') for l in line.split(' ') if len(l) > 0]

        name = sp[0]

        b_ic = int(sp[1])
        b_dr = int(sp[2])
        b_dw = int(sp[3])

        a_ic = int(sp[5])
        a_dr = int(sp[6])
        a_dw = int(sp[7])

        name = name[len("wasm_"):] if name.startswith("wasm_") else name
        name = name[len("lua_"):] if name.startswith("lua_") else name
        name = name[:-len(".js")]

        results[name] = [diff(b_ic, a_ic),
                    diff(b_dr, a_dr),
                    diff(b_dw, a_dw)]

longest_name_len = reduce(max, map(len, results.keys()))
def fill(name):
    if len(name) < longest_name_len:
        name += "".join([ ' ' for i in range(longest_name_len - len(name))])
    return name

print("{} icount\td-read\td-writes".format(fill("name")))
for k, [a,b,c] in results.iteritems():
    print("{} {}\t{}\t{}".format(fill(k), a, b, c))
