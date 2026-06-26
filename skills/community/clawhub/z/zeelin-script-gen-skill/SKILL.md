---
name: zeelin-script-gen-skill-v4
description: "剧本生成技能V4，将文本文件（小说/故事）转换为完整的影视分镜剧本。当用户说'生成剧本'、'小说转剧本'、'创建分镜'、'影视改编'等并上传文本文件时使用此技能。"
metadata: { "openclaw": { "emoji": "📝", "requires": { "bins": ["python3"], "pip": ["flask", "requests", "oss2"] } } }
---

# 剧本生成技能 V4

## 技能说明

这个技能帮助用户将文本文件（小说、故事等）自动转换为完整的影视分镜剧本，包括角色档案、剧集大纲和分镜脚本。

**功能**：将文本内容自动转换为结构化的影视分镜剧本。

---

## 使用方法

> **注意**：以下示例使用 `curl` 展示请求格式，实际由 OpenClaw 工具调用执行，无需手动执行命令。

### 第一步：首次使用配置

使用本技能前，需要配置智灵平台的 App-Key。

**步骤 1：注册智灵账号**
- 访问 https://skills.zeelin.cn
- 点击注册，完成账号创建

**步骤 2：创建应用**
- 登录后进入控制台 → 应用管理
- 点击"创建应用"，填写应用名称
- 复制生成的 `App-Key`

**步骤 3：配置到技能**
- 打开本 Skill 的配置文件：`templates/config.json`
- 将复制的 `App-Key` 粘贴到 `Zeelin_App_Key` 字段
- 保存文件，重新触发本技能即可使用

配置示例：
```json
{
  "Zeelin_App_Key": "xxxxxxxxxxxxxxxxxxx",
  "Zeelin_Api_Url": "https://skills.zeelin.cn",
  "Zeelin_Website_Url": "https://skills.zeelin.cn",
  "service_url": "http://47.98.180.113:8081"
}
```

---

### 第二步：上传文本文件到 OSS

**接口**: `POST {service_url}/api/skill/upload`

**请求格式**: `multipart/form-data` (不是 JSON！)

**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| appKey | form-data | string | 是 | 用户的 Zeelin_App_Key |
| file | form-data | file | 是 | 本地文本文件二进制数据 |

**示例请求**:
```bash
curl -X POST "http://47.98.180.113:8081/api/skill/upload" \
  -F "appKey=YOUR_APP_KEY" \
  -F "file=@/path/to/novel.txt"
```

**成功响应**:
```json
{
  "code": 200,
  "data": {
    "oss_url": "https://jumuai.oss-cn-hangzhou.aliyuncs.com/...",
    "filename": "novel.txt",
    "size": 123456
  }
}
```

⚠️ **文件限制**：
- 最大 50MB
- 格式：PDF、DOCX、TXT、MD

---

### 第三步：提交剧本生成任务

**接口**: `POST {service_url}/api/skill/script`

**请求格式**: `application/json`

**Header**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| App-Key | string | 是 | 用户的智灵应用 Key |

**Body 参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| oss | string | 是 | 上传后返回的 OSS 文件链接 |
| episode_duration_minutes | int | 否 | 每集时长（分钟），默认 2 |
| episode_count_min | int | 否 | 最少集数，默认 10 |
| episode_count_max | int | 否 | 最多集数，默认 15 |

**示例请求**:
```bash
curl -X POST "http://47.98.180.113:8081/api/skill/script" \
  -H "Content-Type: application/json" \
  -H "App-Key: YOUR_APP_KEY" \
  -d '{
    "oss": "https://jumuai.oss-cn-hangzhou.aliyuncs.com/...novel.txt",
    "episode_duration_minutes": 2,
    "episode_count_min": 10,
    "episode_count_max": 15
  }'
```

**成功响应**:
```json
{
  "code": 200,
  "message": "任务已提交，处理中",
  "data": {
    "task_id": "script_xxx",
    "status": "pending"
  }
}
```

---

### 第四步：轮询查询任务状态（必须执行）

⚠️ **剧本生成时间较长，请耐心等待！**

**轮询策略**（根据进度动态调整，节省额度）：

| 当前进度 | 查询间隔 | 说明 |
|---------|---------|------|
| **< 70%**（33% 人物提取、66% 大纲审核） | **每 3 分钟** | 处理初期和中期，耐心等待 |
| **≥ 70%**（接近 100% 完成） | **每 1 分钟** | 接近完成，缩短间隔及时获取结果 |
| **最多轮询 40 分钟** | - | 长文本可能需要较长时间 |

⚠️ **费用提示**：剧本生成涉及多次 AI 调用，使用智灵模型时频繁查询会产生费用，建议严格按上述间隔查询。

**告诉用户的提示语**：
- 提交时："剧本生成任务已提交，预计处理 15-30 分钟，请稍候..."
- 33% 时："当前进度 33%，人物提取完成，正在审核大纲..."
- 66% 时："当前进度 66%，大纲审核完成，正在生成分镜剧本..."
- 完成时："剧本生成完成！"并展示 result

**示例指令（模型执行）**：
```
# 第一次查询（提交后立即）
curl "http://47.98.180.113:8081/api/skill/status/script_xxx"
→ 返回 progress=33（人物提取完成）
→ 告诉用户："当前进度 33%，人物提取完成，正在审核大纲..."
→ sleep 180  # 等待 3 分钟

# 第二次查询
curl "http://47.98.180.113:8081/api/skill/status/script_xxx"
→ 返回 progress=66（大纲审核完成）
→ 告诉用户："当前进度 66%，大纲审核完成，正在生成分镜..."
→ sleep 180  # 等待 3 分钟

# 第三次查询
curl "http://47.98.180.113:8081/api/skill/status/script_xxx"
→ 返回 progress=100, status=succeeded
→ 告诉用户："剧本生成完成！"并展示结果
  最后生成一个 md 文件来让用户进行查看
```

---

## 结果展示格式（Markdown）

⚠️ **重要：获取到 result 后，必须将结果格式化为 Markdown 展示给用户，不要直接返回原始 JSON！**

**格式化要求**：
- 使用 Markdown 标题层级（# ## ###）组织内容
- 使用表格展示结构化数据
- 添加适当的 emoji 图标增强可读性
- 根据实际返回的数据结构灵活调整格式
- 如果某些字段为空，可以省略对应章节
- **不要编造数据**，只展示 result 中实际存在的内容
- 最后给用户呈现结果时生成一个 md 文件来让用户进行查看

**展示内容顺序**：

1. **📌 标题和基本信息**
   - 作品标题
   - 总集数

2. **👥 角色档案**
   - 角色名称、角色定位（男主/女主/配角等）
   - 角色描述（外貌、性格、特点）

3. **📋 剧集大纲**
   - 题材类型
   - 世界观设定
   - 每集的故事节拍、大事件、关键冲突与转折

4. **🎬 分镜剧本（展示前 2-3 个分镜）**
   - 分场信息
   - 情绪曲线
   - 每个镜头的场景、画面描述、台词、角色

---

## 完整调用流程

```
用户: "生成剧本" + 上传文本文件
  ↓
OpenClaw: 读取本地文本文件
  ↓
OpenClaw: 1️⃣ POST {service_url}/api/skill/upload
          Content-Type: multipart/form-data
          Body: appKey=xxx&file=文件二进制
  ↓
Skill服务: 接收文件 → 上传OSS → 返回 oss_url
  ↓
OpenClaw: 2️⃣ POST {service_url}/api/skill/script
          Headers: App-Key={Zeelin_App_Key}
          Content-Type: application/json
          Body: {"oss": "...", "episode_duration_minutes": 2, "episode_count_min": 10, "episode_count_max": 15}
  ↓
Skill服务: 验证额度 → 扣费 → 提交AI任务 → 返回 task_id
  ↓
OpenClaw: 3️⃣ 轮询 GET {service_url}/api/skill/status/{task_id}
          根据进度动态间隔查询（3分钟/1分钟）
  ↓
OpenClaw: 展示剧本生成结果给用户（Markdown 格式）
```

---

## 费用说明

| 服务类型 | 计费标准 | 示例 |
|---------|---------|------|
| 剧本生成 | 120额度/万字 | 8000字=120额度，15000字=240额度 |

**计费规则**：
- 按字数向上取整到万字（如8500字按1万字计）
- 提交任务时扣除额度，任务失败自动返还
- 额度从您的智灵账户中扣除

---

## 常见问题

**Q: App-Key 格式是什么？**  
A: 任意字符串，从 config.json 的 `Zeelin_App_Key` 字段读取。

**Q: 上传接口的 appKey 放哪里？**  
A: 放在 form-data 里（`appKey=xxx`），不是 Header！

**Q: 支持多大的文本文件？**  
A: 单文件最大 50MB。

**Q: 支持哪些文本格式？**  
A: PDF、DOCX、TXT、MD。

**Q: 任务失败会扣费吗？**  
A: 不会。任务失败时自动返还已扣除的额度。

**Q: 上传的文件会保留吗？**  
A: 临时文件上传到服务器配置的 OSS，24 小时后自动过期清理。

---

## 技术支持

- 智灵官网：https://skills.zeelin.cn
