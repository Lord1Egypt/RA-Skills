# CAD Quantity Pipeline

仅在执行图层化几何、结构拓扑或混凝土算量任务时读取本包。

## 单入口

```bash
scripts/cad_quantity_pipeline.sh 结构图.dwg \
  --floor-label "二层梁平法施工图" \
  --support-floor-label "标高X~Y墙柱平法施工图" \
  --slab-floor-label "二层板结构施工图" \
  --out 首层算量
```

流水线生成扫描/详情、目标图框几何、梁对象、结构模型、混凝土分账、统一报告和
`pipeline_manifest.json/.md`。已有 `--scan/--detail` 时跳过重复扫描；`--plan-only` 先出执行清单。

只合并既有结果时：

```bash
scripts/cad_quantity_report.sh \
  --model-json 结构模型.json \
  --ledger-json 混凝土分账.json \
  --scan-json 图纸扫描.json \
  --beam-json 梁对象.json \
  --floor-label 首层 --format all -o 首层统一报告
```

## 证据层

- 梁中心线支撑、净跨/支座闭合、实例去重和编号归属冲突。
- 板厚分区、降板标高、洞口扣减和跨账防重。
- 墙身闭合、边缘构件、特殊构件、预制底板展开和楼梯梁台账。
- 混凝土等级分账、节点区归属、材料/预制子层拆分和口径确认。
- 项目配置可用 `--profile`；缺图名、图框、标高或构件范围时如实 skipped，不猜层。

## 报告与门槛

统一报告输出梁板柱墙基础规格与根数、配筋候选、钢筋估算、板厚洞口、净跨状态、
混凝土差异、异常构件回图坐标、闭合看板和阻断分组。`formal_ready=false` 时只能研发对账。

## 口径

- CAD 候选量、参考模型回填、风险量和已确认入账分列；确认口径后重跑，不得改标签混账。
- 混凝土为材料计划毛量±5~10%；钢筋为估算带，不替代翻样、下料、清单和结算。
- 节点/构造归属、材料分账、预制展开和洞口扣减必须恒等式对平或进入待确认。

## 历史细节

历史 P0-P50 参数、逐项回归和项目案例快照在 `history.md`，只在复现旧基线或排查
特定历史改动时读取；日常算量不默认加载。
