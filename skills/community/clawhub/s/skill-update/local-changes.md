# Local Changes — Updating a Hand-Edited Skill

Users edit installed skills: a tweaked rule, a deleted section that annoyed them, an added preference. A straight update overwrites all of it with no error anywhere. Detect first, decide second, merge third.

## Detecting Local Edits

Diff the installed copy against its published original — the version the user installed, not the latest:

```bash
# Fetch the ORIGINAL of the installed version for comparison
npx clawic install <slug> --dir /tmp/original-<slug>
diff -r .claude/skills/<slug> /tmp/original-<slug>
```

If the registry only serves latest, the previous update's backup in `~/Clawic/data/skill-update/backups/` is the reference copy. No backup and no original available → assume edits exist and show the user the three-way plan below before applying anything.

Empty diff → clean install, proceed with the normal Update Flow. Any hunk → stop and classify.

## Classifying Each Local Edit

| Edit found | Meaning | Default handling |
|---|---|---|
| Changed wording of an instruction | User re-tuned behavior deliberately | Preserve — re-apply onto the new version |
| Deleted section or file | User suppressed behavior they didn't want | Preserve the deletion unless the new version rewrote that section for the same reason |
| Added section, rule, or file | User extended the skill | Preserve — carry the addition over |
| Changed frontmatter description | User re-tuned when the skill triggers | Preserve; upstream description changes need explicit user choice |
| Edits inside a section the update also rewrites | True conflict | Show both versions side by side; the user picks — never auto-merge a conflict |
| Whitespace/formatting only | Editor artifact | Ignore; take upstream |

## The Three-Way Merge

Three states: **original** (published version the user installed) · **local** (installed copy with edits) · **upstream** (new published version).

1. Compute `original → local` (the user's edits) and `original → upstream` (the publisher's changes).
2. Edits and changes touching different sections: apply both — update first, re-apply local edits on top.
3. Both touch the same section: conflict. Present both versions with one line on what each does; the user decides per conflict, not in bulk.
4. Record what was carried over in the update report — the user should see their edits survived, listed by name.

## After the Merge

- Verify with a task that exercises the user's edited behavior specifically — the generic verify run tests upstream behavior, not the customization.
- Persist the edit list to `~/Clawic/data/skill-update/local-edits-<slug>.md` (one line per edit: file, section, one-line intent). Next update starts from this list instead of re-deriving intent from a diff.
- Suggest once: recurring edits that survive multiple updates are config, not forks — if the skill has a Configuration table, moving the preference into `~/Clawic/data/<slug>/config.yaml` ends the merge burden permanently. User declines → keep merging, don't re-raise.

## Traps Specific to Local Edits

- Diffing local against **latest** instead of against the installed original conflates the user's edits with the publisher's changes — every upstream change looks like a user edit.
- "Take upstream for everything, it's newer" silently deletes the user's work; newer is the publisher's intent, not the user's.
- Re-applying a local edit whose target section no longer exists: park it in the edit list as orphaned and tell the user, don't graft it somewhere similar.
