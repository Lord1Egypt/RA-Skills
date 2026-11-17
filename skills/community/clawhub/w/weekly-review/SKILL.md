---
name: weekly-review
description: >
  面向任意 AI Agent 自动复盘的 Skill（weekly-review / 复盘 / 提示词优化 / 会话清理）。

  核心能力覆盖：AI 用量与时间看板、提示词复盘与改写建议、高效/低效归因、
  时间分布与 Token/归因趋势图、开放会话对齐清理、定时自动周报。

  当用户任务涉及周度复盘、用量查看、提示词改进时使用，包括但不限于：
  Token 花了多少、提示词优化改进、一周总结、工作复盘、复盘可视化报告、
  清理对话、AI 自动复盘。
version: 1.2.5
category: 办公效率
read_when:
  - 提示词改进
  - 本周 AI 用量看板
  - 高低效归因
  - 复盘可视化报告
  - 清理开放对话
  - 定时/自动周报
  - weekly-review / 复盘 / /weekly-review
metadata:
  openclaw:
    requires:
      bins:
        - python
    emoji: "📊"
    homepage: https://github.com/testman2025/weekly-review-skill
    os:
      - macos
      - linux
      - windows
---

# AI 用量与提示词复盘助手（weekly-review）

用来做：提示词改进、本周 AI 用量看板、高低效归因、复盘可视化图表、开放会话清理、定时/自动周报。宿主 Agent 采数，本 skill 按六章模板出报告。

## 输出结构（锁定）

1. **一页看板**：`| 指标 | 数值 | 口径说明 |` + **一句话结论** + 可选「辅助图表」PNG 路径  
2. **分项目分析**：`### 2.x 主题（时长/会话）` + `| 维度 | 内容 |`（做了什么 / DB cwd / 磁盘核对 / 低效 / 提示词）；其他用简表  
3. **问题清单 + 根因三类归因** + **做得好的（正面范本）**  
4. **本周动作台账 ★**：当场已改 / 观察 / 待落实（或待落实→执行结果）  
5. **待对齐开放会话**  
6. **自动化概览**  
7. **事实更正**（可选，有核对推翻时必写）

**图表约定**：渲染器生成两张定稿样式图——横向「时间投入分布」、双栏「低效归因 + Token 趋势」（SVG）。数据来自 `charts_data`。看板主表仍是 `| 指标 | 数值 | 口径说明 |`。

## 输入

见 `schema/review-input.example.json` 与 `schema/README.md`。

## 操作流程

1. 安装本 skill（见仓库根 README：`npx skills add` / ClawHub / clone）。  
2. Agent 采集会话/用量，**Glob/ls 核对磁盘**后再归因。  
3. 填 `review-input`（或对话等价结构）；需要图时先出 PNG 再填 `dashboard.charts`。  
4. 按六章输出，或 `python -m cli --input review-input.json -o YYYY-MM-DD周度复盘.md`。  
5. 对开放会话当场拍板。定时场景见仓库 `automations/`。

### CLI

```bash
cd {SKILL_DIR}
python -m cli --input schema/review-input.example.json -o 周度复盘.md
# 图表默认写到报告同目录；关闭：加 --no-charts
```

### MCP

工具 `run_weekly_review`，参数 `review_input`（对象）。
