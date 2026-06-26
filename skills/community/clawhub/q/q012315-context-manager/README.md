# Context Manager 技能

智能上下文管理系统 - 支持多模型自适应、分层记忆、动态注入、SQLite 数据库

## 快速开始

```bash
# 初始化
python3 scripts/context-manager.py --init

# 添加记忆
python3 scripts/context-manager.py --add "Gmail 邮箱已分类" --importance 0.9

# 查看统计
python3 scripts/context-manager.py --stats

# 自动管理
python3 scripts/context-manager.py --auto-manage --model "gpt-4-turbo"
```

## 文件结构

```
context-manager/
├── SKILL.md                    # 技能文档
├── README.md                   # 本文件
├── scripts/
│   └── context-manager.py      # 主脚本
└── .git/                       # Git 仓库
```

## 核心功能

- ✅ 多模型支持 (8K - 1M tokens)
- ✅ 分层记忆系统 (热/温/冷)
- ✅ SQLite 数据库
- ✅ 自适应管理策略
- ✅ 动态记忆注入
- ✅ 智能压缩

## 版本

v1.0.0 (2026-03-21)
