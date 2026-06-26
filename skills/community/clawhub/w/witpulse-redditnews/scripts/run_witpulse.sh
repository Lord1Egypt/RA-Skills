#!/bin/bash
# ~/.agents/skills/WitPulse-redditnews/scripts/run_witpulse.sh
python3 ~/.agents/skills/WitPulse-redditnews/scripts/fetch_reddit.py
python3 ~/.agents/skills/WitPulse-redditnews/scripts/curator.py
