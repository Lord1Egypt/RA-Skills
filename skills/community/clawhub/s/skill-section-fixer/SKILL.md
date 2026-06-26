---
name: skill-section-fixer
slug: skill-section-fixer
version: 2.0.0
author: WorkBuddy Autonomous System
description: "自动修复技能 SKILL.md 中缺少的必需章节（## 功能描述、## 使用示例）和 frontmatter 字段（version/author/changelog/metadata）。支持批量修复整个技能目录。"
changelog: "v2.0.0 新增批量修复模式、frontmatter字段自动补全、智能跳过已达标技能；v1.0.0 初始版本"
metadata: {"workbuddy":{"emoji":"🔧","requires":{"bins":["python"]},"os":["linux","darwin","win32"]}}
---

# 技能章节自动修复工具 (Skill Section Fixer)

## 功能描述

本技能自动检测并修复 SKILL.md 文件中缺少的必需章节和 frontmatter 字段：

### 修复内容
1. **## 功能描述** - 技能功能描述（必需）
2. **## 使用示例** - 使用示例章节（必需）
3. **frontmatter 字段** - name/version/author/description/changelog/metadata（v2.0新增）

### 模式支持
- **单技能修复**: 修复指定技能目录
- **批量修复**: 一键修复整个技能目录下所有技能（v2.0新增）
- **Dry-Run 模式**: 只检查不修改，预览修复内容（v2.0新增）
- **智能跳过**: 自动跳过已达标技能，不重复处理（v2.0新增）

适用场景：批量修复从 clawhub 安装的第三方技能，使其通过 `skill_test_runner.py` 测试。

## 使用示例

### 示例1：修复单个技能
```bash
python skill_section_fixer_v2.py "C:/Users/Administrator/.workbuddy/skills/my-skill"
```

### 示例2：批量修复整个目录（推荐）
```bash
# 修复 skills 目录下所有需要修复的技能
python skill_section_fixer_v2.py "C:/Users/Administrator/.workbuddy/skills" --batch

# 限制最多修复50个
python skill_section_fixer_v2.py "C:/Users/Administrator/.workbuddy/skills" --batch --max 50
```

### 示例3：Dry-Run 预览（不实际修改）
```bash
# 预览哪些技能需要修复
python skill_section_fixer_v2.py "C:/Users/Administrator/.workbuddy/skills" --dry-run --batch
```

### 示例4：在 AI 对话中使用
```
用户: 批量修复所有技能
助手: [调用 skill-section-fixer v2.0，一键修复全部183个技能]
```

## 快速启动

| 用户需求 | 执行操作 |
|---------|---------|
| "修复单个技能" | `python skill_section_fixer_v2.py <skill_path>` |
| "批量修复全部技能" | `python skill_section_fixer_v2.py <skills_dir> --batch` |
| "预览修复内容" | `python skill_section_fixer_v2.py <skills_dir> --dry-run --batch` |
| "限制修复数量" | `python skill_section_fixer_v2.py <skills_dir> --batch --max 50` |
| "检查技能是否完整" | 运行 `skill_test_runner.py` 验证 |

## 修复规则

### 1. 补全 frontmatter 字段（v2.0新增）

**检查字段**: name, version, author, description, changelog, metadata

**缺失时自动补全**:
```yaml
---
name: <技能目录名>
version: 1.0.0
author: "Community"
description: "<技能名> skill for WorkBuddy"
changelog: "v1.0.0 初始版本"
metadata:
  workbuddy:
    emoji: "🛠️"
    displayName: "<技能名>"
    tags: []
---
```

### 2. 添加 `## 功能描述` 章节

**位置**: frontmatter 之后

**内容模板**:
```markdown
## 功能描述

[从现有内容提取的描述，或默认描述]

主要功能包括：

- 核心功能：提供 <技能名> 相关自动化能力
- 扩展功能：支持多种使用场景
- 集成能力：与 WorkBuddy 系统深度集成

适用场景：需要根据具体技能功能补充。
```

### 3. 添加 `## 使用示例` 章节

**位置**: 文件末尾

**内容模板**:
```markdown
## 使用示例

### 示例1：基本使用
```
使用 <技能名> 技能执行相关任务
```

**助手输出：**
（根据技能功能生成相应输出）

### 示例2：进阶使用
```
使用 <技能名> 技能执行进阶任务
```

**助手输出：**
（根据技能功能生成相应输出）
```

## 安全与隐私声明

**本技能不会：**
- 删除任何现有内容
- 修改已存在的章节内容
- 访问外部 API
- 泄露用户数据

**修改范围：**
- 补全缺少的 frontmatter 字段（保留已有字段值）
- 添加缺少的 `## 功能描述` 和 `## 使用示例` 章节
- 如果内容已存在，跳过不做任何修改
- 保留所有原有内容

## 整合来源

本技能基于以下需求设计：
- `skill_test_runner.py` 测试要求（必须包含 `## 功能描述` 和 `## 使用示例`）
- 从 clawhub 安装的第三方技能普遍缺少这些章节
- 手动修复效率低，需要自动化工具

---

*🔧 技能章节自动修复工具 — 让技能测试一次通过*
