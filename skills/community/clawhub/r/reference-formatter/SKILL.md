---
name: reference-formatter
description: 将用户提供的参考文献列表按指定格式整理为可复制的文档。Use when: (1) 用户粘贴了原始参考文献需要格式化, (2) 写论文时需要统一文献格式, (3) 从网站/软件导出的文献格式混乱需要整理, (4) 需要在不同引用格式之间转换(如APA/GB/T/MLA), (5) 用户需要生成格式规范的文献列表文件。
version: 1.3.0
changelog: "v1.3.0: 格式化前输出变更报告给用户确认，确认后才生成文档。v1.2.0: 新增自定义格式上传支持。v1.1.0: 中英文分节排序、标题不加粗、每条文献独立分段、默认去除DOI。v1.0.1: 默认输出 .docx。v1.0.0: 初始版本。"
metadata:
  openclaw:
    emoji: "📚"
    category: "academic"
---

# Reference Formatter 📚

把混乱的参考文献列表整理成专业格式，输出可直接使用的文档。

## Trigger

['整理参考文献', '格式化文献', '文献格式', '参考文献排版', '引用格式', 'APA格式', 'GB/T格式', 'MLA格式', '文献列表整理', 'format references', 'citation format']

## Workflow

### 第一步：接收文献列表

用户提供原始参考文献列表。接受任意格式的输入：
- 直接粘贴的文本
- 从网站/知网/Google Scholar/PubMed 等导出的混乱格式
- 多条参考文献混合

如果用户未提供文献，先追问：「请把需要整理的参考文献粘贴过来，直接 Ctrl+V 就行」

### 第二步：确认目标格式

确认目标格式。优先级如下：

1. **用户上传了自定义格式规范**（如学院格式说明、期刊作者须知）→ 按用户提供的格式输出
2. **用户口头指定了标准格式** → 按该格式输出
3. **未指定** → 默认 APA 第7版标准

**内置支持的格式：**
| 序号 | 格式 | 适用场景 |
|------|------|----------|
| 1 | APA 第7版 | **默认格式**。Publication Manual (7th ed.) 标准版 |
| 2 | APA 第6版 | 旧版学术期刊投稿 |
| 3 | GB/T 7714-2015 | 中国学位论文、国内期刊投稿 |
| 4 | MLA 第9版 | 人文学科、语言文学 |
| 5 | Chicago (Author-Date) | 历史学、部分社会科学 |
| 6 | 自定义 | 用户上传自己的格式规范文件 |

追问格式：「用什么格式？不说就默认 APA 第7版。如果你有自己的格式规范（学院发的、期刊的），直接贴过来就行」

### 第三步：解析与识别

对每条文献自动识别类型：

1. 扫描 DOI、URL、卷期号、出版社等特征
2. 按 `reference/formats.md` 中的检测规则分类：
   - 期刊文章 → 有 DOI 或卷期号
   - 图书 → 有出版社、无卷期
   - 书籍章节 → 包含 "In"、编者、"pp."
   - 网页 → 有 URL、无学术元数据
   - 学位论文 → 含"dissertation"/"thesis"/[D]
   - 会议论文 → 含 conference/symposium/proceedings
3. 无法识别的条目标记为 `⚠️ 需人工确认`，并保留原文

### 第四步：格式化与变更报告

按目标格式规范逐条处理：

- **作者名**：正确处理缩写（APA）、全大写（GB/T 英文）或全名（MLA）
- **标点**：中文文献用中文标点，英文文献用英文标点
- **斜体**：书名、刊名、卷号用斜体（Markdown `*` 标记）
- **DOI/URL**：默认去除 DOI（除非用户要求保留）
- **排序**：中文文献按拼音首字母排序，英文文献按姓氏字母排序，中英文分开为独立小节
- **分段**：每条文献独立成段，段落间有间距
- **标题不加粗**：参考文献标题使用普通字重
- **悬挂缩进**：在输出文档中自动应用

格式化完毕后，**直接生成文档并附带变更报告**，无需用户确认。报告格式如下：

```
📋 格式变更报告（36条文献）

处理摘要：
├─ 期刊文章格式化：16条
├─ 书籍/章节格式化：3条
├─ 学位论文格式化：7条
├─ 会议论文格式化：4条
├─ 其他：6条（含1条⚠️需人工确认）

主要变更：
├─ 作者格式：and→&（3处）、Wang M-W→Wang M.-W.（2处）
├─ 标点符号：～→– 全角→半角（8处）
├─ 页码范围：en dash 统一（5处）
├─ 出版地：删除 New York:、Madison: 等（3处）
├─ 学位论文：调整格式（2处）
├─ DOI：已全部移除
├─ 排序：中文按拼音，英文按姓氏（已分节）

⚠️ 需注意：
└─ Moore (2008) — 缺少学位授予单位信息

文件已生成：references.docx / references.txt
```

格式细节参考：`reference/formats.md`

### 第五步：输出文档

**默认输出（用户未指定文件名和位置时）：**

- 格式：`.docx`（Word 文档）
- 位置：workspace 根目录
- 文件名：`references.docx`

**如果用户指定了文件名或位置，按用户要求执行。**

如果 pandoc 或 Word COM 不可用，降级为 `.txt` 纯文本并告知用户。

**输出位置：** 默认写到 workspace 根目录

**输出示例：**

```
# References (APA 7th Edition)

Smith, J. A., & Jones, B. C. (2023). Understanding cognitive biases in decision-making. *Journal of Behavioral Science*, *45*(2), 112-130. https://doi.org/10.1234/jbs.2023.045

Wang, X., & Li, Y. (2022). 机器学习在自然语言处理中的应用 [Application of machine learning in NLP]. *计算机学报*, *44*(3), 201-215.

U.S. Department of Health and Human Services. (2021, March 15). *Mental health and wellness*. https://www.hhs.gov/mental-health
```

### 第六步：质量检查

输出后自检：
- [ ] 所有条目都成功识别了类型？
- [ ] 有无 ⚠️ 标记的条目？如有，提醒用户核对
- [ ] 标点符号符合目标格式规范？
- [ ] 排序正确？
- [ ] DOI/URL 可点击？

### 失败兜底

- **无法识别类型** → 保留原文格式，标记 ⚠️，不强行猜测
- **作者信息缺失** → 不编造，留空或标 `[Author unknown]`
- **pandoc 未安装** → 仅输出 .md 文件，告知用户：「如需 .docx，可以安装 pandoc 后让我再转一次」

## Examples

### 示例 1：混格式输入 → APA

**输入：**
```
[1] Smith, John, and Jones, Betty. Understanding cognitive biases in decision-making. Journal of Behavioral Science, vol. 45, no. 2, 2023, pp. 112-130.
[2] Wang Xiao, Li Yu. Research on machine learning in NLP. Chinese Journal of Computers, 44(3):201-215, 2022.
```

**输出：**
```
Smith, J., & Jones, B. (2023). Understanding cognitive biases in decision-making. *Journal of Behavioral Science*, *45*(2), 112-130.

Wang, X., & Li, Y. (2022). Research on machine learning in NLP. *Chinese Journal of Computers*, *44*(3), 201-215.
```

### 示例 2：GB/T 输出

**要求：**「转成 GB/T 格式」
**输出：**
```
[1] SMITH J, JONES B. Understanding cognitive biases in decision-making[J]. Journal of Behavioral Science, 2023, 45(2): 112-130.
[2] 王小明, 李雨. 机器学习在自然语言处理中的应用研究[J]. 计算机学报, 2022, 44(3): 201-215.
```

## Tool Usage

- **文件读写**：`read` / `write` — 读入原始文献，写出格式化文件
- **格式参考**：`read reference/formats.md` — 查阅各格式的详细规范
- **文档转换**：`pandoc references_formatted.md -o references_formatted.docx` — Markdown → Word
- **联网查询**（可选）：如果参考文献信息不全（缺 DOI 等），可用 `web_search` 补全

## Additional Information

### 注意事项

1. **不编造信息** — 缺作者或缺日期就留白，不要编
2. **保留原文信息** — 即使识别出的类型不对，原文内容一字不动
3. **中文作者处理** — 中文名字不需要缩写，保留全名，按拼音排序
4. **去敏提醒** — 如果文献信息包含个人标注、内部链接等，保留但不额外处理

### 后续可扩展

- 支持更多格式：Harvard、Vancouver、IEEE
- 批量导入：从 BibTeX/EndNote/RefMan 文件直接导入
- 在文内插入引用标记 [1] 并自动编号
