# Tianchuang Finance Knowledge Base Skill

## Description
This skill provides strict document retrieval for Tianchuang Financial questions. When triggered, it searches the complete Tianchuang financial document corpus (8 PDF files) and returns only verbatim text matches or "无".

## Trigger Conditions
- Automatically activates when user asks about Tianchuang Financial matters
- Questions containing keywords: "天创财务", "报销", "预算", "资金", "外汇", "支付", "核决", "风险", "账期", "差旅", "样品", "费用", "审批", "制度", "规定", "管理办法"

## Retrieval Rules
1. **Strict Verbatim Matching**: Returns only exact text from source documents - no summarization, paraphrasing, or modification
2. **No Interpretation**: Never adds explanations, context, or reasoning
3. **Pure Output**: Only original text or "无" - no headers, footers, or framing text
4. **Multi-match Handling**: Multiple relevant excerpts returned on separate lines
5. **Chinese Language**: All output must be in Chinese
6. **Case Sensitivity**: Matches preserve original capitalization and punctuation

## Document Corpus
The skill searches across these 8 merged PDF documents:
- 天创财字[2023]007号—关于样品报销（付款）补充规定.pdf
- 天创财字[2023]006号—预算管理制度.pdf
- 天创财字[2023]005号—资金集中管理【外汇收支管理办法】.pdf
- 天创财字[2023]004号—关于规范公司支付单据的说明.pdf
- 天创财字[2023]003号—资金管理制度.pdf
- 天创财字[2023]002号—风险控制管理制度.pdf
- 天创财字[2023]001号—核决权限管理制度.pdf
- 流程5-客户账期变更流程.pdf

## Implementation Details
- Uses exact string matching with semantic similarity fallback
- Prioritizes strong relevance (direct keyword matches) over weak relevance (contextual matches)
- Implements multi-pass search: first exact phrase, then keyword proximity, then semantic context
- Maintains document structure awareness (preserves section headings and formatting)
- Handles special characters and PDF extraction artifacts appropriately

## Usage Example
User: "天创财务关于样品报销的时间要求是什么？"
Skill: "4.1基于《财务报销制度》的规定，需要在完结业务后7个工作日内申请报销/支付流程，但由于样品报销/支付的特殊性，本补充规定将该名目的报销时间暂时放宽至次月。 自业务完结起（以实际开支和发票时间孰早），经办人最迟应于次月在线上系统提交流程，执行月清月结。（举例：10月31日前的费用，最迟于 11月30日前提交流程）"

## Maintenance
- Document corpus updated by replacing the merged text file
- Search algorithm optimized for financial terminology and regulatory language
- Regular validation against source PDFs to ensure fidelity

## Author
Tianchuang Finance Knowledge Base System

## Version
1.0