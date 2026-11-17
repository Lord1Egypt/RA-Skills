# text-to-infographic

把文本变成**可编辑、可校验、可安全分享**的单页信息图。

- **text→plan 自动构建**：`--analyze` 启发式推荐布局（给证据），LLM 抽 blocks，`--from-blocks` 组装并即校——粘贴文章不需要从零写 JSON；
- **结构化 plan**：信息图先写成 JSON（schema 见 `schemas/`），改一个块 = 重渲染，不推倒重来；
- **信息正确校验**：布局语义（飞轮必须闭环、鱼骨只能单头、桑基必须守恒、仪表盘必须有单位）+ 数值可溯源；每条问题带**稳定规则码**（FLY-002 / SANK-003 …），`--explain` 中文诊断（为什么/怎么改）、`--json` 机器回执、`--fail-on-warn` 严格模式，可校验任意来源的 plan；
- **chart_family 六布局**：flywheel / fishbone / sankey / pyramid / timeline / dashboard —— 通用模板库不覆盖的专用布局；
- **克制的视觉 token**：8 种 palette preset（含 editorial / technical / warm）+ accent / ink / paper / muted 四 token 覆盖，一套对的而不是十种花的；
- **可选 PNG 导出**：`--png` 用本机已有浏览器截图（2x 高清，小红书/公众号直发），不安装任何东西，失败不影响 HTML；
- **安全渲染**：产物为单文件静态 HTML，零 JavaScript、零外部请求、零依赖安装，离线可用、可打印。

## 快速开始

```bash
# ① 分析文本，拿布局推荐
python3 scripts/build_plan_from_text.py --analyze 文章.md

# ② LLM 抽好 blocks 草稿后组装（组装即校验）
python3 scripts/build_plan_from_text.py --from-blocks draft.json \
    --layout flywheel --style editorial -o plan.json

# ③ 校验（带中文诊断；--json 拿机器回执，CI 用 --fail-on-warn）
python3 scripts/validate_infographic_plan.py plan.json --explain

# ④ 渲染（--png 一并出图，可选）
python3 scripts/render_infographic_html.py plan.json out.html --png
```

已有 plan 也可以直接走 ③④。仅需 Python 3.10+ 标准库；PNG 导出另需本机已装有 Chrome / Chromium / Edge（不自动安装）。

## 文档

- SKILL.md —— agent 调用契约
- docs/校验规则规格 —— A/B/C 三层校验设计
- CHANGELOG.md —— 版本历史
