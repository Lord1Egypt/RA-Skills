---
name: universal-file-ops
author: wUwproject
description: 为普通大模型/智能体用户提供一站式文件操作与 Python 代码质量保障能力。支持文件 CRUD、Python 代码质量流水线、沙箱测试、流程钩子系统。
tags: ['file', 'operations', 'crud', 'copy', 'move', 'delete', 'rename', 'robust', 'python', 'code-quality', 'sandbox-testing', 'error-codes', 'network-retry', 'llm-agent', 'hooks', 'process-workflow']
trigger: ['帮我规范地处理文件', '检查 Python 脚本规范', '生成测试', '帮我搭建 Python 环境', '安装 Python 包', '切换 Python 版本', '这个脚本有什么问题', '帮我 OO 化这个 Python 文件']
trigger_negative: true
data_dir: ../.standardization/universal-file-ops/
license: MIT
external_data_dir: true
audience: llm-agent
sensitive_access: false
critical_write: false
permission_weight: LOW
version: 1.3.0
h1_position: true
data_dir_compliance: true
meta_field_sync: true
---
# universal-file-ops

> **受众**：本技能专为**普通大模型/智能体用户**设计，非专业开发者。目标是让智能体能规范地使用 Python 创造工具脚本，输出即正确，无需反复调试。

## 触发场景

**正向触发词**（满足任一即触发）：
- 「帮我规范地处理文件…」「检查 Python 脚本规范」「生成测试」
- 「帮我搭建 Python 环境」「安装 Python 包」「切换 Python 版本」
- 「这个脚本有什么问题」「帮我 OO 化这个 Python 文件」

**否定条件**（满足任一项即不触发）：
- 用户明确说「只用系统 Python，不用技能」
- 任务仅需单次文件读取，无需规范化/质量保证

## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤460行），详细内容拆分到 `references/*.md` 按需加载。

1. **通用文件操作 (工具箱 B)** — 标准化 IO、**原子写入**、自动备份、错误码输出
2. **Python 脚本质量流水线 (脚本流水线 C)** — 前置规范加载 → 需求一览表 → 代码生成 → 规范化 → 审查 → OO 化建议 → 测试生成 → 沙箱执行 → 修复循环 → 终版报告
3. **Python 环境管理 (环境 A)** — 版本安装/切换/包管理/干净重装（`scripts/python_env.py`，含网络重试）
4. **脚本类型区分** — 自动识别临时脚本 vs 正式工具，临时脚本豁免 600 行 OO 化限制
5. **沙箱测试** — `py_tools.py sandbox-test` 在隔离临时 venv 中自动编译并执行测试
6. **自引用 I/O** — 所有文件写入强制通过 `text_crud.py` / `file_ops.py` 或 `utils.atomic_write()`，禁止原生 `open()`/`write()`
7. **流程钩子系统** — `scripts/hook_runner.py` 强制执行三阶段流水线，每步写状态文件，不可跳过、不可乱序
### 渐进式文件索引

| 文件名 | 位置 | 说明 |
|--------|------|------|
| `references/antipatterns.md` | 反模式 | 常见错误模式和正确做法 |
| `references/report_templates.md` | 报告模板 | A/B/C 三阶段固定报告格式 |
| `references/error_codes.md` | 错误码手册 | UFO-XXXX 全类错误码说明 |
| `references/guide.md` | 使用指南 | 完整操作教程和示例 |
| `references/faq.md` | 常见问题 | 14 对 Q&A |
| `references/py_standards.md` | Python 编码规范 | 13 节规范说明 |
| `references/permissions.md` | 权限说明 | 安全风险扫描结果 |
| `references/changelog.md` | 更新日志 | 版本更新记录 |


→ 详见 [references/guide.md](references/guide.md) 完整使用指南  
→ 反模式参见 [references/antipatterns.md](references/antipatterns.md)  
→ 常见问题参见 [references/faq.md](references/faq.md)

---


## 工作流程
1. 理解用户需求
2. 规划执行步骤
3. 调用相关工具/脚本
4. 返回结果给用户
> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。
## 三阶段架构总览

```text
┌─────────────────────────────────────────────────────────┐
│  PHASE A — 环境准备 (H-A01 ~ H-A03)                      │
│  检测 Python → 创建 venv → 安装依赖                       │
├─────────────────────────────────────────────────────────┤
│  A.1 — 语义路由 (H-A11)                                   │
│  用户意图分析 → 输出 "B" (工具箱) 或 "C" (脚本流水线)       │
├──────────┬──────────────────────────────────────────────┤
│ PHASE B  │  PHASE C                                      │
│ 工具箱    │  脚本流水线                                    │
│ H-B01~04 │  H-C01~C10 含嵌套修复循环 H-C09.1~C09.4       │
│ 读→处理→写│  规范加载→需求→生成→规整→审查→                  │
│ →验证    │  OO化→测试→沙箱→修复→报告                      │
└──────────┴──────────────────────────────────────────────┘
```

**钩子规则：**

| 规则 | 说明 |
|------|------|
| 每个钩子执行前必须 `hook_runner.py check <ID>` | 前置未完成 → 报错阻止 |
| 每个钩子执行后必须 `hook_runner.py done <ID>` | 记录完成，后置才能继续 |
| **`done` 记成功，不记好坏** | review 查到 warning、sandbox 有失败，**只要执行了就用 `done`**，结果数据写在 `--output` 里 |
| **`fail` 只用于致命错误** | 脚本找不到、环境未就绪等导致**根本无法执行**的情况才用 `fail`。一旦 `fail`，后续链路全部阻断 |
| **H-C10 是唯一例外** | 容忍前置 `failed`，路由定了就能出报告。其他钩子前置必须是 `done` |
| 不允许跳过钩子不做标记 | 每个钩子必须有一个 `done` 或 `fail` 状态 |

**故障处理两种路径：**

```text
H-C01 → H-C02 → H-C03 → H-C04 → H-C05 → H-C06 → H-C07 → H-C08 → H-C09 → H-C10
                                                                                ↑
                                                            H-C10 只认 H-A11，
                                                            不认 C/B 链上任何钩子

┌────────────────────────────────────────────────────────────────────┐
│ 步骤执行了但结果不理想（review 有 warning、sandbox 有失败）          │
│   → 用 done，--output 记录实际情况                                  │
│   → 链路继续，C09 修复循环按需启动                                  │
├────────────────────────────────────────────────────────────────────┤
│ 步骤无法执行 → 先尝试修复，而不是直接放弃                             │
│   → 用 fail 标记                                                    │
│   → 排查原因，修复问题（安装 Python、修正代码、装依赖等）               │
│   → 用 done 覆盖 fail 状态（重试通过，retry_count 自动 +1）            │
│   → 链路恢复正常                                                    │
│   → 再次 fail → 再次修复 → **最多 3 次**                             │
│   → 3 次后依然 fail → `done` 被拒绝，只能跳 H-C10 输出报告            │
├────────────────────────────────────────────────────────────────────┤
│ 怎么判断是"可修复"还是"不可修复"？                                    │
│   H-A01 detect_python 失败 → 装 Python → 重试                      │
│   H-A03 install_deps 失败  → 换镜像源 → 重试                        │
│   H-C03 generate_code 失败 → 修正模板 → 重试                        │
│   H-C08 sandbox_test 失败 → 这不属于 fail，用 done 记录结果即可       │
│   Python 解释器本身损坏 → 不可修复 → 放弃                            │
└────────────────────────────────────────────────────────────────────┘
```

---

## PHASE A — 环境准备

| 钩子 | 操作 | 说明 |
|------|------|------|
| **H-A01** | `python_env.py detect` | 检测系统已安装的 Python 版本 |
| **H-A02** | `python_env.py setup` | 创建 venv（默认 Python 3.11） |
| **H-A03** | `python_env.py install --packages ...` | 安装任务所需依赖包 |
| **H-A11** | LLM 语义分析 | 分析用户意图 → 输出 `{"route":"B"}` 或 `{"route":"C"}` |

**H-A11 路由逻辑：**
- 用户要求读/写/改/复制/移动/重命名文件 → `route: "B"`
- 用户要求创建/更新/审查/测试 Python 脚本 → `route: "C"`
- 不确定时问用户

---

## PHASE B — 工具箱（文件 CRUD）

| 钩子 | 操作 | 说明 |
|------|------|------|
| **H-B01** | `text_crud.py read` 或 `file_ops.py` | 读取源文件 |
| **H-B02** | LLM 处理/转换 | 在内存中处理数据，不写磁盘 |
| **H-B03** | `text_crud.py create/update` 或 `file_ops.py copy/move` | **原子写入**目标文件 |
| **H-B04** | `text_crud.py read` 回读 | 验证写入内容与预期一致 |

所有写操作使用 `utils.atomic_write()`（tempfile.mkstemp → `os.replace()` 原子交换），写入中断不会产生残缺文件。

---

## PHASE C — 脚本流水线

| 钩子 | 操作 | 说明 |
|------|------|------|
| **H-C01** | 读取渐进式文件索引中的编码规范 | 前置加载 13 节规范 |
| **H-C02** | 创建需求一览表 | Markdown 表格，R-001 起编 |
| **H-C03** | `text_crud.py create` 写入 `.py` | 依规范+需求表生成并写入 |
| **H-C04** | `py_tools.py normalize --fix` | 自动修复格式问题 |
| **H-C05** | `py_tools.py review` | 语法/docstring/行数/命名检查 |
| **H-C06** | `py_tools.py oo-ify` | 仅 >600 行正式工具，可选 |
| **H-C07** | `py_tools.py gen-test -o test_<target>` | 生成 pytest 框架 |
| **H-C08** | `py_tools.py sandbox-test --file --test-file` | 沙箱执行测试 |
| **H-C09** | 修复循环（见下方嵌套） | 失败时自动修复，最多 3 次 |
| **H-C10** | 输出结构化报告 | 含需求对比、修复记录、测试详情 |

**I/O 规范：** 流水线中所有文件读写必须使用技能自身脚本或 `utils.atomic_write()`。任何地方出现 `open(file, "w")` 都是不合规的。

---

### H-C09 修复循环（嵌套钩子）

sandbox-test 有 failed 或 errors 时进入此循环。每次迭代执行以下子钩子：

| 嵌套钩子 | 操作 | 说明 |
|---------|------|------|
| **H-C09.1** | 分析失败原因 | 查看 sandbox 输出，定位断言/导入/语法错误 |
| **H-C09.2** | `text_crud.py update` 修复代码 | 修复 bug，记录修了什么 |
| **H-C09.3** | `py_tools.py normalize --fix` | 重新规范化修复后的代码 |
| **H-C09.4** | `py_tools.py sandbox-test` | 重新沙箱执行 |

循环条件：
- 全部通过 → 退出循环，进 H-C10
- 仍有失败且迭代 < 3 次 → 重复 H-C09.1 → H-C09.4
- 仍有失败且迭代 ≥ 3 次 → 退出循环，进 H-C10（报告含未通过项）

---

## 输出报告模板

每次流水线执行完毕，必须输出结构化报告。详细模板见 [references/report_templates.md](references/report_templates.md)，包含模板 A（环境准备）、模板 B（工具箱）、模板 C（脚本流水线）及字段填写规则。

## 错误输出规范

所有错误均返回标准化 JSON 格式：

```json
{
  "error_code": "UFO-2001",
  "script": "scripts/py_tools.py",
  "line": 173,
  "message": "这个 Python 文件用了 Tab 缩进，标准写法是用 4 个空格",
  "suggestion": "运行 scripts/py_tools.py normalize 自动修复，或把 Tab 改成 4 个空格"
}
```

→ 完整错误码手册参见 [references/error_codes.md](references/error_codes.md)  
→ Python 编码规范参见渐进式文件索引
