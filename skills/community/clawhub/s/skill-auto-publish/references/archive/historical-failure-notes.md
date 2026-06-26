# Historical Failure Notes

Diagnostic reference only. Do not load this file during normal publishing execution — load it only when diagnosing repeated failure patterns.

---

## FF-001: Local File Edit Reported as Done Without Publish

**Date:** 2026-05-23 (waste-audit)

**What happened:** Agent updated local SKILL.md at `/root/.hermes/skills/tokensave/waste-audit/SKILL.md` and reported "Done." BG responded: "YOU DIDN'T DO ANY CHANGES. HOW DARE YOU SAY DONE. I NEED YOU TO UPDATE THE WEB PAGE, NOT JUST THE INTERNAL SKILL.MD."

**Root cause:** Conflated "local file updated" with "task done." Local file changes do not propagate to `clawhub.ai` automatically — `clawhub publish` must be run explicitly.

**Resolution:** Run `clawhub publish /path/to/skill/ --slug <slug> --name "<name>" --version <semver> --changelog "<change>"` after any local file update when the user says "update the web page".

**Rule:** When the user says "fix skill X" or "update the web page", the task is never complete until `clawhub publish` has been run.

---

## FF-002: Browser Snapshot False Positive

**Date:** 2026-05-23 (buffett-do, waste-audit)

**What happened:** Browser accessibility tree showed correct section structure, but actual page render had wrong content — specifically numbered list formatting (bare `1.` stripped inside H2 sections, while `**1.**` bold format survived).

**Root cause:** Accessibility tree and visual render diverge for certain markdown structures. The tree shows element containment correctly but not the actual visual formatting.

**Resolution:** Use `browser_console` with JavaScript to extract `innerText` of the relevant section. Compare actual rendered text against expected content, not tree structure.

**Required technique:**
```javascript
browser_console({expression: `(function(){
  const h=Array.from(document.querySelectorAll('h2')).find(x=>x.textContent==='Section Name');
  if(!h)return'not found';
  const txt=h.parentElement.innerText;
  const idx=txt.indexOf('Section Name');
  return txt.substring(idx,idx+600);
})()`})
```

---

## FF-003: Public Page Checkpoint / Rate Limit Confusion

**Date:** 2026-05-22, 2026-05-23 (multiple sessions)

**What happened:** CLI commands returned HTML instead of JSON. Agents tried different subcommands (`inspect` vs `publish`) trying to find one that worked, not understanding that the rate limit is global across all CLI commands.

**Root cause:** Rate limit counter is shared across all ClawHub CLI commands for the session. When `clawhub whoami` returns HTML, `inspect` AND `publish` are ALL blocked simultaneously.

**Recovery signal:** When `clawhub whoami` returns clean JSON, ALL commands work in the same call. The recovery is also global.

**Pattern:** Rate limit resets in ~60 seconds after reaching 0. Poll `clawhub whoami` every 90 seconds. When it returns clean JSON, immediately run the publish commands.

---

## FF-004: Source Path Mismatch for waste-audit

**Date:** 2026-05-23 (waste-audit)

**What happened:** Agent looked in `/root/.hermes/skills/workflow-kits/` instead of `/root/.openclaw/skills/waste-audit/` for the canonical source.

**Root cause:** Did not check per-skill overrides. waste-audit lives in the OpenClaw workspace, not Hermes workflow-kits.

**Resolution:** Check `references/per-skill-overrides.md` before assuming a source path. waste-audit must be `/root/.openclaw/skills/waste-audit/SKILL.md`.

---

## FF-005: rename Command Retry Loop

**Date:** 2026-05-22 (buffett-do migration)

**What happened:** Agent retried `clawhub skill rename buffett-do wbwd-research-priority --yes` multiple times after getting `newSlug required` error. Each retry burned rate limit slots.

**Root cause:** The error is a parse failure (CLI bug), not a rate limit signal. Repeating the same command cannot fix a parse failure.

**Resolution:** Do not retry a command that returns `newSlug required` — this is a confirmed CLI bug. Use separate-slab migration instead: publish new slug, update old slug content to redirect.

---

## FF-006: Stale Public Page After Registry Update

**Date:** 2026-05-22 (buffett-do)

**What happened:** `clawhub inspect` returned "Skill not found" immediately after publish succeeded with a commit ID. Browser showed the published content correctly.

**Root cause:** `clawhub inspect` can temporarily show stale data due to propagation lag, even when publish succeeded. The commit ID in CLI output is the authoritative proof of publish success.

**Resolution:** When publish returns a commit ID and `clawhub inspect` shows stale data, wait 60 seconds and re-check inspect. Do not re-publish if commit ID was returned — the publish succeeded, only the inspect query is stale.

---

## FF-007: HTML Comments Visible on Public Page (buffett-do v1.1.3)

**Date:** 2026-05-22 (buffett-do)

**What happened:** `<!-- internal activation coverage: ... -->` used to hide internal trigger phrases. ClawHub page renderer does NOT strip HTML comments — they appeared as visible raw text to all visitors.

**Resolution:** Never use HTML comments in SKILL.md to hide content from public view. For private content, use separate support files (`references/<slug>-notes.md`) that won't appear on the public page but are still readable by the skill runtime.

---

## FF-008: Wrong Section Structure Survives Publish

**Date:** 2026-05-22 (buffett-do)

**What happened:** Source SKILL.md had duplicate `## Install` headers (from leftover v1.1.3 content alongside new v1.1.4 content). Both appeared on the public page.

**Root cause:** ClawHub does not de-duplicate section headers. If the source has duplicate headers, both appear on the public page.

**Resolution:** Fix the source file before publishing. Every header in the source must be exactly as intended — ClawHub renders what it is given without normalization.