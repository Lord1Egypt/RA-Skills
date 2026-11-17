---
name: workopilot-service-builder
description: 帮助开发者创建和集成喔壳(WorkoPilot)AI 能力到业务系统。涵盖创建 AI 服务、配置数字员工、注册 iframe 技能卡片、生成接入代码、提供集成方案、排查对接问题等完整流程。当用户提到 WorkoPilot 对接、喔壳集成、AI 服务创建、数字员工配置、iframe 嵌入、附件分类、文档处理、API 调用示例、鉴权配置、接口测试、集成故障排查,或需要自动化脚本来创建配置时,都应使用此技能。即使用户只是说"对接喔壳"、"创建 AI 服务"、"嵌入聊天窗口"、"测试接口"这样的简短表述,也要触发此技能提供端到端的指导。
compatibility:
  required_tools:
    - Python 3.7+
    - requests library
  optional_tools:
    - curl (for API testing)
---

# 喔壳服务创建与集成助手

## 什么是喔壳(WorkoPilot)

喔壳是一个企业级 AI 应用平台,提供两种使用模式:

### 模式 1: 作为独立的 AI 应用入口

用户通过喔壳 App 或 Web 端直接使用数字员工。

**数字员工 = Agent 聊天智能体 + 业务菜单**

- **Agent 聊天智能体**支持:
  - MCP (Model Context Protocol) - 数据操作能力
  - 系统提示词配置 - 定制对话行为
  - 技能卡片(Iframe) - UI 交互扩展
  - 知识库 - 领域知识注入

- **业务菜单**提供:
  - 业务历史记录(如报价单历史)
  - 业务功能入口
  - 可配置为应用菜单 iframe 页面

**示例 - 报价助理数字员工:**
```
┌─────────────────────────────────────┐
│  对话区: 协助用户生成报价单         │
│  "帮我做一份设备采购的报价单"       │
│  → 通过对话收集信息                 │
│  → 调用 MCP 生成报价                │
│  → 在技能卡片中展示报价单预览       │
├─────────────────────────────────────┤
│  业务菜单: [报价单历史] [客户管理]  │
│  → 点击后加载应用菜单 Iframe 页面   │
└─────────────────────────────────────┘
```

**开发者如何定制数字员工:**
- **UI 层**: 开发 Iframe 技能卡片(对话中触发)或应用菜单 iframe(固定业务菜单)
- **数据层**: 开发 MCP - 连接 ERP 系统、生成报价、保存记录
- **结合**: Iframe(UI) + MCP(数据) = 个性化业务数字员工

### 模式 2: 作为 AI 能力提供平台

第三方系统通过集成喔壳能力,快速实现 AI 化。

**提供两类能力:**

1. **AI 服务** - 通过 API 接口调用
   - 封装可复用的 AI 能力(文本提取、内容生成、智能分析等)
   - 类似函数调用: `POST /api/aiagent/run`
   - 适合后端系统集成

2. **数字员工** - 通过 Iframe 嵌入
   - 将完整的数字员工界面嵌入第三方系统
   - 用户在第三方系统内直接使用喔壳数字员工
   - 适合快速为现有系统增加 AI 对话能力

**典型场景:**
- **改造传统系统**: 在 CRM/ERP 系统中嵌入数字员工,增加智能助手
- **新开发 AI 应用**: 直接调用喔壳 AI 服务,无需自建 AI 基础设施
- **文档智能化**: 调用附件提取服务,自动从合同/发票/简历等文件中提取结构化数据
- **混合模式**: 后端调用 AI 服务处理数据,前端嵌入数字员工提供交互

## 本技能提供什么

本技能帮助开发者使用喔壳的开放 API 和集成能力:

**配置自动化:**
- Python 脚本快速创建 AI 服务、数字员工、技能卡片、附件分类
- 自动化配置,避免手动操作

**代码生成:**
- 生成完整可运行的接入代码
- API 调用示例、Iframe 嵌入代码、MCP 集成模板、附件提取调用示例

**集成指导:**
- 端到端的对接方案和最佳实践
- 区分不同使用模式的实施路径
- 附件分类和提取场景的完整流程

**问题诊断:**
- 排查鉴权、网络、配置等常见问题
- 提供调试方法和解决方案



## 核心能力详解



### 1. AI 服务 - 可复用的 AI 能力封装

**定位:** 类似"AI 函数",封装提示词和输入参数

**典型场景:**
- 文本分析(合同审查、简历筛选、舆情分析)
- 内容生成(报告生成、文案创作、邮件起草)
- 数据转换(非结构化文本 → 结构化 JSON)

**创建流程:** `scripts/create_ai_service.py`

### 2. 数字员工 - Agent 智能体 + 业务菜单

**定位:** 完整的对话式 AI 应用

**扩展能力:**
- MCP: 数据操作(连接 ERP/CRM/数据库)
- 技能卡片: UI 交互(Iframe 嵌入复杂界面)
- 知识库: 领域知识(RAG 检索增强)
- 系统提示词: 行为定制

**创建流程:** `scripts/create_digital_employee.py`
**更新流程:** `scripts/update_digital_employee.py`

### 3. 附件分类与提取 - 文档智能化核心能力 ⭐⭐⭐

**定位:** 从文件中自动提取结构化数据，消除手工录入

**核心价值:**
- **使用频率极高** - 90% 的场景使用"直接提取"模式
- **节省人力** - 合同/发票/简历等文件自动提取，不用人工抄写
- **提升准确率** - 避免人工录入的错误和遗漏
- **秒级响应** - 上传即提取，实时填充表单

**两种使用模式:**

**模式 A: 分类 + 提取** (文件来源复杂，使用较少)
```
上传杂乱文件 → 系统识别类型 → 提取数据
```

**模式 B: 直接提取** (已知类型，高频使用 ⭐⭐⭐)
```
上传合同 → 指定"采购合同"编码 → 提取结构化数据 → 填充表单
```

**快速示例:**
```javascript
// 合同管理系统 - 用户上传合同后自动填充表单
const result = await fetch(`${BASE_URL}/api/attachment/extract`, {
  method: 'POST',
  headers: { 'API-KEY': apiKey },
  body: JSON.stringify({
    fileUrl: uploadedFileUrl,
    categoryCode: 'contract-purchase'  // 指定采购合同分类
  })
});

// 返回结构化数据
// { partyA: "北京公司", partyB: "上海公司", amount: 500000, ... }

// 自动填充表单
fillForm(result.data);
```

**两种提取技术:**
- **OCR + LLM** - 扫描件、纯文本(先识别文字再理解)
- **Vision-Language** - 复杂排版、包含表格图表(直接理解)

系统自动选择最优技术，也可手动指定。

**开发流程:**
1. 检查系统是否有目标分类(如"采购合同")
2. 不存在则创建分类并定义 `ExtractRules`(提取规则)
3. 在业务系统中调用提取接口
4. 获取结构化数据并处理

**关键概念:**
- **AttachmentGroup** - 分组(如"合同"、"财务"、"人力")
- **AttachmentClassification** - 分类(如"采购合同"、"增值税发票")
- **ExtractRules** - 提取规则(定义要提取哪些字段，字段的 description 决定准确率)

**常见分类:**
- 合同类: 采购合同、销售合同、租赁合同
- 财务类: 增值税发票、收据、银行流水
- 人力类: 简历、身份证、学历证书
- 业务类: 订单、报价单、验收单

**创建脚本:** `scripts/create_attachment_classification.py`

**详细文档:** 
- 完整开发流程、提取规则设计技巧、代码示例、故障排查
- 👉 请阅读 `references/attachment-classification.md`

### 4. Iframe 技能卡片 - UI 扩展

**定位:** 在对话中嵌入自定义 UI。数字员工旁边的固定业务菜单属于“应用菜单 iframe”，不要和对话中 `showCard` 触发的 Iframe 技能卡片混淆。

**使用场景:**
- 在对话中展示复杂界面(报价单预览、表单填写)
- AI 先生成或检索结果，再通过 `showCard` 打开可交互卡片

**注册流程:** `scripts/register_iframe_card.py`

### 5. 文档服务 - 文件处理

**定位:** 文档格式转换和处理

**能力:**
- Markdown/HTML 转 PDF
- OCR 识别
- Excel 读写

### 6. 计费模块 - 额度管理 ⚠️

**定位:** 数字员工使用额度消耗和校验

**核心概念:**
- **扣费时机由开发者决定** - 例如创建订单、生成报告、完成审核时
- **扣费额度由平台售价决定** - 平台管理员配置每次消耗的单位数
- **支持 API-KEY 鉴权** - 服务端集成使用 API-KEY（虽然文档写的是 Bearer Token）

**典型场景:**
- 销售助理：生成销售订单时扣费
- 合同审核：生成审核报告时扣费
- HR 助理：生成面试评估报告时扣费

**集成方式:** 在 MCP 工具、iframe 技能卡片或后端 API 中集成

**详细文档:** `references/billing.md`

**⚠️ 重要提醒:**
如果你的数字员工提供以下高价值服务，**强烈建议集成计费**：
- 生成文档、报告、合同等文件
- 创建订单、工单、任务等业务记录
- 数据导出（PDF、Excel、Word）
- 复杂计算或分析
- 批量处理操作
- 调用外部付费 API

**未集成计费的风险:** 用户可以无限制使用高价值服务，导致成本失控。

## 能力层次

```
┌──────────────────────────────────────────────┐
│  应用层                                      │
│  ├─ 模式1: 喔壳 App/Web - 直接使用          │
│  └─ 模式2: 第三方系统 - Iframe嵌入/API调用  │
├──────────────────────────────────────────────┤
│  集成层                                      │
│  ├─ Iframe 嵌入 - 界面集成                  │
│  └─ 开放 API - 程序调用                     │
├──────────────────────────────────────────────┤
│  能力层                                      │
│  ├─ 数字员工 - Agent智能体+业务菜单         │
│  ├─ AI 服务 - 可复用的AI能力封装            │
│  ├─ 基础服务 - 附件分类、文档处理           │
│  └─ 计费模块 - 额度消耗和校验 ⚠️           │
├──────────────────────────────────────────────┤
│  扩展层                                      │
│  ├─ MCP - 数据操作能力                      │
│  ├─ 技能卡片 - UI交互扩展                   │
│  └─ 知识库 - 领域知识                       │
└──────────────────────────────────────────────┘
```

## 快速开始

### 典型场景识别

根据用户需求判断场景类型,选择相应的处理方式:

**场景 1: 需要创建配置资源**

当用户说"创建 AI 服务"、"配置数字员工"、"注册技能卡片"、"创建附件分类"时,使用对应的 Python 脚本:

- 创建 AI 服务 → `scripts/create_ai_service.py`
- 创建数字员工 → `scripts/create_digital_employee.py`  
- 更新数字员工 → `scripts/update_digital_employee.py`
- 配置数字员工应用菜单 → `scripts/configure_app_menu.py`
- 注册 iframe 卡片 → `scripts/register_iframe_card.py`
- 创建附件分类 → `scripts/create_attachment_classification.py` ⭐

这些场景的关键是理解用户的业务需求,设计合理的配置参数。

应用菜单配置是**配置阶段动作**：当用户要给数字员工旁边增加“报价单历史”“客户资料”等固定业务菜单时，由 Agent 调用 `configure_app_menu.py` 新增或更新菜单。开发者运行时只需要实现菜单 `iframeUrl` 对应页面，并按 `references/app-menu-iframe.md` 处理 `runtimeToken` 单点登录。

**特别注意 - 附件分类创建:**

附件分类是**文档智能化的基础**,创建时要重点设计 `extractRules`:
- 明确需要提取哪些字段(name、label、type)
- 字段描述要详细(帮助 AI 准确定位)
- 考虑字段的格式要求(日期格式、数字精度等)

典型附件类型:
- **合同类**: 采购合同、销售合同、租赁合同、劳动合同
- **财务类**: 增值税发票、收据、银行流水、报销单
- **人力类**: 简历、身份证、学历证书、劳动合同
- **业务类**: 订单、报价单、出库单、验收单

**场景 2: 需要调用已有服务**

当用户说"如何提取合同数据"、"调用 AI 服务"、"使用附件识别"时,提供调用示例:

- AI 服务调用 → 生成完整的 API 调用代码
- 附件提取调用 → 生成文件上传 + 提取的完整流程 ⭐
- 数字员工聊天 → 生成会话创建和消息发送示例

**重点: 附件提取高频场景**

附件提取是最常用的功能之一。用户通常的需求:

```
"我有一个合同管理系统,用户上传合同后,
需要自动提取甲方、乙方、金额等信息填充到表单"
```

**标准流程:**
1. **检查**: 查询系统是否已有"采购合同"分类
2. **创建**(如果不存在): 创建分类并定义提取规则
3. **调用**: 在业务系统中调用提取接口
4. **填充**: 将提取的结构化数据填充到表单

**场景 3: 需要集成代码或方案**

当用户说"如何嵌入"、"怎么调用接口"、"对接流程"时,提供方案和代码:

- iframe 嵌入对接 → 阅读 `references/iframe-embed.md`,输出嵌入代码
- API 调用示例 → 阅读对应接口文档,生成 curl/代码示例
- 鉴权配置问题 → 阅读 `references/auth-and-config.md`

这些场景的关键是提供完整可运行的代码,包含错误处理和参数说明。

**场景 4: 需要故障排查**

当用户报告"接口报错"、"鉴权失败"、"数据不对"、"提取结果不准确"时,系统性诊断:

1. 检查鉴权配置(API-KEY 格式、请求头设置)
2. 验证接口路径和参数格式
3. 确认必需资源是否已创建(serviceCode、robotId、分类编码等)
4. 对于附件提取问题,检查:
   - 文件格式是否支持
   - 提取规则 description 是否清晰
   - 文件内容是否包含目标字段
5. 提供调试命令或测试脚本

### 文档按需加载原则

不要一次性加载所有 reference 文档。根据任务类型,按这个优先级读取:

**第一步:总是先读鉴权配置**
- `references/auth-and-config.md` - 所有任务都需要了解鉴权和配置机制

**第二步:根据任务读取对应文档**

| 用户任务 | 需要读取的文档 |
|---------|--------------|
| 创建/调用 AI 服务 | `references/ai-service.md` |
| 创建/使用数字员工 | `references/digital-employee.md` |
| 附件分类场景 | `references/attachment-classification.md` |
| iframe 将数字员工嵌入到当前系统对接 | `references/iframe-embed.md` |
| iframe 技能卡片注册 | `references/iframe-skill-card.md` |
| 数字员工旁边的业务菜单 iframe、菜单 SSO、菜单 runtimeToken 解析 | `references/app-menu-iframe.md` |
| 文档服务对接 | `references/document-service.md` |
| 数字员工计费集成 | `references/billing.md` |

这种按需加载方式避免上下文浪费,让每个任务都能获得最相关的信息。

## 创建配置资源的标准流程

当用户需要创建 AI 服务、数字员工等配置资源时,遵循这个流程:

### 1. 理解业务需求

通过对话明确:
- 这个服务/员工/附件分类要解决什么问题?
- 输入是什么?(用户会提供哪些信息)
- 输出期望是什么?(返回什么格式的结果)
- 有没有特殊的业务规则或限制?

### 2. 设计配置参数

**对于 AI 服务,特别重要:**

设计有意义的 `inputs` 字段。不要只用通用的 `user_message`,而要根据业务场景设计具体的输入字段。

**示例 - 合同审查服务:**

```json
{
  "inputs": [
    {
      "name": "contract_type",
      "label": "合同类型",
      "type": "select",
      "required": true,
      "options": ["采购合同", "销售合同", "服务合同"]
    },
    {
      "name": "contract_content",
      "label": "合同内容",
      "type": "textarea",
      "required": true
    },
    {
      "name": "review_focus",
      "label": "审查重点",
      "type": "text",
      "required": false,
      "placeholder": "如:付款条款、违约责任"
    }
  ],
  "systemPrompt": "你是一个专业的合同审查助手。请审查以下{{contract_type}}:\n\n{{contract_content}}\n\n{{#if review_focus}}重点关注:{{review_focus}}{{/if}}\n\n请从法律风险、条款完整性、权责平衡等角度给出审查意见。"
}
```

为什么这样设计更好?
- 结构化输入让用户明确知道需要提供什么信息
- 类型化字段(select/textarea)提供更好的用户体验
- systemPrompt 中使用 `{{input_name}}` 引用输入,确保提示词和输入对应
- 业务场景清晰,AI 能给出更专业的回答

### 2.5 选择合适的模型

创建 AI 服务、数字员工或附件分类时,需要指定使用哪个大语言模型。**不同场景应该选择不同的模型**,因为各个模型有各自的优势领域。

#### 模型选择策略

**附件分类和文档提取** → 优先选择 **qwen** 或 **deepseek**

这类场景主要是从中文文档中提取结构化数据(合同、发票、简历等)。qwen 和 deepseek 在中文理解和文档解析方面表现更优。

推荐优先级: `qwen` > `deepseek` > `gpt-4` > `gpt-3.5`

使用场景:
- 采购合同信息提取
- 增值税发票字段识别
- 简历结构化解析
- 身份证信息提取
- 银行流水数据提取

**AI 服务(通用任务)** → 优先选择 **GPT-4** 或 **GPT-3.5**

AI 服务通常处理复杂的逻辑推理、内容生成、分析任务。GPT 系列在这些方面能力更强。

推荐优先级: `gpt-4` > `gpt-3.5` > `qwen` > `deepseek`

使用场景:
- 合同审查和风险分析
- 营销文案生成
- 数据分析报告
- 代码审查和生成
- 智能问答

**数字员工(对话交互)** → 优先选择 **GPT-4** 或 **GPT-3.5**

数字员工需要多轮对话、上下文理解和自然流畅的交互。GPT 系列在对话能力上更突出。

推荐优先级: `gpt-4` > `gpt-3.5` > `qwen` > `deepseek`

使用场景:
- 客服助手
- 业务咨询机器人
- 智能问答系统
- HR 招聘助理

#### 如何查询和选择模型

脚本会自动调用 `/api/aiagent/models` 接口获取租户下可用的模型列表,并根据上述策略自动选择。

手动查询模型:
```bash
curl -X GET "${WORKOPILOT_BASE_URL}/api/aiagent/models" \
  -H "API-KEY: ${WORKOPILOT_API_KEY}"
```

响应示例:
```json
{
  "code": 200,
  "data": [
    {
      "id": 123,
      "modelName": "通义千问 Plus",
      "modelCode": "qwen-plus"
    },
    {
      "id": 124,
      "modelName": "DeepSeek V3",
      "modelCode": "deepseek-chat"
    },
    {
      "id": 125,
      "modelName": "GPT-4 Turbo",
      "modelCode": "gpt-4-turbo"
    }
  ]
}
```

在配置文件中指定模型 ID:
```json
{
  "serviceCode": "contract-review",
  "modelId": 125,  // 使用 GPT-4 处理复杂的合同审查
  "systemPrompt": "..."
}
```

```json
{
  "CategoryCode": "invoice-extract",
  "ModelId": 123,  // 使用 qwen 提取中文发票信息
  "extractRules": [...]
}
```

#### 重要提醒

1. **创建前必须先查询模型** - 确保租户下已配置模型,否则会创建失败
2. **根据场景选择模型** - 不要所有场景都用同一个模型
3. **测试验证效果** - 创建后用真实数据测试,如果效果不理想可以尝试其他模型
4. **成本考虑** - GPT-4 能力强但成本较高,简单任务可以用 GPT-3.5 或国产模型

### 3. 创建配置文件

根据设计生成 JSON 配置文件。配置字段直接对应后端接口的字段名。

### 4. 调用脚本创建

运行对应的 Python 脚本。脚本会:
- 自动从环境变量或 .env 文件读取鉴权配置
- **自动查询可用模型并根据场景智能选择**
- 检查资源是否已存在(根据 code 查询)
- 如果存在则复用,不存在则创建
- 返回关键标识(serviceCode、robotId 等)

### 5. 验证和测试

创建成功后:
- 记录返回的关键 ID/Code
- 使用 `scripts/smoke_test.py` 或 curl 命令测试
- 确认功能符合预期
- **特别注意**: 如果是附件提取,用真实文档测试提取效果

### 6. 提供使用示例

输出后续使用的代码示例,包括:
- 完整的 API 调用代码(带错误处理)
- 参数说明和来源
- 安全提醒(APIKEY 不要暴露在前端)

## AI 服务创建的关键注意事项

AI 服务是最常用的功能,也最容易配置不当。遵循这些原则:

### 设计有意义的 inputs

根据业务场景设计输入字段,而不是只用 `user_message` 作为万能输入。

**不推荐的做法:**
```json
{
  "inputs": [{"name": "user_message", "label": "请输入", "type": "textarea"}]
}
```

这样的"空壳服务"没有体现业务逻辑,用户不知道该输入什么,AI 也无法给出专业回答。

**推荐的做法:**

根据业务场景设计具体字段。例如:

- **简历筛选服务:** `job_description`(岗位要求)、`resume_content`(简历内容)、`screening_criteria`(筛选标准)
- **文案生成服务:** `product_name`(产品名)、`target_audience`(目标人群)、`tone`(文案风格)、`key_points`(卖点)
- **数据分析服务:** `data_source`(数据来源)、`analysis_dimension`(分析维度)、`output_format`(输出格式)

### systemPrompt 必须引用所有 inputs

systemPrompt 中使用 `{{input_name}}` 引用输入字段。创建前检查:
- 每个 input 是否都在 systemPrompt 中被引用?
- 引用的占位符名称是否与 input.name 完全一致?
- 是否有拼写错误或遗漏?

**示例 - 正确的对应关系:**

```json
{
  "inputs": [
    {"name": "job_description", "label": "岗位描述", "type": "textarea"},
    {"name": "resume_content", "label": "简历内容", "type": "textarea"}
  ],
  "systemPrompt": "你是 HR 助手。请根据以下岗位要求:\n{{job_description}}\n\n评估这份简历:\n{{resume_content}}\n\n给出匹配度分析和建议。"
}
```

如果 systemPrompt 中没有引用某个 input,用户填写的数据就不会被 AI 使用,导致功能失效。

### 避免创建"空壳服务"

不要创建没有实际业务逻辑的服务。每个服务都应该:
- 有明确的业务场景和用途
- inputs 设计体现业务需求
- systemPrompt 包含领域知识和工作流程
- 能给用户带来实际价值

## 集成代码的输出要求

当提供 iframe 嵌入代码、API 调用示例等集成方案时,确保输出包含:

### 1. 完整可运行的代码

不要只给代码片段,要给完整示例。用户应该能直接复制使用(修改参数后)。

**示例 - AI 服务调用:**

```javascript
// 调用 AI 服务的完整示例
async function callAIService(serviceCode, inputs) {
  const WORKOPILOT_API_KEY = process.env.WORKOPILOT_API_KEY; // 从环境变量读取
  const BASE_URL = 'https://agent.workopilot.com/net-api';
  
  try {
    const response = await fetch(`${BASE_URL}/api/aiagent/run`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'API-KEY': WORKOPILOT_API_KEY
      },
      body: JSON.stringify({
        serviceCode: serviceCode,  // AI 服务的唯一标识
        inputs: inputs,            // 输入参数对象
        stream: false
      })
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API 调用失败: ${response.status} ${errorText}`);
    }
    
    const result = await response.json();
    
    if (result.code !== 200) {
      throw new Error(`业务错误: ${result.msg || '未知错误'}`);
    }
    
    return result.data; // 返回 AI 生成的内容
    
  } catch (error) {
    console.error('调用 AI 服务时出错:', error);
    throw error;
  }
}

// 使用示例
callAIService('contract-review-001', {
  contract_type: '采购合同',
  contract_content: '...',
  review_focus: '付款条款'
}).then(result => {
  console.log('AI 审查结果:', result);
}).catch(error => {
  console.error('调用失败:', error.message);
});
```

### 2. 清晰的参数说明

注释说明每个参数的:
- 含义和用途
- 来源(从哪里获取)
- 是否必需
- 格式要求

### 3. 错误处理

包含 try-catch 和有意义的错误提示。帮助开发者快速定位问题:
- HTTP 错误 - 检查网络、URL、鉴权
- 业务错误 - 检查参数、配置、权限
- 超时错误 - 考虑流式返回或增加超时时间

### 4. 安全提醒

明确告知:
- APIKEY 应该放在服务端环境变量,不要暴露在前端代码
- 不要将 APIKEY 提交到 Git 仓库
- 生产环境使用密钥管理服务

### 5. 验证方法

说明如何测试和确认成功:
- 提供测试命令或脚本
- 说明预期的返回结果
- 列出常见问题和解决方法

## 配置加载机制

所有脚本都支持多种配置方式,优先级从高到低:

### 1. 命令行参数(最高优先级)

```bash
python scripts/create_ai_service.py \
  --base-url https://agent.workopilot.com/net-api \
  --api-key your_api_key_here \
  --config service.json
```

适用场景:临时测试、CI/CD 环境、覆盖默认配置

### 2. 环境变量

```bash
export WORKOPILOT_BASE_URL="https://agent.workopilot.com/net-api"
export WORKOPILOT_API_KEY="your_api_key_here"
python scripts/create_ai_service.py --config service.json
```

适用场景:服务器部署、容器环境、多项目共享配置

### 3. 本地环境文件(推荐方式)

在项目根目录创建 `.env.workopilot`:

```properties
# 生产环境(默认)
WORKOPILOT_BASE_URL=https://agent.workopilot.com/net-api
WORKOPILOT_API_KEY=your_api_key_here

# 测试环境
# WORKOPILOT_BASE_URL=https://agenttest.workopilot.com/net-api
# WORKOPILOT_API_KEY=your_test_api_key_here
```

然后直接运行脚本,无需指定参数:

```bash
python scripts/create_ai_service.py --config service.json
```

脚本会自动发现并加载 `.env.workopilot` 或 `.env.local`。

适用场景:本地开发(推荐)

### 4. 默认值(仅 baseUrl)

如果以上都未配置:
- **生产环境(默认):** `https://agent.workopilot.com/net-api`
- **测试环境:** `https://agenttest.workopilot.com/net-api`

使用测试环境需要显式配置 `WORKOPILOT_BASE_URL` 或 `--base-url` 参数。

**注意:** APIKEY 没有默认值,必须配置。生产和测试环境的 APIKEY 不同,需要分别申请。

## 安全最佳实践

### 配置文件安全

**应该做的:**
- 使用 `.env.workopilot` 存储本地开发配置，用于协助用户配置喔壳的各种服务
- 检测当前是否存在配置文件，比如.env appsetting.json,config等按照当前的项目配置地方来配置apikey，这个配置是用于接口调用服务时使用 
- 确保 `.gitignore` 包含 `.env.workopilot` 和 `.env.local`
- 生产环境使用环境变量或密钥管理服务(如 AWS Secrets Manager)
- 可以提交 `.env.workopilot.example` 作为模板,但只包含占位值

**不应该做的:**
- 不要将 APIKEY 硬编码在代码中
- 不要将 APIKEY 提交到 Git 仓库
- 不要将 APIKEY 暴露在前端代码或浏览器中
- 不要在示例文件中使用真实 APIKEY

**示例 - .env.workopilot.example:**

```properties
# 复制此文件为 .env.workopilot 并填入真实值

# 生产环境(默认)
WORKOPILOT_BASE_URL=https://agent.workopilot.com/net-api
WORKOPILOT_API_KEY=replace_with_your_api_key

# 测试环境(取消注释以使用)
# WORKOPILOT_BASE_URL=https://agenttest.workopilot.com/net-api
# WORKOPILOT_API_KEY=replace_with_your_test_api_key
```

### iframe 技能卡片安全

iframe 技能卡片在测试时可以使用本地 URL,但发布到生产前必须:
1. 将 iframe URL 更新为正式域名(HTTPS)
2. 在正式域名部署并测试
3. 重新注册技能卡片或更新配置

本地测试 URL 只能在开发者本机访问,其他用户无法加载,会导致卡片空白。

## 脚本使用指南

### 推荐的使用方式

在开发者项目根目录运行脚本,脚本会自动发现 `.env.workopilot`:

```bash
# 在项目根目录
python path/to/scripts/smoke_test.py
python path/to/scripts/create_ai_service.py --config ai-service.json
python path/to/scripts/create_digital_employee.py --config digital-employee.json
python path/to/scripts/configure_app_menu.py --employee-id 1001 --action create --config app-menu.json
python path/to/scripts/register_iframe_card.py --config iframe-card.json
python path/to/scripts/create_attachment_classification.py --config attachment-classification.json
```

### 通用参数

所有脚本都支持:

```bash
--base-url <API_BASE_URL>        # API 基础 URL
--api-key <API_KEY>              # API 密钥
--env-file <ENV_FILE_PATH>       # 自定义环境文件路径
--config <CONFIG_FILE>           # 配置 JSON 文件
```

### 幂等性说明

脚本实现轻量级幂等,避免重复创建:

- `create_ai_service.py` - 按 `serviceCode` 查询,存在则复用
- `create_digital_employee.py` - 按 `robotCode` 查询,存在则复用
- `configure_app_menu.py` - create 遇到相同 `menuKey` 会提示改用 update；update 按 `employeeId + menuKey` 定位
- `create_attachment_classification.py` - 按 `GroupCode`+`CategoryCode` 查询,存在时默认编辑覆盖 `ExtractRules`(可用 `--no-edit-existing` 只复用不覆盖)
- `register_iframe_card.py` - 直接创建(当前开放接口只提供注册,不提供查询)

幂等性让脚本可以安全重复运行,适合自动化场景。

## 输出检查清单

帮助开发者完成任务后,确保输出包含:

- **鉴权配置说明** - 如何设置 WORKOPILOT_API_KEY,请求头格式(API-KEY)
- **接口路径** - 精确的 API 端点(注意 Document 服务的特殊路由)
- **关键标识** - 记录已创建资源的 `serviceCode`、`robotId`、`robotCode`、`skillRegistryId`
- **使用示例** - 完整的代码示例,包含参数说明和错误处理
- **验证方法** - 提供 smoke test 命令或 curl 示例
- **后续步骤** - 告诉用户接下来可以做什么
- **常见问题** - 预警可能遇到的问题和解决方法
- **安全提醒** - APIKEY 保管和使用的注意事项

## 特殊场景处理

### 附件分类与提取场景

附件分类与提取是喔壳的**核心高频功能**，特别是"直接提取"模式（90% 使用率）。

**典型需求:** "用户上传合同后，自动提取甲方、乙方、金额等信息填充到表单"

**快速指引:**

1. **检查分类是否存在** - 查询系统是否已有目标分类（如"采购合同"）
2. **创建分类**（如不存在）- 定义提取规则 `ExtractRules`，关键是字段的 `description`
3. **调用提取接口** - 指定 `categoryCode`，上传文件
4. **处理结果** - 获取结构化 JSON，填充表单

**详细内容包括:**
- 两种使用模式详解（分类+提取 vs 直接提取）
- 提取规则设计技巧（description 编写最佳实践）
- 完整开发流程（从需求分析到故障排查）
- 两种提取技术对比（OCR+LLM vs Vision-Language）
- 代码示例（完整的创建、调用、处理流程）
- 常见问题解决方案

👉 **请阅读:** `references/attachment-classification.md`

### AI 服务的 inputs 设计

AI 服务的核心是 `inputs` 和 `systemPrompt` 的配合。设计时:

1. **明确业务场景** - 这个服务要解决什么问题?
2. **识别输入要素** - 用户需要提供哪些信息才能完成任务?
3. **设计字段结构** - 每个输入用什么类型(text/textarea/select/number)?
4. **编写提示词** - systemPrompt 中用 `{{field_name}}` 引用输入
5. **检查完整性** - 所有 inputs 是否都在 systemPrompt 中被引用?

### Iframe 技能卡片的集成要点

如果用户说的是数字员工旁边的固定业务菜单(如“报价单历史”)，不要按技能卡片处理；应读取 `references/app-menu-iframe.md`，说明菜单 iframe 会带 `runtimeToken`、`userId`、`tenantId`，开发者后端需要用 `API-KEY + X-Runtime-Token` 调 runtime 接口解析上下文。

注册 iframe 技能卡片时,开发者需要了解:

**触发条件设计**
- 卡片何时显示?(基于消息内容、用户意图、业务状态)
- `showCard` 参数如何设置?

**数据获取**
- runtimeToken 如何获取?(调用 WorkoPilot 接口)
- 当前业务 ID/数据从哪里来?(父页面传递、URL 参数、localStorage)
- 当前登录用户信息如何获取?(调用父应用接口)

**开发和发布流程**
- 本地开发时先用 `http://localhost:xxxx` 测试
- 发布到生产前,部署到正式域名并更新卡片配置
- 测试卡片在实际场景中的加载和交互

## 响应格式说明原则

维护或生成接口文档时,响应示例应:

1. **使用 jsonc 格式添加注释**

```jsonc
{
  "code": 200,              // 业务状态码,200 表示成功
  "msg": null,              // 提示信息,成功时通常为空
  "data": {
    "id": 123,              // AI 服务 ID(Agent 记录此 ID 用于后续调用)
    "serviceCode": "xxx"    // AI 服务唯一标识(Agent 记录此 Code 用于 /api/aiagent/run 接口)
  }
}
```

2. **明确标注不可直接使用**

在代码块前说明:"以下示例带注释,仅供理解,不可直接作为 JSON 发送"

3. **说明 Agent 需要读取的字段**

注释中标注:"Agent 记录此 ID 用于..."、"Agent 使用此 Code 调用..."

4. **说明字段用于下一步的哪个调用**

让 Agent 清楚了解数据流向和使用场景。

这样 Agent 在阅读文档时,能准确理解需要提取哪些数据、如何使用这些数据。


# 本技能核心流程与要求
- 每次工作必须先检查是否有喔壳的apikey，如果不存在要先引导用户配置后再进行下一步，不要着急动手
- 每次工作必须检查相关服务，配置是否存在，比如在当前项目内接入喔壳的AI服务，附件取数，数字员工，必须先通过脚本查询喔壳是否已配置，没有配置协助用户配置。
- **计费检查**: 如果用户开发的数字员工包含高价值操作（生成文档、创建订单、数据导出、复杂分析、批量处理等），必须提醒用户集成计费模块，否则可能导致成本失控。参考 `references/billing.md` 了解如何集成。
- 必须严格遵守以上原则，通过喔壳脚本协助用户配置喔壳，通过接口文档将喔壳服务对接到当前系统，集成喔壳的任何服务或要开发喔壳的卡片，嵌入员工时要遵照喔壳的开发规范来开发相关的业务
