#!/usr/bin/env bash
# 板厚图例填充子面域拆分：逐块按直接标注/图例填充/说明默认定档并保证面积对平。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_slab_thickness_partition "$@"
