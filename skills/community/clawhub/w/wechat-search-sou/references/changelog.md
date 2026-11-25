# 微信搜一搜技能 更新日志

## 1.1.3

- 精简 frontmatter：删除 `metadata.keywords` / `metadata.category`；有价值词并入精简 `tags`（触发仍以顶层 `description` 为准）。
- 再删无效字段：`openclaw.emoji`、`metadata.enabled` / `runtime` / `env_desc`（门禁仍靠 `openclaw.primaryEnv` + `requires`）。
- 精简 `metadata.examples`：article / video 各一条；去掉排序/时长等参数变体。
- HTTP 429/5xx：可重试（429→`RATE_LIMITED` 且 `noRetry=false`；与业务裸 2 区分）；`classifyPollError` 不再把所有 `ApiError` 一刀切为 fail。
- Create 成功读取出参 `id`（标准 36 字符 uuid）：有 `id` 时查询 `/info` **只传 `id`**（不带业务字段，避免 uuid 未命中时静默回落他单）；无 `id` 或形态不符时仍只按业务字段查。
- 新增 `references/contract.md`：「上游异步任务」约定；CLI schema / 信封不含任务 uuid。
- 执行示例改为 `node "<SKILL_ROOT>/scripts/wechat/…"`；faq 去掉宿主写死路径，统一用 `<SKILL_ROOT>` 占位。
- 文章/视频结果 enrich：非对象元素原样跳过。
- 布尔 flag（如 `--save`）：裸 flag 为 true；`--save=false`/`0` 为 false；非法赋值报错。
- 业务码映射：`410`（TOKEN 停用 Gone）/`405`（未开通）/`77`（过期）→ `AUTH_ERROR`；未知数字码兜底 `API_ERROR`；传输层补 `HTTP_404`/`HTTP_410` 说明。

## 1.1.2

- 新增 `references/faq.md`；SKILL 写入 Windows cmd/PowerShell 双壳例与「cmd 只用双引号」。
- CLI 支持 `--json-args`（与传统 flag 互斥；键名用 `keyword`/`sort`/`limit` 等）；`parseCliArgs` 统一入口；SKILL/faq 补例。
- stdout 信封顶层可选 `cost`（透传取数接口花费估算；错误省略）。
- 成功结果默认不落盘；`--save` 或 `GUAIKEI_ENABLE_LOG=1` 时写入系统临时目录 `wechat-guaikei/logs/`（不再写技能目录 `logs/`）。
- `backendCodes`：在余额判断之后将裸 `errcode === 14` 稳定映射为 `PLAN_LIMIT`。
- 补全 `requestApi` 创建重试注释：以 `noRetry` 为准（频控等稳定业务码不重试）。

## 1.1.1

- 错误码 errmsg 优先：`PLAN_LIMIT` / `INSUFFICIENT_BALANCE` / `RATE_LIMITED` / `DAILY_LIMIT`（日限 errcode 18）。

## 1.1.0

- 对照抖音技能统一 JSON 信封、退出码、Header TOKEN、轮询分类与 fail-fast 参数校验。
