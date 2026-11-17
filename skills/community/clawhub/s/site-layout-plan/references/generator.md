# 自动候选布置与 A/B/C 比选

本文件对应 `site_layout/generator.py` 与 `scripts/generate_site_layout.py`，内容与 0.7.2 代码同步。

## 1. 它解决什么

`build_site_plan.py` 只校核“已经画好的设施”；`generate_site_layout.py` 进一步在**红线、主体轮廓、道路骨架和周边条件**内，自动给出 A/B/C 三套**候选布置**，再把三套都送进 26 条规则、道路 R1~R4、周边校核和三阶段评分，输出可比较的草案。

```text
reader *.site.json / *.crane.json + 周边说明 + 需求 JSON
→ prepare_site.py（单位归一）
→ generate_site_layout.py（A/B/C 候选 + 三阶段校核 + 比选）
→ 每套 DXF/PNG + 规则/道路/周边明细 + comparison.md
```

自动布置的定位是**经验候选**，不是最优解，也不是施工图。除 DXF/PNG 外，每套方案同时输出 `generated-facilities.json` 和 `generated-cranes.json`，两者都采用单位明确、可被 `build_site_plan.py` 直接读取的契约格式；塔吊文件不是对厂家选型的确认。所有自动设施固定写：

- `source = auto-layout`
- `confidence = candidate`
- `assumption = 自动候选位置，需项目确认`

项目技术负责人必须逐项确认位置、尺寸、朝向、净距和阶段归属。

## 2. 三套方案的性格

| 方案 | 键 | 倾向 | 适合 |
|---|---|---|---|
| A 紧凑经济型 | `compact` | 道路短、占地省、临建紧凑 | 场地紧、成本敏感、工期短 |
| B 均衡推荐型 | `balanced` | 安全、成本、施工便利折中 | 大多数常规项目，默认首选 |
| C 安全文明型 | `safe` | 道路宽、间距大、文明施工余量足 | 场地宽、检查多、创优项目 |

三套方案不是“自动选最优”：技能只做同口径比选，最终方案由项目结合场地、工序、成本和审批要求决定。

## 3. 自动布置顺序

1. 主体轮廓：优先需求 JSON 的 `building.footprint`，其次底图 `buildings[0]`/`structure_outline`，最后才按场地中部假定并写 assumption。无主体时默认报错拒绝；只有显式 `--allow-assumed-building` 才出草案。
2. 大门与围挡：按周边道路/出入口条件候选。
3. 道路骨架：按真实红线多边形内缩生成环形临时主路 + 共线消防车道 + 大门连接路 + 永久道路接顺；内缩失败才退回外接矩形并告警。
4. 塔吊：未给 reader 塔吊时，按主体外接圆半径 + 3 m 假定一台，只用于覆盖和临建避让检查；默认 `active_stages=["structure"]`，土石方/装饰阶段自动退场。
5. 加工区/堆场：塔吊覆盖内、靠近大门；钢筋加工区只进主体阶段，木工、砂浆/砌体加工区进主体+装饰阶段，装饰阶段另设材料堆场；垃圾池全阶段保留。
6. 办公区、员工宿舍区、工人生活区先落位；工人生活区内的食堂/卫生间/晾晒三块再在父包络内整体组合搜索。这样后续变压器能按 10 m 矩形边净距主动避让人员区和可燃堆场，也避免食堂先占大块把卫生间挤出包络。
7. 配电室、变压器、消防水池、消防泵房、停车场、宣讲台、洗车池、垃圾池、九牌一图。
8. 施工电梯：贴靠主体四侧候选，优先靠近道路。
9. 临时水电、消防干管、消火栓：沿道路和主体周边布置；消火栓数量按保护半径/间距动态计算，不再固定为若干个。
10. 指标汇总：场地面积、道路长度（按类别、共线只计一次）、设施占地率、大门数、消火栓数。

## 4. 生活区整体组合搜索（0.7.0）

生活区不再逐块贪心放：先把食堂/卫生间/晾晒按 100%/85%/70%/60%/50% 五档尺寸做笛卡尔组合，按“最差一块的保持比例 → 各块保持比例之和 → 总面积”排序；对每个组合用带面积剪枝的回溯放置，前面子块放不下时可回退并缩小，不再被先放的大食堂锁死。

- 三个子块必须完全位于 `A-LIVING-01` 包络内，互不重叠，并声明 `attrs.parent_id=A-LIVING-01`、`inside_parent=true`。
- 子块默认净距 0.8 m；0.8 m 无解时依次尝试 0.6 m、0.5 m，并把实际净距写入 `assumptions`，不静默放宽。
- 子块形心避开塔吊回转半径，与规则 6 同一口径；边缘净距仍须塔吊选型后复核。
- 搜索预算固定为 1,200,000 个候选节点、单个组合 40,000 个节点，保证同输入同结果，超限明确报错。
- 生活区包络或子块因红线/环道/主体/塔吊夹逼而降级时，写 `size_degraded=true` 和中文 `size_note`；这只是候选示意，实际面积必须按人数、床位数、消防疏散重新选址确认。
- 规则 23 在无风玫瑰/未声明上风向证据时只能 `manual`，不能把西/北侧候选说成已证明上风向；规则 24-26 分别校核道路穿越与消防可达、配套完整性、办公区靠近主出入口。

## 5. 道路几何与指标口径

- `permanent_road` 不参与尽头式判定；它的端点可作为临时道路的“接顺点”。
- 共线的 `temporary_road` 与 `fire_access` 只计一次长度；`road_length_by_category_m` 不重复列消防车道。
- 设施矩形只要与道路带相交即判冲突，不要求四个角都压到道路中心线。
- 道路长度成本基准按场地等效周长 `4×√面积` 计算，不用固定 160 m 一刀切。
- 红线按真实多边形内缩，并检查内缩后是否仍在红线内、是否自交；斜置/凹形场地不再直接套外接矩形。
- 自动选址搜索有预算上限；超限时明确报错，不无限循环。
- 出图窗口按红线外扩 50 m，底图线段用 Liang-Barsky 裁剪；红线弧段只把关键转角放入图内表，全量点仍写 CSV。

## 6. 三阶段评分

`evaluate_scheme()` 支持单阶段和三阶段：

- 输入 `{stage: model}`、`{stage: road_check}`、`{stage: context_check}`；
- 任一阶段 `fail` 即进入硬伤，方案结论为“不推荐（存在硬伤）”；
- 人工确认项取三阶段并集，不因某阶段通过而消失；
- 分数取最不利阶段，不用平均值掩盖装饰阶段的消防/道路问题；
- 输出 `evaluated_stages`、`stage_summary`、`manual_total`。

八个评分维度：成本、可施工性、安全、消防、交通、环境、工期、可审查性。评分是**内部比选参考**，不是评标分、报价或安全评级。

## 7. 命令

```bash
cd site-layout-plan
python3 scripts/generate_site_layout.py \
  --base-map tests/fixtures/base_map_demo.json \
  --context tests/fixtures/context_demo.json \
  --requirements tests/fixtures/requirements_demo.json \
  --scheme all --stages all \
  --out-dir /path/to/demo
```

- `--scheme all|A|B|C`：A/B/C 或单套；未知方案直接报错，不静默回退。
- `--stages all|earthwork,structure,finish`：阶段可子集。
- `--context`：周边条件 JSON（`site-context/v1`）；没有时明确警告“未调查”，不默认安全。
- `--requirements`：项目需求 JSON（`site-layout-requirements/v1`），可给主体轮廓、单位、偏好。

## 8. 输出

```text
out/
├─ scheme-A/ scheme-B/ scheme-C/
│  ├─ generated-facilities.json
│  ├─ generated-cranes.json
│  ├─ layout-<stage>.dxf / .png
│  ├─ stage-<stage>.json
│  ├─ road-check-<stage>.json / .md
│  ├─ context-check-<stage>.json / .md
│  ├─ review-panel-<stage>.json / .md
│  ├─ selfcheck-<stage>.json
│  ├─ titleblock-<stage>.json
│  └─ manifest.json
├─ comparison.json
├─ comparison.md
└─ manifest.json
```

## 9. 边界

- 只做平面候选，不做竖向、高差、埋深、地质、排水坡度、吊装工况和基础验算。
- 红线按真实多边形内缩并做落界/自交检查；仅内缩失败时才退回外接矩形并显著告警。凹口、弧段、门位和退界仍需人工复核。
- 周边距离只是平面净距代理，不含高差、埋深、产权边界和当地退距细则。
- 消防车道净空只能人工确认，平面图判不了净高。
- 不替代施工组织设计审批、消防审查、设计签章和现场复核。

## 出入口服务带（0.6.7）

- 洗车台先于其他区域设施落位，跨第一个大门接入道路（`layout=drive-through`、`on_access_road=true`），后续设施自动避让。
- 地磅随后沿同一大门的主环道直段落位（`layout=on_main_road`），长边顺行车方向，按 100 t 占位：B 型 14 m×4.8 m 外轮廓（3 m 宽称重台＋引坡/传感器），A/C 型分别为 12 m/16 m。
- 九牌一图最后在门侧围挡内滑动选址，按 9 块×1.2 m 长条直线排布，避让道路与洗车台。
- 多门时默认第 1 个大门为主重车出入口；`attrs.gate_index/gate_count/main_gate_assumption` 留痕，必须现场确认。
- 规则 22 校核贴路关系与距门距离；规则 14 不把洗车台/地磅压路误报为普通设施冲突。
