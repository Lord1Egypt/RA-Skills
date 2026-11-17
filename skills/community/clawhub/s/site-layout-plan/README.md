# 施工平面布置图（site-layout-plan）

把 CAD 场地识图契约变成可讨论、可校核、可分阶段出图的施工总平面布置草案。技能从项目总工视角给出 A 紧凑 / B 均衡 / C 安全文明三套候选，逐套跑 26 条临建规则、道路 R1~R4 和周边约束，并输出 DXF/PNG、图签、自检与比选表。

## 识图硬链路（不可绕行）

```text
DWG/DXF/PDF
→ lis-skill-bus（唯一定接线）
→ cad-file-reader（唯一解图）
→ cad-contract/v1
→ lis-skill-bus（只搬运契约）
→ site-layout-plan
```

- 本技能不打开、不解析 DWG/DXF/PDF，不 import `ezdwg`/`ezdxf`/`read_cad` 解图。
- `prepare_site.py`、`draw_layout.py` 只收 `cad-site-geometry/v1` 且 `contract.contract_version=cad-contract/v1` 的 reader 契约（出图也接受其派生 `base-map.json`）；直读 CAD 或普通 JSON 一律 exit 2。
- `crane_check.py` 只收带 `contract_id/source_sha256` 的 `site-handoff/v1`。
- 缺 `lis-skill-bus` 或 `cad-file-reader` 时标 `unavailable` 并停止，没有第二套识图路径。

## 安装

1. 安装 `lis-skill-bus` 与 `cad-file-reader`，确认 bus 的 MCP 或 CLI 可用。
2. 把本目录放入 Codex 技能目录，使 `SKILL.md` 的 frontmatter 被识别。
3. 出图依赖 `ezdxf>=1.4` 与 Pillow；校核核心只用 Python 标准库。

## 快速开始

```bash
# 1. reader 契约 -> mm 底图（会先校验契约来源）
python3 scripts/prepare_site.py --site 总图.site.json --out-dir out/prepared

# 2. A/B/C 候选 + 三阶段校核 + 比选
python3 scripts/generate_site_layout.py \
  --base-map out/prepared/base-map.json \
  --context 周边条件.json --requirements 项目需求.json \
  --scheme all --stages all --out-dir out/site-layout

# 3. 确认设施后的正式三阶段校核与出图
python3 scripts/build_site_plan.py \
  --base-map out/prepared/base-map.json \
  --facilities out/site-layout/scheme-B/generated-facilities.json \
  --cranes out/site-layout/scheme-B/generated-cranes.json \
  --stages all --out-dir out/site-plan
```

## 输出

- `base-map.json`：统一 mm 的底图、红线闭合与单位判定留痕。
- `scheme-A/B/C`：候选设施、塔吊、规则结果与评分。
- `site-plan/`：三阶段 DXF/PNG、图签、自检、阶段变化表、角点/设施坐标 CSV。
- 图签始终带 `DRAFT`，`final_check=false`。

## 能力边界

- A/B/C 是经验候选，不是最优解；位置、尺寸、朝向、净距和阶段归属须逐项确认。
- 不做塔吊选型、基础/附着/群塔碰撞、吊装工况与厂家性能表核验。
- 不做竖向、高差、埋深、地质、排水坡度、道路承载力和视距校核。
- 规则 26「办公区靠近主出入口」的 50 m 只是经验提示，超距记 `manual`，不阻断出图。
- 不替代施工组织设计审批、消防审查、设计签章、报建和现场复核。

## 许可

CC-BY-NC-SA-4.0；商业使用需另行授权，详见 `LICENSE.md`。
