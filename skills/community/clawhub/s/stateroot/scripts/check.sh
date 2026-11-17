#!/bin/sh
# StateRoot marketplace skill — status only. Never writes. No prompts.
# Prints which bootstrap step is next, or "expire" when the built-in skill
# should take over.
set -eu

printf 'stateroot-bootstrap:\n'

if ! command -v stateroot >/dev/null 2>&1; then
	printf '  cli: missing\n'
	printf '  next: install\n'
	exit 0
fi

version="$(stateroot --version 2>/dev/null || printf unknown)"
printf '  cli: %s (%s)\n' "$(command -v stateroot)" "$version"

config_home="${STATEROOT_HOME:-${HOME}/.config/stateroot}"
if [ -d "${HOME}/.stateroot" ] || [ -f "${config_home}/config.toml" ]; then
	printf '  machine: setup/config present\n'
	machine_ready=1
else
	printf '  machine: no ~/.stateroot/ or config.toml (setup has not run)\n'
	machine_ready=0
fi

if [ -d .stateroot ]; then
	printf '  project: .stateroot/ present\n'
else
	printf '  project: no .stateroot/ (init only if this repo should be a StateRoot project)\n'
fi

if [ "$machine_ready" -eq 0 ]; then
	printf '  next: setup\n'
	exit 0
fi

printf '  next: expire — follow the built-in skill (`stateroot skill show stateroot`)\n'
if [ ! -d .stateroot ]; then
	printf '  note: run `stateroot init` first if this directory should be a project store, then expire\n'
fi
