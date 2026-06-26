---
name: rembg
description: 使用 rembg AI 模型去除图片背景，生成透明背景的 PNG 图片。首次使用需运行 setup/install.py 初始化环境。
---

# rembg - AI 抠图工具

使用 rembg（基于深度学习的背景去除工具）为图片去除背景。

## 快速开始

### 1. 初始化环境

首次使用必须先运行环境初始化：

```bash
cd <Skill目录>
python3 setup/install.py
```

初始化后会：
- 在用户根目录 `~/.venv/rembg/` 创建虚拟环境
- 自动安装 requirements.txt 中的依赖

### 2. 验证环境

```bash
python3 setup/check_env.py
```

### 3. 使用

```bash
# 单张图片处理
python3 scripts/remove_bg.py <输入图片路径>

# 批量处理
python3 scripts/batch_remove_bg.py <输入目录> [输出目录]
```

## 目录结构

```
rembg/
├── SKILL.md              # 本文件
├── _meta.json           # 元数据
├── setup/               # 环境初始化
│   ├── install.py       # 安装脚本（创建 ~/.venv/rembg/）
│   ├── requirements.txt  # 依赖声明
│   └── check_env.py     # 环境检查
├── scripts/             # 业务脚本
│   ├── remove_bg.py     # 单张处理
│   └── batch_remove_bg.py  # 批量处理
├── references/          # 参考文档
│   └── rembg-guide.md  # 详细指南
└── image_output/        # 输出目录（运行时生成）
    ├── single/          # 单张结果
    └── batch/           # 批量结果
```

## 环境说明

- **虚拟环境位置**：`~/.venv/rembg/`（在用户根目录）
- **AI 模型位置**：`~/.u2net/`
- 首次运行会自动下载 AI 模型（~176MB）
- 所有脚本使用 `~/.venv/rembg/` 中的 Python 执行

## 安装后检查

```bash
# 验证环境是否就绪
python3 setup/check_env.py

# 应该看到：
# ✓ 虚拟环境存在
# ✓ rembg 已安装
# ✓ AI 模型已下载
```
