---
name: zhz-english-learning
description: "英语学习材料生成器：从课文中提取单词、生成音频、创建互动学习页面（课文学习+单词测验+原文理解+句子测验）。Use when user asks to create English learning materials, vocabulary exercises, or 英语学习资料。"
homepage: http://openclaw.bjbook.net/
---

# 英语学习材料生成器 (zhz-english-learning)

从英文课文生成完整学习材料：单词列表、单词/课文音频、4 个互动学习页面（带侧边栏导航互相跳转）。

## 前置依赖

```bash
pip install edge-tts pydub
```

系统需安装 ffmpeg（pydub 用于拼接音频）。

## 工作流程

### 步骤 1：提取单词

从用户提供的英文课文中提取 5~20 个重点单词，保存到 `md/words.md`：

```markdown
# 单词列表

| English | Phonetic | POS | Chinese |
|---------|----------|-----|---------|
| apple | /ˈæp.əl/ | n. | 苹果 |
| beautiful | /ˈbjuː.tɪ.fəl/ | adj. | 美丽的 |
```

- 选择有学习价值的词汇（非常用词、课文关键词）
- POS 使用简写：n. / v. / adj. / adv. / prep. / conj. / pron. / det.
- 音标使用 IPA 格式

### 步骤 2：生成单词音频

```bash
python {baseDir}/scripts/generate_word_audio.py -w md/words.md -o sounds
```

每个单词生成 3 个音频文件到 `sounds/` 目录：
- `{word}_male.mp3` — 男声英文朗读
- `{word}_female.mp3` — 女声英文朗读
- `{word}_chinese.mp3` — 女声中文释义

同时生成 `words.mp3` 合集（顺序：男声→女声→中文，单词间有停顿）。

### 步骤 3：生成课文音频

```bash
python {baseDir}/scripts/generate_text_audio.py --textfile txt/lesson.txt -o sounds/lesson.mp3
```

可选参数：`-r "-15%"` 调整语速，`-v VOICE` 指定音色。

### 步骤 4：生成课文翻译

agent 根据课文生成中文翻译文件 `txt/translation.txt`。

### 步骤 5：生成课文学习页

```bash
python {baseDir}/scripts/generate_lesson_page.py -t txt/lesson.txt -a sounds/lesson.mp3 -o lesson.html --translation txt/translation.txt
```

生成 `lesson.html`：左侧导航栏 + 展示原文 + 音频播放器（带倍速控制）+ 中文翻译。

### 步骤 6：生成单词测验页

```bash
python {baseDir}/scripts/generate_word_quiz.py -w md/words.md -s sounds -o quiz.html
```

生成 `quiz.html`，包含 4 种测验模式：

| 模式 | 说明 |
|------|------|
| 听音选义 | 播放英文发音两遍（男声→女声），选择中文含义（四选一） |
| 英文选义 | 显示英文单词，选择中文含义（四选一），播放发音两遍 |
| 中文选义 | 显示中文含义，选择英文单词（四选一），播放发音两遍 |
| 默写单词 | 显示中文含义，输入英文单词，提交后播放发音两遍 |

### 步骤 7：生成原文理解测验页

agent 根据课文生成题目 JSON 文件 `json/reading_questions.json`，格式：

```json
[
  {
    "type": "choice",
    "question": "What did the boys come out to do?",
    "options": ["A. Play football", "B. Blow bubbles", "C. Feed the cat", "D. Wash the door"],
    "answer": 1,
    "explanation": "原文：The boys have come out on the porch to blow bubbles."
  },
  {
    "type": "judge",
    "question": "The bubble burst when it landed on the cat's back. (True/False)",
    "options": ["True", "False"],
    "answer": 1,
    "explanation": "原文说 'does not burst'，泡泡没有破裂。"
  }
]
```

- `type`: `"choice"`（单选题）或 `"judge"`（判断题）
- `answer`: 正确选项的索引（从 0 开始）
- `explanation`: 可选的解析说明

```bash
python {baseDir}/scripts/generate_reading_quiz.py -q json/reading_questions.json -o reading_quiz.html
```

### 步骤 8：生成句子测验页

agent 根据课文生成句子练习 JSON 文件 `json/sentence_questions.json`，格式：

```json
[
  {
    "type": "fill",
    "sentence": "The boys have come out on the porch to blow ___.",
    "word_bank": ["bubbles", "soap", "mat", "door"],
    "answer": ["bubbles"],
    "explanation": "原文：to blow bubbles（吹泡泡）"
  },
  {
    "type": "transform",
    "original": "The old cat is asleep on the mat.",
    "hint": "将 'asleep' 替换为 'sleeping'，使用现在进行时：",
    "options": [
      "The old cat is sleeping on the mat.",
      "The old cat sleep on the mat.",
      "The old cat was sleep on the mat.",
      "The old cat sleeping on the mat."
    ],
    "answer": 0,
    "explanation": "is asleep → is sleeping，使用 be + V-ing 结构。"
  }
]
```

- `type`: `"fill"`（搭配填空）或 `"transform"`（句型替换）
- fill: `sentence` 中用 `___` 表示填空位，`word_bank` 是备选词，`answer` 是按顺序的正确答案
- transform: `original` 是原句，`hint` 是改写提示，`options` 是四选一选项，`answer` 是正确选项索引

```bash
python {baseDir}/scripts/generate_sentence_quiz.py -q json/sentence_questions.json -o sentence_quiz.html
```

## 生成的文件结构

源文件按类型分别存放：

```
project/
├── md/                        # Markdown 文件
│   └── words.md               # 单词列表
├── txt/                       # 纯文本文件
│   ├── lesson.txt             # 课文原文（用户提供）
│   └── translation.txt        # 中文翻译（agent 生成）
├── json/                      # JSON 数据文件
│   ├── reading_questions.json # 原文理解题目（agent 生成）
│   └── sentence_questions.json # 句子练习题目（agent 生成）
├── lesson.html                # 📖 课文学习页
├── quiz.html                  # 📝 单词测验页
├── reading_quiz.html          # 📚 原文理解测验页
├── sentence_quiz.html         # ✏️ 句子测验页
├── words.mp3                  # 单词音频合集
└── sounds/                    # 音频文件目录
    ├── {word}_male.mp3
    ├── {word}_female.mp3
    ├── {word}_chinese.mp3
    └── lesson.mp3
```

## 页面导航

所有 4 个 HTML 页面共享左侧导航栏，可直接点击跳转到其他页面：
- 📖 课文学习 (`lesson.html`)
- 📝 单词测验 (`quiz.html`)
- 📚 原文理解 (`reading_quiz.html`)
- ✏️ 句子测验 (`sentence_quiz.html`)

移动端自动变为顶部导航栏。

## 默认音色

| 用途 | Edge-TTS 音色 |
|------|---------------|
| 英文男声 | en-US-GuyNeural |
| 英文女声 | en-US-JennyNeural |
| 中文女声 | zh-CN-XiaoxiaoNeural |

## 注意事项

- 所有脚本使用 UTF-8 编码
- 音频生成需要网络连接（Edge-TTS 在线服务）
- words.md 中的 English 列不区分大小写用于文件名匹配
- 测验页中音频文件路径相对于 sounds 目录
- 原文理解和句子测验的题目由 agent 根据课文内容生成 JSON 文件
