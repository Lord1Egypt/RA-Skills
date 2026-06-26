# 灵魂提取 Prompt 模板

## 对话分析提取 Prompt

分析以下对话内容，提取用户的人格信息。只提取你有把握的信息（置信度 > 0.6），不要猜测或编造。

### 提取维度（7 axes）

请按以下格式输出 JSON，**只**包含本次对话中**新发现**的信息：

```jsonc
{
  // 1. 身份（含生活习惯 + 数字身份）
  "basic_info": {
    "name":     { "value": "...", "confidence": 0.9 },
    "occupation": { "value": "...", "confidence": 0.9 },
    "location":   { "value": "...", "confidence": 0.9 },
    "favorite_apps": ["..."]    // 列表类型直接给数组
  },

  // 2. 性格
  "personality": {
    "traits":  ["新发现的性格标签"],
    "values":  ["新发现的价值观"],
    "decision_style": "...",
    "motivation_drivers": ["驱动力"]
  },

  // 3. 语言风格
  "language": {
    "catchphrases":      ["口头禅（出现 2+ 次才算）"],
    "sentence_patterns": ["句式模式描述"],
    "examples":          ["原文例句（直接引用）"],
    "formality_level":   "casual / semi-formal / formal",
    "verbosity":         "concise / moderate / verbose",
    "humor_style":       "描述",
    "filler_words":      ["语气词"],
    "agreement_expressions": ["同意时的表达"],
    "disagreement_expressions": ["不同意时的表达"]
  },

  // 4. 知识与观点
  "topics": [
    {
      "name":         "话题名",
      "sentiment":    "positive / negative / neutral / mixed",
      "stance":       "立场描述",
      "key_opinions": ["具体观点（要有论据）"]
    }
  ],
  "knowledge": {
    "domains":            ["熟悉的领域"],
    "skills":             ["专业技能"],
    "belief_frameworks":  ["信奉的方法论：第一性原理 / 二八法则 / 结论先行 / ..."]
  },

  // 5. 记忆（情景 + 情感）
  "episodic": [
    {
      "event":        "事件描述",
      "emotion":      "当时的情绪",
      "context":      "背景",
      "significance": "normal / important / milestone"
    }
  ],
  "emotional": {
    "triggers": {
      "joy":   ["让 TA 开心的事"],
      "anger": ["让 TA 生气的事"],
      "frustration": ["挫败感来源"]
      // 12 种情绪：joy/anger/sadness/anxiety/excitement/nostalgia/
      //           pride/gratitude/frustration/curiosity/peace/guilt
    },
    "expression_style":   "...",
    "empathy_level":      "low / medium / high",
    "coping_mechanisms":  ["..."]
  },

  // 6. 工作偏好
  "workflow": {
    "tools": {
      "ide":           ["Cursor", "VS Code", "Xcode"],
      "terminal":      ["iTerm2"],
      "ai_tools":      ["Claude Code", "Cursor"],
      "vcs":           ["GitHub", "GitLab"],
      "doc_systems":   ["Notion", "Obsidian"],
      "communication": ["Slack"]
    },
    "tech_stack": {
      "languages":  ["C++", "Python", "Swift"],
      "frameworks": ["React", "FastAPI"],
      "platforms":  ["macOS", "iOS"]
    },
    "hard_rules":          ["禁止 git rebase（仅 merge）", "脏工作树直接 abort"],
    "collab_conventions":  ["公开仓库使用 dqsjqian@163.com"],
    "cli_habits":          ["偏好 gh CLI 而非 git push"],
    "output_preferences": {
      "preferred_format":  "表格优先 / 列表 / 段落",
      "preferred_length":  "简短 / 中等 / 详尽",
      "preferred_tone":    "直接 / 温和 / 活泼",
      "structure_first":   "结论先行 / 推导优先"
    },
    "pet_peeves": ["反感冗长解释", "反感铺垫'好的我来帮你'"]
  },

  // 7. 理想抱负
  "aspirations": {
    "long_term_goals":      ["做一个独立开发者"],
    "active_projects": [
      { "name": "soul-archive", "status": "活跃迭代中", "expectation": "发布到 GitHub" }
    ],
    "identity_aspirations": ["成为兼具技术与产品视野的资深工程师"],
    "skills_to_learn":      ["Rust 异步编程"],
    "knowledge_gaps":       ["最新的 LLM agent harness 设计"]
  },

  "summary": "一句话总结本次提取发现了什么"
}
```

### 提取原则

1. **只提取明确信息**：用户说"我在武汉"→ location: 武汉（✓）；用户聊到武汉的天气 → 不能推断 location（✗）
2. **语言风格看原文**：直接引用用户原话作为 examples，不改写
3. **口头禅要出现 2+ 次**：只出现一次的不算
4. **观点要有论据**：不只记录立场，还要记录支撑理由
5. **情感触发看语境**：不是用户提到的话题，而是能引发 TA 情绪变化的事物
6. **未提及的字段留空**：不要填 null 或空数组，直接不包含该字段
7. **Workflow 优先级最高**：用户的硬规则、反感的事、输出偏好一旦发现就要采集——这是 AI 后续协作时立刻能用的部分
8. **Aspirations 要有方向性**：抓"想做/在做/想学/不懂"这四类，而不是抓所有提到的事情

### 写入策略（自动）

- 写入前会用 bigram-Jaccard 相似度（默认 ≥0.85）做去重合并，无需担心重复条目
- 冲突信息会被标记，不会自动覆盖
- 高置信度优先（confidence > 0.6 才会被记录）

### 触发词

中文：灵魂沉淀 / 灵魂提取 / 灵魂存档 / 沉淀一下 / 分析我

英文：soul extract / soul archive / soul update / soul snapshot / soul sediment
