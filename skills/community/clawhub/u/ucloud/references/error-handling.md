# 错误处理

## 通用规则

当调用失败时：

1. 根据产品命令 help、API 定义、当前命令参数或请求 payload、已知默认值和最近的 lookup 结果进行诊断。
2. 如果修复方案安全且具体，尝试自动修复问题。
3. 仅在存在具体诊断时才重试，不要盲目重复。
4. 如果问题无法安全修复，停止并向用户报告错误详情。
5. 向用户提供重试前可以采取的具体后续操作。

重试默认保持安静。不要仅因为请求失败就开启 CLI 调试日志；仅在用户明确要求打印日志或请求详细调试输出时才开启。

安全修复示例：

- 添加缺失的 `ProjectId`、`Region` 或 `Zone`
- 通过 `ListRegions`、`ListZones` 或 `GetProjectList` 解析公共参数
- 纠正经 CLI help 或 API 定义确认的明显参数、payload 字段错误或遗漏
- 当产品级 CLI 路径缺少能力、行为不明确或封装错误，且原始 Action 已知并更安全可控时，切换到 `ucloud api --local-file`
- 当本地激活配置并非预期的账户上下文时，使用明确指定的 `--profile` 重试
- 依次回退默认计费方式：按小时预付费→按小时后付费→按月预付费，然后询问用户是否尝试按年预付费
- 创建成功后，如果创建响应中缺少用户需要的关键字段，优先调用对应的产品查询命令进行补充；没有合适命令时再调用对应的 Describe API
- 在报告登录信息前，根据镜像发行版推断正确的默认云主机用户名

如果 CLI 因所选 profile 缺失或不可用而失败，停止并请用户选择另一个 profile，或询问是否使用 OAuth 授权。用户同意后执行 `ucloud auth login`；无浏览器环境执行 `ucloud auth login --no-browser`。如果用户不使用 OAuth，再引导 `ucloud init` 或本地 AK/SK profile 配置。不要临时创建包含真实密钥的命令，也不要要求用户把密钥粘贴到对话中。

报告不可恢复的错误时，包含：

- 产品命令、API Action 或服务和方法
- 相关请求范围，如 `ProjectId`、`Region`、`Zone` 或目标资源 ID
- 错误码
- 错误信息
- 建议的后续步骤

建议应具体，例如添加 IAM 权限、提供缺失的标识、确认正确的 Region 或项目、检查余额，或验证该 API 是否对当前账号或 Region 可用。

## `299 IAM permission error`

当 API 调用出现 `299 IAM permission error` 时，使用以下决策规则：

1. 检查 API 定义。
2. 判断该 API 是否需要 `ProjectId`。
3. 如果 API 需要 `ProjectId` 而请求中没有包含，将 `299` 优先视为缺少 `ProjectId` 的问题。
4. 通过 `GetProjectList` 解析 `ProjectId` 或向用户询问确切的 ProjectId，然后重试。
5. 如果 API 需要 `ProjectId` 且请求中已经包含，或者 API 本身不要求 `ProjectId`，将 `299` 视为真正的权限错误。
6. 告知用户当前没有该 API 的权限，需要先在添加所需权限后再重试。

## 操作附注

不要立即认为 `299` 就意味着缺少权限。先检查 `ProjectId` 是否必填，因为某些 API 在 `ProjectId` 必填但被省略时也会返回同样的错误。
