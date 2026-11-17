#!/usr/bin/env bash
# 目标楼层图块展开与几何复核入口。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_geometry "$@"
