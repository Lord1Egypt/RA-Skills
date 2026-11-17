# 测试开发指南

面向复制 `skill-template` 后的新业务 skill：**如何把自动化测试当作一等公民**，而不是等业务写完再补文档级别的空话。本文串起模板自带的 unittest 入口、`tests/` 目录分层与安全档位约定；**更细的开关取值、表格字段与环境变量组合仍以 [`tests/README.md`](../tests/README.md) 为权威来源**。建议你随手开一个编辑器分页：`TESTING.md`（本篇）、[`DEVELOPMENT.md`](DEVELOPMENT.md)（整体节奏）、[`tests/README.md`](../tests/README.md)（落地细则）。

默认心智模型可以用一句话概括：**根目录 `test_*.py` = CI / 本地每次提交都应能通过的无外联套件**；`*integration*`、`*.sample`、`desktop/` = 只在人被明确要求时才启用的高风险或重量级路径。

---

## 1. 测试体系总览

本模板把测试分成四层漏斗：**默认必跑（unittest + `run_tests.py`）**、从 `tests/samples/` **按需复制的 service / golden**、放在 `tests/integration/` **默认不落盘的仿真或真实联调范式（多数仍是 `.sample`）**、以及 **desktop E2E（pytest + 宿主 SDK）**。

[`tests/run_tests.py`](../tests/run_tests.py) 只做三件事：把 `scripts/` 与 `tests/` 放进 `sys.path`、做 Windows UTF-8 包装、收集 **`tests/` 根目录**下的 `test_*.py`。它不递归子目录——这正是刻意的安全边界：**不想让 AI 或拷贝粘贴 accidentally 把 integration 拉进默认套件**。

当你在设计一个新 skill 的测试策略时，请先问自己：**这段代码在没有外部凭证与浏览器的前提下是否有意义？** 若有，留在默认套件；若无，放进 integration / `.sample`，并要求明确的 `OPENCLAW_TEST_TARGET` 组合开关。

更深表格化的目录映射、`FakeAdapter` 与 profile 的耦合细节见 [`tests/README.md`](../tests/README.md) 开头章节『我该把测试写在哪里』。

---

## 2. 默认必跑测试要做什么

必跑套件要像一个紧张的守门员：**快、确定、离线**。典型覆盖：

- CLI：导入 [`cli.app`](../scripts/cli/app.py) 走解析链路、`health`（runtime diagnostics）/ `version` / `logs` / `log-get` 冒烟；
- 架构守护：无 `scripts/jiangchang_skill_core/`、`platform-kit>=1.0.17` 导入来源、文档/runtime 标准（见 `test_platform_import.py` 等）；
- **真实 subprocess**：[`tests/test_entrypoint_subprocess.py`](../tests/test_entrypoint_subprocess.py) 再调用一遍 `python scripts/main.py`，防路径漂移；
- 运行时：`runtime_paths` 与 **`JIANGCHANG_*` 隔离**；
- `SKILL.md` YAML slug vs [`constants.SKILL_SLUG`](../scripts/util/constants.py)；
- SQLite 骨架：`task_logs` 创建幂等与仓储读写；
- 数据管理元数据：`_jiangchang_*` 幂等初始化、中文展示名、`PRAGMA table_info` 字段顺序（见 `test_display_metadata.py`）；
- 标准时间字段：`created_at` / `updated_at` 默认值、trigger 维护与 `datetime_unix_seconds` 元数据（见 `test_timestamp_columns.py`）；
- **adapter profile**：[`tests/test_adapter_profile_policy.py`](../tests/test_adapter_profile_policy.py) + [`adapter_test_utils`](../tests/adapter_test_utils.py) ——验证在未授权情况下绝不误判开启真实网络/RPA。
- **发布打包守护**：[`tests/test_release_packaging_constraints.py`](../tests/test_release_packaging_constraints.py) ——`scripts/**/*.py` 单文件 < 1000 行、文本文件 UTF-8 without BOM。
- **slug 语义**：[`tests/test_slug_naming.py`](../tests/test_slug_naming.py) ——verb-noun-platform 命名规范校验。

**原则：`tests/test_*.py` 不允许隐形访问外网、不允许拉起真实浏览器、不允许读写开发者机器的真实数据根**。如果需要仿真服务器，也应仅在 integration（并由档位变量放行）。

套件能力与表格参见 [`tests/README.md`](../tests/README.md) 「1.2 默认套件覆盖」。

---

## 3. 数据隔离：IsolatedDataRoot

[`tests/_support.py`](../tests/_support.py) 提供的上下文管理器 `IsolatedDataRoot()`：进入一个专用临时目录，写入 `JIANGCHANG_DATA_ROOT`（tempfile）与 `JIANGCHANG_USER_ID` → `_test`。

结束时：**恢复原 environ**，删除目录。

这样可以断言：**SQLite DB / spill files / caches** 都在 sandbox；不会在开发者桌面遗留 `{REAL_ROOT}`。

示例：

```python
from _support import IsolatedDataRoot

def test_whatever():
    with IsolatedDataRoot():
        from db.connection import init_db
        init_db()
        # …断言读写均在隔离路径…
```

**不要把真实凭证路径硬编码进默认测试**：隔离不等于你有权触碰真实目录。

---

## 4. 测试目标档位（OPENCLAW_TEST_TARGET）

模板采用统一闸门：**你想跑到哪一层外部世界，就用变量明说**。合法档位（非法值会让 helper 抛错）如下——**直接摘录自 [`tests/README.md`](../tests/README.md) §5.1**：

| 取值 | 含义 |
|------|------|
| `unit` | **默认**：单元 / 内存 / mock，不跑仿真与真实外联 |
| `mock` | 与 `unit` 类似的安全档位（显式语义） |
| `simulator_api` | 仅允许 **仿真 HTTP** 类集成（如 localhost） |
| `simulator_rpa` | 仅允许 **仿真页面 / 录播 RPA** |
| `real_api` | 真实 API（显式设 `OPENCLAW_TEST_TARGET=real_api`） |
| `real_rpa` | 真实 RPA（显式设 `OPENCLAW_TEST_TARGET=real_rpa`） |

未设置环境变量 ⇒ 等价 `unit`。

默认策略摘要：**不要在 unittest 必跑路径误设 `OPENCLAW_TEST_TARGET=real_*`**。

档位读取与业务代码一致：经 `jiangchang_skill_core.config.get("OPENCLAW_TEST_TARGET")`（见 `CONFIG.md`）。

---

## 5. FakeAdapter：怎么模拟外部系统

[`tests/adapter_test_utils.py`](../tests/adapter_test_utils.py) 暴露 `FakeAdapter`，典型四种 **mode**：

| mode | 用途 |
|------|------|
| `success` | 构造干净的成功响应路径 |
| `timeout` | 模拟悬挂 / 慢链路 |
| `invalid_response` | 畸形负载 / schema drift |
| `unauthorized` | token / license / cookie 失效语义 |

**何时用它**：service 层出现『调用第三方 HTTP / RPA stub』但又不能把真实系统纳入 CI。**契约测试**（复制 [`tests/samples/test_service_contract.py.sample`](../tests/samples/test_service_contract.py.sample)）应优先组合 FakeAdapter，而不是直接把 CLI when-json 断言堆上天。

把它看成：**你把不确定性收敛到可控的测试矩阵里**，而不是在生产日志里才第一次看到错位字段。

---

## 6. 怎么从 .sample 启用一个测试

步骤模板：

1. 找到范式文件（例如 [`tests/samples/test_service_contract.py.sample`](../tests/samples/test_service_contract.py.sample)）。
2. **复制**到 `tests/` 根：`tests/test_service_contract.py`（去掉 `.sample`）。
3. 打开副本：**替换占位函数名 /技能特有枚举 / adapter profile**，删掉与本技能无关的示例断言。
4. 本地执行：`python tests/run_tests.py -v [可选筛选关键词]`。
5. **不要把 integration `.sample` 批量改名混进根目录**——除非你已经读过 [`tests/integration/README.md`](../tests/integration/README.md) 的风险清单。

Golden fixture 流程同理（[`tests/samples/test_golden_cases.py.sample`](../tests/samples/test_golden_cases.py.sample)）。

---

## 7. 真实联调测试的安全约束

任何 touching **真实租户数据** 的路径：

1. **禁止**硬编码 token / cookie / 内部域名落入仓库；
2. **禁止**默认套件隐式导入 integration；
3. **真实 RPA** 只能标记为手动触发（双人复核 / 本地 `.env` 不入库）。

范式阅读 [`tests/integration/README.md`](../tests/integration/README.md)：那里有针对凭证来源、目录 artifact 忽略策略的补充。

记住：**测试代码也是一种部署面**，别把 staging 凭证写死进仓库。

---

## 7.1 simulator_rpa 联调检查表

浏览器 RPA 走 `simulator_rpa` 档位联调前，逐项确认：

- [ ] 数据目录 `.env` 中 `OPENCLAW_TEST_TARGET=simulator_rpa`（非 `mock` / `unit`）
- [ ] account-manager：`platform ensure` + 账号 `active` + 有 `profile_dir`
- [ ] 目标 sandbox UI 已部署（跨团队；本地可用 `sandbox/demo_app.html`）
- [ ] 失败先查 `rpa-artifacts/` 截图，再查 Chrome profile 缓存（`--user-data-dir` 手工打开清站点数据）
- [ ] 默认 `python tests/run_tests.py -v` 仍全部通过（mock 离线）；example 内 `pytest` 不启真实浏览器

参考实现：`examples/simulator_browser_rpa/README.md`。

---

## 8. 新 skill 的最小测试清单

以下清单 **原文摘自 [`tests/README.md`](../tests/README.md) 「新技能最小测试清单」**（复制新仓库后逐项勾选）：

- [ ] `python tests/run_tests.py -v` 能通过。
- [ ] `python scripts/main.py health` 能通过。
- [ ] `python scripts/main.py version` 输出 JSON，且 `skill` 与目录名 / `SKILL.md` / `constants.SKILL_SLUG` 一致。
- [ ] 所有 DB / 文件写入都在 `IsolatedDataRoot`（或等价隔离）下测试，不写真实数据目录。
- [ ] 外部系统默认使用 mock / `FakeAdapter`，不访问真实 API，不打开真实 RPA。
- [ ] 至少有 1 个成功路径测试。
- [ ] 至少有 1 个缺必填字段 / 非法输入测试。
- [ ] 如果有 adapter，至少覆盖 timeout / unauthorized / invalid response（可用 fake 模拟）。
- [ ] 如果有解析 / 计算 / 校验类业务，至少保留 1 组 golden fixture（脱敏）。
- [ ] 真实 API / 真实 RPA 测试只放 `tests/integration/`，并且默认 `.sample`，不默认运行。

---

## 9. AI 编程工具使用测试时的红线

改编自 [`tests/README.md`](../tests/README.md) 「AI 编程工具注意事项」，压缩成 skill 开发者视角：

| 红线 | 解释 |
|------|------|
| 不改业务凑测试 | 除非需求变更已确认，否则**不要为了让 CI 变绿而砍掉业务分支** |
| **默认套件零外联** | 不把真实 HTTP / 浏览器写进 `tests/test_*.py` |
| `.sample` 尊重 | 集成范式改名前先读完 README；别让 `.sample` 悄悄变成根测试 |
| **零硬编码凭证** | token / cookie / 生产 URL → 用虚构域名或 vault ref |
| mock 优先 | 逻辑应在 service + FakeAdapter，而不是巨胖 CLI 断言 |
| 结构化错误 | 断言错误码字段，而不是 substring of stderr 漂移集合 |
| **integration = 显式档位** | 仅 `OPENCLAW_TEST_TARGET`（`real_*` 只放 integration / 手动触发） |

---

## 10. 测试和发布的关系

**在运行 [`release.ps1`](../release.ps1) 之前，`python tests/run_tests.py -v` 必须绿色**。失败的默认套件意味着：

- 打包路径可能根本不可运行；
- CI 加密前的静态假设可能在宿主崩溃；
- metadata slug 漂移将被市场拒绝。

把『本地 unittest 绿』视作 tag 的前置条件，而不是『有空再跑』。发布流水线成功后仍要做安装验证——那是另一个维度；**测试是第一个维度**。

---

## 11. pytest 收集卫生标准

模板根目录提供 `pytest.ini`（或等价配置），约束：

- **只收集** `test_*.py` / `*_test.py`
- **不让** `.txt`、结果文件、日志文件被 pytest 误收集
- `norecursedirs` 排除 `integration/`、`desktop/`、`samples/`、`fixtures/`、`artifacts/`、`diagnostics/`

测试结果文件**不要**放在 `tests/` 根目录；应放 `tests/artifacts/` 或 `tests/diagnostics/` 并加入 `.gitignore`。

默认 `python tests/run_tests.py` 仍只发现 `tests/` 根目录一层 `test_*.py`（不递归子目录），与 pytest 策略一致。

---

## 12. RPA / video 测试标准

- `RpaVideoSession` 调用**不跑真实 ffmpeg**：单测中使用 `unittest.mock` patch session 或设 `OPENCLAW_RECORD_VIDEO=0`。
- 断言 `title` / `closing_title` 是**中文**业务文案。
- 断言 video artifact 会进入 `result_summary`（`video_path`、`raw_video`、`video_log` 等）。
- 断言 step 文案贴近用户动作，不是技术日志（如「准备执行示例任务」而非「enter cmd_run」）。

参考 `tests/test_video_service.py`。

---

## 13. 宿主 E2E 标准

- 使用 `jiangchang_desktop_sdk.e2e_helpers`（见 `tests/desktop/` 下 `.sample`）。
- **不伪造**用户数据目录；通过宿主 IPC 获取真实 `skill_data_dir`。
- E2E **不自动生成**真实密钥或生产凭证。

---

## 14. 测试前检查清单（模板守护）

复制新 skill 或修改模板后，确认：

- [ ] `requirements.txt` **不含** `jiangchang-platform-kit` / `playwright`
- [ ] 无 `scripts/jiangchang_skill_core/` vendored 副本
- [ ] `platform_kit_min_version` **>= 1.0.17**（`SKILL.md` + `constants.py`）
- [ ] `health` 能输出 `platform_kit_version_ok`（或等价诊断行）
- [ ] `config-path` 可输出用户 `.env` 路径 JSON
- [ ] `pytest.ini` 存在且 `python_files` 只收集 `test_*.py` / `*_test.py`
- [ ] pytest **不会**误收集 `tests/` 下的 `.txt` / 日志 / 结果文件
- [ ] `python tests/run_tests.py -v` 全部通过
- [ ] `scripts/**/*.py` 单文件 < 1000 行（`test_release_packaging_constraints.py`）
- [ ] 文本文件为 UTF-8 without BOM，无 `U+FEFF`（同上）

---

- [`tests/README.md`](../tests/README.md) — 表格、变量与目录细则
- [`DEVELOPMENT.md`](DEVELOPMENT.md) §14.5 — 测试驱动的开发顺序
- [`tests/integration/README.md`](../tests/integration/README.md) — 高风险用法
