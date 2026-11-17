# 输出格式规范

本文档定义 song-translation-expert skill 的多种输出格式及其使用场景。

## 目录

1. [默认聊天输出：Markdown 逐行对照](#1-默认聊天输出markdown-逐行对照)
2. [整段对照格式](#2-整段对照格式)
3. [表格对照格式](#3-表格对照格式)
4. [JSON 结构化格式](#4-json-结构化格式)
5. [Word 文档输出](#5-word-文档输出)
6. [Excel 表格输出](#6-excel-表格输出)
7. [PDF 文档输出](#7-pdf-文档输出)
8. [LRC 文件格式](#8-lrc-文件格式)

---

## 1. 默认聊天输出：Markdown 逐行对照

### 使用场景

- 用户在聊天中直接要求翻译
- 用户想快速查看翻译结果
- 默认格式，无需用户指定

### 格式规范

```markdown
## {曲名} - {艺人}

**语种**：{Language} | **流派**：{Genre} | **年份**：{Year}

---

{原文第1行}
{译文第1行}

{原文第2行}
{译文第2行}

...

---

### 译注

注1：{注释内容}
注2：{注释内容}
```

### 完整示例

```markdown
## Imagine - John Lennon

**语种**：English | **流派**：Pop/Philosophical | **年份**：1971

---

Imagine there's no heaven
试想一下世界上没有天堂

It's easy if you try
如果你试着想像，其实并不难

No hell below us
我们脚下也没有地狱

Above us only sky
头顶上只有一片蓝天

Imagine all the people Living for today
想像一下每个人都为当下而活

---

### 译注

注1：Imagine 是 John Lennon 1971 年发行的标志性和平主义歌曲，呼吁用想象力构建一个没有国界、没有宗教冲突的乌托邦。译者保留了 "Imagine" 的祈使句式，引导听众主动参与想象。
```

---

## 2. 整段对照格式

### 使用场景

- 用户要求"原文一段，译文一段"
- 适合抒情长诗类歌曲
- 适合博客/文章发布

### 格式规范

```markdown
## {曲名}

### 原文

{原文段落1}

{原文段落2}

### 译文

{译文段落1}

{译文段落2}
```

### 适用判断

- 歌词较短（< 20 行）且文学性强：适合整段对照
- 歌词较长或需要跟唱：用逐行对照
- 用户明确要求"段落式"：用整段对照

---

## 3. 表格对照格式

### 使用场景

- 用户要求"表格形式"
- 适合教学/学习材料
- 适合 Excel 复制粘贴

### 格式规范

```markdown
| 行号 | 原文 | 译文 |
|------|------|------|
| 1 | {原文1} | {译文1} |
| 2 | {原文2} | {译文2} |
| ... | ... | ... |
```

### 完整示例

```markdown
| 行号 | 原文 | 译文 |
|------|------|------|
| 1 | Imagine there's no heaven | 试想一下世界上没有天堂 |
| 2 | It's easy if you try | 如果你试着想像，其实并不难 |
| 3 | No hell below us | 我们脚下也没有地狱 |
| 4 | Above us only sky | 头顶上只有一片蓝天 |
```

---

## 4. JSON 结构化格式

### 使用场景

- 用户要求"程序处理"
- 用户要求"结构化数据"
- 适合批量处理或多歌曲汇总

### 格式规范

```json
{
  "title": "...",
  "title_translation": "...",
  "artist": "...",
  "genre": "...",
  "language": "...",
  "year": "...",
  "lines": [
    {
      "line_number": 1,
      "section": "Verse 1",
      "original": "...",
      "translation": "...",
      "notes": "..."
    }
  ],
  "global_notes": [
    "注1：...",
    "注2：..."
  ],
  "metadata": {
    "translator": "song-translation-expert",
    "translated_at": "2026-06-27",
    "source_url": "..."
  }
}
```

### 完整示例

```json
{
  "title": "Imagine",
  "title_translation": "想象",
  "artist": "John Lennon",
  "genre": "Pop/Philosophical",
  "language": "English",
  "year": "1971",
  "lines": [
    {
      "line_number": 1,
      "section": "Verse 1",
      "original": "Imagine there's no heaven",
      "translation": "试想一下世界上没有天堂",
      "notes": null
    },
    {
      "line_number": 2,
      "section": "Verse 1",
      "original": "It's easy if you try",
      "translation": "如果你试着想像，其实并不难",
      "notes": null
    }
  ],
  "global_notes": [
    "注1：Imagine 是 John Lennon 1971 年发行的标志性和平主义歌曲..."
  ],
  "metadata": {
    "translator": "song-translation-expert",
    "translated_at": "2026-06-27",
    "source_url": null
  }
}
```

---

## 5. Word 文档输出

### 使用场景

- 用户要求"Word 文档"、".docx"
- 用户要求"下载翻译"
- 适合打印、收藏、编辑

### 生成方式

调用 `docx skill`，按以下结构生成：

1. **封面页**：曲名 + 艺人 + 译者 + 日期
2. **歌曲信息表**：曲名、艺人、流派、语种、年份、来源
3. **歌词正文**：每段一个标题（如"Verse 1"、"Chorus"），段内逐行对照
4. **译注**：单独章节
5. **创作背景**：可选章节

### 排版规范

- 字体：正文用宋体/Noto Serif SC，标题用黑体/Noto Sans SC
- 字号：正文 11pt，标题 14-16pt
- 行距：1.5 倍
- 原文：黑色
- 译文：深蓝色（区分）
- 注释：灰色小字

### 示例脚本

```python
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

def generate_lyrics_docx(song_data, output_path):
    doc = Document()
    
    # 封面
    title = doc.add_heading(song_data['title'], level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    artist = doc.add_paragraph()
    artist.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = artist.add_run(f"演唱：{song_data['artist']}")
    run.font.size = Pt(14)
    
    # 信息表
    doc.add_heading('歌曲信息', level=1)
    info_table = doc.add_table(rows=5, cols=2)
    info_data = [
        ('曲名', song_data['title']),
        ('艺人', song_data['artist']),
        ('流派', song_data['genre']),
        ('语种', song_data['language']),
        ('年份', song_data['year']),
    ]
    for i, (k, v) in enumerate(info_data):
        info_table.cell(i, 0).text = k
        info_table.cell(i, 1).text = v
    
    # 歌词正文
    doc.add_page_break()
    doc.add_heading('歌词对照', level=1)
    
    for line_pair in song_data['lines']:
        # 原文
        p_orig = doc.add_paragraph()
        run_orig = p_orig.add_run(line_pair['original'])
        run_orig.font.size = Pt(12)
        run_orig.font.color.rgb = RGBColor(0, 0, 0)
        
        # 译文
        p_trans = doc.add_paragraph()
        run_trans = p_trans.add_run(line_pair['translation'])
        run_trans.font.size = Pt(11)
        run_trans.font.color.rgb = RGBColor(0x1F, 0x49, 0xC4)
        
        # 空行
        doc.add_paragraph()
    
    # 译注
    if song_data.get('global_notes'):
        doc.add_page_break()
        doc.add_heading('译注', level=1)
        for note in song_data['global_notes']:
            p = doc.add_paragraph()
            run = p.add_run(note)
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    
    doc.save(output_path)
```

---

## 6. Excel 表格输出

### 使用场景

- 用户要求"Excel 表格"
- 用户要求"批量歌曲汇总"
- 适合数据管理、筛选、排序

### 生成方式

调用 `xlsx skill`，生成多 sheet 工作簿：

1. **歌曲总览 sheet**：所有歌曲的元信息
2. **逐行对照 sheet**：所有歌曲的逐行对照（含歌曲分隔行）
3. **统计 sheet**：按语种、流派统计

### 表头规范

**歌曲总览 sheet**：

| # | 曲名 | 中文译名 | 艺人 | 流派 | 语种 | 年份 | 原词行数 | 译文行数 | 来源URL |

**逐行对照 sheet**：

| # | 曲名 | 艺人 | 语种 | 段落 | 行号 | 原文 | 译文 |

---

## 7. PDF 文档输出

### 使用场景

- 用户要求"PDF"
- 用户要求"精美排版"
- 适合打印收藏、歌词本

### 生成方式

调用 `pdf skill`，按"Report"线路生成：

1. **封面**：曲名 + 艺人 + 装饰
2. **歌曲信息**：表格展示元信息
3. **歌词正文**：双栏排版（原文左、译文右）
4. **译注**：脚注或章后注
5. **创作背景**：可选

### 排版规范

- 字体：Noto Serif SC（正文）+ Noto Sans SC（标题）
- 双栏：左栏原文，右栏译文，行对齐
- 配色：原文黑色，译文深蓝
- 装饰：每首歌曲间加分隔线

---

## 8. LRC 文件格式

### 使用场景

- 用户要求"LRC"、"歌词文件"
- 用户要求"配合音乐播放"
- 适合音乐播放器使用

### 格式规范

```
[ti:曲名]
[ar:艺人]
[al:专辑]
[by:译者]
[offset:0]

[00:01.23]原文行
[00:01.23]译文行
[00:05.67]原文行
[00:05.67]译文行
```

### 示例

```
[ti:Imagine]
[ar:John Lennon]
[al:Imagine]
[by:song-translation-expert]
[offset:0]

[00:00.00]Imagine there's no heaven
[00:00.00]试想一下世界上没有天堂
[00:04.50]It's easy if you try
[00:04.50]如果你试着想像，其实并不难
```

### 生成注意事项

- LRC 需要时间戳，如果用户没提供音频，无法自动生成时间戳
- 可生成"无时间戳 LRC"作为歌词文件骨架
- 用户后续可手动添加时间戳

---

## 格式选择决策树

```
用户需求？
├── 仅聊天查看 → Markdown 逐行对照（默认）
├── 程序处理 → JSON
├── 学习教学 → 表格对照
├── 打印收藏 → Word 或 PDF
├── 批量管理 → Excel
├── 音乐播放 → LRC
└── 段落式发布 → 整段对照
```

## 文件保存路径

所有生成的文件必须保存到：

```
/home/z/my-project/download/
```

可创建子目录如 `lyrics_collection/`、`lyrics_translation/` 等组织文件。

文件命名规范：

```
{artist}_{title}_{format}.{ext}
例如：
- john_lennon_imagine.md
- adele_someone_like_you.docx
- blackpink_ddu-du_ddu-du.pdf
```

文件名规范：

- 全小写
- 空格用下划线
- 特殊字符删除
- 长度控制在 50 字符内

---

## 总结

输出格式的选择应基于用户的具体使用场景：

- **快速查看**：Markdown 逐行对照
- **学习研究**：表格对照 + 译注
- **打印收藏**：Word 或 PDF
- **数据管理**：Excel 或 JSON
- **音乐播放**：LRC

不要默认所有用户都需要同一种格式。当用户没明确要求时，用 Markdown 逐行对照作为默认；但完成后主动询问是否需要其他格式的文件输出。
