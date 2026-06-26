# HTML 专家点评用户偏好固化记录

**固化时间：** 2026-03-10 11:00  
**固化位置：** `skills/html-expert-review/SKILL.md`（末尾新增章节）  
**参考文件：** `expert-review-2026-03-08-knowledge-architecture.html`

---

## 🎨 6 大核心风格

### 1️⃣ 渐变背景

- **整体背景：** `#f5f7fa → #c3cfe2`（浅灰蓝渐变）
- **Header：** `#667eea → #764ba2`（紫色渐变）

### 2️⃣ 大圆角设计

- **container：** `border-radius: 20px`
- **卡片/图表：** `border-radius: 15px`
- **表格：** `border-radius: 10px`

### 3️⃣ 阴影效果

- **container：** `box-shadow: 0 20px 60px rgba(0,0,0,0.1)`
- **专家卡片：** `box-shadow: 0 10px 30px rgba(0,0,0,0.1)`

### 4️⃣ 配色方案

| 元素 | 渐变颜色 | 用途 |
|------|---------|------|
| **主色** | `#667eea → #764ba2` | Header、章节标题、评分数字 |
| **专家卡片** | `#ffecd2 → #fcb69f` | 专家评分卡片背景 |
| **存储格** | `#a8edea → #fed6e3` | 七仓存储系统卡片 |
| **高亮** | `#ffeaa7 → #fdcb6e` | 重点文字背景 |

### 5️⃣ 装饰元素

- **Header：** 📚🏗️（大 emoji，opacity: 0.3）
- **章节标题：** 🔹（before 伪元素）
- **专家卡片：** ⭐（右上角，opacity: 0.5）
- **数字编号：** 渐变圆形背景（30px×30px）

### 6️⃣ Mermaid 样式

- ✅ **带 emoji** - 节点名称前加 emoji（📑📁📚💬📊）
- ✅ **自定义颜色** - 紫色系（#667eea, #764ba2, #f093fb）
- ✅ **字体** - Microsoft YaHei
- ✅ **主题** - default

---

## 📋 生成前检查清单（10 项）

- [ ] 背景渐变 - body 使用 `#f5f7fa → #c3cfe2`
- [ ] Header 渐变 - 使用 `#667eea → #764ba2`（紫色）
- [ ] 圆角尺寸 - container 20px、卡片 15px、表格 10px
- [ ] 阴影效果 - container 大阴影（0 20px 60px）
- [ ] 专家卡片 - 橙色渐变背景（`#ffecd2 → #fcb69f`）
- [ ] 存储格 - 青粉渐变背景（`#a8edea → #fed6e3`）
- [ ] 装饰 emoji - Header 有📚🏗️、章节有🔹、卡片有⭐
- [ ] Mermaid emoji - 节点名称前带 emoji
- [ ] Mermaid 颜色 - 紫色系（#667eea, #764ba2, #f093fb）
- [ ] 字体 - Microsoft YaHei（微软雅黑）

---

## ⚠️ 禁止事项（7 项）

- ❌ 不要使用白色背景
- ❌ 不要使用小圆角
- ❌ 不要省略阴影
- ❌ 不要使用单色
- ❌ 不要省略 emoji 装饰
- ❌ Mermaid 不要不带 emoji
- ❌ Mermaid 不要用默认颜色

---

## 🎯 成功案例

**参考文件：**
- `expert-review-2026-03-08-knowledge-architecture.html`（标准模板）
- `expert-review-2026-03-10-openclaw-knowledge-architecture.html`（最新复刻）

**视觉特点：**
- ✅ 渐变背景（浅灰蓝→紫色）
- ✅ 大圆角（20px/15px/10px）
- ✅ 阴影效果（层次感）
- ✅ 多彩渐变（紫色/橙色/青粉色）
- ✅ emoji 装饰（📚🏗️🔹⭐）
- ✅ Mermaid 带 emoji + 自定义颜色

---

## 🔄 三线同步执行

### 1️⃣ MD 文件线
- ✅ `skills/html-expert-review/SKILL.md` - 新增"用户偏好"章节
- ✅ `worklog.txt` - 记录固化操作

### 2️⃣ TXT 记录线
- ✅ `memory/2026-03-10-html-style-preference.md` - 本文件

### 3️⃣ 飞书通知线
- ✅ 发送飞书消息（含本记录摘要）

---

_记录人：阿福 🦞_  
_固化原因：避免再次丢失 2026-03-08 版本的用户偏好_
