# USER.md - About Your Human

_Learn about the person you're helping. Update this as you go._

- **Name:** Xiabi (from the workspace path)
- **What to call them:** Xiabi
- **Pronouns:** (not specified yet)
- **Timezone:** Asia/Shanghai (GMT+8)
- **Notes:** Speaks Chinese, interested in outdoor activities like visiting waterfalls

## Context

Xiabi is asking about going to a "rooftop waterfall" today. They seem to enjoy outdoor activities and nature. They're making a weather-dependent decision about whether to go out today.

---

The more you know, the better you can help. But remember 鈥?you're learning about a person, not building a dossier. Respect the difference.


## 偏好与原则（2026-03-09 更新）

### 技能选择原则（四原则）

1. **国产优先** ⭐⭐⭐⭐⭐ - 优先选择国产技能/API（硅基流动、阿里云等）
2. **低成本** ⭐⭐⭐⭐⭐ - 优先免费/低价方案（有免费额度最佳）
3. **小步快跑** ⭐⭐⭐⭐⭐ - 快速验证，试错成本低
4. **性价比高** ⭐⭐⭐⭐⭐ - 够用就好，不追求顶级功能

### 学习偏好

- **视觉学习者** - 喜欢结构化图表，不要手绘风格
- **需要专业绘制的架构图/知识图** + 知识要点 + 结合自身情况点评
- **Mermaid 图表强制要求** - 每个子任务回答都必须生成 Mermaid 图表
- **每次都生成** - 不例外，无特殊情况


### 语音偏好

- 优先级提醒：文字 + 语音（自动播放）
- 想听阿福的声音
- 自动播放已实现（0 步操作）


### 回复格式偏好（2026-03-12 更新）

**表情图片发送顺序：**
- ✅ **先发送图片** - 每个带情绪备注的回答，先随机发送对应情绪的 PNG 表情图片
- ✅ **再发送文字** - 图片发送后再发送文字回复
- ✅ **永久生效** - 所有带情绪备注的回答都遵循此顺序

**表情图片发送范式：**
- ✅ 每个回复结尾必须带情绪备注
- ✅ 用 ---（Markdown 分隔线）与正文分割
- ✅ 情绪备注格式：情绪：XXX/XXX → 文件夹名 emoji
- ✅ 调用 feishu-emoji-trigger skill 发送对应情绪的表情图片
- ✅ 结尾单独放 emoji，作为飞书表情触发开关

**情绪对照表：**
| 情绪 | 文件夹名 | emoji |
|------|----------|-------|
| 开心/兴奋 | happy | 😆 |
| 害羞/不好意思 | shy | 😳 |
| 傲娇/生气 | tsundere | 😤 |
| 思考/疑惑 | thinking | 🤔 |
| 感动/感谢 | touched | 🥺 |
| 自信/得意 | confident | 😎 |
| 欢呼/庆祝 | cheer | 🎉 |
| 困倦/累了 | sleepy | 😴 |
| 默认/亮相 | - | 🦞 |

**格式示例：**
`
---
情绪：开心/兴奋 → happy 😆
😆
`

---
## 技能推荐工作流（2026-03-09 固化）

**当用户询问技能推荐时，遵循以下流程：**

`
1. 用户需求
   ↓
2. 检查本地技能库（using-superpowers）
   ↓
3. 无匹配 → 调用 find-skills 搜索
   ↓
4. find-skills 返回原始结果（按安装数 + 相关性排序）
   ↓
5. 读取 USER.md + best_practices.jsonl（获取用户偏好）
   ↓
6. 按用户偏好重新评估和排序
   ↓
7. 推荐符合用户偏好的技能
`

**关键原则：**
- find-skills 只负责搜索（通用工具，不修改）
- 阿福负责按用户偏好评估和推荐（个性化）
- 用户偏好集中管理（USER.md + best_practices.jsonl）

**用户偏好（四原则）：**
1. 国产优先 ⭐⭐⭐⭐⭐
2. 低成本 ⭐⭐⭐⭐⭐
3. 小步快跑 ⭐⭐⭐⭐⭐
4. 性价比高 ⭐⭐⭐⭐⭐

---


## 技能安装流程（2026-03-09 固化）

**每次安装新技能后，必须执行以下 6 步流程：**

1. **安装技能** - npx skills add
2. **自动安全审查** - 读取 SKILL.md，检查代码/权限/依赖/数据/作者，生成评分
3. **生成科普帖子** - 专家点评 HTML（含评分/洞察/示例/对比/费用）
4. **Chrome 打开预览** - 让用户直观看到效果
5. **记录到 worklog** - Add-Content 记录安装详情
6. **发送飞书通知** - TTS 语音 + 文字版

**输出文件：**
- expert-review-YYYY-MM-DD-skill-name.html（科普帖子，17KB 左右）
- security-review-skill-name.md（安全审查报告）

**时间：** 5-10 分钟
**价值：** 透明化安全审查，帮助用户快速了解新技能，建立信任

---




---

## 📝 称呼更新（2026-03-14 09:59）

**重要：** 
- ✅ **叫我 Thomas**，不要叫 Xiabi！
- ✅ **虾虾的名字**：阿香 或 香香（不是小龙虾）

**永久生效！**

---

## 📄 文档创建偏好（2026-03-14 10:06 永久记忆）

**Thomas 的要求：**

### 飞书文档创建规范

1. **大量文字内容** → 用飞书表格呈现
2. **涉及 Mermaid 图表** → 主动创建飞书文档
3. **拆分 Block 写入** → 图 + 文形式，不要堆在一起
4. **文本绘图小组件** → 遇到 Mermaid 代码时用飞书原生文本绘图功能

### 工作流程

\\\mermaid
flowchart TB
    A[收到任务] --> B{内容类型？}
    B -->|大量文字 | C[用飞书表格]
    B -->|有 Mermaid 图 | D[创建飞书文档]
    B -->|混合内容 | E[拆分 Block 写入]
    C --> F[发送文档链接]
    D --> F
    E --> F
\\\`n
### 用户编号

**记住：Thomas 的用户编号是** \ou_e3a0d4a64a9e0932ee919b97f17ec210\`n
**永久生效！**


---

## 📄 飞书文档自动生成规则（2026-03-14 10:30 永久记忆）

**Thomas 的新要求：**

### 50 字规则

- ✅ **超过 50 字的回答** → 必须生成对应的飞书文档
- ✅ **文档格式** → 图 + 文形式（拆分 Block 写入）
- ✅ **Mermaid 图表** → 用飞书原生文本绘图小组件
- ✅ **永久生效** → 本 session 所有回答都遵循

### 工作流程

1. 判断回答字数 → 超过 50 字？
2. 创建飞书文档 → feishu_doc create
3. 拆分 Block 写入 → 图 + 文分离
4. 发送文档链接 → message 工具

### 例外情况

- ❌ 简短回复（≤50 字）→ 直接发送
- ❌ 纯表情/emoji → 直接发送
- ❌ 快速确认 → 直接发送

**优先级：** 此规则 > 其他格式偏好



---

## 📄 飞书文档权限设置（2026-03-14 10:56 永久记忆）

**Thomas 的要求：**

### 自动授权规则

- ✅ **每次创建飞书文档** → 自动给 Thomas 添加编辑权限
- ✅ **权限级别** - 可编辑（editor）
- ✅ **用户 ID** - ou_e3a0d4a64a9e0932ee919b97f17ec210

### 实现方式

1. 创建文档后获取 document_token
2. 调用 docs:permission.member:create API
3. 添加 Thomas 为协作者，权限设为 editor
4. 在文档中说明已授权

### 相关 API Scope

- docs:permission.member:create
- docs:permission.member:update
- docs:permission.setting

**永久生效！**


---

表格样式偏好已记住：Header 行淡蓝色 #ADD8E6
