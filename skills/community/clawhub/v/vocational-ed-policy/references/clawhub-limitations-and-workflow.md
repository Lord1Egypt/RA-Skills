# ClawHub Limitations and WSL Publishing Workflow

本文档记录 ClawHub 的系统限制和 WSL 环境下的发布工作流程。

---

## ClawHub 系统限制

### Display Name 自动生成

**现象**: 即使在 SKILL.md 中设置 `displayName` 字段，ClawHub 仍会自动生成显示名称。

**规则**:
- 显示名称基于 slug 自动生成
- 格式：将 slug 中的连字符 `-` 替换为空格，转换为首字母大写（Title Case）

**示例**:
```
Slug: voc-ed-policy         → Display: Voc Ed Policy Scraper
Slug: zhinao-vocational-policy → Display: Zhinao Vocational Policy
Slug: email-notify          → Display: Email Notify
```

**无效字段**:
- `displayName`
- `title`
- `display_name`

**例外情况**:
- `chinese-office-automation` → 显示为 "中文办公自动化"（可能是系统 Bug 或特殊处理）

### Slug 格式要求

**规则**:
```
Slug must start and end with a letter or digit,
contain only lowercase letters, digits, and single hyphens,
and not contain consecutive hyphens.
```

**示例**:
- ✅ 允许: `voc-ed-policy`, `zhinao-vocational-policy`, `email-notify`
- ❌ 不允许: `职业教育政策`, `voc--ed-policy`, `-voc-ed-policy`, `voc-ed-policy-`

### 重命名技能

**命令**:
```bash
clawhub skill rename <old-slug> <new-slug> --yes
```

**注意**:
- 新 slug 必须符合格式要求
- 旧 slug 会保留为重定向
- 仍无法改变显示名称（系统重新生成）

---

## WSL 环境发布流程

### 完整发布步骤

**1. 修改技能内容**
```bash
# 编辑 SKILL.md 或其他文件
vim ~/.hermes/skills/your-skill/SKILL.md
```

**2. 复制到 Windows 桌面**
```bash
cp -r ~/.hermes/skills/your-skill /mnt/c/Users/lenovo/Desktop/
```

**3. 使用 PowerShell 发布**
```bash
# 基本发布（自动生成 slug）
powershell.exe -Command "clawhub publish 'C:\Users\lenovo\Desktop\your-skill' --version X.X.X"

# 指定 slug 发布
powershell.exe -Command "clawhub publish 'C:\Users\lenovo\Desktop\your-skill' --slug your-slug --version X.X.X"
```

**4. 清理桌面**
```bash
rm -rf /mnt/c/Users/lenovo/Desktop/your-skill
```

### 覆盖现有技能

**场景**: 更新已发布的技能

**步骤**:
```bash
# 1. 修改版本号和内容
vim ~/.hermes/skills/your-skill/SKILL.md

# 2. 复制到桌面
cp -r ~/.hermes/skills/your-skill /mnt/c/Users/lenovo/Desktop/

# 3. 使用相同 slug 发布（自动覆盖）
powershell.exe -Command "clawhub publish 'C:\Users\lenovo\Desktop\your-skill' --slug existing-slug --version X.X.X"

# 4. 清理
rm -rf /mnt/c/Users/lenovo/Desktop/your-skill
```

### 验证发布

**查看技能信息**:
```bash
powershell.exe -Command "clawhub inspect your-slug"
```

**查看 SKILL.md 内容**:
```bash
powershell.exe -Command "clawhub inspect your-slug --file SKILL.md"
```

### 删除技能

```bash
powershell.exe -Command "clawhub delete your-slug --yes"
```

**注意**: Slug 会保留一段时间（通常到次月）后才释放。

---

## 故障排除

### Slug 冲突

**错误信息**:
```
Error: Slug redirects to an existing skill. Choose a different slug.
Existing skill: /owner/your-slug
```

**解决方案**:
- 使用 `--slug` 参数指定不同的 slug
- 或删除现有技能后重新发布

### 发布失败 - Version 格式错误

**错误信息**:
```
Error: --version must be valid semver
```

**解决方案**:
- 使用正确的 semver 格式：`X.Y.Z`（如 `1.0.0`, `1.2.0`）
- 每次发布必须提升版本号

### PowerShell 中文乱码

**现象**: PowerShell 输出中文显示乱码

**解决方案**:
- 通常不影响实际功能，可以忽略
- 如需修复，设置 PowerShell 控制台编码为 UTF-8

---

## 技能元数据字段

### 必需字段

```yaml
---
name: skill-name
description: 技能描述
category: 技能分类
version: X.Y.Z
author: 作者
tags: [tag1, tag2]
---
```

### 可选字段（对显示无影响）

```yaml
displayName: 显示名称  # 无效，系统忽略
title: 标题           # 无效，系统忽略
display_name: 显示名称 # 无效，系统忽略
```

---

## ClawHub CLI 常用命令

### 查看帮助
```bash
clawhub --help
clawhub publish --help
clawhub skill --help
```

### 技能管理
```bash
clawhub list                    # 列出已安装技能
clawhub update [slug]           # 更新技能
clawhub uninstall [slug]        # 卸载技能
clawhub inspect [slug]          # 查看技能详情
clawhub search [query]          # 搜索技能
clawhub explore                 # 浏览最新技能
```

### 技能发布
```bash
clawhub publish <path>          # 发布技能
clawhub delete [slug]           # 删除技能
clawhub skill rename <old> <new> # 重命名技能
```

---

## 版本控制建议

### 语义化版本控制

遵循 semver 规范：`MAJOR.MINOR.PATCH`

- **MAJOR**: 不兼容的 API 变更
- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的问题修复

**示例**:
- `1.0.0` → `1.0.1`: 修复 bug
- `1.0.1` → `1.1.0`: 新增功能
- `1.1.0` → `2.0.0`: 重大变更

### 变更日志（changelog）

ClawHub 支持在发布时添加变更日志：

```bash
clawhub publish 'C:\Users\lenovo\Desktop\your-skill' \
  --version 1.1.0 \
  --changelog "- 新增功能X\n- 修复问题Y\n- 提升性能Z"
```

---

## 相关技能

- `clawhub-publishing-workflow`: ClawHub 技能发布完整流程
- `external-skill-installation`: 从外部源安装技能

---

## 更新历史

- **2026-06-01**: 初始版本，记录 ClawHub 显示名称限制和 WSL 发布流程