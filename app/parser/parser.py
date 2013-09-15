#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter, LTChar
from pdfminer.layout import LAParams
from cStringIO import StringIO
from collections import defaultdict, OrderedDict
import re

def to_dict(data, header):
    return {header[key]: value for (key, value) in enumerate(data)}

class ListConverter(TextConverter):
        def __init__(self, *args, **kwargs):
            TextConverter.__init__(self, *args, **kwargs)

        def end_page(self, i):
            lines = defaultdict(lambda : {})
            for child in self.cur_item._objs:
                if isinstance(child, LTChar):
                    (_,_,x,y) = child.bbox
                    line = lines[int(-y)]
                    line[x] = child._text.encode(self.codec)

            for y in sorted(lines.keys()):
                line = lines[y]

                od = OrderedDict(sorted(line.items()))
                last = None
                cols = []
                temp_str = ""
                for k, v in od.iteritems():
                    if not last:
                        last = k
                    dist = k - last 
                    if v != "":
                        if dist > 10:
                            cols.append(temp_str)
                            temp_str = v
                        else:
                            temp_str += v
                    last = k
                cols.append(temp_str)

                try:
                    cols[0]  = int(cols[0])
                except ValueError, e:
                    first = cols.pop(0)
                    match = re.match(r"(\d+)(.+)", first, re.I)
                    if match:
                        cols.insert(0, int(match.groups()[0]))
                        cols.insert(1, match.groups()[1])
                    else:
                         cols.insert(0, first)
                self.outfp.append(cols)

def parse_list(fp):
    if type(fp) is str:
        fp = open(fp, 'rb')

    rsrc = PDFResourceManager()
    res = []
    device = ListConverter(rsrc, res, codec="utf-8",  laparams=LAParams())
    process_pdf(rsrc, device, fp)
    fp.close()
    header = res.pop(0)
    data = [product for product in res if len(product) == len(header)]
    not_parseable = ["; ".join([str(col) for col in prod]) for prod in res if len(prod) != len(header)]
    products = [to_dict(elem, header) for elem in data]
    return (products, header, not_parseable)