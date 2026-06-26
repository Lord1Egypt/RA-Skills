#!/bin/bash
# THUQX AutoOps Engine for OpenClaw
# Continuous social media AutoOps for 4 platforms

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

while true
do

 echo "================================="
 echo "THUQX AutoOps cycle starting"
 echo "================================="

 bash "$SCRIPT_DIR/run_social_ops_v5.sh" "$1"

 # random interval 30 min - 2.5 hours
 RANDOM_DELAY=$((RANDOM % 7200 + 1800))

 echo ""
 echo "Next AutoOps cycle in $RANDOM_DELAY seconds"
 echo ""

 sleep $RANDOM_DELAY

 done
