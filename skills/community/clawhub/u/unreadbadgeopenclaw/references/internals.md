# Internals: how sidebar marks actually render and clear

> **Language index / 语言索引 / 語言索引 / 언어 색인 / Языковой указатель / 言語インデックス / Índice de idiomas / Index des langues**
>
> This reference is maintained in English (below). One-line summaries in 8 languages:
>
> - **English** — Source-level notes on how the Control UI renders and clears session unread marks.
> - **简体中文** — 从 Control UI 源码层面分析未读标记的渲染链与全部清除点。
> - **繁體中文** — 從 Control UI 原始碼層面分析未讀標記的渲染鏈與全部清除點。
> - **한국어** — Control UI 소스 수준에서 읽지 않음 표식의 렌더링 경로와 모든 제거 지점을 분석합니다.
> - **Русский** — Анализ на уровне исходного кода Control UI: цепочка отрисовки и все точки снятия метки.
> - **日本語** — Control UI のソースレベルで、未読マークの描画経路とすべての解除ポイントを分析します。
> - **Español** — Análisis a nivel de código fuente de Control UI: cadena de renderizado y todos los puntos de borrado.
> - **Français** — Analyse au niveau du code source de Control UI : chaîne de rendu et tous les points d'effacement.

## Sidebar subtitle render chain

The session-row subtitle resolves with this priority:

```
attentionNote ?? agentStatusNote ?? runHeadline ?? messagePreview ?? subtitle
```

`attentionNote` is the note stored inside `agentStatus` when an `attention`
icon is set. The catch: when the operator disables **"Show message preview"**
in sidebar settings, the subtitle branch collapses to
`attentionNote ?? headline` — the plain `agentStatusNote` and the message
preview are never rendered.

The `attention` **icon** is resolved through a separate leading-indicator
channel that renders regardless of that setting. Conclusion: **a mark without
an icon is invisible for anyone who turned message previews off.** Always set
`attention` alongside `statusNote`.

## Icon vocabulary

Valid attention ids (anything else is rejected by the gateway):

| id | semantics |
|---|---|
| `flag` | neutral notice — use for "reply completed" |
| `alert` | warning — reserve for confirmed failures |
| `hand` | raise hand / attention |
| `key`, `lock`, `hourglass` | specialty states |

The icon resolution is duration-aware: it checks `expiresAt` against now, so
an expired mark disappears from the UI even if the record still exists.

## All clearing points (debug "vanishing marks" against these)

1. **Read-clear**: opening the session (focusing its input) issues
   `sessions.patch {unread:false}` which stamps `lastReadAt = now` and
   **deletes the whole `agentStatus`**.
2. **New-turn clear**: when the operator sends a new message that starts a
   turn, the reply pipeline resets `agentStatus` for that session
   (`agentStatus: isSystemEvent ? base?.agentStatus : void 0` — heartbeat/cron
   system events keep it, user messages clear it). Marks set *after* the turn
   completes are of course unaffected.
3. **TTL expiry**: `ttlMinutes` clamps to 1–120; the UI honors `expiresAt`.
4. **Keep-alive 7-day fallback** (this skill): unconditional clear.

Timestamps in gateway logs are UTC — convert before comparing with local
`HH:mm` values embedded in notes.

## Patch semantics worth knowing

- `sessions.patch` with `{unread:false}` is the read-clear path (deletes
  agentStatus).
- Sending `attention: null` as part of a patch hits a dedicated clear branch
  for the icon while other fields still apply.
- Omitting `attention` **inherits** the previous value
  (`rawAttention ?? current?.attention`). The safe pattern when changing
  icons: overwrite the entire agentStatus in one patch (icon + note + ttl) —
  the old icon cannot survive because the whole object is replaced.
- CLI `gateway call` always exits 0; validate `"ok":false` in the response body.

## Verification playbook

- **RPC**: `openclaw gateway call sessions.list --params '{"limit":300}'` —
  inspect `agentStatus` (`note` / `attention` / `expiresAt`), `unread`,
  `lastReadAt` for the target key.
- **Timing**: `lastReadAt > markCreated` ⇒ the operator read it; expect the
  mark to be gone.
- **Windows + PowerShell**: pass JSON via `execFileSync` args array (Node) or
  call `node script.js` directly — `Start-Process` in PS 5.1 splits arguments
  on spaces and eats inner quotes, silently truncating notes like
  `[New reply] 14:21` down to `[New reply]`.

## Resurrecting-badge bug (fixed in 1.1.1)

The gateway owns the mark. A keep-alive that decides "unread" from read
bookkeeping alone can re-create a mark the gateway already cleared:

- Wrong order: `lastReadAt > created` first, then a weak
  `!agentStatus && unread === false` check. When the operator opened the
  session at (or milliseconds before) the mark was written, `lastReadAt` was
  not greater than `created`, so the cleared mark was judged unread and renewed
  on the next 90-minute cycle — the badge "came back" after being read.
- Correct rule: **missing `agentStatus` always wins** → drop the record and
  never patch. Only a mark still present on the gateway, and not yet read,
  is renewed.

Verify with `sessions.list` (`agentStatus` present?) instead of trusting a
local timestamp comparison.

## Cadence math

Gateway TTL cap: 120 min. Keep-alive every 90 min renews marks before they
visibly expire (renewal re-stamps a fresh 120 min). Marks whose session was
read in between are dropped from the state file, so renewal never resurrects
a read mark.
