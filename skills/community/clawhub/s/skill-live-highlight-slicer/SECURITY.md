# Security

## Scope

This skill analyzes local livestream recordings and writes generated clips and metadata to the configured output directory.

## Permissions

- Reads the local video passed with `--input`.
- Reads an optional local ASR transcript passed with `--asr-file`.
- Writes clips, `segments.json`, concat metadata, and an optional merged video to `--output-dir`.
- Does not contact remote services.

## Reporting

Before publishing a modified version, inspect `SKILL.md` and `scripts/highlight_slicer.py` line by line. Do not add install hooks, obfuscated commands, remote code download, or credential collection.

