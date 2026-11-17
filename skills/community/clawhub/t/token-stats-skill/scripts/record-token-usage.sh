#!/bin/sh
set -eu
umask 077
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 -I "$script_dir/token_recorder.py" record "$@"
