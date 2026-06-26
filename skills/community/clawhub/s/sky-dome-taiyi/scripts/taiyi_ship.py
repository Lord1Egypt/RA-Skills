#!/usr/bin/env python3
"""Generate a release/publish checklist from a staged directory."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
parser=argparse.ArgumentParser(); parser.add_argument('path'); parser.add_argument('--version',default='0.1.0'); parser.add_argument('--name',default=''); args=parser.parse_args()
root=Path(args.path).resolve(); files=sorted(p for p in root.rglob('*') if p.is_file())
h=hashlib.sha256()
for p in files:
    h.update(str(p.relative_to(root)).encode()); h.update(p.read_bytes())
print(f'''# Taiyi Ship Checklist

Package: {args.name or root.name}
Version: {args.version}
Path: {root}
Files: {len(files)}
SHA256-manifest: {h.hexdigest()[:16]}

## Preflight
- [ ] Clean staging directory only
- [ ] Version bumped
- [ ] Changelog written
- [ ] No state/log/backups/secrets
- [ ] Metadata and description checked
- [ ] User confirmed external publish

## Postflight
- [ ] Inspect published metadata
- [ ] Verify latest version
- [ ] Check usage instructions / registry command if applicable
- [ ] Report evidence

## Files
''')
for p in files: print(f'- {p.relative_to(root)}')
