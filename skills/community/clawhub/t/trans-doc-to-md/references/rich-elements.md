# 富元素识别 + 可移植表达

PDF 解析器会把这些富元素**拍平成一堆零散段落**，丢失结构与视觉强调。本 skill 负责**识别 + 用可移植标注重建**；归档 skill 再把标注映射成各平台专有块。

## 标注契约（与归档 skill 的接口）

| 富元素 | 本 skill 输出（可移植 markdown） | 归档 skill 渲染为 |
|---|---|---|
| 统计高亮框 | `> [!stat] **<数字>**` + EN + CN | callout 块（📊） |
| 定义/术语卡片 | `> [!definition] **<术语>**` + EN + CN | callout 块（📖） |
| 多列信息图 | 1 行 N 列 HTML `<table>` | 原生表格块 |
| 样式化对照表 | `![原图](images/..)` + markdown/HTML 表 | 图片 + 原生表格块 |

> 选 `> [!type]` 这种 Obsidian 风格 callout 语法：标准 markdown 渲染器把它当普通 blockquote（不丢内容），而支持的渲染器/归档 skill 能识别成 callout——可移植且语义不丢。

## 一、统计高亮框（Stat Card）

**识别信号**：左侧大数字 + 右侧说明句；解析后常变成「数字一行 + 英文一行 + 重复数字 + 中文一行」3–4 个孤立段落；同一数字重复 2 次（EN/CN 各一行）是典型；短行以 `%`/`hrs`/`x`/`倍` 开头或整行 ≤40 字符且紧跟 ≥20 字符说明句。

**重建**（数字只出现一次）：

```markdown
> [!stat] **6.4 hrs/week / 6.4 小时/周**
> Workers spend this much time per week on AI babysitting.
> 员工每周花这么多时间照看 AI。
```

## 二、定义/术语卡片

**识别信号**：`DEFINITION` + 术语 + 释义；术语行（如 `Botsitting (n.)`）常被误标成 `##` 标题（污染目录）。

**重建**：

```markdown
> [!definition] **Botsitting (n.) / AI 看护**
> The hidden human labor of making AI output usable.
> 让 AI 产出可用所需的隐性人力劳动。
```

## 三、多列信息图（并排 N 列卡片）

**识别信号**：并排 N 列卡片式信息图（如「Botshitting 三种形式」各列含 Sounds like / What workers do + 百分比）；解析后变成纵向堆叠 + 每列被设 `###` 标题 + 标签/引用拆成多段。

**重建为 1 行 N 列 HTML `<table>`**（`<td>` 内 `<strong>` 加粗列标题/标签/百分比，**不设 `#` 标题**；中英同格用 `<br>`）：

```html
<table>
<tr>
<td><strong>Offloading understanding / 卸载理解</strong><br><strong>41%</strong> deliver work they can't explain.<br>41% 交付无法解释的工作。</td>
<td><strong>Offloading judgment / 卸载判断</strong><br><strong>38%</strong> use unapproved tools.<br>38% 使用未批准工具。</td>
<td><strong>Offloading responsibility / 卸载责任</strong><br><strong>28%</strong> blamed AI for their own mistakes.<br>28% 把自己的错归咎于 AI。</td>
</tr>
</table>
```

复杂多列优先用表格（比多栏布局更稳，markdown/html 均透传渲染）。

## 四、样式化对照表 / 卡片表

**识别信号**：成对/多列、带表头或箭头的对照表（如「奖励谬误表 We say we want… / But we actually reward…」），被拍平成几十个零散段落，既丢表格又没原图。

**重建（两件事都做）**：
1. 裁整张表格图插到标题下方：`![caption / 中文图注](images/table_pNN.png)`（满足"展示原图"）。
2. 内容写成 markdown 表（中英同格，英文 `**加粗**` + 中文常规）：

```markdown
| We say we want 我们声称想要 | But we actually reward 但实际奖励 |
| --- | --- |
| **Thoughtful analysis** 深思熟虑的分析 | **Speed** 速度 |
```

> 表格翻译两个通病：①把中文整行/整表另起（英文行下再来中文行）→ 必须**中英同格**；②原文合并单元格被拍平 → 用 HTML `rowspan`/`colspan` 还原。数据/百分比格不必翻译。

## 五、脚注上标残留 `$^{N}$`

**识别信号**：PDF 解析把脚注/引用上标输出成 `$^{19}$`、`$_{2}$` 这类 LaTeX 语法，普通渲染器显示成乱码。

**清理**：全文正则 `\s*\$\s*\^\s*\{\s*(\d+)\s*\}\s*\$` → **Unicode 上标**（紧贴前字符）：

```python
import re
SUP = {'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'}
rx = re.compile(r" ?\$\s*\^\s*\{\s*(\d+)\s*\}\s*\$")
text = rx.sub(lambda m: "".join(SUP[d] for d in m.group(1)), text)  # $^{19}$ → ¹⁹
```

交付前必搜 `$^{` / `$_{` 确认归零。

## 六、标题层级与目录

解析器给的 `#` 级别**不可信**（常把章节内图表标题、小节、甚至作者名都标成一级），导致目录膨胀。

- **重排层级**：仅文档标题、正文真正大章节及真实附录/尾注使用 `#`。PDF 解析器常把章节内部跨行、字号较大的长论述标题误标成 H1；只要它位于一个正文大章节之后且未开启新章节，就降为 `##`。章节内主题 `##`；主题下论述标题 `###`；确有进一步父子关系的命名卡片、地区/职能/行业项用 `####`，否则降为加粗正文。不能因原解析级别相同就让父标题与直接子标题同级。
- **降级为加粗正文**：作者名、人物叙事名、纯百分比、重复子标签（如各地区下的 The posture / How AI gets absorbed）一律 `**...**`，不当标题。
- **卡片/分项小标题降一级嵌套**：父标题（含 "by the numbers / comes in N forms / N 类"）下一组并列命名卡片是子项，比父低一级。
- **章节序号 kicker 并入 H1**：`# SECTION 03 · English Title / 中文标题`，删原孤立的 `SECTION 03` 行及重复变体。
- **目录页重建**为「一项一行」清单：源文有真实类别时用 `- **Category / 双语类别**: English Title / 中文标题 · p.NN`；源文无类别时用 `- **English Title / 中文标题** · p.NN`。不得为了视觉对称补造 `Section`、`Appendix`、`Directory` 等标签。类别不得吞并或替代原始标题；从原始目录提取的标题须逐字保留在清洗稿及最终英文侧。

**双语标题切分坑**：判定英文标题名时，中文译文以 `AI`/`UX` 等短词开头会污染「首个中文字符前取英文」的切法；而 `Government / public sector`、`Nonprofit / NGO` 这类名称**内部就含 ` / `**，不能当双语分隔符切断。

## 七、页眉/页脚残留清除

PDF 每页页眉/页脚（章节名、`SECTION 0X`、`p.NN`、重复副标题）会被解析成**散落全文的独立短段落**，同一句重复十几到几十次。
- 统计**逐字重复 ≥3 次的短行**（长度 < ~90、不以正文标点收尾）→ 判定页眉家具，全删。
- `SECTION\s*0?\d`、`第.节`、纯章节标题、`English Title 中文`（标题+中文紧贴的页眉）同样删。
- **别误删正文**：双语正文是"英文长段 + 空行 + 中文长段"，与短重复页眉行截然不同。

## 八、署名引语块

**识别信号**：完整引语（直引号或弯引号起止）后，在相邻数行内出现明确的人名与职位署名；普通正文、无署名句子和仅作术语引用的短语不处理。

**可移植表达**：使用标准 Markdown `>`，不默认使用可能被上传器当字面文本的 `[!quote]`：

```markdown
> “English quotation.”
>
> “中文引语。”
>
> **Name | Role**
>
> **姓名 | 职位**
```

英文、中文和署名必须处于同一个连续引用块；署名可加粗，但引语和署名原文不得改写。
