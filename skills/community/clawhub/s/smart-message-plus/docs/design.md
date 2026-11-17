# smart-message-plus 方案设计文档

> 版本：v1.0.0 ｜ 语言：Python ≥ 3.9（标准库，零第三方依赖）

## 1. 定位与目标

smart-message-plus 是一个**跨平台 IM 消息发送 CLI**，通过企业自建应用向**钉钉（DingTalk）**和**飞书（Feishu / Lark）**发送消息，并支持**企业微信（WeCom）群机器人 webhook** 发送群消息。设计目标：

- **一套命令行，多个平台**：同一份 `send.py` 参数在钉钉、飞书间通用，平台差异由适配器内部消化。
- **零第三方依赖**：仅用 Python 标准库（`urllib` / `json` / `argparse` / `hashlib` / `secrets`），拷贝即用，不需要 `pip install`。
- **可运维**：多账号管理、token 缓存、联系人别名、消息模板、发送日志、`--dry-run` 预览。
- **安全可控**：分级人数门控 + 一次性审核码；凭证 600 权限、原子写、绝不进 git。

### 一条红线

**`--msg` 内容必须由用户提供，AI / Agent 禁止代拟后直接发送。** CLI 只是传输管道，不是内容生产者。唯一例外是用户明确授权、且收件人仅为用户本人的自测场景。

---

## 2. 分层架构

```
send.py                     ← CLI 主入口：参数解析、收件人解析、流程编排、门控调用
  │
  ├── core/                 ← 平台无关的通用能力
  │     config.py           数据目录定位 + 配置读写（原子写 + 600 + 深合并）
  │     accounts.py         多账号凭证管理 + token 缓存（提前 5 分钟刷新）
  │     contacts.py         联系人别名（single / members）+ 群别名
  │     http.py             stdlib HTTP（显式超时 + 429/5xx 退避重试 + multipart 上传）
  │     safety.py           人数分级门控 + 审核码（secrets 生成、内容绑定、一次性）
  │     sendlog.py          发送日志（JSONL 滚动）+ 撤回路由索引
  │     templates.py        消息模板渲染（{{var}} 占位）
  │
  └── providers/            ← 平台适配器（各自消化平台差异）
        base.py             Provider 抽象基类 + 能力矩阵 capabilities()
        dingtalk.py         钉钉适配器
        feishu.py           飞书适配器
        org_lookup.py       部门查询分发（builtin 通讯录 API / custom 自定义 HTTP）
```

**核心思路**：`send.py` 只跟抽象的 `Provider` 接口打交道，永远不写 `if provider == "dingtalk"` 这类分支来区分发送逻辑（少数平台特有的引导提示除外）。所有平台差异都被封在 `providers/*.py` 里。

---

## 3. Provider 适配器模式

### 3.1 抽象基类

`providers/base.py` 定义 `Provider` 抽象基类，约定所有平台必须实现的方法：

- 凭证与连通性：`get_token()` / `test()`
- 收件人解析：`resolve_user(raw)` → 平台原生用户 ID
- 发送：`send_p2p` / `send_group` / `send_card_p2p` / `send_card_group` / `send_image_*` / `send_file_*`
- 撤回：`recall(log_entry)`
- 建群 / 群列表：`create_group` / `list_groups`
- 组织架构：`org_resolve_department(dept_name)`

未实现的能力统一抛 `NotSupported`，由主流程转成对用户友好的报错。

### 3.2 能力矩阵

每个 Provider 用 `capabilities()` 返回一张能力表（布尔字典），例如：

```python
p2p_text=True, p2p_markdown=True, group_text=True, group_markdown=True,
image=True, file=True, mention=True, mention_all=True, recall=True,
resolve_by_mobile=True, resolve_by_email=False,   # 钉钉不支持邮箱直发
org_lookup_builtin=True, card=True, create_group=True,
```

主流程在发送前查表，能力缺失时给出明确指引，而不是发出去才失败。

### 3.3 平台能力差异速查

| | 钉钉 | 飞书 |
|--|------|------|
| 单聊收件人 | 手机号 / userId | 邮箱 / 手机号 / open_id |
| Markdown | 原生 | 通过 interactive 卡片 lark_md 渲染 |
| 图片上限 | 20MB | 10MB |
| 文件上限 | 20MB | 30MB |
| 撤回时限 | 不限时 | 24 小时内 |
| 邮箱查 ID | ❌ 不支持 | ✅ 支持（账号需绑定） |
| 群聊前提 | 机器人先进群 | 机器人先进群 |

---

## 4. 关键设计点

### 4.1 数据目录优先级

凭证、联系人、日志等运行时数据**不放在 skill 目录内**（避免升级 / 分发时泄漏或丢失），按以下优先级定位：

```
1. $SMP_DATA_DIR             （显式指定）
2. <agent workspace>/.smart-message/   （探测 workspace 目录）
3. ~/.smart-message/          （兜底）
```

目录以 `0700` 创建，敏感文件 `0600`，写入用 `tempfile.mkstemp` + `os.replace` 保证原子性。

### 4.2 收件人三级解析

`send.py` 的 `resolve_recipients()` 按顺序尝试：

1. **联系人别名**（推荐）：`张三` → 从 `contacts.json` 查对应平台的原生 ID；一个别名可存双平台 ID，`members` 类型可映射一组人。
2. **平台原生标识**：交给 `provider.resolve_user()`（钉钉手机号 / 飞书邮箱/手机号），内部调平台通讯录接口反查。
3. **解析失败**：给出可复制的维护命令（`--save-contact ...`），而不是抛晦涩错误。

> 一个细节：中文昵称如果既不是别名也不是手机号/邮箱，`resolve_user()` 会用 `not raw.isascii()` 提前拦截，直接提示"请先保存别名"，避免把中文当原生 ID 发给平台 API 得到一堆天书报错。

### 4.3 安全门控

`core/safety.py` 按收件人数量分三级（阈值可配）：

| 人数 | 行为 |
|------|------|
| ≤ warn_threshold（默认 50） | 直接发送 |
| warn ~ review（默认 51-100） | ⚠️ 抛 `GateWarn`，需 `--force-send`（退出码 3） |
| > review_threshold（默认 100） | 🔐 抛 `GateReview`，需管理员审核码（退出码 4） |

**审核码机制**：`secrets` 生成 6 位数字，写入 `approvals.json`；绑定 `(排序后的收件人集合 + 消息内容)` 的 SHA-256 前 16 位——改内容或改收件人即失效；TTL 默认 30 分钟；一次性（校验通过即删除）。审核码通过配置的管理员 DM 送达（`safety_gate.admins` 必须填直接的 userId / open_id，不允许用别名，防止死锁）。

### 4.4 撤回路由

每次成功发送都写一条 JSONL 日志（`sendlog.py`，滚动保留最近 500 条），记录 `msg_id` / provider / send_mode / chat_id 等。`--recall <MSG_ID>` 时从日志反查，据此路由到正确的平台和 p2p/group 撤回接口。

### 4.5 部门广播

`org_lookup.py` 支持两种组织架构来源：

- **builtin**（默认）：调平台通讯录 API，BFS 遍历部门树 + 分页拉成员（需通讯录读权限）。
- **custom**：配置 `org_lookup.mode=custom` + `custom_url`，按 `references/org-lookup-contract.md` 契约实现自己的查询服务；鉴权头通过环境变量 `SMP_ORG_AUTH` 注入，不写进配置文件。

### 4.6 HTTP 健壮性

`core/http.py` 是唯一的网络出口：所有请求**显式超时**（默认 15s，上传 60~120s）；对 `429 / 500 / 502 / 503 / 504` 和网络异常做退避重试；JSON 进 JSON 出，非 JSON 响应包成 `{"_raw": ...}` 不炸。multipart 上传也走 stdlib 手写，不引入 `requests`。

---

## 5. 钉钉建群的通道差异（重要坑点）

钉钉有一个绕不开的平台限制：**普通群无法通过 API 把机器人加进去**，且"场景群模板"的控制台配置页在浏览器中不可用（依赖钉钉客户端 JSAPI，普通 Chrome 打开报 `DINGTALK-JSAPI ERROR 4040: notInDingTalk`，"可选应用"下拉永远为空）。

因此 `--create-group` 对钉钉的策略是：

1. **直接建普通群**（返回 chatId）：建完即可发消息，走「应用消息通道」（`chat/send`）——支持文本 / Markdown / 图片 / 文件，但**不支持按钮卡片和撤回**。
2. **建群后自动输出提醒**：列出补加机器人能解锁的能力（按钮卡片 / 撤回 / @提醒 / @机器人触发），并给出手动添加步骤（群设置 → 机器人 → 添加，约 30 秒）和切换命令 `--save-group <别名> dingtalk <cid>`。
3. **高级路径**：如果用户手头已有可用的场景群模板 ID，`--with-bot --scene-template <ID>` 可让机器人建群即在群内（全能力）；模板 ID 会自动记住。

飞书没有这个问题：建群时机器人自动入群，全能力可用。

---

## 6. 设计取舍小结

- **为什么零依赖**：让 skill 能在任意 agent / 任意环境拷贝即用，不受目标机 pip 环境影响。
- **为什么能力矩阵 + NotSupported**：让"平台不支持"变成发送前的明确提示，而不是发送后的失败。
- **为什么审核码绑定内容**：防止"申请时发 A、拿到码后偷偷发 B"，让高危群发有据可查。
- **为什么数据目录在 skill 外**：skill 会被打包分发 / 升级覆盖，凭证放里面既危险又易丢。

---

## 7. 扩展方向

- 新增渠道（企业微信 WeCom / Slack 等）：见同目录 [`add-channel.md`](./add-channel.md)。
- 已落地：企业微信 wecom-webhook provider（v2.1，群聊消息；全能力 wecom-app 模式因企业可信 IP 政策预留，详见 references/console-setup.md）。
- 规划中：wecom-app 全能力模式、Slack provider。
