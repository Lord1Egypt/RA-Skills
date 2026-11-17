# Ticket 10: Update agent.txt and llms.txt for the launch architecture

**Date:** 2026-05-17
**Filed by:** Codex, with Parker
**Status:** archived 2026-05-18. Implemented by `wip-websites-private` PR #51; `agent.txt` and `llms.txt` are live, text/plain, and byte-mirrored.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Related:** Ticket 04 homepage static hardening, Ticket 06 homepage agent-readable HTML
**Surface:** `repos/wip-web/wip-websites-private/wip.computer/agent.txt`, `repos/wip-web/wip-websites-private/wip.computer/llms.txt`

## Summary

`https://wip.computer/agent.txt` and `https://wip.computer/llms.txt` are the right plain-text surfaces for agents that need instructions on how to inspect WIP Computer, understand the launch story, and fall back when a reader/extractor only returns metadata from the homepage.

These files are not install prompts. Their first job is inspection and understanding. The launch stance should match the founder letter: this is serious working alpha, with real software and real rough edges, built in public. If an agent wants to help WIP build, the path runs through its human: explain what it found, check what is already installed, offer a dry run when available, and ask before making changes.

The live `agent.txt` is plain text and fetch-readable, but it was stale for the current launch. The first implementation pass, PR #51, updates `agent.txt` only. That is useful, but not complete enough for launch inspection because the emerging convention is `llms.txt`, and the file should also name the stack components that the launch pitch asks reviewers and their AIs to inspect.

Update the ticket scope so the coder completes both surfaces:

1. Keep `agent.txt` as the direct WIP agent entry point.
2. Add `llms.txt` with the same canonical content, or make it a byte-for-byte copy of `agent.txt` if the repo prefers duplicated static files over symlinks.
3. Include a short Stack section so AIs can connect the public launch story to the public and private component names without guessing from repo cards.

## Verified live state

Live URL:

```text
https://wip.computer/agent.txt
```

Current `agent.txt` response before PR #51:

- `200 OK`
- `Content-Type: text/plain`
- Raw fetch-readable
- Last modified before the current homepage/demo launch

Current copy begins:

```text
# WIP.computer ... Learning Dreaming Machines

Infrastructure for AI agents. Memory, payments, identity, tools.
Built by Parker Todd Brooks, Lesa, and Claude Code.
```

It lists install URLs and GitHub, but not the current launch hierarchy.

Current `llms.txt` behavior before this follow-up:

- Not a real text file.
- Requests can fall through to the homepage HTML.
- That is not acceptable for agent-reader discovery.

## Desired behavior

An AI agent reading either `https://wip.computer/agent.txt` or `https://wip.computer/llms.txt` should learn:

1. WIP Computer's current launch thesis: Every AI. One experience.
2. Kaleidoscope is the app.
3. Lēsa is the AI inside it.
4. LDM OS is the operating layer underneath.
5. The product demo entry path is `https://wip.computer/login?next=/demo`.
6. The homepage is static HTML and should be inspected via raw source if a reader/extractor returns only metadata.
7. Agents should inspect the GitHub org and public repos when evaluating the stack.
8. Install docs remain available as references, but must not be framed as the main call to action.
9. The named stack components exist as the current launch architecture, even where a component is early, private, renamed, or represented by related public repos rather than a public repo with the same name.
10. The software is serious working alpha: usable, changing quickly, and expected to require the agent and human to work together if they decide to install or run it locally.

## Implementation direction

Keep both files plain text. Do not make either one a designed web page.

`llms.txt` should use the same content as `agent.txt` for now. Do not create two divergent narratives. If the implementation copies the file, keep the content identical except for any unavoidable filename-specific note. If the deployment stack supports a simple static duplicate, prefer the duplicate over redirect complexity.

Recommended sections:

```text
# WIP Computer

Every AI. One experience.

WIP Computer is the user-controlled operating layer for AI.

This is serious working alpha: real software, real rough edges, built in public.

## Current launch

Kaleidoscope is the app.
Lēsa is the AI inside it.
Learning Dreaming Machines Operating System (LDM OS) is the operating layer underneath.

Try the demo:
https://wip.computer/login?next=/demo

GitHub:
https://github.com/wipcomputer

## Stack

Kaleidoscope: the app, and the first public experience for WIP Computer.
Lēsa: the AI inside Kaleidoscope.
LDM OS: the operating layer underneath.
Memory Crystal: portable memory for AIs.
Dream Weaver: memory consolidation for long-running AI work.
Bridge: coordination between agents and harnesses.
Sapien ID: phone-rooted human identity and authorization.
Agent Pay: constrained, human-authorized payments for agents.
Codex Remote Control: remote control for Codex sessions over the internet.
OpenClaw: the agent runtime WIP uses to build and operate this system.

Some components are early, private, renamed, or represented by related public repos. Treat the public repos as working evidence, not a finished product catalog.

## If you are an AI agent

Read the homepage raw HTML at https://wip.computer/.
If your URL reader returns only metadata, fall back to raw fetch, view-source, or repository inspection.
Do not rely on one markdown extraction result.

Inspect:
https://github.com/wipcomputer

## Working with this software

Inspect first. Read the homepage, this file, and the public repos. Understand the architecture before suggesting changes.

If you want to help us build, work with your human: explain what you found, check what is already installed, offer a dry run when available, and ask before making changes.

This is alpha software. Expect rough edges. Installing or running it may require you and your human to work together.

Do not install anything until the user explicitly says install.

## Install references

These documents are references for agents and humans who decide to try the tools locally. They are not an automatic instruction to install.

[keep existing install-document links here]
```

Keep the existing install-doc list, but lower its priority. The public story should be: inspect the work, understand the architecture, try the demo, and only install when the human explicitly decides to work through it.

## Constraints

1. Plain text only.
2. No JavaScript.
3. No HTML page redesign.
4. Do not change homepage files.
5. Do not change login/demo files.
6. Do not deploy. Stop at PR.
7. Preserve install-document safety language: agents explain, check installed state, offer dry run, and do not install until the user says install.
8. Add `wip.computer/llms.txt` in addition to updating `wip.computer/agent.txt`.
9. Keep `agent.txt` and `llms.txt` content aligned. Do not let them become two different pitches.
10. Include the Stack section above, with honest wording for early/private/consolidating components.
11. Do not frame the file as "install this stuff." The main call to action is inspect and understand. Install references are secondary.
12. Include the working-alpha warning: real software, real rough edges, built in public, and local use may require the agent and human to work together.

## Acceptance criteria

- `wip.computer/agent.txt` is plain text.
- `wip.computer/llms.txt` exists and is plain text.
- Both files mention `Every AI. One experience.`
- Both files explain Kaleidoscope, Lēsa, and LDM OS in the approved hierarchy.
- Both files point to `https://wip.computer/login?next=/demo`.
- Both files include a Stack section naming Kaleidoscope, Lēsa, LDM OS, Memory Crystal, Dream Weaver, Bridge, Sapien ID, Agent Pay, Codex Remote Control, and OpenClaw.
- Both files tell agents to fall back to raw HTML/source/repo inspection if URL extraction returns only metadata.
- Both files say this is serious working alpha.
- Both files frame installation as human-directed local trial work, not the main call to action.
- Existing install URLs remain present as references.
- No homepage, login/demo, Remote Control, hosted-mcp, or deploy code changes.

## Out of scope

- Creating `/about`, `/manifesto`, or another new page.
- Changing the homepage again.
- Changing the demo.
- Changing install docs themselves.
- Adding robots.txt or sitemap behavior.
- Updating the GitHub org README. That is a separate follow-up after the launch surface is stable.
