# Batch Shoot Plan

Turn approved short-video scripts into a practical shoot order grouped by location and camera setup, plus a searchable media naming table. It reduces resets while preserving the user's script.

**Input:** script IDs, scenes, cast, and action/dialogue summaries. Include known locations, props, and cameras; location and cast availability are optional.  
**Output:** shoot order, on-set checks, and media naming templates. Finished-video duration is not filming effort. When setup, rehearsal, filming, or retake time is unknown, deliver an ordered list without clock times. Missing availability does not cause required-input failure.

## Install

```bash
npx skills add xxjrq/selfmedia-batch-shoot-plan-cn
```

Use it for a single chapter, scene, or short piece with up to 100 records. It does not write fiction, scripts, or storyboards.

See the copyable [complete example](fixtures/success-output.md) and [missing-information example](fixtures/failure-output.md). Run `python3 scripts/self_test.py` from the repository root to validate the release files.

The business category was informed by the public [social-media-skills/skills](https://github.com/social-media-skills/skills) repository; this repository's documentation, workflow, and examples are original. Licensed under [MIT-0](LICENSE).

Actual forward references: [complete input](fixtures/forward-success.md), [partial-input order](fixtures/forward-failure.md), and [new cases](fixtures/forward-additional.md). Old example exposure during repair is disclosed in the audit; the additional cases had no expected answer.
