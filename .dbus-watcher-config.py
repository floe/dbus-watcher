actions = [
	(
		[ "interface=='org.gnome.ScreenSaver'", "member=='ActiveChanged'", "args_list[0]==True" ],
		"os.system('office_light.sh turn_off')"
	),(
		[ "interface=='org.gnome.ScreenSaver'", "member=='ActiveChanged'", "args_list[0]==False" ],
		"os.system('office_light.sh turn_on')"
	)
]

print(actions)
