---
name: wiki-compiler
description: 腾讯 IMA 知识库 Wiki 编译——将原始资料系统化组织为结构清晰的Wiki知识体系，并支持基于文章内容的自动打标签与标签体系管理。当用户说"建知识库""整理资料库""编译知识库""搭建wiki""知识体系化""把资料整理成wiki""给知识库打标签""按标签分类""标签整理"时触发。不适用于单篇摘要、简单问答、或仅搜索已有知识库内容的场景。
requires:
  skills:
    - name: ima-skill
      reason: 本技能依赖 ima-skill 提供的笔记管理和知识库操作能力
env:
  IMA_OPENAPI_CLIENTID: ima OpenAPI 客户端ID
  IMA_OPENAPI_APIKEY: ima OpenAPI API密钥
---

# 知识库 Wiki 编译器

核心理念：用 LLM 作为"知识编译器"，将原始资料一次性编译为结构清晰、内部互联的 Wiki 知识库，而非依赖传统 RAG 的碎片检索拼凑。编译后的 Wiki 是"真理之源"——LLM 直接基于对 Wiki 整体结构的理解进行自检索和回答，知识在系统中持续累积和演化。

## 整体流程

1. **需求理解与资料收集** — 明确主题边界
2. **检查旧版本** — 判断是否已有知识导览，决定增量更新还是新建
3. **编译生成** — 5步法构建Wiki知识体系（新建或增量更新）
4. **主动维护与迭代**

---

## 第一步：需求理解与资料收集

**判断用户状态：**
- 用户只给了主题？→ 先明确知识库边界和目标
- 用户已有资料（上传了文件 / 指定了知识库）？→ 直接进入编译
- 用户想维护已有 Wiki？→ 跳到第三步

**明确知识库边界：**
- 确认主题范围（如"量化投资""大模型应用"）
- 确认目标受众和用途（如"个人研究""团队参考"）
- 这些决定文件夹层级深度和概念粒度

**收集原始资料（"源代码"）：**
- 来源包括：用户上传的文件、已有知识库中的内容、网页文章、公众号文章
- 此阶段追求完整性，不追求结构——所有资料都是后续编译的"原材料"
- 如果用户指定了知识库（kb_id），用 `get_knowledge_list` 逐级浏览并收集所有文件
- 如果用户资料不足，主动用 `search(source="web")` 补充关键资料，但需告知用户

**确认门：** 向用户展示收集到的资料清单和知识库边界，确认后再进入编译。

---

## 第二步·前置：知识库结构诊断

> **目的**：在编译前诊断知识库的当前结构，识别散落文件和层级问题。
> **重要性**：基于 IMA 知识库的"虚拟文件夹"机制，文件可能"看起来在文件夹中"但实际 parent_folder_id 仍指向根目录。**必须先诊断再决定使用 `add_knowledge` 还是 `move_knowledge`**。

### 3.0 诊断流程

#### 步骤 1：拉取知识库根目录

```bash
# 拉根目录所有项目（不带 folder_id）
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/get_knowledge_list" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "limit": 50}'
```

#### 步骤 2：识别散落文件

```python
# 文件在根目录中（来自步骤 1），且 parent_folder_id 等于根目录 ID
ROOT_FOLDER_ID = "<知识库根目录 ID>"  # 通常通过 get_knowledge_base 获取

orphans = [f for f in root_items
           if f.get("media_type") != 99
           and f.get("parent_folder_id") == ROOT_FOLDER_ID]
```

#### 步骤 3：递归扫描文件夹层级

对每个文件夹调用 `get_knowledge_list(folder_id=...)`，记录：
- 子文件夹（`media_type == 99`）
- 文件数
- 每个文件的 `parent_folder_id` 是否等于当前 `folder_id`

#### 步骤 4：分类汇总

| 状态 | 含义 | 处理方式 |
|------|------|---------|
| 文件 parent_folder_id 是根目录 | 真正散落 | 用 `move_knowledge` 归类 |
| 文件 parent_folder_id 是文件夹 ID | 已归类 | 仅检查是否需要打标签 |
| 文件仅在根目录返回但 parent 是文件夹 | 虚拟关联 | 已正确处理 |

### 3.0 诊断输出模板

```markdown
## 知识库结构诊断报告

### 顶层文件夹
| 文件夹 | 文件数 | 含子文件夹 |
|--------|:------:|:----------:|
| ... | ... | ... |

### 散落文件
- 共 X 个文件 parent_folder_id 是根目录
- 列出每个文件的标题和推荐目标文件夹

### 多层结构
- AI 量化与深度学习/
  - 机器学习理论方法/（Y 个文件）
  - 大模型与智能体/（Y 个文件）
  - ...

### 处理建议
- 散落文件：调用 move_knowledge 归类
- 多层结构：导览放父级，子文件夹不需要各自导览
```

### ⚠️ 关键警告

**`add_knowledge` ≠ `move_knowledge`**：

| 操作 | 行为 | parent_folder_id 是否变化 |
|------|------|:-----------------------:|
| `add_knowledge` | 把文件"展示"在文件夹中（虚拟关联）| ❌ 不变（仍是原 parent）|
| `move_knowledge` | **真正改变** parent_folder_id | ✅ 变为目标文件夹 |

**仅调用 `add_knowledge` 而不调用 `move`，文件会永远挂在根目录**！

### 3.0 确认门

向用户呈现诊断报告后，确认：
- 是否需要归类散落文件？
- 是否需要多层结构整理？
- 是否需要新建主题导览？

确认后再进入第三步。

---

## 第二步：检查旧版本

> **重要**：每次编译前必须检查是否已有该主题的知识导览，避免重复创建或丢失历史版本信息。

### 检查方式

1. 在目标文件夹中搜索标题包含"主题导览"的笔记：
   ```bash
   curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/get_knowledge_list" \
     -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
     -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
     -H "Content-Type: application/json" \
     -d '{"knowledge_base_id": "<kb_id>", "folder_id": "<folder_id>", "count": 50}' | \
     python3 -c "import sys,json; data=json.load(sys.stdin); print([f['title'] for f in data.get('data',{}).get('list',[])])"
   ```

2. 如果找到"主题导览：xxx"笔记，记录其 `note_id` 和版本信息

3. 如果没找到，则进入新建流程

### 判断逻辑

| 情况 | 处理方式 |
|------|---------|
| 已有该主题的旧版本导览 | **增量更新**：读取旧版本内容 → 对比知识库增量 → 更新导览 |
| 已有其他主题的导览（非本主题） | **新建**：按正常流程创建新导览 |
| 没有任何知识导览 | **新建**：按正常流程创建新导览 |

### 增量更新流程

当存在旧版本时，执行以下步骤：

1. **读取旧版本**：调用 `export_note` 获取旧版本完整内容
2. **提取版本信息**：从标题下方的版本行获取版本号、更新日志
3. **对比知识库**：获取文件夹中最新的文件列表，与旧版本"相关主题"章节进行对比
4. **识别增量内容**：
   - 新增的文章（需要添加到对应核心概念的关键要素中）
   - 删除的文章（需要从列表中移除）
   - 概念变化（如有新增核心概念）
5. **更新导览内容**：
   - 保留原有结构和核心思想
   - 在关键要素中补充新增文章，移除已删除文章
   - 更新"实践建议"部分
   - 更新学习路径（如有新增依赖）
6. **更新版本号**：
   - 仅增删文章 → patch +0.0.1
   - 修改关键要素/实践建议 → minor +0.1
   - 结构变化 → major +1.0
7. **追加 changelog**：记录本次更新的内容摘要

---

## 第三步：预获取链接信息（编译前必做）

> **重要**：在编译导览笔记之前，必须先批量获取所有文件的链接特性，避免写完后发现无法链接导致返工。

### 步骤1：收集文件列表

获取文件夹中的所有文件，提取每个文件的 `media_id`、`media_type`、`title`：

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/get_knowledge_list" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "folder_id": "<folder_id>", "count": 100}' | \
  python3 -c "import sys,json; data=json.load(sys.stdin); [print(f\"{f['media_id']}|{f['media_type']}|{f['title']}\") for f in data.get('data',{}).get('list',[])]"
```

### 步骤2：批量获取链接特性

对每个文件调用 `export_media_for_ima_sandbox`：

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/export_media_for_ima_sandbox" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"media_id": "<media_id>"}'
```

### 步骤3：生成链接特性表

根据返回结果，建立如下表格：

| media_id | title | media_type | 链接策略 | URL/备注 |
|---------|-------|-----------|---------|---------|
| xxx | 文章A | 2 (网页) | ✅ 可内嵌 | https://... |
| xxx | 文章B | 6 (公众号) | ✅ 可内嵌 | https://... |
| xxx | 文章C | 7 (Markdown) | ⚠️ 不内嵌 | 请在知识库中查看 |
| xxx | 文章D | 11 (笔记) | ⚠️ 不内嵌 | 请在知识库中查看 |

### 步骤4：按类型分类编译

编译导览笔记时，根据链接特性表选择正确的写法：

| 文件类型 | 编译写法 |
|---------|---------|
| type 2/6 | `[标题](永久URL)` |
| type 7/11 | `标题`（纯文本，不加链接） |
| type 1/3/4/5 | `标题 — 请在知识库中查看` |

### 3.5 标签体系设计（文章级方案，可选但强烈推荐）

> **核心原则**：每篇文章 3-5 个关键词作为主题标签，不是固定词表。
> 文章级标签反映内容的"涉及主题"，文件夹反映"归属主题"，二者互补。

#### 标签分类（推荐）

| 类型 | 用途 | 示例 |
|------|------|------|
| **主题标签** | 文章涉及的主题 | 风险因子 / 量化策略 / 机器学习 |
| **属性标签** | 文章固有属性 | 科普 / 进阶 / 待补充 / 已验证 |
| **状态标签** | 维护状态 | 已编译 / 待审核 / 草稿 |

#### 设计流程

1. **拉取文件清单**：`get_knowledge_list` 用 `limit=50` + cursor 分页
2. **LLM 提取关键词**：对每篇文章调用 LLM，提取 3-5 个主题关键词
3. **用户审核**：展示标签清单给用户，支持修改/删除/补充
4. **批量打标**：用 `tag_add` 给每个文件打标签
5. **验证**：`get_knowledge_list(tags=[...])` 验证筛选效果

#### LLM 提取关键词的 prompt 模板

```text
你是一个知识管理专家。请阅读下面的文章，提取 3-5 个最能代表其内容主题的关键词。

要求：
1. 每个关键词 2-6 个中文字
2. 关键词应该是可复用的主题概念（不是专有名词）
3. 必要时可少于 3 个，但不要超过 5 个
4. 输出 JSON 数组

文章标题：<title>
（如有摘要：文章摘要：<summary>）

示例输入：标题="Fama-French 三因子模型详解"
示例输出：["多因子模型", "资产定价", "风险因子"]
```

#### 标签命名规范

✅ 推荐：
- `主题-XXX`：文章主题
- `属性-XXX`：文章属性
- `状态-XXX`：维护状态

❌ 避免：
- 过长（> 6 个汉字）
- 与文件夹名完全重复
- 一词多义（如"苹果"指水果还是公司）
- 临时标签不清理（如 `TODO`、`test`）

---

## 第四步：编译生成（新建模式）

> **适用于**：首次编译或结构重大调整

### 步骤1：明确主题 — 确定核心概念

在阅读所有原始资料后，明确：
- **主题定位**：这个知识库要解决什么问题？
- **核心概念**：有哪些不可分割的基础概念？
- **边界范围**：什么在范围内，什么不在？

### 步骤2：梳理关键词 — 提取关键要素

对每个核心概念，提取：
- **关键要素**：围绕该概念的子主题或相关问题
- **核心思想**：每个要素要传达的1-2句话

### 步骤3：发现关系 — 找出逻辑关联

建立概念之间的连接：
- **层级关系**：上下级依赖（如：随机过程 → 伊藤积分）
- **并列关系**：同层级互补（如：Alpha因子 || 风险因子）
- **因果关系**：先后依赖（如：因子拥挤 → IC衰减）
- **对立关系**：互斥选择（如：简约模型 vs 复杂模型）

### 步骤4：呈现结构 — 可视化知识网络

将关系转化为：
- **知识网络图**：用表格形式展示概念关联
- **推荐路径**：按难度/应用场景的学习路线

### 步骤5：美化优化 — 提升可读性

- **标题规范**：简洁有力，避免冗长
- **排版美观**：合理使用分级标题、列表、空行
- **信息密度**：每个章节有明确的信息承载量
- **可读性**：避免过长的段落，保持节奏

---

## 第五步：增量更新模式

> **适用于**：知识库已有该主题旧版本导览，需要增量更新

### 4.1 读取旧版本

```bash
# 导出旧版本笔记内容
curl -s -X POST "https://ima.qq.com/openapi/note/v1/export_note" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"note_id":"<旧版note_id>","target_content_format":1}' | \
  python3 -c "import sys,json,urllib.request; d=json.load(sys.stdin); url=d['data']['content_url']; req=urllib.request.Request(url); resp=urllib.request.urlopen(req); print(resp.read().decode('utf-8'))"
```

### 4.2 提取版本信息

从标题下方的版本行提取：
```
**版本**：v1.0 | 创建于 2026-05-08 | 更新于 2026-05-08
**更新日志**：v1.0 - 初始版本
```

### 4.3 对比知识库增量

获取文件夹最新文件列表，与旧版本对比：

```bash
# 获取文件夹中的文件列表
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/get_knowledge_list" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "folder_id": "<folder_id>", "count": 100}' | \
  python3 -c "import sys,json; data=json.load(sys.stdin); print([f['title'] for f in data.get('data',{}).get('list',[])])"
```

### 4.4 识别增量内容

| 类型 | 判断方式 | 更新方式 |
|------|---------|---------|
| 新增文章 | 旧版本"四、知识卡片"中不存在 | 补充到对应核心概念的关键要素中 |
| 删除文章 | 旧版本提及但知识库中已不存在 | 从列表中移除 |
| 概念变化 | 知识库中出现新的核心概念分类 | 新增核心概念卡片 |

### 4.5 更新导览内容

更新原则：
- **保留原有结构**：不改变核心概念划分方式
- **更新关键要素**：补充/移除文章引用
- **更新实践建议**：根据新增内容调整实践建议
- **更新学习路径**：如有新的依赖关系

**链接格式要求**（必须严格遵守，引用格式：`[《标题》](URL)`）：
- 所有引用必须提供**可点击的有效链接**
- 链接来源参考**第三步生成的链接特性表**，选择正确的写法：
  - 云文档类：使用相对路径格式 `[《标题》](路径)`
  - 网页链接：使用完整URL格式 `[《标题》](URL)`
  - 纯本地文件：使用文件路径格式并标注来源
- 禁止使用裸链接或纯URL文本，必须包装为引用格式

### 4.6 版本号更新

```yaml
---
version: 1.1  # patch+0.0.1 或 minor+0.1 或 major+1.0
created: 2026-05-08
updated: 2026-05-08
changelog:
  - v1.1: 增量更新，补充了X篇新文章，更新了关键要素描述
  - v1.0: 初始版本
---
```

**版本号规则**：
- 仅增删文章 → patch +0.0.1
- 修改关键要素描述或实践建议 → minor +0.1
- 核心概念结构变化（新增/删除核心概念） → major +1.0

---

## 第六步：写入笔记

## 导览笔记撰写规范

### 结构模板

> **模板来源**：基于"交易策略与系统"主题导览的专业实践版本

```markdown
# 主题导览：[主题名称]

**版本**：v1.0 | 创建于 YYYY-MM-DD | 更新于 YYYY-MM-DD
**更新日志**：v1.0 - 初始版本，基于知识库资料编译

## 一、主题定位
（主题定义 + 解决问题 + 核心逻辑 + 依赖链条）

本主题是XX的XX层，位于XX与XX之间。它解决的核心问题是：如何XX。
本主题涵盖XX、XX、XX三个关键环节，是XX的桥梁。其核心逻辑遵循清晰的依赖链条：XX → XX → XX → XX。

## 二、核心概念与关键要素

### （一）[核心概念A]
**核心思想**：一句话概括该概念的本质。

**关键要素**：
• 要素1：详细说明。相关文章[《文章标题》](链接)指出，具体内容...
• 要素2：详细说明。相关文章[《文章标题》](链接)进一步说明...
• 要素3：详细说明。

**实践建议**：
• 建议1：具体可操作的实践指导
• 建议2：具体可操作的实践指导

### （二）[核心概念B]
（同上结构）

## 三、学习路径（融合知识网络）

（以下学习路径以主线展示知识网络的连接关系，每个步骤标注了所需的核心知识储备和与之相关的概念。可根据主题实际需要设置1-N条路径，不必固定为两条）

（如有多条路径，在此展示）

## 四、相关主题

以下主题与"本主题名称"紧密关联，构成了更宽广的知识网络：

| 相关主题 | 与本主题的关系 | 关键连接点 |
|---------|--------------|-----------|
| XX | XX | XX |
| XX | XX | XX |
```

---

### 4章节结构规范

| 章节 | 内容详略 | 内容要求 | 写作要点 |
|------|---------|---------|---------|
| **一、主题定位** | **略写** 一段话（约100字） | 定义 + 解决问题 + 核心逻辑 + 依赖链条 | 用"是...的XX层，位于XX与XX之间"句式；依赖链条用箭头链展示 |
| **二、核心概念与关键要素** | **详写** 每概念约200-300字 | 核心思想 + 关键要素（引用文章） + 实践建议 | 每个关键要素都要引用知识库文章；实践建议要具体可操作 |
| **三、学习路径（融合知识网络）** | **中等** 表格+一段话 | 两条路径 + 表格形式 + 最终整合 | 表格内容精简，最终整合一段话点明闭环逻辑 |
| **四、相关主题** | **略写** 表格形式 | 主题 + 关系 + 连接点 | 说明每个关联主题的具体连接点，无需展开 |

---

### 关键要素写作规范

每个关键要素的写作采用以下结构：

```markdown
• 要素名称：详细说明。相关文章《文章标题》指出，具体内容...
• 要素名称：详细说明。相关文章《文章标题》进一步说明...
```

**要点**：
- 冒号前是要素名称（简洁短语）
- 冒号后是详细说明（1-2句话）
- 末尾用"相关文章[《标题》](链接)指出/进一步说明/提供了..."格式引用
- 引用来源必须是知识库中的实际文章
- **必须提供可点击的链接**，不能只写文章标题

---

### 实践建议写作规范

每个核心概念卡片末尾，用编号列表展示2-3条具体可操作的实践建议：

```markdown
**实践建议**：
• 先有逻辑，后有回测：策略设计应先论证底层投资逻辑，回测只是验证工具，不能替代逻辑思考。
• 动态适应：策略参数需随市场环境变化而调整，融入宏观前瞻和状态感知可增强跨周期表现。
• 简单性优先：优先选择参数少、逻辑清晰的简单策略，减少过拟合风险。
```

**要点**：
- 建议要具体可操作，不是空泛原则
- 每条建议都有明确的行动指引
- 可以引用具体文章中的实践方法

---

### 学习路径表格规范

**表格列定义**：
| 列名 | 内容 |
|------|------|
| 步骤 | 第X步：具体步骤名称 |
| 核心知识 | 需要掌握的核心概念 |
| 知识网络连接 | 与其他主题的关联（用→表示递进，用→ 需要表示依赖） |

**最终整合**：在表格后用一段话总结闭环流程。

---

### 版本控制机制

**版本信息格式**（放在大标题后）：

```markdown
> **版本**：v1.0 | 创建于 YYYY-MM-DD | 更新于 YYYY-MM-DD
> **更新日志**：v1.0 - 初始版本，基于知识库资料编译
```

**版本更新规则：**
- 增删文章 → patch 版本号 +0.0.1
- 修改关键要素/设计原则 → minor 版本号 +0.1
- 重新编译整个主题 → major 版本号 +1.0

**版本记录位置：** 在笔记大标题下方用加粗行标注版本号、创建日期、更新日期和更新日志。

### 链接处理规则

> **前置要求**：链接处理必须在**第三步（预获取链接信息）**中完成，不得在编译阶段临时获取。

根据预获取阶段生成的链接特性表，选择正确的链接策略：

| media_type | 类型 | 链接策略 |
|-----------|------|---------|
| **2** | 网页链接 | ✅ 获取真实URL，格式：`[《标题》](URL)` |
| **6** | 公众号文章 | ✅ 获取真实URL，格式：`[《标题》](URL)` |
| **7** | Markdown | ⚠️ 不内嵌链接，写为纯文本 |
| **11** | 笔记 | ⚠️ 不内嵌链接，写为纯文本 |
| **1** | PDF | ⚠️ 标注"请在知识库中查看" |
| **3** | Word | ⚠️ 标注"请在知识库中查看" |
| **4** | PPT | ⚠️ 标注"请在知识库中查看" |
| **5** | Excel | ⚠️ 标注"请在知识库中查看" |

**引用格式示例**：

```markdown
# 可链接的类型（type 2/6）
• 多维度指标体系：A股情绪温度计采集12个维度指标...[《A股情绪温度计》](https://...)详细阐述了...

# 不可直接链接的类型（type 7/11/1/3/4/5）
• 系统化执行：（请在知识库中查看）
```

### 获取公众号/网页的永久URL

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/export_media_for_ima_sandbox" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"media_id": "<文件media_id>"}'
```

返回的 `data.media_content_url_info.url` 即为永久可跳转链接。

### 特殊字符处理

文章标题中可能含有干扰Markdown渲染的字符：
- `|` → 替换为全角 `｜` 或省略
- `[` `]` `_` `*` → 需转义或省略

### 内容必须基于知识库实际文件

导览笔记的文章列表必须从 `get_knowledge_list` 返回的实际文件生成，不能依赖本地缓存文件。

---

### 6.5 多层文件夹归类（知识库结构整理）

> **目的**：把"真正散落"的文件（parent_folder_id 是根目录）按主题归类到对应文件夹。
> **前置**：必须先完成"第二步·前置：知识库结构诊断"（3.0）。

#### 何时需要执行

当 3.0 诊断发现以下情况时：
- 根目录有散落文件（parent_folder_id 是根 ID）
- 父文件夹下有应该归入子文件夹的文件
- 多层结构不一致

#### 步骤 1：列出待归类文件

```python
# 从诊断报告中获取散落文件
orphans = [(f["media_id"], f["title"]) for f in orphan_files]
```

#### 步骤 2：推荐目标文件夹（基于关键词）

| 关键词模式 | 推荐目标文件夹 |
|-----------|---------------|
| AkShare、BaoStock、OpenClaw、JQData、MooTdx、聚宽、a-stock-data、数据源、入门 | 数据工具与入门 |
| HFT、harris、Athena、净订单、信息差、微观结构、高频 | 高频交易与微观结构 |
| 情绪、a-share-sentiment | 金融情绪分析 |
| Fama-French、因子、融资融券、IF基差、基差、散户、定价、动量、反转、隔夜、华尔街 | 因子与资产定价 |
| Qlib、AI、Claude、智能体、遗传算法、深度学习、神经网络、图神经网络、LLM | AI 量化与深度学习（顶层）|
| 多层 AI 量化子文件夹 | 机器学习理论方法 / 大模型与智能体 / 深度学习与预测模型 |
| 其他（兜底） | 交易策略与系统 |

#### 步骤 3：批量调用 move_knowledge

```bash
# 移动到目标文件夹（src_kb_id == dst_kb_id 表示知识库内移动）
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/move_knowledge" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "src_knowledge_base_id": "<kb_id>",
    "dst_knowledge_base_id": "<kb_id>",
    "dst_folder_id": "<target_folder_id>",
    "dst_folder_name": "<target_folder_name>",
    "infos": [{"media_id": "<file1_media_id>"}, {"media_id": "<file2_media_id>"}]
  }'
```

**注意**：每次最多 10 个文件，分批调用。

#### ⚠️ move_knowledge 的副作用

| 副作用 | 说明 |
|--------|------|
| **parent_folder_id 改变** | ✅ 这是目标行为 |
| **文件标签可能丢失** | ⚠️ 移动前若有标签，先备份！|

**标签备份与恢复模式**：

```python
# 1. 移动前：备份标签
backup = {f["media_id"]: f.get("tags", []) for f in to_move_files}

# 2. 执行 move_knowledge
api_call("openapi/wiki/v1/move_knowledge", {...})

# 3. 移动后：恢复标签
for media_id, tags in backup.items():
    for tag in tags:
        tag_add(kb_id, media_id, real_title, tag)
```

#### 步骤 4：验证归类效果

```python
# 验证根目录为空
root_items = get_knowledge_list(kb_id, limit=50)  # 不带 folder_id
remaining = [f for f in root_items if f.get("media_type") != 99]
assert len(remaining) == 0, f"根目录仍有 {len(remaining)} 个散落文件"

# 验证每个文件夹的文件数符合预期
```

### 6.5 多层结构设计原则

- **导览放父级**：父文件夹放主题导览，子文件夹**不需要**各自的导览
- **MECE 划分**：子文件夹之间互斥、覆盖完整
- **层级不超过 3 层**：超过 3 层说明分类需要重新设计
- **避免"其他"类子文件夹**：用语义命名而非兜底类

### 6.5 与 6.6 的协同

- **6.5 归类**：解决文件物理位置问题
- **6.6 打标签**：解决多维度检索问题
- 两者互补：归类让文件夹清晰，打标签让检索灵活

---

### 6.6 应用标签（标签体系建立后）

> **前提**：已完成 3.5 标签体系设计，并已确认标签清单。
> **注意**：调用前必须确认用户对该知识库有写权限（创建者/协作成员/管理员）。

#### ⚠️ 关键 API 规范

**`item_name` 必须严格匹配**——使用 `get_knowledge_list` 返回的**完整标题**（含扩展名和括号内容）。简化标题会导致 `220001 文件名称不匹配` 错误。

**`limit` 范围 (0, 50]**——大库需要 cursor 分页循环。

#### 单文件打标

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/tag_add" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "knowledge_base_id": "<kb_id>",
    "item_id": "<file_media_id>",
    "item_name": "<get_knowledge_list 返回的完整 title>",
    "tag_name": "<标签名>"
  }'
```

#### 批量打标（推荐 Python）

```python
import urllib.request
import json

def api_call(path, data):
    url = f"https://ima.qq.com/{path}"
    headers = {
        "ima-openapi-clientid": "...",
        "ima-openapi-apikey": "...",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(
        url, data=json.dumps(data).encode("utf-8"),
        headers=headers, method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def batch_tag_files(kb_id: str, file_tag_map: dict[str, list[tuple[str, str]]]):
    """批量打标。
    file_tag_map: {media_id: [(title, tag), ...]}
    """
    for item_id, items in file_tag_map.items():
        for title, tag in items:
            api_call("openapi/wiki/v1/tag_add", {
                "knowledge_base_id": kb_id,
                "item_id": item_id,
                "item_name": title,  # ⚠️ 必须用完整标题
                "tag_name": tag,
            })
```

#### 重要特性

- **重复操作不报错**：`tag_add` 重复打、`tag_remove` 移除不存在的，都直接返回成功
- **文件夹不支持打标签**（media_type=99 会被 API 拒绝）
- **幂等性**：适合断点续传，无需先查状态

---

## 编译质量标准

1. **原子化**：每个知识节点围绕单一主题，避免东拉西扯
2. **关联性**：知识卡片之间通过超链接形成网状结构
3. **大纲化**：每个卡片内部有完整的章节结构
4. **可溯源**：标注每篇文章的来源出处
5. **可读性**：结构清晰、信息密度适中、美观易读

---

## 第七步：主动维护与迭代

知识库需要"活"起来，而非一次性建好就搁置。

### 6.1 健康检查（"体检"）

当用户说"检查知识库""知识库体检"时：

1. 扫描整个知识库，检查：
   - 是否有空文件夹（有待补充内容）
   - 是否有文件放错了分类
   - 主题之间是否有信息矛盾或重复
   - 是否有重要概念缺少覆盖
2. 生成健康检查报告，列出发现的问题和修复建议
3. 用户确认后执行修复

### 6.2 知识补充

当用户说"补充知识库""更新知识库"时：

1. 识别知识库中的薄弱环节（空文件夹、内容过时的主题）
2. 通过联网搜索补充最新资料
3. 将新资料编译后归入对应位置
4. 更新相关的交叉引用和索引
5. **更新知识导览**：触发增量更新流程（第二步）

### 6.3 输出与回流

用户可基于 Wiki 生成各类产出（研究报告、总结、幻灯片大纲等），这些产出保存回笔记本后，实现知识的"增量训练"——系统持续演化，而非一次性消耗。

### 6.4 标签审查（健康检查的补充）

当用户说"审查标签""整理标签"时：

#### 1. 列出所有标签

```bash
# cursor 分页循环拉取所有标签
cursor = ""
while True:
    r = api_call("openapi/wiki/v1/tag_list", {
        "knowledge_base_id": "<kb_id>",
        "cursor": cursor,
        "limit": 100,
    })
    items.extend(r["data"]["items"])
    if r["data"]["is_end"]: break
    cursor = r["data"]["next_cursor"]
```

#### 2. 检查命名规范

识别近似标签（关键词重叠 > 60%）：
- "机器学习" vs "ML" vs "Machine Learning"
- "风险" vs "风险因子" vs "风险类"

#### 3. 识别孤儿标签

对每个标签，用 `get_knowledge_list(tags=[...])` 检查关联文件数：
- 0 个 → 孤儿标签，建议删除
- < 3 个 → 弱标签，考虑合并
- > 100 个 → 热门标签，考虑细分

#### 4. 标签健康指标

| 指标 | 健康值 | 异常处理 |
|------|:-----:|---------|
| 每个标签的关联文件数 | 5-50 | < 3 考虑删除；> 100 考虑细分 |
| 标签总数 | < 50 | > 100 提示用户清理 |
| 近似标签对数 | 0 | 建议合并 |

#### 5. ⚠️ 破坏性操作前必须确认

`tag_delete` 和 `tag_rename` 是不可逆操作：
- `tag_delete`：所有关联自动解除
- `tag_rename`：新名重复会**自动合并**

**必须先**：
1. 用 `tag_list(keyword=新名)` 检查新名是否存在
2. 用 `get_knowledge_list(tags=[标签])` 列出受影响文件数
3. **用户显式确认**后再执行

---

## 重要提醒

- **预获取链接是编译前的必做步骤**——先建立链接特性表，再基于表编译，避免写完后发现无法链接导致返工
- **增量优先**：每次编译前必须检查旧版本，优先增量更新而非重新创建
- 编译是增量过程——第一次编译不必完美，后续维护中持续优化
- 核心价值在于"结构化 + 互联"而非单纯的文件分类
- 知识库规模适中时（数十到数百篇），LLM 内生理解优于向量检索
- 每次编译后保留变更记录，方便追溯和回退
- **产出是笔记本中的笔记**——使用 import_doc 创建笔记，写入笔记本

---

## 附录A：API命令模板

### 1. 检查文件夹中的笔记

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/get_knowledge_list" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "folder_id": "<folder_id>", "count": 50}'
```

### 2. 导出笔记内容

```bash
curl -s -X POST "https://ima.qq.com/openapi/note/v1/export_note" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"note_id":"<note_id>","target_content_format":1}' | python3 -c "
import sys,json,urllib.request
d=json.load(sys.stdin)
if d['code']==0:
    url=d['data']['content_url']
    req=urllib.request.Request(url)
    resp=urllib.request.urlopen(req)
    print(resp.read().decode('utf-8'))
else:
    print(d)
"
```

### 3. 构建请求JSON

```python
import json
with open('guide_content.md', 'r') as f:
    content = f.read()
with open('note_request.json', 'w') as f:
    json.dump({
        'content_format': 1,
        'content': content,
        'title': '📖 主题导览：[主题名称]'
    }, f, ensure_ascii=False, indent=2)
```

### 4. 创建笔记

```bash
curl -s -X POST "https://ima.qq.com/openapi/note/v1/import_doc" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d @note_request.json | python3 -m json.tool
# 返回: {"code": 0, "data": {"note_id": "xxx"}}
```

---

## 附录B：笔记本管理

### 获取/创建笔记本

```bash
# 列出笔记本
curl -s -X POST "https://ima.qq.com/openapi/note/v1/list_notebooks" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" | python3 -m json.tool

# 创建笔记本
curl -s -X POST "https://ima.qq.com/openapi/note/v1/create_notebook" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "知识导览"}' | python3 -m json.tool
```

### 更新旧笔记（增量更新时）

```bash
# 获取笔记列表
curl -s -X POST "https://ima.qq.com/openapi/note/v1/list_notes" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"notebook_id": "<notebook_id>", "count": 100}' | python3 -c "
import sys,json
d=json.load(sys.stdin)
for note in d.get('data',{}).get('notes',[]):
    if '主题导览' in note.get('title',''):
        print(f\"Found: {note['title']} -> note_id: {note['note_id']}\")
"

# 删除旧笔记
curl -s -X POST "https://ima.qq.com/openapi/note/v1/delete_note" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"note_id": "<旧note_id>"}' | python3 -m json.tool

# 重新创建（推荐方式，保留新的note_id）
```

---

## 附录C：标签管理 API 模板

### ⚠️ 通用 API 规范（基于试跑发现）

| 参数 | 规范 |
|------|------|
| `item_name` | 必须严格匹配 `get_knowledge_list` 返回的**完整标题** |
| `limit` | 范围 `(0, 50]`，超出返回错误 |
| 幂等性 | `tag_add` / `tag_remove` / `tag_delete` 重复调用都返回成功 |

### 列出标签

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/tag_list" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "keyword": "", "cursor": "", "limit": 100}'
```

### 按标签筛选文件

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/get_knowledge_list" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "tags": ["标签1", "标签2"], "limit": 50}'
```

### 重命名标签（⚠️ 破坏性）

```bash
# ⚠️ 调用前必须：
# 1. 用 tag_list(keyword=新名) 检查新名是否存在
# 2. 若存在，告知用户会"自动合并"并显式确认
# 3. 用 get_knowledge_list 列出受影响文件数
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/tag_rename" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "old_tag_name": "<旧名>", "new_tag_name": "<新名>"}'
```

### 删除标签（⚠️ 破坏性）

```bash
# ⚠️ 调用前必须：
# 1. 用 get_knowledge_list 列出该标签关联的文件数
# 2. 告知用户所有关联自动解除且不可恢复
# 3. 用户显式确认
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/tag_delete" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "tag_name": "<标签名>"}'
```

### 从文件移除标签

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/tag_remove" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "knowledge_base_id": "<kb_id>",
    "item_id": "<file_media_id>",
    "item_name": "<完整标题>",
    "tag_name": "<标签名>"
  }'
```

---

## 附录：IMA OpenAPI 调用方法

### 环境变量配置

```bash
# 必需的环境变量
IMA_OPENAPI_CLIENTID=你的ClientID
IMA_OPENAPI_APIKEY=你的APIKey

# 或使用配置文件
mkdir -p ~/.config/ima
echo "你的ClientID" > ~/.config/ima/client_id
echo "你的APIKey" > ~/.config/ima/api_key
chmod 600 ~/.config/ima/*
```

### 通用调用函数（Python）

```python
import urllib.request
import json

def ima_api(path, data=None):
    """IMA OpenAPI 通用调用函数"""
    headers = {
        "ima-openapi-clientid": "你的ClientID",
        "ima-openapi-apikey": "你的APIKey",
        "Content-Type": "application/json"
    }
    url = f"https://ima.qq.com/{path}"
    req = urllib.request.Request(
        url, 
        data=json.dumps(data or {}).encode('utf-8'),
        headers=headers,
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode('utf-8'))
```

### 常用 API 端点

| 功能 | 端点 | 关键参数 |
|------|------|---------|
| **获取知识库列表** | `openapi/wiki/v1/get_knowledge_list` | `knowledge_base_id`, `limit` |
| **搜索知识库** | `openapi/wiki/v1/search_knowledge_base` | `query`, `cursor`, `limit` |
| **获取笔记列表** | `openapi/note/v1/list_note_by_folder_id` | `cursor`, `limit` |
| **搜索笔记** | `openapi/note/v1/search_note` | `query_info` |
| **创建笔记** | `openapi/note/v1/import_doc` | `content_format`, `content` |
| **获取媒体信息** | `openapi/wiki/v1/get_media_info` | `media_id`, `knowledge_base_id` |

### 常见调用示例

#### 1. 获取知识库内容列表

```python
result = ima_api("openapi/wiki/v1/get_knowledge_list", {
    "knowledge_base_id": "你的知识库ID",
    "limit": 50
})
for item in result.get('data', {}).get('list', []):
    print(f"[{item.get('media_type')}] {item.get('title')}")
```

#### 2. 搜索知识库

```python
result = ima_api("openapi/wiki/v1/search_knowledge_base", {
    "query": "关键词",
    "cursor": "",
    "limit": 20
})
```

#### 3. 创建笔记

```python
result = ima_api("openapi/note/v1/import_doc", {
    "content_format": 1,
    "content": "# 标题\n\n正文内容"
})
note_id = result.get('data', {}).get('note_id')
```

### 错误代码参考

| code | 说明 |
|------|------|
| 0 | 成功 |
| 51 | 参数错误（如 limit 超出范围） |
| 220001 | 文件名称不匹配（item_name 未用完整标题） |
| 220004 | 无效的 knowledge_base_id |
| 220030 | 无写权限（普通成员调用 tag_add 等写操作） |
| 404 | API 端点不存在 |

### 移动文件接口（move_knowledge）

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/move_knowledge" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "src_knowledge_base_id": "<kb_id>",
    "dst_knowledge_base_id": "<kb_id>",
    "dst_folder_id": "<target_folder_id>",
    "dst_folder_name": "<target_folder_name>",
    "infos": [{"media_id": "<file_media_id>"}]
  }'
```

**infos 最多 10 个文件**。

| 参数 | 必填 | 说明 |
|------|:----:|------|
| src_knowledge_base_id | ✅ | 原知识库 ID |
| dst_knowledge_base_id | ✅ | 目标知识库 ID（同库移动时与 src 相同）|
| dst_folder_id | ❌ | 目标文件夹 ID（不传=根目录）|
| dst_folder_name | ❌ | 目标文件夹名称（二次校验）|
| infos | ✅ | 移动列表，每项含 `media_id` |

**注意**：返回的 `data.move_results[media_id].ret_code` 表示单文件结果，需检查每个文件的 ret_code 而非顶层 code。

---

## 附录D：试跑经验教训

> 基于 2026-06-29 在量化投资知识库（kb_id: I_49nAThDICNno0gyhjl4dU1zUFtkNWv0X7mhlBQID8=）的 6 步试跑总结。

### 经验 1：`item_name` 必须严格匹配完整标题

完整标题包括扩展名（如 `.pdf`）和括号内容。例如：

```json
// ❌ 简化标题（失败，code=220001）
{"item_name": "金融人工智能：用Python实现AI量化交易"}

// ✅ 完整标题（成功）
{"item_name": "金融人工智能：用Python实现AI量化交易 (伊夫-希尔皮斯科) (z-library.sk, 1lib.sk, z-lib.sk).pdf"}
```

**建议**：从 `get_knowledge_list` 拿标题后不要做任何处理，原样用作 `item_name`。

### 经验 2：`limit` 参数范围 (0, 50]

最大 50，超过会返回 51 错误。大库需要 cursor + is_end 循环分页。

### 经验 3：API 幂等性

`tag_add` 重复打、`tag_remove` 移除不存在的——均直接返回成功。可放心重试和断点续传。

### 经验 4：清理完全可逆

`tag_remove` 后文件 `tags` 字段变为 `[]`，不留痕迹。**`tag_delete` 才是不可逆的**，所以推荐用 `tag_remove` 而不是 `tag_delete` 来"清理"测试。

### 经验 5：媒体类型覆盖建议

试跑中覆盖了 PDF/笔记/公众号/网页（4 种）。未覆盖 Word/PPT/Excel/Markdown/视频/图片等。**真实场景使用前**建议覆盖完整 14 种类型。

### 经验 6：标签数量预期

文章级标签每篇 3-5 个，128 篇内容的知识库预计产生 384-640 个标签。
**标签总数 > 100 时建议人工审查命名规范**。

### 经验 7：标签与导览的协同

通过 `get_knowledge_list(tags=["状态:已编译"])` 可一键筛出所有"已编译导览"，实现"按状态找导览"的需求。配合 `tags=[]` 多标签筛选可发现跨主题相关内容。

### 经验 8：`add_knowledge` ≠ `move_knowledge`（最关键）

> ⚠️ **这是本次试跑发现的最核心经验**。

| 操作 | 行为 | parent_folder_id |
|------|------|:----------------:|
| `add_knowledge` | 文件"展示"在文件夹中（虚拟关联）| ❌ 不变 |
| `move_knowledge` | 真正改变 parent_folder_id | ✅ 变为目标文件夹 |

**仅调用 `add_knowledge` 不调用 `move`，文件会永远挂在根目录**——即使它"看起来在文件夹里"。

判断方法：拉根目录所有项目，看每个文件的 `parent_folder_id`。如果指向根 ID，就是真正散落。

### 经验 9：move_knowledge 会清空标签

`move_knowledge` 在改变 parent_folder_id 时，**会清空文件的标签数组**。

**应对模式**：
1. 移动前备份标签：`backup[media_id] = file["tags"]`
2. 执行 move_knowledge
3. 移动后逐个重新打标：`for tag in backup[media_id]: tag_add(...)`

### 经验 10：根目录调用 ≠ 知识库全貌

不带 `folder_id` 调 `get_knowledge_list` 会返回**所有项目**（含 7 个文件夹 + 35 个散落文件 + 60 个已分配文件的"虚拟副本"）。

**真正判断散落的方法**：比较文件的 `parent_folder_id` 与知识库根目录 ID。

### 经验 11：多层文件夹结构诊断

复杂知识库（如"AI 量化与深度学习"含 3 个子文件夹）需要**递归扫描**：

```
for folder in root_folders:
    items = get_knowledge_list(folder_id=folder.id)
    sub_folders = [f for f in items if f.type == 99]  # 子文件夹
    files = [f for f in items if f.type != 99]  # 直接文件
    
    for sub in sub_folders:
        sub_items = get_knowledge_list(folder_id=sub.id)
        # ... 继续递归
```

判断标准：
- 父文件夹下的"直接挂载文件"如果主题匹配子文件夹，**应该移到子文件夹**
- 导览应放父级，**不需要**给每个子文件夹单独生成导览

### 经验 12：量化投资知识库实战数据（2026-07-01）

| 阶段 | 文件数 | 散落文件 | 标签 | 主题导览 |
|------|:------:|:--------:|:----:|:-------:|
| 初始 | 35 | 35 | 0 | 1 |
| 演示后 | 36 | 35 | 20 | 1 |
| 6 导览+30 打标 | 66 | 35 | 264 | 7 |
| 归类后（move_knowledge）| 101 | 0 | 264 | 7 |
| 多层归类后（PDF 单独处理）| 135 | 0 | 264 | 7 |

**关键收获**：
- 35 个根目录文件归类 → 0 散落
- 14 个父文件夹文件移到子文件夹 → 结构清晰
- 所有 244 个标签保留（移动文件前无标签，零风险）
