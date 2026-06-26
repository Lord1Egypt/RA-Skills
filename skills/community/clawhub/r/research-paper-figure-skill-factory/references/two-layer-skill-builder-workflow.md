# Two-Layer Skill Builder Workflow

Version: 1.0.1

## Purpose

The factory first generates a specialized figure-making skill for a chosen paper-figure class, then uses that locked generated skill for arbitrary target-paper production.

## Layer A: Skill Builder

B1-B9 produce a reusable skill:

1. Target figure-class brief.
2. Corpus plan.
3. Lawful local corpus and retrieval manifest.
4. Figure/caption/panel evidence extraction.
5. Evidence-backed taxonomy.
6. Specialized skill blueprint.
7. Generated skill artifacts.
8. Test report and patches.
9. Locked generated skill with slug, version, package path, limitations, and test results.

## Layer B: Figure Production

P1-P9 use the generated skill:

1. P1 material intake.
2. P2 figure need diagnosis and subtype routing.
3. P3 reader-effect contract and 4-6 text candidates.
4. P4 visual candidate-board setup.
5. P5 `IMAGE_ONLY` candidate-board generation.
6. P6 candidate review and direction lock/revision.
7. P7 final image brief.
8. P8 `IMAGE_ONLY` formal generation/revision.
9. P9 review, caption, legend, and body text.

P4/P5/P6 are mandatory after multi-option text decisions unless the user explicitly chooses text-only selection.

## Production Unlock

P1-P9 are available only when:

```yaml
production_unlocked: true
production_unlocked_by: generated_skill_locked | full_production_fast_track
```

If the generated skill is not locked and the user has not chosen fast-track, continue builder B2-B9 rather than target-paper production.
