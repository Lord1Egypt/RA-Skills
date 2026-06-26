#!/bin/bash
pkill -f monitor_web.py 2>/dev/null
sleep 1
cd /home/fangjinan/.openclaw/workspace/skills/video-note-maker
python3 monitor_web.py
