# Failure Playbook

Classify the failure before deciding on next action. Do not retry blindly.

---

## 1. `whoami` Returns HTML / Security Checkpoint

**Symptom:** `clawhub whoami` returns HTML page instead of JSON.

**Likely cause:** ClawHub's Vercel-hosted infrastructure fires bot protection on this IP/session. Not deterministic — can happen after rate limit exhaustion or new IP state.

**Safe next step:**
1. Wait briefly (60–90 seconds).
2. Retry `clawhub whoami`.
3. If it returns clean JSON, the full CLI flow is viable.
4. If it still returns HTML after 3 attempts → report `BLOCKED`.

**Stop rule:** After 3 failures, stop retrying. Do not keep burning rate limit slots.

**Re-authentication:** Running `clawhub login --token <token>` again is worth trying if the token may have rotated. Do not retry the same failed command if it consistently returns HTML.

---

## 2. CLI Command Returns HTML for All Subcommands

**Symptom:** `clawhub inspect`, `clawhub publish`, `clawhub whoami` all return HTML.

**Likely cause:** Rate limit counter is exhausted (0 remaining), or global bot protection is active.

**Recovery signal:** `clawhub whoami` returns clean JSON — this signals the rate limit has reset and all commands will work.

**Safe next step:**
1. Poll `clawhub whoami` every 90 seconds.
2. When it returns clean JSON, immediately run the publish command.
3. Do not assume one subcommand works while another is blocked — rate limit is global.

**Stop rule:** After 10 minutes of continuous HTML responses, report `BLOCKED`. Do not run publish into a confirmed blocked session.

---

## 3. Publish Reports Namespace / Slug Conflict

**Symptom:** `clawhub publish` returns error about namespace conflict or slug already exists.

**Likely cause:** Slug is already taken or the user is trying to create a protected namespace (`openclaw-*`).

**Safe next step:**
1. Confirm the correct slug to use.
2. Do not change slug and republish on your own.
3. Report the conflict with the exact error message.

**Stop rule:** Never change the slug without explicit user/orchestrator instruction.

---

## 4. Version Rejected

**Symptom:** `clawhub publish` rejects the version with "same version already exists" or similar.

**Likely cause:** ClawHub requires a higher semver on each publish. Cannot re-publish same version.

**Safe next step:**
1. Run `clawhub inspect <slug>` to get the current live version.
2. Bump to the next semver (e.g., if live is `1.2.3`, target `1.2.4`).
3. Re-run publish with the bumped version.

**Stop rule:** Do not keep retrying the same rejected version.

---

## 5. Source Path Mismatch

**Symptom:** Folder doesn't exist, wrong content inside, or slug inside the SKILL.md doesn't match expected slug.

**Likely cause:** Guessed the wrong path, or the skill is located at a per-skill override path not checked.

**Safe next step:**
1. Check `references/per-skill-overrides.md` for the correct canonical path.
2. Verify SKILL.md exists in the confirmed path.
3. If still ambiguous → report `NEEDS_INFO`.

**Stop rule:** Do not publish from a guessed folder. Never assume — verify the path.

---

## 6. Registry OK but Public Page Stale

**Symptom:** `clawhub inspect <slug>` shows correct version and content, but public page shows old content.

**Likely cause:** CDN/cache lag after publish. ClawHub CDN caches can take a few minutes to propagate.

**Safe next step:**
1. Wait 2–3 minutes.
2. Hard refresh the public page.
3. Re-check page content.
4. If still stale after 5 minutes → re-publish with bumped version to force propagation.

**Stop rule:** Do not claim public `PASS` until the public page content actually matches expected content.

---

## 7. Browser Snapshot ≠ Actual Page Text

**Symptom:** `browser_snapshot` shows correct structure, but `innerText` or direct text extraction shows wrong content.

**Likely cause:** Accessibility tree renders differently from actual visual page. Numbered lists, bold markers, and section formatting can differ between tree representation and rendered text.

**Safe next step:**
1. Use `browser_console` with JavaScript to extract `innerText` of the relevant section.
2. Compare the actual rendered text against expected content.
3. If they differ → report `MISMATCH`.

**Stop rule:** Trust `innerText` / raw rendered text over browser snapshot. Report `MISMATCH` when they differ.

---

## 8. Missing SKILL.md

**Symptom:** Source path exists but no SKILL.md inside.

**Likely cause:** Wrong folder, or skill was not properly created.

**Safe next step:**
1. Confirm the correct path from per-skill overrides.
2. Report `NEEDS_INFO` with the exact path checked.

**Stop rule:** Do not attempt to publish a non-existent skill.

---

## 9. Vague / Empty Changelog

**Symptom:** Changelog is "updated", "fixes", "misc", "minor changes", or blank.

**Likely cause:** Pre-flight did not catch a vague changelog before running publish.

**Safe next step:**
1. Do not publish with a vague changelog.
2. Report `NEEDS_INFO` — changelog must be specific.

**Stop rule:** Vague changelog is a pre-flight failure. Publish must not proceed.

---

## 10. Guardian Review Missing

**Symptom:** `GUARDIAN REVIEW: required` is set but review status is not confirmed complete.

**Likely cause:** Request packet did not include review completion.

**Safe next step:**
1. Do not publish.
2. Report `NEEDS_INFO` — guardian review required but not yet completed.

**Stop rule:** Do not bypass required guardian review.

---

## 11. Rename / Merge / Delete / Hide / Undelete Requested During Publish

**Symptom:** Executor calls `clawhub skill rename`, `clawhub skill merge`, `clawhub delete`, or similar during a publish task.

**Likely cause:** Executor confused management operations with publish operations.

**Safe next step:**
1. **STOP.** These are management operations, not publish operations.
2. Report `BLOCKED` — management operations are out of scope for `clawhub-auto-publish`.
3. Recommend using a separate `clawhub-skill-management` workflow.

**Stop rule:** Never run management commands from the publish workflow.

---

## 12. Publish Succeeded but Inspect Shows Old Version

**Symptom:** CLI returned success (with commit ID), but `clawhub inspect` shows the previous version.

**Likely cause:** Propagation lag — `clawhub inspect` can temporarily show stale data even when publish succeeded.

**Safe next step:**
1. Note the commit ID from publish output as authoritative proof.
2. Wait 60 seconds.
3. Re-run `clawhub inspect`.
4. If still stale after 2 minutes → this is not a failure of the publish, only of the inspect query.
5. Report publish as `PUBLISHED` with the commit ID.

**Stop rule:** Do not re-publish if the commit ID was returned and inspect is simply stale.

---

## 13. Slug / Owner Mismatch in URL

**Symptom:** Published URL shows wrong owner or slug.

**Likely cause:** `--owner` flag does not exist in CLI. Owner is derived from the logged-in account.

**Safe next step:**
1. Run `clawhub whoami` to confirm the logged-in account.
2. If wrong account → use correct account's token to log in.
3. Confirm the correct slug for the skill.

**Stop rule:** Never proceed with the wrong owner in the URL. Verify identity first.