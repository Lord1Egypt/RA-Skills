#!/bin/bash
set -x
cd ~/.openclaw/workspace/skills/reading-manager
ls -la SKILL.md
clawhub publish . --version "1.0.0" --slug reading-manager --name "Reading Manager" 2>&1
