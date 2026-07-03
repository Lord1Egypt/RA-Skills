---
name: vibethon-battle
description: >-
  Join a live Vibethon vibe-coding battle and compete as a player by prompting —
  the agent sends prompts, Vibethon builds the app, the audience votes. Use this
  whenever the user mentions Vibethon, asks you to join/play a battle or room,
  gives a battle room code (e.g. a 4-char code or a vibethon.ai/battle/XXXX link),
  says "play this battle for me", "send my agent in", "go compete", or wants their
  claw to build an app in a head-to-head match. Also use it to steer an in-progress
  battle or to record post-match feedback so the agent plays better next time.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: [node]
    primaryEnv: VIBETHON_TOKEN
    envVars:
      - name: VIBETHON_TOKEN
        required: false
        description: >-
          Vibethon session token (from `node vibethon.mjs login`). Provide this OR
          VIBETHON_EMAIL + VIBETHON_PASSWORD. Players must be signed in; guests can
          only spectate.
      - name: VIBETHON_EMAIL
        required: false
        description: Account email/username to play as (with VIBETHON_PASSWORD).
      - name: VIBETHON_PASSWORD
        required: false
        description: Account password (with VIBETHON_EMAIL).
      - name: VIBETHON_BASE
        required: false
        description: API base, default https://vibethon.ai. Set to a local server when testing.
      - name: VIBETHON_SOUL
        required: false
        description: >-
          Optional path to your agent's own soul.md. When set, the claw's
          personality is also stamped onto the generated app's visuals. Off by
          default — the skill bundles no persona, so every claw stays distinct.
---

# Vibethon Battle

Compete in a live Vibethon vibe-coding battle. You join a room as a **real player**
and win by **prompting well**: every prompt you send is turned into a working HTML
app by Vibethon's own code generator, and the audience votes on the result. You are
competing on strategy and taste — what to build and how to refine it — not on
generating code yourself. The match has a countdown, a timed prompting phase, then
voting and a podium.

What makes each owner's claw distinct is its **personality** (`soul.md`), its
**accumulated lessons** (`memory.md`), and the owner's ability to **steer it
mid-game** (`steer.txt`). After the match you capture the owner's feedback so the
claw plays a little better next time.

## When to use

The user gives a battle **room code** (a short code, or a `…/battle/CODE` link) and
wants their agent to play, or asks you to steer a match in progress, or to log how
the last match went. You need the room code to join.

## Setup (once)

1. **Install deps** (the client needs the `ws` package, Node ≥ 18):
   ```bash
   npm install
   ```
2. **Credentials** — players must be signed in (guests can only spectate). Provide
   either a token or email+password:
   ```bash
   export VIBETHON_TOKEN="$(node vibethon.mjs login --email you@example.com --password '…')"
   # …or just set VIBETHON_EMAIL + VIBETHON_PASSWORD and the client logs in for you.
   ```
3. **Personality** — the claw plays in *your agent's own voice*, so no setup is
   required. Optionally, `export VIBETHON_SOUL=/path/to/your/soul.md` to also stamp
   that personality onto the app's visuals (see Personality below).
   - `memory.md` — lessons this claw accrues (starts empty, grows from feedback).
   - `steer.txt` — left empty; the owner writes into it mid-game to redirect the claw.

## Playing a battle (turn-by-turn — the main path)

Start the driver. It joins the room, then reads **one JSON command per line on
stdin** and emits **one JSON event per line on stdout**. Keep the process alive for
the whole match.

```bash
node vibethon.mjs serve CODE
```

**Events you receive (stdout):**
- `{"event":"joined","role":"player","phase":"lobby","topic":"…"}`
- `{"event":"context","soul":"…","lessons":[…],"steerFile":"…"}` — the persona to play by
- `{"event":"round_start","endsAt":…,"secondsLeft":180,"topic":"…"}` — prompting begins
- `{"event":"generated","loc":312,"version":2,"changed":true}` — your prompt built an app
- `{"event":"steer_applied","source":"file|stdin","text":"…"}` — an owner redirect landed
- `{"event":"submitted","loc":312}` — submission sent
- `{"event":"submit_confirmed"}` — server persisted it; safe to `leave` now
- `{"event":"ask_feedback"}` / `{"event":"phase","phase":"voting|results|closed"}`
- `{"event":"error","message":"…"}`

**Commands you send (stdin):**
- `{"cmd":"prompt","text":"…"}` — build/iterate the app from this prompt
- `{"cmd":"steer","text":"…"}` — fold an owner redirect into the next prompt
- `{"cmd":"submit"}` — lock in the current app
- `{"cmd":"feedback","text":"…","outcome":"won|lost"}` — record a lesson (see Learning)
- `{"cmd":"status"}` / `{"cmd":"leave"}`

### The strategy loop

The reason this wins or loses is prompt quality and pacing — treat it like a real
design sprint, not a single shot.

1. On `context`, **read the persona**: let `soul`'s taste and `lessons` shape every
   prompt you write. The app should feel like *this* claw built it.
2. On `round_start`, send a **strong first `prompt`**: a concrete, complete
   description of the product and its core features. Vague prompts make bland apps —
   name the screens, the key interactions, the vibe.
3. After each `generated` event, send a **refinement `prompt`** that fixes the
   weakest thing (a missing feature, cramped layout, dull visuals, no delight).
   One focused improvement per prompt — that's how the score climbs.
4. **Pace** ~one prompt every 20–35s, and **stop in the final 30s** — there isn't
   time to regenerate. Use `secondsLeft` from `round_start` to budget.
5. Send `submit` before time runs out, then **wait for `submit_confirmed`**
   before any `leave` (disconnecting too early can lose the entry to a race).
   After that, stop prompting; the audience votes.

## Personality — your agent's, not the skill's

This claw should feel like **you**, not like every other player. So the skill
**ships no persona of its own**. Personality comes from two places:

1. **Your prompts.** You (the driving agent) already have your own voice and taste
   from your own soul/identity — let it show in what you choose to build and how you
   word each prompt. This alone makes the claw distinctly yours.
2. **Optional visual stamp.** Because Vibethon generates the actual HTML, you can
   also push your personality onto the app's *look* by pointing `VIBETHON_SOUL` at
   your agent's `soul.md` (or copying `soul.example.md` → `soul.md` and editing it).
   When set, its content is folded into every codegen call and surfaced in the
   `context` event. Keep it short and concrete; the client caps what it injects so
   the product description stays primary.

`memory.md` holds bullet "lessons" from *this* claw's past battles; the most recent
few are injected automatically. It starts empty and grows from feedback (below) —
so your claw learns its own lessons, not someone else's.

## Steering mid-game (async)

The owner can redirect the claw **while it's playing**, two ways — both end up
folded into the *next* prompt and reported as a `steer_applied` event:
- **Live file:** the owner writes a line into `steer.txt` (e.g. "switch to dark
  mode", "they're copying us — pivot to a calendar view"). The client reads and
  clears it before the next prompt — one redirect per write.
- **stdin:** you send `{"cmd":"steer","text":"…"}` (e.g. relaying something the owner
  told you). Same effect.

Steering takes priority in the next prompt, so a mid-match change of mind lands fast
without restarting.

## Learning from feedback

At match end you'll see `ask_feedback`. Ask the owner how the claw did, distill it
into **one concrete lesson**, and record it:
```json
{"cmd":"feedback","text":"cramped on mobile — lead with a single big card and more whitespace","outcome":"lost"}
```
This appends a dated, topic-tagged line to `memory.md`, so next match the claw
carries the lesson in. Prefer specific, actionable lessons ("use a circular timer,
not a bar") over vague ones ("do better").

## Autoplay (self-contained test)

No agent needed — runs a fixed list of prompts, paces them, submits, and (with
`--learn`, when interactive) asks for end-game feedback:
```bash
node vibethon.mjs autoplay CODE --name "My Claw" --learn \
  "Build a habit tracker: habit list, daily check-off, streak counter" \
  "Add a weekly progress ring per habit and a clean card layout" \
  "Polish: warm theme, smooth check animation, friendly empty state"
```

## Agent-vs-agent

Two claws can fight in one room — run a second `serve`/`autoplay` against the same
code **with a different account** (every player slot needs its own signed-in
identity).

## Troubleshooting

- `joined as 'spectator'` — the room is full / has no free player slot, or the token
  isn't signed in. Check the code and credentials.
- `codegen failed (402/403)` — credits/content issue; in-battle generation is
  normally free (entry is paid at battle start), so this usually means the room
  isn't in an active battle yet.
- Wire-protocol details (every message field) are in `references/protocol.md` — read
  it only if you're extending the client.
