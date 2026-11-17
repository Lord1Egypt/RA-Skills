# 适配器标准：真实/仿真 × API/RPA 四档模式

> 凡是"连接三方系统"（ERP、CRM、SaaS、银行等）的 skill，都应采用本文的 **adapter 四档模式**。这样同一套业务逻辑可以在不同档位间切换：开发用 mock、半集成用 simulator、上线用真实，互不影响。

## 为什么要分档

对接一个外部系统，工程上无非四种方式的组合：

| | API（有接口） | RPA（操作界面） |
|---|---|---|
| **真实系统** | `real_api` 真实 API | `real_rpa` 真实界面 |
| **仿真/离线** | `mock` 纯内存/fixture | `simulator_rpa` 仿真站点/桌面仿真 |

### 四档定义

| 档位 | 含义 | 默认策略 |
|------|------|----------|
| **`mock`** | 纯内存或 fixture，**默认单测/CI** | 模板 `.env.example` 默认 `OPENCLAW_TEST_TARGET=mock` |
| **`simulator_rpa`** | 仿真站点或桌面仿真，可半集成 | 开发联调可选 |
| **`real_api`** | 真实 API | 生产 / 集成测试显式设 `OPENCLAW_TEST_TARGET=real_api` |
| **`real_rpa`** | 真实浏览器/真实系统 | 生产 / 集成测试显式设 `OPENCLAW_TEST_TARGET=real_rpa` |

- **mock**：纯离线、不联网，给单测 / CI / 开发自测，**保证可重复**。
- **simulator_rpa**：操作仿真平台（如 `sandbox.jc2009.com`），跑端到端流程但不碰生产。
- **real_api**：有官方接口时**首选**（最稳、最快、最易维护）。
- **real_rpa**：没有 API 只能操作生产界面，**风险最高、放最后**。

> 推荐优先级：**real_api > simulator_rpa > real_rpa**，mock 永远保留做 CI。

配置读取见 `CONFIG.md`：**bootstrap 之后业务代码只通过 `config.get*()` 读 `OPENCLAW_TEST_TARGET` 等项**（进程 env > 用户 `.env` > `.env.example`）。

## 目录骨架

```
scripts/service/<domain>_adapter/
  __init__.py        # dispatch：按档位返回对应 adapter 实例
  base.py            # 数据契约（dataclass）+ AdapterBase 接口
  mock.py            # 离线仿真，给 CI/单测
  real_api.py        # 真实系统 API
  sim_rpa.py         # 薄仿真平台 RPA adapter（委托 *_playwright.py）
  real_rpa.py        # 真实系统 RPA（占位，谨慎实现）

scripts/service/
  <platform>_playwright.py   # RPA 主流程（厚）；与薄 sim_rpa.py 并列
  account_client.py            # account-manager subprocess 唯一封装
  browser_session.py           # async persistent context 启动
```

模板示例（均在 `examples/`，**不在** `scripts/`）：

- **仿真浏览器 RPA 完整案例**：`examples/simulator_browser_rpa/` — async mock + simulator_rpa + `simulator_playwright.py` + sandbox 页面 + adapter 分层 + 测试
- **真实浏览器 RPA 完整案例**：`examples/real_browser_rpa/` — 登录/验证码/滚动采集 + `account_client.py`
- **真实 API / 仿真 API**：`examples/real_api/`、`examples/simulator_api/` — 当前为规划占位，尚未沉淀可复制实现

复制 adapter 分层时，以修正后的 `examples/simulator_browser_rpa/`（薄 adapter + `simulator_playwright.py`）与 `examples/real_browser_rpa/scripts/service/account_client.py` 为权威参考，在新技能中创建 `scripts/service/<domain>_adapter/` 并按 README copy map 选择性复制。

> 先判断属于四象限哪一种（`real_browser_rpa` / `real_api` / `simulator_browser_rpa` / `simulator_api`），再读对应 `examples/*/README.md`。示例是**参考架构与边界**，不是业务代码原样复制。

## 档位 dispatch

由 `OPENCLAW_TEST_TARGET` 统一决定用哪个 adapter：

| `OPENCLAW_TEST_TARGET` | adapter | 用途 |
|---|---|---|
| `unit` / `mock` | `MockAdapter` | 单测 / CI，离线 |
| `simulator_rpa` | `SimRpaAdapter` | 开发/演示，操作仿真平台 |
| `real_api` | `RealApiAdapter` | 生产，走官方接口 |
| `real_rpa` | `RealRpaAdapter` | 生产，操作真实界面 |

```python
# __init__.py
from jiangchang_skill_core import config

def get_adapter():
    target = (config.get("OPENCLAW_TEST_TARGET") or "mock").lower()
    if target in ("unit", "mock"):
        return MockAdapter()
    if target == "real_api":
        return RealApiAdapter()
    if target == "real_rpa":
        return RealRpaAdapter()
    return SimRpaAdapter()
```

`get_adapter()` 实现应配合 `tests/adapter_test_utils.py` 的 profile 策略：**默认必跑测试不得误设 `OPENCLAW_TEST_TARGET=real_*`**。

## contract tests

每个 adapter **必须覆盖同一套契约测试**（复制 `tests/samples/test_service_contract.py.sample`）：

- 至少覆盖：**timeout**、**unauthorized**、**invalid response**、**empty result**
- **mock 不允许真实网络**
- 使用 `FakeAdapter` 或等价 stub 模拟异常路径

## 兄弟依赖

依赖 account-manager 或其他兄弟技能时：

1. 在 `SKILL.md` 的 `metadata.openclaw.dependencies.required` 声明。
2. **普通兄弟技能调用**，优先走统一 **`service.sibling_bridge`**（`call_sibling_json`），**不要**在 `task_service.py`、`task_rpa.py` 等业务流程文件中到处散落 `subprocess.run`。
3. **account-manager 账号/租约能力**是例外：可参考 `examples/real_browser_rpa/scripts/service/account_client.py` 与 `examples/simulator_browser_rpa/scripts/service/account_client.py`，封装为**单一** `account_client.py`；允许在该文件内部集中通过 subprocess 调 account-manager CLI。**禁止** import `rpa_helpers` 等 account-manager 内部模块；`simulator_rpa` 与 `real_rpa` 均走同一 `pick_web_account` / `release_lease` 模式。
4. **不允许**直接 `import account-manager` 的内部 Python 模块（如 `service/`、`util/`、`db/`）。
5. **pick lease 后必须 `finally release lease`**；进程被 kill 后可能残留 lease，需在运维文档说明排查方式（查 account-manager lease 列表 / 手动释放）。

```python
# 普通兄弟技能 — 走 sibling_bridge
from service.sibling_bridge import call_sibling_json

result = call_sibling_json("account-manager", ["list", "--limit", "10"])
```

```python
# account-manager 账号/租约 — 集中在 account_client.py
from service.account_client import pick_web_account, release_lease

account = pick_web_account(platform="target_platform")
try:
    ...
finally:
    release_lease(account.get("lease_token"))
```

## 相关文档

- `RPA.md` — 三端 RPA 技术选型与拟人/反反爬范式
- `CONFIG.md` — `.env` 里如何配置运行模式与目标地址
- `TESTING.md` — 测试 target 与隔离体系
