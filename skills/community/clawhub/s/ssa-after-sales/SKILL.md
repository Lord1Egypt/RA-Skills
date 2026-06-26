---
name: after-sales
description: 售后管理技能，提供客户投诉管理、返单报价、满意度调查、分析报表和 OKKI CRM 同步功能。
---

# After-Sales Skill - 售后管理

## 功能

- ⚠️ 客户投诉管理（创建/跟踪/解决）
- 🔄 返单报价管理
- 📊 满意度调查
- 📈 分析报表（投诉统计/客户风险分析）
- 🔄 OKKI CRM 同步（自动创建售后跟进记录）

## 使用方式

### CLI 命令

```bash
# 使用 after_sales.sh 快捷脚本
./after_sales.sh <module> <command> [options]

# 或直接用 Node.js CLI
node cli/after_sales_cli.js <module> <command> [options]
```

### 常用命令

```bash
# 投诉管理
./after_sales.sh complaint list
./after_sales.sh complaint create -n '客户名' -t quality -d '问题描述'
./after_sales.sh complaint get CMP-xxx

# 返单报价
./after_sales.sh repeat-order list
./after_sales.sh repeat-order create -n '客户名' -R 50000

# 满意度调查
./after_sales.sh satisfaction list
./after_sales.sh satisfaction stats

# 分析报表
./after_sales.sh analytics summary
./after_sales.sh analytics risk

# OKKI 同步
./after_sales.sh okki sync-complaint CMP-xxx
./after_sales.sh okki logs
```

## 环境变量

复制 `.env.example` 到 `.env` 并配置：

```bash
# OKKI 路径配置（可选，默认使用相对路径）
OKKI_WORKSPACE_PATH=/path/to/xiaoman-okki
OKKI_CLI_PATH=/path/to/okki_cli.py
OKKI_CLIENT_PATH=/path/to/okki_client.py
```

## 目录结构

```
after-sales/
├── api/           # API 服务
├── cli/           # 命令行工具
├── scripts/       # 脚本工具
├── models/        # 数据模型
├── data/          # 数据文件（运行时生成）
└── test/          # 测试文件
```

## OKKI 集成

- 自动将投诉/返单记录同步到 OKKI CRM
- 使用 `trail_type=107`（售后跟进）
- 支持客户 ID/名称匹配
- 同步日志持久化到 `data/okki_sync_logs/`

## 注意事项

- ⚠️ `data/` 目录为运行时数据，已加入 .gitignore
- ⚠️ 敏感信息请通过环境变量配置
- ⚠️ OKKI 路径支持环境变量覆盖，默认使用相对路径
