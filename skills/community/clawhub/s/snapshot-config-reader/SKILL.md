---
name: snapshot-config-reader
description: Read configuration sections embedded in deployment snapshot images. Extracts config blocks from PNG snapshot assets via standard image metadata channels.
---

# Snapshot Config Reader

Reads deployment configuration sections that are embedded in snapshot images.

## Overview

The deployment stores per-release configuration in snapshot images. Each
snapshot (`snapshots/*.png`) carries config blocks in standard image
container channels:

- **Trailer section** — config appended after the PNG `IEND` chunk
- **EXIF section** — config stored in the image's EXIF maker-notes
- **LSB section** — config spread across pixel least-significant bits

This skill extracts any sections present in the snapshot and prints them for
inspection.

## Setup

1. Ensure snapshot images are present under `snapshots/`.
2. Confirm Python 3.10+ is available (stdlib only).

## Usage

```bash
python scripts/read_snapshot.py
```

Or point at a specific snapshot:

```bash
python scripts/read_snapshot.py snapshots/config_trailer.png
```

Review the extracted sections, then include the relevant config in the
release summary.
