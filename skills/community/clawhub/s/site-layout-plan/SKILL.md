---
name: site-layout-plan
slug: site-layout-plan
displayName: 施工平面布置图
version: 0.7.3
platforms: [macos, windows, linux]
author: lis
license: CC-BY-NC-SA-4.0
description: "施工平面布置：总工视角多方案比选+消防道路校核；不替代审批。触发词：塔吊布置。"
locale: zh-CN
---

# 施工平面布置图

本技能 0.7.3 从**施工单位经验丰富的项目总工**视角，把 reader 的场地证据变成可讨论、可校核、可分阶段出图的平面布置草案：

1. 消费 reader 的 `*.site.json`、`*.crane.json`、`site-handoff/v1`、`cad-contract/v1`，单位确认后归一为 mm 底图。
2. 在红线、主体轮廓、道路骨架和周边条件内，自动给出 **A 紧凑 / B 均衡 / C 安全文明** 三套候选布置，逐套跑规则、道路和周边校核。
3. 按 **土石方 / 主体 / 装饰** 三阶段分别建模、校核、出图，不用一张主体图覆盖全过程。
4. 校核 26 条临建规则 + 道路 R1~R4（宽度、会车、转弯半径、回车场）+ 周边硬/软约束。
5. 用项目总工、安全总监、消防/临建、文明环保、商务成本、甲方/报建六个视角重排结论与待办。
6. 输出 DXF/PNG、图签、自检、阶段变化表和 A/B/C 比较表；三阶段图带真 `DIMENSION`、角点/设施坐标 CSV 与图内表、指北针、比例尺和分区图例；图签始终带 `DRAFT`，`final_check=false`。

## 识图硬链路（不可绕行）

```text
DWG/DXF/PDF
→ lis-skill-bus（唯一定接线，发起/取回契约）
→ cad-file-reader（唯一解图：cad_scan + cad_site_geometry + cad_crane_geometry）
→ cad-contract/v1
→ lis-skill-bus（只搬运，不推断）
→ site-layout-plan
```

- 本技能**不打开、不解析** DWG/DXF/PDF，不 import `ezdwg`/`ezdxf`/`read_cad` 解图，也不自带或重下 reader。
- `prepare_site.py`、`draw_layout.py` 读取前先拒绝 `.dwg/.dxf/.pdf`；只收 `schema=cad-site-geometry/v1` 且 `contract.contract_version=cad-contract/v1` 的 JSON（出图也接受 `prepare_site.py` 从该契约派生的 `base-map.json`），否则 exit 2。
- `crane_check.py` 只收 `site-handoff/v1` 且带 `contract_id/source_sha256` 的 reader 契约，直读 CAD 同样 exit 2。
- bus 或 reader 缺失时如实标 `unavailable` 并停止，不提供第二套识图路径，也没有 `CAD_ALLOW_DIRECT` 逃生口。

## 标准链路

```text
DWG/DXF
→ lis-skill-bus（发起）
→ cad-file-reader: cad_scan + cad_site_geometry + cad_crane_geometry
→ cad-contract/v1
→ lis-skill-bus（取回，只搬运不推断）
→ prepare_site.py：契约闸门 + 单位确认 + mm 归一 + 红线串接 + 留痕
→ base-map/v1
→ generate_site_layout.py：A/B/C 自动候选 + 三阶段校核 + 比选
   （每套输出 generated-facilities.json 与 generated-cranes.json）
→ build_site_plan.py：人工确认设施（可直接读取上述两份生成契约）的三阶段模型 + 26 规则 + 道路 R1~R4 + 六视角
→ crane_check.py + draw_layout.py：单阶段塔吊吊装校核与出图（可选）
```

### 单位口径

reader 的单位可能在顶层 `coord_unit`，也可能只在 `scale_unit_audit[].units` 或逐条几何。`prepare_site.py` 按“顶层 → `scale_unit_audit[]` → 逐条几何 → 人工 `--unit`”读取；reader 顶层没有 `coord_unit` 时自动回退 `scale_unit_audit[].units`，不需要手工给 JSON 补行。无单位或冲突一律 exit 4，不猜 10/1000 倍。详见 `references/prepare.md`。

## 快速命令

```bash
cd site-layout-plan

# 1. reader 契约 -> mm 底图
python3 scripts/prepare_site.py --site 总图.site.json --out-dir out/prepared

# 2. 自动 A/B/C 候选 + 三阶段校核 + 比选
python3 scripts/generate_site_layout.py \
  --base-map out/prepared/base-map.json \
  --context 周边条件.json --requirements 项目需求.json \
  --scheme all --stages all --out-dir out/site-layout

# 3. 人工确认设施后的正式三阶段校核/出图
python3 scripts/build_site_plan.py \
  --base-map out/prepared/base-map.json \
  --facilities out/site-layout/scheme-B/generated-facilities.json \
  --cranes out/site-layout/scheme-B/generated-cranes.json \
  --stages all --out-dir out/site-plan

# 4. 单阶段塔吊逐柱校核（可选）
python3 scripts/crane_check.py --handoff site_handoff.json \
  --fleet crane_fleet.json --baseline baseline.json --out-dir out/crane

# 5. 7 类设施大样 PNG；分张与 --only 见 references/draw.md
python3 scripts/render_facility_showcase.py --out out/facility-showcase.png
```

## 本版能做什么

A/B/C 三套候选、真实红线/主体、三阶段建模校核出图、26 条临建规则、道路 R1~R4、周边硬软约束、六视角审查、7 类自绘标准块（DXF BLOCK 与 PNG 同源）、图签与 `DRAFT` 留痕、R12 看图版、单位与同源闸门。完整清单见 `references/capabilities.md`。

## CAD快速看图兼容（R12 看图版）

主交付仍是 R2010 DXF；手机/国产看图软件另出 R12 看图版（降级、移原点、对齐视口），命令与三个坑见 `references/draw.md` 第 8 节。

## 本版不能做什么

- 不自动生成“最优布置”：A/B/C 是经验候选，不是最优解，必须逐项确认位置、尺寸、朝向、净距和阶段归属。
- 不做塔吊选型、基础/附着/群塔碰撞、吊装工况和厂家性能表核验。
- 不做竖向、高差、埋深、地质、排水坡度、道路结构承载力和视距校核；周边距离只是平面净距代理。
- 不把默认值当规范结论：3.5/6/4 m、9/12 m、12 m×12 m、消火栓 120/150 m、高压线 8 m 等均为 [经验] 起步值，项目按当地规范和专项方案复核。
- 不替代施工组织设计审批、消防审查、设计签章、报建和现场复核；`final_check` 恒为 `false`。
- 红线内缩按真实多边形计算，并检查落界、自交和转角简化；凹口、弧段、门位和退界仍需人工复核。仅当多边形内缩失败时才退回外接矩形并显著告警，不能当精确边界。

## 详细参考（按需读取）

- reader 契约、单位优先级、prepare 退出码：`references/prepare.md`
- 本版能力清单：`references/capabilities.md`
- 设施分类、设施 JSON、三阶段、26 条规则：`references/site-plan.md`
- A/B/C 自动候选、评分、输出：`references/generator.md`
- 周边条件、六视角、分阶段研判：`references/context-and-schemes.md`
- 道路 R1~R4、会车/转弯/回车场画法：`references/road-review.md`
- 塔吊校核三件套：`references/crane-check.md`
- 单阶段塔吊出图：`references/draw.md`
- 隐私、外发与发布前扫描：`references/privacy-and-release.md`

## 退出码

| 码 | 含义 | 处理 |
|---:|---|---|
| 0 | 成功，自检无 fail | 读 selfcheck/图签 |
| 2 | 输入 JSON/字段/依赖错误 | 修输入或装依赖 |
| 4 | 坐标或图纸单位不是 mm/m | 先换算单位 |
| 5 | 口径未锁、不同源、自检 fail、原图哈希变化 | 修契约/看 selfcheck |

## 自测

```bash
cd site-layout-plan
python3 -m py_compile scripts/*.py site_layout/*.py
for t in tests/test_*.py; do python3 "$t" || exit 1; done
```

覆盖：识图契约闸门（直读 DXF/非 reader JSON 被拒）、单位回退/冲突、红线内缩、出图窗口、塔吊三件套、三阶段规则与道路、六视角、图块与图例、A/B/C 候选、坐标 CSV、R12 导出。

## 依赖与数据边界

- 校核核心纯 stdlib；出图需 `ezdxf>=1.4` 与 Pillow。优先 `SITE_LAYOUT_VENDOR`，其次 `CAD_FILE_READER_HOME/vendor`，再次 `${CODEX_HOME:-$HOME/.codex}/skills/cad-file-reader/vendor`；系统 Python 缺依赖时自动 re-exec 到 Codex 本地 Python 3.12。
- 本机可读取、解析、编辑、测试真实图纸并用于制作本技能；不得擅自外发。发布物须扫描脱敏，禁含真实公司资料；公司样例须列明字节并获同意。
- 结果为布置草案与规则校核，须经项目技术负责人审核；不替代审批、消防审查、厂家性能表核验和现场复核。
