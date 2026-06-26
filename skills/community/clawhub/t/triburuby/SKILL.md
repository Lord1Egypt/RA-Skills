---
description: Helps users check in rituals, track streaks, and view tribe activity on TribuRuby.
display_name: TribuRuby Training Agent
env:
- description: TribuRuby Agent API key
  name: TRIBURUBY_API_KEY
  required: true
  secret: true
homepage: "https://triburuby.app"
name: triburuby
primaryEnv: TRIBURUBY_API_KEY
tags:
- fitness
- habits
- training
- community
version: 1.0.1
---

# TribuRuby Skill

This skill connects to the TribuRuby platform and helps users:

-   Check in daily rituals
-   Track training streaks
-   View tribe activity
-   Monitor progress in training protocols

Website: https://triburuby.app

------------------------------------------------------------------------

# Authentication

All API calls require:

Authorization: Bearer \${TRIBURUBY_API_KEY}

The API key must be created in TribuRuby under:

Settings → Agent API Keys

------------------------------------------------------------------------

# API Base

https://triburuby.app/api/agent

------------------------------------------------------------------------

# Initialization

Always verify authentication first:

GET /api/agent

If the response contains:

{"error":"Unauthorized"}

tell the user their key is invalid or expired.

------------------------------------------------------------------------

# Available Actions

## Discover Tribes

GET /api/agent?action=my-tribes

Returns all tribes and protocol IDs.

Use this before making tribe-specific calls.

------------------------------------------------------------------------

## Get Training Context

GET
/api/agent?action=context&tribeId=`<id>`{=html}&protocolId=`<id>`{=html}

Returns:

-   ritual list
-   completion status
-   streak count
-   quantities and units

------------------------------------------------------------------------

## Get Tribe Activity

GET
/api/agent?action=tribe-activity&tribeId=`<id>`{=html}&protocolId=`<id>`{=html}

Optional:

&date=YYYY-MM-DD

Shows:

-   tribe members
-   weekly activity
-   current streaks
-   today's check-ins

------------------------------------------------------------------------

## Check In Ritual

POST /api/agent

Body:

{ "action": "check-in", "ritualId": "`<id>`{=html}", "protocolId":
"`<id>`{=html}", "quantity": 45, "date": "YYYY-MM-DD" }

------------------------------------------------------------------------

# Workflow

When helping a user:

1.  Fetch their tribes with `my-tribes`
2.  Determine the relevant `tribeId` and `protocolId`
3.  Retrieve context
4.  Show tribe activity
5.  Offer to check in incomplete rituals

------------------------------------------------------------------------

# Response Style

Keep responses:

-   concise
-   motivating
-   focused on streaks and consistency

Athletes care most about streaks, progress, and accountability.
