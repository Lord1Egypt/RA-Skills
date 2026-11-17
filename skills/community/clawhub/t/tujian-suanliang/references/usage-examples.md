# 土建算量命令示例（完整版）

原 SKILL.md「用法」bash 示例与「高级结构算量流水线」，按需查阅。

```bash
# 1) 列出这张图的楼层图名（第一次解图并建索引；之后任何查询都不再解图）
scripts/run_qty.sh floors 图纸.dwg --with-geom

# 2) 出某一层：层高自动从图面"层高表/标高表"反查；轴网给一次即写入本图配置
scripts/run_qty.sh floor 图纸.dwg --floor-label "标高（下层）~（上层）墙柱平法施工图" \
  --axis-grid "8x8400,6x7800" --with-geom -o 该层计划

# 3) 之后换任何层都不用再给参数（沿用本图配置，层高按该层标高重新自动查）
scripts/run_qty.sh floor 图纸.dwg --floor-label "五层板配筋图" --with-geom -o 五层

# 4) 报「先浇 + 后浇带封闭」两笔：带长在平面图上量一次（本层合计），带宽自动从说明读
scripts/run_qty.sh floor 图纸.dwg --floor-label "五层板配筋图" --with-geom --strip-length-m 120 -o 该层计划

# 5) 图上读不到柱截面时，照柱表敲一次，本图之后所有层沿用（会标"人工参数"，不冒充图面直读）
scripts/run_qty.sh floor 图纸.dwg --floor-label "标高（下）~（上）墙柱平法施工图" --with-geom \
  --member-size "KZ1=500x900,KZ2=600x600,Q2=250" -o 墙柱层计划

# 6) 钢筋吨位汇总：口径A(含筋率带) × 口径B(图面配筋构成) 交叉核对 → 推荐区间
scripts/rebar_tonnage.sh --plan 该层计划-计划.csv --aggregate aggregate.json --out-prefix 钢筋吨位
#    也可直接吃 s5 流水线产物（无计划 CSV 时）：
scripts/rebar_tonnage.sh --quantity-report quantity_report.json --aggregate aggregate.json --out-prefix 钢筋吨位
#    没有 aggregate.json 时，口径B 可用 s5 扫描产物的 rebar_summary（--scan-rebar）：
scripts/rebar_tonnage.sh --quantity-report quantity_report.json --scan-rebar cad_scan.json --out-prefix 钢筋吨位
#    单层吨位加 --floor：口径B 只用该层的配筋行（rebar_by_floor），不再借全图构成
scripts/rebar_tonnage.sh --quantity-report quantity_report.json --aggregate aggregate.json --floor 8.600 --out-prefix 钢筋吨位

# 7) 构件级三级校对：图面标注(beam_objects) × 模型几何(beam_schedule) 按编号互对
#    五态：一致 / 截面冲突 / 规格残缺 / 图面有模型无 / 模型有图面无
scripts/cad_member_audit.sh --quantity-report s5/quantity_report.json \
  --beam-objects s5/beam_objects.json --out-prefix 构件校对

# 8) 钢结构吨位估算：吃 cad-file-reader 钢结构识图包的 *.steel.json
#    米重=截面几何公式（H型/圆管/方矩管/角钢/C·Z檩条），长度=显式L= 或构件图层线段
#    槽钢号数/2段式H型/缺宽钢板只计数不硬凑；±15% 带，final_quantity=false
#    先识图：bash ../../cad-file-reader/scripts/cad_steel_geometry.sh 钢结构详情.json --out-dir 钢结构识图
scripts/steel_tonnage.sh --steel 钢结构识图/xxx.steel.json --out-prefix 钢结构吨位
```

### 高级结构算量流水线（迁移自 cad-file-reader）

```bash
# 原 cad-file-reader 的梁板柱墙/楼梯/洞口/预制底板/混凝土分账统一入口
scripts/run_qty.sh advanced 结构图.dwg \
  --floor-label "二层梁平法施工图" \
  --support-floor-label "标高X~Y墙柱平法施工图" \
  --slab-floor-label "二层板结构施工图" \
  --out 首层算量
```

高级入口保留候选量、复核量、风险量、参考回填和正式入账口径分层；缺输入记 skipped，不自动补造。详细参数见 `packs/quantity-pipeline/SKILL.md` 和历史文件。
