---
name: 技能商店客户端
slug: skill-shop
version: 1.0.0
description: 技能商店客户端，支持查询在线技能、一键下载安装技能包
author: 龙虾
tags: ["工具", "技能商店", "安装"]
metadata:
  emoji: "🛒"
  requires: ["python3", "unzip"]
---

# 技能商店客户端使用说明

## 功能说明
连接龙虾技能商店，实现技能的在线查询、一键下载安装功能。

## 使用方法
```bash
# 查询所有在线技能
skill-shop list

# 搜索技能
skill-shop search <关键词>

# 安装技能
skill-shop install <技能ID>
```

## 配置说明
无需额外配置，自动连接本地部署的技能商店服务。

## 命令列表
| 命令 | 说明 |
|------|------|
| `list` | 列出所有在线技能 |
| `search <关键词>` | 搜索包含关键词的技能 |
| `install <技能ID>` | 下载并安装指定ID的技能 |
| `info <技能ID>` | 查看技能详细信息 |

## 示例
```bash
# 列出所有技能
skill-shop list

# 搜索包含"API"的技能
skill-shop search API

# 安装ID为7的技能
skill-shop install 7
```
