---
name: review-summary
version: 1.0.0
description: >
  Generate 4-sheet Excel review summary (评审汇总表) from 广联达 export data for
  budget review projects. Auto-classifies review line items into 7 categories:
  repeat-billing, omission, quantity, quota-subitem, material-price, other,
  base-adjustment. Use when: (1) user says "评审汇总表"/"审减底稿"/"审增减明细"/
  "审核汇总"/"导出审减成果"/"生成评审底稿", (2) user provides a folder with
  广联达导表 files and asks for review output, (3) user needs to produce the
  4-sheet review package (评审底稿+汇总表+导表填写+审增减明细), or (4) user wants
  to auto-classify review changes into the standard 7-category breakdown.
---

# 评审汇总表生成

从广联达导表自动生成4张评审汇总表。

## 用法

```bash
python3 scripts/generate_review_summary.py <数据目录> <输出.xlsx> \
  --project "项目名" --building-area 208465.8
```

数据目录下需含 `分部分项汇总审核导表.xlsx` 和 `总审核导表.xlsx`。

## 输出

| Sheet | 内容 |
|-------|------|
| 评审底稿 | 封面：送审/审定金额汇总、签名栏 |
| 汇总表 | 单位工程 × 7大类别矩阵 |
| 导表填写 | 逐条清单分类映射（含审增减原因原文） |
| 审增减明细生成表 | 按7类别归集的正式审增减清单 |

## 分类规则

脚本按优先级匹配关键字自动分类，详见 `references/classification.md`。

⚠️ **自动分类需人工复核**：
- `[调价]` 项默认归入**材料价格**，可能实为**定额子目**调整
- 关键字无法识别隐式重复计取
- 措施费/税金调整依赖"基数/税金"等关键字命中

复核后修正分类，重新运行即可。

## 模板

原始模板位于 `assets/评审汇总表模板（四张表）.xls`，作为样式参考。

## 详细参考

- 模板4张Sheet的完整列结构和数据映射：`references/template_structure.md`
- 7类审增减分类规则及判断依据：`references/classification.md`
