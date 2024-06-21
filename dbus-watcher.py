#!/usr/bin/python3

import os
import sys
import dbus
import gi

from gi.repository import GLib

from dbus.mainloop.glib import DBusGMainLoop

types = [ "invalid", "method_call", "method_return", "error", "signal" ]

actions = []
deferred_actions = {}


def my_filter(bus, message):

	global deferred_actions

	#path = message.get_path()
	#type = types[message.get_type()]
	#sender = message.get_sender()
	member = message.get_member()
	serial = message.get_serial()
	args_list = message.get_args_list()
	interface = message.get_interface()
	#error_name = message.get_error_name()
	#destination = message.get_destination()
	reply_serial = message.get_reply_serial()

	if reply_serial in deferred_actions:
		print(deferred_actions[reply_serial])
		exec( deferred_actions[reply_serial] )
		del	  deferred_actions[reply_serial]

	for item in actions:

		conditions, action = item
		match = True
		defer = False

		for cond in conditions:
			if cond == "wait_reply":
				defer = True
				continue
			if not eval(cond):
				match = False
				break

		if match:
			if defer:
				deferred_actions[serial] = action
			else:
				print(action)
				exec(action)


try:
	configfile=os.environ.get("HOME")+"/.dbus-watcher-config.py"
	exec(open(configfile,"r").read())
except IOError:
	pass


dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()

bus.add_message_filter(my_filter)
bus.add_match_string("")

GLib.MainLoop().run()

