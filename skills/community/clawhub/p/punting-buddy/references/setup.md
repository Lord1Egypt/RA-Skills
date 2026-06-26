# Setup

## Goal

Get `punting-buddy` working with The Racing API free plan as quickly as possible.

This setup is only needed for live API-backed answers.
The skill can still be installed, inspected, and used to explain its workflow without credentials.

## What the user needs

- A The Racing API account
- Their The Racing API username
- Their The Racing API password

## Live API env fields

The minimum setup for live data fetches is:

- `THE_RACING_API_USERNAME=...`
- `THE_RACING_API_PASSWORD=...`

Optional but useful defaults:

- `THE_RACING_API_BASE_URL=https://api.theracingapi.com`
- `THE_RACING_API_TIMEOUT_MS=15000`
- `THE_RACING_API_MIN_INTERVAL_MS=1000`

## Setup prompt style

If credentials are missing, keep the reply short and human.

Good example:
- `We are nearly there. First grab your The Racing API access from https://www.theracingapi.com/#subscribe, then add your login details to your env: THE_RACING_API_USERNAME=... and THE_RACING_API_PASSWORD=... Then I can pull the cards properly.`

Avoid:
- raw stack traces
- raw 401 messages
- long setup manuals unless the user asks for detail

## What to say after setup

Once configured, the skill can immediately help with:
- what races are next
- what is on today
- racecard discussion
- runner comparisons
- today's results

## Important note

The skill should be installable even without credentials.
It should guide the user into setup on first real data request rather than failing awkwardly.
If the user is only asking about how the skill works, packaging, or setup itself, do not imply that credentials are already required.
