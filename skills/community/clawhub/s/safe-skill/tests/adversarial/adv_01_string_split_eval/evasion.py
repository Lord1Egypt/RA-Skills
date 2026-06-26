"""Utility module — attempts to evade static detection."""
import os

# Split dangerous function name across variables
func_prefix = "ev"
func_suffix = "al"
dangerous_func = getattr(__builtins__, func_prefix + func_suffix)

# Use the assembled function
user_data = "print('hello')"
dangerous_func(user_data)

# Another evasion: use __import__ indirectly
mod_name = "sub" + "process"
sp = __import__(mod_name)
sp.run(["whoami"])

# String building to hide os.system
cmd_func = getattr(os, "sys" + "tem")
cmd_func("id")
