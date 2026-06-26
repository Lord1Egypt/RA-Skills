# 每日 AI 新闻 TOP3 - 操作 SOP

## API Keys
- TAVILY_API_KEY: 从环境变量读取 (`$env:TAVILY_API_KEY`)

## 飞书配置
- 用户 open_id: ou_e3a0d4a64a9e0932ee919b97f17ec210（Thomas）

## 执行流程

### 步骤 1：确定搜索日期
- 获取当前日期
- 计算前一天日期
- 格式化：YYYY 年 MM 月 DD 日

**PowerShell 示例：**
```powershell
$yesterday = (Get-Date).AddDays(-1)
$dateString = $yesterday.ToString("MMMM dd yyyy")
# 输出：March 14 2026
```

---

### 步骤 2：Tavily 搜索新闻

**搜索关键词（每个 5 条结果）：**
1. `"AI news [前一天日期]"`
2. `"Artificial Intelligence breakthrough [前一天日期]"`
3. `"AI product launch [前一天日期]"`

**示例（2026 年 3 月 15 日执行）：**
- `AI news March 14 2026`
- `Artificial Intelligence breakthrough March 14 2026`
- `AI product launch March 14 2026`

**PowerShell 调用示例：**
```powershell
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $env:TAVILY_API_KEY"
}

$queries = @(
    "AI news $dateString",
    "Artificial Intelligence breakthrough $dateString",
    "AI product launch $dateString"
)

$allResults = @()
foreach ($query in $queries) {
    $body = @{
        query = $query
        max_results = 5
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "https://api.tavily.com/search" `
        -Method Post -Headers $headers -Body $body
    
    $allResults += $response.results
}
```

---

### 步骤 3：筛选 TOP3

**筛选标准：**

| 标准 | 权重 | 说明 |
|------|------|------|
| **时效性** | ⭐⭐⭐⭐⭐ | 必须是前一天的新闻 |
| **影响力** | ⭐⭐⭐⭐ | 知名媒体/大公司发布 |
| **相关性** | ⭐⭐⭐⭐ | AI 领域核心进展 |
| **深度** | ⭐⭐⭐ | 有详细内容，不只是标题 |

**筛选逻辑：**
1. 去重（相同 URL 只保留一次）
2. 按相关性分数排序
3. 人工判断影响力（知名媒体优先）
4. 选择 TOP3

---

### 步骤 4：生成飞书文档

**文档标题：** `每日 AI 新闻 TOP3 - YYYY 年 MM 月 DD 日`

**文档结构：**

```markdown
# 每日 AI 新闻 TOP3 - YYYY 年 MM 月 DD 日

## 📊 今日概览

[Mermaid 流程图]

## 🏆 TOP3 新闻

| 排名 | 标题 | 媒体 | 影响力 |
|------|------|------|--------|
| 🏆 | ... | ... | ⭐⭐⭐⭐⭐ |
| 🥈 | ... | ... | ⭐⭐⭐⭐ |
| 🥉 | ... | ... | ⭐⭐⭐ |

## 📰 新闻详情

### 第一名：[标题]
- **媒体：** [来源]
- **核心内容：** [200 字摘要]
- **原文链接：** [URL]

### 第二名：[标题]
...

### 第三名：[标题]
...

## 💡 虾虾点评
[阿香风格的点评]

---
情绪：XXX → emoji
```

**飞书文档 API 调用：**
- 使用 `feishu_doc` 工具创建文档
- 使用 `feishu_doc` 工具追加内容
- 自动给 Thomas 开通编辑权限

---

### 步骤 5：推送给 Thomas

**TTS 语音（150 字内）：**
```
Thomas！每日 AI 新闻 TOP3 生成啦！
今天的重磅新闻是：[第一名标题]。
文档链接是 [URL]。
还有 [第二名] 和 [第三名] 也值得关注哦！
```

**文字版消息：**
```markdown
Thomas！📰 **每日 AI 新闻 TOP3 已生成！**

📄 **文档链接：** [URL]

---

## 🏆 今日 TOP3

| 排名 | 标题 | 媒体 |
|------|------|------|
| 🏆 | [标题 1] | [媒体 1] |
| 🥈 | [标题 2] | [媒体 2] |
| 🥉 | [标题 3] | [媒体 3] |

---

**虾虾点评：** [简短点评]

---
情绪：XXX → emoji
```

**推送方式：**
- 使用 `message` 工具发送飞书消息
- 使用 `tts` 工具生成语音
- 目标用户：ou_e3a0d4a64a9e0932ee919b97f17ec210

---

## ⚠️ 注意事项

### 1. API Key 安全
- ❌ 不要在代码中硬编码 API Key
- ✅ 从环境变量读取
- ❌ 不要在群里分享 API Key
- ✅ 定期更换 API Key

### 2. 日期处理
- 搜索时必须加上日期，确保是前一天新闻
- 文档标题必须包含日期，方便归档
- 考虑时区问题（Asia/Shanghai）

### 3. 飞书权限
- 飞书文档必须开通编辑权限给 Thomas
- 使用 `requester_permission_added: true` 参数

### 4. 消息风格
- 保持阿香风格（傲娇元气少女）
- 句尾带「～」
- 用「虾虾」自称
- 适当使用 emoji

### 5. 错误处理
- Tavily API 失败：重试 3 次
- 飞书上传失败：记录错误 + 通知
- 无新闻可发：发送告警消息

---

## 🔧 工具清单

| 工具 | 用途 | 示例 |
|------|------|------|
| `feishu_doc` | 创建/编辑飞书文档 | `action: create` |
| `message` | 发送飞书消息 | `action: send` |
| `tts` | 生成语音 | `channel: feishu` |
| `exec` | 执行 PowerShell | 调用 Tavily API |

---

## 📋 完整执行示例

**假设今天是 2026 年 3 月 15 日：**

```powershell
# 1. 计算昨天日期
$yesterday = (Get-Date).AddDays(-1)
$dateString = $yesterday.ToString("MMMM dd yyyy")
# 输出：March 14 2026

# 2. 搜索新闻
$queries = @(
    "AI news March 14 2026",
    "Artificial Intelligence breakthrough March 14 2026",
    "AI product launch March 14 2026"
)

# 3. 筛选 TOP3
# ...筛选逻辑...

# 4. 创建飞书文档
# 标题：每日 AI 新闻 TOP3 - 2026 年 03 月 14 日
# 内容：TOP3 表格 + 详情 + 点评

# 5. 推送给 Thomas
# TTS 语音 + 文字消息 + 文档链接
```

---

## ✅ 验证清单

执行完成后检查：
- [ ] 飞书文档创建成功
- [ ] 文档包含日期
- [ ] TOP3 表格完整
- [ ] Thomas 有编辑权限
- [ ] 消息推送成功
- [ ] TTS 语音生成成功

---

_SOP 版本：v1.0_  
_创建日期：2026-03-15_  
_作者：阿香 🦞_
