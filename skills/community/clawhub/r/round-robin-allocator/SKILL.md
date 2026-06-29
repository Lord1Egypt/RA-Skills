---
name: round-robin-allocator
author: wUwproject
data_dir: ../.standardization/round-robin-allocator/
license: MIT
version: 1.6.0
description: 均匀轮转分配工具 — 将 N 个对象在 T 个轮次中按比例分配 K 种选项，最大化覆盖多样性，支持四种后处理模式调整重复分布。
tags: ['分配', '轮转', 'round-robin', '覆盖', '后处理', '可视化']
external_data_dir: true
sensitive_access: false
critical_write: false
permission_weight: LOW
trigger: ['分配', '轮转', '分配算法', 'round-robin', '均匀轮转', '覆盖', '后处理', '配额']
trigger_negative: ['不分配', '不需要分配', '与其他无关']
data_dir_compliance: true
---
# round-robin-allocator

> 给 N 个「对象」，在 T 个「轮次」中，按比例把 K 种「选项」分配出去，
> 并让每个对象每轮尽量拿到不同的选项。

## 核心能力

- **自然语言解析**：支持中英文混合描述（如「33个项目，4个月，5套方案，比例7:8:10:3:5」）
- **Hamilton 配额 + 贪心分配**：精确按比例计算配额，最大化覆盖多样性，迭代优化消除重复
- **四种后处理模式**：ID排序 / 随机打乱 / 均匀分布 / 自定义月间重复比例
- **确认表 + 配置系统**：代码强制钩子流程，支持跳过确认、默认模式持久化
- **多种输出**：Markdown 明细表 + HTML 热力图表（含 3D 散点图）+ CSV 可选导出
- **补全机制**：缺参数时不会编造或推断，通过选项 9 自然语言补充

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

### 渐进式文件索引

| 文件 | 说明 |
|------|------|
| `references/usage.md` | 详细使用指南（确认表/菜单/后处理/配置/输出） |
| `references/algorithm.md` | 分配算法与后处理算法说明 |
| `references/antipatterns.md` | 反模式与常见错误 |
| `references/faq.md` | FAQ 与排错指导 |
| `references/changelog.md` | 更新日志 |

## 使用方式

### AI 对话

**场景 1：标准分配（等分比例）**
```text
用户：我有 33 个项目，4 个月，5 套方案，比例是 7:8:10:3:5
计算报告：已解析参数 N=33, T=4, K=5, 比例=7:8:10:3:5
结果：输出分配明细表 + 热力图表（含分布统计和 3D 散点图）
```

**场景 2：均匀分布（避免集中）**
```text
用户：12 个学生，6 周，3 个课题，比例 4:4:4，用 fair 模式
计算报告：已解析参数 N=12, T=6, K=3, 比例=4:4:4, 模式=fair
输出结果：每周 3 个课题均匀分配，每个学生前两周不重复，热力图显示覆盖平衡
```

### 命令行

```bash
python scripts/main.py --input "33个项目，4个月，5套方案，比例7:8:10:3:5"
python scripts/main.py --input "..." --mode fair
python scripts/main.py --input "..." --no-confirm
```

→ 详见 `references/usage.md`
## 限制与边界

| 约束项 | 说明 |
|--------|------|
| **输入规模** | 建议 N ≤ 1000 个对象，T ≤ 52 轮，K ≤ 20 种选项。超过会降低性能 |
| **比例约束** | 比例之和必须等于 N。不指定比例则默认等分 |
| **参数缺失** | N/K/T 缺任意一个无法执行，工具不会自动推断 |
| **运行环境** | 脚本需 Python ≥ 3.8，仅标准库。HTML 可视化图表依赖 CDN（Chart.js + Plotly.js）|
| **后处理范围** | 后处理只影响分配显示顺序，不影响配额计算的正确性 |

## 触发场景

**正向触发**：
- 用户需要均匀轮转分配：将 N 个对象在 T 个轮次中分配 K 种方案
- 需求涉及配额/覆盖/轮转/方案分配
- 需要调整重复事件的月间分布

**否定条件**：
- 简单问答、闲聊、问候
- 用户明确说"不分配"

## 文件结构

```text
round-robin-allocator/
├── SKILL.md              # 入口文档
├── _meta.json            # 元数据
├── references/           # 渐进式文档
│   ├── usage.md          #   使用指南
│   ├── algorithm.md      #   算法说明
│   └── changelog.md      #   更新日志
└── scripts/
    ├── allocator.py      # 核心算法（纯标准库）
    ├── main.py           # CLI 入口
    └── visualizer.py     # HTML 生成器
```

## 依赖

- **Python ≥ 3.8**，仅标准库
- HTML 可视化：Chart.js + Plotly.js（CDN 加载）

> 详见 [反模式](references/antipatterns.md)

> 详见 [FAQ](references/faq.md)

