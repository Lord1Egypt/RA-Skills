# 数据万象服务开通状态查询

## 适用场景

用户询问某个存储桶是否已绑定数据万象，或文档处理、媒体处理、智能语音、文件处理、图片处理（异步）、AI 内容识别（异步）等能力是否已开通时，按本文流程查询。同步图片处理和同步内容识别在 CI 绑定后默认可用，不要用“调用一次处理接口是否成功”代替开通状态查询。

## 查询顺序

总共涉及 7 个查询接口：1 个 CI 总开关、4 个数据处理子项、1 个图片处理（异步）子项、1 个 AI 内容识别（异步）子项。

### 1. CI 总开关（必查）

| Action | 请求 | 响应字段 |
| --- | --- | --- |
| `ci:DescribeCIBuckets` | `GET /`，Host 为 `<bucket>.ci.<region>.myqcloud.com` | `CIStatus`: `on` / `off` / `unbinding` |

状态映射：

- `CIStatus=on`：已绑定，同步图片处理与同步内容识别默认可用，并继续查询数据处理、图片处理（异步）和 AI 内容识别（异步）子项。
- `CIStatus=off`：未绑定，所有子项均视为未开启，不继续请求。
- `CIStatus=unbinding`：正在解绑，所有子项均视为未开启，不继续请求。
- `AccessDenied`：映射为 `noAuth`，跳过四个数据处理查询，但仍独立查询图片处理（异步）和 AI 内容识别（异步）。
- `NoSuchBucket` / `UserNotBucketOwner`：映射为 `off`。
- 其他错误：对齐控制台逻辑，CI 状态按 `on` 继续查询，同时保留原始错误，不能把错误静默当成确定已开通。

### 2. 数据处理子项

仅当 CI 总开关为 `on` 时查询。CI 状态为 `noAuth` 时，这四项返回 `noAuth`，不发请求。

| 功能 | Action | HTTP 路径 | 列表字段 | 开启判定 |
| --- | --- | --- | --- | --- |
| 文档处理 | `ci:DescribeDocProcessBucket` | `GET https://ci.<region>.myqcloud.com/docbucket` | `DocBucketList` | `DocBucketList?.[0]?.BucketId === bucket` |
| 媒体处理 | `ci:DescribeMediaBuckets` | `GET https://ci.<region>.myqcloud.com/mediabucket` | `MediaBucketList` | `MediaBucketList?.[0]?.BucketId === bucket` |
| 智能语音 | `ci:DescribeAsrBuckets` | `GET https://ci.<region>.myqcloud.com/asrbucket` | `AsrBucketList` | `AsrBucketList?.[0]?.BucketId === bucket` |
| 文件处理 | `ci:DescribeFileProcessBucket` | `GET https://ci.<region>.myqcloud.com/file_bucket` | `FileBucketList` | `FileBucketList?.[0]?.BucketId === bucket` |

请求使用 `bucketNames=<bucket>&pageNumber=1&pageSize=1` 精确过滤。列表首项不匹配或列表为空时为 `disabled`；`AccessDenied` 为 `noAuth`；其他失败为 `error`。

### 3. 图片处理

同步图片处理只要 CI 状态为 `on` 就默认可用，不需要单独开通。综合状态字段 `imageProcessing`：CI 为 `on` 时返回 `true`，为 `off` / `unbinding` 时返回 `false`，为 `noAuth` 时返回 `null`，表示无法确认绑定状态。

图片处理异步服务需要单独开通：

| Action | 请求 | 列表字段 | 开启判定 |
| --- | --- | --- | --- |
| `ci:DescribePicProcessBucket` | `GET https://ci.<region>.myqcloud.com/picbucket` | `PicBucketList` | 存在 `BucketId === bucket` 的列表项 |

综合状态查询使用 `bucketNames=<bucket>&pageNumber=1&pageSize=1` 精确过滤。目标桶存在时 `asyncImageProcessing.status=enabled`，不存在时为 `disabled`；`AccessDenied` 为 `noAuth`；其他失败为 `error`。

### 4. 内容识别

同步内容识别只要 CI 状态为 `on` 就默认可用，不需要单独开通。综合状态字段 `contentRecognition`：CI 为 `on` 时返回 `true`，为 `off` / `unbinding` 时返回 `false`，为 `noAuth` 时返回 `null`，表示无法确认绑定状态。

AI 内容识别异步服务需要单独开通：

| Action | 请求 | 列表字段 | 开启判定 |
| --- | --- | --- | --- |
| `ci:DescribeAiProcessBucket` | `GET https://ci.<region>.myqcloud.com/ai_bucket` | `AiBucketList` | 存在 `BucketId === bucket` 的列表项 |

综合状态查询使用 `bucketNames=<bucket>&pageNumber=1&pageSize=1` 精确过滤。正常响应且目标桶存在时 `asyncContentRecognition.status=enabled`，不存在时为 `disabled`；`AccessDenied` 为 `noAuth`；其他失败为 `error`。该接口具有独立 CAM Action，因此 CI 总开关返回 `noAuth` 时仍执行查询。

## 工作台开通交互契约

纯查询 `ci-service-status --bucket ... --region ...` 保持原输出，不触发交互。处理任务前增加 `--required-service ci|document|media|voice|file|asyncImage|asyncContentRecognition`；无效参数在请求前拒绝。

已核实未开通时，在现有 `ok: true`、`tool`、`bucket`、`region` 和状态数据外添加 `interaction` 和可直接转发的 `clientAction`：

```json
{
  "activationStatus": "requires_confirmation",
  "interaction": {
    "type": "ci_activation",
    "version": 1,
    "status": "requires_confirmation",
    "bucket": "example-1250000000",
    "region": "ap-guangzhou",
    "service": "ci",
    "reason": "ci_not_enabled",
    "precheck": { "ciBucketStatus": "off", "serviceStatus": "disabled" }
  },
  "clientAction": {
    "skill": "tencentcloud-cos",
    "command": "{\"action\":\"requestCiActivation\",\"type\":\"ci_activation\",\"version\":1,\"status\":\"requires_confirmation\",\"bucket\":\"example-1250000000\",\"region\":\"ap-guangzhou\",\"service\":\"ci\",\"reason\":\"ci_not_enabled\",\"precheck\":{\"ciBucketStatus\":\"off\",\"serviceStatus\":\"disabled\"}}"
  }
}
```

- CI 已绑定但目标子服务未开通时，`reason=service_not_enabled`，`precheck.ciBucketStatus=on`，`service` 指向所需子服务。
- CI 接口明确 `off` 或 `NoSuchBucket` 可触发。`UserNotBucketOwner` 虽保留历史 `off` 映射，但不生成 interaction；`noAuth`、`unbinding`、未知错误、子服务错误也不触发。原始错误保留在原状态数据和 `activationError` 中，UI `precheck` 只携带状态。
- 可用服务返回 `activationStatus=already_enabled`，非明确可用或未开通返回 `activationStatus=blocked`；两者均不带 `interaction` 或 `clientAction`。纯状态查询也不带这两个字段。
- `KIKI=1` 且没有专用确认回执时，七种开通 action 与 `ci-request` 的等价开通请求统一执行只读前置检查，输出 `operation=precheck`、对应开通命令的 `tool`，以及同一 `interaction` 和 `clientAction`。`ok` / `success` 仅表示前置检查成功，不能解释成已成功开通。
- 共享请求和 COS SDK 请求边界默认阻止直接请求已知 CI 开通端点；专用生命周期执行器只为回执匹配的单个服务写请求传递确认上下文。通用 CLI 不转发此上下文。公开模式保留原有写入行为。本地代码保护覆盖既有 CLI 和请求辅助函数，不构成对任意模型脚本或环境改写的运行时隔离。
- 不接受简单的 `confirmed` 参数。配套工作台声明 `mode=skill`、`decisionVersion=1` 时，可将原 `invokeClient` 的用户决定回填；确认仅表示用户同意，不能当作开通成功。
- 回执固定为 `{"type":"ci_activation_decision","version":1,"status":"confirmed","bucket":"example-1250000000","region":"ap-guangzhou","service":"ci","toolCallId":"example-call"}`。取消为 `status=cancelled`，结束依赖任务且不执行开通。
- 模型必须从原工具的实际结果复制回执，不得自行生成。将完整 JSON 安全地作为一个参数传给原专用命令，例如 `node {baseDir}/scripts/cos_node.mjs create-ci-bucket --bucket example-1250000000 --region ap-guangzhou --activation-confirmation '<原工具确认结果 JSON>'`。脚本校验固定字段及资源/服务一致性；此 JSON 不是签名票据，确认来源沿用 KiKi 会话和 Skill 的既有确认约定，不提供对任意模型脚本的隔离保证。
- 专用确认分支复用原 `createCiService`：预检 blocked 不写入，already_enabled 不重复写入；需要开通时调用原接口一次，随后复查。复查成功返回 `activationStatus=enabled`；无法确认返回 `CiActivationNotVerified`，只查询状态，不自动重试写入。

### 从 CLI 输出到工作台 UI

当前真实对话流中，`bash` 的 tool-output 可能只包含 `{exitCode, stdoutLength, stderrLength}`，不会把 stdout 正文交给前端。CLI 完整结果可供模型读取，但前端不能仅凭长度识别、校验或生成开通卡片；Skill 工具的 `instructionsLength` 也不能证明加载了哪个源码版本。

因此，仅在 `KIKI=1` 且当前客户端明确声明支持 `requestCiActivation` 时，查询返回 `requires_confirmation` 后，Skill 必须立即调用现有 `invokeClient`，原样传入工具生成的 `clientAction`。其中 `command` 严格由 `JSON.stringify({action: 'requestCiActivation', ...interaction})` 生成，不依赖模型重新编写协议。工作台识别该客户端动作后进入本地待确认交互、暂停续跑并展示 UI；前端不转发给 static action registry；确认后由 Skill 在原 Runtime 中执行云端开通。

对支持该动作的 KiKi 工作台，仅口头停下、输出 JSON/Markdown 或建议去控制台都没有完成 UI 请求。`invokeClient` 的请求参数在对话流可见，才是实际 UI 接管入口；前端仍须校验 Skill、action、版本和结构，不能把请求本身视为真实开通授权或成功回执。未经实测，不能将模型转发行为宣称为 Runtime 强制执行。

### 兼容性范围

- 七种开通命令的代码拦截由 `KIKI=1` 控制，适用于所有使用新版 Skill 的 KiKi 客户端，不仅是本次 Tea 工作台。未声明该 UI 能力的客户端应明确说明不支持并停止，不发送未知动作；旧客户端真实开通路径不会自动保留。
- 非 KiKi 公开模式仍按用户确认后执行专用命令的原流程运行，不调用此工作台客户端动作。显式传入新 `--required-service` 参数只增加前置检查数据；不传参数的原状态输出保持不变。
- 默认预检查继续保留原 UI 字段；新确认执行分支增加实际开通状态。普通查询、公开模式开通/关闭等既有 CLI 输出形状保留。
- 已开通资源的 COS 文件操作、图片/视频等实际处理请求和状态查询沿用原实现。严格模式禁止删除的策略不变；与 CI 绑定共享 `PUT /` 端点的解绑通用请求显式拒绝，避免误判成开通前置检查。此次更新没有修改凭证来源、SDK 版本或依赖。

## 服务开通与关闭接口

既有文档记录以下接口已通过临时空桶完成真实的开通、状态查询、关闭和清理测试。本轮工作台 demo 沿用生命周期接口，仅新增本地代码与 fixture 测试，未重新执行真实云端验收。

| 服务 | 开通请求 | 开通 Action | 关闭请求 | 关闭 Action |
| --- | --- | --- | --- | --- |
| 数据万象绑定 | `PUT /` | `ci:CreateCIBucket` | `PUT /?unbind` | `ci:DeleteCIBucket` |
| 文档处理 | `POST /docbucket` | `ci:CreateDocProcessBucket` | `DELETE /docbucket` | `ci:DeleteDocProcessBucket` |
| 媒体处理 | `POST /mediabucket` | `ci:CreateMediaBucket` | `DELETE /mediabucket` | `ci:DeleteMediaBucket` |
| 智能语音 | `POST /asrbucket` | `ci:CreateAsrBucket` | `DELETE /asrbucket` | `ci:DeleteAsrBucket` |
| 文件处理 | `POST /file_bucket` | `ci:CreateFileProcessBucket` | `DELETE /file_bucket` | `ci:DeleteFileProcessBucket` |
| 图片处理（异步） | `POST /picbucket` | `ci:CreatePicProcessBucket` | `DELETE /picbucket` | `ci:DeletePicProcessBucket` |
| AI 内容识别（异步） | `POST /ai_bucket` | `ci:CreateAiProcessBucket` | `DELETE /ai_bucket` | `ci:DeleteAiProcessBucket` |

请求域名为 `https://<bucket>.ci.<region>.myqcloud.com`。开通四类处理服务时，如果存储桶尚未绑定 CI，服务端也可自动完成绑定；推荐先明确执行 `create-ci-bucket`，便于分步确认状态。

CI 解绑前必须先清理工作流、批量任务、自动审核、历史审核及已开通处理服务等配置。`CIStatus=unbinding` 表示异步解绑仍在进行，不应立即当成 `off`。

## CLI

```bash
# 查询 CI 总开关、四项数据处理、同步默认能力、异步图片处理和异步内容识别状态
node {baseDir}/scripts/ci_api.mjs ci-service-status \
  --bucket <bucket-appid> \
  --region <region>

# CI 绑定 / 解绑
node {baseDir}/scripts/cos_node.mjs create-ci-bucket --bucket <bucket-appid> --region <region>
node {baseDir}/scripts/cos_node.mjs delete-ci-bucket --bucket <bucket-appid> --region <region>

# 文档处理开通 / 关闭
node {baseDir}/scripts/cos_node.mjs create-doc-process-bucket --bucket <bucket-appid> --region <region>
node {baseDir}/scripts/cos_node.mjs delete-doc-process-bucket --bucket <bucket-appid> --region <region>

# 媒体处理开通 / 关闭
node {baseDir}/scripts/cos_node.mjs create-media-bucket --bucket <bucket-appid> --region <region>
node {baseDir}/scripts/cos_node.mjs delete-media-bucket --bucket <bucket-appid> --region <region>

# 智能语音开通 / 关闭
node {baseDir}/scripts/cos_node.mjs create-asr-bucket --bucket <bucket-appid> --region <region>
node {baseDir}/scripts/cos_node.mjs delete-asr-bucket --bucket <bucket-appid> --region <region>

# 文件处理开通 / 关闭
node {baseDir}/scripts/cos_node.mjs create-file-process-bucket --bucket <bucket-appid> --region <region>
node {baseDir}/scripts/cos_node.mjs delete-file-process-bucket --bucket <bucket-appid> --region <region>

# 查询已开通图片处理异步服务的存储桶
node {baseDir}/scripts/cos_node.mjs describe-async-image-process-buckets \
  --bucket <bucket-appid> \
  --region <region>

# 开通图片处理异步服务并创建队列
node {baseDir}/scripts/cos_node.mjs create-async-image-process-bucket \
  --bucket <bucket-appid> \
  --region <region>

# 关闭图片处理异步服务并删除队列；严格模式下隐藏并拒绝执行
node {baseDir}/scripts/cos_node.mjs delete-async-image-process-bucket \
  --bucket <bucket-appid> \
  --region <region>

# 查询已开通 AI 内容识别异步服务的存储桶
node {baseDir}/scripts/cos_node.mjs describe-ai-process-buckets \
  --bucket <bucket-appid> \
  --region <region>

# 开通 AI 内容识别异步服务并创建队列
node {baseDir}/scripts/cos_node.mjs create-ai-process-bucket \
  --bucket <bucket-appid> \
  --region <region>

# 关闭 AI 内容识别异步服务并删除队列；严格模式下隐藏并拒绝执行
node {baseDir}/scripts/cos_node.mjs delete-ai-process-bucket \
  --bucket <bucket-appid> \
  --region <region>
```

图片处理异步服务的开通接口使用 `POST https://<bucket>.ci.<region>.myqcloud.com/picbucket`，CAM Action 为 `ci:CreatePicProcessBucket`；关闭接口使用相同路径的 `DELETE` 方法，CAM Action 为 `ci:DeletePicProcessBucket`。

AI 内容识别异步服务的开通接口使用 `POST https://<bucket>.ci.<region>.myqcloud.com/ai_bucket`，CAM Action 为 `ci:CreateAiProcessBucket`；关闭接口使用相同路径的 `DELETE` 方法，CAM Action 为 `ci:DeleteAiProcessBucket`。

## 输出原则

- 始终分别展示 `ciBucketStatus` 和 `dataProcessing`，不要只返回一个总布尔值。
- `imageProcessing` 表示同步图片处理是否默认可用；`asyncImageProcessing` 表示异步服务是否单独开通，禁止混用。
- `imageProcessing` 和 `contentRecognition` 表示同步能力：CI 已绑定时为 `true`，未绑定时为 `false`，无权限确认时为 `null`。
- `asyncImageProcessing` 和 `asyncContentRecognition` 返回带 `status`、`action`、`request` 或 `error` 的异步服务状态对象。
- `noAuth`、`error` 与 `disabled` 含义不同，禁止互相替代。
- 保留请求的 `requestId` 和错误码，排障时不要输出 Authorization、SecretKey 或 Token。
- 综合状态和独立查询完全只读，严格模式可用；KiKi 开通命令默认只执行前置检查，原工具确认回执仅用于专用开通分支；所有关闭与解绑命令都属于删除语义，严格模式隐藏并禁止执行。
