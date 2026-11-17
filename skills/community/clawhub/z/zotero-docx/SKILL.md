---
name: zotero-docx
description: 改写含 Zotero 引用的 .docx 正文而不破坏引用域，或程序化更换参考文献样式。用于论文润色、降 AI 味、批量改写等场景。改完 Zotero 仍能刷新、换样式、重生成参考文献表。
---

# 改带 Zotero 引用的 docx

批量改论文正文，改完 Zotero 引用还是活的。

## 什么时候用

- 要用脚本或模型改写 .docx 正文，而文档里有 Zotero 插入的引用
- 要程序化把参考文献样式换成另一种（比如 nature 换成国标 GB/T 7714）
- 用户提到「论文降 AI 率」「润色」「批量改写」且文件是带引用的 docx

## 先读这个

**默认行为是不确定就拒绝。** 体检不过一律不产出文件。这类故障不报错，改坏之后
用户往往到投稿前要换引用格式时才发现，那时已经无法恢复，所以宁可不产出。

被拒绝时把 `Refused` 的原文转达给用户，里面写了为什么不能处理、以及怎么补救。
不要绕过体检，不要「先试试看」。

## 用法

```python
import sys; sys.path.insert(0, '<skill 目录>')
from zotero_docx import process, precheck, Refused

# 一 先体检，看清楚再动
try:
    rep = precheck('论文.docx')
    print(rep['fields'], '个引用域', rep['bibl'], '个参考文献表')
    print('当前样式', rep['style'], '带修订标记' if rep['has_revisions'] else '')
except Refused as e:
    print('不能处理：', e)

# 二 干跑，只看会改什么，不写文件
r = process('论文.docx', '输出.docx', fn=my_rewriter, dry_run=True)
for part, old, new in r['changes'][:10]:
    print(repr(old), '->', repr(new))

# 三 真改
r = process('论文.docx', '输出.docx', fn=my_rewriter)
print(r['citations'], '个引用', r['bibliographies'], '个文献表',
      r['all_fields'], '个域（含非 Zotero 的）')

# 带修订标记的文档默认拒绝，先在 Word 里接受或拒绝所有修订
r = process('论文.docx', '输出.docx', fn=my_rewriter, allow_revisions=True)

# 大面积改写（降 AI 味这类）会撞上覆盖率上限，确认是有意的就开这个
r = process('论文.docx', '输出.docx', fn=my_rewriter, allow_heavy_rewrite=True)

# 目标文件已存在时默认拒绝，要覆盖得显式说
r = process('论文.docx', '输出.docx', fn=my_rewriter, overwrite=True)

# 四 换样式（改完要用户在 Word 里点 Zotero 刷新才会重排）
process('论文.docx', '输出.docx',
        new_style='http://www.zotero.org/styles/china-national-standard-gb-t-7714-2015-numeric')
```

`fn` 收到的是**跨 run 拼好的完整文本**，不是碎片。返回改写后的文本，返回 `None` 或原样表示不改。

## 改写函数怎么写

```python
def my_rewriter(text):
    if len(text) < 4:          # 太短的片段多半是标点或残片，别动
        return None
    return text.replace('旧说法', '新说法')
```

要交给模型改写时，一段一段送，不要把整篇拼起来送。因为 `fn` 拿到的每一段
对应文档里一处连续同格式文本，一一对应才能安全写回。

## 它挡掉了什么

| 情况 | 处理 |
|---|---|
| Zotero 用 Bookmark 模式存引用 | 拒绝。只扫域会报「0 个引用」然后放手改坏 |
| 书签名带 `ZOTERO_` / `CSL_` 前缀 | 拒绝，同上 |
| strict OOXML 格式 | 拒绝。只在 transitional 上验证过 |
| 域的 begin/separate/end 不配对 | 拒绝，文件已损坏 |
| 未知的 `fldCharType` | 拒绝，伪造的标记能藏住真实的域边界 |
| 文档带数字签名 | 拒绝，重写包会让签名失效且无法重新签名 |
| 一个引用域都没有 | 拒绝，避免把「扫不到」当成「很安全」 |
| 含 altChunk | 拒绝，扫描范围覆盖不到 |
| 源文件和目标文件同一个 | 拒绝原地覆盖 |
| 样式 id 含引号等非法字符 | 拒绝，会损坏偏好数据 |
| 目标文件已存在 | 拒绝，除非传 `overwrite=True` |
| 改动字符数超过正文一半 | 拒绝，除非传 `allow_heavy_rewrite=True` |
| 单个片段改写后超过原文 3 倍 | 拒绝。逐片段判断，不汇总，避免一段膨胀被另一段抵消 |
| 文档带未处理的修订标记 | 拒绝，除非传 `allow_revisions=True` |
| 域从 begin 直接到 end（缺 separate） | 拒绝，域结构损坏 |
| 改完域清单对不上 | 丢弃产出，不写文件 |

写文件走临时文件加校验：zip 完整性、每个 XML 能否解析、域清单逐条比对，全过了才原子替换。

域清单对每个域记四样再算 SHA-256：完整指令代码、`separate` 之后的显示文本、
有没有 `separate` 标记、外层的修订包装链（`w:ins` / `w:del` / `w:moveFrom` / `w:moveTo`）。
按 (part, 域类型, 哈希) 有序列表比对。

包装链是必须记的：两个域可以内容逐字节相同，但一个裸着、一个被 `w:moveFrom` 包着，
接受修订后前者留下、后者连引用一起消失。只比对域内部查不出这种调包。

能查出：域代码被篡改、显示文本被改、`separate` 被去掉、域数量变化、顺序调换、
跨 part 移动、域被塞进或移出修订包装。
查不出：同一 part 里两个四项完全相同的域互换位置（此时互换本身也没有意义）。

## 硬边界

下面这些结构会把文本分段，不会跨过它们合并。因为文字被搬走之后，
这些标记会框住空区间，导致书签失效、批注错位、交叉引用指向空处。

- **run 之间的标记**：书签、批注范围、拼写检查标记、编辑权限范围、移动范围
- **包住 run 的结构**：超链接、修订标记（`w:ins` / `w:del`）、内容控件、smartTag、移动块
- **run 内的非文本元素**：`w:rPr` 和 `w:t` 之外的任何直接子元素都算，
  包括脚注引用、图片、符号、tab、换行、软连字符、分页标记等

最后这条写成排除法，不维护「哪些算锚点」的白名单。白名单要把所有情况列对，
没列进去的会被跨过去合并：实测 `w:lastRenderedPageBreak` 不在白名单时，
两侧文字被合并、标记搬到 run 末尾。

含非文本元素的 run 不跟邻居合并，内部再按这些元素的位置切分：夹在两段文字
中间的才切开，只在首尾的不切（否则 Word 拆出的 `Osteo`/`arthritis` 就拼不回去了）。

## 已知边界

- 只处理 `word/` 下的 document、footnotes、endnotes、comments、header、footer
- 图表里的文字（DrawingML）不归它管
- **带修订标记的文档默认拒绝改写**。`w:ins` / `w:del` 只是不跟邻居合并，
  里面的文字仍会被改，但不会生成新的修订记录，等于无痕改掉别人的修改。
  先在 Word 里接受或拒绝所有修订，或者明确知道后果时传 `allow_revisions=True`
- 换样式只改文件里记的样式 id，实际重排要用户在 Word 里点 Zotero 刷新
- 缺 `docProps/custom.xml` 时：只改正文没问题，换样式会报错

## 验证

```
python3 test_zotero_docx.py                    # 67 项自测（无真实样本时 64 项）
python3 verify_external.py 输出.docx --compare 原始.docx      # 外部交叉验证
```

自测多数是构造出来的坏文件（Bookmark 模式、strict 格式、域缺 end、域缺 separate、
真实 altChunk、书签跨界、批注范围、含锚点的 run 会不会搬移锚点、文本框嵌套段落
会不会被改两次、单片段膨胀会不会被别的片段抵消）。改代码后必须重跑。

数量会随环境浮动：最后那组真实论文回归需要本地有样本文件，缺了就少 3 项（实测 64）。

外部验证用 LibreOffice 和 python-docx 两个独立实现读产出文件，自己的测试只能
证明自己的假设成立，证明不了别的程序认。带 `--compare` 时会把两边都转成 PDF
比页数和体积，实测一篇论文：

```
通过 页数对照 原始 30 页 / 改写后 30 页
参考 体积 181406 -> 181440 字节（差 34）
```

**LibreOffice 转换失败先查组件是否装全。** 症状是转任何文件都报
`Error: source file could not be loaded`，连纯文本都转不了 —— 这不是版本问题，
是缺 `libreoffice-writer`。有些环境只装了 core、draw、impress，没有 Writer 组件就
打不开 txt 和 docx。`apt install libreoffice-writer` 之后即可（本机 7.3.7.2 已实测修复）。

```bash
dpkg -l | grep -c libreoffice-writer     # 0 就是没装
```

带 `--compare` 传原始文件做对照，能区分是环境问题还是产出有问题。

事实依据、实测数据、源码出处见 `references/findings.md`。
