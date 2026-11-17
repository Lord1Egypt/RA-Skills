#!/usr/bin/env bash
# 审计板图层 S-板-开洞 的洞口证据，逐条分类并核对历史洞口候选。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_slab_opening_audit "$@"
