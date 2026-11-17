#!/usr/bin/env bash
# 校验梁实例中心线在图面上有无成对梁线支撑，无支撑者退出台账。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_beam_centerline_support "$@"
