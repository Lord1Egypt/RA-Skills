---
name: shizheng-suanliang
slug: shizheng-suanliang
displayName: 市政算量 · 道路管道井类计划口径速算
version: 1.1.1
platforms: [macos, windows, linux]
author: lis
license: CC-BY-NC-SA-4.0
description: "市政图出管道延米/井数/道路面积估算带；不替代清单编制与结算。触发词：市政算量、管道、道路面积、检查井。"
i18n:
  en: README.en.md
  zh: README.md
locale: zh-CN
locales: [zh-CN, en-US]
---

# 市政算量

## 识图契约红线（硬规则，禁止绕行）

- 算量技能**不得单独识别 DWG/DXF/PDF**：识图只能由 `cad-file-reader` 的 `municipal-geometry` 识图包做一次，产出 `cad-municipal-geometry/v1` 契约后本技能消费。
- **禁止自行 `import ezdwg/read_cad`、自带或重新下载解图器**；底座缺失如实标 `unavailable`，不得降级成「自己解图」。
- 算量入口不提供任何图纸直读逃生开关：DWG/DXF/DWT 一律按退出码 `23` 停止；算量结果必须带契约来源（contract_id/哈希证据）。
- `lis-skill-bus` 是契约与算量技能之间的唯一定接线。
- 内存与解图兜底（ODAFileConverter 转码等）只能发生在 `cad-file-reader` 底座内，本技能不得调用 CAD/看图 App。

## 入口闸门（固定退出码，禁止 fallback）

未安装依赖时唯一正确行为是**停止**：打印固定提示并原样回显安装命令，不得改用其它解析器，也不得内置解析图纸。

| 退出码 | 含义 | 处理 |
|---|---|---|
| `0` | 依赖就绪 | 继续 |
| `20` | 缺 `cad-file-reader` 或版本 < 0.41.0 | 停止，回显安装命令 |
| `21` | 缺 `lis-skill-bus` 或版本 < 0.1.11 | 停止，回显安装命令 |
| `22` | 契约无效（版本/结构/来源/哈希/单位） | 停止，回 `cad-file-reader` 重新生成 |
| `23` | 直接传入 DWG/DXF/DWT | 停止，改走契约 |
| `24` | 证据不足，或只有手工来源却要求正式量 | 停止；仅手工契约可出 `final_quantity=false` 草稿 |

固定提示：`本技能不直接识图，请先安装并调用 cad-file-reader（municipal-geometry 识图包）生成 *.municipal.json，再经 lis-skill-bus 传入；不许 fallback 到内置解析。`

## 口径摘要（全文见 `references/on-demand.md`）

- **管道延米**＝管道图层几何段长合计（图面口径，系统偏低）→ 估算带 ×[1.00, 1.15]，按系统分组（雨水/污水/给水/再生水/热力/燃气/电力/通信）；无法映射系统的段单独归「未分类」，不硬套。
- **管径只分档计数**：从 `pipe_network[].pipe_size` 文本提取 DN/De/d/Φ 进档（300~1500+），**不做管径×几何段强配**——缺"哪段是哪根管"的配对依据，强配就是编造。
- **井类计数**：components 命中 检查井/雨水口/跌水井/阀门井/泵站 按系统计数；`connectivity.junction_candidates` 只交叉核对，不并入计数。
- **道路面积带**＝道路中线/边线段长 × labels 宽度标注多数档，±15%；缺宽度标注一律进缺项清单，面积 `unavailable`，**不默认宽度**。
- **路面结构层**：materials 只列清单并标注层厚缺失，不做分层面积（厚度证据缺失，分层就是编造）。
- **土方不做**：无横断面填挖数据，任何土方数字都是编造，直接进边界说明。
- m 单位图纸必须给 `unit_scale`（m→mm 系数），缺了只出计数与缺项清单，不出长度/面积。

强依赖 cad-file-reader（唯一识图底座）与 lis-skill-bus，缺底座按 entry_gate 退出码 20/21 停止。用法/流水线、口径全文见 `references/on-demand.md`。

## 边界（必须对用户如实说）

1. 这是**计划口径毛量估算带（±15%）**：`final_quantity=false`，**不能**用于工程量清单编制、竣工计量、劳务结算、报价。
2. 缺依据的项一律进**缺项清单**并写明缺什么，绝不用默认值凑数（宽度、管径配对、层厚、土方都没有默认值）。
3. 管道延米是图面口径：不含工作井内接管、预留支管、图幅外管线；`connectivity.open_endpoints` 非零时明确提示延米可能偏少。
4. 桥梁/涵洞/隧道构件（桩基、箱梁、衬砌等）本版只透传识图候选与待复核项，**不出构件量**——缺配筋/截面/标高证据，硬算是编造。
5. m 单位、天正自定义实体、图例符号剔除后剩余证据不足的图纸，会出现可解释的缺项——按缺项清单补参数即可，不要相信"跑通了就是对的"。
6. 图面线段长度只是单段几何证据，不是最终管道/道路长度（识图层边界沿用）。

## 依赖与入口策略（contract-only）

- 强依赖 `cad-file-reader >= 0.41.0`（含 `packs/municipal-geometry` 识图包）与 `lis-skill-bus >= 0.1.11`，Python >= 3.10；本技能不自动下载、不自带解图器。
- 先跑 `python3 scripts/municipal_qty.py --check-deps`：缺依赖 exit 20/21（缺 reader 20、缺 bus 21），并打印可复制的安装命令。
- 手工契约必须显式 `--allow-manual`，结果强制 `final_quantity=false`、`formal_ledger_eligible=false`；无 bus 时正式入口直接停止，不回退本机解图。

## 运行时

所有 `scripts/*.sh` 自动解析 Python、cad-file-reader 和依赖路径。排障与手工安装见 `docs/runtime.md`（同其他算量技能）。

## 授权与保留

CC-BY-NC-SA-4.0，仅限非商业用途。商业使用（含承接造价/算量咨询业务）须另行取得作者书面授权；作者保留全部商业权利。条款全文见 `LICENSE.md`。
