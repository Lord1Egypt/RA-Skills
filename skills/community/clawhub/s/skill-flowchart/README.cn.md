# SkillFlowChart

> 把任何 `SKILL.md` 转换为自包含的决策流程图 HTML。

[English](README.md) | **中文**

SkillFlowChart 从自然语言技能定义生成干净、确定性的决策流程图。它将工作拆分到各自擅长的领域：**AI 提取语义，脚本计算几何**——同一份输入每次渲染的结果像素级一致。

## 目录

- [工作原理](#工作原理)
- [快速开始](#快速开始)
- [nodes.json 结构说明](#nodesjson-结构说明)
- [主题](#主题)
- [示例](#示例)
- [项目结构](#项目结构)
- [设计原则](#设计原则)
- [贡献](#贡献)
- [许可证](#许可证)

## 工作原理

```
SKILL.md  ──AI 提取──▶  nodes.json  ──脚本渲染──▶  HTML
            (语义理解)    (结构化中继)    (确定性)     (SVG)
```

| 阶段 | 执行者 | 原因 |
|------|--------|------|
| 读取 SKILL.md → nodes.json | AI（LLM） | 自然语言不稳定；AI 理解上下文 |
| nodes.json → HTML | 脚本（Python） | 坐标计算必须确定且可复现 |

AI **永远不**输出坐标或 SVG。脚本 **永远不**猜测语义。两者之间的唯一接口是 `nodes.json` 结构。

## 快速开始

### 前置条件

- Python 3.8+（仅标准库，零依赖）
- 任意 LLM 从你的 `SKILL.md` 中提取 `nodes.json`

### 用法

```bash
# 1. 让 AI 读取 SKILL.md 并生成 nodes.json
#    （提取规则记录在 SKILL.md 中）

# 2. 运行脚本
python3 scripts/flowchart.py nodes.json --out flowchart.html

# 3. 在任意浏览器中打开 HTML
open flowchart.html
```

### 选项

```bash
python3 scripts/flowchart.py <nodes.json> [--out <output.html>] [--theme light|dark|transparent] [--json-out <debug.json>]
```

## nodes.json 结构说明

```json
{
  "title": "我的技能",
  "subtitle": "可选描述",
  "nodes": [
    {"id": "entry",   "type": "entry",    "label": "开始",            "role": "ai"},
    {"id": "check",   "type": "decision", "label": "有效？",           "role": "decision"},
    {"id": "exit",    "type": "terminal", "label": "退出",             "role": "terminal"},
    {"id": "process", "type": "process",  "label": "执行",              "role": "script"},
    {"id": "report",  "type": "output",   "label": "生成报告",          "role": "output"}
  ],
  "edges": [
    {"from": "entry",   "to": "check",   "label": "",    "side": "bottom"},
    {"from": "check",   "to": "exit",    "label": "否",   "side": "left"},
    {"from": "check",   "to": "process", "label": "是",   "side": "bottom"},
    {"from": "process", "to": "report",  "label": "",    "side": "bottom"}
  ],
  "legend": []
}
```

### 节点类型

| type | 形状 | 说明 |
|------|------|------|
| `entry` | 圆角矩形 | 流程起点 |
| `decision` | 菱形 | 分支点（是/否、模式切换） |
| `process` | 圆角矩形 | 处理步骤 |
| `output` | 圆角矩形 | 报告/文件输出 |
| `terminal` | 圆角矩形 | 终止/报错 |

### 角色（配色映射）

| role | 说明 |
|------|------|
| `ai` | AI 推理 / LLM 调用 |
| `output` | 报告/文件输出 |
| `decision` | 决策点 |
| `script` | 脚本执行 |
| `terminal` | 终止/报错 |

> **一个节点只能有一个 role。** 如果一个步骤涉及多种不同性质的工作（例如脚本基线 + AI 分析），必须拆成多个独立节点。

### 边的 `side`（关键）

AI 必须显式标注每条边的 `side`——脚本从不猜测方向。

| side | 含义 | 布局行为 |
|------|------|----------|
| `bottom` | 主流程向下 | 目标在下一层，继承来源 x 坐标 |
| `left` | 决策左分支 / 左侧分叉 | 决策 → 同层水平连接；处理步骤 → 下一层正交分叉 |
| `right` | 决策右分支 / 右侧分叉 | 与 left 对称 |
| `""` | 未标注（同 `bottom`） | 继承上游 |

**决策节点** 的 `left`/`right` → 同层水平连接。
**处理节点** 的 `left`/`right` → 下一层正交分叉（无斜线）。

## 主题

三个内置主题：

| 主题 | 背景 | 标签处理 |
|------|------|----------|
| `light`（默认） | 白色 | 居中 + 白色光晕 |
| `dark` | `#0a0a0f` | 居中 + 深色光晕 |
| `transparent` | 透明 | 垂直边标签偏移到线的一侧 |

```bash
python3 scripts/flowchart.py nodes.json --theme dark --out dark.html
```

## 示例

### HaluCatch（幻觉捕获检测）

完整真实案例，含多级决策、侧支回归、多角色节点。

- [亮色主题](docs/halucatch-light.html)
- [暗色主题](docs/halucatch-dark.html)
- [透明主题](docs/halucatch-transparent.html)

### TRAE Security Review（代码安全审查）

17 节点 18 边，含 4 个决策点、2 个侧支回归、2 个终止丢弃。

- [亮色主题](docs/security-review-light.html)
- [暗色主题](docs/security-review-dark.html)

## 项目结构

```
SkillFlowChart/
├── README.md                          # 英文说明
├── README.cn.md                       # 中文说明
├── SKILL.md                           # 技能定义（AI 入口 + 提取规则）
├── scripts/
│   └── flowchart.py                   # 核心：nodes.json → SVG + HTML
├── docs/
│   ├── halucatch-nodes.json           # 示例输入（HaluCatch）
│   ├── halucatch-light.html           # 示例输出（亮色）
│   ├── halucatch-dark.html            # 示例输出（暗色）
│   ├── halucatch-transparent.html     # 示例输出（透明）
│   ├── security-review-nodes.json     # 示例输入（Security Review）
│   ├── security-review-light.html     # 示例输出（亮色）
│   └── security-review-dark.html      # 示例输出（暗色）
├── tests/
│   └── simple.json                    # 最小测试用例
└── LICENSE
```

## 设计原则

- **结构化中继** —— 布局逻辑不依赖 LLM，同一输入永远产生相同输出
- **零依赖** —— 纯 Python 标准库，无需 `pip install`
- **自包含 HTML** —— 单文件输出，无外部 CSS/JS 引用
- **无斜线** —— 所有连接线都是水平或垂直（正交路由）
- **平台无关** —— 适用于任何 LLM（ChatGPT、Claude、Gemini、本地模型等）

## 贡献

1. Fork 本仓库
2. 编辑 `SKILL.md`（提取规则）或 `scripts/flowchart.py`（布局/渲染）
3. 用 `tests/simple.json` 和 `docs/halucatch-nodes.json` 测试
4. 提交 Pull Request

## 许可证

MIT
