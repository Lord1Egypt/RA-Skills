---
name: video-collector
description: 抖音/B站视频收藏入库——接收视频链接，自动抓取信息、生成总结、分类、入库飞书多维表格。触发词：视频入库 / 收藏视频 / 帮我整理这个视频。
argument-hint: <视频链接>
allowed-tools: Bash(curl *), Bash(node *), Bash(date *), Bash(mkdir *), Bash(rm *), WebFetch, Skill
---

# 视频收藏入库

接收抖音/B站视频链接 → 自动抓取信息 → 生成总结+分类 → 写入飞书多维表格。

---

## 配置说明

使用前需要在 skill 文件顶部填写你的飞书多维表格配置：

```
Base Token:  你的Base Token（格式：app_xxxxxxxxxxxx）
Table ID:    你的Table ID（格式：tblxxxxxxxxxxxx）
Base URL:    https://my.feishu.cn/base/你的BaseToken
```

> 如何获取：在飞书多维表格页面 URL 中提取，例如 `https://my.feishu.cn/base/U7DRbtjO6aMlJcsYBGUcvah2nsf`，则 Base Token 为 `U7DRbtjO6aMlJcsYBGUcvah2nsf`。

---

## 字段映射（飞书多维表格）

建议按以下结构创建多维表格字段：

| 字段名     | 类型         | 说明                     |
|-----------|-------------|------------------------|
| 标题       | 文本         | 视频标题（主字段）         |
| 平台       | 单选         | 抖音 / B站               |
| 链接       | 文本         | 原始视频链接              |
| UP主/博主  | 文本         | UP主/博主名称            |
| 时长       | 文本         | 如 "12:34"              |
| 类型       | 单选         | 知识/娱乐/资讯/教程/其他   |
| 主题       | 多选         | AI/产品/编程/设计/投资/生活/职场/其他 |
| 内容总结   | 文本         | 2-4句内容概括            |
| 添加日期   | 日期         | 格式 yyyy/MM/dd          |
| 标签       | 多选         | 已看/想看/反复看/待整理    |

---

## 流程

### 1. 判断平台

- 抖音：`douyin.com` / `v.douyin.com`
- B站：`bilibili.com` / `b23.tv`

### 2. 抓取视频信息

**统一方案：dokobot（支持抖音、B站及所有 JS 渲染页面）**

```bash
# 用 dokobot 读取页面，自动 JS 渲染，所有平台统一处理
dokobot read "<url>" --local --timeout 5000
```

从返回内容中提取：
- **标题**：取第一行标题（去除链接和噪音）
- **UP主/博主**：找 "UP主名" 或 "作者" 相关行
- **时长**：找 "mm:ss" 或 "时长" 相关行
- **描述/简介**：找正文描述段落
- **发布时间**：找 "发布于" 或日期格式内容
- **点赞/播放**：找数字+单位（万/千）

**抖音短链补全**：如果是 `v.douyin.com/xxx` 短链，先用 curl 获取完整 URL：

```bash
# 抖音短链 → 完整 URL
FULL_URL=$(curl -sL "https://v.douyin.com/xxx" -w "%{url_effective}" -o /dev/null)
# 然后送入 dokobot
dokobot read "$FULL_URL" --local --timeout 5000
```

### 3. 生成字段

**类型判断**（根据内容推断）：
- 教程/操作演示 → "教程"
- 知识科普/深度解读 → "知识"
- 资讯/热点/新闻 → "资讯"
- 搞笑/娱乐/休闲 → "娱乐"
- 无法判断 → "其他"

**主题判断**（多选，最多选3个）：
- 涉及 AI/大模型/ChatGPT/编程/模型训练 → ["AI", "编程"]
- 涉及 产品经理/需求/Aha Moment/用户增长 → ["产品"]
- 涉及 UI/UX/设计/视觉/交互 → ["设计"]
- 涉及 投资/理财/股票/黄金/赚钱 → ["投资"]
- 涉及 职场/求职/面试/职场人际 → ["职场"]
- 涉及 生活日常/美食/情感/家居 → ["生活"]
- 无法判断 → ["其他"]

**标签**：默认填 "想看"，如果用户说"已看完"或类似表述则填 "已看"

**内容总结**：根据视频标题+描述，用 2-4 句话概括核心内容。

### 4. 入库

```bash
# 添加日期用当天，格式 "YYYY-MM-DD HH:mm:ss"
ADD_DATE=$(date +"%Y-%m-%d %H:%M:%S")

# 写入飞书（替换 <YOUR_BASE_TOKEN> 和 <YOUR_TABLE_ID> 为实际值）
lark-cli base +record-upsert \
  --base-token <YOUR_BASE_TOKEN> \
  --table-id <YOUR_TABLE_ID> \
  --json @./_record.json
```

其中 `_record.json` 内容格式：

```json
{
  "标题": "视频标题",
  "平台": "抖音",
  "链接": "https://...",
  "UP主/博主": "UP主名",
  "时长": "5:31",
  "类型": "教程",
  "主题": ["AI", "设计"],
  "内容总结": "内容概括...",
  "添加日期": "2026-05-04 10:30:00",
  "标签": ["想看"]
}
```

### 5. 输出确认

```
✅ 已入库视频收藏库
🔗 https://my.feishu.cn/base/<YOUR_BASE_TOKEN>

📋 {标题}
🎯 {平台} · {类型} · {主题}
💬 {内容总结}
```

---

## 错误处理

- 抓取失败 → 检查 URL 是否有效，确认 dokobot 浏览器扩展已连接
- 入库失败 → 检查 Base Token 和 Table ID 是否正确配置
- 字段类型不匹配 → 确认 JSON 中字段值类型与飞书字段类型一致
