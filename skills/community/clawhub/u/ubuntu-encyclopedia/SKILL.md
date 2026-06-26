---
name: ubuntu-encyclopedia
description: >-
  Ubuntu documentation-first workflow for Ubuntu-specific questions,
  maintenance, updates, upgrades, package management, system administration,
  service troubleshooting, networking, storage, logs, release behavior, and
  diagnostics. Use when the request materially depends on Ubuntu or
  Ubuntu-specific tooling/behavior such as Ubuntu release behavior,
  `apt`/`apt-get`/`dpkg`/`snap`, `systemd`/`systemctl`/`journalctl`, Netplan,
  NetworkManager, package repair, repository/key issues, service failures,
  boot issues, mounts/`fstab`, permissions, users/groups, or non-trivial
  Ubuntu maintenance/troubleshooting. Do not use for generic shell, git,
  Python, Docker, or Linux questions unless Ubuntu-specific semantics matter.
metadata: {"openclaw":{"emoji":"🟠","homepage":"https://manpages.ubuntu.com/manpages/","os":["linux"]}}
---

# Ubuntu Encyclopedia

## Overview

Use a docs-first workflow for Ubuntu-specific work. Prefer Ubuntu manpages at `https://manpages.ubuntu.com/manpages/` for command and utility behavior, use official Ubuntu documentation when the task is broader than a manpage, consult cached local copies under `.Ubuntu-Encyclopedia/` before re-fetching, and record useful authoritative excerpts plus environment-specific operational learnings so future work gets faster and safer.

This skill is for the **Ubuntu distro/admin layer**. It should trigger for Ubuntu-specific package, service, networking, storage, and release-behavior questions — not for generic Linux/shell/dev tooling questions that merely happen to be asked from an Ubuntu machine.

## Workflow

1. **Classify the task**
   - Decide whether the task is an Ubuntu-specific question, maintenance task, troubleshooting task, command-planning task, upgrade/update task, or live admin task.
   - Use this skill when the task materially depends on Ubuntu-specific behavior, Ubuntu administration knowledge, Ubuntu package/service behavior, or command semantics that should be verified from manpages or official Ubuntu docs.
   - Do not use this skill for generic shell work, generic Docker/git/Python work, or generic Linux questions that merely happen to be on Ubuntu when Ubuntu-specific semantics do not matter.

2. **Check local cache first**
   - Use `.Ubuntu-Encyclopedia/` as the local knowledge/cache root.
   - Check these locations first when relevant:
     - `.Ubuntu-Encyclopedia/manpages/manpages.ubuntu.com/...`
     - `.Ubuntu-Encyclopedia/docs/...`
     - `.Ubuntu-Encyclopedia/notes/components/...`
     - `.Ubuntu-Encyclopedia/notes/patterns/...`
     - `.Ubuntu-Encyclopedia/inventory/...`
   - If a cached page or note already answers the question well enough, use it.

3. **Consult authoritative Ubuntu sources before answering or acting**
   - Before answering direct or indirect Ubuntu questions that depend on command syntax, package behavior, service behavior, configuration semantics, or version-sensitive distro details, consult the relevant authoritative source unless the answer is already well-supported by the local cache.
   - Prefer sources in this order:
     1. Ubuntu manpages for command and utility behavior
     2. Official Ubuntu docs for broader workflows and distro-specific guidance
   - Before performing non-trivial Ubuntu maintenance or troubleshooting work, consult the relevant docs first when:
     - the exact command semantics matter
     - service/package behavior is easy to misremember
     - the action could affect package state, service health, networking, storage, bootability, or access
   - Do not improvise high-impact Ubuntu admin commands from memory when the docs are easy to check.

4. **Cache consulted docs locally**
   - When you consult a manpage, save a normalized cache copy under `.Ubuntu-Encyclopedia/manpages/manpages.ubuntu.com/...`.
   - When you consult broader Ubuntu docs, save a normalized cache copy under `.Ubuntu-Encyclopedia/docs/...`.
   - Mirror the official path structure as much as practical.
   - Cache only pages actually consulted; do not try to mirror the whole docs site eagerly.
   - Use `scripts/cache_manpage.py` or `scripts/cache_doc.py` when appropriate.

5. **Separate authoritative documentation from local observations**
   - Store manpage-derived material under `.Ubuntu-Encyclopedia/manpages/...`.
   - Store other official-doc-derived material under `.Ubuntu-Encyclopedia/docs/...`.
   - Store environment-specific operational knowledge under:
     - `.Ubuntu-Encyclopedia/notes/components/`
     - `.Ubuntu-Encyclopedia/notes/patterns/`
     - `.Ubuntu-Encyclopedia/inventory/`
   - Distinguish clearly between:
     - authoritative documentation
     - observed local configuration/state
     - inferred best-practice guidance

6. **Record useful local learnings**
   - After useful live work, save durable notes such as:
     - package/service management patterns
     - host-specific quirks
     - repeated repair/maintenance sequences
     - networking/storage/admin gotchas
     - safe/unsafe operational boundaries for the environment
   - Prefer concise durable notes over re-learning the same Ubuntu-specific details later.

## Live Work Rules

- Treat manpage/docs lookup as the default preflight for non-trivial Ubuntu work.
- Prefer read/inspect first when entering an Ubuntu area you have not recently reviewed.
- Treat release upgrades, package repair, service/network/storage changes, and boot-impacting admin work as high-sensitivity areas.
- When uncertainty remains after checking cache + docs, say so and avoid bluffing.
- When answering a question, mention when useful whether the answer comes from cached manpages, cached official docs, a fresh lookup, or live observed environment state.

## Data Root

Use this workspace-local root for cache and notes:

- `.Ubuntu-Encyclopedia/`

Expected structure:

- `.Ubuntu-Encyclopedia/manpages/manpages.ubuntu.com/...`
- `.Ubuntu-Encyclopedia/docs/...`
- `.Ubuntu-Encyclopedia/notes/components/...`
- `.Ubuntu-Encyclopedia/notes/patterns/...`
- `.Ubuntu-Encyclopedia/inventory/...`

Use `scripts/init_workspace.py` to create or repair the expected directory structure.

## Note Destinations

- Component-specific observations → `.Ubuntu-Encyclopedia/notes/components/<component-name>.md`
- Reusable Ubuntu patterns/gotchas → `.Ubuntu-Encyclopedia/notes/patterns/<topic>.md`
- Environment-wide deployment/access info → `.Ubuntu-Encyclopedia/inventory/*.md`
- Cached manpages → `.Ubuntu-Encyclopedia/manpages/manpages.ubuntu.com/...`
- Cached official docs → `.Ubuntu-Encyclopedia/docs/...`

## Secrets / Sensitive Data

- Do not store plaintext credentials, API keys, session tokens, private URLs, recovery codes, or other secrets in the encyclopedia notes/inventory tree.
- If a note needs to mention access details, keep it high-level and redact or omit secret material.
- Treat these workspace notes as operational memory, not as a secrets vault.

## Resources

- `scripts/init_workspace.py` — create or repair the `.Ubuntu-Encyclopedia/` directory tree.
- `scripts/cache_manpage.py` — fetch and cache a consulted Ubuntu manpage under `.Ubuntu-Encyclopedia/manpages/...`.
- `scripts/cache_doc.py` — fetch and cache a consulted official Ubuntu docs page under `.Ubuntu-Encyclopedia/docs/...`.
- `references/workflow.md` — detailed operating workflow and evidence-handling rules.
- `references/cache-layout.md` — canonical `.Ubuntu-Encyclopedia/` directory structure.
- `references/topic-map.md` — useful Ubuntu topic groupings for faster authoritative lookup.

## Good Outcomes

- Answer an Ubuntu-specific question using cached or freshly checked manpages/docs instead of guesswork.
- Inspect a live Ubuntu host after checking the relevant docs and record any new local operational knowledge.
- Build a growing local Ubuntu knowledge cache that makes later work faster, safer, and more grounded.
- Turn one-off Ubuntu discoveries into durable notes so future work does not rediscover them from scratch.

## Avoid

- Triggering on generic shell work that is not materially Ubuntu-specific.
- Answering Ubuntu-specific questions purely from memory when authoritative sources are easy to consult.
- Treating local observed behavior as if it were guaranteed authoritative documented behavior.
- Dumping large amounts of low-value docs into the workspace without a reason.
- Making high-impact live changes before checking the relevant docs when exact behavior matters.
