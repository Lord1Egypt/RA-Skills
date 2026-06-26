---
name: logistics
description: 物流管理技能，提供提单生成、报关单据生成、物流跟踪等功能。支持 OKKI 客户数据同步和自动化文档处理。
---

# Logistics Skill - 物流管理

## 功能

- 📄 提单 (Bill of Lading) 生成与管理
- 📋 报关单据自动生成
- 🚚 物流状态跟踪
- 🔄 OKKI 客户数据同步
- 📊 物流数据报表

## 使用方式

### CLI 命令

```bash
# 使用 logistics.sh 快捷脚本
./logistics.sh <command> [args]

# 或直接用 Node.js CLI
node cli/logistics_cli.js <command> [args]
```

### API 端点

```bash
# 启动 API 服务
node api/server.js
```

## 环境变量

复制 `.env.example` 到 `.env` 并配置：

```bash
LOGISTICS_API_URL=http://localhost:3000
```

## 目录结构

```
logistics/
├── api/           # API 服务
├── cli/           # 命令行工具
├── scripts/       # 脚本工具
├── templates/     # 文档模板
├── data/          # 示例数据
├── models/        # 数据模型
└── test/          # 测试文件
```

## 注意事项

- ⚠️ `data/` 目录仅存放示例数据，真实数据应存储在外部
- ⚠️ `output/` 目录为运行时生成，已加入 .gitignore
- ⚠️ 敏感信息请通过环境变量配置
