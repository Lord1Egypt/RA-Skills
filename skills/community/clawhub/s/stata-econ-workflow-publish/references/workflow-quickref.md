---
paths:
  - "dofiles/**/*.do"
  - "templates/**/*.do"
  - "CLAUDE.md"
---

# Workflow Quick Reference

> 源自 codex-stata-for-economists (陈铸)。标准操作：PLAN → CONFIRM → EXECUTE → REPORT

## 核心循环

```
[你的指令] → [PLAN] → [你确认计划] → [EXECUTE: 写do文件+跑Stata] → [REPORT: 结果+日志]
```

## 标准流程（按顺序执行）

### 1. 倾听并规划 (LISTEN & PLAN)

#### 倾听
理解用户在做什么：原始数据、目标答案、感兴趣的处理/方法。

#### 提问确认
在写任何代码前，出一份计划。包含：
- 分析目标（一句话）
- 建议的方法（DiD / IV / 事件研究 / DDML / 描述统计）
- 需要的变量及其来源
- 预期输出（表格/图形）
- 可能的陷阱（聚类标准误、缺失值、少量聚类）

用如下格式呈现在代码块中：

```
## PLAN: <分析标题>

- **目标:** [一句话]
- **方法:** [方法名]
- **数据:** [哪个.dta]
- **变量:**
  - Y: [因变量]
  - D: [处理变量]
  - X: [控制变量]
  - cluster: [聚类层级]
- **预期输出:** [表格/图形]
- **陷阱:** [已知风险]
```

等待用户确认后再执行。

### 2. 执行 (EXECUTE)

确认后写do-file。使用 Do File 标准结构（见 `stata-coding-convention.md`）。

#### 写do文件的结构

```
* 00_master.do — 项目总入口 (如需)
* 01_clean/xxx.do — 数据清洗
* 02_construct/xxx.do — 变量构造
* 03_analysis/xxx.do — 回归分析
* 04_output/xxx.do — 表格/图形输出
```

每一个do文件必须:
- 顶部 `version <pin>`
- 设置 `set more off`, `set varabbrev off`
- 开启 `log using` 写入 `logs/` 目录
- 相对路径（不要 `cd "C:\..."`）
- `set seed` 如果涉及随机过程
- 末尾关闭日志

#### 运行

```bash
# 方式1: uvx stata-mcp (推荐，跨平台)
uvx stata-mcp tool do dofiles/03_analysis/main.do --log-file-name main

# 方式2: Stata批处理 (Windows)
"D:\stata19\StataMP-64.exe" /e do dofiles/03_analysis/main.do
```

### 3. 报告 (REPORT)

读取日志，提取结果，呈现为：

```
## RESULTS: [分析名称]

**来源:** logs/xxx.log (第N行)

| 变量 | 系数 | 标准误 | p值 | 显著性 |
|:-----|:----:|:------:|:---:|:-----:|
| treated | -1.632 | (0.584) | 0.006 | *** |
| ... | ... | ... | ... | ... |

**诊断:** N=12,453, R²=0.284, F=28.4
**日志校验:** ✓ 每个数值均可追溯
```

### 4. 学习 (LEARN)

用户修正时记录到 `MEMORY.md`、`TOOLS.md` 或 `CLAUDE.md`。

---

## 各种分析类型的模板速查

| 你想做什么 | 模板文件 |
|:-----------|:---------|
| 差异中的差异 (DiD) | `templates/did-analysis.do` |
| 双/双机器学习 (DDML) | `templates/ddml-analysis.do` |
| 事件研究 | 参考 `event-study.md` |
| RD断点回归 | 参考 `rdrobust.md` |
| 合成控制 | 参考 `synth.md` |

---

## 检查清单 (每次执行后自查)

- [ ] 所有数值结论找到日志/CSV出处
- [ ] 所有do文件有文件头和 `version`
- [ ] 日志文件存在且无错误
- [ ] 路径是相对路径
- [ ] est store 了重要结果
- [ ] set seed 设置（如涉随机）
- [ ] 中文注释
