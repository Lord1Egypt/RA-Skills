# Orchestrator Archive Guide / 归档流程指南

> **Version:** v1.1 | **Updated:** 2026-03-31
> **Executor:** Orchestrator Agent (main session)

---

## 🎯 Archive Responsibilities / 归档职责

**Orchestrator Agent must perform all archive operations itself, without external scripts.**

---

## 📋 Full Archive Workflow / 完整归档流程

### Step 1: Read Temp File / 读取临时文件

```python
# Relative to your book directory
temp_file = "books/{BOOK_NAME}/temp_chapters/chapter-N.txt"
with open(temp_file, 'r', encoding='utf-8') as f:
    content = f.read()
```

### Step 2: Split Content & Metadata / 分离正文和元数据

```python
if '【变量更新】' in content:
    main_content, variables_section = content.split('【变量更新】', 1)
    main_content = main_content.strip()
else:
    main_content = content

# Extract title (first line)
lines = main_content.split('\n')
title = lines[0].strip().lstrip('# ')
main_content = '\n'.join(lines[1:]).strip()
```

### Step 3: Extract Continuity / 提取 continuity 信息

- Extract `setups` (foreshadowing created)
- Extract `payoffs` (foreshadowing resolved)
- If no continuity data output by Writer Agent, leave empty — do not fabricate

### Step 4: Word Count / 统计字数

```python
import re
chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', main_content))
english_words = len(re.findall(r'[a-zA-Z]+', main_content))
word_count = chinese_chars + english_words
```

### Step 5: Update canon_bible.json

```python
canon_file = "books/{BOOK_NAME}/meta/canon_bible.json"
# Read → update continuity (setups/payoffs/pending_setups) → Save
```

### Step 6: Create Summary JSON

```python
summary_file = f"books/{BOOK_NAME}/summaries_json/chapter_{N:03d}.json"
chapter_data = {
    "chapter": N,
    "title": title,
    "word_count": word_count,
    "summary": summary_text,
    "setups": setups,
    "payoffs": payoffs
}
```

### Step 7: Move to Final Location

```python
final_file = f"books/{BOOK_NAME}/chapters/chapter-{N}_{title}.txt"
```

### Step 8: Verify Archive

- [ ] `chapters/chapter-N_标题.txt` exists
- [ ] `summaries_json/chapter_N.json` exists
- [ ] `canon_bible.json` updated
- [ ] Temp file deleted

---

## ⚠️ Key Principles / 关键原则

1. **No external scripts** — Orchestrator handles everything / 不依赖外部脚本
2. **Data truthfulness > completeness** — Never fabricate / 数据真实性 > 完整性
3. **Step-by-step verification** / 逐步验证
4. **Serial execution** — Archive current chapter completely before starting next / 串行执行
