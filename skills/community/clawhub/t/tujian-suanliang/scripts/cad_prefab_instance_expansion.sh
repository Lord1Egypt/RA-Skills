#!/usr/bin/env bash
# 预制底板图面实例展开：逐编号数量倍率自证，不再借用外部模型块数当倍率。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_prefab_instance_expansion "$@"
