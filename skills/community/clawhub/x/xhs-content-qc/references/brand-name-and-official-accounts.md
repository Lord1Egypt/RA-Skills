# 品牌名与官方账号规范

质检时品牌**正确/错误写法**以 `assets/` 下词表为准，本文件说明**读取方式**、**@ 官号**及**无法收入词表的细则**。

| 词表文件 | 用途 |
|---|---|
| [../assets/brand-names-correct.txt](../assets/brand-names-correct.txt) | 推荐/可接受的品牌写法：**每行一条**；仅忽略空行 |
| [../assets/brand-names-wrong.txt](../assets/brand-names-wrong.txt) | 错误写法黑名单：**每行一条**；命中即维度1 品牌名 FAIL；仅忽略空行 |

必带话题见 [../assets/required-topics.txt](../assets/required-topics.txt)（规则以 SKILL 维度 1.2 为准）。

## 品牌名检查（与词表配合）

1. **错误词表**：将标题、正文与 `assets/brand-names-wrong.txt` 每一行做**子串匹配**，**不区分大小写**；任一命中 → 品牌名 **FAIL**，列出命中词与上下文。
2. **正确词表**：在无错误命中的前提下，若笔记**明显在推广本品牌**，应至少出现 `assets/brand-names-correct.txt` 中**一条**的规范写法（同样子串、不区分大小写）；若通篇推广品牌却无任何正确词表命中 → 品牌名 **WARNING**（可能用了未收录的变体，建议人工复核）。
3. **本文件补充规则**（机械词表未覆盖时由你语义判断）：
   - **平台限制**：小红书等平台在话题、标题等场景下常无法或不便输入英文中间空格，**「bubbletree」连写与「bubble tree」带空格同等视为正确**；质检时**不得**仅因英文未加空格判 FAIL。双语组合以 `assets/brand-names-correct.txt` 为准（如「bubbletree泡泡树」「bubble tree泡泡树」均可）。
   - 业务若要求**必须写完整双语品牌**而笔记仅写英文或仅写中文，可结合 brief 判 **WARNING** 或 **FAIL**，并在报告中说明依据。

## 官方账号 @ 标准写法

笔记须正确 @ 下列账号**至少其一**（可多 @）：

| 标准写法 | 说明 |
|---|---|
| `@BUBBLE TREE` | 品牌主号 |
| `@BUBBLE TREE达人体验官` | 达人体验官号 |

### @ 匹配规则

- `@` 后账号名须与上表完全一致（含空格）
- 「BUBBLE TREE」中间须有一个空格；缺空格视为错误
- 大小写须与上表一致（全大写）
- 未 @ 任一官方账号视为遗漏

