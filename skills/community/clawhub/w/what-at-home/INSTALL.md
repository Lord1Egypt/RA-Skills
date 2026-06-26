# 🏠 家里有什么 - 安装指南

## 概述

智能家庭物品管理系统，解决"东西在哪"、"家里有什么"的日常困惑。支持四级结构：套房 → 房间 → 家具 → 物品。

## 关键词

收纳、整理、居家、存储、物品管理、找东西、家里有什么、东西放在哪、清点物品

## 环境要求

- **Python 3.7+** - OpenClaw 服务器必须已安装 Python（系统级依赖）
- 无需额外 pip 包（只使用 Python 标准库）

## 安装方式

### 方式一：通过 ClawHub 安装（推荐）

```bash
clawhub install what-at-home
```

### 方式二：手动安装

1. 将 `home-storage` 目录复制到你的 skills 目录
2. 确保 Python 3 已安装
3. 数据文件会自动创建在：`{workspace}/data/home_storage.json`（默认为 `~/.openclaw/workspace/data/home_storage.json`）

## 快速开始

### 1. 创建套房和房间

```
设置一套房叫中海寰宇，有客厅、卧室、厨房、卫生间
```

### 2. 添加家具

```
客厅有个电视柜
卧室有个大衣柜
厨房有个橱柜
卫生间有个镜面柜
```

### 3. 添加物品

```
把遥控器放在客厅电视柜里
把剃须刀放在卫生间镜面柜里
```

## 常用命令

| 功能 | 命令 |
|------|------|
| 查看套房 | 查看 中海寰宇 |
| 查询物品 | 我的遥控器在哪？ |
| 搜索物品 | 搜索 遥控 |
| 移动物品 | 把遥控器搬到卧室大衣柜 |
| 删除物品 | 删除 遥控器 |
| 备份数据 | 备份数据 |
| 导出数据 | 导出数据 |

## 数据存储

- 主数据：`{workspace}/data/home_storage.json`（默认为 `~/.openclaw/workspace/data/home_storage.json`）
- 备份目录：`{workspace}/data/backups/`

## 卸载

```bash
clawhub uninstall what-at-home
```

或手动删除 `what-at-home` 目录。

## 许可证

MIT License