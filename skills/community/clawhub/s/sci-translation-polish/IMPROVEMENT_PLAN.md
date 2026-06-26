# 学术翻译技能完善计划

## 当前状态
- **完善度**：65/100
- **理论框架**：85分（扎实）
- **实操指导**：40分（严重缺失）

---

## 必须补充内容（按优先级）

### P0：执行工作流程（预估2小时）
**目标**：提供清晰的Step-by-Step执行流程

**新增章节**：`## V. Execution Workflow`
```
Step 1: Pre-processing Analysis
  - Identify journal type (Nature/IEEE/ACM/APA)
  - Extract key terms and create terminology table
  - Flag culture-specific concepts

Step 2: Semantic Extraction
  - Read each paragraph, ask "What is this actually saying?"
  - Remove Chinese rhetoric, keep only core meaning
  - Output: Bullet points of key ideas

Step 3: Logical Restructuring
  - Apply PEEL structure to each paragraph
  - Convert inductive → deductive logic
  - Create smooth transitions

Step 4: Native Writing
  - Write in English WITHOUT looking at Chinese original
  - Apply journal-specific style guidelines
  - Use terminology table for consistency

Step 5: Quality Check
  - Run through translationese checklist
  - Verify terminology consistency
  - Check citation style compliance

Step 6: Final Polish
  - Read aloud for flow
  - Trim unnecessary words
  - Strengthen verbs
```

---

### P1：Examples示例库（预估6-8小时）
**目标**：14-20个完整段落对照示例，覆盖多学科

**文件结构**：
```
examples/
├── medical_examples.md      # 医学领域 3-4个
├── cs_examples.md           # 计算机科学 3-4个
├── education_examples.md    # 教育学 3-4个
├── engineering_examples.md  # 工程学 3-4个
└── social_science_examples.md # 社会科学 3-4个
```

**每个示例格式**：
```markdown
## Example: [Title]
**Context**: [Journal type, field]

### Original Chinese
[原文段落]

### ❌ Translationese
[直译版本，展示常见错误]

### ✅ Native English
[专业润色后版本]

### Key Improvements
1. [具体改进点1]
2. [具体改进点2]
3. [具体改进点3]
```

---

### P2：References参考文档（预估4-5小时）
**目标**：10-12个权威参考文献

**文件结构**：
```
references/
├── academic_writing_guide.md     # 学术写作通用指南
├── nature_style_guide.md         # Nature投稿风格
├── ieee_style_guide.md           # IEEE投稿风格
├── apa_style_guide.md            # APA格式指南
├── terminology_database.md       # 常用术语数据库
├── common_errors.md              # 常见错误汇总
├── hedging_strategies.md         # 模糊限制语策略
├── transition_words.md           # 过渡词库
├── citation_styles.md            # 引用格式对比
├── abstract_writing.md           # 摘要写作指南
├── discussion_writing.md         # 讨论部分写作
└── response_letter.md            # 回复审稿人信
```

---

### P3：Prompts提示词模板（预估3-4小时）
**目标**：7个场景的提示词模板

**新增章节**：`## VI. Prompt Templates`
```
1. Full Paper Translation
2. Abstract Only
3. Discussion Section
4. Response to Reviewers
5. Cover Letter
6. Method Section
7. Results Presentation
```

---

## 改进目标
补充后完善度可达 **85-90分**，达到专业翻译服务中等以上水平。

---

## 执行策略
1. **先补P0** - 执行流程是骨架，优先完成
2. **再补P1** - Examples是血肉，影响用户体验
3. **然后P2** - References是支撑，增强专业性
4. **最后P3** - Prompts是工具，提升效率

---

**创建时间**：2026-04-09
**来源**：导师评估报告 + Anthropic官方skill-creator方法论
