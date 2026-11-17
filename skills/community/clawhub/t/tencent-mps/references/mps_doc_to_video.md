# AIGC 文档生成视频参数与示例 — `mps_doc_to_video.py`

**功能**：将 PDF / PPTX / DOCX / PNG / JPG 文档自动生成讲解视频，适用于教学视频、产品讲解、内容速览等场景。
> ⚠️ 未配置 COS 存储时使用 MPS 临时存储，链接有效期有限，请尽快下载使用。

---

## 🛑 生成命令前的强制前置检查（在写任何命令之前必须先做）

**规则**：以下三项参数越界时，**绝对禁止生成任何命令**，必须先向用户追问。**即使用户明确要求"直接生成"、"就这么执行"，也必须先追问**。

| 参数 | 合法范围 | 越界时的必答追问 |
|---|---|---|
| `--url` / `--local-file` 合计 | 最多 **3 个** | "文档最多 3 个，您希望保留哪 3 份？" |
| `--aspect-ratio` | 只能是 `16:9` / `9:16` / `1:1` | "宽高比仅支持 16:9 / 9:16 / 1:1，您希望使用哪个？" |
| `--reference-duration` | `[15, 1200]` 秒 | "参考时长需要在 15~1200 秒之间，您希望设为多少？" |

### 越界场景正反例（务必按此模式回答）

**❌ 错误示范**（越界但仍然生成命令）：
```
用户："把这份文档转成 4:3 的视频"
错误回答：python3 scripts/mps_doc_to_video.py --url ... --aspect-ratio 4:3
```

**✅ 正确示范**（越界时先追问、不生成命令）：
```
用户："把这份文档转成 4:3 的视频"
正确回答：宽高比仅支持 16:9 / 9:16 / 1:1，4:3 不在支持范围内，您希望使用哪个？
（不生成任何 python3 命令）
```

**❌ 错误示范**：
```
用户："把这份文档转成 5 秒短视频"
错误回答：python3 scripts/mps_doc_to_video.py --url ... --reference-duration 5
```

**✅ 正确示范**：
```
用户："把这份文档转成 5 秒短视频"
正确回答：参考时长需要在 15~1200 秒之间，5 秒低于下限，您希望设为多少？
（不生成任何 python3 命令）
```

**❌ 错误示范**：
```
用户："把这 4 份文档合并生成一个视频：a.pdf、b.pptx、c.docx、d.png"
错误回答：python3 scripts/mps_doc_to_video.py --url a.pdf --url b.pptx --url c.docx --url d.png
错误回答：python3 scripts/mps_doc_to_video.py --url a.pdf --url b.pptx --url c.docx （擅自丢弃 d.png）
```

**✅ 正确示范**：
```
用户："把这 4 份文档合并生成一个视频"
正确回答：文档最多支持 3 个，您提供了 4 份，希望保留哪 3 份？
（不生成任何 python3 命令）
```

---

## 参数说明

| 参数 | 说明 |
|------|------|
| `--url` | 文档 URL（**可多次指定，最多 3 个**）。支持 pdf/pptx/docx/png/jpg，单个不超过 10MB，最多 100 页 |
| `--local-file` | 本地文档路径（可多次指定），脚本自动上传到 COS 后生成预签名 URL 传入 API。需配置 `TENCENTCLOUD_COS_BUCKET` 或 `--output-bucket` |
| `--prompt` | 生成视频的描述文本（**必填**，最多 2000 字符）|
| `--model-name` | 文档生成视频模型名称，默认 `Wand` |
| `--model-version` | 模型版本号，默认 `1.0` |
| `--aspect-ratio` | 生成视频宽高比：`16:9`（默认）/ `9:16` / `1:1` |
| `--language` | 生成视频语言：`zh`（默认）/ `en` / `ja` / `ko` / `ru` / `fr` / `es` / `de` |
| `--reference-duration` | 生成视频的时长参考（秒），取值范围 `[15, 1200]`，仅供大模型参考，非精确时长 |
| `--enable-tts` | 开启 AI 配音功能 |
| `--voice-id` | AI 配音音色 ID（仅 `--enable-tts` 时生效，不传则使用平台默认音色）|
| `--no-wait` | 只提交任务，不等待结果 |
| `--task-id` | 查询已有任务结果 |
| `--output-bucket` | 结果存储 COS Bucket（不配置则使用 MPS 临时存储）|
| `--output-region` | 结果存储 COS 区域 |
| `--output-dir` | 结果存储 COS 路径前缀，默认 `/output/doc-to-video/` |
| `--download-dir` | 任务完成后将生成视频下载到指定本地目录（默认仅打印链接）|
| `--poll-interval` | 轮询间隔（秒），默认 10 |
| `--max-wait` | 最长等待时间（秒），默认 1800 |
| `--verbose` / `-v` | 输出详细信息 |
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）|
| `--dry-run` | 只打印参数，不调用 API |

## ⚠️ 强制规则（违反将导致命令执行失败）

- **文档数量限制**：`--url` / `--local-file` 合计最多 **3 个**，超出必须拒绝并提示用户精简文档数量（**见文首「越界处理规则」**）。
- **单文档大小限制**：单个文档不超过 **10MB**，最多 **100 页**；`--local-file` 本地文件超限时脚本会直接报错退出。
- **`--prompt` 必填**：未提供 prompt 时必须先询问用户希望生成的视频内容/用途描述，不得留空或使用占位符。
- **`--aspect-ratio` / `--language` 严格枚举校验**：只能是文档中列出的取值，传入其他值脚本会报错退出（**见文首「越界处理规则」**）。
- **`--reference-duration` 范围限制**：仅接受 `[15, 1200]` 秒，超出范围脚本会报错退出；该参数只是"参考"，最终生成时长由模型决定，不能保证精确匹配（**见文首「越界处理规则」**）。
- **`--enable-tts` 与 `--voice-id`**：开启配音但未指定音色时使用平台默认音色；如需指定音色，需先通过 `mps_dubbing.py` 的 `clone` 模式获取 `VoiceId`。
- **查询任务专用接口**：本任务类型没有独立的 DocToVideo 专属查询接口，脚本复用 `DescribeAigcTaskStatus` 查询结果，不能混用其他脚本查询本任务。
- **`--task-id` 与创建参数互斥**：`--task-id` 用于查询已有任务，不能与 `--url`/`--local-file`/`--prompt` 等创建类参数同时使用，否则脚本会报错退出。

```bash
# 单文档 + prompt（最简用法）
python3 scripts/mps_doc_to_video.py --url https://example.com/sample.pdf \
    --prompt "根据文档内容，帮我生成一个教学视频"
```

## 示例命令

```bash
# 多文档输入（最多3个，整合成一个视频）
python3 scripts/mps_doc_to_video.py \
    --url https://example.com/a.pdf --url https://example.com/b.pptx \
    --prompt "帮我把这两份文档整合成一个产品介绍视频"

# 指定宽高比 + 语言 + 参考时长（竖屏 + 英文 + 参考60秒）
python3 scripts/mps_doc_to_video.py --url https://example.com/sample.docx \
    --prompt "生成一个产品介绍视频" --aspect-ratio 9:16 --language en --reference-duration 60

# 开启 AI 配音（指定音色 ID）
python3 scripts/mps_doc_to_video.py --url https://example.com/sample.pdf \
    --prompt "生成教学视频" --enable-tts --voice-id v1_shUQBcs3N6VrPd9RMTf50H7M5kxeZ1VHIiWGDzq5Q9pE0HoEQ959hpulWHGFZSp3v4w=

# 本地文档（自动上传到 COS 后传入 API）
python3 scripts/mps_doc_to_video.py --local-file /path/to/sample.pdf \
    --prompt "生成教学视频"

# 结果存储到用户自己的 COS 桶（永久保存）
python3 scripts/mps_doc_to_video.py --url https://example.com/sample.pdf \
    --prompt "生成宣传片" --output-bucket mybucket-125xxx --output-region ap-guangzhou

# 任务完成后自动下载到本地目录
python3 scripts/mps_doc_to_video.py --url https://example.com/sample.pdf \
    --prompt "生成教学视频" --download-dir ./output

# 仅提交任务不等待
python3 scripts/mps_doc_to_video.py --url https://example.com/sample.pdf --prompt "生成视频" --no-wait

# 查询已有任务结果
python3 scripts/mps_doc_to_video.py --task-id e084efaa-d25a-xxxx-xxxx-6b85e473c0e5

# Dry Run（仅打印请求参数）
python3 scripts/mps_doc_to_video.py --url https://example.com/sample.pdf --prompt "测试" --dry-run
```
