#!/usr/bin/env bash
# 整册 DXF 梁编号标注的图框归属：判断偏少编号该回本层图框还是别的楼层。
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.sh" cad_beam_frame_label_index "$@"
