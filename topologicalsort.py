#!/usr/bin/python3

from collections import deque
import collections, subprocess, glob, sys
from collections import defaultdict
from itertools import takewhile, count

def sort_topologically(graph):
    levels = {}
    names = defaultdict(set)

    def df(a):
        if a in levels:
            return levels[a]
        children = graph.get(a, None)
        level = 0 if not children else (1 + max(df(lname) for lname in children))
        levels[a] = level
        names[level].add(a)
        return level

    for a in graph:
        df(a)

    return list(takewhile(lambda x: x is not None, (names.get(i, None) for i in count())))

if __name__ == '__main__':
    for file in glob.glob(sys.argv[1] + "/*.wdf"):
        fp= open(file)
        content = fp.read()
        print(content)
    st1, st2 = content.split('%%')

    lines= st1.split('\n')
    del lines[-1]

    dict1= {}
    for line in lines:
        a1, a2 = line.split(':')
        dict1.__setitem__(a1, a2)
    dict1 = collections.OrderedDict(sorted(dict1.items()))
    print(dict1)

    st2 = st2.replace(' ','')
    lines2 = st2.split('\n')
    del lines2[-1]
    del lines2[0]

    dict2 = {}
    for line in lines2:
        a1, a2 = line.split('=>')
        dict2.setdefault(a2, [])
        dict2[a2].append(a1)

    diff = set(dict1.keys())^set(dict2.keys())
    for a in diff:
        dict2.setdefault(a, [])

    dict2 =collections.OrderedDict(sorted(dict2.items()))
    print(dict2)

    topo = sort_topologically(dict2)
    print("HEREEE")
    print(topo)

    for a in topo:
        for b in a:
            dict1[b] = dict1[b].lstrip(' ')
            subprocess.getoutput("python3 " + sys.argv[1] +"/"+ dict1[b])



