#!/bin/bash
#
# Verify GPUs are free using rocm-smi --showpids. MUST run on the HOST
# (not inside docker) so PIDs in sibling containers are visible.
#
# Usage:
#   bash verify_stop.sh           # local host
#   ssh <node> bash -s < verify_stop.sh   # remote host
#
# Exit 0: no KFD PIDs. Exit 1: PIDs still holding GPUs (printed to stderr).
#

set -eu

OUT=$(rocm-smi --showpids 2>&1)

if echo "$OUT" | grep -q "No KFD PIDs currently running"; then
  echo "OK: No KFD PIDs currently running."
  exit 0
fi

echo "FAIL: GPU PIDs still alive:" >&2
echo "$OUT" >&2
exit 1
