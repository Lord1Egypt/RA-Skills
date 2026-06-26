# Bug: Merge, Deploy, and Install are conflated

**Filed by:** CC-Mini + Parker on 2026-03-13
**Severity:** High. Agents bypass dogfooding by deploying directly to extensions.

---

## The Problem

There are three distinct steps in the release workflow, but agents (and tooling) treat them as one:

| Word | What it means | What happens |
|------|--------------|-------------|
| **Merge** | Development done. PR merged to private main. | Code lands on the private repo's main branch. Nothing else changes. |
| **Deploy** | Ship to public. | `wip-release` (version bump, npm publish, GitHub release) + `deploy-public.sh` (sync to public repo). The package is available to the world. Still not on our machine. |
| **Install** | Put it on our system. | `crystal init` (or equivalent) runs. Extensions updated. Hooks configured. We're dogfooding the new version. Only happens when Parker says "install." |

Today (2026-03-13), a CC session:
1. Merged a PR to memory-crystal-private (correct)
2. Ran `wip-release patch` and `deploy-public.sh` (correct)
3. Then ran `cp -r dist ... ~/.ldm/extensions/memory-crystal/` and `npm install -g memory-crystal` (WRONG)

Step 3 is installing. It should only happen when Parker runs the install prompt and says "install." The agent skipped dogfooding by deploying directly to the extension directories.

A previous CC session also ran `npm link` from the private repo, which made every repo change instantly update the production tool. Same conflation: development = production.

## Why This Matters

We always dogfood our own software. The install prompt exists so Parker can:
- See what's new
- Review the dry run
- Decide to install
- Test the install flow itself

If agents deploy directly to extensions, the install prompt says "already up to date" and the dogfooding loop is broken. We never test the actual install experience.

## What Needs to Change

### 1. Dev Guide update

Add to the Dev Guide (both private and public versions):

```
## Merge, Deploy, Install

These are three separate steps. Never combine them.

Merge ... PR merged to private main. Development is done.
Deploy ... wip-release + deploy-public.sh. Package is published. Available to the world.
Install ... crystal init (or equivalent). Updates the running system. Only when Parker says "install."

After Deploy, STOP. Do not copy files to ~/.ldm/extensions/ or ~/.openclaw/extensions/.
Do not run npm install -g. Do not run npm link. Do not touch the installed system.

Parker tests the install flow by running the install prompt. That's how we dogfood.
```

### 2. Tooling guardrails

- `wip-release` should NOT auto-deploy to extensions after publishing
- Add a check: if the agent tries to `cp` to `~/.ldm/extensions/` or `~/.openclaw/extensions/` after a release, warn
- The file guard could potentially catch `cp` to extension directories (but that may be too aggressive)

### 3. Agent instructions

Add to CLAUDE.md and the Dev Guide:

```
After merging and deploying (wip-release + deploy-public.sh), your job is done.
Do NOT install the new version. Do NOT copy files to extension directories.
Tell Parker: "v0.X.Y is published. Run the install prompt when you're ready to update."
```

### 4. `npm link` prevention

`crystal doctor` should check if the global binary is npm-linked to a repo and warn. This was filed separately (memory-crystal-private issue #50).

## The Dogfooding Rule

Every install goes through the install prompt. No exceptions. If the prompt doesn't work, that's a bug in the prompt. If `crystal init` doesn't handle the upgrade, that's a bug in the installer. We find these bugs by dogfooding, not by bypassing.
