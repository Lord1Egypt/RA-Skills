#!/usr/bin/env sh
set -eu

if [ "$#" -ne 0 ]; then
  printf '%s\n' '{"contractVersion":"1.0","status":"error","error":{"code":"arguments_not_allowed","message":"Read one JSON request from stdin."}}'
  exit 2
fi

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
exec node "$script_dir/invoke.mjs"
