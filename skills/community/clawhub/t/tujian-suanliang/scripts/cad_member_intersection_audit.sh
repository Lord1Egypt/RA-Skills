#!/usr/bin/env bash
# 审计梁、连梁、柱、墙和边缘构件的矩形重叠，输出构件相交重复计量候选。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_member_intersection_audit "$@"
