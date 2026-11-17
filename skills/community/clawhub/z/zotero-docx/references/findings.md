# 事实依据

所有结论都来自实测或源码，标注了来源。写代码前先读这里，别凭印象。

## Zotero 在 docx 里的两种存储形态

**Field 模式（默认，推荐）** —— OOXML complex field：

```
fldChar(begin) → instrText(" ADDIN ZOTERO_ITEM CSL_CITATION {…JSON…}") → fldChar(separate) → 显示文本 → fldChar(end)
```

也可能是 `w:fldSimple`（一个元素带 `w:instr` 属性，子元素是显示文本的 run）。**两种都要保护**，实测样本里只有前者，但后者是合法 OOXML 写法。

**Bookmark 模式（跨 Word/LibreOffice 协作时用）** —— 引用不在域里，而是：
- 书签名以 `ZOTERO_` 或 `CSL_` 开头
- 真正的域代码存在**同名的自定义文档属性**里

来源：`zotero/zotero-word-for-windows-integration` 的 `build/zoteroWinWordIntegration/field.cpp` 第 34 行：

```cpp
static wchar_t* FIELD_PREFIXES[]    = {L" ADDIN ZOTERO_", L" CSL_", NULL};
static wchar_t* BOOKMARK_PREFIXES[] = {L"ZOTERO_", L"CSL_", NULL};
```

第 138-155 行的逻辑是：先用 BOOKMARK_PREFIXES 匹配书签名，命中后再 `getProperty(doc, bookmarkName, ...)` 从自定义属性里取域代码。

Zotero 官方说明 Bookmark 模式「不支持脚注样式，偶尔会导致引用损坏，编辑多了容易断」，只在必须跨字处理器协作时用。

**只扫 field 会把 Bookmark 模式文档判成「零引用=安全」，然后放手改坏。必须探测并拒绝。**

## 样式偏好

存在 `docProps/custom.xml` 的自定义属性 `ZOTERO_PREF_1`、`ZOTERO_PREF_2`…，Word 单属性上限 255 字符，所以按 255 切片。读要按序号拼、写要重新切并重排 pid。

拼起来是一段 XML：

```xml
<data data-version="3" zotero-version="…"><session id="…"/>
<style id="http://www.zotero.org/styles/nature" hasBibliography="1" bibliographyStyleHasBeenSet="1"/>
<prefs><pref name="fieldType" value="Field"/>…</prefs></data>
```

`fieldType` 的值就是存储模式（`Field` / `Bookmark`），这是最可靠的探测点。

## 实测数据（样本：一篇真实论文，37 个引用域、1 个参考文献表、带修订标记）

| 观察项 | 数值 |
|---|---|
| `w:fldSimple` / `w:fldChar` | 0 / 114 |
| `paragraph.text = "…"` 改一段 | 引用域 37→**33**，fldChar 114→**102** |
| XML 里 `w:r` 总数 vs `paragraph.runs` 返回 | 1461 vs **1385**（差 76，其中 3 个是 fldChar） |
| `ZOTERO_ITEM` 在 `w:delInstrText` 里的 | 37 个中有 **1** 个 |
| 段落被拆成多个 `w:t` | 245 段中 **155** 段，最碎 47 片 |
| 逐 `w:t` 替换的漏检率（5 个探针词） | 130 次中漏 2 次，**2%** |

碎片化实例，`osteoarthritis` 被拆开：

```
'Keywords: ', 'O', 'steoarthritis; ', 'S', 'ynovial ', 'fluid; '
```

## 已复现的代码缺陷（旧版 zotero_docx.py）

**正则删属性会误删相邻属性**。`re.sub(r'<property[^>]*name="ZOTERO_PREF_\d+".*?</property>', ...)` 遇到合法的 `</property >`（带空格）时，非贪婪匹配跨过它一路吃到下一个 `</property>`：

```
删除前含 Company 属性: True
删除后含 Company 属性: False
```

**字符串插值改样式会损坏数据**。`new_style` 含双引号时写成 `style id="a"b"`，读回只剩 `a`。

**strict OOXML 命名空间下代码静默失效**。硬编码 `…/2006/main`，遇到 `http://purl.oclc.org/ooxml/wordprocessingml/main` 的文档：实际 5 个 run，`iter()` 出 0 个，改写什么都不做，审计报 0 个域看起来像「安全」。

**`w:fldSimple` 不被保护**。构造测试后保护集合为空，域内显示文本会被当正文改写。

**`audit()` 从未被 `process()` 调用**。安全校验只存在于测试脚本里，模块本身零检查。

## 命名空间

| 族 | URI |
|---|---|
| transitional（常见） | `http://schemas.openxmlformats.org/wordprocessingml/2006/main` |
| strict | `http://purl.oclc.org/ooxml/wordprocessingml/main` |

不认识的命名空间必须拒绝，不能当成「没有内容」。

---

# 打磨过程中反复出现的几类错误

八轮下来，问题不是随机分布的，集中在几个固定模式上。以后改这个模块，
先对照这几条自查。

## 一、拿一个样本的成功当普遍成立

真实论文那篇是标准 complex field、transitional 命名空间、图片名不带空格。
它一个坑都不触发。每次「拿它测通过了」都不构成任何保证。

踩过的：`fldSimple` 不受保护、strict 命名空间静默失效、关系 Target 带
`%20` 被误判成断链——三次都是这篇论文测不出来的。

## 二、测试绿不代表被测过

- `audit()` 写了但 `process()` 从没调用，安全校验只存在于测试脚本里
- `_check_relationships()` 加了之后，测试文件里 `.rels` 出现 0 次，这段代码从没执行过
- altChunk 测试用的样本文件被我命名成 `word/altChunk1.xhtml`，恰好命中我那个查文件名的错误实现，等于自己出题自己答
- 锚点搬移的测试用 `dry_run=True`，根本没走写回逻辑，掩盖了真正的 bug

改完一段逻辑就要问：有没有测试真的执行到这一行。

## 三、修 bug 引入 bug

- 修「含锚点的 run 被静默跳过」→ 改成整个 run 单独成段 → 制造了「锚点被搬到末尾」
- 修「锚点被搬移」→ 改成每个 `w:t` 各自成段 → 制造了「`Osteo`/`arthritis` 拼不回去」
- 加关系校验 → 校验本身把带 `%20` 的正常文件误判成损坏

新加的保护也是代码，也会有 bug，也要构造反例测。

## 四、白名单式判断必然漏

维护「哪些元素算锚点」的列表，漏一个就错一个。`w:lastRenderedPageBreak`
不在列表里时，两侧文字被合并、标记被搬到末尾。

改成反向判断：`w:rPr` 和 `w:t` 之外的任何直接子元素都算位置边界。穷尽，不用维护。

## 五、文档和实现悄悄分叉

SKILL.md 一度写着「修订标记内的文字不会被改写」，而代码只是把 `w:ins`
当成不合并的边界，里面的文字照改。文档撒谎比代码有 bug 更危险，因为
用户会照文档做决定。

改行为就要同步改文档，两边对不上时先查哪个是对的。

## 六、同一个词表示两个意思

`precheck` 返回的 `fields` 只数 Zotero 引用（37），`process` 返回的
`fields` 数所有 Word 域含参考文献表（38）。数字都对，但用户看到
37 变 38 会以为改坏了。已拆成 `citations` / `bibliographies` / `all_fields`。

## 七、lxml 的坑

`id()` 不能用来做节点身份判断。lxml 的 Python 代理对象按需生成，
同一个 XML 节点两次访问 `id()` 可能不同。要判断归属就沿 `getparent()`
往上走，要断言就数文本出现次数。
