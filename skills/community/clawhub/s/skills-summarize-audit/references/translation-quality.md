# 翻译质量评估 TQI v1.0 — Translation Quality Index

> 大脑加强：把 v7.1.0 的"命中词典就 ready"升级为四维量化评分。
> 业界参考：BLEU（n-gram 精确率）/ COMET（神经网络语义）/ BERTScore（嵌入相似）/ MQM（多维质量度量）。
> 本技能不引入模型，采用规则化的"轻量 TQI"，覆盖 80% 的实用场景。

## 一、TQI 四维评分（核心创新）

| 维度 | 权重 | 满分标准 | 扣分项 | 0 分示例 | 10 分示例 |
|:-:|:-:|---|---|---|---|
| **术语保护率** | 30% | 所有受保护术语（API/CLI/MCP 等）100% 保留 | 每个被翻译/丢失的术语 -2 | "应用程序编程接口" | "API" |
| **触发词命中率** | 30% | 符合"动词+宾语"或"主题→功能·功能·功能"格式 | 缺触发词 -3，格式错乱 -2 | "用于搜索网络内容" | "互联网调研 → 13渠道·多平台" |
| **长度合规率** | 20% | ≤40 字符（侧栏短说明）；≤80（长描述） | 每超 10 字符 -1 | 整段 200 字描述 | "DOCX → 创建·编辑·分析" |
| **同源一致性** | 20% | 同类技能（如 3 个 MCP）描述风格统一 | 与同组平均差异大 -2 | 同组里独一份的句式 | 同组都是"X → A·B·C" |

### TQI 综合分公式

```
TQI = 术语×0.30 + 触发词×0.30 + 长度×0.20 + 同源×0.20
```

### 判定阈值

| TQI | 等级 | 处理 | 标签 |
|:-:|:-:|---|:-:|
| ≥8.0 | 🟢 ready | 直接采用 | `ready` |
| 6.0–7.9 | 🟡 minor | 修改 1-2 处即可采用 | `needs_minor` |
| 4.0–5.9 | 🟠 rewrite | 需重新翻译 | `needs_agent_refinement` |
| <4.0 | 🔴 fail | 放弃翻译，保留原文 | `untranslatable` |

## 二、保护术语清单（v1.0）

> 这些术语在任何情况下都必须保留原文，不得意译

```yaml
protected_terms:
  # 协议/标准
  - HTTP, HTTPS, SSL, TLS, SSH, FTP, TCP, UDP, DNS, CDN
  
  # 协议/规范
  - MCP, ACP, SDK, API, REST, GraphQL, gRPC, WebSocket, JSON-RPC
  
  # 文件格式
  - JSON, YAML, TOML, XML, HTML, CSS, CSV, MD5, SHA256
  - DOCX, XLSX, PPTX, PDF, PNG, JPG, SVG, GIF
  
  # 语言/运行时
  - Python, JavaScript, TypeScript, Go, Rust, Java, Kotlin, Swift, Ruby, PHP
  - Node.js, Deno, Bun, .NET, JVM
  
  # 框架/库（短名）
  - React, Vue, Angular, Svelte, Next.js, Nuxt, Astro
  - Django, Flask, FastAPI, Express, NestJS, Spring Boot
  - PyTorch, TensorFlow, Transformers, LangChain
  
  # 平台/产品
  - Codex, Claude, Cursor, GitHub, GitLab, OpenAI, Anthropic
  - ZCode, Xiaping, ClawHub
  - npm, pip, brew, cargo
  
  # 工具
  - MCP, CLI, IDE, LSP, CI, CD, PR, TDD, BDD
  
  # 数据库
  - PostgreSQL, MySQL, SQLite, MongoDB, Redis, Supabase
  
  # 云服务
  - AWS, GCP, Azure, Vercel, Netlify, Cloudflare
```

### 自动判定规则

```python
# 伪代码：检查译文是否保留所有保护术语
def check_protected_terms(original, translation):
    protected_in_original = [t for t in PROTECTED_TERMS if t in original]
    preserved_in_translation = [t for t in protected_in_original if t in translation]
    
    if not protected_in_original:
        return 10  # 无保护术语，本维度满分
    
    ratio = len(preserved_in_translation) / len(protected_in_original)
    return round(ratio * 10, 1)
```

## 三、触发词命中率检查

### 合格格式（任一）

```
格式 A: 触发词 → 功能1·功能2·功能3
        例: "互联网调研 → 13渠道·多平台·信息获取"

格式 B: 触发词·同义词 → 动词+宾语
        例: "技能审查·审计 → 画像·评分·推荐"

格式 C: 双语并列: 中文 | English
        例: "总结 → 错误收割·自进化·压缩 | Summarize → ..."
```

### 扣分规则

| 问题 | 扣分 |
|---|:-:|
| 无 `→` 或 `·` 分隔符 | -3 |
| 触发词是完整句子（>10 字符无分隔） | -3 |
| 触发词在原英文中找不到对应（凭空生成） | -2 |
| 触发词太宽泛（如"工具"、"功能"） | -1 |

### 检测算法

```python
def check_trigger_quality(translation, skill_id):
    score = 10
    
    # 1. 必须有 → 或 · 分隔符
    if '→' not in translation and '·' not in translation:
        score -= 3
    
    # 2. 触发词部分（→ 之前或 · 之前）不超过 10 字符
    trigger_part = translation.split('→')[0].split('·')[0]
    if len(trigger_part) > 10:
        score -= 2
    
    # 3. 触发词与 skill_id 相关
    # 简单词形匹配：summarize → 总结/归纳/汇总/精炼
    # 完整映射表见 codex-ui-zh-glossary.json skill_overrides
    if not is_relevant_trigger(trigger_part, skill_id):
        score -= 2
    
    # 4. 触发词过于宽泛
    vague_words = ['工具', '功能', '助手', '系统', '模块', '应用']
    if any(w in trigger_part for w in vague_words):
        score -= 1
    
    return max(0, score)
```

## 四、长度合规检查

### 阈值

```yaml
length_thresholds:
  sidebar_short_description:
    max_chars: 40       # 字符数
    penalty_per_10: 1   # 每超 10 字符扣 1 分
  
  command_palette_display_name:
    max_chars: 24
  
  long_description:
    max_chars: 80
    penalty_per_20: 1   # 每超 20 字符扣 1 分
```

### 字符数计算规则

- 中文字符：算 1
- 英文字母：连续字母组合算 1（如 "API" = 1，"Codex" = 1）
- 数字：连续数字算 1
- 标点：算 1
- 空格：不算

> 这个规则使中英混排的描述长度估算更接近"认知长度"

```python
def cognitive_length(text):
    # 中文每个字算 1
    # 英文连续字母算 1（一个词 = 1）
    # 数字连续算 1
    pattern = r'[\u4e00-\u9fff]|[A-Za-z]+|[0-9]+|.'
    tokens = re.findall(pattern, text)
    return len([t for t in tokens if t.strip()])
```

## 五、同源一致性检查

> 同类技能的描述风格应当统一，避免用户认知负担

### 同类分组规则

```yaml
similarity_groups:
  
  - group: "MCP 服务器"
    pattern: 'name.*mcp|type:\\s*mcp-server'
    expected_style: "{能力名} → {动作}·{对象}·{产出}"
    example: "Firecrawl → 抓取·搜索·爬取"
  
  - group: "官方文档技能"
    pattern: 'source.*anthropic|source.*openai'
    expected_style: "动词+宾语，正式语调"
    example: "审查拉取请求评论"
  
  - group: "调研类技能"
    pattern: 'tags.*research|tags.*search'
    expected_style: "{调研主题} → {渠道}·{平台}·{产出}"
    example: "互联网调研 → 13渠道·多平台·信息获取"
  
  - group: "总结/记忆类"
    pattern: 'tags.*summary|tags.*memory'
    expected_style: "{核心动作} → {子能力1}·{子能力2}"
    example: "总结 → 错误收割·自进化·压缩"
```

### 一致性评分

```python
def check_consistency(translation, same_group_translations):
    if not same_group_translations:
        return 10  # 无同类对比项，本维度满分
    
    # 计算与同组的平均风格相似度
    # 简单特征：是否有 → 符号、是否有 · 分隔、是否有双语
    def features(t):
        return [
            1 if '→' in t else 0,
            1 if '·' in t else 0,
            1 if '|' in t else 0,
            len(t) // 10,  # 长度档位
        ]
    
    my_feat = features(translation)
    group_feats = [features(t) for t in same_group_translations]
    avg_feat = [sum(f[i] for f in group_feats) / len(group_feats) for i in range(len(my_feat))]
    
    # 余弦相似度
    similarity = cosine_similarity(my_feat, avg_feat)
    return round(similarity * 10, 1)
```

## 六、自学习规则（关键创新）

> 当用户确认某条翻译后，自动从该确认中学习，扩充术语库

### 学习触发条件

```yaml
auto_learn:
  
  enabled: true
  
  # 触发：用户在报告中标注 "ready" 或 "verified"
  triggers:
    - user_marks_ready
    - user_accepts_candidate
    - manual_add_to_glossary
  
  # 学习对象
  learn_from:
    - field: "phrases"
      # 短语级：英文短语 → 中文翻译
      # 例：从 "create dashboards for product metrics" → "构建产品指标仪表板"
      condition: "原文是短语（≤8 词）且译文无 needs_* 标记"
      store_in: "codex-ui-zh-glossary.json#phrases"
    
    - field: "skill_overrides"
      # 技能级：skill_id → 中文 display_name + short_description
      # 例：imagegen → { display_name: "图像生成", short_description: "..." }
      condition: "skill_id 已知且译文 TQI ≥ 8"
      store_in: "codex-ui-zh-glossary.json#skill_overrides"
    
    - field: "words"
      # 词级：英文单词 → 中文词
      # 例：从 "scrape" 在多个上下文中均译为 "抓取"
      condition: "同一英文词在 3+ 不同技能中被译为同一中文"
      store_in: "codex-ui-zh-glossary.json#words"
```

### 学习流程（不动手，只指导）

```
1. Audit 输出翻译候选 + TQI 分数
2. 用户在确认对话中说："imagegen 这个翻译我用"
3. Audit 检测到确认信号（ready 标记）
4. Audit 输出学习建议：
   "📌 已学习：imagegen → 图像生成 / 为网站、游戏等生成或编辑图像
    建议追加到 codex-ui-zh-glossary.json 的 skill_overrides 段。
    是否授权写入？"
5. 用户授权 → Audit 给出 agent 应执行的修改：
   - 文件: ~/.agents/skills/skills-summarize-audit/references/codex-ui-zh-glossary.json
   - 操作: 在 skill_overrides 段追加键值对
   - 学习时间: 2026-07-19T03:00Z
   - 学习来源: user_confirmed
6. Agent（用户的）按指令完成写入
```

### 反学习（unlearning）

```yaml
# 用户标记某条学习无效时
unlearn:
  triggers:
    - user_marks_wrong
    - translation_proved_problematic
  
  action:
    - 从 learned_phrases / learned_overrides 段移除
    - 不删除 base 段（保留手工维护的核心词典）
    - 在 .data/glossary-unlearn-log.jsonl 记录，避免重复学习
```

## 七、TQI 报告输出格式

```text
📋 翻译质量报告（TQI 评分）

| 技能 ID | 原文 | 译候选 | TQI | 术语 | 触发 | 长度 | 一致 | 等级 |
|---|---|---|:-:|:-:|:-:|:-:|:-:|:-:|
| imagegen | Generate or edit images | 图像生成 → 为网站·游戏生成或编辑 | 9.2 | 10 | 10 | 8 | 9 | 🟢 ready |
| old-skill | Use when you want to research | 研究 → 多源·对比·报告 | 7.0 | 10 | 7 | 8 | 3 | 🟡 minor |
| broken | Some random text here | 通用技能 | 2.5 | 0 | 0 | 10 | 0 | 🔴 fail |

⚠️ 待精炼：
  - old-skill: 触发词 "研究" 与同组（research 类）的 "调研/搜索" 不一致
  - broken: 术语保护率 0%（原文无可识别术语）

📌 已学习（本次确认）：
  - "图像生成 → ..." 写入 codex-ui-zh-glossary.json#skill_overrides
  - 累计学习条目: 28
```

## 八、与 v7.1.0 的兼容性

### 向下兼容

- v7.1.0 的 `collect_codex_display_candidates.py` 输出的 `translation_quality` 字段保留
- 旧值映射：
  - `ready` → TQI ≥ 8
  - `needs_agent_refinement` → TQI < 8（细分为 `needs_minor` 和 `needs_agent_refinement`）

### 新增字段

```python
# 在 collect_codex_display_candidates.py 输出中追加
translation_quality_v2:
  tqi_score: 8.5
  tqi_grade: "ready"  # ready / needs_minor / needs_agent_refinement / untranslatable
  tqi_breakdown:
    term_preservation: 10
    trigger_match: 9
    length_compliance: 8
    source_consistency: 7
  learned: false       # 是否从用户确认中学习的
  learnable: true      # 是否符合自动学习条件
```

## 九、质量回归（self-audit）

> 本技能自身的 description 必须通过 TQI ≥ 8

```yaml
self_audit:
  target: "skills-summarize-audit"
  fields:
    - SKILL.md frontmatter description
    - agents/openai.yaml interface.short_description
  expected_tqi: ">= 8"
  on_fail: "输出修正候选，标记 self_audit_failed=true"
```

## 十、维护

- 新增保护术语：追加到第二节 protected_terms
- 新增同类分组：追加到第五节 similarity_groups
- 自学习阈值调整：第六节 triggers
- 业界评估方法对照：BLEU/COMET/BERTScore/MQM 在 _docs/translation-research.md（如有）
