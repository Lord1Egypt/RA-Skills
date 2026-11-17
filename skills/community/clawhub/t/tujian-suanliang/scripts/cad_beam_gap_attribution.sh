#!/usr/bin/env bash
# 按体积口径归因梁编号量差，区分真实缺量与实例计数口径差。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_beam_gap_attribution "$@"
