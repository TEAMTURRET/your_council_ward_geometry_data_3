#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import requests
import scraperwiki.sqlite as db

import csv
import scraperwiki

#--via @mhawksey
# query string crib https://views.scraperwiki.com/run/python_querystring_cheat_sheet/?
import cgi, os
qstring=os.getenv("QUERY_STRING")

PARENT_ID = 33895# Barking and Dagenham

key=2502 #AI (@nuttyxander) Use Hammersmith as a default, make it local!

if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'key' in get: key=get['key']
#---

PARENT_ID = key

def iter_children_areas_kml(parent_id):
    children = getjs('http://mapit.mysociety.org/area/%s/children' % parent_id)
    for id, data in children.items():
        kml = requests.get('http://mapit.mysociety.org/area/%s.kml' % id).content
        entry = {'parent_area': int(data['parent_area']),
                 'id': int(id),
                 'name': data['name'],
                 'kml': kml}
        yield entry


def getjs(url, **opts):
    return json.loads(requests.get(url, **opts).content)


#
# Main
#
data = list(iter_children_areas_kml(PARENT_ID))
db.save(['id'], data, verbose=0)

with open("newfile.csv",'wb') as f:
    writer = csv.DictWriter(f, delimiter='\t', fieldnames="parent_area,id,name,kml")
    writer.writerows(data)

scraperwiki.utils.httpresponseheader("Content-Type", "text/plain")
print data