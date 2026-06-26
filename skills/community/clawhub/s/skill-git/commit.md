---
name: skill-git:commit
description: Use when the user wants to snapshot, save, or version their skills. Triggers on "commit my skills", "save skill changes", "new version of my skill", or after editing any SKILL.md file.
---

You are running `/skill-git:commit`. Follow these steps exactly.

## Step 1 — Init Check

Read `~/.skill-git/config.json`.

If the file does not exist, or if it exists but has no `skills` field under the current agent, tell the user:

> skill-git is not initialized. Please run `/skill-git:init` first.

Then stop.

Otherwise, extract the skills registry for the current agent (default: `claude`):
- `global_base` — the agent's base directory
- `skills` — map of skill name → `{ path, version }`

## Step 2a — Filesystem Scan

Run:

```bash
ls -1d <global_base>/skills/*/
```

For each subdirectory found, check if its basename exists as a key in the `skills` map from config.json.

If any subdirectories are **not** in the map, classify each:
- Has a `.git` directory inside → `"has .git, not registered"`
- No `.git` directory → `"no git, never initialized"`

Display (do not stop, do not prompt):

```
⚠️  Found N skill folder(s) not registered in config.json:

  - <skill-name>    (has .git, not registered)
  - <skill-name>    (no git, never initialized)

These skills will NOT be included in this commit.
Run `/skill-git:init` to register them, then commit again.
```

Then continue to Step 2b.

## Step 2b — Parallel Scan

Spawn one subagent per skill in parallel. Each subagent receives a single skill's `name` and `path` and runs:

Instructions for each subagent:
1. **First**, run `git -C <path> status --porcelain` and check its exit code.
   - If the exit code is **128** (directory missing or not a git repo) → return `{ "missing": true, "name": "<skill-name>", "path": "<path>" }`. Do not run git diff.
2. If `status --porcelain` is empty → return `{ "changed": false }`.
3. If status is non-empty → run `git -C <path> diff HEAD` and return:
   - `changed: true`
   - `files`: list of changed file paths (from status output)
   - `diff`: full output of `git diff HEAD`
   - `untracked`: list of files with `??` prefix from status (these are new, untracked files — **return filenames only, do NOT read their content**)

Wait for all subagents to complete.

Collect all results where `missing: true`. If any, display the list and prompt once:

```
⚠️  The following skill directories no longer exist:

  🗑  <skill-name>    (<path>)
  🗑  <skill-name>    (<path>)

Remove these entries from config.json? [y/n]
```

Wait for the user's response:
- `y` → for each missing skill, run:
  ```bash
  jq --arg agent "claude" --arg name "<skill_name>" \
    'del(.agents[$agent].skills[$name])' \
    ~/.skill-git/config.json > /tmp/sg-cfg.json \
    && mv /tmp/sg-cfg.json ~/.skill-git/config.json
  ```
  Then display: `Removed N entries from config.json.`
- `n` → keep config.json unchanged; these skills are excluded from further steps.

Then proceed to Step 2c with only non-missing skills.

## Step 2c — Untracked File Content Confirmation

Collect all untracked files reported by subagents across all skills.

**Sensitive filename blocklist** — never read or include these regardless of user consent:

```
.env  .env.*  *.env
*.pem  *.key  *.p12  *.pfx  *.crt  *.cer  *.keystore
credentials  credentials.*  credential.*
secrets  secrets.*  secret.*
*_token  *_token.*  *.token
*password*  *passwd*  *secret*  *apikey*  *api_key*
.aws  .ssh  id_rsa  id_ed25519  id_ecdsa
*.gpg  *.pgp
```

Apply the blocklist (case-insensitive filename match). For any untracked file whose name or path component matches a blocked pattern:
- Do **not** show it for content confirmation.
- Include a note in the final summary: `(content skipped — sensitive filename)`.

If any **non-blocked** untracked files remain, display:

```
📄 The following untracked file(s) were found. Read their content to include in the commit summary?

  Skill: <skill-name>
    - <filename>
    - <filename>

  [y] Yes, read content   [n] No, use filenames only
```

Wait for the user's response:
- `y` → read the content of each listed file and attach it to the corresponding skill's result for use in Step 3.
- `n` (or no untracked files after blocklist filtering) → proceed without reading content; use filename list only in Step 3 summary.

If there are **no** untracked files at all, skip this step silently.

## Step 3 — Display Change Summary

If all skills returned `changed: false`:

```
✅ Nothing to commit. All skills are up to date.
```

Stop here.

Otherwise, for each skill with `changed: true`, read the diff/content returned by its subagent and write **2-3 sentences in English** describing what actually changed (new rules added, behaviors modified, files restructured — not just file names).

A skill is a **new skill** if its name does not appear in the `skills` map in config.json.

Display the summary and prompt the user:

```
📋 Detected changes in N skill(s):

  1. <skill-name>    ~ <N> file(s) changed
     <2-3 sentence English description of what changed>

  2. <skill-name>    + new skill
     <2-3 sentence English description of the new skill>

  ...

How to proceed?
  a) Commit all
  b) Commit selected (enter numbers or names, e.g. "1,3" or "humanizer code-review")
  c) Cancel
  d) Other (describe what you want)
```

Wait for the user's response. Parse it to determine which skills to commit:
- `a` → all changed skills
- `b` + input → match by number (1-based index in the list) or by skill name; both are accepted
- `c` → stop, tell the user nothing was committed
- `d` or free text → interpret the user's intent and clarify if needed

## Step 4 — Version & Message Suggestions

For each skill selected in Step 3:

1. **Pre-flight tag check**: run `git -C <path> tag --list "v*"` to see existing tags. If the tag you are about to suggest already exists, pick the next logical version.

2. Analyze the diff and apply SemVer rules:

   | Bump        | When to apply                                                         |
   |-------------|-----------------------------------------------------------------------|
   | PATCH x.x.+1 | Wording fixes, minor rule tweaks, typo corrections                   |
   | MINOR x.+1.0 | New rules or behaviors, new supporting files (scripts, examples)      |
   | MAJOR +1.0.0 | Core behavior rewrite, major rule deletions, fundamental purpose change |

3. Generate a short, lowercase imperative commit message (e.g. `"add em-dash detection rule"`).

Output **all suggestions in a single message** — do not prompt skill by skill:

```
Here are the suggested versions and messages for all selected skills:

  1. <skill-name>    <current> → <suggested>
     "<commit message>"

  2. <skill-name>    <current> → <suggested>
     "<commit message>"

  ...

How to proceed?
  a) Accept all
  b) Edit specific ones (enter numbers or names + your changes)
  c) Cancel
  d) Other
```

Wait for the user's response. Collect all final versions and messages before moving to execution. Do not execute anything yet.

## Step 5 — Execute

After all versions and messages are confirmed, execute for each skill in order:

```bash
git -c user.email=skill-git@local -c user.name=skill-git -C <path> add -A
git -c user.email=skill-git@local -c user.name=skill-git -C <path> commit -m "<message>"
git -c user.email=skill-git@local -c user.name=skill-git -C <path> tag <version>
```

If any command fails, print the git error, skip the config.json update for that skill, and continue with the remaining skills.

After each successful commit+tag, update config.json:

```bash
jq --arg agent "claude" --arg name "<skill_name>" --arg ver "<version>" \
  '.agents[$agent].skills[$name].version = $ver' \
  ~/.skill-git/config.json > /tmp/sg-cfg.json \
  && mv /tmp/sg-cfg.json ~/.skill-git/config.json
```

When all done, show the final result:

```
✅ <skill-name>    → <version>  committed
✅ <skill-name>    → <version>  committed
⏭️  <skill-name>   skipped

[skill-git] Done. Run /skill-git:revert to roll back any skill to a previous version.
```
