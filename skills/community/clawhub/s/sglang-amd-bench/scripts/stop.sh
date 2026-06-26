#!/bin/bash
#
# Stop sglang server (kill matching processes inside this container).
# Use verify_stop.sh on the host afterwards to confirm GPUs are free.
#
# Usage:
#   bash stop.sh
#

set -eu

echo "Stopping sglang server..."
ps -ef | grep -i sglang | grep -v grep | awk '{print $2}' | xargs -r kill -9
sleep 6
echo "Done. Now run verify_stop.sh on the HOST to confirm GPUs are released."
