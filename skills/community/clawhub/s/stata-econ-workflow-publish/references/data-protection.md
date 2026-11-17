---
paths:
  - ".claude/MEMORY.md"
  - "dofiles/**/*.do"
  - "MEMORY.md"
---

# Data Protection Protocol

> 源自 codex-stata-for-economists (陈铸)

## 核心规则

```
data/raw/     → 永不提交          (初始数据源，只读)
data/derived/ → 永不提交          (可复现的中间文件)
data/external/ → 可提交           (公共数据集，附引用)
```

## 原因

- 原始数据通常包含敏感信息（纳税人ID、企业名称、地址）
- 中间数据体积大（可复现就无需提交）
- 提交原始数据可能导致法律/合规问题
- **流水线可复现性**：中间文件应当能从原始数据通过do文件复现

## 数据引用

所有数据集必须注明：
- 来源机构
- 年份/版本
- 获取方式
- 使用限制

## 敏感数据处理

处理敏感数据时：

1. 在do文件注释中说明哪些变量包含敏感信息
2. 使用 `drop` 或 `keep` 在早期阶段移除敏感变量
3. 如必须提交样本数据（用于复现），使用去标识化的合成数据
4. 个体层面数据切勿提交

## `.gitignore` 配置

```gitignore
# Data
data/raw/
data/derived/

# Logs
logs/
*.log

# Large files
*.dta
*.csv
*.npy

# OS files
.DS_Store
Thumbs.db
```
