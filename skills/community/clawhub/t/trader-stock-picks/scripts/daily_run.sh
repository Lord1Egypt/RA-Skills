#!/usr/bin/env bash
# Daily stock recommendation runner
# Called by cron at 8:30 AM Beijing time
# This script generates the prompt for the agent to execute the daily stock screening
echo "Daily stock recommendation triggered at $(date)"
echo "Time (Beijing): $(TZ=Asia/Shanghai date)"
echo ""
echo "The agent will be called with the daily stock screening task."
