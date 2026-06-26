#!/bin/bash
# Quick snapshot script
# Usage: ./snapshot.sh

cd "$(dirname "$0")"
/usr/bin/python3.10 motion_detector.py --snapshot