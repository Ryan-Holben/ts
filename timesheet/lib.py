import dataset as ds
# from pprint import pprint
from time import time, strftime, gmtime, localtime, ctime
from collections import OrderedDict

entry_keys = ['id', 'tag', 'start', 'end']

def red(string):
    return "\x1b[1;31m" + string + "\x1b[0m"

def open_db(filename):
    """Open a database connection, build up the tables if needed, return the object"""
    db = ds.connect("sqlite:///" + filename)
    db['active']
    db['history']
    return db

def get_tags(db):
    active = db['active']
    history = db['history']
    tags = set()
    for r in active.distinct('tag'):
        tags.add(r['tag'])
    for r in history.distinct('tag'):
        tags.add(r['tag'])

    print("Timesheet has tracked " + red(str(len(tags))) + " tags:")
    for t in tags:
        print("\t" + red(t))


def contains_tag(table, tag):
    return table.find_one(tag=tag) is not None

def start_entry(db, tag):
    table = db['active']
    if contains_tag(table, tag):
        print("The activity " + red(tag) + " is already running.")
        exit()
    e = OrderedDict.fromkeys(entry_keys)
    e.tag = tag
    e.start = time()
    e.end = float(-1)
    table.insert(e.__dict__)
    print("Started tracking " + red(tag) + ".")

def end_entry(db, tag):
    table = db['active']
    r = table.find_one(tag=tag)
    if not r:
        print("The activity " + red(tag) + " is not in progress.")
    else:
        r['id'] = None
        r['end'] = time()
        table.delete(tag=tag)
        table = db['history']
        table.insert(r)
        print("Finished working on " + red(tag) + ".")

def cancel_entry(db, tag):
    table = db['active']
    r = table.find_one(tag=tag)
    if r:
        table.delete(tag=tag)
        print("Canceled the activity " + red(tag) + ".")
    else:
        print("The activity " + red(tag) + " is not in progress.")

def status(db):
    table = db['active']
    now = time()
    n = len(table)
    if n == 0:
        print("There are " + red(str(n)) + " tasks active.")
        exit()
    print("Currently tracking " + red(str(n)) + " tasks:")
    for r in table:
        print("\tYou have been " + red(r['tag']) + " for " + strftime("%H:%M:%S", gmtime(now - r['start'])) + ".")

def sec_to_hms(sec):
    h = int(sec / 3600)
    m_remaining = sec % 3600
    m = int(m_remaining / 60)
    s = int(m_remaining % 60)
    return "{:02d}:{:02d}:{:02d}".format(h, m, s)

def history(db):
    table = db['history']
    for r in table:
        print("\tOn " + strftime("%d/%m/%Y %H:%M:%S", gmtime(r['start'])) + ": " + red(r['tag']) + " lasted " + sec_to_hms(r['end'] - r['start']) + ".")

def summary(db):
    table = db['history']
    totals = {}
    for r in table:
        dt = r['end'] - r['start']
        totals[r['tag']] = totals[r['tag']] + dt if r['tag'] in totals else dt
    totals = {k: v for k, v in sorted(totals.items(), key=lambda item: item[1], reverse=True)}
    print("Your total times are:")
    for k in totals:
        print("\t" + red(k) + ": " + str(sec_to_hms(totals[k])))

