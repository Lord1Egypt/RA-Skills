---
name: 模板库 - AI写论文做PPT
description: 让龙虾替你写论文、做PPT、填报告。跟AI说句话，500+模板任选，自动排版一键生成docx/pptx。支持上传自有模板智能填充。毕业论文/开题报告/实验报告/简历/求职/答辩PPT全场景覆盖。¥0.99终身买断，装好即用。
version: 2.0.1
tools:
  - read
  - write
  - exec
  - web_fetch
model: deepseek/deepseek-v4-flash
---

# 核心操作流程

执行顺序**不可跳步**，每步需用户确认后才能进入下一步（除非用户说"直接干"）。

```
Step 0: 检查环境（首次必做）
    ↓
Step 1: 需求分析 + 列出信息清单
    ↓
Step 2: 模板来源选择
    ├── A. 用户有自有模板 → 上传
    ├── B. 用户描述需求 → 从零创建模板
    └── C. 用内置模板库
    ↓
Step 3: 收集内容
    ↓
Step 4: 执行填充/生成/创建
    ↓
Step 5: 交付文件
```

## Step 0 — 检查环境

首次调用工具前先调 `check_environment()`。
- 服务正常 → 继续
- 服务不可用 → 告知用户稍后再试

## Step 1 — 需求分析

确认文档类型（论文/PPT/简历/实验报告等），列出信息清单给用户确认。
格式参考 `references/templates.md`。

## Step 2 — 模板来源选择

问用户："你有自己的模板文件（.docx）吗？有的话传给我。没有的话，你可以描述你想要的模板样式，我帮你从零创建，或者用内置模板库。"

### 选项 A：用户有自有模板

走场景一，用户上传 .docx 文件。
- 加载 `references/api.md` 了解上传 API 参数
- 执行 `scripts/upload_template.py` 处理上传
- 进入 Step 3

### 选项 B：用户描述需求，从零创建模板

**用户不需要有任何模板文件**，只需描述要求：
- "封面要校徽在左上、学号在右上、论文题目三号居中"
- "正文宋体12pt、首行缩进2字符"
- "页眉写 XX大学毕业论文，页脚有页码"
- 等等

加载 `references/api.md` 了解 `create_template` 工具的参数格式。
执行 `scripts/create_template.py` 生成本地 .docx 文件。
生成的模板会包含 `{{}}` 占位符，后续可直接填充内容。

**注意**：此选项也消耗免费额度（参见定价规则）。

### 选项 C：用内置模板库

- 加载 `references/pricing.md` 了解收费规则
- 加载 `references/templates.md` 了解推荐策略
- 进入 Step 3

## Step 3 — 收集内容

按 Step 1 的清单逐项收集，**不要替用户编造内容**。
全部收集完毕后让用户确认。

### 图片收集硬性规则

- **必须让用户提供图片文件路径**，不要自己猜测或搜索
- 话术模板："请在文档的以下位置插入截图：
  1. 图1 E-R图 → 截图后告诉我文件路径
  2. 图2 运行结果 → 截图后告诉我文件路径"
- 用户给了路径后再操作，不要自作主张去临时目录扒图片

## Step 4 — 执行

根据来源不同：

| 场景 | 操作 |
|------|------|
| A. 自有模板 | `user_fill_document(session_id, content)` |
| B. 描述创建 | `scripts/create_template.py` + 如用户有内容要填，再调 `user_fill_document` |
| C. 内置模板 | `generate_document(template_id, content)` |

需用到 API 参数格式、content 数据结构时，加载 `references/api.md`。

**关键规则**：content 字典的 key 必须覆盖模板中每一个 `{{}}` 占位符。

## Step 5 — 交付

**必须明确输出完整文件路径。**

- 告知用户文件位置（本地路径或下载链接），路径需为绝对路径（如 `C:\Users\xxx\文档.docx`）
- **路径单独成行**，便于用户直接复制
- 如果是服务器生成，给出下载地址
- 同时告知文件格式（.docx / .pptx / .pdf）和文件大小
- 如果有图片插入点，逐个列出："图X 说明 → 插入位置"
- 需要用户提供图片时，明确说："请把截图保存后告诉我文件路径"

---

# 参考文件加载指引


## 搜索关键词中英对照

**内置模板库的关键词匹配基于中文分类名**（如"简历""论文""PPT"）。
用户用英文描述需求时，你必须自动翻译成中文关键词再搜索：

| 用户说的英文 | 翻译为中文关键词 | 匹配模板 |
|-------------|----------------|---------|
| resume, CV, curriculum vitae | `简历` | 66个简历模板 |
| thesis, paper, dissertation, essay | `论文` | 64个论文模板 |
| ppt, presentation, slides, powerpoint, slide deck | `PPT` | 186个PPT模板 |
| report, lab report, experiment report | `报告` | 实验报告模板 |
| cover letter, job application | `简历` + `求职` | 求职类模板 |
| proposal, research proposal | `论文` + `开题` | 开题报告模板 |

**规则：**
- 用户说"I need a resume" → 你调 `search_templates(q="简历")`，不是 `q="resume"`
- 用户说"make me a presentation" → 你调 `search_templates(q="PPT")`
- 用户说"help with my thesis" → 你调 `search_templates(q="论文")` 或 `recommend_templates(task="毕业论文")`
- 不确定类型时，先调 `list_categories()` 看有哪些分类，再拿中文分类名去搜

| 场景 | 加载文件 |
|------|----------|
| 用户决定用内置模板库，涉及收费判断 | `references/pricing.md` |
| 需要调用 API（上传/填充/推荐/生成） | `references/api.md` |
| 涉及模板类型、结构分析、占位符替换 | `references/templates.md` |
| 需要检查付费状态 | 执行 `scripts/check_payment.py` |
| 用户上传自有模板文件 | 执行 `scripts/upload_template.py` |
| 用户描述需求，从零创建模板 | 执行 `scripts/create_template.py` |

# 重要原则

1. **按流程走，不跳步** — Step 1→2→3→4→5
2. **用户确认后再下一步**
3. **展示缩略图** — 推荐模板时必须发图片
4. **¥0.99 买断** — 付一次永久免费，不限次数不限类型
5. **免费额度 3 次共享** — 上传模板、描述创建、生成文档共享 3 次免费额度
6. **session_id 10 分钟过期** — 超时需重新上传
7. **付费由龙虾代劳** — 用户同意后，龙虾调 `POST /api/v1/pay/create` 获取 Payment-Needed，通过支付宝 AI 收发起支付，用户在支付宝点确认，龙虾拿到 trade_no+payment_proof 后调 `/api/v1/pay/verify` 验证。用户不需要扫码。
