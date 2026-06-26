# LDM OS: Architecture Decisions

**Date:** 2026-02-26
**Source:** Parker + CC conversation during Memory Crystal Phase 2 docs session

## LDM OS Is a Product

LDM OS is not just a description of what your machine looks like after setup. It's a codebase. An installer. The entry point.

"How do you install LDM OS?" You run one command. It sets up Memory Crystal, Dream Weaver, scaffolds `~/.ldm/`, wires up hooks for whatever harness you're using.

## Two Components, One Install

```
LDM OS (entry point, installer)
  ├── Memory Crystal (learning)
  │     capture, search, embeddings, transcripts, sync
  └── Dream Weaver (dreaming)
        relearning, journals, boot sequence, narrative, identity
```

Memory Crystal and Dream Weaver are separate repos, separate packages. LDM OS pulls them together. One install command delivers everything.

## Harness-Agnostic Design

The whole point of LDM OS is that it works with any harness.

- **OpenClaw** is a harness. It wraps model APIs, manages sessions, runs plugins and hooks.
- **Claude Code** is also a harness. Different runtime, different interface, same concept.
- **Codex, Cursor, whatever comes next** ... also harnesses.

LDM OS sits above all of them. `~/.ldm/` doesn't care which harness is running. Any harness can read from it and write to it.

## Agent ID Convention

Agent IDs encode platform, agent name, and machine location:

- **OpenClaw agents:** `oc-{agent}-{machine}` ... `oc-lesa-mini`, `oc-lesa-air`
- **Claude Code agents:** `cc-{machine}` ... `cc-mini`, `cc-air`

This matters for multi-agent, multi-machine setups. Each agent gets its own directory under `~/.ldm/agents/{id}/` with isolated transcripts, sessions, daily logs, journals, and identity files. Search spans all agents by default.

## Identity Is Memory

Parker's insight: identity is not a separate system from memory. Your identity IS your memories.

Think about a human. You don't have a "memory module" and a separate "identity module" in your brain. Your preferences, values, how you talk, what you care about, who you trust ... all of that is just memory that's been reinforced over time. You are what you remember.

SOUL.md isn't an identity file. It's a memory file. A collection of things the agent has learned about itself, crystallized into a document. CONTEXT.md is recent memory. Journals are episodic memory.

This is why Memory Crystal handles identity scaffolding too. `crystal init` creates the directories where identity files live, because identity is just persistent memory with a name.

## Why Separate Repos

The repos are documentation boundaries, not product boundaries.

Dream Weaver is a concept. The paper, the protocol spec, the explanation of how relearning works ... that stays in its own repo because it's easier for an LLM to read one focused document than to dig through a monorepo. Context windows work better with focused documents.

Same principle as writing SOUL.md as its own file instead of appending it to a giant config.

Three repos. Clear boundaries. One install:
- **`memory-crystal`** ... the learning infrastructure
- **`dream-weaver-protocol`** ... the relearning process
- **`wip-ldm-os`** ... the installer that delivers both
