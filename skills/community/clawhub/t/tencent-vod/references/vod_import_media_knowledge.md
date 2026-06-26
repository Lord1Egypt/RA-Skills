# vod_import_media_knowledge — 详细参数与示例
> 此文件由 references 拆分生成，对应脚本：`scripts/vod_import_media_knowledge.py`

### ⚠️ 常见参数错误

| 错误用法 | 正确用法 | 说明 |
|---------|---------|------|
| `vod_import_media_to_trtc_knowledge.py ...` | `vod_import_media_knowledge.py import --file-id <id>` | 知识库导入脚本名是 `vod_import_media_knowledge.py` |

## 参数说明


### import 子命令参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--sub-app-id` | int | ✅ | 点播应用 ID（也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--file-id` | string | ✅ | 媒体文件 ID |
| `--definition` | int | - | 大模型理解模板 ID（默认 100，包含音频级别的摘要和 ASR） |
| `--region` | string | - | 地域（默认 `ap-guangzhou`） |
| `--no-wait` | flag | - | 仅提交任务，不等待结果（默认自动等待） |
| `--max-wait` | int | - | 最大等待时间（秒，默认 600） |
| `--json` | flag | - | JSON 格式输出完整响应 |
| `--dry-run` | flag | - | 预览请求参数，不实际执行 |

### batch 子命令参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--sub-app-id` | int | ✅ | 点播应用 ID（也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--file-ids` | string[] | ✅ | 媒体文件 ID 列表（空格分隔） |
| `--definition` | int | - | 大模型理解模板 ID（默认 100，包含音频级别的摘要和 ASR） |
| `--region` | string | - | 地域（默认 `ap-guangzhou`） |
| `--json` | flag | - | JSON 格式输出完整结果 |
| `--dry-run` | flag | - | 预览请求参数，不实际执行 |

### 预置模板说明

| 模板 ID | 说明 |
|---------|------|
| 100 | 音频级别的摘要和 ASR（语音识别），默认模板 |

### 错误码说明

| 错误类型 | 原因 | 处理建议 |
|---------|------|---------|
| InvalidParameterValue.FileId | 文件 ID 无效 | 检查 FileId 是否正确 |
| InvalidParameterValue.Definition | 模板 ID 无效 | 使用有效的模板 ID（默认 100） |
| ResourceNotFound | 资源不存在 | 检查文件是否存在 |
| FailedOperation | 操作失败 | 检查账户权限和余额 |
| LimitExceeded | 频率限制 | 默认 20次/秒 |

---


---


## 使用示例


### 基础导入

#### 导入单个媒体到知识库（默认模板 100）
```bash
python scripts/vod_import_media_knowledge.py import \
    --sub-app-id 1500046806 \
    --file-id 5285485487985271487
```

#### 指定大模型理解模板
```bash
python scripts/vod_import_media_knowledge.py import \
    --sub-app-id 1500046806 \
    --file-id 5285485487985271487 \
    --definition 100
```

#### 导入并等待任务完成
```bash
python scripts/vod_import_media_knowledge.py import \
    --sub-app-id 1500046806 \
    --file-id 5285485487985271487 \

```

#### 导入并输出 JSON 格式结果
```bash
python scripts/vod_import_media_knowledge.py import \
    --sub-app-id 1500046806 \
    --file-id 5285485487985271487 \
    --json
```

#### 预览请求参数（不实际执行）
```bash
python scripts/vod_import_media_knowledge.py import \
    --sub-app-id 1500046806 \
    --file-id 5285485487985271487 \
    --dry-run
```

---

### 批量导入

#### 批量导入多个媒体文件
```bash
python scripts/vod_import_media_knowledge.py batch \
    --sub-app-id 1500046806 \
    --file-ids 528548548798527148 528548548798527149 528548548798527150
```

#### 批量导入并输出 JSON 结果
```bash
python scripts/vod_import_media_knowledge.py batch \
    --sub-app-id 1500046806 \
    --file-ids 528548548798527148 528548548798527149 \
    --definition 100 \
    --json
```

#### 批量导入预览
```bash
python scripts/vod_import_media_knowledge.py batch \
    --sub-app-id 1500046806 \
    --file-ids 528548548798527148 528548548798527149 \
    --dry-run
```

---

### 模板管理

#### 列出可用的大模型理解模板
```bash
python scripts/vod_import_media_knowledge.py templates
```

#### 列出模板（指定子应用 ID）
```bash
python scripts/vod_import_media_knowledge.py templates \
    --sub-app-id 1500046806
```

> 📌 **规则**：`templates` 子命令支持 `--sub-app-id` 参数。若用户在请求中提供了子应用 ID，**必须**将其作为 `--sub-app-id` 传入，不得忽略。

---

### 组合使用示例

#### 上传视频后导入知识库
```bash
#!/bin/bash
# 1. 上传视频
RESULT=$(python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --sub-app-id 1500046806 \
    --json)
FILE_ID=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('FileId',''))")

# 2. 导入到知识库
if [ -n "$FILE_ID" ]; then
    python scripts/vod_import_media_knowledge.py import \
        --sub-app-id 1500046806 \
        --file-id "$FILE_ID" \

fi
```

#### 批量导入目录下所有已上传的文件
```bash
#!/bin/bash
SUB_APP_ID=1500046806
FILE_IDS="528548548798527148 528548548798527149 528548548798527150"

python scripts/vod_import_media_knowledge.py batch \
    --sub-app-id $SUB_APP_ID \
    --file-ids $FILE_IDS \
    --definition 100 \
    --json
```

---

