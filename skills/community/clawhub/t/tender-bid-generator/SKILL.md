---
name: tender-bid-generator
description: Generate high-quality bid documents from tender documents. Use when users need to create bid proposals based on tender documents, including extracting tender requirements, generating bid document structure, writing section content, and outputting Word format documents. Supports parsing tender documents in PDF, Word, TXT formats, automatically identifying key information such as project details, qualification requirements, technical specifications, and evaluation criteria to generate complete bid documents that meet standards. 适用于：招标文件、投标文件、标书制作、投标书生成、招投标文档。
---

# 投标文件生成器

根据招标文件自动生成专业、高质量的投标文件。

## 工作流程

### 1. 读取招标文件

支持格式：PDF、DOCX、TXT

使用脚本解析招标文件：
```bash
python3 scripts/parse_tender.py <招标文件路径>
```

输出为JSON格式的关键信息提取结果。

### 2. 分析招标要求

提取以下关键信息：
- **项目基本信息**：项目名称、编号、采购单位、预算金额
- **资质要求**：企业资质、人员资质、业绩要求
- **技术规格**：产品/服务技术要求、参数指标
- **商务条款**：交货期、付款方式、质保期
- **评分标准**：分值分布、评分细则
- **投标文件要求**：格式、份数、装订、密封要求

### 3. 生成投标文件结构

标准投标文件结构：
```
1. 投标函
2. 法定代表人授权书
3. 投标报价表
4. 资格证明文件
   - 营业执照
   - 资质证书
   - 财务报表
   - 业绩证明
5. 技术响应文件
   - 技术方案
   - 产品说明
   - 实施计划
6. 商务响应文件
   - 交货期承诺
   - 售后服务
   - 培训方案
7. 其他材料
```

### 4. 撰写内容

参考 [references/writing-guide.md](references/writing-guide.md) 撰写各章节内容：
- 使用专业、规范的商务语言
- 针对评分标准逐条响应
- 突出企业优势和竞争力
- 确保内容完整、逻辑清晰

### 5. 输出文档

使用 [assets/bid-template.txt](assets/bid-template.txt) 模板生成最终投标文件（可导入Word使用）。

## 使用示例

**用户**: "帮我根据这个招标文件生成投标文件"

**执行步骤**:
1. 确认招标文件路径
2. 运行解析脚本提取关键信息
3. 分析招标要求
4. 基于模板生成投标文件
5. 输出Word文档

## 注意事项

- 生成的投标文件需人工审核后使用
- 确保所有资质证明文件真实有效
- 报价部分需根据实际情况填写
- 技术方案需结合企业实际能力
- 注意投标截止时间，预留足够准备时间
