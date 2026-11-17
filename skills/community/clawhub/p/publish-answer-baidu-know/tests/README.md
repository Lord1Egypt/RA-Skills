# skill-template 测试说明（企业数字员工技能）

本目录提供面向 **ERP / TMS / WMS / 船司 / 报关 / 邮件 / 浏览器 / LLM / RPA** 等外联场景的**分层测试骨架**：默认仅内存与本地 SQLite；**真实 API / 真实 RPA** 必须显式设置 ``OPENCLAW_TEST_TARGET``，且仅以 ``*.sample`` 或复制后的文件提供范式。

复制为新技能后，请保留隔离数据根与 profile 策略，再按域扩展用例。

---

## 我该把测试写在哪里？

人类开发者与 Cursor 等 AI 工具在加用例前，先对照下表决定**文件落点**与**是否默认执行**：

| 场景 | 放在哪里 | 默认是否运行 | 说明 |
|------|----------|--------------|------|
| CLI / health / version / metadata / runtime 路径 | `tests/test_*.py` | 是 | 默认必跑，保持轻量、无外联 |
| 纯函数 / 业务规则 | `tests/test_*.py` | 是 | 不依赖真实外部系统 |
| service 层契约 | 从 `tests/samples/test_service_contract.py.sample` 复制到 `tests/test_service_contract.py` | 是，复制后 | 用 `FakeAdapter` / stub 注入外部依赖 |
| golden fixture 回归 | 从 `tests/samples/test_golden_cases.py.sample` 复制到 `tests/test_golden_cases.py` | 是，复制后 | 输入样例 + 期望输出，适合解析、计算、校验类技能 |
| 仿真 API | `tests/integration/test_simulator_api_contract.py.sample` | 否 | 复制并设置 `OPENCLAW_TEST_TARGET=simulator_api` 后按需运行 |
| 仿真 RPA / 页面操作 | `tests/integration/test_simulator_rpa_contract.py.sample` | 否 | 用 localhost / 仿真页面，不碰真实系统 |
| 真实 API | `tests/integration/test_real_api_contract.py.sample` | 否 | 必须 `OPENCLAW_TEST_TARGET=real_api` |
| 真实 RPA | `tests/integration/test_real_rpa_contract.py.sample` | 否 | 最高风险，只能手动触发 |
| 桌面宿主 E2E | `tests/desktop/test_desktop_smoke.py.sample` | 否 | 需要 pytest + `jiangchang_desktop_sdk` |

说明：`python tests/run_tests.py` **只**收集 `tests/` **根目录**下的 `test_*.py`；子目录里的 `*.sample` 与 desktop 用例**不会**被默认发现。

---

## 新技能最小测试清单

从本模板复制出新技能仓库后，建议至少逐项确认：

- [ ] `python tests/run_tests.py -v` 能通过（含 platform-kit 导入与无 vendored core 守护）。
- [ ] `python scripts/main.py health` 能通过（输出 runtime diagnostics；warning 不导致非零退出）。
- [ ] `python scripts/main.py version` 输出 JSON，且 `skill` 与目录名 / `SKILL.md` / `constants.SKILL_SLUG` 一致。
- [ ] 所有 DB / 文件写入都在 `IsolatedDataRoot`（或等价隔离）下测试，不写真实数据目录。
- [ ] 外部系统默认使用 mock / `FakeAdapter`，不访问真实 API，不打开真实 RPA。
- [ ] 至少有 1 个成功路径测试。
- [ ] 至少有 1 个缺必填字段 / 非法输入测试。
- [ ] 如果有 adapter，至少覆盖 timeout / unauthorized / invalid response（可用 fake 模拟）。
- [ ] 如果有解析 / 计算 / 校验类业务，至少保留 1 组 golden fixture（脱敏）。
- [ ] 如果技能有**特有** Python 三方依赖，`requirements.txt` 已声明且版本约束合理（尽量收窄范围）；公共依赖（platform-kit、playwright）由宿主共享 runtime 提供，**不要**写入技能 requirements。
- [ ] `health` 能在依赖缺失或原生运行库未就绪时给出清晰、可操作的错误（非裸 traceback）。
- [ ] 真实 API / 真实 RPA 测试只放 `tests/integration/`，并且默认 `.sample`，不默认运行。

---

## 1. 默认必跑（unittest）

在**技能仓库根目录**执行：

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python tests/run_tests.py
python tests/run_tests.py -v
python tests/run_tests.py cli_smoke
python tests/run_tests.py test_cli_smoke
```

### 1.1 收集范围

- ``run_tests.py`` **只**发现 ``tests/`` **根目录**下 ``test_*.py``。
- **不递归**：``tests/samples/``、``tests/integration/``、``tests/desktop/``（其中文件为 ``*.sample`` 或需 pytest 单独跑）。
- 启动时把 ``scripts/`` 与 ``tests/`` 加入 ``sys.path``。
- Windows 下将 **stdout/stderr** 包装为 **UTF-8**。

### 1.2 默认套件覆盖

| 能力 | 文件 |
|------|------|
| CLI 冒烟（import ``cli.app.main``） | ``test_cli_smoke.py`` |
| **subprocess 真实入口** ``python scripts/main.py`` | ``test_entrypoint_subprocess.py`` |
| 运行路径与 **JIANGCHANG_*** 隔离 | ``test_runtime_paths.py`` |
| ``SKILL.md`` slug 与 ``constants.SKILL_SLUG`` | ``test_skill_metadata.py`` |
| DB / ``task_logs`` 骨架冒烟 | ``test_db_smoke.py`` |
| 数据管理元数据 / 字段顺序 | ``test_display_metadata.py`` |
| 标准时间字段（Unix 秒 / trigger / 元数据） | ``test_timestamp_columns.py`` |
| **adapter profile / 外呼授权策略** | ``test_adapter_profile_policy.py`` + ``adapter_test_utils.py``（非 ``test_`` 前缀，不自动当用例收集） |
| **无 vendored ``jiangchang_skill_core``** | ``test_platform_import.py`` |
| **runtime diagnostics 架构守护** | ``test_runtime_diagnostics_integration.py`` |
| **文档/runtime 标准守护** | ``test_template_runtime_standard.py`` |
| **配置 bootstrap / config-path** | ``test_config_bootstrap.py`` |
| **health runtime diagnostics** | ``test_health_runtime.py`` |

复制为新技能后**不得删除**上述架构守护测试，除非同步更新模板标准并理解影响。

### 1.3 数据隔离（``_support.IsolatedDataRoot``）

进入同一临时目录 / 用户：

| 变量 | 值 |
|------|-----|
| ``JIANGCHANG_DATA_ROOT`` | ``tempfile.mkdtemp(prefix="skill-test-")`` |
| ``JIANGCHANG_USER_ID`` | ``_test`` |

退出时两个键均恢复（原不存在则 ``pop``），并删除临时目录。

### 1.4 产物与密钥

- ``tests/.gitignore`` 忽略 ``__pycache__``、``.pytest_cache``、``*.pyc``、``desktop/artifacts/``、``integration/artifacts/``、``.env`` 等。
- 推荐运行前设置 ``PYTHONDONTWRITEBYTECODE=1`` 减少 ``.pyc``。

---

## 2. 可选：Service / Golden（``tests/samples/*.sample``）

- 展示 **service 契约** 与 **fixture 回归** 写法；**默认不执行**。
- 启用：复制 ``tests/samples/test_service_contract.py.sample`` 等为 ``tests/test_*.py``（去掉 ``.sample``），按业务修改后再 ``python tests/run_tests.py``。
- 脱敏样例数据见 ``tests/fixtures/README.md`` 与 ``sample_request.json`` / ``expected_response.json``；profile 结构见 ``adapter_profiles.sample.yaml``。

---

## 3. 可选：Integration（``tests/integration/*.sample``）

- **默认不跑**；文件均为 ``*.py.sample``。
- 说明与开关见 **`tests/integration/README.md`**。
- **禁止**在样例中硬编码真实 token、密码、生产 URL；凭证须来自密钥库或受控环境变量。

---

## 4. 可选：Desktop E2E（pytest）

见 **`tests/desktop/README.md`**。示例为 `test_desktop_smoke.py.sample`，需复制为 `test_desktop_smoke.py` 后用 pytest 运行。

---

## 5. 环境变量：测试档位

### 5.1 测试档位

- ``OPENCLAW_TEST_TARGET``

**合法取值**（非法值将使 ``get_test_target()`` 抛 ``ValueError``）：

| 取值 | 含义 |
|------|------|
| ``unit`` | **默认**：单元 / 内存 / mock，不跑仿真与真实外联 |
| ``mock`` | 与 ``unit`` 类似的安全档位（显式语义） |
| ``simulator_api`` | 仅允许 **仿真 HTTP** 类集成（如 localhost） |
| ``simulator_rpa`` | 仅允许 **仿真页面 / 录播 RPA** |
| ``real_api`` | 真实 API（显式设 ``OPENCLAW_TEST_TARGET=real_api``） |
| ``real_rpa`` | 真实 RPA（显式设 ``OPENCLAW_TEST_TARGET=real_rpa``） |

未设置时等价 ``unit``。

### 5.2 默认安全策略（``adapter_test_utils``）

- 默认 ``unit``：不访问真实 API、不跑真实 RPA、不做写操作、不读取真实密钥、不写真实数据根。
- ``assert_no_real_network_env()`` 断言默认未误设 ``OPENCLAW_TEST_TARGET`` 为 ``real_api`` / ``real_rpa``（用于必跑用例自检）。

---

## AI 编程工具注意事项（Cursor 等）

以下约束适用于为本仓库或复制出的技能编写/修改测试时，**避免误伤业务与生产**：

- **不要为了**让测试通过去改业务代码，除非用户明确要求修改实现。
- **不要**把真实外部系统调用写进默认的 `tests/test_*.py`（默认套件须无外联、无真实浏览器）。
- **不要**把 `*.sample` 改名为可执行测试或移入根目录并去掉 `.sample`，除非用户明确要求启用 integration / 真实联调。
- **不要**硬编码真实凭证、token、cookie、生产 URL；占位请用明显虚构域名（如 `example.invalid`）或文档约定的 `credential_ref`。
- 默认测试只能使用 **mock、stub、`FakeAdapter`、fixtures、隔离 SQLite** 等安全手段。
- 业务逻辑应优先在 **service 层** 编写与测试，不要只断言 CLI 文案。
- 异常路径应返回**结构化错误**（如统一错误码/字段），避免裸异常直接穿透到 CLI。
- 有真实系统联调需求时，测试应写在 `tests/integration/`，并显式设置 ``OPENCLAW_TEST_TARGET`` 为 ``real_api`` / ``real_rpa``；不得默认开启。

---

## 6. 与 content-manager 的关系

- **未**复制 article / media / prompt / NotebookLM 等业务测试。
- 本骨架面向**通用外联技能**；业务契约请放在各自技能的 ``tests/samples`` / ``tests/integration`` 复制件中实现。
