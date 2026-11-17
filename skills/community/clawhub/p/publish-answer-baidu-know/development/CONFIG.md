# 配置标准：`.env` 规范与首次落盘机制

> 解决"每个 skill 每次都要手动搞一堆环境变量、账号、地址"的痛点。统一约定：**模板内置 `.env.example`，skill 首次运行自动落盘到用户数据目录，之后从那里读。**

## 核心原则

1. **三层优先级**：`进程环境变量` > `{数据目录}/.env` > 仓库 `.env.example` 默认值。
2. **`.env.example` 进仓库**：带注释的全量默认配置，是配置项的"单一事实来源"。
3. **首次运行自动 copy（bootstrap）**：`scripts/main.py` 启动与 `cli.app.main()` 均会调用 `util.config_bootstrap.bootstrap_skill_config()`，把仓库根目录 `.env.example` 复制到
   `{JIANGCHANG_DATA_ROOT}/{JIANGCHANG_USER_ID}/{slug}/.env`（**已存在则不整体覆盖**，保护用户改过的值）。
4. **技能升级合并缺失项**：`merge_missing_env_keys` 会把 `.env.example` 中新增、但用户 `.env` 尚未包含的 key **追加**进去（带注释块）。
5. **敏感信息绝不进 `.env`**：密码/密钥/口令走 account-manager 的 `secret-ref`（见下"红线"）。

## 标准配置项（`.env` 分组）

每个 skill 的 `.env.example` 至少包含这些通用项（按需增减）：

```ini
# ── 运行模式 / adapter 档位（见 ADAPTER.md）──
OPENCLAW_TEST_TARGET=mock              # mock | simulator_rpa | real_api | real_rpa

# ── 目标系统（示例占位，复制后改为业务地址）──
TARGET_BASE_URL=https://sandbox.jc2009.com

# ── 默认账号（仅非敏感标识；密码走 account-manager）──
# 浏览器 RPA simulator_rpa 联调账号来自 account-manager（platform + profile_dir），不是此处的 DEFAULT_LOGIN_ID
DEFAULT_LOGIN_ID=04110001

# ── 浏览器 / RPA ──
OPENCLAW_BROWSER_HEADLESS=0            # 0=有头(默认) 1=无头(CI)
OPENCLAW_PLAYWRIGHT_STEALTH=1          # 1=开启反检测指纹(默认)

# ── 录屏与失败存证 ──
OPENCLAW_RECORD_VIDEO=1                # 1=录屏+字幕+旁白+背景音+MP4（RPA 默认开，见 RPA.md）
OPENCLAW_ARTIFACTS_ON_FAILURE=1        # 1=失败截图(默认)

# ── 节流 / 超时 ──
STEP_DELAY_MIN=1.0
STEP_DELAY_MAX=5.0
HUMAN_WAIT_TIMEOUT=180                 # 滑块/验证码/2FA 等人工超时(秒)
```

**业务专属配置必须带技能前缀**（如 `DEMO_XXX`、`MY_SKILL_XXX`），**不要污染全局命名空间**（禁止 `SCRAPE_1688_*`、`RECEIVE_ORDER_*` 等跨技能前缀写入模板）。

## 🚫 红线：敏感信息不进 `.env`

`.env` 只放**非敏感运行参数**（模式、地址、开关、超时、账号标识）。密码、密钥、动态口令、token——

- 走 **account-manager** 注册凭据，用 `--secret-storage env --secret-ref XXX` 引用；
- 真实值由宿主/用户通过进程环境变量注入，**不落任何文件、不进 git**。

`.gitignore` 必须包含：

```gitignore
.env
*.env.local
```

## 配置 bootstrap（模板提供）

模板在 `scripts/util/config_bootstrap.py` 提供 `bootstrap_skill_config()`：

```python
from util.config_bootstrap import bootstrap_skill_config

bootstrap_skill_config()  # main.py 与 cli.app.main() 启动时调用
```

内部委托共享 runtime 的 `jiangchang_skill_core.config`：

```python
config.ensure_env_file(SKILL_SLUG, example_path)      # 首次落盘
config.merge_missing_env_keys(example_path, env_path)   # 升级后追加缺失 key
```

业务代码**只通过 `config.get*` 读配置**，不直接 `os.environ`：

```python
config.get("TARGET_BASE_URL")
config.get_bool("OPENCLAW_BROWSER_HEADLESS")
config.get_float("STEP_DELAY_MIN", 1.0)
```

## health / config-path

- **`health`**：输出 `collect_runtime_diagnostics` 字段（`platform_kit_version_ok`、`ffmpeg_path` 等），**不打印敏感值**；补充 `env_path` / `env_exists` / `example_path`。
- **`config-path`**：输出 JSON，包含 `skill`、`env_path`（用户数据目录 `.env`）、`example_path`（仓库 `.env.example` 绝对路径），便于排查落盘位置。

## doctor / setup 命令（可选）

每个 skill 可提供自检命令：

- `python scripts/main.py doctor`：检查浏览器、Profile/账号、`.env` 落盘、设备等。
- `python scripts/main.py setup`：初始化演示账号、首次落盘 `.env`。

## 相关文档

- `RPA.md` — 三端 RPA 标准与各开关含义
- `ADAPTER.md` — `OPENCLAW_TEST_TARGET` 四档模式
- `RUNTIME.md` — `JIANGCHANG_*` 环境变量与数据目录约定
