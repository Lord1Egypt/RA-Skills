# 基于skill-standardization渐进式披露规范的权限说明

本文档由 `skill-standardization` 权限扫描器自动维护。

## 风险等级

CRITICAL

## 高权限操作说明

- 操作：读取其他 skill 的 `.py`/`.md` 文件进行审计；修正被审 skill 的 SKILL.md frontmatter
- 必要性：审计检查需要读取源码；修正必须写入被审 skill
- 如何降低风险：仅读取用户指定的 skill 目录；修正前在报告中列出更新内容供用户确认

---

# 权限说明

权限扫描风险等级：**CRITICAL**

## 权限总览

本技能（skill-standardization）的核心行为是**扫描其他 skill 的权限风险**，以下列出的项目均为**检测规则**（即：本技能扫描其他 skill 时检查这些模式），不是本技能自身的行为。

共 2 类检测规则，说明如下：

### 检测规则：敏感信息访问模式（1 项）
> **规则作用**：扫描其他 skill 的代码是否访问 `~/.ssh/`、`~/.aws/`、密钥文件等敏感路径

| # | 检测模式位置（本技能内部） | 说明 |
|---|--------------------------|------|
| 1 | `scripts/skill_audit/permission_checks.py` | 字符串常量匹配敏感关键词（`credential`、`secret`、`password` 等），用于判断被审 skill 是否访问敏感信息 |

### 检测规则：子进程调用模式（5 项）
> **规则作用**：扫描其他 skill 的代码是否调用 `subprocess`、`os.system` 等子进程

| # | 检测模式位置（本技能内部） | 说明 |
|---|--------------------------|------|
| 1 | `scripts/skill_audit/permission_checks.py` | 定义 `_check_subprocess_call()` 检测函数 |
| 2 | `scripts/skill_audit/permission_checks.py` | 扫描 `import subprocess` 语句 |
| 3 | `scripts/skill_audit/permission_checks.py` | 扫描 `subprocess.run()` / `subprocess.Popen()` 调用 |
| 4 | `scripts/skill_audit/permission_checks.py` | 扫描 `os.system()` / `os.popen()` 调用 |
| 5 | `scripts/skill_audit/permission_checks.py` | 扫描 `subprocess` 字符串常量（拼接命令） |

## 本技能自身的实际权限行为

| 行为 | 说明 | 对应 frontmatter 声明 |
|------|------|----------------------|
| 读取其他 skill 的 `.py`/`.md` 文件 | 审计时读取被审 skill 的源码和文档 | `sensitive_access: true` |
| 修正被审 skill 的 `SKILL.md` frontmatter | `_apply_fixes()` 自动补全/修正字段 | `critical_write: true` |
| 执行 Python 脚本（`python scripts/...`） | 通过 Bash 工具调用自身子脚本 | `permission_weight: CRITICAL` |

## 授权方式说明

- **即时授权**：每次执行前需获得用户批准（用于子进程调用）
- **统一授权**：首次执行前获得用户批准，后续不再询问
- **静默授权**：无需用户交互，自动执行并记录

## 注意事项

本技能的 `sensitive_access: true` 和 `critical_write: true` 是指**对被审 skill 的文件有读取/修正权限**，不是指本技能自身访问用户敏感文件。

---
