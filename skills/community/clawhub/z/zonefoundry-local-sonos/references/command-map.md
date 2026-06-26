# Command Map

Prefer JSON output and stable machine-readable commands.

## Skill/runtime update

```bash
clawhub update zonefoundry-local-sonos
zf update self --check --format json
```

## Preflight

```bash
zf update self --check --format json
zf setup --format json
zf doctor --format json
zf discover --format json
zf config get defaultRoom
zf service list --format json
zf config get defaultService
zf doctor service --service "Spotify" --query "Miles Davis" --format json
zf auth smapi complete --service "Spotify" --wait 2m --format json
```

## Direct control

```bash
zf execute --data '{"action":"status","target":{"room":"Office"}}'
zf execute --data '{"action":"pause","target":{"room":"Office"}}'
zf execute --data '{"action":"next","target":{"room":"Office"}}'
zf execute --data '{"action":"volume.set","target":{"room":"Office"},"request":{"volume":20}}'
```

## Playback (global examples)

```bash
zf play music "Taylor Swift" --format json
zf play music "Adele" --enqueue --format json
zf play music "Miles Davis" --enqueue --limit 5 --format json
zf play music "黎明 夏日傾情" --service "Apple Music" --format json
zf play music "黎明" --enqueue --service "Apple Music" --limit 5 --format json
zf queue list --name "Office" --format json
zf queue remove 3 --name "Office"
```

## Playback (China service examples)

```bash
zf play music "周杰伦" --service "网易云音乐" --format json
zf play music "郑秀文" --enqueue --service "QQ音乐" --limit 5 --format json
zf play music "郑秀文 舍不得你" --service "QQ音乐" --format json
zf ncm lucky --name "客厅" "郑秀文" --format json
zf smapi search --name "客厅" --service "QQ音乐" --category tracks --open --index 1 --format json "周杰伦"
```

## Insert / announcement

```bash
zf say "<text>" --name "<room>" --mode queue-insert --format json
```

## Recovery

```bash
zf queue heal --name "Office" --timeout 15s --settle 2s --fallback-window 5 --format json
zf group rebuild --name "Office" --via "Kitchen" --format json
```

## China service readiness

```bash
zf doctor service --service "QQ音乐" --query "郑秀文" --format json
zf auth smapi begin --service "QQ音乐" --format json
zf auth smapi complete --service "QQ音乐" --wait 2m --format json
```

## Playback routing note

- For Apple Music and QQ Music playback, prefer `zf play music` first.
- Do not require browser-style `auth smapi begin/complete` before every Apple Music or QQ Music play request.
- Use `auth smapi ...` only when the user is explicitly trying to link an account or when diagnostics require it.

## Recovery rules

- `queue heal` is the preferred single-room recovery attempt.
- `group rebuild` is a stronger helper-room recovery path.
- `--restore-reltime` is experimental and should not be the default path.
