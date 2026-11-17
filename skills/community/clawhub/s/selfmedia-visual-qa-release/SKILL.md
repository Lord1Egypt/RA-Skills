---
name: selfmedia-visual-qa-release
description: Validate a rendered media delivery package against an explicit file and media contract, including video streams, image sizes, and subtitle timing; report failures without promoting or overwriting files.
license: MIT-0
metadata:
  version: "1.0.0"
---

# Media Release Package QA

Use this skill to inspect a finished media package before handoff. First identify the user's actual contract: required filenames, video codec/frame rate/dimensions/audio requirements, image dimensions, subtitle rules, and destination. Do not treat the included Douyin five-file profile as a universal platform requirement.

Run the validator with an explicit package directory and contract:

```bash
python3 scripts/validate_release_package.py /path/to/package --contract contracts/douyin-five-file.json
```

The included profile is a reusable example based on a project-specific five-file handoff: copy, video, 3:4 cover, 4:3 cover, and SRT captions. Its dimensions are declared in the contract. Adjust the JSON contract when the actual user or platform requirements differ; do not silently add requirements based on convention.

The validator requires `ffprobe` on PATH. It checks exact file membership, probe-readable media, declared codec/frame rate and image dimensions, and valid ordered SRT cue times within video duration. It reports findings only: it never edits, deletes, copies, or promotes the package. On any failure, preserve the user's package and report the precise field. A pass is a check against the selected local contract, not proof of platform acceptance or visual quality.

Run local regression checks with `python3 scripts/self_test.py`. Review images at intended display size and inspect the video visually; automated metadata checks cannot judge legibility, crop, visual artifacts, or editorial quality.
