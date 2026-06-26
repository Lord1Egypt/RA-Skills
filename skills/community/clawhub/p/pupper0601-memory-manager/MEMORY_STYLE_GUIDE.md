# Memory Manager — 记忆文件使用规范 v1.0

> 制定日期: 2026-04-04
>
> 适用版本: memory-manager v3.5.0+
>
> 目的: 确保记忆文件结构整洁、内容规范、易于检索

---

## 目录

1. [目录结构规范](#1-目录结构规范)
2. [文件命名规范](#2-文件命名规范)
3. [Frontmatter 规范](#3-frontmatter-规范)
4. [内容格式规范](#4-内容格式规范)
5. [权限管理规范](#5-权限管理规范)
6. [生命周期管理](#6-生命周期管理)
7. [GitHub 同步规范](#7-github-同步规范)
8. [禁止事项](#8-禁止事项)
9. [最佳实践](#9-最佳实践)

---

## 1. 目录结构规范

```
memory-markdown/
├── shared/                    # 🟢 公共记忆（L2/L3）
│   ├── projects/              # 项目相关
│   │   ├── openclaw/          # OpenClaw 项目
│   │   ├── memory-manager/    # memory-manager 自身
│   │   └── ...
│   ├── domains/               # 领域知识
│   │   ├── tech/              # 技术笔记
│   │   ├── design/            # 设计规范
│   │   └── ...
│   ├── meta/                  # 元信息
│   │   ├── tags.md            # 标签定义
│   │   ├── people.md          # 联系人
│   │   └── glossary.md        # 术语表
│   └── archive/               # 🔒 归档（不常用）
│
└── users/                     # 🔒 用户私有记忆
    └── {uid}/
        ├── daily/             # 每日记录 (L1→L2压缩后)
        ├── projects/          # 用户个人项目
        ├── learn/             # 学习笔记
        ├── ideas/             # 灵感想法
        ├── decisions/         # 重要决策记录
        └── archive/           # 归档
```

### 目录层级限制

| 层级 | 数量限制 | 说明 |
|------|----------|------|
| `shared/` | 最多 4 个一级目录 | projects, domains, meta, archive |
| `users/{uid}/` | 最多 6 个一级目录 | daily, projects, learn, ideas, decisions, archive |
| 子目录 | 最多 3 层深度 | 避免过深嵌套 |

---

## 2. 文件命名规范

### 2.1 通用规则

```
{类型前缀}_{简短描述}_{日期/版本}.md
```

**示例**:
```
idea_openclawsync_conflict_20260404.md
decision_migration_siliconflow_v2.md
learn_rustOwnership_borrowcheck.md
```

### 2.2 类型前缀

| 前缀 | 用途 | 示例 |
|------|------|------|
| `mem_` | 一般性记忆 | `mem_meeting_summary_202604.md` |
| `idea_` | 灵感想法 | `idea_darkmode_themegen.md` |
| `dec_` | 决策记录 | `dec_techstack_python_v3.md` |
| `learn_` | 学习笔记 | `learn_rust_lifetime.md` |
| `proj_` | 项目文档 | `proj_openclaw_arch.md` |
| `ref_` | 参考资料 | `ref_tauri_docs_api.md` |
| `daily_` | 每日记录 | `daily_20260404.md` |
| `task_` | 任务追踪 | `task_ui_design_v2.md` |
| `bug_` | Bug 记录 | `bug_memoryleak_fix.md` |

### 2.3 命名限制

| 规则 | 限制 |
|------|------|
| 文件名长度 | 最大 64 字符 |
| 禁止字符 | `: / \ * ? " < > |` |
| 禁止空格 | 使用 `_` 或 `-` 替代 |
| 编码 | UTF-8 无 BOM |

### 2.4 自动命名

使用 `mm new` 命令自动生成规范文件名：

```bash
# 自动生成: idea_autosave_interval_202604041920.md
mm new idea --desc "自动保存间隔优化" --tag feature

# 自动生成: learn_react_hooks_202604.md
mm new learn --desc "React Hooks 学习" --tag frontend
```

---

## 3. Frontmatter 规范

### 3.1 必须字段

```yaml
---
type: idea              # 类型 (必须)
created: 2026-04-04     # 创建日期 YYYY-MM-DD (必须)
updated: 2026-04-04     # 更新日期 YYYY-MM-DD (必须)
tags: []                # 标签数组 (必须，至少1个)
scope: private          # 权限: public/private (必须)
---
```

### 3.2 推荐字段

```yaml
---
author: pupper           # 作者 (推荐)
status: active           # 状态: active/archived/draft
importance: 3            # 重要性 1-5 (推荐)
expires: null            # 过期日期 YYYY-MM-DD (可选)
project: openclaw       # 关联项目 (推荐)
related: []              # 关联记忆 ID 列表 (推荐)
---
```

### 3.3 字段类型说明

| 字段 | 类型 | 枚举值 | 默认值 |
|------|------|--------|--------|
| `type` | string | idea/dec/learn/ref/proj/task/mem/daily/bug | mem |
| `scope` | string | public/private | private |
| `status` | string | active/archived/draft | active |
| `importance` | int | 1-5 | 3 |
| `tags` | array | 用户自定义 | [] |

### 3.4 示例

```yaml
---
type: idea
created: 2026-04-04
updated: 2026-04-04
tags: [openclaw, feature, ui]
scope: public
author: pupper
status: active
importance: 4
project: openclaw
related: [mem_001, mem_023]
---

# 自动保存间隔优化

## 问题
当前设置需要手动保存，容易丢失未保存内容。

## 方案
- 间隔 30 秒自动保存
- 失联重试机制
- 冲突检测

## 优先级
P1 - 下一版本实现
```

---

## 4. 内容格式规范

### 4.1 Markdown 规范

| 规则 | 说明 |
|------|------|
| 标题层级 | 最多 H3 (###)，避免过深 |
| 列表嵌套 | 最多 2 层 |
| 代码块 | 必须标注语言 |
| 图片 | 使用相对路径或图床链接 |

### 4.2 内容模板

#### 灵感想法 (idea)

```markdown
---
type: idea
created: YYYY-MM-DD
tags: []
scope: public/private
importance: 1-5
---

# {简短的标题}

## 问题/背景
{描述发现的问题或背景}

## 方案/想法
{详细描述解决方案或想法}

## 可行性
{评估技术可行性和资源需求}

## 下一步
- [ ] {待办事项}
```

#### 决策记录 (dec)

```markdown
---
type: dec
created: YYYY-MM-DD
tags: []
scope: public
importance: 5
project: {项目名}
---

# {决策标题}

## 背景
{为什么要做这个决定}

## 选项分析
| 选项 | 优点 | 缺点 | 成本 |
|------|------|------|------|
| A | ... | ... | ... |
| B | ... | ... | ... |

## 最终决定
{选择哪个方案，为什么}

## 后果
- 收益: ...
- 风险: ...

## 回滚计划
{如果失败如何回退}
```

#### 学习笔记 (learn)

```markdown
---
type: learn
created: YYYY-MM-DD
tags: []
scope: private
project: {可选}
---

# {学习主题}

## 核心概念
{1-3 句话概括}

## 关键要点
1. {要点1}
2. {要点2}
3. {要点3}

## 示例代码
```language
// 代码示例
```

## 常见误区
- {误区1}
- {误区2}

## 延伸阅读
- [链接/书籍/视频]

## 实践项目
{用这个知识做了什么}
```

### 4.3 每日记录 (daily)

```markdown
---
type: daily
created: YYYY-MM-DD
scope: private
tags: []
---

# {日期} 日报

## 今日完成
- [x] {任务1}
- [x] {任务2}

## 进行中
- [ ] {任务} (进度: 50%)

## 明日计划
- [ ] {任务1}
- [ ] {任务2}

## 遇到的问题
{问题描述}

## 灵感/备注
{任何值得记录的内容}
```

---

## 5. 权限管理规范

### 5.1 权限定义

| 权限 | 可见范围 | 同步范围 | 适用场景 |
|------|----------|----------|----------|
| `public` | 所有团队成员 | 团队设备 | 项目规范、决策、通用知识 |
| `private` | 仅本人 | 仅本设备 | 私人笔记、密码、个人想法 |

### 5.2 权限选择原则

```python
def choose_scope(content_type: str) -> str:
    """自动建议权限"""
    public_types = {
        "proj",   # 项目文档
        "dec",    # 决策记录
        "ref",    # 参考资料
        "task",   # 任务追踪
    }
    private_types = {
        "daily",  # 每日记录
        "learn",  # 学习笔记（可选）
        "idea",   # 灵感想法（如果是通用创新可public）
        "mem",    # 一般记忆
    }

    return "public" if content_type in public_types else "private"
```

### 5.3 权限变更

- `private` → `public`: 需要审查内容，确保不包含敏感信息
- `public` → `private`: 记录原因，可能影响团队协作

---

## 6. 生命周期管理

### 6.1 记忆生命周期

```
L1 (临时) → L2 (长期) → L3 (永久)
   ↓            ↓           ↓
  <7天        7-90天        >90天
   ↓            ↓           ↓
 自动清理    自动压缩      手动归档
```

### 6.2 压缩规则

| 条件 | 触发动作 |
|------|----------|
| 访问频率 < 1次/30天 | 降低优先级 → 归档候选 |
| 重要性 < 2 且访问 < 1次/60天 | 标记为过期 |
| 超过 90 天未更新 | 自动压缩内容 |
| 超过 180 天未访问 | 移动到 archive/ |

### 6.3 归档管理

```bash
# 查看归档内容
mm archive --list

# 恢复归档
mm archive --restore {memory_id}

# 彻底删除（不可恢复）
mm archive --purge {memory_id}
```

---

## 7. GitHub 同步规范

### 7.1 分支策略

| 分支 | 用途 | 保护规则 |
|------|------|----------|
| `main` | 稳定版本 | PR 合并，禁止直接推送 |
| `sync/{device}` | 设备同步分支 | 自动创建，定期合并 |
| `archive` | 归档分支 | 仅追加，不修改 |

### 7.2 同步频率

| 记忆类型 | 同步时机 |
|----------|----------|
| L1 (临时) | 不同步，仅本地 |
| L2 (长期) | 每小时自动同步 |
| L3 (永久) | 每次修改立即同步 |

### 7.3 冲突处理

```bash
# 冲突时优先策略
priority:
  - newer         # 最新优先（默认）
  - local         # 本地优先
  - remote        # 远程优先
  - manual        # 手动合并
```

---

## 8. 禁止事项

### 🚫 绝对禁止

| 禁止项 | 原因 |
|--------|------|
| 记录密码/密钥/Token | 安全风险 |
| 记录他人隐私信息 | 法律风险 |
| 记录信用卡/身份证号 | 安全风险 |
| 创建无 tags 的记忆 | 难以检索 |
| 创建超过 10KB 的单文件 | 难以管理 |

### ⚠️ 强烈不建议

| 不建议 | 替代方案 |
|--------|----------|
| 中文英文混杂命名 | 统一使用英文或拼音 |
| 创建嵌套超过 3 层的目录 | 扁平化或重新分类 |
| 记录时效性很强的内容 | 放入 daily 而非 general |
| 使用 emoji 作为文件名开头 | 使用前缀如 `idea_` |

---

## 9. 最佳实践

### 9.1 标签系统

```yaml
# 推荐标签分类
tags:
  # 维度标签
  - dimension/tech      # 技术
  - dimension/design    # 设计
  - dimension/biz      # 业务

  # 项目标签
  - project/openclaw
  - project/memory-manager

  # 状态标签
  - status/draft
  - status/review
  - status/approved

  # 优先级标签
  - priority/p0
  - priority/p1
  - priority/p2
```

### 9.2 检索技巧

```bash
# 按标签搜索
mm search --tag "project/openclaw"

# 按类型搜索
mm search --type "idea"

# 按时间范围
mm search --after "2026-04-01" --before "2026-04-30"

# 组合搜索
mm search --tag "learn" --importance "4-5"
```

### 9.3 定期整理

建议每月执行一次：

```bash
# 1. 检查孤立文件（无关联）
mm stats --orphans

# 2. 检查过期内容
mm stats --expired

# 3. 清理临时文件
mm clean --dry-run  # 先预览
mm clean            # 确认后执行
```

---

## 附录

### A. 违规检测脚本

```python
# scripts/memory_lint.py
"""记忆文件规范检查工具"""

import os
import re
from pathlib import Path
from typing import List, Dict

class MemoryLinter:
    MAX_FILENAME_LEN = 64
    MAX_FILE_SIZE = 10 * 1024  # 10KB
    FORBIDDEN_CHARS = [':', '/', '\\', '*', '?', '"', '<', '>', '|']

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.errors: List[Dict] = []

    def check_filename(self, path: Path) -> bool:
        """检查文件名规范"""
        name = path.name

        # 长度检查
        if len(name) > self.MAX_FILENAME_LEN:
            self.errors.append({
                "file": str(path),
                "rule": "filename_length",
                "message": f"文件名超过 {self.MAX_FILENAME_LEN} 字符"
            })
            return False

        # 禁止字符检查
        for char in self.FORBIDDEN_CHARS:
            if char in name:
                self.errors.append({
                    "file": str(path),
                    "rule": "forbidden_chars",
                    "message": f"文件名包含禁止字符: {char}"
                })
                return False

        return True

    def check_frontmatter(self, content: str) -> bool:
        """检查 Frontmatter"""
        if not content.startswith('---'):
            self.errors.append({
                "rule": "missing_frontmatter",
                "message": "缺少 frontmatter"
            })
            return False

        # 检查必须字段
        required = ['type', 'created', 'tags', 'scope']
        for field in required:
            if f"{field}:" not in content[:500]:  # 只检查前500字符
                self.errors.append({
                    "rule": "missing_field",
                    "message": f"缺少必需字段: {field}"
                })
                return False

        return True

    def check_file_size(self, path: Path) -> bool:
        """检查文件大小"""
        size = path.stat().st_size
        if size > self.MAX_FILE_SIZE:
            self.errors.append({
                "file": str(path),
                "rule": "file_size",
                "message": f"文件超过 {self.MAX_FILE_SIZE/1024}KB"
            })
            return False
        return True

    def lint_all(self) -> Dict:
        """检查所有文件"""
        for md_file in self.base_path.rglob("*.md"):
            self.check_filename(md_file)
            self.check_file_size(md_file)
            with open(md_file, 'r', encoding='utf-8') as f:
                self.check_frontmatter(f.read())

        return {
            "total_files": len(list(self.base_path.rglob("*.md"))),
            "errors": self.errors,
            "passed": len(self.errors) == 0
        }
```

### B. 命令行工具集成

```bash
# 在 mm.py 中添加 lint 命令
mm lint              # 检查所有文件
mm lint --fix        # 自动修复可修复的问题
mm lint --format     # 格式化 frontmatter
```

---

## 变更记录

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v1.0 | 2026-04-04 | 初始版本 |
