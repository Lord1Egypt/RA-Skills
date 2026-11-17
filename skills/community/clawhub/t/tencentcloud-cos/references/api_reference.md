# COS Node.js SDK 操作参考

本文档提供 `scripts/cos_node.mjs` 常用与扩展操作的参数参考；完整 action 列表以 CLI 帮助输出和 `SKILL.md` 功能表为准。

**环境设置**：首次使用请运行 `{baseDir}/scripts/setup.sh --check-only`；需要安装和配置时再运行 `--from-env`，详见 `SKILL.md` 首次使用章节。

**官方文档链接：**
- COS Node.js SDK: https://cloud.tencent.com/document/product/436/8629
- 数据万象(CI): https://cloud.tencent.com/document/product/460
- cos-nodejs-sdk-v5 GitHub: https://github.com/tencentyun/cos-nodejs-sdk-v5

---

## 通用说明

所有命令格式：`node scripts/cos_node.mjs <action> [--option value ...]`

- 输出统一为 JSON 格式
- `success: true` 表示成功，退出码 0
- `success: false` 表示失败，退出码 1
- 所有 `--key` 参数为存储桶内的相对路径，如 `images/photo.jpg`

---

## COS 存储操作

### upload — 上传本地文件
- `--file` (string, **必需**): 本地文件路径
- `--key` (string, 可选): 存储桶中的对象键，默认使用文件名

### put-string — 上传字符串内容
- `--content` (string, **必需**): 要上传的字符串内容
- `--key` (string, **必需**): 存储桶中的对象键
- `--content-type` (string, 可选): MIME 类型，默认 `text/plain`

### download — 下载文件
- `--key` (string, **必需**): 存储桶中的对象键
- `--output` (string, 可选): 本地保存路径，默认使用文件名

### list — 列出文件
- `--prefix` (string, 可选): 路径前缀过滤
- `--max-keys` (number, 可选): 最大返回数量，默认 100
- `--marker` (string, 可选): 翻页起点，传入上一页返回的 `nextMarker` 续页；`isTruncated: true` 表示还有更多数据

### sign-url — 获取签名下载链接
- `--key` (string, **必需**): 存储桶中的对象键
- `--expires` (number, 可选): 签名有效期（秒），默认 3600

### head — 查看文件元信息
- `--key` (string, **必需**): 存储桶中的对象键

### delete — 删除文件
- `--key` (string, **必需**): 存储桶中的对象键

---

## COS 补充只读查询

以下 action 均可使用全局 `--bucket`、`--region` 覆盖默认存储桶和地域。

### 存储桶配置查询

- 无额外必选参数：`get-bucket-policy`、`get-bucket-replication`、`get-bucket-website`、`get-bucket-referer`、`get-bucket-domain`、`get-bucket-origin`、`get-bucket-logging`、`get-bucket-accelerate`、`get-bucket-encryption`、`get-bucket-access-monitor`、`get-bucket-logging-analysis`、`get-bucket-notification`、`get-bucket-object-lock`、`get-bucket-strict-signature`、`get-bucket-bandwidth-quota`、`get-bucket-response-control`。
- `get-bucket-inventory`：`--id` (string, **必需**)，查询指定清单任务。
- `list-bucket-inventory`：`--continuation-token` (string, 可选)，分页列出清单任务。
- `get-bucket-intelligent-tiering`：`--id` (string, 可选)，传入时查询指定规则，不传时列出规则。
- `get-bucket-domain-certificate`：`--domain` (string, **必需**)，查询指定自定义域名的证书配置。

### 对象与分块上传查询

- `list-object-versions`：可选 `--prefix`、`--delimiter`、`--key-marker`、`--version-id-marker`、`--max-keys`、`--encoding-type`。
- `get-object-acl`、`get-object-tagging`、`get-object-retention`、`get-symlink`：`--key` (string, **必需**)，可选 `--version-id`。
- `list-multipart-uploads`：可选 `--prefix`、`--delimiter`、`--key-marker`、`--upload-id-marker`、`--max-uploads`、`--encoding-type`。
- `list-multipart-parts`：`--key`、`--upload-id` (string, **必需**)，可选 `--part-number-marker`、`--max-parts`、`--encoding-type`。
- `options-object`：`--key`、`--origin`、`--request-method` (string, **必需**)，可选 `--request-headers`，用于查询对象的 CORS 预检响应。

---

## CI 图片基础处理

### image-info — 获取图片元数据
- `--key` (string, **必需**): 图片在存储桶中的路径

### watermark-font — 添加文字水印
- `--key` (string, **必需**): 图片在存储桶中的路径
- `--text` (string, **必需**): 水印文字内容（支持中文）

处理后的图片存储到同一存储桶，文件名格式 `{date}_{原名}_{随机码}`。

---

## CI AI 图片处理

### assess-quality — 图片质量评估
- `--key` (string, **必需**): 图片在存储桶中的路径

返回图片质量评分。

### ai-super-resolution — AI 超分辨率
- `--key` (string, **必需**): 图片在存储桶中的路径

处理后的高分辨率图片存储到同一存储桶。

### ai-pic-matting — AI 智能裁剪
- `--key` (string, **必需**): 图片在存储桶中的路径
- `--width` (string, 可选): 输出宽度
- `--height` (string, 可选): 输出高度

### ai-qrcode — 二维码识别
- `--key` (string, **必需**): 含二维码的图片路径

返回识别到的二维码内容。

---

## CI 文档处理

### create-doc-to-pdf-job — 文档转 PDF
- `--key` (string, **必需**): 文档在存储桶中的路径（支持 docx/xlsx/pptx 等）

提交异步任务，脚本自动轮询（最多 10 次，间隔 2 秒）等待结果。转换后的 PDF 存储到同一存储桶。

### describe-doc-job — 查询文档处理任务
- `--job-id` (string, **必需**): 任务 ID

---

## CI 媒体处理

### create-media-smart-cover-job — 视频智能封面
- `--key` (string, **必需**): 视频在存储桶中的路径

提交异步任务，脚本自动轮询（最多 10 次，间隔 4 秒）等待结果。

### describe-media-job — 查询媒体处理任务
- `--job-id` (string, **必需**): 任务 ID

---

## CI MetaInsight（以图搜图/文本搜图）

数据集按 `--dataset`、`TENCENT_COS_DATASET_IMAGE_SEARCH`、`TENCENT_COS_DATASET_NAME` 的顺序选择。

### image-search-pic — 以图搜图
- `--uri` (string, **必需**): 查询图片地址

### image-search-text — 文本搜图
- `--text` (string, **必需**): 检索文本

---

## CI 服务生命周期管理

所有命令都需要 `--bucket <BucketName-APPID>` 和 `--region <Region>`。服务状态统一通过 `ci-service-status` 查询。

| 服务 | 开通 action | 请求 | 关闭 action | 请求 |
| --- | --- | --- | --- | --- |
| 数据万象绑定 | `create-ci-bucket` | `PUT /`，CAM `ci:CreateCIBucket` | `delete-ci-bucket` | `PUT /?unbind`，CAM `ci:DeleteCIBucket` |
| 文档处理 | `create-doc-process-bucket` | `POST /docbucket`，CAM `ci:CreateDocProcessBucket` | `delete-doc-process-bucket` | `DELETE /docbucket`，CAM `ci:DeleteDocProcessBucket` |
| 媒体处理 | `create-media-bucket` | `POST /mediabucket`，CAM `ci:CreateMediaBucket` | `delete-media-bucket` | `DELETE /mediabucket`，CAM `ci:DeleteMediaBucket` |
| 智能语音 | `create-asr-bucket` | `POST /asrbucket`，CAM `ci:CreateAsrBucket` | `delete-asr-bucket` | `DELETE /asrbucket`，CAM `ci:DeleteAsrBucket` |
| 文件处理 | `create-file-process-bucket` | `POST /file_bucket`，CAM `ci:CreateFileProcessBucket` | `delete-file-process-bucket` | `DELETE /file_bucket`，CAM `ci:DeleteFileProcessBucket` |

请求域名均为 `https://<bucket>.ci.<region>.myqcloud.com`。所有 `delete-*` action 在严格模式下隐藏并拒绝执行；其中 `delete-ci-bucket` 虽使用 `PUT`，仍按解绑删除语义保护。

---

## CI 图片处理（异步）服务管理

同步图片处理只要存储桶绑定 CI 即默认可用；以下接口仅管理需要独立开通的异步图片处理服务。

### describe-async-image-process-buckets — 查询已开通服务的存储桶

- `--region` (string, **必需**): 地域
- `--bucket` (string, 可选): 精确查询的存储桶，未传 `--bucket-names` 时作为默认值
- `--bucket-names` (string, 可选): 逗号分隔的存储桶名称，精确搜索
- `--bucket-name` (string, 可选): 存储桶名称前缀
- `--page-number` (integer, 可选): 页码，默认 `1`
- `--page-size` (integer, 可选): 每页数量，范围 `1~100`，默认 `10`

调用 `GET https://ci.<region>.myqcloud.com/picbucket`，CAM Action 为 `ci:DescribePicProcessBucket`。

### create-async-image-process-bucket — 开通服务

- `--bucket` (string, **必需**): 存储桶名称，格式为 `<BucketName-APPID>`
- `--region` (string, **必需**): 地域

调用 `POST https://<bucket>.ci.<region>.myqcloud.com/picbucket`，开通异步图片处理服务并创建队列。CAM Action 为 `ci:CreatePicProcessBucket`。

### delete-async-image-process-bucket — 关闭服务

- `--bucket` (string, **必需**): 存储桶名称，格式为 `<BucketName-APPID>`
- `--region` (string, **必需**): 地域

调用 `DELETE https://<bucket>.ci.<region>.myqcloud.com/picbucket`，关闭异步图片处理服务并删除队列。CAM Action 为 `ci:DeletePicProcessBucket`。该 action 在严格模式下隐藏并拒绝执行。

---

## CI AI 内容识别（异步）服务管理

同步内容识别在存储桶绑定 CI 后默认可用；以下接口仅管理需要独立开通的 AI 内容识别异步服务。

### describe-ai-process-buckets — 查询已开通服务的存储桶

- `--region` (string, **必需**): 地域
- `--bucket` (string, 可选): 精确查询的存储桶，未传 `--bucket-names` 时作为默认值
- `--bucket-names` (string, 可选): 逗号分隔的存储桶名称，精确搜索
- `--bucket-name` (string, 可选): 存储桶名称前缀
- `--page-number` (integer, 可选): 页码，默认 `1`
- `--page-size` (integer, 可选): 每页数量，范围 `1~100`，默认 `10`

调用 `GET https://ci.<region>.myqcloud.com/ai_bucket`，CAM Action 为 `ci:DescribeAiProcessBucket`。

### create-ai-process-bucket — 开通服务

- `--bucket` (string, **必需**): 存储桶名称，格式为 `<BucketName-APPID>`
- `--region` (string, **必需**): 地域

调用 `POST https://<bucket>.ci.<region>.myqcloud.com/ai_bucket`，开通 AI 内容识别异步服务并创建队列。CAM Action 为 `ci:CreateAiProcessBucket`。

### delete-ai-process-bucket — 关闭服务

- `--bucket` (string, **必需**): 存储桶名称，格式为 `<BucketName-APPID>`
- `--region` (string, **必需**): 地域

调用 `DELETE https://<bucket>.ci.<region>.myqcloud.com/ai_bucket`，关闭服务并删除队列。CAM Action 为 `ci:DeleteAiProcessBucket`。该 action 在严格模式下隐藏并拒绝执行。

---

## CI 通用请求（扩展入口）

### ci-request — 通用 CI API 请求

用于调用尚未封装为独立 action 的 CI 能力（如内容审核、文件处理等）。

- `--method` (string, 可选): HTTP 方法，默认 `GET`；严格模式禁止 `DELETE`
- `--path` (string, **必需**): CI API 路径，如 `image/auditing`、`file_jobs`、`jobs`
- `--body` (string, 可选): 请求体内容
- `--content-type` (string, 可选): 请求体类型，默认 `application/xml`
- `--query` (string, 可选): 查询参数，JSON 字符串格式

请求自动发送到 `https://{Bucket}.ci.{Region}.myqcloud.com/{path}`。

**扩展示例：**

```bash
# 内容审核 — 提交图片审核任务
ci-request --method POST --path "image/auditing" --body '<Request><Input><Object>images/test.jpg</Object></Input><Conf><BizType></BizType></Conf></Request>'

# 文件处理 — 提交文件哈希计算
ci-request --method GET --path "test.docx" --query '{"ci-process":"filehash","type":"md5"}'

# 查询任务结果
ci-request --method GET --path "file_jobs/<jobId>"
```
