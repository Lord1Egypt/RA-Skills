---
name: tencentcloud-cos
description: >
  腾讯云对象存储(COS)和数据万象(CI)集成技能。覆盖文件存储管理、AI处理和知识库三大核心场景。
  存储场景：上传文件到云端、下载云端文件、批量管理存储桶文件、获取文件签名链接分享、查看文件元信息、查询数据万象及子服务开通状态。
  图片处理场景：图片质量评估打分、AI超分辨率放大、AI智能裁剪、二维码/条形码识别、添加文字水印、获取图片EXIF信息、缩放、裁剪、旋转、格式转换。
  文档处理场景：Word/Excel/PPT等办公文档转PDF、文档预览。
  媒体处理场景：视频智能封面提取、视频转码、视频截帧、获取媒体信息。
  内容审核场景：图片/视频/音频/文本/文档内容审核，检测违规内容。
  智能语音场景：语音识别（音频转文字）、语音合成（文字转语音）、音频降噪、人声分离。
  文件处理场景：文件哈希计算、文件压缩打包、文件解压。
  内容识别场景：描述单个图片或视频文件的内容、图片标签识别、OCR文字识别、视频ASR/OCR和粗分类。
  知识库场景：一键创建知识库、上传文档到知识库、从知识库检索内容片段。
  智能检索场景：MetaInsight以图搜图、以文搜图、以文搜视频片段、人脸搜索、元数据检索、多模态检索（文档/图片/视频）、
  AI 媒资详情（GetAIMediaInfo，按 URI 拉取已入库图片或视频的 AI 标签、ASR、OCR、粗分类与整体描述，视频可按片段拼出片段描述）。
  控制台功能引导场景：当前 Skill 无法直接满足时，为大量数据迁移、数据导出、拓展功能、数据备份、SDK、
  具身智能生态和湖仓生态提供对应的 COS 控制台入口。
  当用户提到以下关键词或口语化表述时应触发此技能：
  上传到COS、腾讯云存储、对象存储、云存储、存储桶、Bucket、图片处理、图片压缩、图片放大、超分辨率、抠图、裁剪、二维码识别、水印、文档转换、转PDF、视频封面、智能封面、以图搜图、图片搜索、MetaInsight、COS上传、COS下载、签名URL、腾讯云文件、数据万象、CI处理、内容审核、图片审核、视频审核、文本审核、语音识别、语音合成、降噪、人声分离、OCR、文字识别、图片标签、文件内容描述、这个文件讲了什么、图片里有什么、视频讲了什么、创建知识库、建一个知识库、上传到知识库、往知识库里加文件、查询知识库、从知识库找、搜索知识库、知识库检索、文档检索、文档搜索、数据迁移、批量迁移、数据导出、数据备份、COS SDK、具身智能生态、湖仓生态、COS 拓展功能。
description_zh: "腾讯云 COS 对象存储、数据万象智能处理、MetaInsight 检索、知识库与控制台功能引导"
description_en: "Tencent Cloud COS Storage, CI Processing, MetaInsight Retrieval, Knowledge Base, and Console Feature Guidance"
message: >
  我是腾讯云 COS 与数据万象 Skill，提供对象存储管理、图片与媒体处理、内容审核、
  MetaInsight 数据检索、数据集分析、结果预览和知识库能力。例如可以帮你上传或下载文件、
  生成签名链接、处理图片、转换文档、检索桶内文件、查询数据集或创建知识库；
  当前能力无法满足时，也会提供匹配的 COS 控制台功能入口。
client_commands: true
conditions:
  - url: 'https://console.cloud.tencent.com/cos/**'
    mode: discover
defaultMode: discover
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "requires":
          {
            "secrets":
              [
                "SecretId",
                "SecretKey"
              ],
            "optionalSecrets":
              [
                "Token"
              ],
            "config":
              [
                "Region",
                "Bucket"
              ],
            "optionalConfig":
              [
                "DatasetName",
                "Domain",
                "ServiceDomain",
                "Protocol"
              ],
            "envMapping":
              {
                "SecretId": "TENCENT_COS_SECRET_ID",
                "SecretKey": "TENCENT_COS_SECRET_KEY",
                "Token": "TENCENT_COS_TOKEN",
                "Region": "TENCENT_COS_REGION",
                "Bucket": "TENCENT_COS_BUCKET",
                "DatasetName": "TENCENT_COS_DATASET_NAME",
                "DatasetImageSearch": "TENCENT_COS_DATASET_IMAGE_SEARCH",
                "DatasetFaceSearch": "TENCENT_COS_DATASET_FACE_SEARCH",
                "DatasetMeta": "TENCENT_COS_DATASET_META",
                "MetaInsightRegion": "TENCENT_COS_METAINSIGHT_REGION",
                "Domain": "TENCENT_COS_DOMAIN",
                "ServiceDomain": "TENCENT_COS_SERVICE_DOMAIN",
                "Protocol": "TENCENT_COS_PROTOCOL"
              },
            "secretsDescription":
              {
                "SecretId":
                  {
                    "label": "腾讯云 API 密钥 ID",
                    "type": "cloud-credential",
                    "provider": "Tencent Cloud",
                    "sensitivity": "critical",
                    "scope": "COS object storage and CI data processing APIs"
                  },
                "SecretKey":
                  {
                    "label": "腾讯云 API 密钥 Key",
                    "type": "cloud-credential",
                    "provider": "Tencent Cloud",
                    "sensitivity": "critical",
                    "scope": "COS object storage and CI data processing APIs"
                  },
                "Token":
                  {
                    "label": "STS 临时安全令牌",
                    "type": "session-token",
                    "provider": "Tencent Cloud STS",
                    "sensitivity": "high",
                    "scope": "Time-limited access (default 1800s), auto-expires"
                  }
              }
          },
        "security":
          {
            "credentialStorage":
              {
                "default": "ephemeral",
                "ephemeral":
                  {
                    "description": "Credentials exist only in shell session environment variables; nothing written to disk",
                    "persistsToDisk": false,
                    "recommendation": "RECOMMENDED — use with STS temporary credentials"
                  }
              },
            "requirements": [
              "MUST use sub-account keys with least-privilege COS-only policy; root account keys are FORBIDDEN",
              "STS temporary credentials are recommended; default behavior is ephemeral (no disk persistence)",
              "Credentials are NEVER echoed back to the user in chat"
            ]
          },
        "install":
          [
            {
              "id": "node-cos-sdk",
              "kind": "node",
              "package": "cos-nodejs-sdk-v5",
              "label": "Install COS Node.js SDK"
            }
          ]
      }
  }
---

# 腾讯云 COS 技能

一站式管理腾讯云对象存储(COS)和数据万象(CI)，通过统一的 Node.js SDK 脚本提供以下能力：

- **文件存储**：上传、下载、列出、删除文件，获取签名下载链接，批量操作，复制
- **存储桶管理**：列出/创建存储桶，查询数据万象及各子服务开通状态，读写 ACL、跨域、标签，并查询版本控制、生命周期、Policy、防盗链、默认加密、静态网站、日志等 COS 配置
- **图片处理**：缩放、裁剪、旋转、格式转换、文字水印、质量评估、超分辨率、智能裁剪、二维码识别
- **内容识别**：描述单个图片或视频的内容、图片标签识别、OCR 文字识别、视频 ASR/OCR 和粗分类
- **文档处理**：办公文档转 PDF、文档预览（图片/HTML）
- **媒体处理**：视频智能封面、转码、截帧、媒体信息
- **内容审核**：图片/视频/音频/文本/文档违规检测
- **智能语音**：语音识别、语音合成、音频降噪、人声分离
- **文件处理**：哈希计算、压缩、解压
- **智能检索 MetaInsight**：数据集管理、索引管理、以图搜图、文本搜图、以文搜视频片段、人脸搜索、元数据检索、多模态检索（文档/图片/视频）
- **数据集分析**：自然语言条件筛选、聚合统计、桶反查数据集、图片理解、EXIF 和 AI 媒资详情（`ci_api.mjs get-ai-media-info`：按 URI 拉取已入库图片或视频的 AI 标签、ASR、OCR、粗分类）
- **结果预览**：为图片、视频和文档检索结果生成可交互 HTML 预览
- **🚀 知识库**：一键创建知识库（自动创建桶+数据集+绑定），上传文档到知识库，语义检索知识库内容

统一 Skill 提供三个入口，均输出 JSON：

- `scripts/cos_node.mjs`：COS 存储、写操作、处理作业和通用 CI 能力。
- `scripts/ci_api.mjs`：数据集筛选、聚合和语义检索等只读能力。
- `scripts/preview_gen.mjs`：检索结果的本地批量签名与 HTML 预览生成。

> **请注意**对象存储(COS)与数据万象(CI)均为腾讯云付费服务，使用前请知悉，**使用本 skill 默认视为已知悉并接受相关费用**。具体见官方文档：
> [COS 费用](https://cloud.tencent.com/document/product/436/16871) ｜ [CI 费用](https://cloud.tencent.com/document/product/460/6970)

## 运行模式与能力策略

每次执行前读取环境变量 `KIKI`：仅当 `KIKI=1` 时进入严格模式，其他值或未设置均为公开模式。

| 模式 | 判断 | 功能策略 |
| --- | --- | --- |
| **公开模式** | `KIKI` 不为 `1` | 提供全部功能 |
| **严格模式** | `KIKI=1` | 禁止所有删除操作，隐藏本地凭证配置、持久化、`encrypt-env`、`decrypt-env`；CI 开通默认仅预检查；配套工作台确认回执可驱动专用开通命令 |

`KIKI` 控制严格模式的功能策略，不参与身份认证或凭证选择。脚本优先使用运行时提供的 `TENCENTCLOUD_*` 凭证；未提供时使用公开环境的 `TENCENT_COS_*`、`.env` 或 `.env.enc`。严格模式隐藏并拒绝删除类操作与本地凭证管理功能；CI 开通命令默认只读预检查，仅在当前客户端声明支持 `requestCiActivation` 时通过 `invokeClient` 请求开通 UI。配套工作台声明 `ciActivation.mode=skill`、`decisionVersion=1` 且原工具返回有效确认后，按下述流程复用专用开通命令；通用请求仍不放行开通。其他业务能力沿用原有实现；**这不表示任何数据万象（CI）能力可以豁免删除限制**。

严格模式下，**禁止一切删除语义的操作，COS 与数据万象（CI）同样生效，没有任何 CI 例外**。具体包括：

- 所有 `delete-*` action（删除对象、批量删除、CI 解绑、各处理服务关闭、删除文件索引等），均禁止执行并从可用 action 列表隐藏。
- **删除数据集、删除数据集绑定关系**等没有专用 action 的删除操作，同样禁止，不得通过 `ci-request`、`ci_api.mjs`、直接 HTTP/curl、内联脚本或任何其他入口绕行执行。
- `ci-request --method DELETE` 一律拒绝。

除了入口拦截，`scripts/lib/ci_client.mjs` 的 `cosRequest` 与 `scripts/cos_node.mjs` 的 `cosRequestPromise` 会在请求层再次拒绝 DELETE 请求，双重兜底避免绕过。需要调整隐藏列表时，修改其中的 `STRICT_HIDDEN_ACTIONS`，并同步本节说明与测试。

## 首次使用 — 自动设置

当用户首次要求操作 COS 时，按以下流程操作：

### 步骤 0：识别运行模式

先运行 `{baseDir}/scripts/setup.sh --check-only`。若 `KIKI=1`，本地凭证管理功能会被隐藏，直接跳到「操作指南」；否则继续公开模式设置流程。

### 步骤 1：检查当前状态

```bash
{baseDir}/scripts/setup.sh --check-only
```

如果 Node.js 和 cos-nodejs-sdk-v5 已安装、环境变量已配置，跳到「操作指南」。

### 步骤 2：公开模式未配置时，引导用户提供凭证

本步骤仅适用于公开模式。严格模式不得进入本步骤。

告诉用户：
> 我需要你的腾讯云凭证来连接 COS 存储服务。请放心，你的密钥会受到以下保护：
>
> #### 🛡️ 凭证安全保障
> - **默认不落盘**：凭证仅存于当前终端会话内存中，关闭终端即消失
> - **可选持久化**：如需保存，凭证写入项目本地 `.env` 文件（仅当前用户可读，权限 600）
> - **支持 AES-256 加密**：持久化后可一键加密为 `.env.enc`，明文自动删除，密钥绑定本机+本用户，拷贝到其他环境无法解密
> - **自动防误提交**：`.env` / `.env.enc` 自动添加到 `.gitignore`，不会进入版本控制
> - **永远不会在对话中回显你的密钥**
>
> #### 🔒 推荐方案：STS 临时凭证（最安全，自带有效期）
> 1. **SecretId** — TmpSecretId
> 2. **SecretKey** — TmpSecretKey
> 3. **Token** — SecurityToken
> 4. **Region** — 存储桶区域（如 ap-guangzhou）
> 5. **Bucket** — 存储桶名称（格式 name-appid）
>
> #### ⚠️ 降级方案：永久密钥（必须使用子账号最小权限密钥）
> 1. **SecretId** / **SecretKey** / **Region** / **Bucket**
>
> #### 可选配置
> - **DatasetName** — 数据万象数据集名称（仅 MetaInsight 检索需要）
> - **Domain** / **ServiceDomain** / **Protocol** — 自定义域名配置

### 步骤 3：公开模式设置环境变量并运行安装

```bash
export TENCENT_COS_SECRET_ID="<SecretId>"
export TENCENT_COS_SECRET_KEY="<SecretKey>"
export TENCENT_COS_TOKEN="<Token>"  # STS 临时凭证才需要
export TENCENT_COS_REGION="<Region>"
export TENCENT_COS_BUCKET="<Bucket>"

# 默认模式：凭证仅存于当前 session，关闭终端后需重新 export
{baseDir}/scripts/setup.sh --from-env

# 持久化模式：凭证写入项目本地 .env 文件，下次自动读取
{baseDir}/scripts/setup.sh --from-env --persist
```

脚本会自动安装 `cos-nodejs-sdk-v5` 到项目本地 `node_modules/` 并验证连接。

**持久化说明**：`--persist` 会将凭证写入项目目录下的 `.env` 文件（权限 600），并自动添加到 `.gitignore`。
`cos_node.mjs` 启动时会自动读取 `.env`（环境变量优先于 `.env` 文件）。清理凭证：`rm -f .env`。

---

## 操作指南

存储和处理作业使用 `scripts/cos_node.mjs`；数据集只读检索优先使用 `scripts/ci_api.mjs`；检索结果预览使用 `scripts/preview_gen.mjs`。三个入口共享相同的运行模式与凭证策略。

如果用户需求无法由当前 Skill 满足，但与迁移、导出、拓展功能、备份、SDK、具身智能生态或湖仓生态匹配，按 `references/console-feature-guides.md` 提供对应控制台链接。已有 action 优先，未命中映射时不要猜测链接。

```
node {baseDir}/scripts/cos_node.mjs <action> [--option value ...]
```

**全局可选参数**（所有 action 均支持，用于覆盖环境变量中的默认值）：
- `--bucket <BucketName>` — 指定操作的存储桶（覆盖 `TENCENT_COS_BUCKET`）
- `--region <Region>` — 指定地域（覆盖 `TENCENT_COS_REGION`）
- `--dataset-name <Name>` — 指定数据集名称（覆盖 `TENCENT_COS_DATASET_NAME`）

> 初始配置的 Region、Bucket、DatasetName 只是默认值，每次调用都可以通过参数自由指定。

### COS 存储操作

```bash
# 上传文件
upload --file /path/to/file.jpg --key remote/path/file.jpg

# 上传字符串
put-string --content "文本内容" --key remote/file.txt --content-type "text/plain"

# 下载文件
download --key remote/path/file.jpg --output /path/to/save/file.jpg

# 列出文件（--marker 用于翻页：上一页返回 isTruncated=true 时，用 nextMarker 续页）
list --prefix "images/" --max-keys 100
list --prefix "images/" --max-keys 100 --marker "<上页返回的nextMarker>"

# 获取签名 URL
sign-url --key remote/path/file.jpg --expires 3600

# 查看文件信息
head --key remote/path/file.jpg

# 删除文件（仅公开模式）
delete --key remote/path/file.jpg

# 批量删除（仅公开模式）
delete-multiple --keys '["file1.txt","file2.txt"]'

# 复制对象
copy-object --source bucket.cos.region.myqcloud.com/source.jpg --key dest.jpg
```

补充对象只读 action：`list-object-versions`、`get-object-acl`、`get-object-tagging`、`get-object-retention`、`get-symlink`、`list-multipart-uploads`、`list-multipart-parts`、`options-object`。完整参数见 `references/api_reference.md`。

### COS 存储桶管理

> ⚠️ **安全限制**：本技能禁止删除存储桶和清空存储桶操作。

```bash
# 列出所有存储桶
list-buckets

# 创建存储桶
create-bucket --bucket mybucket-1250000000 --region ap-guangzhou

# 检查存储桶是否存在
head-bucket --bucket mybucket-1250000000

# 获取/设置存储桶 ACL
get-bucket-acl
put-bucket-acl --acl private

# 获取/设置跨域配置
get-bucket-cors
put-bucket-cors --origin "*" --methods "GET,POST,PUT"

# 获取/设置标签
get-bucket-tagging
put-bucket-tagging --tags '[{"Key":"env","Value":"prod"}]'

# 查询版本控制/生命周期/地域
get-bucket-versioning
get-bucket-lifecycle
get-bucket-location
```

补充存储桶只读 action：`get-bucket-policy`、`get-bucket-replication`、`get-bucket-website`、`get-bucket-referer`、`get-bucket-domain`、`get-bucket-origin`、`get-bucket-logging`、`get-bucket-inventory`、`list-bucket-inventory`、`get-bucket-accelerate`、`get-bucket-encryption`、`get-bucket-intelligent-tiering`、`get-bucket-access-monitor`、`get-bucket-logging-analysis`、`get-bucket-notification`、`get-bucket-object-lock`、`get-bucket-domain-certificate`、`get-bucket-strict-signature`、`get-bucket-bandwidth-quota`、`get-bucket-response-control`。完整参数见 `references/api_reference.md`。

### 使用 CI 功能前：先查状态，未开通先确认

用户要使用数据万象处理能力（图片处理、内容识别、文档处理、媒体处理、内容审核、智能语音、文件处理、异步任务等）时，先查询该桶的 CI 服务状态并通过 `--required-service` 指定本次任务所需服务，不要直接执行处理任务。KiKi 工作台（`KIKI=1`）声明支持 `requestCiActivation` 时，通过 `invokeClient` 接收固定结构化开通请求并展示 UI；配套工作台确认后由本 Skill 执行原有开通命令并复查状态。公开模式保留用户确认后执行专用开通命令的流程。

功能与所需服务映射：

| 用户需求 | `--required-service` | 对应开通命令 |
| --- | --- | --- |
| 同步图片处理、同步内容识别、内容审核 | `ci` | `create-ci-bucket` |
| 文档处理（转 PDF / 预览） | `document` | `create-doc-process-bucket` |
| 媒体处理（封面 / 转码 / 截帧 / 媒体信息） | `media` | `create-media-bucket` |
| 智能语音（识别 / 合成 / 降噪 / 人声分离） | `voice` | `create-asr-bucket` |
| 文件处理（哈希 / 压缩 / 解压） | `file` | `create-file-process-bucket` |
| 图片处理异步任务 | `asyncImage` | `create-async-image-process-bucket` |
| AI 内容识别异步任务 | `asyncContentRecognition` | `create-ai-process-bucket` |

任务前置检查与确认流程：

1. 查询时携带所需服务，例如内容审核用 `node {baseDir}/scripts/ci_api.mjs ci-service-status --bucket <bucket-appid> --region <region> --required-service ci`。
2. 在 `KIKI=1` 且当前工作台明确声明支持 `requestCiActivation` 时，工具返回 `activationStatus=requires_confirmation` 及 `clientAction` 后，**下一步必须调用 `invokeClient`，把工具返回的整个 `clientAction` 对象原样作为参数传入**。它固定包含 `skill="tencentcloud-cos"` 和已序列化的 `command` 字符串（`action="requestCiActivation"` 加完整 `ci_activation` v1 数据）；不要重新拼接、改字段或省略参数。`invokeClient` 发出后等待工作台 UI 处理，不继续创建处理任务，也不重试其他开通入口。
3. 只有已核实 `ciBucketStatus=off`（含 CI 接口的 `NoSuchBucket`）或已绑定且目标子服务 `disabled` 才触发交互。`noAuth`、`UserNotBucketOwner`、`unbinding`、未知错误和子服务错误都不能解释成可开通；说明实际问题并停止，不尝试开通。
4. `activationStatus=already_enabled` 才表示本次所需服务已核实可用。它是查询结果，不是本轮成功开通的回执。
5. **确认后复用专用开通命令**：仅当当前工作台声明 `ciActivation.mode=skill`、`decisionVersion=1`，并且原 `invokeClient` 的工具结果返回 `type=ci_activation_decision`、`version=1`、`status=confirmed`，且 `toolCallId/bucket/region/service` 与该待确认请求完全一致时，将这个工具结果 JSON **原样**作为对应专用 `create-*` 命令的 `--activation-confirmation` 参数。命令仍使用原 Bucket/Region；一次只开通这个服务。该分支先重新预检，已开启则不写入，需要开通时复用原接口，写后再查状态；只有 `activationStatus=enabled` 或 `already_enabled` 才继续原任务。`unverified`、失败、超时先查询状态，不自动重复写入或换其他端点尝试。
6. **取消和缺失确认**：原工具回执为 `cancelled` 时，简短说明已暂不开通并结束本轮，不再发起开通、处理任务或新的开通追问。无有效回执时，七个 `create-*` 命令和 `ci-request` 等价端点仍只返回前置检查。旧 demo 客户端、普通正文/自然语言确认、模型自行填写的 `--confirmed` 均不升级为本回执；不得编造、改写或跨工具复用 `--activation-confirmation`，不得更改 `KIKI`、另写 HTTP 脚本或用处理任务隐式开通。
7. 非 KiKi 公开模式不调用此 `requestCiActivation`；工具中的 `clientAction` 不改变公开模式的执行方式。仍先说明状态并获取用户明确确认，再执行原有专用开通命令；未确认不得自动变更或以创建处理任务的方式代替开通。
8. `KIKI=1` 但当前客户端未声明该 UI 能力时，说明“当前客户端暂不支持数据万象开通交互”并停止依赖任务；不要调用未知客户端动作、宣称已展示 UI 或绕过前置检查执行开通。此代码限制适用于所有 KiKi 客户端，UI 需要客户端配套支持。

**支持该 UI 的 KiKi 工作台为何必须调用 `invokeClient`**：当前工作台对话流中的 `bash` 结果可能只有 `exitCode`、`stdoutLength`、`stderrLength`，CLI 的完整 stdout 只对模型可见。只执行查询、输出 JSON 文本、口头说“等待开通”或让用户去控制台，都不能让前端收到开通请求；不能用 `askUser` 或 Markdown/XML 标记代替 `invokeClient`。工作台接管 `requestCiActivation` 为待确认 UI，按原工具回填用户决定；真实执行由本 Skill 完成，不需要 static 注册开通动作。

假设工具已经返回以下 `clientAction`，则直接将该对象用于 `invokeClient`（示例资源仅为虚构；实际调用必须使用工具原值）：

```json
{
  "skill": "tencentcloud-cos",
  "command": "{\"action\":\"requestCiActivation\",\"type\":\"ci_activation\",\"version\":1,\"status\":\"requires_confirmation\",\"bucket\":\"example-1250000000\",\"region\":\"ap-guangzhou\",\"service\":\"ci\",\"reason\":\"ci_not_enabled\",\"precheck\":{\"ciBucketStatus\":\"off\",\"serviceStatus\":\"disabled\"}}"
}
```

若返回 `blocked`、`already_enabled` 或仅做纯状态查询，则没有 `clientAction`，不得自行制造开通请求。非 KiKi 环境一律按上述公开模式确认流程处理，不因存在 `invokeClient` 工具而切换到此工作台 UI，也不宣称已展示 UI。


### 万象计费提示（严格模式首次使用拦截）

数据万象（CI）与智能检索（MetaInsight）为按量计费服务。严格模式（`KIKI=1`）下，**首次**执行计费类动作时脚本不直接执行，而是返回计费提示交互：

1. **拦截范围**：`cos_node.mjs` 的同步/异步处理、审核、语音、文件处理、MetaInsight 数据集写入与检索、`create-knowledge-base` 等计费类 action；`ci_api.mjs` 的检索与图片理解命令。只读状态查询（`describe-*` / `list-*` / `ci-service-status`）、COS 存储操作与 `ci-request` 扩展入口不拦截。
2. 被拦截时返回 `success=false`、`billingStatus=requires_confirmation` 和 `clientAction`，不发起任何云请求。
3. 工作台声明支持 `requestBillingNotice` 时，**下一步必须调用 `invokeClient`，把工具返回的整个 `clientAction` 对象原样传入**（固定包含 `skill="tencentcloud-cos"` 和已序列化的 `command`，`action="requestBillingNotice"` 加 `billing_notice` v1 数据）；不得改写字段、不得用正文说明或 Markdown 代替卡片。
4. 仅当原 `invokeClient` 工具结果返回 `type=billing_notice_decision`、`version=1`、`status=confirmed` 时，将该 JSON **原样**作为原命令的 `--billing-confirmation` 参数重试同一命令；脚本记录确认后本次及后续计费动作直接放行。回执为 `cancelled` 时停止依赖任务，不重复发起确认。
5. 不得编造、改写或复用其他交互的回执充当 `--billing-confirmation`；无效回执会被拒绝（`InvalidBillingNoticeConfirmation`）。
6. 确认状态记录在本机 Skill 目录的 `.billing-notice-ack.json`（权限 600，非敏感标记）；自动化环境可用 `TENCENT_COS_BILLING_ACK=1` 显式跳过拦截。
7. 当前客户端不支持 `requestBillingNotice` 交互时，说明「当前客户端暂不支持计费提示确认」并停止依赖任务，不要绕过拦截直接执行。
8. 公开模式不拦截，计费提示以本文档顶部的费用说明为准。

### CI 服务开通状态

用户询问存储桶是否绑定数据万象，或文档处理、媒体处理、智能语音、文件处理、图片处理（异步）、AI 内容识别（异步）是否开通时，先查询状态，不要通过尝试创建处理任务来推断。同步图片处理和同步内容识别在 CI 绑定后默认可用。

```bash
node {baseDir}/scripts/ci_api.mjs ci-service-status \
  --bucket <bucket-appid> \
  --region <region>
```

查询顺序和结论解释：

1. 必须先查 CI 总开关。`off` / `unbinding` 时停止后续查询，全部子服务按未开启返回。
2. CI 为 `on` 时，继续查询文档处理、媒体处理、智能语音、文件处理、图片处理（异步）和 AI 内容识别（异步）；异步图片处理通过 `GET /picbucket`、异步内容识别通过 `GET /ai_bucket` 独立判断。
3. CI 总开关无权限时映射为 `noAuth`，跳过四个数据处理查询，但仍独立查询图片处理（异步）和 AI 内容识别（异步）状态。
4. 同步图片处理与同步内容识别只要 CI 已绑定就默认可用；不要用同步能力推断对应异步服务已经开启。
5. `disabled`、`noAuth`、`error` 含义不同，回答时必须分别说明。

完整的查询接口、字段和错误映射见 `references/ci-service-status.md`。该查询完全只读，严格模式可用。

### CI 服务开通与关闭

非 KiKi 模式的服务开通和关闭必须使用专用 action，不要通过创建处理任务推断或代替。KiKi 的开通 action 默认只返回前置检查；携带上述有效原工具确认回执时才走专用执行分支。关闭服务、删除队列和 CI 解绑属于删除语义，严格模式下隐藏并拒绝执行。

```bash
# 绑定 / 解绑数据万象
create-ci-bucket --bucket <bucket-appid> --region <region>
delete-ci-bucket --bucket <bucket-appid> --region <region>

# 文档处理
create-doc-process-bucket --bucket <bucket-appid> --region <region>
delete-doc-process-bucket --bucket <bucket-appid> --region <region>

# 媒体处理
create-media-bucket --bucket <bucket-appid> --region <region>
delete-media-bucket --bucket <bucket-appid> --region <region>

# 智能语音
create-asr-bucket --bucket <bucket-appid> --region <region>
delete-asr-bucket --bucket <bucket-appid> --region <region>

# 文件处理
create-file-process-bucket --bucket <bucket-appid> --region <region>
delete-file-process-bucket --bucket <bucket-appid> --region <region>
```

`create-ci-bucket` 使用 `PUT /`，`delete-ci-bucket` 使用 `PUT /?unbind`；其余四类服务使用对应路径的 `POST` 开通和 `DELETE` 关闭。完整路径与 CAM Action 见 `references/ci-service-status.md`。

### CI 图片基础处理

同步图片处理在存储桶绑定 CI 后默认可用；异步图片处理需要单独开通。

```bash
# 查询已开通图片处理异步服务的存储桶
describe-async-image-process-buckets --bucket <bucket-appid> --region <region>

# 开通图片处理异步服务并创建队列
create-async-image-process-bucket --bucket <bucket-appid> --region <region>

# 关闭图片处理异步服务并删除队列（严格模式隐藏并拒绝执行）
delete-async-image-process-bucket --bucket <bucket-appid> --region <region>

# 获取图片元信息
image-info --key images/photo.jpg

# 图片缩放
image-thumbnail --key images/photo.jpg --width 200 --height 200

# 图片裁剪
image-crop --key images/photo.jpg --width 300 --height 300 --gravity center

# 图片旋转
image-rotate --key images/photo.jpg --degree 90

# 格式转换（webp/png/jpg/avif/heif/tpg）
image-format --key images/photo.jpg --format webp

# 添加文字水印（支持中文）
watermark-font --key images/photo.jpg --text "版权所有"
```

### CI AI 图片处理

```bash
# 图片质量评估
assess-quality --key images/photo.jpg

# AI 超分辨率
ai-super-resolution --key images/photo.jpg

# AI 智能裁剪
ai-pic-matting --key images/photo.jpg --width 200 --height 200

# 二维码识别
ai-qrcode --key images/qrcode.jpg
```

### CI 内容识别

同步内容识别在存储桶绑定 CI 后默认可用；AI 内容识别异步服务需要单独开通。

```bash
# 查询已开通 AI 内容识别异步服务的存储桶；--bucket 默认作为精确过滤条件
describe-ai-process-buckets --bucket <bucket-appid> --region <region>

# 开通 AI 内容识别异步服务并创建队列
create-ai-process-bucket --bucket <bucket-appid> --region <region>

# 关闭 AI 内容识别异步服务并删除队列（严格模式隐藏并拒绝执行）
delete-ai-process-bucket --bucket <bucket-appid> --region <region>

# 同步图片标签识别
recognize-image --key images/photo.jpg

# 同步 OCR 文字识别
ocr-general --key images/document.jpg
```

#### 单个文件内容描述

当用户问“这个文件里有什么”“描述这张图片”“这个视频讲了什么”时，先按文件类型和数据集状态选择能力，不要只返回文件元信息：

| 文件情况 | 优先能力 | 说明 |
| --- | --- | --- |
| 单张图片，需要自然语言描述 | `ci_api.mjs image-analysis` | 无需数据集；`ImageLabels` 返回整体描述和分层标签，`Custom` 可按用户问题分析 |
| 单张图片，只需标签或文字 | `recognize-image` / `ocr-general` | 分别用于图片标签和 OCR，不要把标签结果冒充完整内容描述 |
| 已进入智能检索、已完成入库，且属于 `ImageSearch` / `VideoSearch` 数据集的图片或视频 | `ci_api.mjs get-ai-media-info` | 仅在这三个条件同时满足时使用；按 URI 获取 AI 标签、ASR、OCR、粗分类、整体描述与片段描述 |
| 文档或纯文本文件 | 文档检索或直接读取文本 | `get-ai-media-info` 不支持 `DocSearch`；纯文本优先读取正文后总结 |

```bash
# 描述桶内单张图片
node {baseDir}/scripts/ci_api.mjs image-analysis \
  --bucket <bucket-appid> --region <region> \
  --object images/photo.jpg --type ImageLabels

# 按用户关注点分析图片
node {baseDir}/scripts/ci_api.mjs image-analysis \
  --bucket <bucket-appid> --region <region> \
  --object images/photo.jpg --type Custom --prompt '请描述图片中的人物、场景和正在发生的事情'

# 获取智能检索图片或视频数据集中已完成入库文件的 AI 详情（接口名 GetAIMediaInfo）
node {baseDir}/scripts/ci_api.mjs get-ai-media-info \
  --bucket <bucket-appid> --region <region> \
  --dataset-name <dataset> --uri 'cos://<bucket-appid>/<object-key>'
```

执行原则：

1. 图片内容描述优先使用 `image-analysis`；只有标签需求时才使用 `recognize-image`。
2. 只有文件已加入智能检索，并在 `ImageSearch` 或 `VideoSearch` 数据集中完成入库后，才能使用 `get-ai-media-info`。仅找到同桶数据集不代表该文件已经入库；无法确认时不要调用，图片回退到 `image-analysis`，视频则说明需要先完成智能检索入库。
3. 若用户已确认文件入库但不知道数据集名称，可用 `find-datasets-by-bucket` 查询候选数据集；不要臆造名称，也不要把 `DocSearch` 数据集用于该接口。
4. `get-ai-media-info` 返回的是结构化 AI 信息，但**包含描述类内容**：视频的 `AiRoughData.Description` 是整体描述，回答"这个视频讲了什么"时优先采用；片段描述没有单独字段，需按 `AsrInfo`/`OcrInfo`/`AiLabelInfo` 的 `From`~`To`（或 `ClipId`）聚合出每个时间段说了什么、画面有什么字、出现什么标签。回答用户时应综合整体描述、标签、ASR、OCR 和粗分类生成友好描述，并说明缺失或尚未分析的字段。
5. 图片需要更完整说明时，可组合 `image-analysis` 的整体描述与 `get-ai-media-info` 的结构化信息，但后者仍必须满足智能检索入库前置条件。
6. 详细字段和前置条件见 `references/dataset-catalog.md` 的“媒资 AI 信息查询”和“图片理解”。

### CI 文档处理

```bash
# 文档转 PDF（自动轮询等待结果）
create-doc-to-pdf-job --key docs/report.docx

# 查询文档处理任务
describe-doc-job --job-id <jobId>

# 文档预览（转图片）
doc-preview --key docs/report.docx --page 1 --format jpg

# 获取文档在线预览 HTML 链接
doc-preview-html-url --key docs/report.docx
```

### CI 媒体处理

```bash
# 视频智能封面（自动轮询等待结果）
create-media-smart-cover-job --key videos/demo.mp4

# 查询媒体处理任务
describe-media-job --job-id <jobId>

# 视频转码
media-transcode-job --key videos/demo.mp4 --format mp4

# 视频截帧
media-snapshot --key videos/demo.mp4 --time 5 --format jpg

# 获取媒体文件信息
media-info --key videos/demo.mp4
```

### CI 内容审核

```bash
# 图片同步审核
audit-image --key images/photo.jpg

# 图片异步审核任务
audit-image-job --key images/photo.jpg

# 视频审核任务
audit-video-job --key videos/demo.mp4

# 音频审核任务
audit-audio-job --key audio/song.mp3

# 文本审核任务
audit-text-job --content "待审核的文本内容"

# 文档审核任务
audit-document-job --key docs/report.docx

# 查询审核任务结果（--type 可选 image/video/audio/text/document）
describe-audit-job --job-id <jobId> --type image
```

### CI 智能语音

```bash
# 语音识别
speech-recognition-job --key audio/meeting.mp3 --engine 16k_zh_video

# 语音合成（文字转语音）
tts-job --text "你好，欢迎使用腾讯云"

# 音频降噪
noise-reduction-job --key audio/noisy.mp3

# 人声分离
voice-separate-job --key audio/song.mp3
```

### CI 文件处理

```bash
# 文件哈希计算（md5/sha1/sha256）
file-hash --key docs/report.docx --type md5

# 文件压缩
file-compress-job --prefix "images/" --format zip

# 文件解压
file-uncompress-job --key archive.zip --prefix "output/"

# 查询文件处理任务
describe-file-job --job-id <jobId>
```

### CI 数据集只读检索与分析（推荐）

数据集筛选、聚合、语义检索、图片理解和 EXIF 查询优先使用 `scripts/ci_api.mjs`。它与 `cos_node.mjs` 共用运行模式和凭证解析，不创建、修改或删除资源。

```bash
node {baseDir}/scripts/ci_api.mjs help
node {baseDir}/scripts/ci_api.mjs list-datasets --appid <AppId> --region <region>
node {baseDir}/scripts/ci_api.mjs find-datasets-by-bucket --appid <AppId> --region <region> --bucket <bucket-appid>
node {baseDir}/scripts/ci_api.mjs simple-query --bucket <bucket> --region <region> --body '<json>'
node {baseDir}/scripts/ci_api.mjs image-search --bucket <bucket> --region <region> --dataset-name <name> --mode text --text '<query>'
```

按任务读取对应参考文件，不要臆造字段或操作符：

- 条件筛选与聚合：`references/dataset-simple-query.md`
- 图片、文档、视频和人脸检索：`references/dataset-search.md`
- 数据集字段与模板：`references/dataset-catalog.md`
- 桶内容总结与聚合：`references/bucket-content-summary.md`、`references/bucket-content-aggregation.md`

检索命中文件后保留原始 `cos://` URI。需要可视化时，按 `references/search-results-preview.md` 生成 spec，再执行：

```bash
node {baseDir}/scripts/preview_gen.mjs --spec-file <spec.json> --out <result.html>
```

宿主环境提供 `exportFile` 时可继续导出 HTML；不提供时直接返回生成路径，不得伪造 artifact ID。

宿主提供 `invokeClient` 时，可按 `references/query-spec.schema.json` 下发数据集信息查询。宿主不支持时，`describeDatasets` 回退到 `ci_api.mjs list-datasets`；`describeDatasetFields` 当前没有 CLI 回退，只能使用 `invokeClient`，不得伪造字段结果。

### CI MetaInsight

> **地域约束**：MetaInsight 数据集仅支持 `ap-chengdu`（成都）、`ap-beijing`（北京）、`ap-shanghai`（上海）三个地域。绑定数据集时，数据集必须与存储桶在同一地域，跨地域绑定会失败；如果桶所在地域不在上述列表，提示用户该地域暂不支持智能检索/数据集，建议改用支持地域的桶，不要强行绑定。
>
> **创建数据集 / 知识库时必须显式指定地域**：未通过 `--mi-region`（或 `--region`）/ `TENCENT_COS_METAINSIGHT_REGION` 指定时命令会直接报错，**不要默认使用成都等任何地域**——收到该报错时向用户说明「目前仅支持北京、上海、成都」并询问要使用哪个地域，确认后再带上地域参数重试。

#### 数据集管理

绑定存储桶到数据集前，**必须先询问用户采用增量索引还是存量索引**，不要默认选择：

| 模式 | 含义 | 适用场景 |
| --- | --- | --- |
| `Mode=1` 存量索引 | 绑定后自动索引桶内**已有全部文件** | 需要立即检索历史文件 |
| `Mode=0` 增量索引 | 只索引绑定后**新上传**的文件 | 历史文件量大或无需检索历史文件，节省索引成本与时间 |

> **注意**：存量/增量索引只能在**绑定存储桶与数据集时**设置一次，绑定完成后无法再修改。若绑定后想切换模式，只能删除绑定后重新绑定。

**若当前没有合适的数据集**（桶未绑定数据集，或已绑定但模板与需求不符），引导用户创建新数据集，不要直接失败：

1. 用 `find-datasets-by-bucket` 反查桶绑定，或用 `list-datasets` 列出全部数据集，按所需模板筛选。
2. 无合适数据集时，告知用户当前状态与所需模板，询问是否创建；确认后执行 `create-dataset`。
3. 创建后 `create-dataset-binding` 绑定目标桶，并询问增量/存量索引。
4. 需要检索或统计历史文件时选存量索引（`Mode=1`）。

> 示例：用户要「统计桶内文件的类型分布」→ 属于元数据聚合分析，需元数据数据集 `Official:COSBasicMeta` → 创建数据集 → 绑定并开启存量索引（`Mode=1`）→ 索引完成后用 `simple-query` 的 `Aggregations` 按 `MediaType` 分组统计。

```bash
# 列出所有数据集
list-datasets

# 创建数据集（模板：Official:COSBasicMeta / Official:ImageSearch / Official:VideoSearch / Official:FaceSearch）
# 地域必须显式指定（--mi-region，与要绑定的桶同地域）；未指定会报错，需向用户确认（仅支持北京/上海/成都），不要默认成都
create-dataset --name my-dataset --template "Official:ImageSearch" --description "图片搜索" --mi-region ap-beijing

# 查询数据集详情
describe-dataset --name my-dataset

# 绑定存储桶到数据集（先询问用户增量/存量，再选 --mode；存量=1 默认索引已有文件，增量=0 只索引新文件）
# 注意：数据集必须与桶同地域，且地域需在 MetaInsight 支持列表（ap-chengdu/ap-beijing/ap-shanghai）内
create-dataset-binding --name my-dataset
create-dataset-binding --name my-dataset --mode 1          # 存量索引：索引桶内已有全部文件
create-dataset-binding --name my-dataset --uri "cos://other-bucket-1250000000" --mode 0  # 增量索引：只索引新上传文件

# 查询数据集的绑定关系
describe-dataset-bindings --name my-dataset
```

> **删除约束**：删除数据集、删除数据集绑定关系属于删除语义操作，与删除对象/解绑数据万象同级。公开模式下也必须先向用户明确确认；严格模式（`KIKI=1`）下一律禁止，且当前没有提供 `delete-dataset` / `delete-dataset-binding` action，**不要通过 `ci-request --method DELETE` 或任何其他方式绕行**。

#### 索引管理

```bash
# 创建文件元数据索引
create-file-meta-index --name my-dataset --uri "cos://bucket/images/photo.jpg" --media-type image

# 查询文件元数据索引
describe-file-meta-index --name my-dataset --uri "cos://bucket/images/photo.jpg"

# 删除文件元数据索引（仅公开模式）
delete-file-meta-index --name my-dataset --uri "cos://bucket/images/photo.jpg"
```

#### 检索（需预建数据集）

检索前先确认桶已绑定对应数据集：用 `find-datasets-by-bucket` 反查桶绑定的数据集；若未绑定，先 `create-dataset-binding` 建立绑定；若也没有合适的数据集，引导用户创建新数据集（流程见「数据集管理」）。绑定数据集必须与桶同地域，且桶地域需在 MetaInsight 支持列表内；地域不支持时提示用户，不要强行绑定。绑定前同样需询问用户采用增量索引还是存量索引（见「数据集管理」）。

检索前必须确认数据集模板。图片和元数据检索可使用 `cos_node.mjs` 的兼容 action；当前人脸粗搜优先使用 `ci_api.mjs`，字段与限制以 `references/dataset-search.md` 为准。

| 检索类型 | 所需数据集模板 | 数据集选择 |
|---------|---------------|----------|
| 图片检索（以图搜图/文本搜图） | `Official:ImageSearch` | `--dataset` → `TENCENT_COS_DATASET_IMAGE_SEARCH` → `TENCENT_COS_DATASET_NAME` |
| 视频检索（以文搜视频片段） | `Official:VideoSearch` | `--dataset` → `TENCENT_COS_DATASET_VIDEO_SEARCH` |
| 人脸粗搜 | `ImageSearch` / `VideoSearch`（需开白） | `--dataset-name`，必要时先按桶反查 |
| 元数据检索 | `Official:COSBasicMeta` 或其他可检索模板 | `--dataset` → `TENCENT_COS_DATASET_META` |

`cos_node.mjs face-search` 是兼容旧 `Official:FaceSearch` 接口的 action，不要与 `ci_api.mjs face-search` 的人脸粗搜混用。

```bash
# 以图搜图（ImageSearch 数据集）
image-search-pic --uri "https://example.com/query.jpg"

# 文本搜图（ImageSearch 数据集）
image-search-text --text "蓝天白云"

# 当前人脸粗搜（ImageSearch / VideoSearch 数据集）
node {baseDir}/scripts/ci_api.mjs face-search --bucket <bucket-appid> --region <region> --dataset-name <name> --uri "cos://bucket/photo.jpg" --limit 10 --match-threshold 80

# 元数据检索 — 简单查询（任意数据集；返回含 nextToken 时表示还有下一页，须续页拉全）
dataset-simple-query --dataset my-dataset --sort CustomId --order desc --max-results 50
dataset-simple-query --dataset my-dataset --query '{"Operation":"eq","Field":"ContentType","Value":"image/jpeg"}'
dataset-simple-query --dataset my-dataset --query '{"Operation":"eq","Field":"ContentType","Value":"image/jpeg"}' --next-token "<上页返回的nextToken>"

# 视频检索 — 以文搜视频片段（VideoSearch 数据集；视频检索仅支持文搜，不支持图搜）
video-search --text "骑行的片段" --dataset my-video-dataset --limit 10

# 多模态检索（hybrid-search 统一走 datasetquery/hybridsearch）：文档检索默认 DocSearch
hybrid-search --text "包含一颗大树的文档" --dataset docsearch --templates DocSearch --limit 10
hybrid-search --text "关键词" --dataset docsearch --filter '{"$and":[{"MediaType":{"$in":["image","document"]}},{"Size":{"$gt":123}}]}'
```

### 🚀 知识库（快捷功能）

> **重要**：这是一组面向用户口语化描述的快捷流程。用户不需要知道底层命令，只需用自然语言描述意图。

#### 用户意图识别

| 用户可能的说法 | 对应操作 |
|---------------|----------|
| "帮我创建一个知识库" "建一个知识库" "我想做个文档库" | → 执行 `create-knowledge-base` |
| "上传到知识库" "把文件放进知识库" "往知识库里加文档" | → 执行 `upload`（指向知识库对应的桶） |
| "查询知识库" "从知识库找" "搜索知识库" "知识库里有没有关于XX的内容" | → 执行 `hybrid-search`（指向知识库对应的数据集） |

#### 流程 1：创建知识库

当用户说"创建知识库"/"建一个知识库"/"我想做个文档库"时：

1. 如果用户没指定名称 → 询问用户想给知识库起什么名字
2. 如果用户没指定地域 → 向用户说明「目前仅支持北京、上海、成都」并询问使用哪个地域（未指定地域命令会报错，不要默认成都）
3. 执行创建：

```bash
create-knowledge-base --name <用户指定的名称> --region <ap-beijing | ap-shanghai | ap-chengdu>
```

4. 自动完成三步：创建存储桶 → 创建 DocSearch 数据集 → 绑定
5. **记住本次创建的知识库信息**（桶名、地域、数据集名），后续上传/查询时直接使用
6. 告诉用户：

> ✅ 知识库「<名称>」已创建！
> - 你可以把文档（PDF、Word、Excel、PPT、TXT 等）上传到这个知识库
> - 上传后系统会自动建立索引（需要几秒到几分钟）
> - 之后你可以直接说"从知识库里搜一下XXX"来查询内容

#### 流程 2：上传到知识库

当用户说"上传到知识库"/"把文件放进知识库"/"往知识库里加文档"时：

**判断使用哪个知识库：**

1. 如果本次对话中已创建/使用过知识库 → 直接使用该知识库的桶和地域
2. 如果不确定 → 执行 `list-datasets` 列出所有数据集，筛选 TemplateId 为 `Official:DocSearch` 的数据集：
   - 只有 1 个 DocSearch 数据集 → 直接使用它，通过数据集绑定关系推断对应的桶
   - 有多个 DocSearch 数据集 → 列出让用户选择
   - 没有 DocSearch 数据集 → 告诉用户"你还没有知识库，要帮你创建一个吗？"
3. 确定知识库后，执行上传：

```bash
upload --file <用户的文件路径> --key <文件名> --bucket <知识库桶名> --region <知识库地域>
```

4. 告诉用户：

> ✅ 文件已上传到知识库「<名称>」，索引建立中，稍后即可检索。

#### 流程 3：查询知识库

当用户说"查询知识库"/"从知识库找XX"/"搜索知识库"/"知识库里有没有关于XX的"/"从知识库里搜一下"时：

**判断使用哪个知识库：**

1. 如果本次对话中已创建/使用过知识库 → 直接使用该知识库的数据集
2. 如果不确定 → 执行 `list-datasets` 列出所有数据集，筛选 TemplateId 为 `Official:DocSearch` 的数据集：
   - 只有 1 个 DocSearch 数据集 → 直接使用它
   - 有多个 DocSearch 数据集 → 列出让用户选择（展示名称和文件数）
   - 没有 DocSearch 数据集 → 告诉用户"你还没有知识库，要帮你创建一个吗？"
3. 确定知识库后，执行检索：

```bash
hybrid-search --text "<用户的查询内容>" --dataset <知识库数据集名> --templates DocSearch
```

4. **结果呈现**（不要直接输出 JSON，用友好格式）：
   - 按相关度排序展示检索结果
   - 每条结果展示：**相关度分数** + **来源文件名** + **匹配内容摘要**
   - 如果没有匹配结果 → 告诉用户"知识库中没有找到相关内容，你可以上传更多文档试试"

### CI 通用请求（扩展入口）

用于调用尚未封装为独立 action 的 CI 能力：

```bash
ci-request --method POST --path "image/auditing" --body '<xml>...</xml>'
ci-request --method GET --path "jobs/<jobId>"
```

---

## 功能对照表

| 分类 | action | 说明 |
|------|--------|------|
| **存储** | `upload` | 上传文件 |
| | `put-string` | 上传字符串 |
| | `download` | 下载文件 |
| | `list` | 列出文件 |
| | `sign-url` | 获取签名链接 |
| | `delete` | 删除文件（严格模式隐藏） |
| | `delete-multiple` | 批量删除（严格模式隐藏） |
| | `head` | 文件元信息 |
| | `copy-object` | 复制对象 |
| **存储桶管理** | `list-buckets` | 列出所有存储桶 |
| | `create-bucket` | 创建存储桶 |
| | `head-bucket` | 检查存储桶是否存在 |
| | `get-bucket-acl` / `put-bucket-acl` | ACL 权限管理 |
| | `get-bucket-cors` / `put-bucket-cors` | 跨域配置 |
| | `get-bucket-tagging` / `put-bucket-tagging` | 标签管理 |
| | `get-bucket-versioning` | 查询版本控制 |
| | `get-bucket-lifecycle` | 查询生命周期 |
| | `get-bucket-location` | 查询存储桶地域 |
| **CI 服务绑定** | `create-ci-bucket` | 绑定存储桶并开通数据万象 |
| | `delete-ci-bucket` | 解绑数据万象（严格模式隐藏） |
| **图片基础** | `describe-async-image-process-buckets` | 查询已开通图片处理异步服务的存储桶 |
| | `create-async-image-process-bucket` | 开通图片处理异步服务并创建队列 |
| | `delete-async-image-process-bucket` | 关闭图片处理异步服务并删除队列（严格模式隐藏） |
| | `image-info` | 图片元信息 |
| | `image-thumbnail` | 缩放 |
| | `image-crop` | 裁剪 |
| | `image-rotate` | 旋转 |
| | `image-format` | 格式转换 |
| | `watermark-font` | 文字水印 |
| **AI图片** | `assess-quality` | 质量评估 |
| | `ai-super-resolution` | 超分辨率 |
| | `ai-pic-matting` | 智能裁剪 |
| | `ai-qrcode` | 二维码识别 |
| **内容识别** | `describe-ai-process-buckets` | 查询已开通 AI 内容识别异步服务的存储桶 |
| | `create-ai-process-bucket` | 开通 AI 内容识别异步服务并创建队列 |
| | `delete-ai-process-bucket` | 关闭 AI 内容识别异步服务并删除队列（严格模式隐藏） |
| | `recognize-image` | 图片标签识别 |
| | `ocr-general` | OCR 文字识别 |
| **文档处理** | `create-doc-process-bucket` | 开通文档处理服务并创建队列 |
| | `delete-doc-process-bucket` | 关闭文档处理服务并删除队列（严格模式隐藏） |
| | `create-doc-to-pdf-job` | 文档转 PDF |
| | `describe-doc-job` | 查询文档任务 |
| | `doc-preview` | 文档预览（转图片） |
| | `doc-preview-html-url` | 文档在线预览链接 |
| **媒体处理** | `create-media-smart-cover-job` | 智能封面 |
| | `describe-media-job` | 查询媒体任务 |
| | `media-transcode-job` | 视频转码 |
| | `media-snapshot` | 视频截帧 |
| | `media-info` | 媒体文件信息 |
| **内容审核** | `audit-image` | 图片同步审核 |
| | `audit-image-job` | 图片异步审核 |
| | `audit-video-job` | 视频审核 |
| | `audit-audio-job` | 音频审核 |
| | `audit-text-job` | 文本审核 |
| | `audit-document-job` | 文档审核 |
| | `describe-audit-job` | 查询审核结果 |
| **智能语音** | `create-asr-bucket` | 开通智能语音服务并创建队列 |
| | `delete-asr-bucket` | 关闭智能语音服务并删除队列（严格模式隐藏） |
| | `speech-recognition-job` | 语音识别 |
| | `tts-job` | 语音合成 |
| | `noise-reduction-job` | 音频降噪 |
| | `voice-separate-job` | 人声分离 |
| **文件处理** | `create-file-process-bucket` | 开通文件处理服务并创建队列 |
| | `delete-file-process-bucket` | 关闭文件处理服务并删除队列（严格模式隐藏） |
| | `file-hash` | 哈希计算 |
| | `file-compress-job` | 文件压缩 |
| | `file-uncompress-job` | 文件解压 |
| | `describe-file-job` | 查询文件任务 |
| **MetaInsight 管理** | `list-datasets` | 列出数据集 |
| | `create-dataset` | 创建数据集 |
| | `describe-dataset` | 查询数据集详情 |
| | `create-dataset-binding` | 绑定存储桶 |
| | `describe-dataset-bindings` | 查询绑定关系 |
| **MetaInsight 索引** | `create-file-meta-index` | 创建文件索引 |
| | `describe-file-meta-index` | 查询文件索引 |
| | `delete-file-meta-index` | 删除文件索引（严格模式隐藏） |
| **MetaInsight 检索** | `image-search-pic` | 以图搜图 |
| | `image-search-text` | 文本搜图 |
| | `face-search` | 兼容旧 FaceSearch 人脸搜索；当前粗搜优先使用 `ci_api.mjs` |
| | `dataset-simple-query` | 元数据检索 |
| | `hybrid-search` | 多模态检索（文档/图片/视频统一入口：文搜或图搜由 `--templates` 与 `--mode` 决定；注意视频/文档仅支持文搜，图搜仅 ImageSearch 支持） |
| | `video-search` | 视频检索（以文搜视频片段，需 VideoSearch 数据集；仅支持文搜） |
| | `get-ai-media-info`（`ci_api.mjs`） | AI 媒资详情（`GetAIMediaInfo`）：按 URI 拉取已入库图片或视频的 AI 标签、ASR、OCR、粗分类与整体描述；视频可按 `From`~`To`/`ClipId` 拼出片段描述（需 ImageSearch / VideoSearch 数据集） |
| **通用** | `ci-request` | 调用未封装的 CI API（严格模式禁止 DELETE） |
| **🚀 知识库** | `create-knowledge-base` | "创建知识库" → 一键创建桶+数据集+绑定 |
| | `upload` → 指向知识库桶 | "上传到知识库" → 上传文档 |
| | `hybrid-search` → 指向知识库数据集 | "查询知识库" → 语义检索文档内容 |
| **🚫 禁止** | ~~deleteBucket~~ | **不允许删除/清空存储桶** |
| **🔐 凭证管理** | `encrypt-env` | 加密 .env → .env.enc 并删除明文 |
| | `decrypt-env` | 解密 .env.enc → .env 还原明文 |

## 安全注意事项

### 凭证处理

公开模式可使用以下三种凭证存储方式；`KIKI=1` 时以下本地凭证管理功能会被隐藏：

| 模式 | 存储位置 | 安全性 | 用法 |
|------|---------|--------|------|
| **默认模式** | shell session 环境变量 | ⭐⭐⭐ 最安全（关闭终端即消失） | `{baseDir}/scripts/setup.sh --from-env` |
| **持久化模式** | 项目 `.env` 文件（权限 600） | ⭐⭐ 便捷但明文 | `{baseDir}/scripts/setup.sh --from-env --persist` |
| **加密持久化** | 项目 `.env.enc`（AES-256-GCM） | ⭐⭐⭐ 推荐 | 先 `--persist`，再 `encrypt-env` |

#### 加密存储（推荐）

持久化后执行 `encrypt-env` 即可加密凭证：

```bash
# 1. 先持久化
{baseDir}/scripts/setup.sh --from-env --persist

# 2. 加密（自动删除明文 .env，生成 .env.enc）
node {baseDir}/scripts/cos_node.mjs encrypt-env

# 3. 之后脚本自动从 .env.enc 解密读取，所有功能正常使用
node {baseDir}/scripts/cos_node.mjs list
```

**加密原理**：
- 算法：AES-256-GCM（认证加密，防篡改）
- 密钥派生：`SHA-256(hostname + username + 项目绝对路径)`
- **加密文件绑定当前机器和用户**，拷贝到其他机器/用户无法解密
- 如需还原明文：`node scripts/cos_node.mjs decrypt-env`
- 清理凭证：`rm -f .env .env.enc`

**其他安全要求**：
- **永远不要在对话中回显** SecretId/SecretKey
- 推荐使用 **STS 临时凭证**（自带有效期，过期自动失效）

### 最小权限与子账号密钥

> ⚠️ **永远不要使用主账号密钥**。

推荐创建专用子账号并授予最小权限策略：
- `QcloudCOSDataReadOnlyAccess` — 仅读取
- `QcloudCOSDataFullControl` — COS 数据读写
- 如需数据万象功能，额外添加 `QcloudCIFullAccess`

可进一步限制到具体存储桶：
```json
{
  "statement": [{
    "effect": "allow",
    "action": ["cos:*"],
    "resource": ["qcs::cos:<Region>::uid/<APPID>:<BucketName>/*"]
  }]
}
```

### 安装包说明

本技能通过 npm 安装 `cos-nodejs-sdk-v5`（腾讯云 COS 官方 Node.js SDK），安装到项目本地 `node_modules/`，不执行全局安装。

## 分页与全量查询规范

任何列表/检索类接口都可能分页返回。**不得把第一页（或任何单页）结果说成「全部」，也不得隐去「还有后续数据」这一事实**：

1. **如实呈现分页状态**：响应中出现 `isTruncated: true`、`nextMarker`、`NextToken` / `nextToken`、`hasMore: true` 任一标志时，必须向用户明确说明——本次只返回了部分结果（已返回 N 条），还有更多数据可翻页；不得省略或弱化。
2. **禁止以偏概全**：只有确认翻完所有页（最后一页无续页标志）后，才能使用「全部」「共 X 个」这类全量表述；单页结果只能说「前 N 条」或「当前页 N 条」。
3. **用户要「全部」时必须翻页拉全**：用返回的 `nextMarker`（`list --marker`）或 `NextToken`（`dataset-simple-query --next-token`、`simple-query --body` 内 `NextToken`、`list-datasets --nexttoken`）循环请求，直到无续页标志。统计类需求（多少个、类型分布、总大小等）优先改走 `Aggregations` 聚合，让服务端全量统计，不逐页拉文件。
4. **安全上限**：循环翻页设上限（默认 1000 条 / 10 页），达到上限时停止并向用户如实说明：已拉取 X 条且仍有后续，建议缩小范围、加大单页 `--max-keys` / `MaxResults`，或改用聚合统计；若用户要对这些结果做批量操作，按「操作数量过多时引导控制台」处理。
5. **分页参数透传**：翻页时保持查询条件（`--prefix`、`Query`、排序等）与首页一致，只追加分页 token，避免每页筛选条件不一致导致漏数据或重复。

## 操作数量过多时引导控制台

当用户需求的操作对象数量过多、不适合由本 Skill 逐条执行时，**不要在 CLI 里硬扛**，主动说明并引导到控制台批量能力：

- **触发标准**（满足其一即建议引导）：
  - 批量删除 / 批量上传 / 批量复制超过 100 个对象；
  - 批量数据处理（转码、水印、恢复归档等）超过 50 个对象；
  - 按分页拉全数据已超过安全上限（1000 条），且用户仍要逐条处理；
  - 清空存储桶、按前缀全量删除等大规模删除操作——一律引导控制台，本 Skill 不执行。
- **引导方式**：如实说明当前规模下逐条执行耗时且易出错，控制台批量处理（或数据迁移）更高效；按 `references/console-feature-guides.md` 的「批量处理」「数据迁移」条目提供链接，并明确告知**本 Skill 未执行任何实际操作**。
- **严格模式（`KIKI=1`）下更不得以「批量」「用户要求」为由绕过删除限制**；大规模删除操作只能引导控制台由用户自行完成。
- 少量操作（如删除十几个文件）仍正常用 action 执行，不要动辄甩链接给用户。

## 使用规范

1. **首次使用先运行** `{baseDir}/scripts/setup.sh --check-only` 检查模式和环境；`KIKI=1` 时不展示或调用 `--from-env` / `--persist`
2. **所有文件路径**（`--key`）为存储桶内的相对路径，如 `images/photo.jpg`
3. **异步任务**（文档转换、视频封面）脚本会自动轮询结果，也可通过 `--job-id` 手动查询
4. **上传后主动获取链接**：上传完成后调用 `sign-url` 返回访问链接
5. **错误处理**：调用失败时先用 `{baseDir}/scripts/setup.sh --check-only` 诊断环境问题
6. **扩展 CI 能力**：通过 `ci-request` action 调用尚未封装的 CI API；严格模式禁止 `DELETE` 方法
7. **能力不足时引导**：确认现有能力无法满足后，按 `references/console-feature-guides.md` 查找匹配功能并提供控制台链接
8. **脚本源码**见 `scripts/cos_node.mjs`
9. **命令参考**见 `references/api_reference.md`
