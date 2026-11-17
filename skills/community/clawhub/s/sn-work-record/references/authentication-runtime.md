# 认证、凭据与运行环境

## 快速开始

> 在已安装技能目录下运行 `scripts/` 中的 Python 入口；本发布包不提供 `sn-work-record` launcher，不要假定某个 agent 的安装路径。
>
> 所有 Python 脚本现在都带运行时自检：即使误用系统 `python3` 启动，也会优先自动切换到依赖完整的解释器。也可通过环境变量 `SN_WORK_RECORD_PYTHON` 显式指定解释器路径。

### 登录（自动执行，ddddocr 闭环）
```bash
python scripts/sn_oa_login.py [--credentials PATH] [--base-url http://X.X.X.X:PORT]
```
→ 登录入口可能把 token 输出到 stdout；交互任务优先让查询/提交入口通过 `OAAuth` 自动登录并复用受保护缓存，不把 token 打印到聊天、普通日志或用 `tee` 另存明文。必须单独登录时，在权限受限的本地进程内消费结果，只向用户报告认证状态。

### 登录（agent 多模态优先，推荐）
```bash
python scripts/sn_oa_login.py --fetch-only
# → JSON：uuid / image_path / data_url，不登录
python scripts/sn_oa_login.py --submit --uuid <uuid> --code <答案>
```
→ 由使用者当前 agent 的模型识别验证码；若被服务端拒绝，自动回退 ddddocr 重新取图登录。

## 验证码识别策略（agent 多模态优先 → ddddocr 兜底）

默认顺序：

1. **取图**：`--fetch-only` 取验证码，落盘到 `~/.cache/sn-oa/captcha_latest.jpg`，同时输出 `data_url`
2. **识别**：用使用者当前 agent 的多模态能力看图（Hermes 用 `vision_analyze`），得到算术答案
3. **提交**：`--submit --uuid <uuid> --code <答案>`
4. **兜底**：提交被拒（`验证码不正确`）时脚本自动回退 ddddocr，重新取图完成登录；`--no-ddddocr-fallback` 可关闭

登录成功后 token 会自动进缓存（见下节），因此**一次识别可以覆盖后续多轮查询**。

要点：

- 验证码按 `uuid` 校验，**不绑定 HTTP 会话**——取图与提交可跨进程/跨命令（已实测）
- 接口返回的 `img` 本身就是 data URL，前缀写 `image/png`，**实际字节是 JPEG**，落盘用 `.jpg`
- 让模型只输出表达式字符，算术在本地完成更稳（末尾干扰线可能被误当成运算符）
- 只把验证码图片交给模型，**不要附带账号、密码或 token**
- 独立脚本 / cron（没有 agent loop）没有视觉通路，继续用默认 ddddocr 闭环

### 跨 agent 通用性

该流程不绑定 Hermes；任何「模型多模态 + 能把图片喂进模型」的 agent（Claude Code、Codex CLI、OpenClaw 等）都适用。差异只在第 2 步怎么把图递给模型：

- 只支持文件路径的：读 `image_path`
- 支持 data URL 的：用 `data_url`
- 没有视觉通路的：跳过第 2 步，直接用默认 ddddocr 模式

### token 缓存与自动续期（默认自动生效）

登录成功后 token 会写入缓存，后续脚本**不需要显式传 token**：

- **加密存储**：有密钥（`OA_ENC_KEY` 或 `.cache/oa_enc_key`）时写 `~/.cache/sn-oa/token.enc`（AES-256-CBC，与凭据同一套密钥）；无密钥时降级为明文 `token.json`。两者都是 0600
- **账号绑定**：缓存只存账号指纹（哈希，不落明文账号），读取时校验 `base_url` + 账号指纹，**换账号后不会误用旧会话**
- 无 `--token` 时：优先读缓存 → 未超 20 分钟 TTL 就直接复用，**跳过验证码登录**
- 缓存缺失/过期/主机或账号不符：正常登录并把新 token 写回缓存
- 任意接口返回 `401`：自动清缓存 → 重新登录 → **重试一次**

```bash
python scripts/query_fee_requests.py          # 自动复用受保护缓存，不重新登录
```

**写操作（提交/修改工时）在 401 时不会自动重试**。普通提交现在由公共底层 API 执行同日核对、本地锁、持久写入意图与提交后只读核实：完全相同的有效已提交记录直接跳过，其他同日记录停止且不覆盖；超时或未知结果仅查询，不重发。历史未核实意图也禁止再次 POST。此保护不是跨机器/客户端的服务端 exactly-once 保证。草稿真实写入暂时 fail-closed，仍可 `--save-draft --preview`。详见 [提交去重与不确定写入保护](submission-idempotency.md)。

已接入 `OAAuth` 的脚本：`query_fee_requests.py`、`query_time_entry.py`、`submit_time_entry.py`、`update_time_entry.py`、`get_time_entry_details.py`、`list_projects.py`。

> 缓存文件等同短期会话凭据（约 20 分钟有效），位于 `~/.cache/`（不在 `~/.hermes` 仓库内，不会被 git 提交）；需要强制重新登录时删掉 `~/.cache/sn-oa/token.enc` 与 `token.json` 即可。

## 凭证文件格式

存放在 `memory/sn-work-record-credentials.md`：

```markdown
# 蜀宁 OA 凭证

- **账号**: <手机号>
- **密码**: <密码>
- **Base URL**: http://<IP>:<PORT>
旧凭据中的默认项目字段只兼容读取，提交不使用；个人设置单独存储。
```

支持加密存储（`.md.enc`），使用 AES-256-CBC + openssl，密钥通过 `OA_ENC_KEY` 环境变量或 `~/.openclaw/workspace/.cache/oa_enc_key` 提供。

### 凭据留存策略

- 用户只做一次查询时，使用权限受限的临时凭据文件，完成后删除。
- 用户希望以后直接查询时，应先征得同意，再加密持久保存；后续任务不得误删持久凭据，也不要再次索要密码。
- 凭据写入后必须实际验证解密、解析和登录成功，但验证输出禁止包含账号、密码、密钥或 token。
- 账号、密码、密钥和 token 不得写入 Hermes memory 或普通日志；memory 只可记录“已配置加密凭据”及非敏感路径。
- 完整的 Hermes 存储布局、复用流程与安全边界见 [`references/hermes-credential-storage.md`](hermes-credential-storage.md)。

## 环境要求

- Python 3
- ddddocr：`pip3 install ddddocr`
- chinese_calendar：`pip3 install chinese_calendar`（用于精确判断中国工作日/节假日）
- requests：`pip3 install requests`
- 凭据文件：`memory/sn-work-record-credentials.md`（明文或 .enc 加密均可）

> 说明：脚本会优先使用依赖完整的解释器。若环境特殊，可通过 `SN_WORK_RECORD_PYTHON=/path/to/python` 显式指定解释器路径。若需要单独准备虚拟环境，推荐名称优先使用 `sn_work_record_env`（也兼容 `oa_worktime_env`、`ddddocr_env`、`.venv`、`venv` 等常见命名）。

## 维护自建驱动时的返回签名

优先复用 `query_time_ranges.py`，以下仅用于维护排错。OA 查询响应的 `fillDate` 可为 `YYYY-MM-DD 00:00:00`，不能仅凭提交使用纯日期就假定返回也相同。批量入口严格接受纯日期、已验证的午夜时间格式及周几后缀，并校验日期与查询目标一致；新增格式先补回归测试，不用任意字符串截断掩盖错日数据。模拟接口测试通过后，仍须做真实只读验证。

   自建驱动脚本（不经过 `scripts/` 入口）时，先按 `oa_utils` 的真实返回签名接数据，不要按 REST 直觉假设：
   - `load_credentials(path)` 返回**元组** `(账号, 密码, base_url)`，不是 dict；直接 `cred["base_url"]` 会抛 `TypeError: tuple indices must be integers`。
   - `query_time_entries(session, base_url, date)` 返回**元组** `(records, raw_response)`；它已在内部调用 `_ensure_ok`，所以不要再对返回值调 `_ensure_ok` 或 `.get("data")`。逐日空记录返回 `([], raw)`，属正常，不要当成查询失败。
   - 自建脚本不会被 `runtime_bootstrap` 接管，必须用依赖完整的解释器启动（技能支持探测 `sn_work_record_env` / `oa_worktime_env` / `ddddocr_env` / `.venv` / `venv`）；用系统 `python3` 会在登录阶段因 `ModuleNotFoundError: ddddocr` 反复重试后失败，而错误信息指向登录而非解释器，容易误判为账号问题。
   - 首次登录要过一次验证码，批量查询务必复用同一个 `OAAuth`（token 缓存 TTL 20 分钟），不要每天重新登录。
