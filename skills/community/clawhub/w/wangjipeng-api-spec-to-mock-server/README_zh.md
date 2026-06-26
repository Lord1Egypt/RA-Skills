# Api Spec To Mock Server

[English](./README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![版本](https://img.shields.io/badge/version-1.0-blue)

> user provides API spec in OpenAPI or Swagger format and needs a runnable mock server

## 解决什么问题

简要说明这个技能解决的具体工程问题。
触发条件：[trigger condition]。

## 功能特性

- 将 api spec to mock server 输入转换为结构化输出
- 处理 user provides api spec in openapi or swagger format ...
- 保持数据完整性——无静默丢弃或虚构

## 快速开始

### 安装

```bash
# 通过 ClawHub 安装
clawhub install Api Spec To Mock Server

# 或手动复制
cp -r Api Spec To Mock Server ~/.openclaw/skills/
```

### 使用方法

```bash
# 模式 1：读取
clawhub run Api Spec To Mock Server --mode read

# 模式 2：写入
clawhub run Api Spec To Mock Server --mode write --input ./data.json
```

## 目录结构

```
Api Spec To Mock Server/
├── SKILL.md          # 技能入口
├── LICENSE           # MIT 许可证
├── README.md         # 英文说明
├── README_zh.md      # 本文件
├── CONTRIBUTING.md    # 贡献指南
├── .gitignore
├── references/       # 模板和 schema
│   └── ...
└── scripts/          # 辅助脚本（如有）
    └── ...
```

## 配置

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `API_KEY` | 是 | 服务 API Key |

## 许可证

本项目采用 MIT 许可证 — 详见 [LICENSE](LICENSE)。

---

由 [MiniMax](https://minimax.io) 提供支持。