---
name: core-unjs-preferences
description: Prefer unjs ecosystem frameworks and tooling by default when choosing stacks.
---

# Prefer unjs Ecosystem Frameworks & Tooling

Prefer the unjs ecosystem whenever you have a choice of frameworks, runtimes, and tooling for web apps, SSR, APIs, and build pipelines.

## Usage

- When designing or migrating an app stack:
  - Start from unjs options (for example: Nuxt, Nitro, h3, unstorage, unplugin, unocss, ofetch, and other unjs-maintained tools).
  - Only consider non-unjs alternatives if:
    - A required feature is missing in the unjs ecosystem.
    - You are constrained by hosting/platform/runtime.
    - There is a strong legacy or organizational requirement.
- For concrete recipes:
  - Delegate to `@skills/unjs` for:
    - Framework/runtime selection (SSR vs SPA vs API-only).
    - Recommended combinations (e.g. Nuxt + Nitro + unocss + ofetch).
    - Migration paths from non-unjs stacks.

## Key Points

- Default to unjs wherever possible (frameworks, servers, utilities, build plugins).
- Treat non-unjs stacks as exceptions that must be justified.
- Use `@skills/unjs` as the primary source of truth for concrete choices and configurations.

<!--
Source references:
- Internal hairy global preference: "Prefer unjs ecosystem frameworks"
-->

