# 基于 skill-standardization 渐进式披露规范的权限说明

本文档由 `skill-standardization` 权限扫描器自动维护。

## 风险等级

**MEDIUM**（实际权重: 0.3）

## 权限总览

| 权限类别 | 涉及项数 | 风险等级 |
|-----------|----------|----------|
| `subprocess_call` | 38 项 | 🔴 HIGH |
| `file_delete` | 5 项 | 🔴 HIGH |
| `network_access` | 0 项 | ✅ LOW |
| `sensitive_access` | 0 项 | ✅ LOW |
| `critical_write` | 0 项 | ✅ LOW |

## 高权限操作说明

- **子进程调用（subprocess）**（38 项，unified）

- **文件删除**（5 项，unified）


## 权限详细说明

### 子进程调用（subprocess）（38 项）

> **功能说明**：技能需要通过 subprocess/操作系统调用来执行外部命令或脚本。
> **授权方式**：unified

| 文件 | 行号 | 匹配内容 | 功能说明 |
|------|------|----------|----------|
| `scripts\backup.py` | 13 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\backup.py` | 27 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\backup.py` | 177 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\backup.py` | 179 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\gen_report.py` | 8 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\gen_report.py` | 19 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\gen_report.py` | 24 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\hooks.py` | 19 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\hooks.py` | 67 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\inspector.py` | 20 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\inspector.py` | 29 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\inspector.py` | 34 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\inspector.py` | 44 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\runner.py` | 17 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\s4_engine.py` | 14 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\s4_engine.py` | 22 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\s4_engine.py` | 27 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\s4_engine.py` | 37 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\scenario_engine.py` | 23 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\scenario_engine.py` | 47 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\scenario_engine.py` | 52 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\scenario_engine.py` | 62 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\scenario_engine.py` | 72 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\scenario_engine.py` | 77 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\scenario_engine.py` | 80 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\scenario_engine.py` | 400 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\scenario_engine.py` | 416 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\scenario_engine.py` | 482 | `exec(` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\scenario_engine.py` | 488 | `exec(` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\scenario_engine.py` | 538 | `exec(` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\test_engine.py` | 13 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\test_engine.py` | 30 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\test_engine.py` | 35 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\test_engine.py` | 45 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\test_engine.py` | 171 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\test_engine.py` | 187 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\timeline.py` | 54 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\timeline.py` | 161 | `subprocess` | 自动化技能：一次性授权，后续自动执行不再询问 |


### 文件删除（5 项）

> **功能说明**：技能在执行过程中需要删除临时文件或清理旧版产物。
> **授权方式**：unified

| 文件 | 行号 | 匹配内容 | 功能说明 |
|------|------|----------|----------|
| `scripts\backup.py` | 153 | `shutil.rmtree` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\hooks.py` | 994 | `os.remove` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\s4_engine.py` | 578 | `os.remove` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\s4_engine.py` | 587 | `os.remove` | 自动化技能：一次性授权，后续自动执行不再询问 |
| `scripts\test_config.py` | 824 | `os.remove` | 自动化技能：一次性授权，后续自动执行不再询问 |


### 网络访问

**无**。


### 敏感信息访问

**无**。


### 关键位置写入

**无**。


## 授权方式说明

- **immediate（即时授权）**：每次执行前需获得用户批准
- **unified（统一授权）**：首次执行前获得用户批准，后续不再询问
- **silent（静默授权）**：无需用户交互，自动执行并记录

<!-- fp:risk=MEDIUM|sensitive=0|critical_write=0|network=0|delete=5|subprocess=38|issues=43 -->
---

# 基于 skill-standardization 渐进式披露规范的权限说明

本文档由 `skill-standardization` 权限扫描器自动维护。

## 风险等级

**LOW**（声明：LOW，实际风险：LOW）

## 高权限操作说明

- 无。所有文件操作均限制在技能独立数据目录内，不涉及系统关键目录、网络监听或外部请求。

---

---

# skill-function-test — 权限说明

本文档由 `skill-standardization` 权限扫描器自动生成，描述本技能运行所需的权限及其风险等级。

## 权限总览

| 工具 | 访问级别 | 风险等级 | 授权方式 | 说明 |
|------|----------|----------|----------|------|
| Read | read-only | 低 | 静默 | 读取输入文件和配置 |
| Write | write | 中 | 即时 | 写入输出结果到 `data/output/` |
| Bash | restricted | 中 | 统一 | 运行 `scripts/` 目录下的内部脚本 |

## 权限详细说明

### Read（读取）

- **用途**：读取用户输入文件、配置文件、参考数据
- **范围限制**：仅读取技能安装目录和指定输入文件，不访问系统敏感路径
- **不会读取**：系统敏感路径或凭证文件

### Write（写入）

- **用途**：将处理结果写入输出目录
- **范围限制**：仅写入 `data/output/` 目录，不写入安装目录或其他系统目录
- **文件覆盖策略**：默认不覆盖现有文件，添加 `--force` 参数可覆盖

### Bash（命令执行）

- **用途**：运行内部处理脚本
- **范围限制**：仅执行 `scripts/` 目录下的脚本，不执行用户 Shell 配置
- **不会执行**：`rm -rf /`、`curl` 外部 URL、`git` 远程操作等危险命令

## 风险缓解措施

1. **输入验证**：所有用户输入都经过格式和范围验证
2. **输出隔离**：输出文件限制在 `.standardization/skill-function-test/data/<skill>/outputs/` 目录内
3. **错误隔离**：单个文件处理失败不影响整体流程
4. **审计日志**：所有操作记录到 `.standardization/skill-function-test/data/<skill>/outputs/ops.log`

## 授权方式说明

- **即时授权**：每次执行前需获得用户批准（用于 Write 操作）
- **统一授权**：首次执行前获得用户批准，后续不再询问（用于 Bash 操作）
- **静默授权**：无需用户交互，自动执行并记录（用于 Read 操作）

---

> 本文档会在每次运行 `python -m skill_audit audit . --fix` 后自动更新。

---
