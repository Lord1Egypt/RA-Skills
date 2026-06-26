---
id: sun-to-spotify
name: sun-to-spotify
description: Generate Sun audio and stream episodes to Spotify as a podcast. Uses the `sun` CLI (or HTTP API) to authenticate, mint a personal API token, create an audio job from a prompt, fetch episodes incrementally as they finish, and upload each episode sequentially to a freshly-created Spotify show.
enabled: true
---

# sun-to-spotify — Sun Audio Generation + Streaming Spotify Upload

`sun-to-spotify` produces audio through the Sun public API, then streams each finished episode to Spotify as a podcast episode. Given a prompt and a target duration, it creates a job, fetches episodes incrementally as they finish, and uploads each one in order to a Spotify show (a new show is created by default — one Sun audio = one Spotify show).

The skill is built around the `sun` CLI (>=0.2.1 for incremental fetch). For environments where the CLI isn't available, the same flow can run directly against the HTTP API.

> **Naming**: the canonical CLI subcommand is `sun audio`. `sun courses` still works as a hidden alias that prints a one-line deprecation warning on stderr. Use `sun audio` in all new examples.

> **Framing note**: when talking to the user, describe the output as a **podcast, audiobook, or audio course** (whichever fits the topic and duration best — short topical takes lean podcast, long narratives lean audiobook, structured multi-segment lessons lean audio course). Avoid framing this as a "course generator" — it's a versatile audio-experience generator.

## Reference Directory

Load only the file you need — don't inline them.

- [references/cli-usage.md](references/cli-usage.md) — `sun` CLI commands: `login`, `whoami`, `tokens`, `audio`. Install methods, flags (including `--partial` and `--callback-url`), output layout, JSON mode, env-var overrides, troubleshooting.
- [references/http-api.md](references/http-api.md) — HTTP-only flow when the CLI isn't installed: `auth-config` discovery, Supabase password grant, token mint, audio create / status / result (with `?include_partial=true` and `callback_url`), signed-URL audio download, rate-limit headers, error envelope.

---

## Install

The `sun` CLI is independently installable — no monorepo checkout required. Four options, in order of recommendation for external users:

```bash
# 1. curl installer (simplest — picks uv/pipx/pip automatically)
curl -fsSL https://sunapp-ai.github.io/sun-to-spotify/install.sh | bash

# 2. uv tool (manual, fastest)
uv tool install 'sun-cli>=0.2.1'

# 3. pipx (isolated)
pipx install 'sun-cli>=0.2.1'

# 4. pip
pip install 'sun-cli>=0.2.1'
```

Verify:

```bash
sun --help
sun --version    # prints "sun-cli <version>"
```

> PyPI package name is `sun-cli`; the installed binary is `sun`. The curl installer is hosted on GitHub Pages from the [`sunapp-ai/sun-to-spotify`](https://github.com/sunapp-ai/sun-to-spotify) repo and requires `uv`, `pipx`, or `pip` to already be available; if none is, it prints install instructions and exits.

If `sun --help` fails after install, ask the user how they installed it before troubleshooting. See [references/cli-usage.md](references/cli-usage.md) for monorepo-dev install (`uv sync` + `uv run sun`) and platform-specific notes.

---

## Core Principles

### Inputs come from the user

Don't invent a prompt. If the user said "make a podcast / audiobook / audio course about X", that's the prompt. If they didn't supply one, ask. Never substitute a creative prompt of your own.

### Save incrementally

Write the `job_id` to disk (or echo it back to the user) immediately after the `202` response. If polling crashes mid-loop, the job keeps generating server-side — re-poll with the same `job_id` rather than restarting.

### Stream — don't wait for the full course

Starting in 0.2.1, episodes finish one-by-one and are visible via `sun audio get --partial`. As soon as episode 1 lands, start uploading to Spotify. Don't block on `SUCCESS` before kicking off Spotify uploads — that wastes minutes per episode and the user loses the streaming benefit.

### Don't cache signed URLs

`audio_url` values are signed for 7 days, but the result endpoint re-signs them on every read. Always fetch fresh URLs from `sun audio get` (which calls `/v1/public/courses/{job_id}`) right before downloading; never persist them.

### Treat `SUCCESS` and `show_uri` as eventually consistent

Two surfaces in this pipeline are eventually consistent. Plan for both — neither is a bug:

- **`sun audio status` returns `SUCCESS` before every episode's `audio_url` is signed.** Generation completes per-episode, then signed URLs land on a slight delay. Keep calling `sun audio get --partial` after `SUCCESS` until every `audio_url` in the manifest is non-null (equivalently: every `NNN-*.mp3` file has appeared under `episodes/`). Don't treat post-`SUCCESS` null `audio_url`s as failures, and don't exit the loop on `SUCCESS` alone — exit only when every episode has been downloaded *and* uploaded.
- **`save-to-spotify shows create` can return `{"show_uri": null}` and succeed seconds later on retry.** Show creation is queued; the URI is confirmed on a short delay. Watch out for `jq -r .show_uri` rendering JSON `null` as the literal string `"null"` — that's not a valid URI. Use `jq -r '.show_uri // empty'` so the result is empty on null, then retry the same `shows create` call on the next poll until a real URI lands. Never upload with `--show-id null`.

The streaming loop in section 2 implements both rules. If you adapt it, preserve those guards.

### Surface server-reported errors verbatim

The API returns a bare `{"error": {"code": "...", "message": "...", ...}}` envelope on every non-2xx. When something fails, show the user the `error.message` and `error.code` — don't paraphrase or hide them. For `429`, read `Retry-After` instead of computing waits yourself.

---

## Required Inputs

Before generating, confirm the user has supplied:

1. **Prompt** — the topic for the audio (podcast, audiobook, or audio course). 1-4000 chars. Mandatory.
2. **Duration** — minutes of audio. 5-120, default 30. Optional.
3. **Voice** — voice UUID. Optional. If not given, the API picks a default.
4. **Output directory** — where to save the manifest + downloaded MP3s. Optional; default to `./audio-<short-job-id>/`.
5. **Spotify show choice** — defaults to creating a new show named after the manifest's `name` field. Only switch to "publish under an existing show" if the user explicitly asks.
6. **Spotify cover image** — defaults to the `cover.<ext>` file `sun audio get` downloads. Only ask for a replacement path if the user explicitly wants one, **or** if Spotify rejects the auto cover for size/format reasons.

If the prompt is missing, ask once and stop. Don't proceed without it.

---

## Execution Checklist

Run these in order. Do not skip preflight.

### 0. Preflight — CLI presence and auth

```bash
sun --help              # verify the CLI is on PATH and runnable
sun whoami              # verify there's an active session + token
```

- If `sun --help` fails, the CLI isn't installed. Show the user the Install section above and ask them to confirm before running the installer. If install isn't possible, fall back to the HTTP flow in [references/http-api.md](references/http-api.md).
- If `whoami` reports unauthenticated: do **not** run `sun login` from the agent. `sun login` opens a browser for the loopback POST handoff — this won't complete in an agent context, and there is no `--email`/`--password` fallback. Ask the user to run `sun login` themselves in their terminal and re-invoke the skill. If the user is signing up for the first time, remind them to click the confirmation email link on the same machine where `sun login` is still running — the original loopback completes automatically post-confirmation, no second `sun login` needed. The same applies to the password-reset flow. For CI / fully non-interactive contexts, the user must first run `sun login` interactively on a machine with a browser, then carry the resulting `~/.config/sun/credentials.json` (or a minted `SUN_TOKEN`) over to the headless environment.
- If `whoami` reports authenticated but no active token, run `sun tokens create <name>` (`<name>` matches `^[a-z0-9-]+$`, 1-64 chars). The full secret prints to stdout once and is stored as the active token; surface it to the user but never log it elsewhere.

### 1. Create the audio job

```bash
sun audio create \
  --prompt "<the user's prompt>" \
  --duration-minutes <N> \
  --json
# Prints {"job_id": "...", ...} to stdout. Do NOT pass --wait — we need
# control of the streaming loop in the next step.
```

- Pass `--voice-id <uuid>` if the user specified a voice.
- Pass the prompt via `--input <path>` or stdin if it's longer than a comfortable shell argument.
- A `429` response means the user hit their daily limit. Show them `error.message`, `Retry-After`, and `X-RateLimit-Reset`. Do not auto-retry.

Save the `job_id` immediately:

```bash
JOB_ID=$(sun audio create --prompt "..." --duration-minutes 30 --json | jq -r .job_id)
echo "$JOB_ID" > "$OUT_DIR/.sun-job-id"   # so a crash + restart can resume
```

### 2. Stream episodes → Spotify as they finish

This is the new core flow. The skill polls `sun audio get --partial` every ~10 seconds. As each new episode lands in `episodes/NNN-<slug>.mp3`, it uploads to Spotify in order. The first episode to land also triggers Spotify show creation (we need the cover and the manifest's `name` to seed the show).

#### Output layout (after at least one `sun audio get --partial`)

```
<OUT_DIR>/
  overview.json                                                # the manifest (source of truth)
  cover.<ext>                                                  # downloaded cover image (Spotify show cover)
  episodes/
    001-<slug>.mp3                                             # first episode audio
    001-<slug>.<ext>                                           # first episode artwork (optional)
    002-<slug>.mp3
    002-<slug>.<ext>
    ...
```

Filename convention: `NNN-<slug>.mp3` where `NNN` is the zero-padded episode number (`001`, `002`, …). The slug is the episode title slugified by the CLI. `001` is the first episode and is always uploaded first; sequential ordering is preserved.

#### Show creation policy

- **Default**: create a new Spotify show. One Sun audio = one Spotify show.
- **Title**: `overview.json` `.name` field.
- **Summary**: `overview.json` `.description` field (may be empty mid-generation; re-read after SUCCESS if you want the refined description).
- **Cover**: the `cover.<ext>` file under `<OUT_DIR>/`.
- Only deviate from "create new" if the user explicitly says "publish under my existing show <X>".

#### The streaming loop

```bash
OUT_DIR=./audio-${JOB_ID:0:8}
mkdir -p "$OUT_DIR"
SHOW_URI=""
COVER=""
declare -a UPLOADED=()    # episode numbers we've already uploaded

while true; do
  STATUS=$(sun audio status "$JOB_ID" --json | jq -r .status)

  # Pull whatever's ready right now. The CLI quietly skips episodes whose
  # audio_url is still null, so it's safe to call repeatedly.
  sun audio get "$JOB_ID" --partial --out "$OUT_DIR" >/dev/null 2>&1 || true

  # Create the Spotify show on first episode arrival (we now have cover + name).
  # `shows create` is eventually consistent: it can return show_uri=null and succeed
  # on the next call. Retry while SHOW_URI is empty — never persist literal "null".
  if [ -z "$SHOW_URI" ] && \
     [ -f "$OUT_DIR/overview.json" ] && \
     ls "$OUT_DIR"/episodes/001-*.mp3 >/dev/null 2>&1; then
    COVER=$(ls "$OUT_DIR"/cover.* 2>/dev/null | head -1)
    SHOW_TITLE=$(jq -r '.name'                "$OUT_DIR/overview.json")
    SHOW_DESC=$( jq -r '.description // ""'    "$OUT_DIR/overview.json")

    SHOW_URI=$(save-to-spotify --json shows create \
      --title   "$SHOW_TITLE" \
      --summary "$SHOW_DESC" \
      --image   "$COVER" \
      | jq -r '.show_uri // empty')   # `// empty` collapses JSON null to "" instead of "null"
    if [ -n "$SHOW_URI" ]; then
      echo "[show ] created: $SHOW_TITLE → $SHOW_URI"
    else
      echo "[show ] not ready yet — will retry next poll"
    fi
  fi

  # If the show is ready, upload each new episode in order.
  if [ -n "$SHOW_URI" ] && [ -f "$OUT_DIR/overview.json" ]; then
    TOTAL=$(jq -r '.lectures | length' "$OUT_DIR/overview.json")
    NEXT=$(( ${#UPLOADED[@]} + 1 ))

    while [ "$NEXT" -le "$TOTAL" ]; do
      FILE=$(ls "$OUT_DIR"/episodes/$(printf "%03d" "$NEXT")-*.mp3 2>/dev/null | head -1)
      [ -z "$FILE" ] && break   # not ready yet — try again next poll

      TITLE=$(jq -r --argjson n "$NEXT" '.lectures[] | select(.number == $n) | .title' "$OUT_DIR/overview.json")

      save-to-spotify --json upload "$FILE" \
        --title   "$TITLE" \
        --show-id "$SHOW_URI" \
        --image   "$COVER" >/dev/null

      UPLOADED+=( "$NEXT" )
      echo "[upload] episode $NEXT/$TOTAL: $TITLE"
      NEXT=$(( NEXT + 1 ))
    done

    # Progress checklist after each iteration.
    print_checklist "$TOTAL" "${UPLOADED[@]}"
  fi

  # Terminate when sun says SUCCESS AND every episode has been uploaded.
  # SUCCESS can fire before every audio_url is signed — keep iterating so the
  # next `sun audio get --partial` picks up late-signed episodes.
  if [ "$STATUS" = "SUCCESS" ] && [ -n "$SHOW_URI" ] && \
     [ "${#UPLOADED[@]}" -eq "$TOTAL" ]; then
    break
  fi
  if [ "$STATUS" = "ERROR" ]; then
    echo "Generation failed. Read 'sun audio status $JOB_ID --json' for details." >&2
    exit 1
  fi

  sleep 10
done

echo "[done ] All $TOTAL episodes uploaded to $SHOW_URI"
```

`print_checklist` formats one line per episode. Render it after every upload so the user can watch progress live:

```
Sun → Spotify upload progress (5/10):
  [x] 001 — From Manya to Governess: Early Years and Formative Struggles
  [x] 002 — Paris and the Pursuit of Science
  [x] 003 — Discovering Radioactivity
  [x] 004 — Polonium and Radium: The Discovery of New Elements
  [x] 005 — Nobel Prizes and International Recognition
  [ ] 006 — generating…
  [ ] 007 — generating…
  [ ] 008 — generating…
  [ ] 009 — generating…
  [ ] 010 — generating…
```

For each line, look up the title from `overview.json` by episode number. Episodes still mid-generation will be in the manifest but their `audio_url` will be `null` — surface them as "generating…" so the user can see the total expected count from the start.

#### Webhook alternative

If the user is running their own publicly-reachable HTTP endpoint, you can register it with `--callback-url` at job creation and replace the polling loop with a push-driven upload. The webhook body is:

```json
{
  "event": "episode_ready",
  "job_id": "...",
  "episode_id": "...",
  "episode_number": 1,
  "title": "...",
  "audio_url": "https://...signed.../l1.mp3?token=..."
}
```

Treat the webhook as a hint — still fetch `sun audio get --partial --out DIR` for the manifest + a fresh signed URL before uploading. Webhooks are best-effort (fire-and-forget on the server). The polling loop is the recommended default; the webhook is for users with an existing HTTP receiver.

### 3. Final verification

When the loop exits, confirm the manifest's lecture count matches the uploaded count:

```bash
TOTAL=$(jq -r '.lectures | length' "$OUT_DIR/overview.json")
echo "Manifest expected $TOTAL episodes; uploaded ${#UPLOADED[@]}."
test "$TOTAL" -eq "${#UPLOADED[@]}" || echo "WARNING: count mismatch — re-run the loop to pick up missing episodes." >&2
```

If counts disagree, re-run the streaming loop once. The CLI's `--partial` fetch re-signs URLs and fills in any episode whose `audio_url` was transiently null on the previous pass. If they still disagree, surface the gap to the user — don't loop indefinitely.

---

## End-to-end example

User request: "Make me a 30-minute course on Marie Curie and publish it to Spotify."

```bash
sun --help >/dev/null || { echo "CLI not installed"; exit 1; }
sun whoami >/dev/null || { echo "Not logged in. Run 'sun login' in your terminal first."; exit 1; }
save-to-spotify --json auth status >/dev/null \
  || { echo "Not authed with Spotify. Run 'save-to-spotify auth login' first."; exit 1; }

JOB_ID=$(sun audio create \
  --prompt "The life and scientific contributions of Marie Curie" \
  --duration-minutes 30 \
  --json | jq -r .job_id)

OUT_DIR="./audio-${JOB_ID:0:8}"
mkdir -p "$OUT_DIR"
echo "$JOB_ID" > "$OUT_DIR/.sun-job-id"
echo "job_id: $JOB_ID"

# Then run the streaming loop in section 2. After it returns,
# `$SHOW_URI` holds the Spotify show URI for the user.
```

---

## When the user wants the rich `save-to-spotify` production flow

If the user wants `save-to-spotify`'s **content production** (custom timeline with chapters, image companions, external links, Spotify entity cards, polished cover generation) rather than a straight upload of sun's MP3s, that's outside this skill's scope. Defer to the full `save-to-spotify` skill — it owns the rich-timeline production pipeline.

`sun-to-spotify` only does sun audio → straight Spotify upload. It hands off to `save-to-spotify`'s `auth`, `shows`, and `upload` surfaces; it does **not** invoke save-to-spotify's interview, scripting, TTS, or timeline production.

---

## Error handling

Surface `save-to-spotify` errors verbatim — its JSON envelope already carries `error.code` and `error.message`. Do not auto-retry on `429` or `auth_required`.

If Spotify rejects the cover image on `shows create` (wrong dimensions, wrong format, file too small), tell the user the exact error and ask for a replacement path. Spotify requires roughly **3000×3000 JPG/PNG, ≤500KB**; the auto-downloaded `cover.<ext>` usually meets this but isn't guaranteed.

---

## When the CLI isn't available

If `sun` isn't installable (sandboxed env, restricted shell, etc.), the HTTP API supports the same operations. See [references/http-api.md](references/http-api.md) — it covers `auth-config` discovery, the Supabase password grant for token minting, audio create / status / result (including `?include_partial=true` and `callback_url`), and the audio-download loop in pure curl or `httpx`.
