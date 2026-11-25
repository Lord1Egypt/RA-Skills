#!/bin/sh
# align markdown table columns (stdout only)
awk -F'|' '{print $1}' "$1"
