# 普通工时提交：提交前核对、提交后读回与不确定写入保护

## 适用范围

保护位于公共 `oa_utils.submit_time_entry()`，不是仅 CLI 增加判断。真实提交仍须先确认工作事实和用户授权；CLI 重新实时验证项目/字典，不保存单次覆盖。直接导入公共 API 同样受日期、业务字段、认证绑定、同日核对、锁和持久日志保护，但不会替调用者查询业务字典；交互提交使用统一 CLI。

草稿写入当前 **fail-closed**：`save_or_submit=0` 或不带 `--preview` 的 `--save-draft` 拒绝，不创建/更新真实草稿。`--save-draft --preview` 保持只读可用。事假等非普通工作拒绝。修改/删除 API 不在此次保护范围，不应拿它们绕过同日冲突。

## 同日处理规则

- 严格解析请求日期 `YYYY-MM-DD`，检查真实日历日期，业务代码不去空格、补零或修复格式。
- 完整且成功的当日列表只有一条记录，且日期、项目 ID/名称、填报类型、阶段、工作类型、项目/商机属性、时长和描述全部相同，`isDeleted=0`、状态为 `20` 或 `30`，返回 `submission_status=skipped-existing`，不调用写端点。
- 时长使用 `Decimal` 数值比较，`8`、`8.0`、`"8.00"` 相同；拒绝布尔、非有限值。代码只接受完整相同的字符串/整数表示，`5` 与 `"5"` 相同，但 `"05"`、`"5.0"` 不修复。
- OA 查询实际日期形式 `YYYY-MM-DD 00:00:00` 可与同日请求比较。仅允许精确午夜后缀，不截断任意时间、附注或垃圾字符。
- 同日其他记录（含其他项目）、多条记录、草稿、驳回/未知状态、逻辑删除、字段缺失等全部停止，绝不覆盖旧记录。查询失败、无 `data`、`data=null`、错误格式或显式不完整分页也停止。正常无记录必须有真实空列表 `data=[]`。

## 写入与读回

持有本地锁期间，完成查询后才能持久保存 `pending` 意图，然后 **最多一次** 调用 `saveOrUpdate`。写请求禁用 HTTP 重定向，不支持有自动重试策略的标准 requests adapter，不会自动重登重发。

无论写响应成功还是超时/网络/HTTP/应用错误，后续仅只读查询。最多三次读回，后两次各间隔 0.2 秒，用于空列表/查询失败的短暂最终一致性；不会重发 POST。只有完整字段匹配、`isDeleted=0` 且状态精确为 `20` 才返回：

- `submitted-confirmed`：写响应成功且读回已核实；
- `observed-after-uncertain`：写响应不确定，但已观察到精确匹配的已提交记录。它不证明该记录一定由本次请求创建；
- `skipped-existing`：提交前就有完全相同的有效已提交记录。

均带 `verified=true`。HTTP 200 或服务端“成功”信息本身不等于核实成功。读回观察到非空冲突/字段缺失/其他状态，立即报 `SubmissionUncertain`；空列表或查询失败耗尽次数也报结果未知。不得宣称成功或自动重发。

## 认证绑定与公共 API

`OAAuth` 创建和刷新会话时，绑定规范化 OA origin、真实账号 SHA-256 指纹和当前双认证头 token 指纹。绑定缺失、地址不同、认证头不一致或处理中身份变化，禁止写入/禁止确认成功。

已有可信认证会话的程序调用者须显式绑定真实账号（不猜 token 所属账号）：

```python
from oa_utils import OAAuth, submit_time_entry
# 首选 OAAuth(...).session；其账号绑定与缓存校验已有统一实现。

from submission_guard import bind_submission_session
bind_submission_session(session, base_url, actual_authenticated_account)
# 然后调用公共 submit_time_entry，完整提供已确认字段。
```

绑定是调用者对真实登录账号的明确断言，不是服务端身份 introspection；调用者不得把其他账号 token 绑定到错误账号。自定义 HTTP transport 必须保证单次调用不会在内部重发；受支持的真实会话是 `OAAuth` 创建的无自动重试标准 requests session。测试使用注入 HTTP fake，不代表 live 写入证据。

## 本地锁与持久日志

默认目录：`~/.local/state/sn-work-record/submission-guard/`，当前用户私有目录（0700）、常规单链接文件（0600），拒绝符号链接/宽权限/其他用户拥有的文件。`SN_WORK_RECORD_GUARD_DIR` 仅用于明确选择同一共享保护目录或隔离测试；不得用切换目录规避保护。

锁以 **规范化 OA origin + 账号指纹 + 日期** 为键，比项目范围更严格：同账号同日即使换项目也冲突。POSIX `flock` 非阻塞锁覆盖历史日志读取、提交前查询、持久意图、一次写入和读回；竞争/加锁失败立即拒绝。不删除锁文件，避免锁 inode 分裂；进程退出自动释放锁。不支持 `fcntl` 的平台拒绝写入。

日志以私有临时文件、文件 fsync、原子 replace 和父目录 fsync 保存。仅保存版本、组合 scope 摘要、完整请求摘要和 `pending/observed`，不保存主机、账号、token、项目名称、项目 ID、工时描述或服务端完整记录。请求摘要包含项目及所有工作字段；账号、项目和日期不能混用。

在 POST 前保存 `pending`，因此进程崩溃/中断后不能直接重新写入。后续调用仍只读核对；历史请求不匹配，或无法观察到与历史请求匹配的有效已提交记录，一律禁止新 POST。确认后标记 `observed` 而非删除日志；以后记录消失，也不会自动重发。明确的提交前输入/查询/冲突失败不留下 `pending`。日志损坏、权限错误、持久化失败均停止。此保守策略可能让“尚未发出 POST 就崩溃”的日期暂时被锁定，需要人工核实；没有自动日志清除/强制重发入口。

**这不是服务端通用 exactly-once 保证。** 不同机器/用户/保护目录、OA 地址别名、其他客户端或绕过公共 API 的操作不共享本地锁；服务端未提供幂等键或事务式日期唯一约束。外部客户端可能在查询与写入之间竞争。日志保留依赖本地文件系统和 fsync 正确性，删除/丢失日志会削弱保护。不要宣称跨主机严格只执行一次。

## 验证与证据

通过 `terminal` 在技能目录运行：

```text
python -m unittest discover -s tests -v
```

使用依赖完整的既有解释器。单元测试全部离线，HTTP fake 明确标记为模拟；覆盖重复、同日冲突、草稿/驳回/删除/缺字段、失败/不完整查询、严格日期/代码/时长、写后核对、超时无重发、持久意图、中断恢复、私有日志、跨进程锁和认证绑定。

`tests/live_duplicate_readonly.py` 是**需显式运行的 live 只读验证工具**，不会由 unittest 自动执行。仅针对用户明确授权的既有记录，参数用实际已确认项目/描述：

```text
python tests/live_duplicate_readonly.py --date <exact-existing-date> --project "<authorized-existing-project>" --job-desc "<authorized-existing-description>" --proof references/submission-idempotency-live-verification.json
```

工具使用已有缓存 token，不登录、不修改认证或个人设置；transport 仅允许同一 OA origin 上项目、字典、日期查询三个只读端点，所有其他请求在网络前拒绝，禁用重定向。真实 CLI 中文路径须返回 `skipped-existing`，前后记录总数与完整内容一致，写端点尝试为零，才生成脱敏成功证明。真实新写入未在此次 live 验证执行；不得把离线 fake 的提交结果当真实 OA 写入结果。

### 已完成的验证

2026-10-10 11:28 CST，实际普通提交 CLI（不是 `--preview`）在 transport 强制只读 allowlist 下返回 `skipped-existing`、`verified=true`；既有记录前后均为 1 条，完整内容未变，工时写端点请求/拒绝尝试均为 0，个人设置与认证文件字节未变。仅项目、字典、日期查询三个路径实际访问。脱敏证明：`submission-idempotency-live-verification.json`。

随后全套离线测试 43 项通过（原基线 24 项；0 failure、0 error、0 skip），修改 Python 文件语法编译成功，`git diff --check` 通过。证明：`submission-idempotency-test-verification.json`；原始测试日志路径在该文件内。静态扫描无新增问题；两个旧验证码算术 `eval` 标记不在此次修改范围。未执行真实新工时写入，未做独立 reviewer 审核。
