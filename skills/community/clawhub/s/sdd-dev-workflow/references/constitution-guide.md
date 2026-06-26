# 公共宪法模板指南

## 为什么需要公共宪法？

宪法是项目的通用工程原则，不应该每次新项目都从零开始。我们提供了一套公共宪法模板，可以在新项目中直接引用。

## 宪法模板位置

```
~/.openclaw/skills/sdd-dev-workflow/templates/
├── constitution-enterprise.md    # 企业级模板（推荐）
└── constitution-lite.md          # 精简模板
```

## 使用方式

### 方式 1：通过 Speckit 命令引用（推荐）

在 Claude Code 中执行：

```bash
/speckit.constitution 阅读并使用公共宪法模板 ~/.openclaw/skills/sdd-dev-workflow/templates/constitution-enterprise.md 作为当前项目的宪法
```

### 方式 2：手动复制

```bash
# 复制公共宪法到新项目
cp ~/.openclaw/skills/sdd-dev-workflow/templates/constitution-enterprise.md \
   /path/to/project/.specify/memory/constitution.md
```

### 方式 3：使用辅助脚本

```bash
# 初始化项目时指定宪法模板
~/.openclaw/skills/sdd-dev-workflow/scripts/init-project.sh my-project --constitution=enterprise
```

## 宪法模板说明

| 模板 | 文件 | 适用场景 |
|------|------|----------|
| **enterprise**（推荐） | `constitution-enterprise.md` | 企业级项目，完整严格 |
| **lite** | `constitution-lite.md` | 小型项目，精简灵活 |

> 💡 你也可以添加自己的宪法模板到 `templates/` 目录，然后在初始化时指定。

## 宪法版本管理

- 宪法使用语义化版本号：`MAJOR.MINOR.PATCH`
- 更新公共宪法模板后，所有新项目自动使用新版本
- 已有项目可选择性升级宪法

## 自定义宪法

你可以在 `templates/` 目录添加自己的宪法模板：

```bash
# 创建自定义模板
cp ~/.openclaw/skills/sdd-dev-workflow/templates/constitution-enterprise.md \
   ~/.openclaw/skills/sdd-dev-workflow/templates/constitution-myorg.md

# 编辑模板
vim ~/.openclaw/skills/sdd-dev-workflow/templates/constitution-myorg.md

# 使用自定义模板
~/.openclaw/skills/sdd-dev-workflow/scripts/init-project.sh my-project --constitution=myorg
```

## 宪法内容建议

一个完整的宪法应该包含：

1. **核心原则**（非协商）
   - 测试覆盖率要求
   - 代码规范（类型注解、命名规范）
   - 安全标准

2. **技术栈规范**（必须）
   - 编程语言版本
   - 框架选择
   - 数据库类型

3. **架构要求**（必须）
   - API 设计规范
   - 认证方式
   - 数据加密

4. **开发流程**（建议）
   - 代码审查流程
   - 提交规范
   - 测试策略
