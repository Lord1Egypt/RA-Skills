---
name: zeelin-video-analysis-skill
description: "视频分析技能，支持本地视频文件直接上传分析。当用户说'分析视频'、'视频处理'、'分析这个视频'等并上传视频文件时使用此技能。"
metadata: { "openclaw": { "emoji": "🎬", "requires": {} } }
---

# 视频分析技能

## 技能说明

这个技能帮助用户分析视频文件，自动提取实体、生成关系图谱和角色档案。

**功能**：将视频内容（剧集、电影等）转换为结构化的分析结果。

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
  "Zeelin_Website_Url": "https://skills.zeelin.cn"
}
```

---

### 第二步：上传视频文件到 OSS

**接口**: `POST {service_url}/api/skill/upload`

**请求格式**: `multipart/form-data` (不是 JSON！)

**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| appKey | form-data | string | 是 | 用户的 Zeelin_App_Key |
| file | form-data | file | 是 | 本地视频文件二进制数据 |

**示例请求**:
```bash
curl -X POST "http://47.98.180.113:8083/api/skill/upload" \
  -F "appKey=YOUR_APP_KEY" \
  -F "file=@/path/to/local/video.mp4"
```

**成功响应**:
```json
{
  "code": 200,
  "data": {
    "oss_url": "https://jumuai.oss-cn-hangzhou.aliyuncs.com/...",
    "filename": "video.mp4",
    "size": 12345678
  }
}
```

⚠️ **视频文件限制**：
- 最大 500MB
- 格式：mp4, mov, avi 等常见格式

---

### 第三步：提交视频分析任务

**接口**: `POST {service_url}/api/skill/video`

**请求格式**: `application/json`

**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| appKey | JSON body | string | 是 | 用户的 Zeelin_App_Key |
| videos | JSON body | array | 是 | 视频列表，每项包含 sequence 和 oss |

**videos 数组格式**:
```json
[
  {"sequence": 1, "oss": "https://xxx.com/video1.mp4"},
  {"sequence": 2, "oss": "https://xxx.com/video2.mp4"}
]
```

**示例请求**:
```bash
curl -X POST "http://47.98.180.113:8083/api/skill/video" \
  -H "Content-Type: application/json" \
  -d '{
    "appKey": "YOUR_APP_KEY",
    "videos": [
      {"sequence": 1, "oss": "https://jumuai.oss-cn-hangzhou.aliyuncs.com/...video1.mp4"},
      {"sequence": 2, "oss": "https://jumuai.oss-cn-hangzhou.aliyuncs.com/...video2.mp4"}
    ]
  }'
```

**成功响应**:
```json
{
  "code": 200,
  "data": {
    "task_id": "analysis_xxx",
    "status": "pending",
    "video_count": 2,
    "total_duration": 45.5,
    "cost": 46
  }
}
```

---

### 第四步：轮询查询任务状态（必须执行）

⚠️ **视频处理时间更长，请耐心等待！**

**轮询策略**（视频处理更慢，间隔更疏）：

| 当前进度 | 查询间隔 | 说明 |
|---------|---------|------|
| **≤ 50%** | **每 5 分钟** | 视频处理较慢，前期耐心等待 |
| **> 50%** | **每 2 分钟** | 过半后关注进度直到完成 |
| **最多轮询 60 分钟** | - | 视频可能需要较长时间 |

⚠️ **费用提示**：视频处理时间长，使用智灵模型时频繁查询会产生较多费用，建议严格按上述间隔查询。

**告诉用户的提示语**：
- 提交时："视频分析任务已提交，共 N 集，预计处理 10-30 分钟/集，请耐心等待..."
- 轮询中："当前进度 XX%，视频分析中，请继续等待..."
- 完成时："视频分析完成！"并展示 result

**示例指令（模型执行）**：
```
# 第一次查询（提交后立即）
curl "http://47.98.180.113:8083/api/skill/status/analysis_xxx"
→ 返回 progress=25
→ 告诉用户："当前进度 25%，视频分析中..."
→ sleep 300  # 等待 5 分钟

# 第二次查询
curl "http://47.98.180.113:8083/api/skill/status/analysis_xxx"
→ 返回 progress=50
→ 告诉用户："当前进度 50%，继续处理中..."
→ sleep 300  # 等待 5 分钟

# 第三次查询
curl "http://47.98.180.113:8083/api/skill/status/analysis_xxx"
→ 返回 progress=70
→ 告诉用户："即将完成，请稍候..."
→ sleep 120  # 等待 2 分钟

# 第四次查询
curl "http://47.98.180.113:8083/api/skill/status/analysis_xxx"
→ 返回 progress=100, status=succeeded
→ 告诉用户："视频分析完成！"并展示结果
  最后生成一个md文件来让用户进行查看
```

---

## 结果展示格式（Markdown）

⚠️ **重要：获取到 result 后，必须将结果格式化为 Markdown 展示给用户，不要直接返回原始 JSON！**

**格式化要求**：
- 使用 Markdown 标题层级（# ## ###）组织内容
- 使用表格展示关系数据
- 添加适当的 emoji 图标增强可读性
- 根据实际返回的数据结构灵活调整格式
- 如果某些字段为空，可以省略对应章节
- **不要编造数据**，只展示 result 中实际存在的内容
- 最后给用户呈现结果时生成一个md文件来让用户进行查看

---

**接口和查询方法**：
```bash
curl "http://47.98.180.113:8083/api/skill/status/analysis_xxx"
```

---

## 完整调用流程

```
用户: "分析这个视频" + 上传视频
  ↓
OpenClaw: 读取本地视频文件
  ↓
OpenClaw: 1️⃣ POST {service_url}/api/skill/upload
          Content-Type: multipart/form-data
          Body: appKey=xxx&file=视频二进制
  ↓
Skill服务: 接收文件 → 上传OSS → 返回 oss_url
  ↓
OpenClaw: 2️⃣ POST {service_url}/api/skill/video
          Content-Type: application/json
          Body: {"appKey": "xxx", "videos": [...]}
  ↓
Skill服务: 验证额度 → 扣费 → 提交AI任务 → 返回 task_id
  ↓
OpenClaw: 3️⃣ 轮询 GET {service_url}/api/skill/status/{task_id}
          根据进度动态间隔查询（5分钟/2分钟）
  ↓
OpenClaw: 展示视频分析结果给用户
```

---

## 费用说明

| 服务类型 | 计费标准 | 示例 |
|---------|---------|------|
| 视频分析 | 2500额度/分钟 | 30秒=2500额度 |

**计费规则**:
- 视频按时长向上取整到分钟
- 提交任务时扣除额度，任务失败自动返还

---

## 常见问题

**Q: App-Key 格式是什么？**  
A: 任意字符串，从 config.json 的 `Zeelin_App_Key` 字段读取。

**Q: 上传接口的 appKey 放哪里？**  
A: 放在 form-data 里（`appKey=xxx`），不是 Header！

**Q: 支持多大的视频文件？**  
A: 单文件最大 500MB。

**Q: 支持哪些视频格式？**  
A: mp4, mov, avi 等常见格式。

---

## 技术支持

- 智灵官网：https://skills.zeelin.cn
