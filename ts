#!/usr/bin/env python3

"""
      .
. \x1b[1;31mtimesheet\x1b[0m .
      .

Time tracker app

Usage:
  timesheet start <tag>
  timesheet end <tag>
  timesheet cancel <tag>
  timesheet status
  timesheet tags
  timesheet history [tag]

Options:
  -h --help         Show this screen
  -v --version      Show version info
"""

from docopt import docopt
from pprint import pprint
from timesheet import lib

filename = "data.db"

def do_categories():
	pass

def main():
	args = docopt(__doc__, options_first=True, version="\x1b[1;31monx\x1b[0m.alpha.2020.05.09.0")
	
	# pprint(args)
	db = lib.open_db(filename)

	if args['start']:
		# pprint(args)
		lib.start_entry(db, args['<tag>'])
	elif args['end']:
		lib.end_entry(db, args['<tag>'])
	elif args['cancel']:
		lib.cancel_entry(db, args['<tag>'])
	elif args['status']:
		lib.status(db)
	elif args['tags']:
		lib.get_tags(db)
	elif args['history']:
		lib.history(db)
	else:
		print("__doc__")
    

if __name__ == "__main__":
    main()