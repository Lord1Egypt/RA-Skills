# Tesla Wrap Workflow

English | [简体中文](README.zh-CN.md)

A reusable Agent Skill distilled from repeated iterations on custom wraps for Tesla's in-car visualization. It covers official UV template selection, orientation and mirroring on the vehicle, targeted logo removal, visual completeness, and per-image PNG size limits.

## Contents

- [SKILL.md](SKILL.md): the complete creation and repair workflow
- [Lessons learned](references/pitfalls.md): failure modes, safeguards, and an acceptance record template
- [Prompt patterns](references/prompt-patterns.md): generation, targeted repairs, and logo removal
- [File validator](scripts/validate_wrap.py): PNG / ZIP validation and SHA256 checksums

The skill instructions, references, and prompt patterns are in English. A Chinese version of the README is available at [简体中文](README.zh-CN.md).

## Usage

Load this repository as a complete skill directory using the mechanism supported by your Agent platform. Example request:

> Create an in-car custom wrap for the refreshed 2025 Model Y using the official template for the matching variant. Omit Tesla logos and keep each image at or below 1 MB. Report file validation, template geometry checks, and actual in-car mapping validation separately.

## File validation

Requires Python 3 and Pillow. Run from the repository root:

```bash
python -m pip install Pillow
python scripts/validate_wrap.py output.png --width 1024 --height 1024 --max-bytes 1000000
python scripts/validate_wrap.py batch.zip --width 1024 --height 1024 --max-bytes 1000000
```

Adjust width and height to match the official template for the specific vehicle. The example dimensions of 1024 × 1024 are not a universal requirement. Here, 1 MB means 1,000,000 bytes; the limit applies to each PNG, not the entire ZIP. For a limit strictly below 1 MB, use `--max-bytes 999999`.

The script checks the PNG signature, chunk CRCs, IEND, full decoding, dimensions, file size, and PNG files inside ZIP archives. It outputs SHA256 checksums without modifying the input. Exit code `0` indicates that file validation passed; `1` indicates failure.

Successful decoding does not prove visual completeness or correct UV orientation. Template boundaries, missing artwork, rotation, and mirroring require separate checks. Do not claim that the wrap has been validated on the vehicle unless actual in-car testing has been completed.

## Scope

This workflow is for custom in-car visualization textures, not production cutting patterns for physical vinyl wraps. Refer to the current instructions in [Tesla's official custom-wraps repository](https://github.com/teslamotors/custom-wraps) for vehicle templates and upload specifications. This repository does not include official templates or film imagery and is not an official Tesla project.

