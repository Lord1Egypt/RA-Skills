---
name: ps2-bios-checksum
description: Inspect a local PS2 BIOS file — MD5, SHA-1, size, and basic dump-size validation. No BIOS downloads.
license: MIT
homepage: https://allps2bios.com/ps2-bios-retroarch/
---

# PS2 BIOS Checksum

## What this skill does

Runs local checksum and size checks on a PlayStation 2 BIOS dump the user already has.

## Steps

1. Ask for (or accept) a local file path.
2. Hash with MD5 and SHA-1 on-device.
3. Report size; flag empty files and sizes outside 2/4/8/16 MiB.
4. Optionally compare against a user-supplied expected hash.
5. State clearly that matches are reference-only.

## Do not

- Download or attach BIOS binaries
- Link to unauthorized BIOS mirrors
- Treat checksum equality as legal authenticity

## More reading

https://allps2bios.com/ps2-bios-retroarch/
