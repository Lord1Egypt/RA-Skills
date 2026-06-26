# China Service Readiness Notes

Use this reference when the user specifically mentions:

- QQ Music
- NetEase Cloud Music
- Chinese room names or service names
- a just-finished login flow

## Key state model

Do not collapse these states into one:

1. `service_visible`
2. `service_linked_in_sonos`
3. `zonefoundry_ready`

Important implication:

- Sonos being able to show or even play a service does not automatically prove local ZoneFoundry readiness

## Mobile-only rule

If the user only has a phone:

- guide service add/login through the official Sonos iOS / Android app
- do not promise persistent local bot control
- do not treat this as a user error

## `service list` interpretation

The most important fields are `tokenReady` and `nextAction`.

- `tokenReady=yes`: ZoneFoundry already has a usable local token or ready state
- `tokenReady=no`: ZoneFoundry does not yet have enough local readiness to continue directly
- `linked`: conservative hint only, not authoritative Sonos account truth
- `nextAction`: preferred routing hint for the next safe step

Correct rule:

- never reject the user only because one field looks like "not linked"

## Recommended probe

Use a real readiness check:

```bash
zf doctor service --service "QQ音乐" --query "郑秀文" --format json
zf doctor service --service "网易云音乐" --query "陈奕迅" --format json
```

## Routing rule

Prefer runtime hints over hard-coded service stories.

If `nextAction=ready`:

- proceed to playback

If `nextAction=begin_link`:

```bash
zf auth smapi begin --service "<service>" --format json
```

If `pendingLink=true` or `nextAction=complete_link`:

- resume `complete`
- do not restart from zero unless the pending flow is definitely invalid

```bash
zf auth smapi complete --service "<service>" --wait 2m --format json
```

For NetEase Cloud Music examples:

```bash
zf auth smapi begin --service "网易云音乐" --format json
zf auth smapi complete --service "网易云音乐" --wait 2m --format json
```

Public skill copy should not assume every household or build uses the same behind-the-scenes path for QQ Music or other China services. Follow `zf doctor service`, `nextAction`, and actual runtime readiness instead of hard-coding one explanation.

## New-session rule

If the user comes back and says:

- "done"
- "complete"
- "已经绑好啦"
- "我登录好了"

prefer resuming the local completion flow instead of repeating onboarding questions.
