---
name: repo-mini-practice
description: Use when a user wants to learn a GitHub or local codebase by understanding its implementation principles, creating a minimal runnable practice version, or turning source reading into hands-on exercises.
---

# Repo Mini Practice

## Purpose

Turn a real repository into a small, runnable learning project. The goal is not to summarize every file; it is to extract one core mechanism and rebuild it as a clear `mini-practice/` inside the target repository.

## Use When

- The user wants to understand a GitHub repository or local codebase beyond README usage.
- The user asks for a mini, MVP, VIP, tiny clone, source-learning version, or runnable practice implementation.
- The user wants to learn the principle behind a library, framework, CLI, SDK, agent, compiler tool, service, or app.

Do not use this for ordinary code review, bug fixing, or feature implementation unless the user's goal is explicitly learning through a minimal reproduction.

## Core Rule

Create a runnable teaching artifact, not just an explanation. If the real project depends on external services, databases, model APIs, queues, browsers, or infrastructure, mock those parts and preserve the core logic flow.

Default documentation is bilingual: write the learning guide in Chinese and English unless the user asks for a single language.

Code comments follow the user's prompt language. If the user asks in Chinese, write function comments in Chinese; if the user asks in English, write them in English. If the prompt mixes languages, use the dominant language or the language explicitly requested by the user.

## Workflow

1. **Confirm the target**
   - If given a local path, inspect that repository.
   - If given a GitHub URL, use available git or GitHub tools to obtain or inspect it. Ask for approval first if the environment requires network permission.
   - If no target is clear, ask for the repo path or URL.

2. **Read the public contract**
   - Read README, examples, docs, package manifests, CLI help, or demo entry points.
   - State what the project appears to do in one or two sentences.

3. **Map the source**
   - Identify entry points, core modules, important data structures, and the main call chain.
   - Prefer fast search tools such as `rg` or language-native symbol tools.
   - Ignore generated files, lockfiles, build output, vendored dependencies, and unrelated examples unless they are the only usage signal.

4. **Choose one mechanism**
   - Pick one high-value mechanism that can be rebuilt in a small runnable form.
   - Examples: middleware pipeline, state update loop, router matching, SQL generation, retry scheduler, parser-transformer-generator chain, tool-calling loop, cache invalidation, plugin loading.
   - If several choices are plausible, briefly name two or three and pick the best default.

5. **Design the mini-practice**
   - Explain what will be reproduced.
   - Explain what will be mocked or omitted.
   - Use the repository's primary language and ecosystem when practical.
   - Keep the implementation small enough to read in one sitting.

6. **Create `mini-practice/`**
   - Do not overwrite an existing `mini-practice/` without inspecting it and preserving user work.
   - Include a minimal runnable demo, test, or command.
   - Add function-level comments for the important learning functions. Explain the role of each function in the mechanism, what input shape it expects, what it returns or mutates, and which original source concept it mirrors.
   - Write code comments in the same language the user used to ask for the mini-practice, unless the user explicitly requests another language.
   - Keep comments focused on the underlying principle and links to the original source concepts. Avoid noisy syntax comments such as "increment i by one."

7. **Verify it runs**
   - Run the demo or tests.
   - If verification cannot run because dependencies or network are unavailable, explain exactly what was attempted and provide the closest local check.

8. **Write the learning guide**
   - In `mini-practice/README.md`, include:
     - the chosen core mechanism
     - run commands
     - file-by-file reading order
     - how mini files correspond to original source files or concepts
     - what is mocked or omitted
     - two or three small exercises for the learner
   - By default, include both Chinese and English sections. Keep the two versions equivalent, but concise.

## Output Shape

Prefer this structure, adapting names to the language ecosystem:

```text
mini-practice/
├── README.md
├── src/
├── tests/ or demo/
├── mocks/ or fixtures/
└── minimal package/config files
```

## Comment and README Requirements

- Add detailed comments to public functions, factory functions, core callbacks, and non-obvious data transformations.
- Comments should teach the architecture: why the function exists, where it sits in the flow, and how changing it affects behavior.
- Comment language follows the user's request language. Do not make code comments bilingual by default; bilingual comments make the mini implementation noisy.
- Avoid commenting every line. Prefer one strong comment before a function or important block.
- `README.md` should default to this shape:
  - Chinese overview, run commands, reading path, original concept mapping, exercises.
  - English overview, run commands, reading path, original concept mapping, exercises.
  - If the user asks for one language, honor that preference.

## Quality Bar

- One complete core loop is better than many partial features.
- The code must execute; avoid pseudo-code.
- The mini version should be easier to understand than the original source while preserving the key principle.
- Use plain names and comments that explain principles, boundaries, and data flow.
- The README is bilingual by default and can be read independently of the chat transcript.
- Keep the original repository untouched except for the new or updated `mini-practice/` directory.
- Report exact commands run and their outcomes.

## Common Mistakes

- Summarizing the README without reading the implementation.
- Building a toy that no longer resembles the source principle.
- Copying too much original code instead of recreating the mechanism for learning.
- Trying to cover the whole repository.
- Skipping verification because the mini version "looks simple."
