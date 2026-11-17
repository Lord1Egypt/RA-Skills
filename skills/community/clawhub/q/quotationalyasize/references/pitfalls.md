# 踩坑与修复记录（multi-project-quote-board）

按「症状 → 根因 → 修复」记录，全部为实际发生过的坑。

---

## 坑 1 — 大段 HTML 用 `%` 格式化 → TypeError，产物静默为空

**症状**
```
TypeError: not enough arguments for format string
```
或更隐蔽：脚本「好像跑完了」但 `board.html` 没生成 / 是空的，后续校验脚本报 `FileNotFoundError: board.html`。

**根因**
渲染层把整页 HTML 拼成一个大字符串。CSS 里的 `width:100%`、字体 `font:14px/1.6` 不触发，但任何 `%s` / `%d` / 单独的 `%`（如 `100%`）一旦落在被 `%` 格式化的字符串里，就会与 Python 的 `%` 运算符冲突。

**修复（模板已采用）**
- 标题等动态值用 token 占位：`"<title>@@TITLE@@</title>"` → 最后 `"".join(H).replace("@@TITLE@@", BOARD_TITLE[0])`。
- 新增含 `%` 的文案时，用局部 `+` 拼接或 `.replace()`，**不要**把含 `%` 的整段 HTML 丢进 `%` 格式化。

**判据**：如果生成脚本 exit 0 但产物缺失，先怀疑这一条，而不是文件权限。

---

## 坑 2 — `TERMS` 取值顺序与 `SUPPLIERS` 不一致 → 整列条款静默错位

**症状**：条款对比表里，供应商 A 的材质被显示成供应商 B 的。无任何报错。

**根因**
`TERMS` 每行 `(中, 英, v1, v2, …)`，`v1…vn` 按 `SUPPLIERS` 列表顺序对应。中途插入/删除供应商、或重排 `SUPPLIERS` 而忘了同步 `TERMS`，就整体错位。

**修复**
- 定一条规矩：**`TERMS` 取值顺序 == `SUPPLIERS` 顺序**，写进 SKILL.md §6。
- 交付前逐列肉眼核对一次（尤其列数多时）。可加断言：每行取值个数 == `len(SUPPLIERS)`。

---

## 坑 3 — Excel 图片全部静默跳过（media=0，体积异常小）

**症状**：`gen_excel.py` 显示成功，但 xlsx 里没有图；体积异常小（如 18KB）；解压 `xl/media/` 为空。

**根因**
用了托管的基础解释器 `3.13.12`，**它没有 Pillow**。`openpyxl.drawing.image.Image` 在缺 PIL 时会跳过图片而不抛错。

**修复**
出 Excel（含图）必须用带 Pillow 的 venv 解释器：
```
C:/Users/admin/.workbuddy/binaries/python/envs/default/Scripts/python.exe gen_excel.py
```
（Pillow 10.4.0 + openpyxl 3.1.5）

**验证**：解压 xlsx 数 `xl/media/` 下的文件数，应等于预期图片数。

---

## 坑 4 — 双语不等长（zh span ≠ en span）

**症状**：切到英文后个别句子仍是中文，或反之；或某段两种语言同时显示。

**根因**：新增文案时只加了 `Z(...)` 没加 `E(...)`（或反之）；或直接把中文字符串裸写进 HTML 忘了包 span。

**修复/自检**：
```python
h = open("board.html", encoding="utf-8").read()
print(h.count('<span class="zh">'), h.count('<span class="en">'))   # 必须相等
```
模板示例为 134 = 134。不相等就去找漏的那段。

---

## 坑 5 — KPI 说「A 最低」但第七节推荐 B（口径打架）

**症状**：项目卡 / KPI 卡上的「当前报价最低」显示的是纯最低价那家，但第七节按「满足工期者中最低价」推的是另一家。

**根因**：KPI/chip 走了 `min_pid`（纯最低价），而定标走 `sched_lowest`（工期门槛内最低价）。两个口径。

**修复**：KPI、chip、「最低」标注**统一走 `sched_lowest`**，并显式标注「工期满足+报价最低」。这样全板只有一个「最低」口径。

---

## 坑 6 — 绝对日期排期的供应商被错误顺延

**症状**：某家明确说「X 月 X 日交付」，但看板按「统一起算日 + 天数」平移成了另一个日期。

**根因**：该家用的是绝对日期，不适用「起算日 + 天数」。

**修复**：把它放进 `LEAD_ABS_END[<key>][<pid>] = dt.date(...)`；`lead_result()` 会优先用绝对日期，不平移。

---

## 坑 7 — `RECON` 未通过仍交付

**症状**：`生产 + 运输 + 安装 ≠ Total`（多为报告本身的分项与总额不自洽，或抄录时漏项）。

**纪律**：`RECON` 不是 `ALL OK` 时**先修数字再交付**。若源头报价本身不自洽（例如欧元分项加总与 Total 差 0.x），**按原文保留并在待澄清清单里列 P0**，不得自行改数抹平。
