## Housekeeping protocol — keeps the docs tree from rotting

**You are responsible for keeping the docs tree current.** The whole point of slimming this file was to push reference material into topical files; that only works if those files stay fresh. After every session that changes something material, do the following before the user wraps up (or when writing the session recap):

1. **Identify which doc(s) the change touched.** Use the "Where to find things" map above. Changes to a feature → the matching `docs/features/*.md`. New script → `docs/scripts/README.md`. Env var name change or credential rotation (in hosting dashboard) → update `CLAUDE.local.md` to reference the new env var name. Schema change → `docs/architecture/database.md`.

2. **Update the relevant doc inline.** Don't leave the new fact only in a session recap. Recaps are journal entries; topical docs are the source of truth. A recap that says "added X" without updating the corresponding doc is a future drift bug.

3. **Stat tables go in `docs/STATE-SNAPSHOT.md`, not in topical docs.** Counts (entities, rows, users, etc.) belong in the dated snapshot file. Topical docs should describe *behavior*, not *current totals*. When refreshing the snapshot, **replace** it — do not append a new dated section.

4. **CLAUDE.md (this file) only gets updated when:**
   - A hard rule changes (add/remove from "Hard rules").
   - A new top-level docs area is added (add a pointer under "Where to find things").
   - The branch / environment topology changes.
   - The "Today's state" bullets need a refresh (every few sessions, or after a significant change).
   - **Never** add narrative changelogs, "Updated YYYY-MM-DD" markers, or feature deep-dives directly here. Those belong in topical docs + recaps.

5. **`CLAUDE.local.md` updates require care.** It's gitignored, so changes leave no trace in `git log`. When you add or rotate an env var name reference or service URL, **mention it in the session recap**: e.g. "Updated CLAUDE.local.md: rotated production DB password via Railway dashboard." That recap line is the only trace of the change in git history.

5a. **Contract docs (`TECHNICAL-DOCUMENTATION.md`, `FUNCTIONAL-SPECIFICATIONS.md`) must stay in sync with code.** When finishing work on a feature, update the matching section of the technical and functional contracts. The recap workflow prompts for this explicitly. Never declare a feature done while these contracts are stale — track the gap as a known debt in the recap if you must defer.

6. **Drift check — run before any session ends with non-trivial doc changes:**
   - `wc -l CLAUDE.md` → should still be ≤ ~300 lines. If it's growing, move content out.
   - `git status` → must NOT show `CLAUDE.local.md` as tracked or untracked (the gitignore should hide it).
   - For every new doc path mentioned in CLAUDE.md, confirm the file exists.

7. **When the user reports "Claude pointed at the wrong environment" or "asked me for a URL again":** that's a `CLAUDE.local.md` bug. Patch the local file so the next session has it. **Do not just answer the question — fix the source.**

8. **Quarterly hygiene pass** (or whenever this file feels heavy again):
   - Re-snapshot `docs/STATE-SNAPSHOT.md` from live data (replace, don't append).
   - Archive session recaps older than 90 days into `docs/recaps/archive/`.
   - Audit topical docs for `Updated YYYY-MM-DD` markers and remove them — git history is the source of truth for "when".
   - Audit topical docs for stat tables that crept in; move them to `STATE-SNAPSHOT.md`.
