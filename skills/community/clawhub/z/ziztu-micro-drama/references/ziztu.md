# Producing episodes on Ziztu

Ziztu (getziztu.com) turns a script into a finished vertical episode: it plans the shots, keeps the same characters in every shot, voices the dialogue inside the clips, adds music and captions, and exports an MP4. This file is the playbook for driving it from Claude or Codex through the Ziztu connector (an MCP server), and for the web app when no connector is present.

Contents
1. Is the connector here? (and how to add it)
2. The money rules
3. One episode, start to finish
4. Keeping the cast the same across episodes
5. Checking the plan before paying
6. Errors and what they mean
7. No connector: the web app path
8. The planning-only edition

The tool descriptions the connector sends are the source of truth. If a tool's own description disagrees with this file, follow the tool.

## 1. Is the connector here?

Look at the tools you can call. The Ziztu tools have these names (some clients add a prefix, such as `mcp__ziztu__import_script` in Claude Code or `ziztu:import_script`):

- Projects: `list_projects`, `create_project`, `get_project`
- Director: `director_chat`, `apply_plan`, `director_plan`
- Script: `import_script`, `script_to_shots`, `read_script`, `get_script_job`, `ask_script_editor`, `decide_script_edit`, `get_script_doctor_notes`, `list_script_versions`, `restore_script_version`, `get_script_file`, `start_script_draft`
- Price and make: `quote`, `get_credits`, `make_first_frames`, `animate_shots`, `make_music`, `export_film`, `job_status`, `list_jobs`

If none are present, finish the writing anyway (the scripts are the user's to keep), save each episode as a `.fountain` file, and tell the user how to connect so production is one sentence away next time:

| App | How to add Ziztu |
|---|---|
| claude.ai and Claude Desktop | Customize, then Connectors, then **+ Add**, then **Add custom connector**. Name it Ziztu, paste `https://getziztu.com/mcp`, sign in to Ziztu and press Allow. In a chat: **+**, Connectors, switch Ziztu on. |
| Claude Code | `claude mcp add --transport http ziztu https://getziztu.com/mcp` (add `--scope user` for every project), then type `/mcp`, pick ziztu and sign in. |
| Codex (CLI, IDE extension, desktop app) | `codex mcp add ziztu --url https://getziztu.com/mcp`, then add `tool_timeout_sec = 180` under `[mcp_servers.ziztu]` in `~/.codex/config.toml` (a Director call can take longer than Codex's 60 second default), then `codex mcp login ziztu`. Check with `codex mcp list`. |
| Cursor | Add `"ziztu": { "url": "https://getziztu.com/mcp" }` inside `mcpServers` in `.cursor/mcp.json`, then sign in from Cursor's MCP settings. |
| Anything else | Step-by-step pages for each app: https://getziztu.com/connect |

Every AI step uses credits: Starter is $7 a month (4,800 credits) and All access starts at $49 a month (see https://getziztu.com/pricing). For unattended agents, an API key from the Studio (Settings, API keys) can replace the browser sign-in.

## 2. The money rules

These are the user's credits. Ziztu enforces a cap on every paid call, and the skill adds the human step on top:

1. **Price first.** Before any paid step, get the exact price: `quote` (operations `frames`, `animate`, `music`) or the same tool with `dry_run: true` (the script tools: `script_to_shots`, `ask_script_editor`, `get_script_doctor_notes`, `start_script_draft`). A dry run still needs a `max_credits` number in the call (the field is required; any number works, for example 10) and spends nothing. It answers with `price_credits` and `suggested_max_credits`.
2. **Show the price and wait for a yes.** Say what it buys in plain words ("first frames for 14 shots: 420 credits; balance 11,800"). Use `get_credits` for the balance.
3. **Spend with a cap.** Pass `max_credits` at or just above the quoted price. Above 5,000 credits the call also needs `confirm: true`, which you only send after the user has seen that price.
4. **Pilot before the batch.** Animate one shot first (`shot_ids` with one id) when the look or a character is new, and let the user see it before animating the rest.
5. **Never repeat a paid call to "retry"** without checking `list_jobs` first: the first one may have started.

Free: `create_project`, `get_project`, `list_projects`, `import_script`, `apply_plan`, `quote`, `get_credits`, `job_status`, `list_jobs`, `read_script`, `export_film`. Small metered cost: `director_chat` and `director_plan` messages. Paid with a cap: `script_to_shots`, `make_first_frames`, `animate_shots`, `make_music`, and the script editor and doctor tools.

## 3. One episode, start to finish

One Ziztu project per episode. Each project exports one MP4, which is exactly one episode on TikTok, Reels, Shorts or an app.

**Step A. Create the project.** `create_project` with `name` "<Series title> · Ep 01 · <episode title>" and `aspect` "9:16" (use "16:9" only for a widescreen anime episode or a YouTube cut). Note the project id.

**Step B. Give the Director the brief, naming the medium.** Call `director_chat` once, before importing the script, with a brief of 40 to 120 words that starts with the medium. Ziztu makes no picture until a project has a look, and it takes the look from the words in the first brief, so the medium word has to be there: "Live-action", "photorealistic", "2D anime", "3D animated" or "cartoon". Do not start the brief with a command word (Plan, Make, Write, Add): write it as a description of the story. Template:

> Live-action, cinematic vertical micro drama, episode 1 of 30 of "<Series title>". <Two-sentence series logline>. This episode: <one-sentence episode summary>. Leads: <Name> (<Character Lock in one line>), <Name> (<...>). Places: <place 1>, <place 2>. Tone: <tone words>. Layered depth in every shot: soft foreground, sharp subject, hazy background. Plan only for now, no pictures yet: the script comes next.

Do not call `apply_plan` on this reply; it is only there to set the idea and the look. Check it with `get_project`: `style.preset_id` now names a look (for example `live-action-cinema`) and `brief.logline` holds your brief. The brief and the look are saved even when the Director's reply itself is an error message (for example when the balance is empty). If no look was set, the medium word was missing: say it in plain words in the next message.

**Step C. Import the episode script.** `import_script` with `project_id`, `format` "fountain" and `text` = the episode's Fountain (title page included). It is free and keeps the dialogue word for word. Check the returned `scene_count` and `characters` against the script; a character listed twice under two spellings means the script used two names for one person, so fix the script and import again with `replace_existing: true`.

**Step D. Turn the scenes into shots.** `script_to_shots` with `dry_run: true` and `max_credits: 10` first (planning one episode's shots costs about ten or twenty credits; the dry run gives the exact price), show the price, then call it again with `max_credits` set to `suggested_max_credits`. One run plans up to 6 scenes; pass `scenes` to choose them. It may return a `job_id`: poll `get_script_job` with `wait_seconds: 15` until `status` is `done`, then read `result.message_id`.

**Step E. Apply the plan.** `apply_plan` with that `message_id`. The cast, places and shots are now in the project. Read them with `get_project` and run the checks in section 5, including tightening a plan that came back long.

**Step F. Lock the cast and places.** For each character, make sure the Ziztu description matches the bible's Character Lock (face, age, hair, build, the signature costume and its colour, accessories, voice). If it does not, ask the Director: "Update <Name>'s description to: <Character Lock>. Keep everything else." then `apply_plan`. Same for places. (`director_chat` answers with the Director's reply message, usually as `{ "message": { "id": "msg_...", "text": ..., "actions": [...] } }`: the id to pass to `apply_plan` is that message's `id` (`message.id`, or the top-level `id` when the reply comes unwrapped). Read its `actions` first to see what will change.)

**Step G. First frames.** `quote` with `operation: "frames"`, show the price, then `make_first_frames` with `max_credits` (add `skip_blocked: true` if the quote lists blocked shots and the user agrees). Poll with `list_jobs` or `job_status` every 10 to 20 seconds until every job is `final`. Ask the user to look at the frames in the Studio (https://getziztu.com/app#/p/<project_id>) before paying for motion: this is the cheap moment to catch a wrong face, a missing person, the wrong place or a flat frame (everyone on one plane against a wall: ask the Director to restage that shot with the place's foreground piece and background, as in `depth-and-staging.md`).

**Step H. Clips.** `quote` with `operation: "animate"`, show the price, pilot one shot, then `animate_shots` for the rest with `max_credits`. Clips come back with the shot's dialogue spoken and its sound.

**Step I. Music and captions.** Ask the Director for the score: "Add one music track for the whole episode: <genre, instruments, tempo in BPM, the mood arc from tension to the cliffhanger sting>. Instrumental only, no vocals." Then `apply_plan`, `quote` with `operation: "music"`, and `make_music` with `max_credits`. For on-screen text, ask the Director for captions from the dialogue, a name strap on each character's first appearance ("MIA CALLOWAY · the cleaner"), and the hook banner if the series uses one, then `apply_plan`.

**Step J. Export.** When every clip and track is final, `export_film`. Poll `job_status` until final, then read the video from `get_project` (exports). Shots without a clip export as stills, so a draft can be exported early to check pacing.

Report to the user after each step in one or two lines: what was made, what it cost, what is next.

## 4. Keeping the cast the same across episodes

Each episode is its own project, so continuity is something you carry:

- Paste the exact same Character Lock text for every recurring character into every episode's brief and, if needed, the Director update in step F. Never paraphrase it between episodes: a changed adjective is a changed face. In the Studio a character has three fields that match the lock: **Describe them**, **Voice** (age, pitch, pace, timbre) and the **Identity line** (at most 45 words), which is why the lock's look line is kept under 45 words.
- After episode 1's character sheets are approved, reuse them: save the approved sheet image from episode 1, then in each later episode's project open the Library, then Cast, open the character, upload the sheet under **Reference images**, choose **My image is the final design**, then **Use my image as the official sheet**. The same sheet then guides every shot of that character in that episode.
- Costume changes are story events: give the new outfit its own line in the bible ("Mia, gala look: emerald satin gown, hair up, no gloves") and name which look each episode uses.
- Keep the same place names and descriptions; recurring sets are the cheapest way to make a series feel like one show.

## 5. Checking the plan before paying

Read `get_project` after `apply_plan` and check, before any frame is made:

- Every speaking character in the script exists once in the cast, with the bible's name and look.
- The total of shot durations is close to the episode's target length (for example 75 to 95 s for a 90 s episode), and no shot carries more dialogue than it can hold: about 2.5 spoken words a second plus a beat, at most about 15 seconds per shot.
- **Tighten a long plan.** The planner gives each scene about a minute of screen time per printed page, the pace of a feature film. Micro drama dialogue plays faster than that (short lines, two-second shots), so a plan often comes back 20 to 40 percent long, which on screen means slow, dead holds. `scripts/episode_check.py` predicts it ("Ziztu's planner will give this about ... s"). When the total is more than about 15 percent over the target, send `director_chat`: "Tighten this episode to about <target> seconds. Keep every line and every beat. Most shots 2 to 4 seconds; a talking shot holds its line plus half a second; no holds longer than 2 seconds except the final frame." Then `apply_plan` and read `get_project` again.
- The first shot is the hook, not an establishing view of a building. The last shot is the cliffhanger beat itself, cut at its peak.
- Each shot names everyone who is in the frame. A person in the frame who is not named tends to vanish; a person named in a shot they are not in tends to appear twice.
- The dialogue on the shots is the script's dialogue. If the planner reworded a line that matters, put it back with `director_chat` ("Shot 6: Mia's line is exactly: ...") and `apply_plan`.

## 6. Errors and what they mean

| Message | Meaning | Do this |
|---|---|---|
| "Choose how the film looks before any picture is made" (409) | The project has no look | Send `director_chat` a sentence naming the medium ("This is a live-action, photorealistic drama."), or set it in the Studio: the project name menu, then Look and style text |
| `max_credits_required` | A paid call without a cap | Quote it, show the price, call again with `max_credits` |
| `over_max_credits` | The real price is above the cap | Nothing was charged; quote again and ask the user |
| `confirm_required` | Above 5,000 credits | Show the price; add `confirm: true` only after a yes |
| `insufficient_credits` or 402 | The balance is too low | `get_credits`, tell the user, link https://getziztu.com/pricing |
| A Codex tool call times out | Codex's default 60 s limit | Set `tool_timeout_sec = 180` for the ziztu server and call `get_script_job` or `list_jobs` to see if it ran |
| `script_not_empty` (409) | Importing over an existing script | Send `replace_existing: true` (the old script is kept as a version) or use a new project |
| A job ends with an error | One frame or clip failed | `list_jobs` for the reason; re-run only that shot id after showing the price |

## 7. No connector: the web app path

Everything works in the browser too:

1. Sign in at https://getziztu.com/app.
2. On Home, open **Script** (beside the start options), then **Start from a script**, then **Import a script**, and pick the episode's `.fountain` file (Fountain, Final Draft `.fdx` or plain text, up to 8 MB).
3. When the Director asks how the film should look, pick Live action, 2D animated, 3D animated or Cartoon.
4. Turn the scenes into shots, check the board, then make frames, clips and music; the Studio shows each price before it runs. Export the episode.

## 8. The planning-only edition

Some directories list `https://getziztu.com/mcp/planner`, which plans, writes and prices but makes no images, video or audio. You can tell it apart by its tools: it has `quote` but no `make_first_frames`, `animate_shots`, `make_music` or `export_film`, and it adds writing tools that use a few credits a run (`write_logline`, `write_script` and others). With it, do steps A to F and the quotes, then give the user the project's `app_url` to make the frames, clips and music in the web app. For everything in this file, the user can add the full connector at `https://getziztu.com/mcp`.
