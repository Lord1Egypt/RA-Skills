#!/usr/bin/env bash

# This script registers the background cron job for the Temporal KG Synthesizer
# It will run at 3 AM daily to parse logs from the previous day without interrupting active sessions.

openclaw cron add \
  --name "Temporal KG Synthesis" \
  --cron "0 3 * * *" \
  --session isolated \
  --message "Synthesize the temporal knowledge graph. Parse our recent daily logs and construct relationship mappings."

echo "Cron job 'Temporal KG Synthesis' successfully registered."
