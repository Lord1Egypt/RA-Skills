# Plan: README Polish + MCP Examples

**Date:** 2026-03-10
**Author:** cc-mini
**Source:** GPT feedback (filtered), Grok feedback, Parker direction, notes/2026-03-10--cc-mini--readme-standard-and-universal-installer-vision.md
**Repo:** wip-ai-devops-toolbox-private

## Goal

Make the README and SKILL.md immediately useful for someone landing on the repo for the first time. Four concrete additions based on external feedback.

## Phase 1: 60-Second Golden Path (README)

Add a dead-simple install-and-verify sequence at the top of the README, right after the "Teach Your AI to Dev" section.

```
## Quick Start (60 seconds)

# Install the universal installer
npm install -g @wipcomputer/universal-installer

# Preview what will be installed
wip-install wipcomputer/wip-ai-devops-toolbox --dry-run

# Install everything
wip-install wipcomputer/wip-ai-devops-toolbox

# Verify: run one check from each major category
wip-license-guard check              # copyright compliance
wip-repo-permissions audit <org>     # visibility guard
wip-repos check                      # manifest reconciliation
```

**Status:** DONE

## Phase 2: Compatibility Matrix (README + SKILL.md)

Add a single table showing all tools and their interfaces. Data already exists; just needs consolidating.

| Tool | CLI | Module | MCP | OpenClaw | Skill | CC Hook |
|------|-----|--------|-----|----------|-------|---------|
| wip-universal-installer | Y | Y | - | - | Y | - |
| wip-release | Y | Y | Y | - | Y | - |
| wip-license-hook | Y | Y | Y | - | Y | - |
| wip-license-guard | Y | Y | - | - | - | - |
| wip-repo-permissions-hook | Y | Y | Y | Y | Y | Y |
| wip-file-guard | Y | Y | - | Y | Y | Y |
| wip-repos | Y | Y | Y | - | Y | - |
| deploy-public | Y | - | - | - | Y | - |
| post-merge-rename | Y | - | - | - | Y | - |
| LDM Dev Tools.app | - | - | - | - | - | - |

Put this in the README after the features list and in SKILL.md after the tool table.

**Status:** DONE

## Phase 3: "Can I Use This?" License Examples (README)

Add plain-English examples after the license code block:

```
### Can I use this?

**Yes, freely:**
- Use any tool locally or on your own servers
- Modify the code for your own projects
- Include in your internal CI/CD pipelines
- Run on your personal cloud instances

**Need a commercial license:**
- Bundle into a product you sell
- List on a marketplace (VS Code, JetBrains, etc.)
- Offer as part of a hosted/SaaS platform
- Redistribute commercially
```

**Status:** DONE

## Phase 4: MCP "Ask Your AI" Examples (README + SKILL.md)

Add concrete prompts for each MCP-callable tool. This is the killer feature.

```
## Talk to Your Tools

Once installed, your AI can call these directly:

"Scan all dependencies for license changes"
  -> calls license_scan

"Check if memory-crystal can go public"
  -> calls repo_permissions_check

"Do a patch release with notes 'fix login bug'"
  -> calls release

"Show me which repos aren't in the manifest"
  -> calls repos_check

"Audit the whole org's repo visibility"
  -> calls repo_permissions_audit
```

**Status:** DONE

## Phase 5: SKILL.md Auto-Staleness Check in wip-release

Add a check to `wip-release` that warns if SKILL.md version doesn't match the new version being released. Not auto-generate content (too complex), just flag it.

```
// In wip-release, after version bump:
if (skillMdVersion !== newVersion) {
  console.warn('  ! SKILL.md version is ' + skillMdVersion + ' but releasing ' + newVersion);
  console.warn('    Update SKILL.md before publishing.');
}
```

**Status:** DONE

## Phase 6: README Standard Enforcement

From notes/2026-03-10--cc-mini--readme-standard-and-universal-installer-vision.md.

Every repo README must follow the standard structure:
1. Tagline (what it solves, not what it is)
2. "Teach Your AI to [verb]" (copy-paste prompt block)
3. Features (human-readable, stability tags)
4. More Info (links to technical docs)
5. License

### Enforcement options (pick one):
- **Option A:** Add a README check to `wip-license-guard` (since it already audits repo structure)
- **Option B:** New tool `wip-readme-guard` that validates README structure
- **Option C:** Add to Dev Guide as a convention, enforce manually

Option A is simplest. wip-license-guard already walks tools/ and checks files. Add README structure validation alongside the license checks.

### What to check:
- Has `#` title
- Has `## License` section
- Has `## Features` or feature list
- Tagline is not "a tool that does X" pattern
- No architecture diagrams or config in README (those belong in TECHNICAL.md)

**Status:** DONE

## Phase 7: Validate Current READMEs Against Standard

Run the README standard check against all sub-tool READMEs. Memory Crystal's README is the reference implementation: https://github.com/wipcomputer/memory-crystal

Ensure our root README and all sub-tool READMEs match the standard pattern.

**Status:** DONE

## Deferred (do later)

- Evidence screenshots/artifacts (need to capture real examples first)
- Recommended adoption order (need external users first)
- CI badges (need CI first)
- COMMERCIAL-LICENSE.md (premature, but keep in mind)

## Done criteria

- README has golden path, matrix, license examples, MCP examples
- SKILL.md has matrix and MCP examples
- wip-release warns on stale SKILL.md
- README standard enforcement added to wip-license-guard (or equivalent)
- All READMEs validated against standard
- Deploy to public
- v1.6.0 release
