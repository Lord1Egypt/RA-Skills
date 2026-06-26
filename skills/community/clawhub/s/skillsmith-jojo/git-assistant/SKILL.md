---
name: git-assistant
description: |
  Git 智能助手，提供高级 Git 操作能力。
  使用场景：
  - 用户说"帮我提交代码"、"提交刚才的修改"
  - 用户说"查看仓库状态"、"现在改了什么"
  - 用户说"创建新分支"、"切换分支"
  - 用户说"看看我的改动"、"代码审查"
  - 用户说"撤销"、"回滚"、"恢复"
metadata:
  openclaw:
    emoji: "📦"
    requires:
      bins:
        - git
---

# Git 智能助手

## 使用场景

| 场景 | 命令 | 输出 |
|------|------|------|
| 智能提交 | `git-commit.py` | 生成规范的 commit message |
| 仓库状态 | `git-status.py` | 可视化状态 + 关键指标 |
| 分支管理 | `git-branch.py` | 规范命名 + 自动切换 |
| 代码审查 | `git-review.py` | diff 摘要 + 改动统计 |

## 命令详解

### git-commit.py
```bash
python scripts/git-commit.py [--all] [--message "自定义消息"]
```

### git-status.py
```bash
python scripts/git-status.py
```

### git-branch.py
```bash
python scripts/git-branch.py create feature <name>
python scripts/git-branch.py switch <branch>
```

## 分支命名规范

- feature/功能名
- fix/问题描述
- hotfix/紧急修复

## 注意事项

- 所有操作前自动备份当前状态
- 危险操作需要用户确认
- 遵循 Conventional Commits 规范
