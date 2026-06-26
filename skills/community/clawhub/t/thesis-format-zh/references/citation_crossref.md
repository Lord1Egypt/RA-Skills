# 参考文献交叉引用体系

## 目标

正文中的 `[1]`、`[2]`、`[3]` 必须是 Word `REF` 域，引用参考文献条目的书签编号；参考文献条目原文一字不改。

## 执行顺序

1. 提取模板与目标文档格式，确认正文引用是否上标。
2. 整理参考文献原始条目，记录原始序号与原文。
3. 按正文语义确定插入计划：一个插入位置只放一个参考文献，一个参考文献默认只插一次。
4. 若学校/用户要求按正文首次出现编号，先按插入计划重排参考文献条目，但不改条目文字。
5. 给每条参考文献条目加隐藏书签，如 `_RefThesisRef001`。
6. 在正文相关段落最后标点前插入 `REF _RefThesisRef001 \r \h` 域，显示为 `[1]`。
7. 检查参考文献自动编号格式：如果 `numbering.xml` 的编号本身是 `[%1]`，方括号由 `REF \r` 结果自带，正文外层不要再手打括号。
8. 根据模板字段 `superscript` 决定域结果是否上标。
9. 设置 `updateFields=true`，交付前用 Word 更新域并复核。

## 计划文件

```json
{
  "options": {
    "reference_title": "参考文献",
    "superscript": false,
    "bracket_mode": "auto",
    "placement": "before_final_period",
    "order": "first_appearance",
    "max_per_paragraph": 1,
    "each_reference_once": true,
    "preserve_reference_text": true,
    "allow_reorder_reference_list": true
  },
  "citations": [
    {
      "source_index": 2,
      "paragraph_prefix": "传统西方艺术哲学发展进程中"
    }
  ]
}
```

## 校验标准

- `citations` 顺序就是正文首次出现顺序。
- `source_index` 指向原始参考文献编号，不能重复，除非用户明确允许重复引用。
- `paragraph_prefix` 必须唯一定位到正文段落。
- 插入前先检查段落末尾有句号、问号或感叹号，引用放在该标点前。
- 插入后参考文献条目文本集合必须与插入前完全一致。
- 模板或用户说不上标时，域结果不能带 `w:vertAlign w:val="superscript"`。
- `bracket_mode=auto` 时必须读取 `numbering.xml`：自动编号已有 `[%1]` 就使用域内编号标签，防止更新域后出现 `[[1]]`。

## 工具

```bash
python3 ~/.openclaw/workspace/thesis-auto-review/citation_crossref.py input.docx \
  --plan citation-plan.json -o output.docx
```

不要用 `citation_superscript.py` 代替本工具；它只改变已有普通文本的上标格式，不会创建 Word 交叉引用域。
