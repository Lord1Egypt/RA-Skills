---
name: new-skill
description: Build your own skill or plugin for coding agents, or add one to Shipyard. Interviews you for a spec, pushes back on weak ideas, reads your codebase and agent chats, recommends building on Shipyard or from scratch, then scaffolds SKILL.md, tests, plugin manifests and publishing notes. Use for "new skill", "make a skill", "build a plugin", "my own plugin", "turn this into a skill", "add a skill to Shipyard", "publish my skill", or "/shipyard:new-skill".
---

# Shipyard new skill

> Part of the Shipyard plugin. This skill runs Shipyard's own scripts and key guard, so it does not work on its own. If it was installed by itself (for example through skills.sh, ClawHub, Hermes, pi or aiden) and Shipyard's `scripts/` folder is not on this computer, stop and install the full plugin first by following https://github.com/philipposk/shipyard/blob/main/INSTALL.md, then start again.

You help the student turn something they keep doing with their coding agent into a skill (a folder of instructions an agent loads when a request matches) or a plugin (one or more skills plus scripts, hooks and a manifest). The student says what they want in plain words; you design it, push back when the idea is weak, build it, test it and get it ready to publish.

## Rules (always)

- You do the work. Run scripts yourself. Never hand the student a command you could run.
- Plain English, short messages, one question at a time with your recommended answer. Explain any new word in five words or fewer ("front matter: the name and description block").
- Never read `~/.shipyard/secrets.env` or `.env*` files, and never put a key in a skill. A skill that needs a key reads it from a file or variable the student fills in themselves.
- Read the student's code and agent chats only with a yes, and only the parts you need: file lists, READMEs, the instruction files (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules`), and summaries of chats, not whole transcripts. Say what you read.
- Publishing, pushing, opening pull requests on other people's repos and filling in submission forms: ask first, wait for a clear yes, once per action.
- Verify before saying done. Say what was checked and what was not.
- Helper agents: one model cheaper than yours, mechanical work only (listing files, running checks).

## 0. Find what they have

Check the current folder: is it a skill (`SKILL.md`), a plugin (a manifest in `.claude-plugin/` or `.cursor-plugin/`), Shipyard itself, an app, or empty? If they already have a skill, offer to check it first: `node "${CLAUDE_PLUGIN_ROOT}/scripts/skill-scaffold.mjs" check <folder>`, and read the result as ticks and crosses.

## 1. Interview

Read `references/interview.md`. At most 5 questions, about outcomes: what job the skill does, who uses it, what words they type when they want it, what "done" looks like, and what it must never do. Rambling answers are fine; you write the spec.

## 2. Push back, then let them choose

Read `references/pushback.md` and check the spec against it. If something is weak (too broad, duplicates a skill they already have, needs keys in the chat, publishes without asking, could be a one-line rule instead), say so in one or two sentences, give your better version, and ask which they prefer. Their choice wins unless it is unsafe; then say plainly why you will not build that part.

## 3. Recommend where to build it

Read `references/build-or-extend.md`. First check `references/external-skills.md`: if a good existing skill already does the job, point to it instead of building (install only with their yes). With their yes, look at their codebase and agent chats (the instruction files, recent work, and repeated requests or mistakes in the chats). Recommend one of three, with one line of why:

1. **A new skill inside Shipyard** (it is about building, publishing or running web apps the Shipyard way).
2. **A new plugin built on Shipyard's shape** (their own name and repo, Shipyard's rules, tests and installer pattern).
3. **A plugin from scratch** (unrelated to apps, or they want nothing Shipyard does).

## 4. Write the spec

Write a short spec in the chat: name (lowercase words joined by dashes), the description with its trigger phrases, the steps, the rules, the scripts it needs (if any), and the tests. Read `references/anatomy.md` for what a good SKILL.md looks like. Ask "Shall I build this?" and wait.

## 5. Build it

- From scratch or as its own plugin: `node "${CLAUDE_PLUGIN_ROOT}/scripts/skill-scaffold.mjs" create <folder> --name <name> --description "<description>" --plugin` (leave out `--plugin` for a single skill). It writes the skill, a test, both plugin manifests, a README with install and publishing notes and a licence, and never overwrites a file that is there.
- Inside Shipyard: read `references/in-shipyard.md` and follow it (the Codex and Cursor copy, the rewrite table, version and README).
- Then fill in the real steps. Keep SKILL.md under about 100 lines; detail goes in `references/`. Anything a script can check, a script checks.

## 6. Test it

Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/skill-scaffold.mjs" check <folder>` and the skill's own tests (`node --test tests/*.test.mjs`). Then try it for real: start a new session, type one of the trigger phrases and see that the skill starts. Turn every lesson from the try into a rule or a test (`references/anatomy.md`, "Lessons"). After fixing review findings, review the fixed code again.

## 7. Publish

Read `references/publish.md`. Show the list of places, what each one needs, and which are automatic. Ask before each one. Bump the version and add a "What changed" line on every release.

## Done when

- `skill-scaffold.mjs check` is all ticks, the tests pass, and the skill started from a trigger phrase in a fresh session.
- The student knows how to install it, how to update it and where it is published.
