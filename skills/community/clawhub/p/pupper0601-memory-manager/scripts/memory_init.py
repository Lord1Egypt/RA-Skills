#!/usr/bin/env python3
"""
memory_init.py - 初始化三层记忆管理系统（支持多用户 + GitHub）

用法:
  # 全新初始化（在现有空仓库中）
  python scripts/memory_init.py --uid pupper

  # 从 GitHub 克隆现有仓库并加入新用户
  python scripts/memory_init.py --clone --repo-url https://github.com/owner/memory-repo \
                                  --uid pupper --github-token TOKEN

  # 仅为当前仓库添加新用户
  python scripts/memory_init.py --add-user alice --repo-dir /path/to/repo
"""

import os
import sys
import re
import subprocess
import argparse
from datetime import datetime


# ──────────────────────────────────────────
# 工具函数
# ──────────────────────────────────────────

def write_file(path, content, overwrite=False):
    if os.path.exists(path) and not overwrite:
        print(f"  ⏭️  已存在，跳过: {os.path.relpath(path)}")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ 创建: {os.path.relpath(path)}")


def is_git_repo(path):
    return os.path.exists(os.path.join(path, ".git"))


# ──────────────────────────────────────────
# 公共目录初始化
# ──────────────────────────────────────────

def init_shared(repo_dir):
    """初始化 shared/ 公共记忆目录"""
    print("\nfrom typing import List, Dict, Optional, Union, Any, Tuple\n📂 初始化公共记忆 (shared/)...")
    now = datetime.now().strftime("%Y-%m-%d")

    shared = os.path.join(repo_dir, "shared")
    permanent = os.path.join(shared, "permanent")
    os.makedirs(permanent, exist_ok=True)

    # 公共永久记忆分类
    categories = {
        "decisions": "公共决策记录",
        "projects": "项目信息与里程碑",
        "tech-stack": "技术选型与架构",
        "knowledge": "公共知识库",
    }
    for fname, desc in categories.items():
        write_file(
            os.path.join(permanent, f"{fname}.md"),
            f"# {desc}\n_最后更新: {now}_\n\n<!-- 团队共享记忆，所有成员均可读写 -->\n\n",
        )

    # 公共 INDEX
    write_file(
        os.path.join(shared, "INDEX.md"),
        f"""# Shared Memory Index
_最后更新: {now}_

## 分类目录
| 分类 | 条目数 | 最近更新 | 说明 |
|------|--------|----------|------|
| decisions | 0 | — | 公共决策 |
| projects | 0 | — | 项目信息 |
| tech-stack | 0 | — | 技术选型 |
| knowledge | 0 | — | 知识库 |

## 活跃用户
_（用户加入后自动更新）_

## 公共待办
_暂无_
""",
    )

    # SKILL_VERSION.md — 版本通知（存放在仓库根目录）
    create_skill_version(repo_dir)

    # 公共 STATS
    write_file(
        os.path.join(shared, "STATS.md"),
        f"""# Shared Memory Statistics
_最后更新: {now}_

## 概览
| 指标 | 数值 |
|------|------|
| 总条目数 | 0 |
| 活跃用户数 | 0 |
| 最后写入 | — |

## 分类统计
| 分类 | 条目数 | 最后写入者 |
|------|--------|------------|
| decisions | 0 | — |
| projects | 0 | — |
| tech-stack | 0 | — |
| knowledge | 0 | — |
""",
    )


# ──────────────────────────────────────────
# 用户目录初始化
# ──────────────────────────────────────────

def init_user(repo_dir, uid):
    """初始化 users/{uid}/ 私人目录"""
    print(f"\n👤 初始化用户私人记忆 (users/{uid}/)...")
    now = datetime.now().strftime("%Y-%m-%d")

    user_dir = os.path.join(repo_dir, "users", uid)
    dirs = ["daily", "weekly", os.path.join("permanent")]
    for d in dirs:
        os.makedirs(os.path.join(user_dir, d), exist_ok=True)

    # 私人永久记忆分类
    private_categories = {
        "decisions": "个人决策记录",
        "lessons": "经验教训与踩坑",
        "preferences": "个人偏好与工作风格",
        "people": "重要人物与关系",
    }
    for fname, desc in private_categories.items():
        write_file(
            os.path.join(user_dir, "permanent", f"{fname}.md"),
            f"# {desc}\n_最后更新: {now}_\n_用户: {uid}_\n\n",
        )

    # HABITS
    write_file(
        os.path.join(user_dir, "HABITS.md"),
        f"""# Habits & Preferences — {uid}
_最后更新: {now}_
_总观察次数: 0_

---

## 🕐 工作节奏
- **活跃时段**: _待观察_
- **会话平均时长**: _待观察_

## 💻 技术偏好
- **主要技术栈**: _待记录_
- **代码风格**: _待观察_

## 🗣️ 沟通风格
- **语言**: _待观察_
- **回答详细程度**: _待观察_
- **偏好格式**: _待观察_

## 🎯 决策模式
- **决策风格**: _待观察_

## ⚠️ 特别注意
_暂无_

---
| 日期 | 观察到的习惯 | 置信度 |
|------|-------------|--------|
""",
    )

    # INDEX
    write_file(
        os.path.join(user_dir, "INDEX.md"),
        f"""# Memory Index — {uid}
_最后更新: {now}_

## 快速摘要
| 层级 | 文件数 | 条目数 | 最近更新 |
|------|--------|--------|----------|
| L1 临时 | 0 | 0 | — |
| L2 长期 | 0 | 0 | — |
| L3 私人永久 | 0 | 0 | — |

## 未完成任务
_暂无_

## L1 临时记忆
| 日期 | 主要活动 | 条目数 |
|------|----------|--------|

## L2 长期记忆
| 周次 | 主要内容 | 条目数 |
|------|----------|--------|

## L3 私人永久记忆
| 分类 | 条目 | 更新日期 |
|------|------|----------|
| decisions | 0 | — |
| lessons | 0 | — |
| preferences | 0 | — |
| people | 0 | — |
""",
    )

    # STATS
    write_file(
        os.path.join(user_dir, "STATS.md"),
        f"""# Memory Statistics — {uid}
_最后更新: {now}_

## 总览
| 指标 | 数值 |
|------|------|
| L1 文件数 | 0 |
| L2 文件数 | 0 |
| L3 条目总数 | 0 |
| 未完成任务 | 0 |
| 最近7天活跃 | 0 条 |

## 健康度
- L1 状态: ✅ 正常
- L2 状态: ✅ 正常
- 索引状态: ✅ 最新

## 压缩历史
| 日期 | 层级 | 原行数 | 压缩后 | 压缩率 |
|------|------|--------|--------|--------|
""",
    )

    # config
    write_file(
        os.path.join(user_dir, "config.md"),
        f"""# Memory Config — {uid}
_最后修改: {now}_

## 压缩阈值
- L1 压缩触发: 150 行
- L2 压缩触发: 200 行

## 同步设置
- 自动同步: 开启
- 同步范围: all（私人+公共）

## 归档策略
- L1 超过 30 天 → 归档到 archive/
""",
    )

    # profile.md — 身份锚点文件（随 Git 同步，跨设备识别用户）
    write_file(
        os.path.join(user_dir, "profile.md"),
        f"""---
uid: {uid}
created: {now}
device_setup: local
---

# Profile — {uid}

_此文件由系统自动生成，用于跨设备识别用户身份。_
_任何设备 `git pull` 后，AI 可通过此文件确认 uid。_

## 用户信息
- **uid**: {uid}
- **加入时间**: {now}

## 设备记录
| 设备 | 初始化时间 | 说明 |
|------|------------|------|
| local | {now} | 首次初始化 |
""",
    )

    # .current_user 标记文件（本地快速读取，不入 Git）
    current_user_path = os.path.join(repo_dir, ".current_user")
    with open(current_user_path, "w", encoding="utf-8") as f:
        f.write(uid)
    print(f"  ✓ 设置当前用户: {uid}")

    # 更新 shared/INDEX.md 的活跃用户列表
    shared_index = os.path.join(repo_dir, "shared", "INDEX.md")
    if os.path.exists(shared_index):
        with open(shared_index, "r", encoding="utf-8") as f:
            content = f.read()
        if uid not in content:
            content = content.replace(
                "_（用户加入后自动更新）_",
                f"- {uid} (加入: {now})\n_（用户加入后自动更新）_",
            )
            with open(shared_index, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✓ 已将 {uid} 添加到公共索引")


# ──────────────────────────────────────────
# SKILL_VERSION.md — 版本通知文件
# ──────────────────────────────────────────

# 当前记忆系统所需的 Skill 最低版本（与 SKILL.md 的 version 字段同步）
REQUIRED_SKILL_VERSION = "3.5.0"

def create_skill_version(repo_dir):
    """创建/更新 SKILL_VERSION.md，用于提示 Skill 用户更新"""
    now = datetime.now().strftime("%Y-%m-%d")
    write_file(
        os.path.join(repo_dir, "SKILL_VERSION.md"),
        f"""---
required_skill_version: {REQUIRED_SKILL_VERSION}
last_updated: {now}
---

# Memory Manager Skill 版本要求

> 此文件由记忆系统自动维护，AI 在每次会话启动时读取并检查版本。

## 当前要求

本记忆仓库需要 **memory-manager skill >= {REQUIRED_SKILL_VERSION}**

## 如何检查本地版本

打开 `~/.workbuddy/skills/memory-manager/SKILL.md`，查看顶部 `version:` 字段。

## 如何更新 Skill

```bash
git -C ~/.workbuddy/skills/memory-manager pull
```

或访问 GitHub Release 页面手动下载：
https://github.com/Pupper0601/memory-manager/releases

## 更新历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| 3.5.0 | 2026-04-05 | 修复跨设备身份识别；新增 profile.md 身份锚点；SKILL.md 加入 uid 自动解析 + 版本检查 |
| 3.4.0 | 2026-04-04 | 关联记忆网络；重要性评分；访问日志；向量搜索综合排序 |
| 3.0.0 | 2026-04-03 | 初始发布 |
""",
        overwrite=True,
    )
    print(f"  ✓ 更新 SKILL_VERSION.md (required >= {REQUIRED_SKILL_VERSION})")


# ──────────────────────────────────────────
# .gitignore
# ──────────────────────────────────────────

def create_gitignore(repo_dir):
    write_file(
        os.path.join(repo_dir, ".gitignore"),
        """# 备份文件
*.bak
.compress_backup/

# 系统文件
.DS_Store
Thumbs.db
desktop.ini

# Python
__pycache__/
*.pyc
*.pyo
.env

# 编辑器
.vscode/
.idea/
*.swp

# 本地身份文件（每台设备独立维护，不同步）
# 注意：users/{uid}/profile.md 才是跨设备身份锚点，会同步到 Git
.current_user
.mm.json

# 向量数据库（本地生成，不同步）
.memory_vectors.db
.memory_access_log.db
.lancedb/
""",
    )


# ──────────────────────────────────────────
# README
# ──────────────────────────────────────────

def create_readme(repo_dir):
    write_file(
        os.path.join(repo_dir, "README.md"),
        """# Memory Repository

AI 三层记忆管理系统 — 多用户 · 跨设备

## 目录结构

```
shared/                     ← 公共记忆（团队共享）
├── permanent/
│   ├── decisions.md
│   ├── projects.md
│   ├── tech-stack.md
│   └── knowledge.md
├── INDEX.md
└── STATS.md

users/                      ← 私人记忆（按用户隔离）
└── {uid}/
    ├── daily/              ← L1 临时记忆
    ├── weekly/             ← L2 长期记忆
    ├── permanent/          ← L3 私人永久记忆
    ├── HABITS.md
    ├── INDEX.md
    └── STATS.md
```

## 加入方式

```bash
# 克隆仓库
git clone https://github.com/owner/memory-repo
cd memory-repo

# 初始化你的用户空间
python scripts/memory_init.py --add-user YOUR_GITHUB_USERNAME
```

## 同步命令

```bash
python scripts/memory_sync.py pull --uid YOUR_UID
python scripts/memory_sync.py push --uid YOUR_UID
python scripts/memory_sync.py status
```
""",
        overwrite=True,
    )


# ──────────────────────────────────────────
# Git 初始化和远程设置
# ──────────────────────────────────────────

def setup_git(repo_dir, repo_url=None, token=None):
    """初始化 git 并安全设置远程（不暴露 token）"""
    if not is_git_repo(repo_dir):
        subprocess.run(["git", "init", "-b", "main"], cwd=repo_dir, check=True)
        subprocess.run(
            ["git", "config", "user.email", "memory@openclaw"],
            cwd=repo_dir, check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Memory Manager Bot"],
            cwd=repo_dir, check=True,
        )
        print("  ✓ Git 仓库初始化完成")

    if repo_url:
        # 检查当前 remote
        rc = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=repo_dir, capture_output=True
        ).returncode

        if rc == 0:
            print(f"  ✓ 远程已配置，跳过")
        else:
            # 去掉 URL 中的 token（如果带了的话）
            clean_url = repo_url
            if token and f"https://{token}@" in repo_url:
                clean_url = repo_url.replace(f"{token}@", "")

            # 用 credential helper 安全存储 token（不写进 remote URL）
            if token:
                cred_file = os.path.join(repo_dir, ".git", "credentials")
                os.makedirs(os.path.dirname(cred_file), exist_ok=True)
                with open(cred_file, "w", encoding="utf-8") as f:
                    f.write(f"https://{token}@github.com\n")
                try:
                    os.chmod(cred_file, 0o600)
                except Exception:
                    pass
                subprocess.run(
                    ["git", "config", "credential.helper",
                     f"store --file {cred_file}"],
                    cwd=repo_dir, check=True,
                )

            subprocess.run(
                ["git", "remote", "add", "origin", clean_url],
                cwd=repo_dir, check=True,
            )
            print(f"  ✓ 远程已配置（token 通过 credential helper 存储）")


def initial_commit_and_push(repo_dir, uid):
    """执行首次提交并推送"""
    try:
        subprocess.run(["git", "add", "-A"], cwd=repo_dir, check=True)
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=repo_dir, capture_output=True,
        )
        if result.returncode != 0:
            subprocess.run(
                ["git", "commit", "-m", f"memory(init): 初始化记忆系统 — 用户 {uid}"],
                cwd=repo_dir, check=True,
            )
            print("  ✓ 提交完成")

        # 尝试推送
        rc = subprocess.run(
            ["git", "push", "-u", "origin", "main"],
            cwd=repo_dir, capture_output=True,
        ).returncode
        if rc == 0:
            print("  ✓ 推送到 GitHub 成功")
        else:
            print("  ⚠️  推送失败（可能需要先在 GitHub 创建仓库）")
    except Exception as e:
        print(f"  ⚠️  Git 操作失败: {e}")


# ──────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="初始化三层记忆管理系统（多用户+GitHub）")
    parser.add_argument("--uid", help="当前用户ID（GitHub 用户名）")
    parser.add_argument("--add-user", help="仅为现有仓库添加新用户")
    parser.add_argument("--repo-dir", default=".", help="本地仓库目录")
    parser.add_argument("--repo-url", help="GitHub 仓库 URL（HTTPS）")
    parser.add_argument("--clone", action="store_true", help="克隆现有仓库后初始化")
    parser.add_argument("--github-token", help="GitHub Personal Access Token")
    args = parser.parse_args()

    repo_dir = os.path.abspath(args.repo_dir)
    token = args.github_token or os.environ.get("GITHUB_TOKEN", "")

    print(f"\n🧠 三层记忆管理系统 — 初始化工具 v2.0")

    # ── 克隆模式 ──
    if args.clone and args.repo_url:
        if not os.path.exists(repo_dir) or not is_git_repo(repo_dir):
            print(f"\n⬇️  克隆仓库: {args.repo_url}")
            clone_url = args.repo_url
            if token and "https://github.com" in clone_url:
                clone_url = clone_url.replace("https://", f"https://{token}@")
            os.makedirs(os.path.dirname(repo_dir) or ".", exist_ok=True)
            subprocess.run(["git", "clone", clone_url, repo_dir], check=True)
            print(f"✅ 克隆完成: {repo_dir}")
        else:
            print(f"✅ 仓库已存在，跳过克隆: {repo_dir}")

    # ── 仅添加用户 ──
    uid = args.uid or args.add_user
    if not uid:
        # 尝试读取 .current_user
        current_user_file = os.path.join(repo_dir, ".current_user")
        if os.path.exists(current_user_file):
            with open(current_user_file, encoding="utf-8") as f:
                uid = f.read().strip()
            print(f"ℹ️  使用已有用户: {uid}")
        else:
            uid = input("请输入你的用户ID（建议使用 GitHub 用户名）: ").strip()
            if not uid:
                print("❌ 必须提供用户ID")
                sys.exit(1)

    print(f"👤 用户ID: {uid}")
    print(f"📁 仓库目录: {repo_dir}")

    os.makedirs(repo_dir, exist_ok=True)

    # ── Git 设置 ──
    if not args.clone:
        setup_git(repo_dir, args.repo_url, token)

    # ── 创建公共目录（若不存在） ──
    if not os.path.exists(os.path.join(repo_dir, "shared")):
        init_shared(repo_dir)
    else:
        print("\n📂 shared/ 目录已存在，跳过公共初始化")

    # ── 创建用户目录 ──
    user_dir = os.path.join(repo_dir, "users", uid)
    if os.path.exists(user_dir):
        print(f"\n👤 users/{uid}/ 已存在，仅更新 .current_user")
        current_user_path = os.path.join(repo_dir, ".current_user")
        with open(current_user_path, "w", encoding="utf-8") as f:
            f.write(uid)
    else:
        init_user(repo_dir, uid)

    # ── .gitignore 和 README ──
    create_gitignore(repo_dir)
    create_readme(repo_dir)

    # ── 首次提交 ──
    if not args.clone:
        initial_commit_and_push(repo_dir, uid)

    print(f"""
✅ 初始化完成！

记忆仓库结构:
{repo_dir}/
├── shared/                  ← 公共记忆（团队共享）
│   ├── permanent/
│   │   ├── decisions.md
│   │   ├── projects.md
│   │   ├── tech-stack.md
│   │   └── knowledge.md
│   ├── INDEX.md
│   └── STATS.md
└── users/
    └── {uid}/               ← 你的私人记忆空间
        ├── daily/           ← L1 临时记忆
        ├── weekly/          ← L2 长期记忆
        ├── permanent/       ← L3 私人永久记忆
        ├── HABITS.md
        ├── INDEX.md
        └── STATS.md

💡 快速上手:
  - 同步: python scripts/memory_sync.py pull --uid {uid}
  - 统计: python scripts/memory_stats.py --uid {uid} --update
  - 索引: python scripts/memory_index.py --uid {uid}

  或直接对AI说"记住这个" / "查找记忆 [关键词]"
""")


if __name__ == "__main__":
    main()
