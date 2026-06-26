---
name: stickyhive
description: Manage communities, schedule posts, automate workflows, and run DM sequences across Skool, Circle, Mighty Networks, Discord, and Slack via the stickyhive CLI. Use when the user asks about community management, post scheduling, workflow automation, DM sequences, or member engagement.
---

# StickyHive Agent Skill

Manage communities, schedule posts, automate workflows, and run DM sequences across platforms like Skool, Circle, Mighty Networks, Discord, and Slack — all from the CLI.

## Setup

```bash
npm install -g stickyhive
export STICKYHIVE_API_KEY=hm_live_...  # Get from StickyHive dashboard → Settings → API Keys
# Optional: export STICKYHIVE_API_URL=https://app.stickyhive.com
```

## Commands

### Communities

```bash
stickyhive communities:list                  # List all communities
stickyhive communities:get <id>              # Get community details and spaces
```

### Spaces

```bash
stickyhive spaces:list                       # List all posting destinations
stickyhive spaces:get <id>                   # Get space details
```

### Scheduled Posts

```bash
# Create & manage
stickyhive posts:create -t "Title" -c "Body content" -i <spaceId> [-s "2026-06-01T09:00:00Z"] [--pin] [--comment "First!"] [--poll '["Option A","Option B"]']
stickyhive posts:list [--status pending|published|failed] [--draft] [--spaceId 42] [--dateFrom "2026-01-01"] [--dateTo "2026-12-31"]
stickyhive posts:get <id>
stickyhive posts:update <id> -d '{"title":"New title","content":"New body"}'
stickyhive posts:delete <id>

# Scheduling actions
stickyhive posts:reschedule <id> -s "2026-07-01T09:00:00Z"
stickyhive posts:publish <id>                # Publish immediately
stickyhive posts:bulk-schedule --ids "1,2,3" --startTime "2026-06-01T09:00:00Z" --interval 2
```

### Workflows (Automation Rules)

```bash
stickyhive workflows:list -C <communityId>
stickyhive workflows:get <id> -C <communityId>
stickyhive workflows:create -C <communityId> -n "Welcome new members" --config '{"trigger":{"type":"member.joined"},"actions":[{"type":"send_dm","config":{"message":"Welcome!"}}]}'
stickyhive workflows:update <id> -C <communityId> -d '{"name":"Updated name","daily_limit":100}'
stickyhive workflows:delete <id> -C <communityId>
stickyhive workflows:toggle <id> -C <communityId>      # Enable/disable
stickyhive workflows:run <id> -C <communityId>          # Manual trigger
stickyhive workflows:runs <id> -C <communityId> [--limit 20]  # Run history
stickyhive workflows:test <id> -C <communityId> [--triggerData '{"member":{"name":"Test"}}']  # Dry run
stickyhive workflows:registry [--platform skool]         # Available triggers, actions, conditions
```

### DM Sequences

```bash
stickyhive sequences:list -C <communityId>
stickyhive sequences:get <id> -C <communityId>
stickyhive sequences:create -C <communityId> -n "Onboarding" [--description "..."] [--steps '<JSON>']
stickyhive sequences:update <id> -C <communityId> -d '{"name":"Updated"}'
stickyhive sequences:delete <id> -C <communityId>
stickyhive sequences:toggle <id> -C <communityId>       # Enable/disable

# Enrollment management
stickyhive sequences:enroll <sequenceId> -C <communityId> -m <memberId>
stickyhive sequences:enrollments <sequenceId> -C <communityId> [--status active|paused|completed]
stickyhive sequences:manage-enrollment --sequenceId <id> --enrollmentId <id> -C <communityId> -a pause|resume|cancel

# Discovery
stickyhive sequences:step-types              # Available step types for building sequences
```

### Webhooks

```bash
stickyhive webhooks:list
stickyhive webhooks:create -u "https://example.com/hook" -e "post.published,member.joined"
stickyhive webhooks:delete <id>
```

## Notes

- All commands output structured JSON.
- Dates use ISO 8601 format (e.g. `2026-06-01T09:00:00Z`).
- The `communityId` (`-C`) flag is required for workflows and sequences — get it from `communities:list`.
- Use `posts:create` without `--date` to save as a draft.
- Workflow configs define trigger → condition → action pipelines. Use `workflows:registry` to discover available types.
