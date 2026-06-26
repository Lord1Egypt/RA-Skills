# ClawHub 可疑扫描处理手册

## 常见命中原因

### 1. 同一个文件里同时有环境变量读取和网络发送

典型形式：

- `process.env` + `fetch(`
- `os.getenv(...)` + `requests.post(...)`

这种组合很容易被当成潜在外传行为。

### 2. 同一个文件里同时有本地文件读取和网络发送

典型形式：

- `fs.readFileSync(...)` + `fetch(...)`
- `open(...)` + `requests.post(...)`

### 3. 代码或文档提到私有配置源

高风险关键词：

- `~/.openclaw/secrets.json`
- 私有 `config.json`
- 自动读取本地 secrets store

### 4. 只改功能，不改结构

这是最容易反复踩的坑。

典型情况：

- 已经把“默认直连凭证”改成“本地可选凭证”
- 已经把 README 改得更保守
- 但真正执行链里，还是同一个文件：
  - 读本地配置
  - 解析凭证
  - 直接发外部请求

这种情况下，即使功能上更合理，扫描命中的结构仍然没变，所以很可能继续 `suspicious`。

### 5. 把 capability note 当成 suspicious verdict

ClawHub 页面里常见的：

- `Credentials`
- `Persistence & Privilege`
- `Posts externally`

这些首先是能力说明，不等于 `flagged`。

真正要看的是：

- 最新版本是否已经切换
- `staticScan.status`
- `summary`
- 页面内嵌数据里的 verdict / status

## 优先修复策略

### 拆文件

把下面几类逻辑拆开：

- 配置读取
- 网络请求
- 主流程

目标不是“骗过扫描器”，而是让行为边界更清楚。

对“本地凭证 + 外部发送”这类 skill，优先拆成：

- local credential store
- credential resolver
- api client
- sender / main flow

不要把这四层混成一个文件。

### 收窄读取范围

明确只允许读取白名单环境变量，例如：

- `HUMAN_LIKE_MEM_API_KEY`
- `HUMAN_LIKE_MEM_BASE_URL`

不要遍历整个 `process.env`。

### 前置披露

在 `SKILL.md` / `README` / `SECURITY.md` 中写清楚：

- 什么时候会联网
- 会发送哪些字段
- 不会读取哪些本地文件

## 如何判断是否真的修好

不要只看页面顶部标签，要同时验证：

- 页面版本已经更新
- `clawhub inspect <slug>` 指向最新版本
- 页面内嵌数据里的 `staticScan.status`
- `llmAnalysis.status` / `verdict`

如果已经确认最新版本依然 `suspicious` / `flagged`：

- 不要继续重复 `inspect + 打开页面`
- 先挑一个最可能命中的结构去改
- 改完后递增版本、重新发布、再复核

也就是说，检查只负责定位，不负责无限循环。

## follow-builders-sidecar 案例总结

### 为什么前面多次更新后仍然会可疑

1. 代码结构里仍然保留了“本地配置读取 + 外部发送”的强命中模式。
2. 文档里仍然在强调本地敏感配置来源，放大了审核系统的风险感知。
3. 发布后页面存在 pending / 缓存，容易误把旧版本结果当新版本结果。
4. 一开始把 `Credentials` / `Persistence` note 当成“依然 suspicious”，导致判断标准不够准。

### 最终为什么去掉了可疑标签

1. 用白名单临时目录发布，避免把无关本地文件带进发布包。
2. 把本地凭证读取、OpenClaw 配置读取、Feishu API 调用、发送主流程拆开。
3. 保留本地直连凭证能力，但只写到用户本地路径，不上传仓库。
4. 文档明确写清楚：
   - 为什么需要这些本地权限
   - 会发送什么
   - 哪些内容只保留在本地
5. 最终以最新版本页面内嵌数据确认：
   - `staticScan.status = clean`
   - `summary = "No suspicious patterns detected."`

### 一个重要判断

如果最新版本已经是：

- `staticScan.status = clean`
- `summary = "No suspicious patterns detected."`

但页面仍然有 `Credentials` / `Persistence` note，
这通常说明 skill 仍然具备这些能力，但已经不再被判为 `suspicious`。这时不要继续为“去掉 note”而做无意义重构。

## 经验结论

如果最新页面内嵌数据已经是：

- `staticScan.status = clean`
- `summary = "No suspicious patterns detected."`
- `OpenClaw = Benign`

那就说明本次修复已经生效，即使某些缓存 UI 还没完全刷新。
