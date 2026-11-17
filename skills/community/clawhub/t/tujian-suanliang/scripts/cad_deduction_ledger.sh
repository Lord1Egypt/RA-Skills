#!/usr/bin/env bash
# 统一扣减台账：构件相交节点格与板洞口开洞图线走一套归属规则，防跨账重复扣减。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_deduction_ledger "$@"
