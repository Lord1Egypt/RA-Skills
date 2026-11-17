# CAD Quantity Pipeline

该技能包保存结构几何展开、梁墙柱板拓扑、支座净跨、楼梯梁、结构模型和混凝土
分账的完整参数、状态分栏与边界。仅在执行图层化几何或混凝土算量任务时读取。

## 范围

- 图层化几何、梁对象、全图拓扑、引线、实例倍率和支座净跨。
- 墙柱、边缘构件、柱、板拓扑、板厚、洞口和预制底板。
- 楼梯梁独立台账、结构模型和混凝土分账。
- 所有候选量、复核量和正式准入门槛。

## 定位

该包不替代主 `SKILL.md` 的文件读取入口；执行算量前先完成图纸读取、图层化扫描和
目标图框展开。

### 单入口流水线与统一报告（2026-09-10 P0 加）

同一份结构图包含梁、墙柱、板图框时，使用单入口顺序编排，避免手工拼接各脚本参数：

```bash
scripts/cad_quantity_pipeline.sh \
  结构图.dwg \
  --floor-label "二层梁平法施工图" \
  --support-floor-label "标高〈标高〉~〈标高〉墙柱平法施工图" \
  --slab-floor-label "二层板平法施工图" \
  --component-sheet 34 --slab-sheet 36 \
  --story-height-mm 3870 --elevation-mm 2810 --concrete-grade C30 \
  --reference-floor 首层 --reference "梁及连梁=〈实测〉" \
  --out 首层算量
```

流水线依次生成扫描/详情、三个图框几何、梁对象与拓扑、结构模型、混凝土分账、
统一报告和 `pipeline_manifest.json/.md`。清单记录每步命令、耗时、重试和 SHA-256。
已有 `--scan/--detail` 时跳过扫描；`--plan-only` 只写执行清单。只合并已有结果时运行：

```bash
scripts/cad_quantity_report.sh \
  --model-json 结构模型.json \
  --ledger-json 混凝土分账.json \
  --scan-json 图纸扫描.json \
  --beam-json 梁对象.json \
--supplement-json 特殊构件=<项目阶段产物>.json \
--supplement-json 梁实例=梁编号实例分解.json \
  --floor-label 首层 --format all -o 首层统一报告
```

统一报告直接给出梁板柱墙基础规格和根数、柱配筋候选、钢筋型号、板厚洞口、
梁净跨状态、混凝土差异以及异常构件回图坐标。P1 起，`cad-beam-reference-reconciliation/v0.1`
补充 JSON 会归一成“梁实例对账”：参考实例、已定位等效实例、缺失等效实例、
编号级量和 A/A+B 转移投影；缺失实例直接进入阻塞异常，B 级转移只进复核异常。
P2 起，统一报告新增“闭合门槛与阻断分组”：`closure_dashboard` 汇总门槛
`pass/warn/fail`、按区域和状态聚合的 blocking 组、梁等效实例/板材料/墙柱归类/
特殊构件的剩余缺口，以及不超过 10 类的高层下一步动作；CSV 和 Markdown 同步输出。
它不重写几何算法，也不补造缺失字段；`formal_ready=false` 时只能用于研发对账。
表格型柱表尚未结构解析时会保留 `partial/index-only`。

P3 起，`cad-quantity-report/v0.4` 会读取结构模型里的 `phase15` 板厚修正摘要和
<项目阶段产物>补充 JSON 里的 `phase15` 回执，直接暴露板拓扑毛面积、净面积、洞口数、
洞口面积、板厚分面积和洞口扣减后的粗折量。板记录也新增 `net_area_m2`。
这只说明洞口扣减口径已经可见，不等于全部板洞口和材料体系闭合。

`cad-member-intersection-audit/v0.1` 把梁中心线拓扑、连梁实例、柱、墙条带和边缘
构件转成矩形后做两两相交检查，输出重叠面积、最小截面高度和潜在重复体积。
`cad-quantity-report/v0.5` 将该结果并入统一报告：直接数据增加重叠对、重叠面积和
潜在重复量，闭合看板增加“构件相交扣减”门槛。当前只给候选扣减证据，不自动改写
混凝土候选合计；必须先确认节点混凝土归属、构件顶底标高和竖向构件通高口径，
才能由同一引擎输出构件净量。

`cad-member-intersection-audit/v0.2` 将同坐标的多组成对重叠先合并成唯一重叠格，
避免三构件同点相交时被重复累计；报告 `v0.6` 同时显示成对原值、去重后体积和消减
的重复量。首层样例为 25 对成体重叠合并成 29 个唯一重叠格，`〈实测〉 m3` 去重为
`〈实测〉 m3`。

`cad-member-intersection-audit/v0.3` 增加候选构件净量：竖向构件保留节点格，
多梁同点保留最大截面高度者，其余按自身截面高度扣除；连梁扣减只作参考，
墙、边缘构件和柱之间的归属未决时不自动扣。`cad-quantity-report/v0.7` 输出梁净扣
`〈实测〉 m3` 和规则试算总量 `〈实测〉 m3`，正式候选合计仍保持 `〈实测〉 m3`。

`cad-slab-opening-audit/v0.1` 把板图开洞图层当作台账逐条清点：先确认成环图形
（对角 X 四端点命中矩形四角、闭合多段线、同图层线段首尾成环），再对剩余图线按
引线包络、紧贴已确认洞口、图框外重复和未闭合折线分类，并允许在板边线、降板边线、
墙、柱和连梁图层上做跨层闭合探测。只有成环图形参与扣板面积，其余一律不扣；
同时把历史洞口候选板逐条映射回当前分类。首层实测：开洞图层 17 条图线全部完成分类，
确认 2 个矩形洞口 `〈实测〉 m2`，板面毛 `〈实测〉 m2`、扣洞净 `〈实测〉 m2`，
3 组待复核折线给出体积上限 `〈实测〉 m3`（不计入扣减），历史 7 个候选板
4 个已解释、3 个待复核。`--reference-gap-m3` 提供一致性判据：待复核项全部按洞口扣除
会超出当前量差，即证明至少部分图线不是洞口。

`cad-quantity-report/v0.8` 读取该审计：直接数据新增开洞图层图线数、确认洞口数/面积、
待复核图线组、待复核体积上限和板毛/净面积，闭合看板新增“板洞口证据”门槛
（台账闭合且无待复核才通过），Markdown 与 CSV 同步输出逐条证据。
`cad_quantity_pipeline.sh` 默认在结构模型之后运行该审计并把结果作为 `板洞口=` 补充
输入统一报告，可用 `--no-slab-opening-audit` 关闭，用 `--slab-opening-dxf`、
`--slab-opening-prior-json`、`--slab-opening-closure-layers`、`--reference-gap-m3`
指定输入。

单独复算板洞口证据台账（不需要重跑整条流水线时）：

```bash
scripts/cad_slab_opening_audit.sh \
  --model-json 首层板属性修正模型.json \
  --geometry-dxf 二层板结构施工图展开.dxf \
  --prior-json <项目阶段产物>模型.json \
  --slab-transform=-117804.128826,〈实测〉 \
  --reference-gap-m3 〈实测〉 \
  -o 板洞口证据台账
```

`--geometry-dxf` 必须是板平面图图框的展开 DXF，且与 `--model-json` 用同一坐标口径；
`--slab-transform` 缺省时读模型里的 `slab_transform`。`--entities-json` 可代替 DXF 复算。

`cad-beam-gap-attribution/v0.1` 把"缺 N 个梁实例"换成可核查的体积归因：以编号体积对账为准，
把差额拆成偏少、偏多和已对齐三类，并用 `min(偏少合计, 偏多合计)` 给出只改归属就能解释的量，
剩下的才是真正需要新几何的量；同时用已展开图中未归属图线池做上限扣减，并给出每个偏少编号
按截面换算的需补梁线长度。实例计数口径差单独计数，明确只影响钢筋支数，不得补造几何。
首层实测：30 个编号中体积一致 8 个、偏少 12 个 `〈实测〉 m3`、偏多 10 个 `〈实测〉 m3`，
净未定位 `〈实测〉 m3`，未归属图线池只有 1 条 `〈实测〉 m3`（最长 400 mm），
仍需新几何 `〈实测〉 m3`；原报缺失 26 个实例中体积只支撑 4 个，其余 22 个是计数口径差。
分解合计 `-〈实测〉 m3` 与台账梁缺口完全一致（`residual_unexplained_m3=0`）。

```bash
scripts/cad_beam_gap_attribution.sh \
  --reconciliation-json <项目阶段产物>梁编号实例分解.json \
  --model-json 结构模型.json \
  --endpoint-json <项目阶段产物>梁端分级.json \
  -o 梁体积缺口归因
```

`cad-quantity-report/v0.9` 读取该归因：新增"梁体积缺口归因"章节、
`beam-volume-gap-attribution` 门槛、分解合计与检索目标，并把梁直接数据键
（净未定位、可转移解释、仅计数口径实例数、需检索新几何量）暴露到"直接可读数据"表。
`cad_quantity_pipeline.sh` 另支持 `--beam-gap-reconciliation-json`、
`--beam-gap-endpoint-json`、`--beam-gap-volume-tolerance-m3` 和 `--no-beam-gap-audit`；
传入梁编号参考对账 JSON 后，流水线会在板洞口审计之后再跑梁体积缺口归因，
并以 `梁量差=` 注入统一报告，产物记入 `beam_gap_json`。

### P9 梁图层覆盖审计与提取盲区（2026-09-11 加）

`cad-beam-coverage-audit/v0.1` 回答"梁图层里还有多少图线没被算量实例吃到"。覆盖判定用
**区间求交**而不是端点命中，部分覆盖的梁线按实长折算，避免"端点碰到就整条算已覆盖"：

```bash
scripts/cad_beam_coverage_audit.sh \
  --model-json 结构模型.json \
  --geometry-dxf 梁几何.dxf \
  --residual-gap-m3 〈实测〉 \
  -o 梁图层覆盖审计
```

未覆盖线段按视图归属分五桶，只有 `inside-extraction-window`
、`outside-window-inside-plan-envelope` 和 `beyond-plan-envelope` 才可能进检索目标；
`mirror-pair-outside-window`（关于模型已登记镜像轴翻折后与已提取实例重合）和
`translated-duplicate-view`（整视图统一偏移的平移孪生）只登记证据、不计漏量。
镜像判定按 `run_registry.mirror_axes` 的**字典列表**逐轴翻折比对（`{"axis_mm": …}`），
平移判定取全窗口模态偏移，偏移候选按"覆盖率最高、位移最小"择优。
平面轮廓取 `members.slab_panels` 与实例范围并集，并回写 `beyond_plan_bbox` 交叉验证。

首层实测（P10 更正后）：窗口内梁线 231 条 / 534399.7 mm，覆盖率 **〈实测〉%**；未覆盖
6 段 / 12100 mm，来自 14 条梁线（8 条部分覆盖），配对 3 条候选梁 / `〈实测〉 m3`，
对照梁缺口 `〈实测〉 m3` 仍有 `〈实测〉 m3` 未被窗口内候选解释。窗口外图线 69 条
（162199.9 mm / `〈实测〉 m3`）判为镜像对称视图、8 条（27200 mm / `〈实测〉 m3`）判为
`-28050 mm` 平移孪生，板面域内窗口外与板面域外候选量均为 `0 m3`。
**P9 的"4.5 m 系统性提取盲区、扩窗可补 `〈实测〉 m3`"结论已证伪**：用
`--bbox=-1470000,720000,-1390000,790000 --margin 0` 重跑源 DWG 新增实体为 0，
且镜像体量是本层缺口的 8 倍，计入即超出广联达参考量，故 `mirror_pair_countable=false`
把它锁在证据层。剩余缺口只能从截面高度取值与编号归属里找，不得用窗口外图线凑量。

`cad-quantity-report/v0.10`（P10 起为 `v0.11`）读取该审计：新增"梁图层覆盖审计"章节、`beam-coverage-audit`
门槛（`coverage_closed` 且未解释量在容差内才 pass）、direct 键
（`beam_in_frame_coverage_ratio`、`beam_uncovered_in_frame_length_mm`、
`beam_candidate_in_frame_volume_m3`、`beam_candidate_window_out_volume_m3`、
`beam_candidate_beyond_plan_volume_m3`、`beam_duplicate_view_offset_mm`、
`beam_residual_still_unexplained_m3`、`beam_coverage_closed`、
`beam_mirrored_view_count`、`beam_mirror_pair_volume_m3`、`beam_mirror_pair_countable`、
`beam_translated_view_volume_m3` 等）和 CSV
`梁覆盖审计`/`梁覆盖候选` 行。`cad_quantity_pipeline.sh` 新增 `--beam-coverage-dxf`、
`--beam-coverage-residual-gap-m3`、`--beam-coverage-tolerance-m3`、
`--no-beam-coverage-audit`：默认复用梁几何产物，缺口默认取 P8 的
`residual_needing_new_geometry_m3`，在梁体积缺口归因之后执行并以 `梁覆盖=` 注入统一报告，
产物记入 `beam_coverage_json`。审计只登记覆盖证据，不改变任何构件体积，
`formal_ready` 仍为 false。

### P11 梁候选段归属与截面口径复核（2026-09-11 加）

P9/P10 把"窗口外图线"清零之后，剩余缺口只剩两种可能：截面高取低了，或者实例长度/编号
归属没配齐。`cad-beam-candidate-attribution/v0.1` 先把这两种可能分开，再谈回图：

```bash
scripts/cad_beam_candidate_attribution.sh \
  --model-json 结构模型.json \
  --coverage-json 梁图层覆盖审计.json \
  --reconciliation-json 梁编号参考对账.json \
  --gap-json 梁体积缺口归因.json \
  --floor-label 首层 -o 梁候选段归属
```

- **截面口径复核**：把每条实例截面换成编号的 `reference_single_section` 重算体积，
  编号匹配大小写不敏感（`KL13A(1)` 与对账表 `KL13a(1)` 必须能配上，否则复核会静默漏掉）。
  首层 63 条可比对实例全部一致，体积差 `〈实测〉 m3` —— 偏少编号的缺口**不是**截面高造成的。
- **候选段归属**：窗口内未覆盖候选段只有在**同轴 ≤60 mm、端头间隙 ≤400 mm** 时才归属到已有
  编号实例，并按实例真实截面计量（首层 `271+272` → `KL13A(1)` 200x500 = `〈实测〉 m3`）；
  无同轴实例的一律记 `no-coaxial-run`，梁宽与实例截面不一致的记 `section-conflict`，两者都
  **不得**凭位置补编号或回写体积。
- **缺口分解恒等式**：`缺口 = 可归属 + 有几何无编号 + 本图框无法解释`，另列
  `caliber_adjustment_m3`（候选假定高换成实例截面高的量差）与覆盖审计口径交叉核对，
  首层为 `〈实测〉 = 〈实测〉 + 〈实测〉 + 〈实测〉`，交叉核对差 `〈实测〉 m3`。
- **偏少编号认领**：候选段按缺量从大到小**排他认领**（一条线只能被一个编号认领），
  首层 14 个偏少编号中 2 个可认领、2 个属计数口径（不需要新几何）、**10 个本图框无线可配**，
  共需跨图框检索 `37785 mm / 〈实测〉 m3`（毛差口径，净需补几何仍是 `〈实测〉 m3`）。

`cad-quantity-report/v0.12` 读取该结果：新增"梁候选段归属与截面口径复核"章节、
`beam-candidate-attribution` 门槛（四项门槛全过才 pass）、direct 键
（`beam_section_caliber_delta_m3`、`beam_section_mismatch_run_count`、
`beam_candidate_attached_m3`、`beam_candidate_unattached_m3`、
`beam_unexplained_in_frame_m3`、`beam_unattached_length_mm`、
`beam_decomposition_identity_closed`、`beam_cross_frame_code_count`、
`beam_cross_frame_needed_length_mm`）和 CSV `梁候选归属`/`梁候选段`/`梁跨图框目标` 行。
`cad_quantity_pipeline.sh` 在覆盖审计之后自动执行本步，可用
`--no-beam-candidate-attribution` 关闭，或用 `--beam-candidate-reconciliation-json`、
`--beam-candidate-axis-tolerance-mm`、`--beam-candidate-joint-max-mm` 调整；
产物记入 `beam_candidate_attribution_json`，以 `梁候选归属=` 注入统一报告。
本节只澄清证据归属，不改变构件体积，`formal_ready` 仍为 false。

### P12 梁编号图框标签索引（2026-09-11 加）

P11 把剩余缺量写成"须跨图框或大样检索"，但没人证明过那些编号**画在哪个图框**。
`cad-beam-frame-label-index/v0.1` 流式扫整册展开 DXF（43 MB / 624 万行，边读边判组码，
不加载实体），只留两类文字：梁编号集中标注（`KL\d+(n)` 等）和图名（`S-图名`），
再按"图名在图框下方"的规则给每条标注建图框归属：

```bash
scripts/cad_beam_frame_label_index.sh \
  --geometry-dxf 整册展开.dxf \
  --reconciliation-json 梁编号参考对账.json \
  --target-frame 二层梁平法施工图 -o 梁编号图框标签索引
```

- 图框先按 `x` 分列（默认列容差 50 km，**必须先在列内按 `y` 排序**再取下一条图名的 `y`
  作为上界，否则图框带上界会串到别的列，实测把 44 条标注误算成 114 条）。
- 标注归属"下方最近图名"所在图框；同名编号在别的楼层图框的标注一律不计本层。
- 与广联达对账表联接后按 `CAD链长 ÷ 参考单实例轴长` 分四类：
  `length-not-closed-in-same-beam`（〈实测〉~〈实测〉，缺在同一根梁的长度里）、
  `instance-or-length-missing`（<〈实测〉）、`instance-count-mismatch`（≥〈实测〉，
  CAD 链长已超单实例，是参考实例数与图面标注数不一致）、
  `no-label-in-target-frame`（本层图框根本没标注）。

首层实测：整册 353 条编号标注、38 处图名、9 个梁图框 + 6 个墙柱图框，
`二层梁平法施工图` 框内 44 条标注（`x` 全部 ≤ -1420000，右侧无半幅图，
`一层` 框 84 条是其真实规模差异）。14 个偏少编号**在本层图框都有标注**（
`no-label-in-target-frame = 0`）：5 个 `length-not-closed-in-same-beam`
（`〈实测〉 m3`，走支座与净跨闭合）、7 个 `instance-count-mismatch`
（`〈实测〉 m3`，按图面标注数复核广联达实例数口径）、2 个 `instance-or-length-missing`
（`〈实测〉 m3`，`L5(1)` CAD 链长 0、`WKL1(2)` 只有单实例的 〈实测〉）。
**P11 的"须跨图框检索 10 个编号 / 37785 mm"方向被更正**：同名标注的其余副本都在
别的楼层图框（`KL18(3)`/`KL12(2)`/`KL14(1)`/`KL10(1)`/`L5(1)` 各在三层~五层、六层~十层等
出现 1 次），跨楼层取量会算错层，缺量必须回到本层图框的长度闭合与实例口径核对。

产物 JSON/CSV/MD + `sha256`，键 `code_index`、`frames`、
`summary.classification_volume_m3`；不并入统一报告，也不改任何构件体积，
`formal_ready` 仍为 false。

### P13 梁净跨口径与支座扣减对账（2026-09-11 加）

P12 分出"同一根梁长度未闭合"之后，必须先问一句：那段长度是**没画**还是**被支座占掉了**。
`cad-beam-span-closure/v0.1` 用模型自身的支座证据把毛差定责：

```bash
scripts/cad_beam_span_closure.sh \
  --model-json 结构模型.json \
  --reconciliation-json 梁编号参考对账.json \
  --frame-index-json 梁编号图框标签索引.json \
  --intersection-json 构件净量相交扣减试算.json \
  --floor-label 首层 -o 梁净跨口径与支座扣减对账
```

- 逐根梁：`members.beams` 的 `centerline_length_mm` 减 `clear_length_mm` 得支座扣减，
  带 `inferred_end_supports` 推定端宽度、`support_evidence` 类型和中心线起止坐标（回图用）。
- 逐编号：`参考单实例轴长 −（CAD 链长 ÷ 选中实例数）` 得单实例长度差，再按
  链丢失 → 实例口径不稳定（选中数 ≠ 模型实例数）→ 无长度差 → 长度差 ≤ 支座扣减 →
  长度差 ≤ 推定端宽度 → 真需补几何 的顺序定责。
- 毛差恒等：五类量差合计必须等于偏少编号毛差（首层 `〈实测〉 m3`，与 P11 一致）。

首层实测：44 根梁中心线 `240800` mm、净长 `201725` mm，支座扣减 `39075` mm；
中心线口径 `〈实测〉 m3` 与净跨口径 `〈实测〉 m3` 差 `〈实测〉 m3`，
而构件相交审计的梁侧可扣只有 `〈实测〉 m3`，**两者相差 `〈实测〉 m3`**：
净跨扣减里有大量推定端（`clear-span-inferred` 19 根、`clear-span-review` 24 根、
推定端宽度合计 `10000` mm），支座未经原图确认前不得用净跨口径替换中心线口径。
14 个偏少编号定责结果：`deficit-within-support-deduction` 5 个 `〈实测〉 m3`
（轴线/净跨口径差，计入即与柱墙重复）、`no-length-deficit` 2 个 `〈实测〉 m3`、
`instance-count-caliber-unstable` 5 个 `〈实测〉 m3`（选中实例数与模型实例数不一致）、
`chain-lost-in-reconciliation` 1 个 `〈实测〉 m3`（`L5(1)` 模型有实例但编号链没选中）、
`deficit-exceeds-support-inference` 1 个 `〈实测〉 m3`（`WKL1(2)` 两跨只提出一跨）。
**真正需要补几何的只剩 `〈实测〉 m3` + 修链 `〈实测〉 m3`**，其余是口径问题。
产物 JSON/CSV/MD + `sha256`，不改任何构件体积，`formal_ready` 仍为 false。

### P19 单入口单报告收口（2026-09-11 加）

P12/P13 两个索引工具已并入统一报告与流水线，`cad-quantity-report/v0.13` 一次输出 8 项闭合门槛：

```bash
scripts/cad_quantity_pipeline.sh 结构图.dwg \
  --floor-label 二层梁平法施工图 --out 输出目录 \
  --beam-gap-reconciliation-json 梁编号参考对账.json \
  --frame-index-dxf 整册展开.dxf
```

- 流水线新增步骤 `beam-frame-label-index`（需要 `--frame-index-dxf`，
  目标图框取 `--frame-index-target-frame`，缺省用 `--floor-label`）和
  `beam-span-closure`（需要图框索引 JSON，可用 `--span-closure-frame-index-json` 指定已有产物）；
  关闭开关 `--no-beam-frame-index`、`--no-beam-span-closure`。
- 统一报告新增章节"梁编号图框标签索引""梁净跨口径与支座扣减"，
  门槛 `beam-frame-label-index`、`beam-span-caliber`，direct 键 19 个
  （`beam_frame_count`、`beam_length_not_closed_volume_m3`、
  `beam_no_label_in_target_frame_count`、`beam_centerline_length_mm`、
  `beam_clear_length_mm`、`beam_support_deduction_length_mm`、
  `beam_span_caliber_difference_m3`、`beam_span_vs_intersection_conflict_m3`、
  `beam_deficit_caliber_volume_m3`、`beam_deficit_needs_geometry_m3`、
  `beam_chain_lost_volume_m3`、`beam_verdict_total_m3` 等），
  CSV 新增 `梁图框归属`/`梁净跨口径`/`梁长度定责` 行。
- 回归口径：并入前后 `concrete_candidate_total_m3` 必须逐项相等（首层 `〈实测〉 m3`，
  仅 `gate_status_counts` 由 1 fail/5 warn 变为 1 fail/7 warn），
  证据收口不得改变任何构件体积。

### P20 多跨梁跨支座续接候选（2026-09-11 加）

P13 剩下的"真需补几何"经 P19 复查其实是链在中间支座被截断。
`cad-beam-multispan-closure/v0.1` 用图面线段把续接补出来：

```bash
scripts/cad_beam_multispan_closure.sh \
  --model-json 结构模型.json \
  --geometry-dxf 梁图层展开.dxf \
  --reconciliation-json 梁编号参考对账.json \
  --axis-tolerance-mm 400 --gap-tolerance-mm 200 -o 多跨梁续接候选
```

- 图层分工：梁线取 `S-梁-虚线`/`S-梁-实线`，支座取 `S-柱*`/`砼墙*`/`S-墙*`，
  明确排除 `S-剪力墙-连梁`（那是构件不是支座）和 `梁附加箍筋`（标注线）。
- 带宽数 `(n)` 才允许 `n-1` 次续接，两端交替外扩：先找紧贴当前端头的支座段
  （间隙 ≤200 mm），再找紧贴该支座另一侧的同轴梁段（轴偏 ≤400 mm），
  支座宽度计入轴线长、梁段长度单列，逐条留 `support_handle`/`beam_handle` 证据。
- 无参考单实例轴长的编号判 `no-reference-single-length`，不得算"已闭合"；
  全部结果 `applied_to_formal_quantity=false`，属候选台账。

首层实测：8 根带宽 ≥2 的梁（7 个编号）里 2 根续接成功 —— `B0037 WKL1(2)` 穿过
`S-柱#260`(500 mm) 接上 `#1AC`(3700 mm)，中心线 5650→9850 mm；`B0044 WKL5(2)` 穿过
`S-柱#263` 接上 `#1BB`(3300 mm)，5650→9450 mm。合计补梁线 `7000 mm` + 支座 `1000 mm`
= 轴线长 `8000 mm`，候选体积 `〈实测〉 m3`；单实例长度缺口 `12500 mm → 4500 mm`（闭合率 64%）。
6 根 `no-continuation-found` 是链已按轴链合并或端头无紧贴支座段，不属续接问题。

`cad-quantity-report/v0.14` 已并入该台账（章节"多跨梁跨支座续接候选"、门槛
`beam-multispan-continuation`、direct 键 8 个 `beam_multispan_*`、CSV
`多跨梁续接`/`多跨梁续接段`）；`cad_quantity_pipeline.sh` 新增
`--multispan-geometry-dxf`、`--no-beam-multispan-closure`，产物键
`beam_multispan_closure_json`，并入后回归校验：`concrete_candidate_total_m3`
仍 `〈实测〉 m3` 不变，只有门槛由 1 fail/7 warn 变为 1 fail/8 warn。

### P21 梁实例双口径去重（2026-09-11 加）

模型里同时存在两套梁口径：`run_registry`（算量实例，按平行线中心线成链，70 条）
和 `members.beams`（拓扑模型梁，44 根）。统一分账的梁量走的是 `run_registry`
（`〈实测〉 m3`）加楼梯梁等特殊构件，因此必须先确认模型梁口径能不能再并进来。
`cad-beam-instance-dedup/v0.1` 干这件事：

```bash
scripts/cad_beam_instance_dedup.sh \
  --model-json 首层结构模型.json \
  --code-axis-tolerance-mm 5000 --min-overlap-ratio 0.5 \
  --floor-label 首层 -o 梁实例双口径去重
```

- 配对以「同编号 + 同向 + 沿轴重叠 ≥ 较短者一半」为主证据。模型梁轴是网格轴、
  run 轴是边线中轴，两者可差 1.5 m 级（实测 2185.5 mm），所以轴距只作 5 m 的
  宽松约束；先按轴距最近做一对一锁配，再给未覆盖的梁续接同编号 run。
- 无 run 可配的模型梁分三类，只有后两类才是候选新增：
  `attribution-conflict` 同编号在 CAD 里有未配对 run，只是位置或方向不符；
  `model-extra-instance` 该编号其余实例已被配对，模型多出一根；
  `code-absent` run 口径完全没有该编号。
- 反向也记：只有 run 没有模型梁的实例按编号证据分层
  （`leader-target`/`mirror-label`/`nearest-label`/`unresolved`）单列，
  镜像推定的编号不得升级为构件量。

首层实测：44 根模型梁里 21 根与 run 判为同一根物理梁，两套口径相加会重复计量
`〈实测〉 m3`；23 根无 run 可配的梁中 22 根/`〈实测〉 m3` 属归属冲突，
真编号缺失只有 `L5(1)` 一根/`〈实测〉 m3`。**结论：模型梁口径净新增仅 `〈实测〉 m3`，
梁的 `-〈实测〉 m3` 缺口不能靠并入 44 根模型梁补齐。** run 侧另有 46 条/`〈实测〉 m3`
没有模型梁对应，其中 `mirror-label` 19 条/`〈实测〉 m3` 只有镜像推定证据，
`leader-target` 20 条/`〈标高〉 m3` 有引线标注但模型未建实例，属下一步回图复核对象。

定责还反查 run 侧：46 条未配对 run 分为 `continuation-candidate` 2 条/`〈实测〉 m3`
（端头与同编号梁相邻，是续接段不是新实例）、`attribution-conflict` 15 条/`〈实测〉 m3`
（同位置模型梁挂别的编号，需回图定谁对）、`same-code-other-location` 10 条/`〈实测〉 m3`
（同编号实例在别处，多为镜像推定）、`model-missing-instance` 19 条/`〈实测〉 m3`
（该位置没有任何模型梁，其中仅 8 条 `leader-target` 带引线证据）。
另外对 run 口径内部做同轴重叠扫描（`--self-overlap-axis-tolerance-mm 400`）：
首层 `70` 条 run 两两零重叠/`〈实测〉 m3`，说明统一分账的梁基数 `〈实测〉 m3` 自身没有
重复计量，门槛 `run-population-no-self-overlap=true`。

### P22 梁实例双口径去重并入单入口与统一报告（2026-09-11 加）

P21 的判定是独立脚本，P22 把它接成一条命令的一部分：`cad_quantity_pipeline.py`
默认多跑一个 `beam-instance-dedup` 步骤（只吃结构模型 JSON，不需要额外 DXF），
产物键 `beam_instance_dedup_json`，开关 `--no-beam-instance-dedup`，
并把结果作为 `梁实例去重=<json>` 自动喂给统一报告。

`cad-quantity-report/v0.15` 新增内容：

- direct 键 14 个 `beam_dedup_*`（配对根数、重复计量、净新增候选、归属冲突、
  编号缺失、未配对 run 体积、模型缺实例体积、run 内部重叠处数与体积、
  `beam_dedup_applied_to_formal=false`）。
- 门槛 `beam-instance-dedup`：`no-silent-double-count` 且
  `run-population-no-self-overlap` 同时成立才 `pass`，否则 `warn`。
- Markdown 章节「梁实例双口径去重」含无 run 梁分类表与未配对 run 定责表；
  CSV 新增 `梁实例去重`/`梁实例去重-无run梁`/`梁实例去重-未配对run` 三类行。

回归（重跑脚本已落 `work/run_unified_report.sh`，14 项 supplement）：
`concrete.quantities` 与 P20 报告逐项相同，`concrete_candidate_total_m3` 仍
`〈实测〉`、差额仍 `〈实测〉`；`direct_outputs` 113 → 127 键，只新增不修改，
唯一变化键是 `gate_status_counts`（1 fail/8 warn → 1 fail/9 warn）；
构件表、柱表、钢筋表、板表、梁表、异常清单逐项零漂移。
单测 132 → **135/135**（新增报告集成 1 项、流水线默认执行与开关跳过 2 项）。

### P23 梁编号归属冲突定责（2026-09-11 加）

P21 暴露出 22 根"归属冲突"模型梁，但按轴距 5000 mm 判冲突会把平行邻线误算进来。
`cad-beam-attribution-conflict/v0.1` 收紧判据并用引线标注定责：

```bash
scripts/cad_beam_attribution_conflict.sh \
  --model-json 首层结构模型.json \
  --conflict-axis-tolerance-mm 2500 --min-overlap-ratio 0.5 \
  --strong-label-axis-tolerance-mm 1000 -o 梁编号归属冲突定责
```

- 冲突对判据：同向 + 同截面 + 轴距 ≤2500 mm + 沿轴重叠 ≥ 较短者一半 + 底编号不同
  （`KL13A(1)` 与 `KL13` 归一后仍算不同编号）。`--any-section` 可放开截面要求。
- 定责证据只用落在**两条几何重叠区间**内的引线标注，避免邻线编号混入；
  引线轴距 ≤1000 mm 记 `strong`，否则记 `near`。
- 四类判定：`run-label-holds` 只有 run 编号被标注指向这段线（模型梁错挂）；
  `beam-label-holds` 反之；`dual-label-same-line` 两侧都有标注指向同一条线，
  属图纸同轴两构件，必须人工定跨；`no-label-evidence` 两侧都无标注，不得改编号。

首层实测：19 对冲突（涉及 run 13 条、模型梁 18 根，完全同轴 3 对），
两口径相加重复计量风险 `〈实测〉 m3`；`run-label-holds` 15 对/`〈实测〉 m3`、
`beam-label-holds` 1 对/`〈实测〉 m3`、`dual-label-same-line` 1 对/`〈实测〉 m3`、
`no-label-evidence` 2 对/`〈实测〉 m3`；引线置信 `strong` 17 对、`near` 2 对。
典型：`B0005 KL12(2)` 与 `R0043 WKL4(1)` 同轴同截面全长重合，该线上只有 `L0008`
（`WKL4`）有编号，判模型梁错挂。定责只影响编号台账与逐编号对账，不改混凝土总量。

P23 已并入单入口与统一报告：`cad_quantity_pipeline.py` 默认多跑
`beam-attribution-conflict` 步骤（产物键 `beam_attribution_conflict_json`，
开关 `--no-beam-attribution-conflict`），`cad-quantity-report/v0.16` 新增 11 个
`beam_conflict_*` 键、门槛 `beam-attribution-conflict`、章节「梁编号归属冲突定责」
与 CSV `梁编号归属冲突`/`梁编号归属冲突对`。回归：`concrete.quantities` 与 P22 报告
逐项相同、候选总量仍 `〈实测〉`，`direct_outputs` 只新增键，唯一变化键仍是
`gate_status_counts`（1 fail/9 warn → 1 fail/10 warn，共 11 项门槛）。
单测 142 → **145/145**；重跑命令仍走 `work/run_unified_report.sh`。

### P24a 冲突定责改用引线共线判据（2026-09-11 加）

P23 的 2500 mm 轴距容差把相距 1300~2300 mm 的平行邻线也算成同轴冲突，
导致 15 对"run 编号成立"和 3 对"要人工定跨"里有假。修法：**是否同一根梁由两侧引线的
target 轴决定，不由几何轴距决定**（模型梁轴是网格轴，轴距不可信）。

```bash
scripts/cad_beam_attribution_conflict.sh \
  --model-json 结构模型.json --same-line-label-axis-tolerance-mm 200 \
  --same-line-max-axis-offset-mm 1200 --span-split-min-gap-mm 200 -o 梁编号归属冲突定责
```

- 两侧都有引线时：`|引线A.target轴 - 引线B.target轴| ≤ 200 mm` 才算同轴；
  否则 `parallel-distinct-lines`，风险记 0。缺一侧引线时退回几何轴距 ≤1200 mm。
- 同轴且两侧引线目标区间首尾分开（间隙 ≥200 mm）判 `same-line-different-spans`：
  这是算量实例成链没在支座断开的证据，同时给出断点区间。
- 引线取证范围由"重叠区间"改为"并集区间"，否则同轴异跨的引线会被自己排除掉。

首层实测：19 对候选 → 真同轴 9 对、平行邻线误判 10 对（〈标高〉 m³ 体积不再算风险），
重复计量风险由 `〈实测〉 m3` 降到 **`〈标高〉 m3`**；`run-label-holds` 8 对/`〈标高〉 m3`、
`same-line-different-spans` 1 对/`〈实测〉 m3`、`dual-label-same-line` 与
`no-label-evidence` 均为 0 对 → **原先"需要人工确认"的两项消失**。
断链证据：`R0057 KL2(1)` 与 `B0043 WKL4(1)` 引线 target 轴相同（x=-1430014.5），
目标区间 764990.5~767140.5 与 769640.5~773440.5，断点 `767140.5→769640.5`（2500 mm 支座）。
`cad-quantity-report/v0.16` 新增 `beam_conflict_same_line_pair_count`、
`beam_conflict_parallel_pair_count`、`beam_conflict_span_split_pairs`，
门槛 `beam-attribution-conflict` 在有异跨断链时保持 warn。回归：
候选总量仍 `〈实测〉`、差额仍 `〈实测〉`，只有定责类键变化。单测 145 → **147/147**。

### P25 广联达清单口径分解与算量范围边界（2026-09-11 加）

同一个广联达模型有两份导出：`模型云指标/…(指标报表).xlsx`（清单口径，按构件
类型分层）和`按构件分混凝土工程量-主体/….xls`（构件实物量口径）。两者类别
集合不同，之前只用了后者，等于把口径边界当成了 CAD 缺口。

```bash
scripts/cad_glb_indicator_scope.sh \
  --indicator-xlsx "…/模型云指标/某栋楼(导出)(指标报表).xlsx" \
  --component-export-json outputs/<项目阶段产物>-广联达首层按构件参考工程量.json \
  --floor 首层 --reference-total-m3 〈实测〉 \
  --cad-slab-volume-m3 〈实测〉 --cad-beam-independent-m3 〈实测〉 \
  --cad-vertical-candidate-m3 〈实测〉 \
  -o outputs/<项目阶段产物>
```

结论（某栋楼首层，全部由脚本重算，非手填）：

- 清单口径 `〈实测〉 m3`（13 类）与构件实物量口径 `〈实测〉 m3`，扣掉清单不含的
  叠合整厚+预制底板+板缝+坡道 `〈实测〉 m3` 后残差 `-〈实测〉 m3`，两口径勾稽成立。
- 参考量 `〈实测〉 = 主体 〈实测〉 + 装配式板层 〈实测〉`，其中预制底板
  `〈实测〉 m3` 是叠合整厚的子层，叠加即重复计量，去重参考应为 `〈实测〉 m3`。
- 现浇板 7 行的 `是否叠合板后浇` 全为 `否`、合计 `〈标高〉` 与清单现浇板相同，
  且预制底板面积 `〈实测〉` 是整厚面积 `〈实测〉` 的子集，据此判叠合口径为 A。
  此前"整厚反算 87 mm 对不上图面 130 mm"的疑点不成立：广联达现浇板行同样
  反算出 `〈实测〉/180.1/165.7 mm`（名义 `120/130/140`），说明投影面积列不能作
  板厚分母，禁止再用体积除面积反算板厚。
- CAD 独立现浇板 `〈实测〉` 对现浇口径 `〈实测〉` 差 `〈实测〉 m3`。这个吻合
  **不作为口径证据**（P26 更正）：CAD 板面域同时含纯现浇与叠合区整厚，两个
  方向相反的误差会抵消，见下面 P26。
- 二次结构 `〈实测〉`、楼梯梯段 `〈实测〉`、建筑零星 `〈实测〉`（台阶 `〈实测〉`
  最大）判为 CAD 结构图范围外，不得再用来解释 CAD 缺口。
- CAD 独立可核量落为机器键：`cad_independent_verifiable_m3 = 〈实测〉`
  （梁 `〈实测〉` + 墙柱 `〈实测〉`），含独立板量 `〈实测〉`；
  参考回填 `reference_backfill_m3 = 〈实测〉`。
- 统一报告 `v0.17` 增 18 个直接数据键和 2 个门槛（`glodon-schedule-scope`
  pass、`prefab-sublayer-double-count` fail），量值零漂移。
- 单入口流水线新增可选步骤 `glodon-indicator-scope`，成对给出
  `--glodon-indicator-xlsx` 与 `--glodon-component-export-json` 才跑；
  CAD 侧口径值由流水线从台账和模型自取，不需要手填。

### P26 叠合区覆盖探测与板口径拆解（2026-09-11 加）

用 100 mm 网格做点-多边形覆盖，把 CAD 板面域按"压在已观测预制底板上 / 没压在"
拆开，分别按各自板厚折算体积，再与广联达现浇板和叠合板整厚对账。
脚本：`work/phase26_slab_prefab_coverage_probe.py`（项目级，未升为 skill 内核），
产物 `outputs/<项目阶段产物>`。

- 双向验证一致：预制底板侧交叠 `〈实测〉 m2`，板面域侧 `〈实测〉 m2`（网格偏差 0.9%）。
- CAD 纯现浇体积 `〈实测〉 m3` 对广联达现浇板 `〈标高〉 m3`，差 `+〈实测〉 m3`（〈实测〉%）。
- CAD 叠合区整厚体积 `〈实测〉 m3` 对广联达整厚 `〈实测〉 m3`，差 `-〈实测〉 m3`，
  只覆盖叠合区面积的 `〈实测〉%`。
- 面积缺口 `〈实测〉 m2` 被拆成两笔反向误差：叠合区少 `〈实测〉 m2`
  （布置图只观测到 40/78 块预制底板，另 38 块无 CAD 面域）、
  纯现浇多 `〈实测〉 m2`（广联达现浇板面积列偏小，与"投影面积不可作分母"一致）。
- 由此撤回 P25 里"CAD 总量吻合支持口径 A"的说法；口径 A 只由现浇板纯净性
  与面积包含关系支撑。
- 下一步明确：把预制底板布置图整册展开，补到 78 块面域，叠合区才有独立量。

### P27 叠合层配比核验与预制底板图框孪生（2026-09-13 加）

一次性流式扫描整册展开 DXF（43 MB，`work/1f_full_flatten.dxf`，不整体载入内存），
把 `S-PC-叠合板轮廓` 闭合环按图名就近归到图框，再与广联达叠合板面积配比核对。
脚本 `work/phase27_prefab_frame_twin_check.py`，
产物 `outputs/<项目阶段产物>`。

- 整册 123 个闭合叠合轮廓里，标准层图框 42 个 / 〈实测〉 m2，屋面层图框 42 个 /
  〈实测〉 m2；两组面积多重集完全相同且整幅平移 (0, -74400) mm，
  是同一布置的复用图框，**两层面积不得相加**（〈实测〉 m2 是错误值）。
  <项目阶段产物>取 42 块 〈实测〉 m2 正确，窗口切图假设已证伪。
- 叠合层配比：预制底板 〈实测〉 m2 是整厚 〈实测〉 m2 的 〈实测〉%，余量 〈实测〉 m2
  与板缝 〈实测〉 m2 同量级；单块均面积 CAD 〈实测〉、预制 〈实测〉（差 -4.4%）、
  整厚 〈实测〉（差 2.3 倍）→ 图面画的是预制条板层，口径 A 得到量化支撑。
- 广联达按构件导出的 `板厚(m)` 列不可用：DHB 记 2.6 m、B-120 记 〈实测〉 m、
  B-130 记 〈实测〉 m、B-140 记 〈实测〉 m、基础层小计 2.6 m，与体积/投影面积不自洽；
  广联达侧只有 `体积` 与 `数量` 两列可作对账依据。
- 内核 `cad_glb_indicator_scope.sh` 增 `--cad-outline-count/--cad-outline-area-m2`，
  自动算 `prefab_over_whole_area_ratio`（〈实测〉~〈实测〉 才算配比一致）与三类单块均面积，
  并加 `prefab-sublayer-ratio-consistent` 闭包位；统一报告 v0.17 增 3 个键，
  门槛 `prefab-sublayer-double-count` 证据带上配比。回归：量值零漂移，
  候选仍 〈实测〉、参考仍 〈实测〉、13 项门槛 2 fail / 10 warn / 1 pass。

### P28 板面域分层与板缝条带归属（2026-09-13 加）

把 CAD 板面域按 100 mm 网格分成三类：压在预制底板轮廓上、紧邻轮廓 350 mm 条带、
纯现浇，再与广联达现浇板/板缝/整厚三行分别对账。脚本
`work/phase28_slab_bin_reconciliation.py`（复用 P27 的流式读图函数），
产物 `outputs/<项目阶段产物>`。

- 布置图图框到模型坐标的平移 `(-353412.428826, 68505.754354)` 自证通过 32/40 块
  （中心 500 mm、面积 〈实测〉 m2 容差），未过的那 8 块是异形板中心偏移，取用前须知晓。
- CAD 板面域 〈实测〉 m2（网格统计 〈实测〉，误差 〈实测〉 m2）分成：
  纯现浇 〈实测〉、板缝条带 〈实测〉、压在预制底板上 〈实测〉。
- 恒等式闭合：广联达整厚未覆盖 〈实测〉 m2 - 纯现浇多出 〈实测〉 m2
  - 网格误差 〈实测〉 m2 = 净缺口 〈实测〉 m2，残差 〈实测〉。
  所以"缺 〈实测〉 m2"不是漏画板，而是叠合区整厚没有 CAD 面域，被现浇多出的面积抵掉。
- 新发现的重复计量：CAD 板缝条带 〈实测〉 m2 是广联达单列板缝 〈实测〉 m2 的 〈实测〉%，
  折方 〈实测〉 m3 与广联达板缝 〈实测〉 m3 重叠，之前没识别。
- 纯现浇体积 〈实测〉 m3 对广联达现浇板 〈标高〉 m3，差 -〈实测〉 m3（-4.8%）。
- 真瓶颈是板厚证据链：69 块面板里 〈实测〉 m2（〈实测〉%）板厚取自图纸说明默认 130 mm，
  只有 〈实测〉 m2 来自尺寸直接标注，12 块 120 mm 靠图例填充判定。
  因此**逐厚档面积差不可用**（120 档 CAD 〈实测〉 对广联达 〈实测〉、130 档 〈实测〉 对 〈实测〉），
  只有总量差可信；分档出量前必须逐块取证板厚。
- 统一报告 v0.17 -> v0.18：新增 10 个直接数据键和 2 个门槛
  （`slab-seam-band` warn、`slab-thickness-evidence` fail），
  15 项门槛 3 fail / 11 warn / 1 pass，回归零漂移。

### P29 板厚图例冲突与体积敏感性（2026-09-13 加）

先量化再决定修不修：把"图例填充厚度"和"当前归档厚度"逐块比对，
算出改档后的体积摆动区间，同时把图面 `S-板-板厚 h=` 标注绑定回面板。
脚本 `work/phase29_slab_thickness_evidence.py`（自含流式读图，不再依赖临时文件），
产物 `outputs/<项目阶段产物>`。

- 冲突 10 块 / 〈实测〉 m2（占板面域 〈实测〉%），但改档的体积摆动只有
  〈实测〉 m3，占候选总量 〈实测〉%。**总量对板厚归档不敏感，分档才敏感。**
- 图面直接板厚标注只有 4 处 `h=130`，其中 2 处落进面板且与归档一致，
  另 2 处落在面板外（降板区与叠合区）；说明默认档实测有 130 与 140 两档。
  所以"逐块直接板厚证据"在图纸本身里就是稀缺的，不是提取遗漏。
- 要按档出量必须做子面域拆分：一块面板内可同时有 130 与 140 填充
  （如 `P0002` 〈实测〉 m2 里 〈标高〉 m2 被 140 填充压住），
  当前面板只记了 `hatch_area_m2` 汇总值，缺 HATCH 边界几何。
- 统一报告 v0.18 增 7 个键、1 个门槛（`slab-thickness-conflict` warn），
  16 项门槛 3 fail / 12 warn / 1 pass，重跑幂等（`direct_outputs` 与门槛全等）。
- 项目内分析脚本已共用 `work/cad_dxf_stream.py` 流式读展开 DXF，
  不再引用 `/tmp`，可重复执行。

### P48 编号归属必须逐对定主并做转移对平，判不了的不许硬定（2026-09-14 加）

冲突定责以前只给一句"两口径相加风险若干立方"，等于把几十对冲突压成一个数让人自己看图。
`cad_beam_attribution_conflict.sh` 现在在判定之后再加一层归属：

- 每对冲突必须落一个归属结论：`owner-decided`（引线目标落在这段绘制线上的一侧成立）、
  `resolved-separate-lines`（两侧引线各指自己的轴，本就是平行邻线，不算冲突）、
  `review-open`（同轴双标注、无标注证据、同线异跨中间段）。
- 定主只搬编号归属、不搬几何：重叠段体积从错挂方搬到成立方，
  逐编号增减求和必须为 0（`conflict-ownership-transfer-balanced`）；
  残差非 0 就是归属层偷偷改了总量，先回退再查因。
- 风险量必须拆成 `closed + residual = total`，报告与清单都只引用归属后的剩余风险；
  整块风险量与逐对明细分两列，同一笔重叠不得在清单里被加两遍。
- 同线异跨（一根绘制线被两个编号首尾共用）默认判 open：这是算量实例未在支座断链的症状，
  先修断链再定主，直接定主等于承认几何是对的。
- 新门槛一律追加尾部（`tail_gates`），插在中间会把后面每条门槛的索引挪掉，
  逐项回归会报出一片假漂移。

### P50 换一栋楼先查图框裁切，别急着怀疑算量内核（2026-09-14 加）

单入口在第二栋楼（2# 楼结构图）上第一次真跑，结论是"跑得通、出不了量"，
而根因不在算量，在图框定位与裁切：

- 图框 bbox 若来自文字聚类，只会框到标题栏附近，按它裁切会把梁线、墙线大半切掉。
  症状非常具体：构件表能识别出全部梁编号与截面，但状态一律 `no-centerline`、体积 0。
  看到"编号有、截面有、长度为 0"，第一嫌疑是裁切框，不是链式算法。
- 图名到图框的自动配对在图框密集排布的本子上会错配（同一张墙柱图，
  文字聚类把它配成别的名，块名聚类又配成板配筋图）。错配比配不上更危险，
  因为它会静默算另一层的量。所以流水线必须支持显式 `--beam-bbox/--support-bbox/--slab-bbox`
  覆盖，且覆盖优先于自动定位。
- 跨图框自动配准失败不能终止整条流水线：允许退回单图框模式继续产出，
  但必须把降级原因写进 manifest 和报告"口径声明"，报告顶部没有声明才算正常出图。
- 零长构件（降级模式和裁切后常见）必须在全链路防除零：覆盖率、重叠比这类
  除法一律取绝对值分母并兜底，一个 0 长度实例不该让两个内核崩掉。
- 泛化验收的门槛顺序：先证明"图框裁出来是全的"（图面线段数、梁链总长与图框面积比），
  再谈配准，最后才是量。顺序倒了会把图框问题误诊成算法问题。

### P49 单入口必须一次跑完证据层，缺输入的如实记 skipped（2026-09-14 加）

阶段脚本一条条手点，换一栋楼就要重排二十多次命令，还会漏跑某一层证据。
`cad_quantity_pipeline.sh` 现在在同一个入口里跑中心线支撑、墙身闭合、板厚分档、
统一扣减、预制实例展开，并把它们并入同一套报告：

- 每一步都先查输入：缺实测梁线 DXF、缺墙身面域几何、缺材料分账 JSON、缺展开 DXF
  时不猜不补，写 `{"name":..., "status":"skipped", "reason":...}` 进
  `manifest["skipped_steps"]`，报告里对应门槛直接不出现——少一步比假闭合安全。
- 可选输入一律走项目配置（`--profile`）：`centerline_geometry_dxf`、`wall_geometry_json`、
  `slab_notes_json`、`slab_panel_texts_json`、`slab_note_frame_bbox`、`deduction_verdict_json`、
  `deduction_sheet_json`、`prefab_material_ledger_json`、`prefab_expanded_dxf`。
- 只有本层自己能产出的输入才允许默认跑（结构模型、相交审计、板洞口审计），
  其余必须显式给路径，否则新楼第一次跑就会把外部参考口径当成 CAD 自证。
- 单入口的验收标准是"一条命令出一套 JSON/CSV/MD + manifest"，
  不是"脚本数量变少"；门槛计数与锁量必须与分步跑完全一致。

### P47 预制底板展开倍率必须拆到编号级，图面能自证面积自证不了块数（2026-09-14 加）

"展开倍率"以前直接取外部模型的块数除以图面块数，等于把别人的答案抄成自己的证据。
`cad_prefab_instance_expansion.sh` 流式扫展开 DXF（43 MB 不吃内存），按图名把轮廓与编号
归进图框，逐编号把图面块数/单块面积和模型块数/单块面积摆在一起，只定证据不动混凝土量。

- 倍率必须是编号级 `模型块数 ÷ 图面块数`，并满足恒等式
  `Σ(图面面积 × 该编号倍率) = 模型展开面积`；整册一个全局系数会把换位、漏画、
  重复建模混成一坨，残差永远解释不清。
- 单块面积是图面能自证的那一半：图面轮廓面积与模型单块面积在容差内相等，
  说明面积单元可信；不一致时先找"一正一负且合计对平"的换位数（判
  `code-outline-swapped-pair`），编号与轮廓互换了总量不变，不得当成漏量补面积。
- 谈"图面只画半幅"之前先做镜像审计：在图面 x 跨度内扫镜像轴，统计配对率与同面积配对数。
  全部轮廓都能在同 y 找到等面积镜像伙伴，说明图面已含双侧，倍率不能用镜像解释；
  只有大面积配不上对才允许用镜像补齐块数。
- `(W)` 后缀是另一个图框（屋面层）的编号族，不是同层镜像系列；图框归属按图名 y 序带
  （图名在图框下方、不得越过上一个图名），邻域窗口统计只能当线索、不能当块数。
- 一处编号只认领一块轮廓：包含优先、多块包含取最小块，否则 1500 mm 内就近认领；
  无编号认领的轮廓不进编号块数，单独计数，避免把引线框、填充框当板。
- 块数缺口只影响装配式采购台账：现浇报量不含预制子层，输出必须显式写
  `prefab_cast_in_place_impact_m3 = 0.0`，不得为凑块数去改混凝土量。
- 并入统一报告时对旧 `prefab-instance-expansion-anchor` 做原位替换（列表按索引展平比较，
  挪位置会造出假漂移），只追加两条新判定；`direct_outputs` 要落图面块数、模型块数、
  重构面积、残差、倍率、换位对数、镜像配对率和块数差。
- 统一报告里新增局部变量不得与外层同名：本步第一版把构件分档的 `blockers` 复用到
  component_gaps 分支，`closure_dashboard.blocking_count` 从 38 静默变成 3，
  是逐项回归的"量值漂移"抓到的，不是人眼；回归基线就是防这个的。

### P46 洞口与构件相交必须并成一套归属规则，同一空间只能扣一次（2026-09-14 加）

相交审计回答"这一格归谁"，洞口审计回答"这块面积扣不扣板"。两本账各跑各的会出两类错：
同一段对角线既挂复核洞口又挂已扣洞口；洞口格与节点格在平面里压在一起，板扣一次梁再扣一次。
`cad_deduction_ledger.sh` 把两边并进同一张台账，只定归属与对平，不改任何构件原值。

- 节点格体积按面积比例分摊已扣量时，最后一格必须吃掉舍入残差，
  否则"逐格合计 = 审计已扣量"永远差千分级，门槛会被自己的舍入卡住。
- 开洞图线必须先过看图结论再定档：`opening`/`not-opening` 两类结论带句柄入台账；
  图线自证解释（引线、紧邻已确认洞口、图框外）单独归一档，不得混进"未判定"，
  否则待复核组数永远降不下来，复核清单变成噪声。
- 报量表里已存在的洞口扣减行必须与本台账"看图确认"体积对平（残差为 0 才 pass）；
  同一笔扣减只能在一张表出现一次，两边各扣一次不会被任何单本账发现。
- CAD 自证但尚未进报量表的洞口不得静默入账：先确认参考模型的板是否已按同一洞口开洞，
  未核对前挂账不扣，并给出它占分账剩余量的比例。
- 跨账重叠用 bbox 求交：一旦有重叠就 fail，列出洞口行、节点格行、重叠面积与潜在重复扣减体积。
- 门槛并入统一报告时对既有 `slab-opening-evidence`、`member-intersection-deduction`
  两行做原位替换（列表按索引展平比较，挪位置会造出假漂移），只追加新判定行。
- 台账结论要进 `direct_outputs`（节点格数、已扣量、未定归属量、看图确认量、
  CAD 自证未入账量、报量残差、跨账重复扣量），否则待确认清单看不见归属结论。
- 清单里“待复核洞口整块上限”这类粗风险量，一旦被逐组定性的台账取代就必须摘掉，
  换成台账口径的真实待入账量；两者并存会把同一段图线报两遍、清单总量虚高一个整块上限。

### P45 板厚三档证据逐格拆分，"直接标注"必须按归属复核（2026-09-14 加）

面板整块取一个厚度会与图例冲突：一块板里可以同时压着两档填充。
`cad_slab_thickness_partition.sh` 用 100 mm 网格把每块面板切成子面域，按
"直接标注 > 图例填充 > 说明默认"三档定厚，分档面积必须等于面板面积。

- 图例句只认带"填充部分"的句子，其厚度由填充区域承载；整板默认档只认
  "未标注的板厚为 XXmm"这类说明句。两类句子混成一档，填充区就被默认值吃掉。
- 降板类填充只进浇筑标高控制分区，面积单列、体积影响必须为 0（P41 的具体执行）。
- **上游模型给的 `thickness_source` 不是证据。** 早先按"面板附近找得到含该厚度的文字"
  复核，一处标注能同时给十几块面板当"直接标注"，报出来的标注面积远大于图面实际标注数。
  改成按归属复核：每处板厚文字只归一块面板——落在谁的面域内算谁的（一块面板被多块包含时
  取最小那块），谁都不包含时才给半径内最近的一块；查无归属文字的标注档一律降级为说明默认档。
- 数字匹配要排除钢筋间距和尺寸标注：`@130` 是间距不是板厚，尺寸标注层上的数字是轴距；
  只采信写在板厚图层或写明"板厚/h="的文字。
- 降级只改证据口径；厚度值恰好与默认档相同时体积不变，一旦降级引起体积变化，
  必须在门槛里写明变化量，不能只报"证据已闭合"。
- 没有传入板图文字台账时判 `no-text-ledger` 并把归属门槛降为 warn，
  禁止把"没核对"写成"已验证"。
- 并入统一报告：`slab-thickness-evidence` 门槛由分档结果原位替换，另加
  `slab-label-claim-ownership`；分档体积只进 CAD 独立板量，报量仍走材料分账口径，
  两本账不得相加。标注优先与图例优先的摆动必须并列报出。

### P44 材料分账必须落到报量行，整厚含子层时不能只改标签（2026-09-14 加）

叠合板"整厚"口径里含预制底板子层，报现浇混凝土量时只能取补浇部分。
台账早先只加了"现浇叠合层口径"这类标签、行值仍填整厚，结果现浇量把工厂供的预制板也算了一遍。
标签对不上数值不会被任何门槛拦住，因为分账恒等式两边都用了同一个整厚值。

- 内核 `cad_concrete_grade.sh` 增加 `--material-split-json`：读现浇/预制材料分账结果，
  把 `member_group` 为 `composite-whole` 的行拆成 `cast_in_place_volume_m3`（进分级）与
  `prefab_sublayer_volume_m3`（退回装配式采购台账），整厚原值保留在行里作审计。
- 三重恒等式一起判，任一不平等即 fail：整厚 = 补浇层 + 预制子层；
  现浇板 + 板缝 + 补浇层 = 现浇口径；Σ分级 = 分账基准（基准含整厚时同步减掉预制子层，
  并把 `identity_baseline_source` 标成减层来源，不静默改基准）。
- 拆出来的子层与规则行里原有的子层剔除是同一笔体积，`excluded_sublayer_m3` 与
  `prefab_sublayer_split_excluded_m3` 分开记，不得相加成一个"剔除总量"。
- 拆分份额超过该行体积时按上限取，避免把别的构件量吃掉。
- 统一报告里 `prefab-sublayer-double-count` 门槛改为由分标号台账的拆分结果原位替换判定：
  没有 `--material-split-json` 输入时报 fail，并直接写明"仍按整厚全额计入、会重复计预制体积"。
- 独立佐证口径：报量改完必须拿现场实报量（各层混凝土计划单）与层高比复核方向。
  去重前首层/标准层比明显高于层高比，去重后落到层高比附近，说明方向正确；
  比值仍高出的部分只能由底部加强区截面增大等构造解释，不得反过来用实报量凑数。
- 给使用者的选项措辞要精确：说"已剔除"之前必须确认表里那一行的**数值**已剔除，
  不能只看行标签或只看台账结论。

### P43 墙端边缘构件逐格解释与特殊构件归属定档（2026-09-14 加）

墙身面域按墙双层线闭合重建时，墙线画到边缘构件内边就断，于是边缘构件外凸那部分
永远落在重建面域之外。这块面积既不能当"墙身重复扣除"，也不能顺手并进来当独立构件体积，
必须逐格给出归属。`cad_wall_edge_closeout.py` 做这件事，同时给特殊构件定归属。

- 面积恒等式：`outside_total = attached + unattributed`，残差必须为 0；
  重算值还要与历史台账登记值对平，对不平先查格分解，不得改阈值。
- 归属判定按"面域外格到最近墙类面域边线的距离"：距离在贴墙容差内记 `wall-end-attached`
  （墙线止于边缘构件内边、与墙身互补），超出记 `wall-end-unattributed` 并输出格的坐标、面积与距离，
  只有后者继续阻塞墙身空间闭合门槛。
- 重复计量防护：边缘构件与墙身重叠的面积已计入墙身面域，竖向档不得再按边缘构件单列体积行；
  收口产物把重叠面积与外凸面积同时给出，供审计两本账。
- 特殊构件先证归属再谈独立量：读参考量分表，逐编号回查其体积是否已在同构件类别合计内，
  并用"类别合计 = 逐编号求和"恒等式自证；已含者定档为
  `counted-in-reference-beam-bucket-not-additive`、`additive_volume_m3 = 0`，
  CAD 侧只登记图面轨迹句柄与轴长覆盖率，不再加量。参考量未含时才允许走独立 CAD 量。
- 门槛就地替换不改顺序：回归比对按列表索引展平，替换既有门槛必须原位替换、新门槛追加在尾部，
  否则会产生整段 `next_actions` 位移的假漂移。
- 用法：

```bash
scripts/cad_wall_edge_closeout.sh --phase18-geometry 墙身几何模型.json \
  --ledger-json 特殊构件与边缘构件台账.json \
  --reference-csv 参考工程量.csv -o 输出前缀
```

`--attach-tolerance-mm` 贴墙容差（默认 250，实测外凸格离墙边都在半墙厚以内）、
`--closure-tolerance-m2` 未解释面积阈值。

### P42 实例中心线必须有图面成对梁线支撑（2026-09-13 加）

按轴线推定的构件实例可能落在轴网上：中心线处图面根本没有成对梁线，长度和截面都是推定的。
这种实例一旦当缺量依据，就会把"参考比 CAD 多"当成漏量去补，方向整个反掉。
`cad_beam_centerline_support.py` 把这件事从人工判读升级为内核校验。

- 状态分五档：`centerline-verified`（成对梁线覆盖达标）、`centerline-partial`（部分覆盖，留在台账但转长度闭合）、
  `centerline-length-unsupported`（该轴有实测线对、本实例区间没覆盖，长度不可信）、
  `centerline-single-line`（只实测到单边线，梁宽无法定）、
  `centerline-axis-phantom`（该轴图面无成对梁线，幻影）。后三档 `ledger_excluded` 为真，既不扣也不加，先退出分标号台账。
- 双口径分开统计：算量实例由实测线对生成，模型实例由轴线推定生成，两者支撑率差距极大；
  报量口径固定用前者，后者只作复核证据，不得直接用来对缺量。
- 无支撑实例输出 `nearest_pair_axis_mm` 与 `axis_correction_mm`，把"中心线该平移多少"变成可回图证据；只登记，不自动改编号。
- 配对判定：两条同朝向梁线间距落在梁宽容差内、轴向重叠达标，取线对中点与实例轴线偏差在容差内才算支撑；
  单边线用更紧的横向容差，防止把邻梁边线当本梁证据。
- 与人工判读交叉核对写成 `overlap_cross_check` 与门槛 `centerline-support-cross-check`：
  分类不一致时回图核看重叠区间本身，不得调容差凑一致。
- 统一报告以 `--supplement-json "中心线支撑=..."` 入账，新增三个门槛与一条构件缺口；
  证据类并入按逐项回归：量值零漂移、缺键为零，门槛计数按预期变化后另锁新基线。
- 用法：

```bash
scripts/cad_beam_centerline_support.sh --model-json 结构模型.json \
  --geometry-dxf 楼层梁几何.dxf --overlap-verdict-json 重叠轴线实测核验.json \
  -o 输出前缀
```

容差：`--axis-slack-mm`（线对中点可偏离轴线多少）、`--face-tolerance-mm`（单边线横向容差）、
`--width-tolerance-mm`（线间距对梁宽容差）、`--verified-ratio`、`--partial-ratio`。

### P41 标高类属性不得换算成方量（2026-09-13 加）

填充图例区被当成"未入账的板厚差"，用面积乘高差报出一段方量敏感带，
实际图例写的是板顶标高比楼层标高低一个定值，板厚不变、混凝土方量不变。
结构模型里 `elevation_drop_mm` 与 `hatch_evidence[].source_text` 早已把图例原文入账，
报"读不出来"之前必须先查这两处。

- 分工固定：标高类属性（降板、升板、加腋、找坡）只进浇筑标高控制分区，不进混凝土分账；
  厚度类属性（图例给板厚档、直接标注板厚）才进分标号台账。
- 判"图面无解、需设计核定单"的前置条件是图例证据链为空；
  已有 `legend-confirmed` 的项不得推回人工确认清单。
- 比对参考量前先定清单口径边界：把范围外构件（楼梯、二次结构、建筑零星）先剔除，
  落在范围外的那部分量要归位到对应台账，不得当成"本层比参考少算"去补几何。
- 新增扣减行时不改被扣构件的原值，单列一行负值，便于回查与冲销；
  同一笔扣减禁止既改构件行又加扣减行（会重复扣）。

### P40 洞口可扣量的归属口径（2026-09-13 加）

待复核图线的"可扣体积"原先按包络矩形面积乘厚度、并对同一包络压到的每块板逐块累加，
于是一条斜穿的剖断线被当成一个大洞，上限虚高到数倍于当前量差，
按项目规则只能判为口径错误、不得用来闭合差额。

- 内核新增 `potential_volume_attributed_m3`（逐条）与 `review_volume_attributed_m3`（汇总），
  只认匹配到的那块板：取包络面积与板面面积的较小值乘该板厚度。
- 原 `potential_volume_upper_bound_m3` / `review_volume_upper_bound_m3` 保留不动，
  语义降级为"跨板重叠累加的保守上限"，两个口径同时给出，避免静默改历史量。
- 一致性判定 `gap_consistency` 一并输出归属口径，回图判读时以归属口径为准、
  以上限口径作风险带。
- 新增键属纯增量：统一报告逐键回归比对，量值零漂移、缺键零、新增键零；
  单测 `test_attributed_deduction_uses_matched_panel_not_overlap_sum` 锁住
  "归属口径必须不大于重叠累加上限、且等于匹配板面的自身贡献"。
- 判"某条图线不是洞口"要回展开图核对同处文字与同图层其它实体
  （楼梯另详类文字、降板填充闭合面域、板厚文字），单看包络尺寸会误判。

### P39 口径决定入账（2026-09-13 加）

清单里绝大多数条目不是"看图"问题，而是口径问题：板厚采信谁、板缝算几次、
预制底板进不进现浇计划、梁按中心线还是净跨、未定档残差归哪级、待认定洞口扣不扣。
这类决定由使用者拍板，但必须入账，不能只留在对话里。

- 做法固定五步：确认单（每题推荐值＋依据＋影响量）→ 决定记录
  （谁确认、何时确认、采纳了什么、还开着什么）→ 规则行改写 → 分标号台账重跑 → 前后对照。
- 入账口径：归级变化用 `source_type=user-rule`，`source_ref` 追加决定编号与一句话结论，
  让每一方量能回查到"被哪条决定影响"。
- 硬约束：分标号合计、恒等式残差、构件体积必须零变化，只允许等级归属、
  需复核量和门槛状态变化；出现体积变化即视为改动了算量，先回退再查因。
- 决定只解决口径，不解决几何：缺实例、缺几何、待认定洞口仍挂在门槛与不确定带里，
  `formal_ready` 不因口径确认而变真。
- 报量表要同时写"不进本表的部分"（预制子层等）和"不确定带"（缺量、摆动、扣减上限），
  让报出去的数字自带口径边界。

### P38 项目配置化（2026-09-13 加）

以前换一层就得重抄一长串命令行参数，参数抄错等于算错一层。现在 `--profile` 读一个
项目配置 JSON（schema `cad-project-profile/v0.1`），键名与命令行 dest 同名：
图名三件套（梁图、墙柱图、板图）、图框 sheet 号、竖向净高与标高、默认板厚、
混凝土等级、楼层映射说明与来源、等级规则 JSON、展开 DXF 路径、
以及 `grade_regions`（等级表在图面上的区域框，供提取内核用）。

- 取值优先级：命令行显式值 > 项目配置 > 内置默认。实现方式是解析完命令行后，
  只对"仍等于 argparse 默认值"的参数用配置补齐，所以不会出现配置悄悄盖掉手工参数。
- `--floor-label` 从必填改成可由配置提供；两者都没给时直接报错，
  绝不拿图名猜楼层（图名不等于楼层名是本项目的硬规则）。
- `schema`/`notes`/`grade_regions` 属元信息，不进参数表；`grade_regions`
  留给 `cad_grade_source.sh` 使用，避免同一份表区 bbox 抄两处。
- manifest 新增 `inputs.profile` 与 `inputs.profile_applied_keys`，
  报告能看出这轮用了哪套配置、哪些键是配置给的。
- 配置文件本身含项目图名与坐标，属公司内部数据，只放项目目录，不进技能发布包。

### P37 共用助手合并（2026-09-13 加）

`_number`/`_text`/`_round` 原先在 14 个内核里各抄一份（`_number` 12 份、`_text` 10 份、
`_round` 16 份），改一处口径要改十几处。现在统一走 `scripts/cad_common.py`：

- `to_number(value, default=0.0)`：脏数据返回默认值，不抛异常。
- `to_text(value)`：只把 None 当空串，**不剥空格**——图面原文（如"层 号"）剥空格会改变匹配结果。
- `to_label(value)`：剥首尾空格，只用于表格行标签和图名。
- `round_number(value, digits=4)`：台账列默认四位，脏数据当 0。
- 迁移方式是逐字节比对：只有函数体与共享实现完全一致的内核才替换成
  `from cad_common import to_number as _number, ...`，调用点一字不改；
  变体（返回 None 的清洗、`float(value or 0.0)`、集合拼接的 `_text`）保持原样不并。
  唯一语义收窄：脏数据原本会抛异常的角落现在返回 0.0。
- 几何助手（bbox、距离、面域）各内核算法口径不同，不合并。
- 验证：单测 203 -> 208（新增语义锁定 5 例）；真图重跑统一报告对 P35 基线
  10734 键零漂移，等级表提取、规则草稿、分标号台账、待确认清单四个产物按
  P35 校验清单 `shasum -c` 全部 OK（字节级不变）。

### P36 门槛可核对化与待确认清单（2026-09-13 加）

两件事：把循环定义的门槛改成能核对的量，把散在各处的未闭合项合成一张现场能用的表。

- `special-member-closeout` 原先写 `status = not formal_ready`、evidence 取台账里不存在的
  `status` 字段，等于"因为没闭合所以没闭合"。现在由
  `cad_quantity_report._special_member_closeout_gate()` 统计：独立 CAD 算量未定档的特殊构件
  清单（状态含 `not-independent`、`reference-only`、`partially`、`candidate` 即未定档），
  加上边缘构件面域外面积、复核阈值与完全在面域外的根数；三项全过才 pass。
  台账自带 gates 时仍以台账为准，不覆盖证据脚本的判定。
- 新内核 `cad_review_checklist.py`（`cad_review_checklist.sh`，schema
  `cad-review-checklist/v0.1`）读统一报告 JSON，合并六类来源：已算出的未闭合量
  （板缝重叠、板厚摆动、洞口扣减上限、预制覆盖缺口、缺实例体积、未定档等级量）、
  梁逐根状态、板逐块厚度与洞口、特殊构件与边缘构件、异常记录、未过门槛。
  去重按"类别+构件"合并，每行必带一个具体确认动作；
  重复计量风险与参考口径选择不计入合计（`non_additive_m3` 单列），避免和缺口相加。
  判定用词先认未闭合词再认闭合词，防止 `not-independent` 被 `independent-cad` 误判成已闭合。
- 门槛语义变化只做证据侧：统一报告量值键逐项对账零漂移，基线随之重锁。

### P35 合并格分档定界与自动规则对照（2026-09-13 加）

P34 提取出来的逐层等级当时全部挂"需复核"，理由是数值靠距离继承。
本轮把"能不能定"讲清楚，做法是 `interval_boundaries_confirmed()`：

- 整列只有一个等级值时没有边界可猜，所有行都算确定（水平构件列常属这种）。
- 相邻两个不同等级值的中点就是合并格的分档线；表格分档线必须是行线，
  所以中点落在相邻两行之间时，逐层归属被表结构唯一确定。
- 中点正好压在某一行的行线上（重合判定按 1 mm 容差），或落在行范围之外（说明表结构对不上），
  那一行归属不定，保持需复核。
- 三张门槛改成：表头定位、合并格已定界或挂复核（未定界又没挂复核直接 fail）、
  行标签覆盖；行标签与逐行等级按内核产物取用，项目脚本不再自己算第二遍。

项目侧对照（`--components-json` 之外另跑的人工规则比对）要求：
分标号合计、各档体积、恒等式残差、剔除子层与节点区量必须零变化，
只允许需复核量下降和门槛状态变化；等级值与人工规则不一致时记冲突交人裁决，
内核不得改写定档。定界成立后摘掉的是"来源不可追溯"，不是构件几何缺口，
`formal_ready` 仍按全部门槛走。

### P34 图面等级表自动提取（2026-09-13 加）

分标号规则原先是我照图转写的，等级来源那一档说不清"哪句文字证的"。
新内核 `scripts/cad_concrete_grade_source.py`（`cad_grade_source.sh`，
schema `cad-concrete-grade-source/v0.1`）把这件事变成可回放的提取。

- 表格模型：先两遍扫。第一遍找表头行（有列头关键词且整行没有等级值；
  楼层标高表常把表头画在数据下方，所以不能假设表头在最上面），
  从表头行取列带：含墙/柱/连梁的列归竖向，含梁/板/楼梯的列归水平，
  含"混凝土/强度"的列归材料列，最左一列当行标签列。
  第二遍把数据行里的等级格按 x 落到最近列带，再按 y 就近归属到每个行标签。
- 合并单元格：等级文字画在格的中间，它会自成一行"锚点行"（没有行标签）。
  锚点行不出绑定行，只当证据源；靠距离继承的行标 `inherited` 并给
  `band_gap_mm`，同时 `needs_review`，不当图面直接证据。
  等级格正好落在某行高度时算直取，`needs_review` 为假。
- 材料表不继承：一行一个部位，部位格为空或写"详某表"就没有等级值，
  不跨行猜；部位文字含"梁板楼梯"归水平构件，含圈梁/构造柱/过梁归二次结构，
  含筏板/基础/垫层归基础。耐久性表的"最低强度等级"不是工程用标号，
  提取时靠"只认表格列带内的等级格"这条挡住。
- 大图画法：`--dxf` 走 ezdxf（几十 MB 会吃内存），或先流式抽出表格区域文字，
  用 `--records-json` 喂内核；区域用 `--region name=,x0=,y0=,x1=,y1=,role=`
  或 `--region-file`。给 `--components-json` 时另出 `<输出>-rules.json`
  （`cad-concrete-grade-rules/v0.1` 草稿），可直接接 `cad_concrete_grade.sh`。
- 真图验证（首层那两张结构图）：层高表表头识别成功，逐层竖向等级自下而上分档，
  首层落在最高档、往上递减两档，水平构件全行同一档；材料表抽出筏板与梁板楼梯两档，
  竖向部位写"详主楼层高表"故不绑。逐层结果与人工转写的规则一致，
  本轮不动分账基线，量值零漂移（统一报告逐键对账通过）。

### P33 分标号入单入口流水线 + 发布脱敏守护（2026-09-13 加）

三件事：分标号步骤内联、恒等式基准可自动取、发布前必过的脱敏守护。

- **分标号内联**：`cad_quantity_pipeline.sh` 新增 `--grade-rules-json`（等级规则 JSON）
  与 `--no-grade-ledger`。给规则时流水线内直接调 `cad_concrete_grade.py`，
  产物 `concrete_grade_ledger.{json,csv,md,sha256}` 进 manifest 的
  `concrete_grade_ledger_json`，同时以 `分标号=` 补充项并入统一报告，
  合计与占比写进 `metrics.grade_ledger`；不给规则该步 `skipped`，其余步骤零变化。
  这条是"一条命令跑到分标号报量"的收口，用户不再需要手工串两级脚本。
- **恒等式基准来源**：优先级 `--expected-total-m3` > 规则文件 `expected_total_m3`
  > 分账报告里的 `concrete_candidate_total_m3`/`candidate_total_volume_m3` > 自身合计，
  结果记在 `summary.identity_baseline_source`。原实现在三处都取不到时会把基准落成负一，
  残差直接失真，现按自身合计处理并显式标 `self`。规则文件没写楼层时从分账报告回填
  `floor`/`floor_label`，避免台账楼层空白。
- **发布脱敏守护**：cad-file-reader 的 `cad_release_scrub.py`（迁移前入口为 `python3 scripts/cad_release_scrub.py .`）
  扫 `.md/.txt/.sh/.json/.toml`，跳过 `vendor`、`tests` 等目录，判五类敏感：
  带小数的工程量、标高数值、`/Volumes` 与家目录文档路径、十六进制摘要串、
  阶段产物文件名。命中即 exit 1，`--apply` 就地打码且幂等。
  语义版本号（如解析库版本）和耗时/内存标记（毫秒、秒、MB、百分比）先摘除再判，
  避免把方法说明当实测结果。技能包内只留方法描述，真实数值留在项目 `outputs/`
  与脱敏前备份目录，不进发布包。`.sh` 入口一律不写死家目录，按
  `$CAD_PYTHON` → PATH `python3` → `$HOME/.cache/codex-runtimes/*/dependencies/python/bin/python3` 找解释器。
- **回归自锁**：`cad_quantity_regression.py`（`.sh`）把新报告与锁定基线逐键对账。
  做法是把报告 JSON 扁平化成点号键路径（含数组下标），只比标量叶节点：
  默认忽略标题与时间戳，数值按 `--tolerance` 比较，其余必须全等；
  出现量值漂移或基线键消失即 exit 1。`--quantities-only` 只审 `_m3`、`_m2`、
  `volume`、`area`、`total`、`count`、`ratio` 类键，`--update-baseline` 用于口径
  确实变更后重锁。项目侧在报告脚本末尾自动跑一次，基线文件放项目 `outputs/`，
  含公司工程量，不进技能发布包。
- **回归**：统一报告除标题外逐键零漂移（首层一轮 10734 键全等，合计、门槛计数、
  `direct_outputs` 键数不变）；单测 164 -> 181，新增流水线分标号步骤 4 例、
  基准来源 4 例、脱敏守护 3 例、回归比对 6 例。

### P32 梁柱节点区按柱等级浇筑（2026-09-13 加）

使用者确认的施工做法：梁柱接头处柱混凝土要浇到梁端 500 mm。
分标号报量必须把这部分体积从梁档移到竖向构件档，脚本
`work/phase32_joint_zone_transfer.py`，产物
`outputs/<项目阶段产物>` 与
`outputs/<项目阶段产物>`。

- 计算式：逐根 `支座数 × 0.5 m × 梁宽 × 梁高`，44 根已定位梁合计 **〈实测〉 m3**；
  支座数分布 2 个 36 根、3 个 6 根、4 个 2 根，截面全部解出，逐根带 X-Y 可回图。
- 口径：清单计量里节点核心区已含在柱内（柱按层高全高），所以这里是**等级归属换算**，
  不是加量；分标号合计仍 〈实测〉 m3，恒等式残差 〈实测〉。
- 等级来源新增一档 `user-rule`（经使用者确认的施工做法）：按可采信处理，
  不计入"未定/推定"，但也不冒充图面直接计量证据；来源链展示为
  `design-booklet-table, user-rule`。
- 首层分标号定档结果：C30 `〈实测〉` m3、C40 `〈实测〉` m3（含节点区 〈实测〉）、
  未定 `〈实测〉` m3，剔除预制子层 `〈实测〉` m3。
- 统一报告 v0.20 -> v0.21：新增 `grade_joint_zone_m3`，`grade_volume_C30/C40_m3`
  随换算更新（这三项是本轮新引入的分标号键，不属于锁定基线）；
  `concrete_candidate_total_m3=〈实测〉`、`concrete_reference_total_m3=〈实测〉` 等
  锁定量值零漂移，23 项门槛 4 fail / 13 warn / 6 pass，重跑幂等。

### P31 混凝土分标号台账（2026-09-13 加）

物资计划必须按强度等级分开报，所以等级绑定要能机器出账，不能停在"图上写着 C30"。
新内核 `scripts/cad_concrete_grade.py`（`cad_concrete_grade.sh`），
规则输入 `--rules-json`（<项目阶段产物>）+ 分账校核 `--ledger-report-json`，
产物 `outputs/<项目阶段产物>`，
schema `cad-concrete-grade-rules/v0.1` 与 `cad-concrete-grade-ledger/v0.1`。

- 图面等级来源有三处，必须分清：
  ①结构设计总说明 **表5.1 主要结构材料表**（构件部位/钢筋级别/混凝土强度/备注）——
    主楼梁板楼梯 C30、主楼筏板基础 C30、地下车库柱墙梁顶板 C30、
    圈梁构造柱过梁 C25、**主楼柱墙写作"详主楼层高表"**；
  ②设计专篇 **结构楼层标高表** 的「墙、柱、连梁」列与「梁、板」列——
    墙柱连梁列出现 C40/C35/C30 三个合并单元格（自下而上递减），梁板列 C30；
  ③构件级说明——预制墙板 YNQ-01/02/03 为 C35/C30（第四层 C35，其余 C30），
    筏板 C30/P6、垫层 C15 素混凝土、后浇带高一级膨胀混凝土。
  耐久性表里的"最低强度等级 C20/C25/C30"是耐久要求，**不是工程用标号，禁止当等级取用**。
- 首层结果（去重口径 〈实测〉 m3，恒等式残差 〈实测〉）：

  | 等级 | 体积 m3 | 来源 |
  |---|---:|---|
  | C30 | 〈实测〉 | 图面表格（主梁 〈实测〉 + 楼梯梁 〈实测〉 + 现浇板 〈标高〉 + 叠合整厚 〈实测〉 + 板缝 〈实测〉） |
  | C40 | 〈实测〉 | 层高表合并单元格推定（竖向 〈实测〉 + 连梁 〈实测〉），需回图逐层确认 |
  | 未定 | 〈实测〉 | 梁未分解残差 |
  | 剔除 | 〈实测〉 | 预制底板子层，不得与整厚相加，也不得计入分级合计 |

- 内核三条硬规矩：Σ分级必须等于分账基准（残差不为 0 直接 fail）；
  预制子层必须走 `treatment=excluded-sublayer`；等级来源分 6 级
  （`member-label` > `drawing-table` > `design-booklet-table` > `drawing-note` > `inferred` > `unknown`），
  推定与未定单独计数并计入 `needs_review_m3`，占比过半即门槛 fail。
- 统一报告 v0.19 -> v0.20：新增 10 键（`grade_volume_C30_m3`、`grade_ledger_total_m3`、
  `grade_ledger_identity_residual_m3`、`grade_ledger_needs_review_ratio` 等）和 3 个门槛
  （恒等式 pass、来源证据 fail、子层剔除 pass）；23 项门槛 4 fail / 13 warn / 6 pass；
  既有量值逐项回归零漂移，`direct_outputs` 203 -> 213 键。

### P30 装配式计算书设计锚点与图纸版本自证（2026-09-13 加）

板差只有两种解释：模型版本早于图纸，或 CAD 提取覆盖不全。先用同一册设计文件做第三方判定，
脚本 `work/phase30_prefab_booklet_design_anchor.py`（自带 DWG→DXF 转换与缓存），
产物 `outputs/<项目阶段产物>`。

- 版本自证：`某栋楼+结构+20230807(改装配式）.dwg` 与 2024-09 微信接收副本 md5 全等
  （`〈摘要已隐去〉`），图纸侧只有一个版本。广联达指标报表的
  编制日期 2023-07-11 是招投标阶段属性字段，导出包时间戳是 2024-03-31，
  两者都不能单独当版本证据。
- 计算书给出每层设计指标：水平构件 〈实测〉 m2/层、预制叠合板 〈实测〉 m2/层（〈实测〉%）、
  竖向构件 〈实测〉 m3/层（〈实测〉 m2×2.9 m）、机房层 〈实测〉 m3、1~24 层竖向合计 2188 m3、
  叠合板厚 130 mm（130 档占 95%）、梁宽与墙厚 200 mm、接缝 350 mm、装配率 P=51%、
  预制墙板只从 〈标高〉 m 起（首层竖向全现浇）。
- 引用前必须先过算术自证：9 条恒等式全中（〈实测〉×24+〈实测〉=2188、
  〈实测〉×(V−V1a1)=V1a2、A1a×24=〈实测〉、A2c合计/Aw3合计=〈实测〉% 等）。
  表内另有 3 处合计格前缀写错（A1a/A1c/A1d 的合计写成 A1b）和机房层两值不一致，
  只记为图纸内部口径提示。
- 三方对表：CAD 板面域 〈实测〉 m2 对设计 〈实测〉 m2 只差 −〈实测〉%，板总量首次拿到
  不依赖广联达的锚点。预制面积必须分三种口径记：图面闭合轮廓 〈实测〉 m2（42 块）、
  按编号展开 〈实测〉 m2（78 块）、设计书 〈实测〉 m2/层。设计值对图面轮廓的倍率是
  〈实测〉，对广联达模型块数的倍率是 〈实测〉，两者只差 7.3% —— 这独立证明了
  “图面按编号代表块绘制、一块轮廓代表约两块板”，所以 42 对 78 不是版本差也不是漏画。
- 残留口径差：展开后仍比设计书少 〈实测〉 m2/层，折整厚 130 mm 只有 〈实测〉 m3，
  属设计书与施工图/模型的计量差，进复核清单，不影响候选总量。
- 实例倍率目前的来源是广联达模型块数，属非独立证据；邻域复核线索：
  布置图附近 `S-PC-叠合板轮廓` 62 条 / 〈实测〉 m2、`S-PC-编号` 82 条、
  其中 (W) 镜像系列 26 条、无配对编号 20 条（窗口含相邻图框，只作线索）。
- 统一报告 v0.18 -> v0.19：新增 24 个直接数据键（`design_*`、`cad_prefab_outline_area_m2`、
  `cad_prefab_expanded_area_m2`、`prefab_expansion_multiplier_design/glodon`、
  `prefab_area_gap_vs_design_m2`、`prefab_frame_w_series_label_count`、
  `drawing_version_copies_identical` 等）和 4 个门槛：`drawing-model-version-consistency`
  pass、`slab-plate-area-independent-anchor` pass、`prefab-instance-expansion-anchor` warn、
  `prefab-booklet-arithmetic-selfcheck` pass；20 项门槛为 3 fail / 13 warn / 4 pass。
  `concrete_candidate_total_m3=〈实测〉` 等全部既有量值逐项回归不变，`direct_outputs` 179 -> 203 键。

### 图层化几何与单层初算/缺口报告（2026-09-10 P4 加）

读取结构图做真实构件几何前，建议让 cad-file-reader 的 `cad_scan` 同时保存几何图层，否则无法区分
“梁轴线、板边线、墙柱轮廓、钢筋标注线、尺寸线”：

```bash
# 在 cad-file-reader 技能目录执行（迁移后底座识图入口）
scripts/cad_scan.sh 图纸.dwg \
  --with-mtext --with-geom --with-geom-layer --cluster 1500 \
  --detail-json 图纸.detail.json --format json -o 图纸.scan
```

图层化详情会新增 `geometry_layers`，长度与 `geometry_segments` 一一对应；DWG 文字也会带图层。
该参数实测在 1# 结构图（约 6MB）增加约 1 秒和少量内存，`geometry_segments` 保持原有调用兼容。

然后运行单层初算/缺口报告：

```bash
scripts/cad_quantity.sh \
  --scan 图纸.scan.json --detail 图纸.detail.json \
  --floor 一层 --format all -o 一层混凝土初算报告
```

报告目前会自动做以下内容：

- 查找结构层高表图框，按“层号 + 结构标高 + 层高 + 混凝土等级”列位置解析为行；
  混凝土等级若在 CAD 中是跨多行合并单元格，会按相邻 Cxx 中点分摊并标 `[推测]`。
- 把图框名解析为梁平法/板结构/墙柱图纸，并判断覆盖楼层范围。
- 对选定楼层匹配梁平法图和板图，梁可继续输出当前粗算体积；梁混凝土等级可绑定层高表。
- 板图输出文字线索、图框内几何段、板轮廓图层段、闭合轮廓粗提示；
  在得到可信闭合边界和板厚前，不输出板方量。
- 墙柱图按标高范围列出，说明“按图自动单层拆分尚未建模”，不输出伪方量。
- Markdown/JSON/CSV 都会保留状态和缺口，避免把自动粗算误报成结算量。

当前边界：

- 梁方量仍是“图面线段合并 + 截面”的粗算，不扣支座、不识别原位多跨净跨。
- 板、墙、柱的量需要真实展开后的闭合轮廓和尺寸；若 DWG 把构件几何放在 INSERT/图块内，
  直接扫描只能得到标注层，必须先用 CAD 软件导平、把块展开或补几何层后再交给本脚本。
- 层高表解析依赖设计院表头文字和坐标列位置，不是所有图纸都一致；无法解析时报告会标
  `no-story-table`，不会硬套一个混凝土等级。

### 梁中心线对象复核（2026-09-10 P5 加）

在“图层化几何”和“目标图框块展开”之后，可以用梁边界图层生成可逐条复核的梁对象。
真实 某栋楼二层验证里，`S-梁-虚线` 是梁轮廓边界线，不是尺寸线；展开后可以先按边界间距
配对中心线，再把中心线长度绑定到集中标注位置。

```bash
# 1. 展开目标图框内图块的几何，写出 DXF/SVG（只处理一个图框，不做全图长时间解析）
scripts/cad_geometry.sh 图纸.dwg \
  --scan 图纸.scan.json --detail 图纸.detail.json \
  --floor-label "二层梁平法施工图" -o 二层几何

需要浏览器直接打开复核时加 `--format svg`，会输出同名的 `*.svg`；
不传时默认仍同时输出 DXF/JSON/MD，兼容原有工作流。

# 2. 梁边界层 → 中心线候选 → 梁对象 JSON/CSV/MD/DXF
scripts/cad_beam_objects.sh \
  --dxf 二层几何.dxf \
  --scan 图纸.scan.json --detail 图纸.detail.json \
  --floor-label "二层梁平法施工图" -o 二层梁中心线对象
```

脚本会输出：

- `centerline_width_counts`：本图梁边界配对宽度分布；若某设计院不是 200 宽梁边界，
  会从本图截面 b 值自动取宽度。
- 每条梁对象：编号、截面、梁高、长度、体积、中心线方向、标注坐标。
- `*.objects.dxf`：把自动中心线画出来，方便 CAD 里逐条对图复核。
- `volume_status=no-section/no-length`：缺截面或没匹配到中心线时保留缺口，不补假数。
- 默认同时输出 `*.runs.json` / `*.runs.csv` 全图中心线拓扑台账；主 `rows` 仍保持
  “一条标注对一个梁对象”的兼容口径，两个总额禁止混加。

当前边界：中心线长度是合并粗长，尚未自动扣柱/墙支座宽度、梁端节点和叠合板影响。
真实 某栋楼二层初测：44 条梁标注全部有截面和中心线，自动梁体积约 `〈实测〉 m3`；
此前广联达模型同层梁参考值约 `〈标高〉 m3`，两者差距约 `2.6%`，只能作为算法闭环自检，
不能直接替代广联达净跨模型。输出仍必须按“梁对象中心线粗算”口径解释。

### 多楼层对照与差距量化（2026-09-10 P5.1 加）

`cad_beam_objects` 单层接近不能外推。标准层图纸存在“无独立集中标注的重复梁跨”，
当前“一条标注对一段中心线”会漏掉大量梁段；屋面层梁轮廓还在 `S-梁-实线`，不是同一个图层。
因此新增模型对照工具，内测时先量化，再决定是否继续：

```bash
scripts/cad_beam_benchmark.sh \
  --model-summary 某栋楼各层混凝土方量汇总.csv \
  --auto-json 二层梁中心线对象.json 3_5f_beam_auto.json \
  -o 梁自动模型对照
```

某栋楼真实对照：二层 `-2.6%`；三层~五层 `-〈实测〉%`；六层~十层 `-〈实测〉%`；
十一层~十五层 `-〈实测〉%`；十六层~二十层 `-〈实测〉%`；二十一层~二十四层 `-〈实测〉%`；
屋面层当前因图层不同未能解析。没有通过全楼层对照前，不允许把 CAD 梁自动方量当交付量。

`cad_beam_objects.py` 还支持 `--support-dxf` 和 `--support-transform` 输出墙柱轮廓区间提示，
供支座净跨开发；该提示当前只能用于研发，不能直接算净跨。

梁中心线对象默认使用 `--run-mode axis-chain`。当归一化梁编号声明跨数大于 1 时，脚本会沿
同一轴线连接跨间短空隙，避免一条 `KL17(3)` 只绑定到其中一跨；可用
`--chain-gap-mm`、`--chain-max-perp-mm`、`--chain-max-annotation-mm` 控制连接边界。
该长度仍是中心线粗长，支座宽度由 `cad_structure_model` 再扣减。

### 梁编号级模型自检（2026-09-10 P5.2 加）

用本机广联达导出的 xlsx 做“对象级”而不是“总额级”对照，避免单层总额碰巧接近时误判能力。
该工具先按梁编号集合自动匹配 CAD 梁平法图最可能的模型层，再把每个编号的 CAD 自动方量
与模型方量列出缺口，并输出唯一编号、对象数和完整 JSON。

```bash
scripts/cad_model_code_compare.sh \
  --model-xlsx 广联达1#.xlsx \
  --auto-json 3_5f_beam_auto.json \
  -o 梁编号模型对照
```

已在本机 某栋楼真实工作簿验证：

- “二层梁平法施工图”按编号匹配广联达“首层”，不是直接按图名猜“第2层”；
- “三层~五层”等标准层按编号匹配“第2层~第23层”同编号组，主要缺口集中在 `TL2/TL3`
  楼梯梁与重复梁跨；
- “屋面层梁平法施工图”匹配广联达“第24层”编号集合，证明此前把该图直接对到“屋 面”总量
  是口径错误；
- 输出可以继续作为算法改进基线，不对外宣称已经达到广联达精度。

`cad_model_code_compare.sh` 现已兼容 `cad_structure_model` 输出，并可用
`--quantity-field clear_volume_m3` 直接核对净跨推定结果。传入
`--auto-total-field run_registry.quantities.estimated_volume_m3` 时，编号表会同时给出
拓扑归属方量；该字段仍是研发对账口径，不替代正式净算量。

```bash
scripts/cad_model_code_compare.sh \
  --model-xlsx 广联达1#.xlsx \
  --auto-json 结构模型.json \
  --quantity-field clear_volume_m3 \
  -o 梁净跨模型对照
```

### 全图中心线拓扑台账（2026-09-10 P5.3 加）

标准层梁平法图经常只在一处写编号，镜像单元里的相同梁段没有第二份集中标注。
`cad_beam_objects` 现在额外建立 `cad-beam-run-registry/v0.3`：先合并同轴短断口，
再按“标注直接命中、近邻标注传播、镜像轴传播、低置信默认截面”四级生成全图梁段。

```bash
scripts/cad_beam_objects.sh \
  --dxf 三层五层梁几何.dxf \
  --scan 图纸.scan.json --detail 图纸.detail.json \
  --floor-label "三层~五层梁平法施工图" \
  --run-registry --format all -o 梁对象-全图拓扑回归
```

关键字段：

- `run_registry.quantities.estimated_volume_m3`：全图拓扑中心线粗方量；
- `run_registry.mirror_axes`：由等长梁段投票出的镜像轴，每条传播结果带 `mirror_axis_mm`；
- `section_status=label-overlap/nearest-label/mirror-label/assumed-default-section`
  分别表示当前截面的证据等级；
- `run_registry.code_quantities` / `*.codes.csv`：把拓扑段归到梁编号，并单列竞争编号段；
- `run_registry.runs` 保留轴线、起终点、配对宽度、截面来源、编号来源、
  `competing_codes` 和匹配编号，便于回图复核；
- 镜像传播支持端部截断容差；通配次级配对与高置信候选中心距不超过 `450 mm`
  且重叠超过 80% 时按重复配对剔除。
- `*.leaders.csv` / `run_registry.leader_targets`：把集中标注引线的文字端和梁中心线端
  分开保存，直接用引线目标消解相邻编号串线；同一条引线只允许绑定一个实际文字位置，
  同一位置解析出多个编号时才记为 `leader-alias`；
- `leader-target` 作为高于文字簇锚点的编号来源；文字簇锚点只用于无可靠引线时的回退。
  通过 `--leader-layer-pattern`、`--leader-max-distance-mm`、
  `--leader-target-max-distance-mm`、`--annotation-cluster-mm` 控制绑定边界。

真实 某栋楼三层~五层回归：编号级粗算仍为 `〈实测〉 m3`；拓扑去重、端部截断镜像、
引线目标并补长已命中拓扑段后为 `〈实测〉 m3 / 211350 mm / 57` 段。`KL12`
由截断的 `〈实测〉` 修正为 `〈实测〉 m3`，`KL13` 为 `〈实测〉 m3`，`KL1` 为
`〈实测〉 m3`，与广联达 `〈实测〉 m3` 接近。当前拓扑方量对广联达 `〈实测〉 m3`
仍低约 `6.1%`；补长只作用于引线已经命中的拓扑段，不再把相邻同轴编号跨缺口合并。
该结果仍只能用于研发对账，不能作为翻样或结算量。

### 楼梯梁独立台账（2026-09-10 P6.1 加，P6.2 增加显式实例倍率）

`cad_stair_beam_registry.sh` 单独读取楼梯平面中的 `TL` 编号、文字位置和
`S-梁-*` 中心线，按“近距离优先、远距离用梁长先验”绑定候选，再合并同轴短断口。
输出 `cad-stair-beam-registry/v0.2`，不得把 `TL` 段加入主梁台账。

```bash
scripts/cad_stair_beam_registry.sh \
  --dxf 楼梯平面几何.dxf \
  --scan 图纸.scan.json --detail 图纸.detail.json \
  --bbox=-1206500,1195000,-1195000,1206000 \
  --codes TL2,TL3,TL4 --known-widths 200 \
  --instance-multiplier 2 \
  --multiplier-basis "同一楼梯平面按上下行两跑叠合绘制" \
  --section-json 楼梯梁截面.json \
  --format all -o 楼梯梁独立台账-标准层
```

关键边界：

- `TL2 260X16=4160` 中 `260X16` 是踏步宽×数量，不是梁截面，通用梁解析器不得把它当 `260x16 mm`；
- 楼梯大样一页常含首层、标准层、顶层等多个局部平面，必须按局部图框分别建账，不能把不同楼层同名 `TL` 合并；
- `--instance-multiplier` / `--member-multipliers TL2=2,TL3=2` 只用于表达图中叠合绘制的上下行梯梁或成对楼梯实例，
  并必须同时写 `--multiplier-basis`；不得用广联达方量反推倍率；
- 输出中的 `centerline_length_mm` 是图面唯一拓扑长度，`quantity_centerline_length_mm`
  才计入显式倍率；两者必须同时保留；
- `--merge-axis-offset-mm` 限制跨短断口的轴线偏移，默认 `5 mm`；同轴端点相接仍允许
  `--axis-tolerance-mm` 的较大聚类容差，但中间已有缺口的错位轴线不得借缺口合并；
- `--section-json` 的截面状态会原样写入台账；模型反算或人工输入只能用于研发对照，仍须图纸大样复核；
- `centerline_length_mm` 和 `gross_volume_m3` 是独立楼梯梁粗算，不扣支座/平台节点，也不与主梁方量相加。

### 结构模型与混凝土台账（2026-09-10 P6/P7/P8 加）

`cad_structure_model.sh` 把已有梁中心线对象、墙柱展开 DXF、板展开 DXF 组装成统一的
`cad-structure-model/v0.5` JSON，并输出 Markdown、CSV 和可回 CAD 复核的模型 DXF。
它不再把“同一图号的不同实例”混成一条，也不把梁中心线粗长冒充净跨。

```bash
scripts/cad_structure_model.sh \
  --beam-json 二层梁中心线对象.json \
  --beam-dxf 二层梁几何.dxf \
  --support-dxf 二层墙柱几何.dxf \
  --slab-dxf 二层板几何.dxf \
  --opening-dxf 二层板几何.dxf \
  --support-transform auto \
  --slab-transform auto \
  --assumed-end-support-width-mm 500 \
  --text-json 结构图.detail.json --component-sheet 34 --slab-sheet 36 \
  --slab-hatch-source 原图.dwg \
  --slab-hatch-rule "H1,H2=drop-30;H3=140;H4=120" \
  --slab-default-thickness-mm 130 \
  --floor-label "二层" --elevation-mm 2810 --story-height-mm 2900 \
  --concrete-grade C30 \
  --format all -o 二层结构模型
```

当前模型输出：

- 梁：中心线粗方量、逐跨净长、支座区间和
  `clear-span/clear-span-review/clear-span-inferred/support-gap/centerline-mismatch`
  状态；`clear-span-review` 表示净跨已形成但含端部构件或 T 形候选复核支座；
- 梁：若梁对象 JSON 带全图拓扑台账，同时保留 `topology_volume_m3` 和四级截面来源统计；
- 墙：平行边界配对出的中心线候选，按边缘构件/柱轮廓扣除重叠区间；
- 边缘构件：`S-剪力墙-边缘构件` 的简单开口链按缺口方向闭合，输出截面面积和候选体积；
- 边缘构件编号：实际 TEXT 最近轮廓为 `direct`，严格同形状镜像为
  `mirror-propagated`；截断轮廓在 `800 mm` 宽窗内只生成
  `mirror-propagated-review` 候选，并保留镜像伙伴、距离和复核原因；
- 柱：正交边界矩形和开口 `U` 形轮廓候选，分开列账；
- 板：保留闭合板环；同时用板边线、梁、墙和柱边界切分平面拓扑面，输出面数量、面积和
  可回图的多段线候选，并按 `h=130` 等文字、HATCH 规则和默认值分级绑定板厚；
- `*.model.dxf`：用不同图层标出梁、墙、柱、板、边缘构件待复核项和未闭合问题，
  同时写出构件编号及依据状态，供 CAD 逐条复核。
- `--*-transform auto`：按共同结构图层的等长线投票估计平移，再用目标梁图框覆盖长度
  和可形成的支座/净跨数量复核。v0.5 优先使用同名图层等长线形，再对匹配线段残差取中位数；
  不使用旋转和缩放，跨图旋转或不同比例的图纸需先统一坐标。

新增参数：

- `--edge-member-layers`：边缘构件图层，默认 `S-剪力墙-边缘构件$`；
- `--wall-width-tolerance-mm`：墙厚吸附到 `200/250 mm` 模板的容差，默认 `60`；
- `--slab-boundary-layers`：板面切分使用的梁、墙、柱和板边界图层；
- `--slab-panel-min-area-m2`：板拓扑面的最小面积，默认 `1.0`。
- `--edge-mirror-match-tolerance-mm`：严格镜像容差，默认 `25`；
- `--edge-mirror-review-tolerance-mm`：截断轮廓待复核镜像容差，默认 `800`；`0` 关闭；
- `--edge-mirror-review-shape-tolerance-mm`：待复核匹配允许的边长差，默认 `600`；
- `--slab-hatch-rule`：填充句柄到板厚或降板规则的显式映射；
- `--slab-default-thickness-mm`：只有无直接尺寸和 HATCH 规则时才使用的默认板厚。
- `--include-beam-intersections`：把正交梁段作为交叉支座候选，并逐条保存来源；
  平行梁段不会被当作连续支座。
- `--beam-intersection-end-tolerance-mm`：正交梁端部距目标梁轴在此范围内时，
  作为 T 形交叉待复核支座；默认 `0`，<项目阶段产物>用 `300` 处理截断端部。
- `--arbitrate-support-count`：候选支座超过梁编号声明跨数要求时，端点优先、
  按证据分保留指定数量，其余候选进入仲裁记录。
- `--support-cluster-tolerance-mm`：同一支座节点附近的候选归并距离，默认 `400 mm`。
- `--endpoint-polygon-support-search-mm`：梁端该距离内存在边缘构件或柱轮廓时，
  补一个 `endpoint-polygon` 复核支座；默认 `0` 关闭，<项目阶段产物>用 `1000 mm`；
- `--endpoint-polygon-width-mm`：端部构件与梁投影不重叠时采用的复核支座宽度，
  默认 `500 mm`；

方量分栏保留，禁止直接相加：

- `梁中心线粗方量`：所有梁对象，只用于能力测试和差异定位；
- `梁支座净跨方量`：仅首尾支座闭合且净跨链条成立的梁，口径接近正式算量但仍需逐条复核；
- `梁推定端支座净跨方量`：仅在显式传 `--assumed-end-support-width-mm` 时生成，端部
  自动补一个假定支座宽度，必须单独列账、不得混入已检出支座净方量；
- `梁待复核支座净跨方量`：梁端存在边缘构件/柱或 T 形复核支座时单列，不能升级为确认净跨；
- `板净闭合区域方量`：仅闭合板环，开放板边界不计入；
- `板拓扑面候选面积`：梁墙边界切出的面，材料类别和板厚未分账前不得折算方量；
- `板按当前板厚粗折`：仅用于核对，HATCH 图例、材料系统和洞口未闭合前不是正式量；
- `墙条带候选`、`边缘构件候选`、`柱候选`：用于拓扑验证，三者不得直接相加为正式剪力墙量。

二层层图回归已得到：

- 边缘构件 114 个、截面面积 `〈实测〉 m2`，对广联达柱表截面 `〈实测〉 m2` 差 `+〈实测〉%`；
- 边缘构件编号为 57 个直接标注、48 个严格镜像、9 个待复核镜像；
- 墙条带 37 段、`44449.9 mm`、`〈实测〉 m3`；
- 独立柱 8 个、`〈实测〉 m3`，清单归类仍需复核；
- 板拓扑面 69 个、`〈实测〉 m2`，对广联达现浇板+叠合板整厚投影 `〈实测〉 m2` 差 `+〈实测〉%`；
- 板厚分账 `120 mm=〈实测〉 m2`、`130 mm=〈实测〉 m2`、`140 mm=〈实测〉 m2`；
  其中 17 个面积项来自直接尺寸标注，17 个来自待视觉复核的 HATCH 规则，35 个来自默认值；
- 7 个洞口候选 `P0005/P0022/P0034/P0043/P0054/P0058/P0064` 尚未闭合扣减；
- 当前板厚粗折为 `〈实测〉 m3`，只能作研发核对，不能作为正式板方量；
- <项目阶段产物>属性修正后，`P0054`、`P0058` 两个矩形-X 洞口合计 `〈实测〉 m2` 已可扣减；
  板拓扑净面积 `〈实测〉 m2`，粗折修正为 `〈实测〉 m3`。`〈实测〉 m3` 是修正前口径；
- 显式启用交叉梁支座后，<项目阶段产物>净跨从<项目阶段产物>的 `2+35` 闭合/推定根提升到 `3+39`，
  未闭合梁从 7 根降到 2 根；`WKL1(2)`、`WKL5(2)` 仍需回原图核对中间支座；
- 梁梁交叉仍只是几何支座候选，已检出加推定净跨 `〈实测〉 m3` 对广联达 `〈实测〉 m3`
  仍低约 `〈实测〉%`，尚未达到梁钢筋翻样门槛；
- <项目阶段产物>用 `300 mm` 端部容差把 `WKL1(2)`、`WKL5(2)` 补为待复核两跨，
  全部 44 根梁都有候选支座链，候选净跨增至 `〈实测〉 m3`；
- <项目阶段产物>同时识别 17 根“支座数超过编号声明跨数”的梁，说明平面相交不能直接等同
  竖向支承；这些梁必须停留在复核层，禁止直接进入梁钢筋翻样；
- <项目阶段产物>启用支座仲裁后，44 根梁的支座数全部与编号跨数一致，21 根发生候选取舍，
  共剔除 32 个低优先候选；候选净跨增至 `〈实测〉 m3`，扣除模型独有 TL/LB 后仍低约
  `〈实测〉%`，而且 43 根仍含 `500 mm` 端部推定支座，不能升级为正式翻样数据；
- <项目阶段产物>用 `1000 mm` 近端构件搜索和 `500 mm` 复核支座宽度补入 42 个
  `endpoint-polygon` 候选；其中 40 个当选、2 个随跨数仲裁淘汰。最终
  `1 clear-span=〈实测〉 m3`、`24 clear-span-review=〈实测〉 m3`、
  `19 clear-span-inferred=〈实测〉 m3`，三者必须分栏，不能把 `〈实测〉 m3`
  冒充已确认净跨；
- 广联达第2层柱汇总行的 `〈实测〉` 是周长，不是体积；不得作为柱模型量。

已执行单元测试覆盖支座扣减、梁端点与粗长一致、同名图层配准、边缘构件开口闭合、
镜像编号分级、HATCH 板厚分账、洞口候选、墙条带扣除、正交柱候选和板面切分。

### 混凝土分账收口（2026-09-10 P13 加，P14 修订）

`cad_concrete_ledger.sh` 读取 `cad-structure-model/v0.5` JSON，可选读取预制底板
拆分图 DXF 和同编号模型汇总 JSON，把梁拓扑、墙柱候选、板厚粗折、预制底板观测面积、
图面重复因子和各完整性门槛汇总为 `cad-concrete-ledger/v0.1`。预制底板优先读取
闭合 `LWPOLYLINE/POLYLINE_2D`；没有闭合多段线时才回退到 `LINE` 开链闭合并。
`S-PC-编号` 文字会按几何近邻绑定到构件，重复编码按模型块数计算重复因子。

```bash
scripts/cad_concrete_ledger.sh \
  --model-json 二层结构模型.json \
  --prefab-dxf 预制底板展开.dxf \
  --prefab-model-json 首层预制底板模型汇总.json \
  --prefab-transform='-353412.428826,68505.754354' \
  --reference '梁及连梁=〈实测〉' \
  --reference '剪力墙=〈实测〉' \
  --reference '板体系=〈实测〉' \
  --reference-floor '首层' \
  --floor-mapping-source '二层梁平法施工图、标高〈标高〉~〈标高〉墙柱平法施工图对应模型首层' \
  --format all -o 首层混凝土分账收口
```

楼层口径必须先核对。某项目 某栋楼的“二层梁平法施工图”和
“标高〈标高〉~〈标高〉墙柱平法施工图”对应广联达“首层”，不能按图纸序号直接
对照广联达“第2层”。修正后的首层收口结果：

- 梁拓扑 `〈实测〉 m3` 对首层梁及连梁 `〈实测〉 m3`，差 `-〈实测〉%`；
- 墙柱候选 `〈实测〉 m3` 对首层剪力墙 `〈实测〉 m3`，差 `-〈实测〉%`；
- 板厚粗折 `〈实测〉 m3` 对首层板体系 `〈实测〉 m3`，差 `-〈实测〉%`；
- 上述 `〈实测〉 m3` 对 `〈实测〉 m3` 只能作研发对账，`formal_ready=false`；
- 预制底板布置图解析出 `42` 个闭合 `LWPOLYLINE`、`〈实测〉 m2`；
  `31` 块中心直接落入板拓扑面，`11` 块在 `500 mm` 内按近边界证据归位，
  当前 `42` 块全部有归属；
- 图面 `YDB-1~12` 与首层模型 `12/12` 个编号匹配；重复因子按同编号模型块数
  计算后，投影面积 `〈实测〉 m2` 对模型 `〈实测〉 m2`，只差 `-〈实测〉 m2`；
- `YKTB-1` 空调板在模型表中未单列，保持 `model-unlisted`，不得偷偷并入 `YDB`；
- 梁支座、板厚依据、叠合/现浇体系、洞口扣减四类门槛仍未通过，禁止进入梁钢筋翻样。
