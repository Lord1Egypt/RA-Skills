# README License Section Audit

**Date:** 2026-03-14
**Tool:** `wip-license-guard readme-license --dry-run`
**Scope:** All repos under `ldm-os/`
**Result:** 52 issues across 49 repos. 3 correct, 2 missing README entirely.

---

## Correct (3 repos, no changes needed)

| Repo | Path |
|------|------|
| wip-ldm-os-private | `components/wip-ldm-os-private/README.md` |
| wip-ai-devops-toolbox-private | `devops/wip-ai-devops-toolbox-private/README.md` |
| wip-1password-private | `utilities/wip-1password-private/README.md` |

## Non-standard license section (22 repos, would replace with standard dual block)

| Repo | Path | Current |
|------|------|---------|
| grok-search | `apis/_to-privatize/grok-search/README.md` | MIT |
| wip-music-api | `apis/_to-privatize/wip-music-api/README.md` | MIT |
| grok-search (dup) | `apis/grok-search/README.md` | MIT |
| wip-xai-grok-private | `apis/wip-xai-grok-private/README.md` | MIT |
| wip-xai-x-private | `apis/wip-xai-x-private/README.md` | MIT |
| CLVR-private | `apps/CLVR-private/README.md` | Custom (source MIT, binaries copyrighted) |
| wip-markdown-viewer-private | `apps/_to-privatize/wip-markdown-viewer-private/README.md` | MIT |
| wip-todo | `apps/_to-privatize/wip-todo/README.md` | MIT |
| x-bookmarks-reviewer | `apps/_to-privatize/x-bookmarks-reviewer/README.md` | MIT (Part of Lesa's workspace) |
| cc-session-export | `components/_to-privatize/cc-session-export/README.md` | MIT |
| lesa-openclaw-context-embeddings | `components/_to-privatize/lesa-openclaw-context-embeddings/README.md` | MIT |
| wip-enterprise-agents | `components/_to-privatize/wip-enterprise-agents/README.md` | Proprietary |
| dream-weaver-protocol-private | `components/dream-weaver-protocol-private/README.md` | MIT |
| memory-crystal-private | `components/memory-crystal-private/README.md` | Partial dual block |
| memory-crystal-py-private | `components/memory-crystal-py-private/README.md` | MIT. Work In Progress, Inc. |
| wip-agent-pay-private | `components/wip-agent-pay-private/README.md` | Partial dual block |
| wip-bridge-private | `components/wip-bridge-private/README.md` | MIT |
| wip-cloud-private | `components/wip-cloud-private/README.md` | Partial dual block |
| wip-ldm-mirror-test | `identity/wip-ldm-mirror-test/README.md` | MIT |
| wip-mirror-test-private | `identity/wip-mirror-test-private/README.md` | MIT |
| security-audit-skill | `utilities/_to-privatize/security-audit-skill/README.md` | MIT License (custom) |
| wip-healthcheck | `utilities/wip-healthcheck/README.md` | MIT |
| wip-understand-video | `utilities/wip-understand-video/README.md` | MIT |
| wip-secrets-ios-private | `utilities/wip-secrets-ios-private/README.md` | MIT |

## Missing license section entirely (18 repos, would append standard block)

| Repo | Path |
|------|------|
| wip-exec-brief | `apps/_to-privatize/wip-exec-brief/README.md` |
| wip-field-notes-papers | `apps/_to-privatize/wip-field-notes-papers/README.md` |
| wip-ldm-scrapbook | `apps/_to-privatize/wip-ldm-scrapbook/README.md` |
| wip-scrapbook | `apps/_to-privatize/wip-scrapbook/README.md` |
| agent-identity-builder | `components/_to-privatize/agent-identity-builder/README.md` |
| fading-heartbeat | `components/_to-privatize/fading-heartbeat/README.md` |
| voice-training-plugin | `components/_to-privatize/voice-training-plugin/README.md` |
| wip-total-recall | `components/_to-privatize/wip-total-recall/README.md` |
| wip-heartbeat | `devops/_to-privatize/wip-heartbeat/README.md` |
| open-claw-upgrade-private | `devops/open-claw-upgrade-private/README.md` |
| weekly-tuning | `identity/weekly-tuning/README.md` |
| wip-weekly-tuning-private | `identity/wip-weekly-tuning-private/README.md` |
| imessage-reply-context | `utilities/imessage-reply-context/README.md` |
| imessage-rich | `utilities/imessage-rich/README.md` |
| lesa-voice-call | `utilities/lesa-voice-call/README.md` |
| md-to-x | `utilities/md-to-x/README.md` |
| openclaw-tavily | `utilities/openclaw-tavily/README.md` |
| wip-obsidian | `utilities/wip-obsidian/README.md` |
| compaction-indicator-private | `utilities/compaction-indicator-private/README.md` |
| wip-healthcheck-private | `utilities/wip-healthcheck-private/README.md` |

## Sub-tool READMEs with license sections (6, would remove)

| Sub-tool | Path |
|----------|------|
| wip-file-guard | `devops/wip-ai-devops-toolbox-private/tools/wip-file-guard/README.md` |
| wip-license-hook | `devops/wip-ai-devops-toolbox-private/tools/wip-license-hook/README.md` |
| wip-release | `devops/wip-ai-devops-toolbox-private/tools/wip-release/README.md` |
| wip-repo-permissions-hook | `devops/wip-ai-devops-toolbox-private/tools/wip-repo-permissions-hook/README.md` |
| wip-repos | `devops/wip-ai-devops-toolbox-private/tools/wip-repos/README.md` |
| wip-universal-installer | `devops/wip-ai-devops-toolbox-private/tools/wip-universal-installer/README.md` |

## No README found (2 repos, can't fix)

| Repo | Path |
|------|------|
| wip-private-mode-private | `utilities/wip-private-mode-private/` |
| wip-root-key-private | `utilities/wip-root-key-private/` |

## Flags for Parker

- **wip-enterprise-agents**: Currently says "Proprietary. This is the product." Should this stay proprietary or get the dual block?
- **CLVR-private**: Has custom license (source MIT, binaries copyrighted). Should this get the standard block or keep its custom section?

---

All paths are relative to: `~/Documents/wipcomputer--mac-mini-01/staff/Parker/Claude Code - Mini/repos/ldm-os/`
