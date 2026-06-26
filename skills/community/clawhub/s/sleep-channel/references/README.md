# Sleep Tracking System

## Overview
This system tracks sleep-related events and renders a formatted sleep log.

## Current Layout

### Data
- `data/sleep_log.csv` — canonical sleep event log
- `state/sleep_summary_state.json` — message/state tracking for the rendered summary

### Scripts
- `scripts/tracker.py` — add/correct/delete/render sleep entries

## Core Principles
- Use the actual log file as the source of truth
- Use source Discord message timestamps for event times unless the user gives an explicit time
- Convert displayed times to the configured timezone (`SLEEP_TIMEZONE`)
- Never use `now` as a logged time
- Never invent entries, dates, or corrections

## Typical Usage
- add a new sleep event
- correct the latest sleep event
- delete the latest sleep event when explicitly requested
- render the current formatted sleep log from file
