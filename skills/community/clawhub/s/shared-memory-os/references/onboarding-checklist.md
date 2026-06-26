# Onboarding Checklist

Use this checklist when a new agent/robot joins a workspace that already uses Shared Memory OS.

## Startup
1. Read `SOUL.md`
2. Read `USER.md`
3. Read today and yesterday daily files if present
4. In direct/private main sessions, read `MEMORY.md`
5. Read `memory/active-thread.md` and `memory/current-state.md`
6. Read `memory/index.md` only if routing help is needed
7. Do not read `memory/private-secrets.md` unless the task explicitly requires secret lookup or credentialed action

## Behavioral contract
- Do not invent a parallel memory system
- Use the existing tiers: HOT / DAILY / WARM / RESTRICTED / CONTROL
- Write facts to daily first unless the correct target is already obvious
- Load WARM files only on context match
- Respect privacy boundaries around `MEMORY.md`
- Treat `private-secrets.md` as restricted and opt-in, not default memory

## Write routing
- Stable preference → `MEMORY.md`
- Current main line of work → `memory/active-thread.md`
- Current front-of-mind status → `memory/current-state.md`
- Recent active theme → `memory/recent-focus.md`
- High-frequency alias / fuzzy trigger → `memory/trigger-map.md`
- Proven good collaboration pattern → `memory/success-patterns.md`
- Default learned behavior → `memory/default-behaviors.md`
- User evaluation / feedback pattern → `memory/feedback-model.md`
- Ongoing project → `memory/projects/*.md`
- Tradeoff decision → `memory/decisions.md`
- Reusable workflow → `memory/routines.md`
- Explicit mistake / lesson → `memory/corrections.md`
- Skill release state → `memory/skill-release-state.md`
- Secrets that truly must be remembered → `memory/private-secrets.md`
- System-level learning / evolution → `memory/evolution-log.md`
- Temporary unsorted item → `memory/inbox.md`

## Maintenance
- Follow `HEARTBEAT.md`
- Update `memory/heartbeat-state.md` only when real maintenance occurred
- Use weekly/monthly review docs for heavier cleanup
