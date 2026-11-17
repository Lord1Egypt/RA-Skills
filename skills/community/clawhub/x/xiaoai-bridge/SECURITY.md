# 安全说明

## 支持的版本

| 版本 | 状态 |
|------|------|
| 1.2.x | 接收安全修复（当前版本） |
| 1.1.x | 不再支持；存在 T09 缓存目录校验缺陷 |
| 1.0.x | 禁止使用；发布包含已泄露的会话文件 |

## 1.2.x 安全审计响应

依据 ClawHub 审计（[security-audit](https://clawhub.ai/warm-winter/skills/xiaoai-bridge/security-audit)）逐条处理：

| 审计发现 | 级别 | 处理方式 |
|---|---|---|
| T09：凭据缓存接受攻击者可控目录、忽略权限失败（`scripts/lib/core.js`） | Warning | 默认目录迁出共享临时目录；目录/文件强制属主与权限校验；校验失败**默认中止（退出码 2）**；缓存文件登录前 0600 预创建、登录后复验；仅“权限无法强制/ACL 无法验证”可用 `XIAOAI_ALLOW_INSECURE_STATE_DIR=true` 显式放行 |
| 二次自查补充（硬链接、清理边界、开关语义、`.env` 注入） | — | 硬链接在 Windows/POSIX 全部拒绝；`clean` 只对当前状态目录尝试删除空目录，legacy 位置只删“像会话缓存”的文件；`check` 在不安全放行时退出码 2；`.env` 不能注入可信根与不安全开关；登录前清理未知字段/`__proto__`；登录后要求缓存非空并比对 dev/ino |
| 1.2.0 发布扫描：上游登录/轮询失败会把含 Cookie 的 axios 错误对象写入日志 | Suspicious | 1.2.1 在 CLI 入口安装 console 脱敏包装：`Cookie`/`Set-Cookie`、`passToken`、`password`、`serviceToken`、`ssecurity`、`nonce`、`MI_PASS_TOKEN`、Bearer 头、JSON/表单字段全部打码；自身状态/错误日志同样脱敏。1.2.1 版本级扫描已为 clean/benign |
| 1.2.1 发布扫描：静态分析 `suspicious.env_credential_access` ×2（入口同时读 env 并导入网络库） | Critical（启发式） | 1.2.2 把 `@mi-gpt/miot` 调用封装到 `scripts/lib/mi-client.js`（只接收配置、不读 env）；1.2.3 进一步把全部 `process.env` 读取集中到 `scripts/lib/runtime.js`，入口脚本不再直接读 env 或导入网络库，并用 manifest 测试固定两个边界 |
| Credential Access（读取 `.env` / `passToken`） | High（启发式） | 见下方“文件访问清单”；只读 `.env` 与自有 `.mi.json`，不访问 SSH/AWS/浏览器/钥匙串；`.env` 权限过宽会告警并尽力收紧到 0600 |
| Incomplete referenced artifact analysis ×15 | High（扫描限制） | `.clawhubignore` 排除 `node_modules/` 与 `test/`，发布物收敛为约 15 个 UTF-8 文本文件，扫描器可完整分析 |
| 未声明 `permissions`/`allowed-tools`，但检测到 `env` | Medium | `SKILL.md` 声明 `allowed-tools: read, write, exec, env` 与 `metadata.openclaw`（`primaryEnv`、`requires.env`、`requires.bins`、`envVars`） |
| 顶层建议：专用账号、`XIAOAI_STATE_DIR` 需私有、passToken 等同密码、保护转写日志、高危语音动作需确认 | — | 写入 `SKILL.md` 安全模型与最佳实践；`debug-fetch.js` 默认隐藏转写；文档示例不再把 stdout（含转写）重定向到日志文件 |

## 凭据模型

`MI_PASS_TOKEN`（或 `MI_PASSWORD`）等价于小米账号的登录能力，可读取设备列表与语音对话记录、控制音箱播放。

- 请使用专用账号，不要使用主账号。
- 优先使用 `passToken`，密码登录可能触发验证码与风控。
- 不要把 `.env`、`.mi.json` 提交到版本库或打包进发布物。
- 删除本地缓存**不等于撤销凭据**；如怀疑泄露，请在小米账号中心退出所有登录、修改密码并更换 passToken。

## 文件访问清单

运行时只读取以下文件：

| 路径 | 用途 | 说明 |
|---|---|---|
| `scripts/.env` 或技能根目录 `.env`，或 `XIAOAI_ENV_FILE` 指定路径 | 读取 MI_* 配置 | POSIX 下可被同组/他人修改时直接拒绝；仅“可读”过宽时告警并收紧到 0600。`.env` 不能设置 `LOCALAPPDATA`/`APPDATA`/`USERPROFILE`/`HOME`/`XDG_STATE_HOME`/`ProgramData`/`PUBLIC`/`SystemRoot`/`windir`/`TEMP`/`TMP`/`TMPDIR`/`XIAOAI_ALLOW_INSECURE_STATE_DIR`，这些安全敏感变量只接受进程环境 |
| `<XIAOAI_STATE_DIR>/.mi.json` | 复用/写入小米会话 | 该文件由本 Skill 以 0600 预创建，登录后复验；内容限制为已知服务键，未知字段与 `__proto__` 会被清理 |

**不会**读取 SSH 私钥、AWS/GCP/Azure 凭据、浏览器 Cookie/密码库、系统钥匙串、其他应用数据，也不做文件系统枚举。除小米账号接口（由锁定版本的 `@mi-gpt/miot` 发起）外不发起网络请求，不发送遥测。

## 会话缓存目录校验

> Windows 说明：POSIX 权限位在 Windows 上不可信（`fs.Stats.mode` 是合成值）。Windows 的安全判定链为：目录必须位于当前用户 profile 内 → 用系统内置 `icacls` 读取目录**真实 ACL** → 缓存文件 `.mi.json`（凭据最终所在）在登录前预创建与登录后复验时同样做 `icacls` ACL 校验。三者规则一致：把访问权授予当前用户 / `SYSTEM` / `Administrators` 之外账户（Everyone / Users / Authenticated Users 等）一律拒绝；`icacls` 不可用、输出无法解析（含无法归因的 SID 授权）时同样拒绝。**Windows 上不存在任何覆盖开关**（1.3.8）：`XIAOAI_ALLOW_INSECURE_STATE_DIR` 在 Windows 上不被读取，任何校验失败都直接中止，不存在“未经 ACL 校验就接受目录”的代码路径。该检查只读 ACL，不做任何修改；`icacls` 是运行期唯一的子进程调用。

上游依赖 `@mi-gpt/miot@1.2.2` 硬编码把会话写入 `process.cwd()/.mi.json`，内容包括 `passToken`、`serviceToken`、`ssecurity` 与设备信息。npm 上暂无新版本修复该行为，因此由本 Skill 在登录前切换工作目录并强制校验。

### 默认目录

| 平台 | 目录 |
|------|------|
| Windows | `%LOCALAPPDATA%\xiaoai-bridge` |
| macOS | `~/Library/Application Support/xiaoai-bridge` |
| Linux 等 POSIX | `$XDG_STATE_HOME/xiaoai-bridge`（需绝对路径），否则 `~/.local/state/xiaoai-bridge` |

无法确定用户主目录时直接报错，**不会**回落到 `os.tmpdir()`。

### 校验矩阵

| 检查 | 平台 | 行为 |
|---|---|---|
| 目录最后一级是符号链接 | 全部 | 中止 |
| 路径存在但不是目录 | 全部 | 中止 |
| 目录属主不是当前 uid | POSIX | 中止（无开关可绕过） |
| 目录权限宽松 | POSIX | 仅当目录为空或只含 `.mi.json` 时自动 `chmod 0700` 并复验；否则提示手动处理，不擅自修改 `$HOME` 等项目目录 |
| 目录位于公共目录/其他用户 profile（`C:\Users\Public`、`C:\Windows\Temp`、`C:\ProgramData`、`C:\Users\<其他用户>`） | Windows | 中止（无开关可绕过） |
| 目录不在用户目录内（ACL 不可验证） | Windows | 中止，除非显式开启不安全开关 |
| 登录后缓存是符号链接/非普通文件/属主异常/存在硬链接/超过 1 MiB | 全部（硬链接含 Windows NTFS） | 删除该文件并中止 |
| 登录后缓存权限宽松 | POSIX | 收紧 0600 并复验，失败则删除并中止 |
| 登录成功但缓存缺失、仍为空或无法解析 | 全部 | 中止并提示检查目录可写性/重新登录 |
| 登录后缓存文件 dev/ino 与预创建时不一致 | 全部 | 视为被替换，删除并中止 |

上述校验失败都以 `ConfigError` 退出（退出码 2），文案不含任何凭据内容。`node scripts/xiaoai-listen.js check` 不登录、不校验也不输出凭据；它会加载 `.env` 以取得 `XIAOAI_STATE_DIR`。目录不存在时会按 0700 创建（不含凭据）；**使用不安全开关放行时 `check` 仍返回退出码 2 并标注“不安全”**；对运行时本来会自动收紧的权限问题，`check` 也保守返回 2，便于先修好再运行。

已知限制：Node 没有跨平台的 ACL API，Windows 用“用户目录内”路径策略替代 ACL 逐条校验；POSIX 上的扩展 ACL 也无法读取，0700 检查不覆盖 ACL 中额外授予的权限。使用不安全开关放行共享/无权限目录时，仍存在“检查与写入之间”的竞态窗口（上游按路径写 `.mi.json`），因此该开关只应在确认没有其他可写用户的单用户环境使用。共享主机上仍应使用专用、非特权账号运行。

`XIAOAI_ALLOW_INSECURE_STATE_DIR=true` 只放宽“POSIX 权限无法强制”与“Windows 非公共目录但 ACL 无法验证”两类问题，并打印安全告警；不会绕过符号链接、非目录、属主不符、硬链接、公共目录/他人 profile、缓存为空或 dev/ino 变化等检查。该开关只接受进程环境，不能写在 `.env` 中；使用后 `check` 仍返回退出码 2。

登录前还会清理缓存里的未知顶层键与 `__proto__`/`constructor`/`prototype`，只保留 `micoapi`/`mina`/`miot` 服务键；登录后要求缓存非空且可解析，并把文件的 `dev/ino` 与预创建时比对，避免“上游没写成功却显示校验通过”或被替换文件蒙混过关。

### 清理

`node scripts/xiaoai-listen.js clean` 会删除当前状态目录的 `.mi.json`；只有当该目录为空时才删除目录本身。对旧临时目录 `os.tmpdir()/xiaoai-bridge/.mi.json`、`scripts/`、技能根目录、当前目录下的遗留 `.mi.json`，只删除“内容像小米会话缓存”（含 `passToken`/`serviceToken`/`ssecurity` 或已知服务键）的文件，且**绝不删除这些目录**；无法判定或清理失败时返回非 0。目录为符号链接时拒绝清理。

## Windows 说明

Windows 没有 POSIX uid/gid，Node 也无法直接读取 ACL，因此采用“路径必须位于当前用户目录（`%LOCALAPPDATA%`、`%APPDATA%`、用户主目录）”的策略；目录模式仅作参考。公共目录与其他用户 profile（`C:\Users\Public`、`C:\Windows\Temp`、`C:\ProgramData`、`C:\Users\<其他用户>`）一律拒绝，即使开启不安全开关也不放行。若把 `XIAOAI_STATE_DIR` 指向用户目录之外的其他位置（例如其他盘符的普通目录），默认中止，需要显式开启不安全开关并自行确认该目录的 ACL。Windows 的 NTFS 硬链接同样会被检测并拒绝。

## 关于 v1.0.0 中泄露的会话数据

v1.0.0 的发布包包含 `scripts/.mi.json`，其中有一个真实的小米账号会话（账号 ID 与设备序列号不再在此重复）。该文件已在 1.1.0 中删除，但**删除文件不等于撤销会话**：

1. 如果你是该账号的所有者，请立即在小米账号中心退出所有设备的登录并修改密码；
2. 重新获取 passToken，旧 token 视为已泄露；
3. 检查账号下是否有异常的智能家居操作或设备绑定。

其他使用者请勿使用该文件中的任何凭据；它可能早已过期，但仍属于敏感数据。

## 依赖策略

- 依赖源固定为 `https://registry.npmjs.org/`（见 `scripts/.npmrc`），禁止明文 HTTP；
- `package-lock.json` 锁定完整依赖树并校验 integrity；
- 直接依赖使用精确版本（`@mi-gpt/miot@1.2.2`、`dotenv@17.3.1`）；
- 发布包不包含 `node_modules/`（`.clawhubignore` 排除），由使用者执行 `npm ci`；
- 发布前执行 `npm ci`、`npm test` 与 `npm audit --omit=dev`，要求 0 漏洞。

## 转录与日志

- 监听模式只在 stdout 输出 JSON 行，其中 `originalText` / `text` 为语音转写；消费方不应把 stdout 落盘。
- `debug-fetch.js` 默认不打印转写，需要 `PRINT_TRANSCRIPTS=true` 才输出。
- 状态与错误日志写入 stderr。上游库在登录/轮询失败时会打印 axios 错误对象（含请求头 Cookie），因此 1.2.1 起所有 console 输出与自身状态日志都会经过 `scripts/lib/redact.js` 脱敏：`Cookie`/`Set-Cookie`、`passToken`、`password`、`serviceToken`、`ssecurity`、`nonce`、`MI_PASS_TOKEN`/`MI_PASSWORD`、Bearer 头等。
- 脱敏是尽力而为，不覆盖上游把凭据拼进任意无键名文本的情况；不要把 stderr 长期落盘。

## 第三方数据流（Jev 判定，可选）

- **默认关闭**：不配置 `JEV_API_KEY` 时，本 Skill 不存在小米接口与消费方 stdout 之外的网络发送，无任何遥测。
- **启用后的唯一第三方数据流**：配置 `JEV_API_KEY` 即表示同意把语音转写文本发送至 Jev 判定服务（默认 `https://tokenrhythm.studio`，可用 `JEV_BASE_URL` 覆盖，仅支持 https），用于「该语音是否转发给外部 AI」的判定。发送内容仅限转写文本与固定的能力边界说明文案，**不含**小米账号 ID、设备标识、passToken、本地路径或位置信息。
- **与热词模式的差异**：热词模式下只有命中 `TRIGGER_PREFIX` 的消息会进入后续处理；Jev 模式下**全部新语音转写**都会提交判定（由判定模型决定转发与否），这是显式的、已披露的数据面扩展。
- **最小化措施**：判定请求走隔离的网络客户端（不读 `process.env`）；`sk_` 平台密钥在所有日志中脱敏；判定日志只保留转写前 20 个字符；同文本判定在进程内缓存 10 分钟（上限 200 条）以减少第三方调用；请求超时可配（1–30 秒），超时请求不自动重试。
- **退出方式**：从 `.env`/进程环境移除 `JEV_API_KEY` 即完全回到热词模式；如需撤销已发送的数据，请联系 Jev 服务方（TokenRhythm）。

## 运行建议

- 使用专用、非特权系统账号运行；
- 只向该进程提供必要的环境变量；
- 不要把监听进程的 stdout 转写长期落盘；
- 定期执行 `check` 与 `clean`，并检查 `XIAOAI_STATE_DIR` 权限；
- 语音触发的高危动作（删除、支付、门锁、安防等）必须由消费方二次确认。

## 报告安全问题

请通过仓库 Issue 或发布者主页私下联系维护者，不要在公开 Issue 中粘贴 passToken、serviceToken、账号 ID 或语音转写内容。
