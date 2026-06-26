---
name: read-policy
description: Read OpenClaw policies from PostgreSQL through the local Supabase Docker stack. Use for inspecting policy keys such as auto_approve, priority_routing, or available_skills.
metadata: {"clawdbot":{"notes":["Reads public.openclaw_policies through docker exec on supabase-db"]}}
---

# Read Policy

Read policy values from the real OpenClaw database.

## Commands

- Read one policy key  
  `{baseDir}/scripts/read-policy.sh get "auto_approve"`

- List all policy keys  
  `{baseDir}/scripts/read-policy.sh list`

## Notes

- Uses the local Docker container `supabase-db`
- Reads from `public.openclaw_policies`
- Intended for inspection only
