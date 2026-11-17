# integration（可选集成 / 真实外联）

本目录**默认不执行**：

- ``python tests/run_tests.py`` 只收集 ``tests/`` 根目录下 ``test_*.py``，**不会**进入本目录。
- 本目录下文件一律为 ``*.py.sample``，pytest / unittest **默认也不会**按普通 ``test_*.py`` 收集。

## 与 samples 的区别

| 维度 | `tests/samples/` | `tests/integration/` |
|------|------------------|------------------------|
| 目的 | 默认可**升级**为根目录 `test_*.py` 的 **业务单元 / service 契约 / golden** 范式 | **外联联调**范式：网络、浏览器、仿真或真实系统 |
| 默认执行 | `.sample` 不执行；复制到根目录并改名后才进入默认套件 | **永远不**作为默认 unittest 的一部分；复制后仍需显式环境变量与手动/CI 任务触发 |
| 典型内容 | `FakeAdapter`、fixture、隔离 DB | `localhost` 仿真、真实 API、真实 RPA（最高风险） |

**原则**：只要会访问**网络**、**浏览器**、**真实或仿真外部系统**，应优先放在 `integration`（并保持 `.sample` 直至团队同意启用），而不是写进默认 `tests/test_*.py`。

## 何时使用

| 场景 | 建议 ``OPENCLAW_TEST_TARGET`` | 其它条件 |
|------|------------------------------|----------|
| 本地 / CI 对接**仿真 HTTP** | ``simulator_api`` | 仿真服务如 ``http://localhost:5180`` |
| **仿真页面** / 录播 RPA | ``simulator_rpa`` | 本地页面或沙箱浏览器 profile |
| **真实 API** | ``real_api`` | **仅手动触发** |
| **真实 RPA**（最高风险） | ``real_rpa`` | **仅手动触发** |

## 环境变量（与 ``adapter_test_utils`` 一致）

- **目标档位**：``OPENCLAW_TEST_TARGET``  
  取值：``unit`` | ``mock`` | ``simulator_api`` | ``simulator_rpa`` | ``real_api`` | ``real_rpa``  
  默认未设置等价于 ``unit``。

## 安全约束

- **禁止**在样例或复制后的测试代码中硬编码真实账号、密码、token、cookie、生产 URL。
- 凭证应来自**平台密钥库**、受控环境变量或本机安全配置（``.env`` 已列入 ``tests/.gitignore``，勿提交）。
- 真实 RPA 可能对 ERP/TMS/WMS 等产生真实操作；**务必**沙箱账号、只读权限，并由人工触发 CI job。

## 如何运行某个样例

1. 将目标 ``*.sample`` 复制为 ``test_*.py``（去掉 ``.sample``）。
2. 按技能修改其中的占位 URL / 路由 / 断言。
3. 使用 **pytest** 指向该文件（或整目录），并导出上表所需环境变量。

```powershell
$env:OPENCLAW_TEST_TARGET = "simulator_api"
pytest tests/integration/test_simulator_api_contract.py -v
```
