---
name: zeelin-text-analysis-skill
description: "文本分析技能，支持本地文件直接上传分析。当用户说'分析文本'、'文本处理'、'分析这个文档'等并上传文本文件时使用此技能。"
metadata: { "openclaw": { "emoji": "📄", "requires": { "bins": ["python3"], "pip": ["flask", "requests", "oss2"] } } }
---

# 文本分析技能

## 技能说明

这个技能帮助用户分析文本文件，自动提取实体、生成关系图谱和角色档案。

**功能**：将小说、文档等文本内容转换为结构化的分析结果。

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
  "Zeelin_App_Key": "xxxxxxxxxxxxxxxxxx",
  "Zeelin_Api_Url": "https://skills.zeelin.cn",
  "Zeelin_Website_Url": "https://skills.zeelin.cn"
}
```

---

### 第二步：上传文件到 OSS

**接口**: `POST {service_url}/api/skill/upload`

**请求格式**: `multipart/form-data` (不是 JSON！)

**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| appKey | form-data | string | 是 | 用户的 Zeelin_App_Key |
| file | form-data | file | 是 | 本地文件二进制数据 |

**示例请求**:
```bash
curl -X POST "http://47.98.180.113:8083/api/skill/upload" \
  -F "appKey=YOUR_APP_KEY" \
  -F "file=@/path/to/local/file.txt"
```

**成功响应**:
```json
{
  "code": 200,
  "data": {
    "oss_url": "https://jumuai.oss-cn-hangzhou.aliyuncs.com/...",
    "filename": "file.txt",
    "size": 12345
  }
}
```

---

### 第三步：提交文本分析任务

**接口**: `POST {service_url}/api/skill/text`

**请求格式**: `application/json`

**参数**:
| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| appKey | JSON body | string | 是 | 用户的 Zeelin_App_Key |
| oss | JSON body | string | 是 | 上一步返回的 oss_url |

**示例请求**:
```bash
curl -X POST "http://47.98.180.113:8083/api/skill/text" \
  -H "Content-Type: application/json" \
  -d '{
    "appKey": "YOUR_APP_KEY",
    "oss": "https://jumuai.oss-cn-hangzhou.aliyuncs.com/..."
  }'
```

**成功响应**:
```json
{
  "code": 200,
  "data": {
    "task_id": "analysis_xxx",
    "status": "pending",
    "word_count": 3760,
    "cost": 1
  }
}
```

---

### 第四步：轮询查询任务状态（必须执行）

⚠️ **重要：提交任务后，必须通过工具调用查询接口获取结果，不能直接回复用户！**

**接口**: `GET {service_url}/api/skill/status/{task_id}`

**轮询策略**（根据进度动态调整，节省额度）：

| 当前进度 | 查询间隔 | 说明 |
|---------|---------|------|
| **≤ 60%**（25%, 50%, 60%） | **每 3 分钟** | 处理初期和中期，耐心等待 |
| **≥ 70%**（70%, 100%） | **每 1 分钟** | 接近完成，加密查询及时获取结果 |

**你必须这样做**：
1. 提交任务后，**立即告诉用户"任务已提交，预计处理 10-20 分钟，请稍候..."**
2. **根据返回的 `progress` 决定等待时间**：
   - `progress ≤ 60%` → **等待 3 分钟后查询**
   - `progress ≥ 70%` → **等待 1 分钟后查询**
3. 根据 `status` 判断：
   - `status: "pending"` → 继续轮询
   - `status: "succeeded"` → **展示 `result` 结果**（结束）
   - `status: "failed"` → **展示错误信息**（结束）
4. **最多轮询 30 分钟**，超时告诉用户"任务还在处理中，请稍后自行查询"

**示例指令（模型执行）**：
```
# 第一次查询（提交后立即）
curl "http://47.98.180.113:8083/api/skill/status/analysis_xxx"
→ 返回 progress=25
→ 告诉用户："当前进度 25%，处理中..."
→ 必须sleep 180  # 等待 3 分钟

# 第二次查询
curl "http://47.98.180.113:8083/api/skill/status/analysis_xxx"
→ 返回 progress=50
→ 告诉用户："当前进度 50%，继续处理中..."
→ 必须sleep 180  # 等待 3 分钟

# 第三次查询
curl "http://47.98.180.113:8083/api/skill/status/analysis_xxx"
→ 返回 progress=70
→ 告诉用户："即将完成，请稍候..."
→ 必须sleep 60   # 等待 1 分钟

# 第四次查询
curl "http://47.98.180.113:8083/api/skill/status/analysis_xxx"
→ 返回 progress=100, status=succeeded
  生成一个md文件来让用户进行查看
```


**示例请求**:
```bash
curl "http://47.98.180.113:8083/api/skill/status/analysis_xxx"
```

**响应字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | `pending`(处理中) / `succeeded`(成功) / `failed`(失败) |
| `progress` | int | 进度百分比: 0, 25, 50, 60, 70, 100 |
| `result` | object | **分析结果**（只有 status=succeeded 时才有） |
| `word_count` | int | 文档字数 |
| `cost` | int | 实际扣除额度 |

**轮询示例流程**：
```
提交任务 → 收到 25%
  ↓
告诉用户："任务已提交，预计处理 10-20 分钟，请稍候..."
  ↓
等待 3 分钟 → 查询 → 50%
  ↓
告诉用户："当前进度 50%，继续处理中..."
  ↓
等待 3 分钟 → 查询 → 60%
  ↓
告诉用户："即将完成，加密查询中..."
  ↓
等待 1 分钟 → 查询 → 70%
  ↓
等待 1 分钟 → 查询 → 100%（完成）
  ↓
告诉用户："分析完成！"生成一个md文件来让用户进行查看
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

## 完整调用流程

```
用户: "分析这个文档" + 上传文件
  ↓
OpenClaw: 读取本地文件
  ↓
OpenClaw: 1️⃣ POST {service_url}/api/skill/upload
          Content-Type: multipart/form-data
          Body: appKey=xxx&file=文件二进制
  ↓
Skill服务: 接收文件 → 上传OSS → 返回 oss_url
  ↓
OpenClaw: 2️⃣ POST {service_url}/api/skill/text
          Content-Type: application/json
          Body: {"appKey": "xxx", "oss": "oss_url"}
  ↓
Skill服务: 验证额度 → 扣费 → 提交AI任务 → 返回 task_id
  ↓
OpenClaw: 3️⃣ 轮询 GET {service_url}/api/skill/status/{task_id}
          根据进度动态间隔查询（3分钟/1分钟）
  ↓
OpenClaw: 生成md文件展示结果给用户
```

---

## 费用说明

| 服务类型 | 计费标准 | 示例 |
|---------|---------|------|
| 文本分析 | 120额度/万字 | 3760字=120额度 |

**计费规则**:
- 文本按字数向上取整到万字
- 提交任务时扣除额度，任务失败自动返还

---

## 常见问题

**Q: App-Key 格式是什么？**  
A: 任意字符串，从 config.json 的 `Zeelin_App_Key` 字段读取。

**Q: 上传接口的 appKey 放哪里？**  
A: 放在 form-data 里（`appKey=xxx`），不是 Header！

**Q: 分析接口的 appKey 放哪里？**  
A: 放在 JSON body 里（`{"appKey": "xxx"}`）。

**Q: 支持多大的文件？**  
A: 单文件最大 500MB。

**Q: 为什么查询任务状态也会产生扣费记录？**  
A: 使用智灵提供的模型时，每次调用（包括查询）都会经过智灵平台。查询虽然不扣技能额度，但会产生平台调用记录。建议按 SKILL.md 的轮询间隔查询，避免频繁调用。

---

## 技术支持

- 智灵官网：https://skills.zeelin.cn
