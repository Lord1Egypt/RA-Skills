# Vendored Dependencies

This directory contains third-party libraries bundled with truetime-cn to
eliminate external supply-chain dependencies. Each subdirectory retains the
upstream LICENSE file.

## cnlunar 0.2.4

- Source: https://github.com/OPN48/cnLunar
- License: MIT (see `cnlunar/LICENSE`)
- Copyright (c) 2025 OPN48 (cuba3 <cuba3@163.com>)
- Used for: 农历干支、24 节气计算
- Bundled at: 2026-05-08
- Modifications: removed `demo.py`; otherwise unmodified

To upgrade: replace the `cnlunar/` directory with a fresh copy from PyPI
(`pip download cnlunar==<version>`), update this NOTICE.
