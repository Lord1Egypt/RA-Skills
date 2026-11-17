# 万方产品目录与选型

## 当前快照

快照时间为 2026-10-02，来源是 wanfang.cqccjy.cn 的公共 config。所有产品当前按每 1000 字符计费，最小提示值 200、最大提示值 300000；价格必须以 products 的实时返回和支付页为准。

| Code | 用途 | 价格/1000字符 | 格式 | 日期 |
|---|---|---:|---|---|
| WF_UNDERGRADUATE | 本科 | 2.40 | doc/docx/txt/pdf/rtf | 否 |
| WF_GRADUATE | 硕博 | 2.40 | doc/docx/txt/pdf/rtf | 否 |
| WF_VOCATIONAL | 高职高专 | 2.40 | doc/docx/txt/pdf/rtf | 否 |
| WF_JOURNAL | 期刊 | 2.40 | doc/docx/txt/pdf/rtf | 否 |
| WF_TITLE | 职称 | 4.00 | doc/docx/txt/pdf/rtf | 是 |
| WF_NEW_LITERATURE | 新文献 | 2.40 | doc/docx/txt/pdf/rtf | 否 |
| WF_MONOGRAPH | 专著 | 2.60 | doc/docx/txt/pdf/rtf | 否 |
| WF_COURSEWORK | 课程作业 | 2.40 | doc/docx/txt/pdf/rtf | 否 |
| WF_TEXT_AIGC | 文本 AIGC | 1.60 | doc/docx/txt/pdf | 否 |

## 选型判断

1. 先看学校、导师、期刊或单位的书面要求；产品名称相同不代表比对库和合格线相同。
2. 本科/硕博/高职高专按论文层级和培养类型选择，不按最低价格选择。
3. 期刊、职称、新文献、专著和课程作业是不同场景，不能互相替代。
4. WF_TEXT_AIGC 只处理 AI 生成风险，不报告传统文字相似性；用户说“AI率”才进入该产品。
5. 只有用户明确从事职称/已发表材料检测，且能提供真实日期时才选 WF_TITLE。

## 文件和字符

平台最终解析字符数是计费事实。本地字数统计只能预估；不要承诺实际金额等于 Word/WPS 统计。若用户接近 300000 字符上限、上传 PDF 解析异常或文件格式边界不明，应先让用户在页面确认。
