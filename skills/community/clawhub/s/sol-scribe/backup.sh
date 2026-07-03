#!/bin/bash
# Daily SolScribe backup — runs at 2am every day
# Backs up book state, chapters, and pushes to GitHub
cd ~/Projects/solscribe
python3 -c "from solscribe import backup; backup('Daily backup')" 2>> ~/Projects/solscribe/backups/backup.log
