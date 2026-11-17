---
title: "Installer should expose stable beta and alpha track choices"
status: in-review
priority: P1
owner: unassigned
repo: wip-ldm-os-private
created: 2026-05-11
---

# Installer Should Expose Stable Beta And Alpha Track Choices

## Problem

The public install spec is a single file. It is not split into alpha, beta, and stable variants.

That means the install prompt should not hardcode one track forever. The installer and prompt should discover what tracks are available, explain the installed state, and let the user choose the track they want.

Current confusion:

- public and private docs can drift on whether examples say `--alpha` or `--beta`;
- alpha, beta, and stable are all public npm dist-tags, even if alpha is mostly internal canary work;
- a user may explicitly ask for "latest alpha" or "latest beta", but the prompt still reads like one generic install flow;
- release notes placement is mixed with install-track messaging, which makes it unclear which notes should ship publicly.

## Expected Product Behavior

When an agent reads an install spec for a WIP package, it should check local installed state and available npm dist-tags before asking the user to install.

For a package like `wip-codex-remote-control`, the agent should be able to say:

```text
Installed:
wip-codex-remote-control@0.0.4-alpha.2

Available:
stable/latest: 0.0.2-alpha.2
beta: 0.0.5-beta.1
alpha: 0.0.4-alpha.3

Which track do you want to install?
- stable
- beta
- alpha
```

If the user already said a track explicitly, the installer should not force a generic chooser.

Examples:

```text
install latest alpha
install alpha
install latest beta
install beta
install current
install stable
```

Those should map to the right command:

```bash
ldm install --alpha wip-codex-remote-control
ldm install --beta wip-codex-remote-control
ldm install wip-codex-remote-control
```

Before running a real install, the agent should show the exact package and track it is about to install.

## Required Installer Behavior

1. `ldm install` should support a track-aware query and explanation flow for `latest`, `beta`, and `alpha`.
2. The install spec should tell agents to report installed version and all available tracks before asking for an install decision.
3. Natural language track requests should skip the generic chooser once the requested track is clear.
4. The installer should disclose risk by track:
   - stable/latest: normal public path;
   - beta: public prerelease test path;
   - alpha: canary path, likely rougher, but still installable if the user asks.
5. The single public install spec should stay single-file. Do not create separate alpha and beta install spec files.

## Remote Control README And Install Spec Follow-Up

The Remote Control README prompt is part of this bug because users dogfood by copying the whole README prompt, not just the raw `.txt` URL.

Required alignment:

- Update the source README in the private working repo:

```text
/Users/lesa/wipcomputerinc/repos/ldm-os/apps/wip-codex-remote-control-private/README.md
```

- Keep the README prompt short for humans.
- The README should say: "tell me what version I have and tell me what's available."
- Do not put the stable, beta, and alpha command matrix in the README prompt.
- Put the detailed track rules in the install spec source, which is the private repo `SKILL.md` and the served `https://wip.computer/install/wip-codex-remote-control.txt`.
- The install spec should tell the agent to check installed state, read npm dist-tags, show stable/current, beta, and alpha availability, then ask which track the user wants.
- Preserve natural-language shortcuts such as "install latest alpha" and "install latest beta" in the install spec.
- Update the public README only through the normal private-to-public release or sync path. Do not clone or patch `wipcomputer/wip-codex-remote-control` directly.

The public mirror must eventually show the same short README prompt, but the edit must originate in the private source repo.

## Release Notes Placement Dependency

The installer behavior depends on release-note placement being clear.

Policy to encode in the related release-pipeline work:

- Public beta and stable release notes can live outside `ai/` and can ship to the public repo and GitHub Releases.
- Alpha and internal canary notes should live under `ai/`, not in the public mirror.
- For Remote Control, the concrete internal notes folder is:

```text
/Users/lesa/wipcomputerinc/repos/ldm-os/apps/wip-codex-remote-control-private/ai/release-notes-private
```

The installer ticket should not own the full release-note migration, but it should depend on that policy so install prompts do not mix public track guidance with internal canary notes.

## Acceptance

- Install specs can instruct agents to list installed, stable/latest, beta, and alpha versions.
- `ldm install` supports the selected track without requiring separate public install spec files.
- "install latest alpha" maps to the latest alpha install path.
- "install latest beta" maps to the latest beta install path.
- "install current" and "install stable" map to the stable/latest install path.
- The agent shows the exact target package, version, and track before installing.
- Alpha remains visible as an available track, but is labeled as canary or internal validation.
- A release-pipeline follow-up covers public versus private release-note placement, including Remote Control alpha notes under `ai/release-notes-private`.
- Remote Control README prompts are updated from the private source repo and then reflected in the public mirror through the approved sync path.
- The served install spec carries the detailed stable, beta, and alpha command mapping.
- No direct public repo edits are part of the fix.
- No em dashes are introduced.

## LDM OS Port (Canonical Pattern)

This ticket originally listed `wip-codex-remote-control` as the only example, and the implementing work (release notes: `apps/wip-codex-remote-control-private/ai/release-notes-private/2026-05-11--codex--install-prompt-split-alpha.md`) landed only on the Codex Remote Control SKILL.md. The canonical install-prompt pattern is owned by LDM OS, not by Codex Remote Control. The work landed in the wrong place first.

The LDM OS SKILL.md (`wip-ldm-os-private/SKILL.md`) has no Tracks section, no `npm view @wipcomputer/wip-ldm-os dist-tags` step, and no natural-language track translation. Its install command at line 105 is hard-coded to `npm install -g @wipcomputer/wip-ldm-os@latest`. The 2026-05-13 dogfood (CC and Codex sessions both following `https://wip.computer/install/wip-ldm-os.txt`) reproduced the gap: neither session offered alpha/beta/stable choice, and the CC session misreported that running the install command would preserve the user's alpha pin (it would not; `@latest` downgrades alpha.27 to 0.4.84 stable).

### Required additions to `wip-ldm-os-private/SKILL.md`

Port the four sections from `apps/wip-codex-remote-control-private/SKILL.md`, adjusted for LDM OS as the package:

1. **`## Tracks`** section: name stable/beta/alpha, map each to `ldm install`, `ldm install --beta`, `ldm install --alpha`. Match the structure of CRC SKILL.md lines 68-108. Note: LDM OS installs itself, not a sub-package, so there is no positional package argument in the install commands.
2. **`### Pick the right track`**: instruct the AI to run `npm view @wipcomputer/wip-ldm-os dist-tags --json`, read the output, translate to track names + versions in plain English. Include the "do not paste raw JSON" rule. Match CRC SKILL.md lines 76-108.
3. **`### How to phrase the track to the user`**: language map plus user-facing message templates for install-state report ("You have `<LOCAL>` installed. Available: stable/current..."), named-track responses, the `@latest`-resolves-to-a-prerelease case, track risk language, and anti-patterns ("do not print raw npm dist-tags JSON," "do not use `latest` as a synonym for newest prerelease," etc.). Match CRC SKILL.md lines 110-146 (the full section). "stable / current / latest" → stable install; "beta / latest beta" → `--beta`; "alpha / latest alpha" → `--alpha`.
4. **`## Track caveats`**: track-by-track risk language (alpha is canary, breakage-possible, opt-in only; beta is stabilization candidate, feature-frozen; stable is production). Match CRC SKILL.md lines 532-544. Note: the `@latest`-resolves-to-a-prerelease handling is NOT in this section; it lives in the "Pick the right track" section (line 84) and the "How to phrase the track to the user" section (lines 128-130), which bullets 2 and 3 already cover.

Replace the hard-coded `@latest` install command at LDM OS SKILL.md line 105 with track-aware variants per the language map above.

### Test alignment

Add a regression test at `wip-ldm-os-private/scripts/test-readme-install-prompt.mjs` (or fold into the existing `scripts/test-install-prompt-policy.mjs`) modeled on `apps/wip-codex-remote-control-private/test/readme-install-prompt.test.mjs`. The test must assert:

- README install prompt stays short: it does NOT contain `Track choices:`, `ldm install --alpha`, `ldm install --beta`, `ldm install --dry-run`.
- README install prompt delegates to the install document.
- The track-selection logic lives in `wip-ldm-os-private/SKILL.md`, not in the README.

Wire the test into `prepublishOnly` per the same pattern PR #938 used for `test:legacy-npm-sources-migration`.

### Canonical pattern ownership (rule)

The Codex Remote Control implementation is downstream of LDM OS. Cross-cutting install-prompt and SKILL.md patterns land in `wip-ldm-os-private` first and propagate to child products. Child-first implementations leave the parent out of date with its own descendants. The 2026-05-11 implementation order (CRC first, LDM OS never) is the failure mode to avoid. Captured in `wip-ldm-os-private/CLAUDE.md` under "Canonical pattern ownership."

## Non-Goals

- Do not create separate alpha, beta, and stable install spec files.
- Do not hide alpha from users who explicitly ask for it.
- Do not change npm dist-tag semantics.
- Do not solve the entire release-note archive policy in this installer ticket.
