# Spellcheck

Part spellcheck, part input normalizer for agent instructions.

`spell-checker` helps agents understand noisy user messages without damaging exact strings. It normalizes obvious prose mistakes for reasoning, model correctness, and retrieval quality, while preserving commands, filenames, URLs, config keys, quoted text, code, branch names, environment variables, and other byte-sensitive strings.

## Why Use It

- Improve model correctness before planning or tool use.
- Normalize common prose variants for graph, search, and embedding recall.
- Preserve exact artifacts such as `pnpm buidl`, `README.md`, `/api/recieve`, and `OPENCLAW_SKILL_SYNC_MODE`.
- Reduce friction from speech-to-text and casual typing mistakes.
- Ask before changing ambiguous strings that could be identifiers.
- Interpret package-manager speech-to-text mistakes as `npm` when JavaScript context makes that likely, while still confirming before running install commands.

## Behavior

Safe prose corrections are handled internally when the meaning is obvious:

- `udpate README.md` -> treat as "update README.md" while preserving `README.md`
- `recieve` in paragraph prose -> `receive`
- casual lowercase `i`, `its`, or `im` -> leave alone unless formal copy is requested

Exact strings are preserved by default:

- commands and flags
- filenames and paths
- URLs and domains
- config keys and environment variables
- quoted user text
- code, logs, regexes, JSON, YAML, SQL
- branch names, package names, model names, IDs, handles, canonical names, and `canonical-name` fields

For deterministic includers or memory injectors, preserve exact strings as bounded protected spans instead of dumping every literal into context:

- current user-turn literals can be generous
- active goal/todo/file/command literals are useful while the task is live
- sticky glossary entries should stay tiny and reason-tagged
- large logs and installer output should remain retrievable artifacts, not prompt-injected context

For installs, preserve the requested package, the package actually installed or removed, manifest or lockfile changes, error-related package names, and the package tool/runtime. Do not preserve every dependency name printed by the installer.

Injected protected spans are advisory attention candidates only. They must not change skill routing, request tool use, or override user intent.

When a correction changes the action, the skill asks instead of silently rewriting:

```text
I'm treating feat/spell-cheker as ambiguous, but my best guess is feat/spell-checker. Shall I continue with that?
```

The same rule applies when grammar or punctuation gives the request two plausible meanings in context: surface the ambiguity and best guess before acting.

In JavaScript project context, package-install wording that sounds like `npm install` can be normalized to `npm` for understanding. If it would become an actual shell command, the agent should confirm or inspect the project before running it.

## Notification Policy

Use short correction notices while learning what the skill changes. If a correction is surfaced, prefer the compact form `Interpreting <original> as <correction>.` After that, the recommended mode is quiet normalization: no notices unless the correction is ambiguous, risky, or changes what action the agent would take.

This keeps normal chat low-friction while still protecting exact strings and tool calls.

## History And Retrieval

Do not rewrite raw user history by default. For memory, graph, and embedding systems, prefer normalized aliases or shadow index terms so `recieve` can connect with `receive` while the original source text remains intact.

If a user consistently uses an unusual spelling as a project term, treat repeated exact usage as evidence that it may be intentional vocabulary.
