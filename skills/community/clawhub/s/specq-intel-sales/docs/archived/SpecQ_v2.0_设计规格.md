# SpecQ v2.0 设计规格

> 日期：2026-06-23 | 作者：悟空（PM + 架构工程师） | 状态：设计阶段
> 基于 v1.0 升级，新增记忆系统 + 联网搜索 + 多模态 + 智能编排

---

## 一、v1.0 → v2.0 变更总览

### Tool 变更

| Tool | 动作 | 说明 |
|---|---|---|
| `specq_memory` | 🆕 新增 | 三层记忆（recall / save / get_plan / set_plan） |
| `specq_search` | 🆕 新增 | 联网搜索实时公开数据 |
| `specq_generate_intel` | ✏️ 修改 | 增加联网搜索注入、脱敏、多格式输出 |
| `specq_log_visit` | ✏️ 修改 | 增加图片/语音/视频输入 |
| `specq_extract_insights` | ✏️ 修改 | 增加本地/在线数据库读取 |
| `specq_feedback` | ✏️ 修改 | 增加成交率追踪埋点 + 自动写入记忆 |

### Skill 编排层变更

| 项 | 动作 | 说明 |
|---|---|---|
| 场景判断 | ✏️ 修改 | 新增自动意图路由（无需用户指定走哪个分支） |
| 脱敏规则 | 🆕 新增 | 内置于所有输出 pipeline，客户名→行业标签 |
| 多任务管理 | 🆕 新增 | 由 `specq_memory` 的 get_plan/set_plan 驱动 |
| 多模态输入 | 🆕 新增 | 图片 OCR、语音转录、视频关键帧提取 |
| 多格式输出 | 🆕 新增 | Word (.docx)、PPT、邮件、聊天消息 |

---

## 二、新增 Tool 规格

### 2.1 specq_memory — 三层记忆

> 详见飞书文档：https://www.feishu.cn/docx/Us68dycZJosRIQxMQ5ccI3eInZb

| action | 功能 | 必填参数 |
|---|---|---|
| `recall` | 语义搜索召回记忆 | query, limit(默认5), uid |
| `save` | 写入一条新记忆 | content, category, uid, metadata(可选) |
| `get_plan` | 读取当前工作记忆 | uid |
| `set_plan` | 设定/更新工作记忆 | goal, plan, current_step, uid |

**存储方案**：
- 长期记忆：ChromaDB `specq_memory` collection，智谱 embedding-2，1024 维
- 工作记忆：`{SPECQ_DATA_DIR}/specq_working_memory_{uid}.json`
- Per-user 隔离：长期记忆按 `user_id` metadata 过滤，工作记忆按 uid 分文件

**Memory 分类**：

| category | 触发时机 | 保留策略 |
|---|---|---|
| `visit` | log_visit 后自动写 | 永久 |
| `feedback` | feedback 后自动写 | 永久 |
| `intel` | generate_intel 后自动写 | 180 天 |
| `insight` | extract_insights 结构化发现 | 180 天 |
| `preference` | 用户显式偏好 | 永久 |

### 2.2 specq_search — 联网搜索

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| query | str | ✅ | 搜索关键词 |
| limit | int | ❌(默认5) | 返回结果数 |
| source | str | ❌(默认"web") | 搜索源：web / news / scholar |

**处理流程**：
1. 调用搜索引擎 API（建议 Brave Search 或 SerpAPI）获取 Top-N 摘要
2. 对每条摘要做关键信息提取（技术指标、参数、竞品名）
3. 返回结构化结果

**响应格式**：
```json
{
  "results": [
    {
      "title": "...",
      "url": "...",
      "snippet": "...",
      "published": "2026-06-20",
      "extracted_info": {"competitor": "安美特", "metric": "Ra<0.3μm"}
    }
  ],
  "total": 5,
  "source": "web"
}
```

**使用场景**：
- `generate_intel` 调用前：补充公开网页中的竞品动态、行业新闻
- 作为情报包模块 2（竞品格局）和模块 3（应用场景适配）的实时数据补充

---

## 三、修改 Tool 规格

### 3.1 specq_generate_intel（修改）

**新增参数**：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| product | str | ✅ | （不变） |
| application | str | ✅ | （不变） |
| scenario | str | ✅ | （不变） |
| **output_format** | str | ❌(默认"markdown") | **🆕 输出格式：markdown / docx / ppt / email / chat** |
| **context_block** | str | ❌ | **🆕 外部注入的上下文块（来自 memory.recall / search 结果）** |
| **anonymize** | bool | ❌(默认true) | **🆕 是否脱敏客户名称** |

**处理流程变更**：
```
原有流程（不变）：
  三字段 → extract_insights → 暗数据注入 → LLM 生成 → 输出

🆕 新增步骤：
  ① specq_search(product + application) → 联网补充竞品/行业信息
  ② specq_memory.recall(product + customer) → 召回历史记忆
  ③ 合并为独立上下文块（【历史记忆】+【联网搜索】）
  ④ 注入 → LLM Prompt
  ⑤ 脱敏后处理（如 anonymize=true，替换客户名为行业标签）
  ⑥ 按 output_format 格式化输出
```

**输出格式映射**：

| output_format | 输出内容 | 说明 |
|---|---|---|
| `markdown` | 八模块 Markdown | ✅ 已有 |
| `docx` | .docx 文件（八模块） | 🆕 生成 Word 文档 |
| `ppt` | PPT 提纲（八模块 → 幻灯片结构） | 🆕 生成汇报提纲 |
| `email` | 邮件正文 + 主题 | 🆕 可直接复制发送 |
| `chat` | 300 字精简消息 | 🆕 适配飞书/微信 |

### 3.2 specq_log_visit（修改）

**新增参数**：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| customer_id | int | ✅ | （不变） |
| content | str | ✅ | （不变） |
| visit_date | str | ❌ | （不变） |
| visit_type | str | ❌ | （不变） |
| **image_paths** | list[str] | ❌ | **🆕 图片文件路径列表（名片/白板/报告截图）** |
| **audio_path** | str | ❌ | **🆕 录音文件路径（自动转文字）** |
| **video_path** | str | ❌ | **🆕 视频文件路径（提取关键帧+语音）** |

**处理流程变更**：
```
原有：文本直接存储
🆕：
  ① 如有 audio_path → 调用语音转文字 API → 追加到 content
  ② 如有 image_paths → OCR 提取文字 → 追加到 content
  ③ 如有 video_path → 提取关键帧 + 语音转录 → 追加到 content
  ④ 合并后的 content → 存储
  ⑤ 自动写入 memory.save(category="visit", content=内容摘要)
```

### 3.3 specq_extract_insights（修改）

**新增参数**：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| customer_id | int | ❌ | （不变） |
| limit | int | ❌ | （不变） |
| **db_path** | str | ❌ | **🆕 本地数据库路径（SQLite）** |
| **db_query** | str | ❌ | **🆕 SQL 查询语句** |
| **api_url** | str | ❌ | **🆕 在线数据库 API 地址** |
| **api_params** | dict | ❌ | **🆕 API 查询参数** |

**处理流程变更**：
```
原有：CRM 拜访记录 + 丢单复盘 → LLM 提取
🆕 新增数据源：
  ① 本地 SQLite → 执行 db_query → 结构化数据 → 注入 LLM
  ② 在线 API → GET api_url + api_params → 注入 LLM
  ③ 所有数据源统一注给 LLM 提取洞察
```

### 3.4 specq_feedback（修改）

**新增参数**：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| product | str | ✅ | （不变） |
| application | str | ✅ | （不变） |
| outcome | str | ✅ | （不变） |
| lesson | str | ❌ | （不变） |
| accuracy_notes | str | ❌ | （不变） |
| **uid** | str | ❌(默认"default") | **🆕 用户标识（用量追踪）** |

**处理流程变更**：
```
原有：存储反馈 → 返回确认
🆕 新增：
  ① 自动写入 memory.save(category="feedback", content=lesson)
  ② 埋点：记录 uid + product + outcome + timestamp（用于成交率漏斗）
```

---

## 四、Skill 编排层变更

### 4.1 场景判断（自动路由）

```
用户输入
  ↓
① 意图识别（Keyword + LLM）
  ├─ 匹配"情报包" / "攻单" → 场景 A/B（新/老客户）
  ├─ 匹配"上次" / "之前" / "聊过" → 场景 C（查历史）
  ├─ 匹配"成交" / "丢了" / "赢了" → 场景 D（反馈）
  ├─ 匹配"多个" / "三个" / "一批" → 场景 E（多任务）
  └─ 默认 → 场景 A（新客户情报包）
```

### 4.2 脱敏规则

**规则**：
- 所有输出中，客户真实公司名自动替换为行业标签（如"华南 PCB 中大型厂"）
- 联系人姓名、手机号、邮箱全部移除
- 替换矩阵：`{customer_name} → {industry}_{region}_{scale}`

**实现**：Skill 输出后处理 + generate_intel 的 System Prompt 约束

### 4.3 多模态输入处理

**优先级**：
1. 音频 → 语音转文字 → 重点提取
2. 图片 → OCR → 结构化提取
3. 视频 → 关键帧 + 语音 → 合并处理

**实现**：log_visit tool 内部处理，对 Skill 透明

### 4.4 多格式输出

**路由规则**：
- 用户说"发邮件" / 无明确格式 → `email`
- 用户说"做 PPT" / "汇报" → `ppt`
- 用户说"Word" / "导出" → `docx`
- 用户说"总结一下" / 聊天场景 → `chat`
- 默认 → `markdown`

---

## 五、运维观测层

### 5.1 用量追踪

| 指标 | 埋点位置 | 说明 |
|---|---|---|
| 日活用户 | feedback.uid | 每天有多少不同用户 |
| Tool 调用次数 | 每个 tool 入口 | 哪个功能用得最多 |
| 情报包生成量 | generate_intel | 核心 KPI |
| P95 延迟 | tool 计时 | 性能监控 |
| 错误率 | 异常捕获 | 可用性 |

### 5.2 成交率验证

```
漏斗：
  generate_intel 调用数
    → log_visit 调用数（情报包→实际拜访）
      → feedback.outcome=won（成交）
      → feedback.outcome=lost（丢单）
```

**基准线**：v2.0 上线前手工记录基线数据，一个月后对比。

---

## 六、数据流全景（v2.0）

```
用户输入（文本/图片/语音/视频）
  ↓
① 多模态处理（OCR / 语音转文字 / 关键帧提取）
  ↓
② specq_memory.recall → 【历史记忆】
  ↓
③ specq_memory.get_plan → 检查未完成任务
  ↓
④ 场景判断 → 路由到对应分支
  ↓
⑤ specq_search(query) → 【联网搜索】
  ↓
⑥ extract_insights(customer, db_path, api_url) → 【暗数据】
  ↓
⑦ generate_intel(product, application, scenario, context_block, output_format, anonymize)
  ├─ 脱敏后处理
  └─ 按 output_format 格式化
  ↓
⑧ specq_memory.save → 写入长期记忆
  ↓
⑨ 输出（Markdown / Word / PPT / 邮件 / 聊天消息）
  ↓
⑩ feedback(outcome) → 写入成交记录 + 埋点
```

---

## 七、MCP Server 文件结构（v2.0）

```
specq-mcp/
├── mcp_server.py          # 6 个 tool（主线，~800行）
├── memory.py              # 记忆模块（ChromaDB + embedding）
├── search.py              # 联网搜索模块
├── multimodal.py          # 多模态处理（OCR / 语音 / 视频）
├── output.py              # 多格式输出（docx / ppt / email）
├── anonymizer.py          # 脱敏模块
├── analytics.py           # 用量追踪模块
├── SKILL.md               # Skill 工作流文档（v2.0）
├── requirements.txt       # 依赖清单
├── .env.example           # 配置模板
├── LICENSE                # Apache 2.0
└── README.md              # 接入文档
```

---

## 八、成功标准

| 指标 | 目标 |
|---|---|
| 记忆召回准确率 | ≥85% |
| 召回延迟 P95 | ≤500ms |
| 联网搜索延迟 P95 | ≤5s |
| 情报包生成延迟 P95（含搜索+记忆） | ≤60s |
| 暗数据注入率 | 有历史记录的客户 100% 注入 |
| 脱敏准确率 | 100%（不应出现真实客户名） |
| 输出格式正确率 | 100% |
| 成交率变化 | v2.0 上线后 3 个月对比基线 |

---

## 九、MVP 边界

### v2.0 做

- 6 个 MCP Tool（4 修改 + 2 新增）
- 场景判断自动路由
- 脱敏规则（客户→行业标签）
- 多格式输出（Markdown / Word / PPT / 邮件 / 聊天）
- 多模态输入（图片 OCR / 语音转文字 / 视频关键帧）
- 联网搜索实时数据
- 用量追踪 + 成交率漏斗
- Per-user 记忆隔离

### v2.0 不做

- 记忆自动合并/去重
- 实时语音对话（只做录音转录）
- 视频实时分析（只做关键帧提取）
- 自定义脱敏规则（只用预设模板）
- 邮件/PPT 的视觉效果模板（只生成内容结构）

---

*悟空 🐱 | 2026-06-23*