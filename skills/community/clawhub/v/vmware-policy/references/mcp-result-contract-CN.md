# MCP 公共结果契约（Policy 1.26.0）

这是共享库/传输层契约，不是新增 MCP 工具或权限。工具名、参数、成功返回值和 CLI 确认不变。

## 错误

失败的 MCP 工具结果保持 `isError=true`，统一提供
`structuredContent.vmware_error={"error":"资源未找到","hint":"先列出资源"}`。
`error` 为非空字符串，`hint` 为工具提供的字符串或 null，不猜测修复方法。
`vmware_error` 为保留的传输元数据。旧文本及结构化业务字段保留，不改变 Python 工具调用方。只读取 `content` 的客户端仍会看到旧错误格式；
需读取结构化视图才能使用这一公共契约。文本体本身的迁移须单独进行版本设计。
成功、预览及已恢复的内层失败，不会仅因数据提到 error 而被标记失败。
SDK ToolError 保留已有错误文本并增加同一视图；取消继续传播。
不新增错误码分类，不放宽 Policy/RBAC、审计、undo、熔断或确认机制。

失败结果的完整结构化对象会新增字段，严格比较整个对象的客户端须允许这一新增字段。
客户端应按需读取公共视图或旧文本，同时展示两者可能重复诊断内容。

## offset 分页

`page_envelope` 保留 `items`、`returned`、`limit`、`total`、`truncated`、`hint`，
为确实支持 offset 的工具提供 `offset` 和 `next_offset`。
`next_offset` 为 null 时结束，不以 `truncated` 作为循环条件。未知总数保持 null；
未知总数且末页刚好满页时，可能需再读空页。空页停止。各组件保留原有分页上限和默认值。

新公共 helper 的 `truncated` 表示“本页不是整个集合”。AIops、Harden、Storage、VDI/PrivateAI 的旧 helper
暂时保留“后面还有页”的旧语义及 hint，只新增公共 `next_offset`，不静默改变旧字段。
跨组件客户端以 `next_offset` 判断是否继续；无 offset 参数的工具不伪造续页，cursor API 保留 cursor。

发布顺序：先发布 Policy 1.26.0，再更新依赖组件并重新生成发布锁。
源码覆盖测试不等于已发布落地。
