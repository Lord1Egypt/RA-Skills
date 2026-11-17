#!/usr/bin/env bash
# 审计梁图层图线是否已被算量实例覆盖，区分漏量候选、重复视图与板面域外。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_beam_coverage_audit "$@"
