---
name: redcap-data-dictionary-generator
description: |
  开发者：邹和建、刘从进

  REDCap Data Dictionary Generator - 将 Word/Excel 文档（CRF/方案）转换为 CSV 格式的 REDCap 数据字典。
  
  ⚠️ 原 redcap-crf-generator 已不再更新，请使用本版本。
  
  适用场景：
  - 用户上传临床试验 CRF/方案 Word/Excel 文档，要求生成数据字典
  - 将问卷/调查表转换为 REDCap 可导入的 CSV 格式
  
  功能特点：
  - 智能识别表单、分节、字段结构
  - 支持单选题、多选题、Likert量表、频率量表
  - 自动生成 CDISC 兼容的变量名
  - 自动识别图片内容（OCR）用于评分表
  - 支持分支逻辑、计算字段、文件上传字段

metadata:
  openclaw:
    emoji: "📋"
    author: "邹和建、刘从进"
    version: "1.0.0"
    homepage: https://clawhub.ai/kenlcj/redcap-data-dictionary-generator
    requires:
      bins: ["python3", "pip"]
      python_pkgs: ["python-docx", "lxml", "markitdown"]
    install:
      - id: "python-docx"
        kind: "pip"
        package: "python-docx"
      - id: "lxml"
        kind: "pip"
        package: "lxml"
      - id: "markitdown"
        kind: "pip"
        package: "markitdown"
---

# REDCap Data Dictionary Generator

> ⚠️ **原 redcap-crf-generator 已不再更新，请使用本版本。**

## 概述

本技能将临床试验 CRF/方案文档（Word/Excel/PDF）转换为符合 REDCap 标准的数据字典 CSV 文件。

### 核心流程

1. **文档解析** → 使用 markitdown 转换为 Markdown，充分理解文档结构
2. **图片识别** → 对文档中的评分表/诊断标准图片进行 OCR 识别
3. **字段生成** → 按照 REDCap 规范生成数据字典
4. **格式修正** → 确保 Section Header、验证类型、计算字段等符合规范

## 数据字典格式（REDCap CSV）

| 列名 | 说明 | 示例 |
|------|------|------|
| Variable / Field Name | 字段变量名，CDISC规范 | `sex`, `ie_1`, `dm_3` |
| Form Name | 表单英文名 | `demography`, `inclusion_exclusion` |
| **Section Header** | **分节标题（仅首字段填写）** | `患者基本信息` |
| Field Type | 字段类型 | `text`, `dropdown`, `radio`, `checkbox`, `calc`, `notes`, `file` |
| Field Label | 字段中文标签 | `性别`, `年龄（岁）` |
| Choices, Calculations, OR Slider Labels | 选项或计算公式 | `1, 男 \| 2, 女` 或 `round([weight]/(([height]/100)^2),1)` |
| Field Note | 特殊说明/格式要求 | `单位：岁`, `YYYY-MM-DD` |
| Text Validation Type | 验证类型 | `date`, `number`, `integer`, `datetime` |
| Text Validation Min/Max | 数值范围 | `0`, `120` |
| Identifier? | 是否隐私字段（仅限姓名、身份证等直接身份标识） | `y`（是）或留空 |
| Branching Logic | 分支逻辑 | `[dm_10] = "7"` |
| Required Field? | 是否必填 | `y`（是）或留空 |

### ⚠️ 关键规则

#### 1. Section Header 仅首字段填写
> 同组字段只在第一个字段设置 Section Header，后续字段**留空**。

```csv
Variable / Field Name,Form Name,Section Header,Field Type,Field Label,...
record_id,inclusion_exclusion,,text,Record ID,...
enroll_date,inclusion_exclusion,入排标准判定,text,入组日期,...
ie_1,inclusion_exclusion,,dropdown,纳入标准1：≥18周岁,...
ie_2,inclusion_exclusion,,dropdown,纳入标准2：同种异体肝移植术后,...
```

#### 2. record_id 必须为第一行
> 第一个字段必须是 `record_id`，类型为 text，标签为 "Record ID"。

```csv
Variable / Field Name,Form Name,Section Header,Field Type,Field Label,...
record_id,inclusion_exclusion,,text,Record ID,...
```

#### 3. Identifier? 仅用于直接身份标识字段
> 仅当字段涉及患者**直接身份标识**（如姓名、身份证号、住院号、手机号等）时设置 `y`。
> 一般人口学资料（年龄、性别、体重等）不属于隐私标识，**不要**设置。

```csv
Variable / Field Name,Field Type,Identifier?,...
dm_1,text,y,...  # 编号（含姓名首字母），属于隐私
dm_3,text,,...   # 年龄，不属于隐私，无需设置
```

#### 4. calc 字段不需要验证类型
> 计算字段（calc）的 Text Validation Type / Min / Max 留空。

```csv
Variable / Field Name,Field Type,Choices, Calculations, OR Slider Labels,Text Validation Type,...
dm_bmi,calc,round([dm_6]/(([dm_5]/100)^2),1),,...
```

## 字段类型选择规则

> **选项数量决定字段类型：**
> - **≤4个选项** → 使用 `radio`（单选按钮），界面更直观
> - **≥5个选项** → 使用 `dropdown`（下拉选择），避免界面拥挤
> - **多选** → 使用 `checkbox`

| 选项数 | 推荐类型 | 示例 |
|---------|----------|------|
| 2-4 | `radio` | `1, 是 \| 0, 否` |
| ≥5 | `dropdown` | `1, HBV \| 2, HCV \| 3, DILI \| 4, PBC \| 5, 肿瘤 \| 6, 其他` |
| 多选 | `checkbox` | `1, 血流 \| 2, 肺部 \| 3, 腹腔 \| 4, 泌尿系统` |

### 支持的字段类型

| 类型 | 说明 | Choices 格式 |
|------|------|-------------|
| `text` | 单行文本 | 无 |
| `notes` | 多行文本/备注 | 无 |
| `radio` | 单选按钮（≤4个选项） | `0, 否 \| 1, 是` |
| `dropdown` | 下拉选择（≥5个选项） | `0, 否 \| 1, 是 \| 2, 其他` |
| `checkbox` | 多选框 | `1, 选项1 \| 2, 选项2 \| 3, 选项3` |
| `calc` | 计算字段 | `round([weight]*10000/([height]^2),1)` |
| `file` | 文件上传 | 无 |
| `date` | 日期（用 text + date 验证） | 无 |
| `datetime` | 日期时间（用 text + datetime 验证） | 无 |

## 处理复杂文档的技巧

### 1. 文档结构识别
- 使用 `markitdown` 将文档转为 Markdown
- 识别 `表X：` 或 `表X  ` 格式的表单标题（注意可能混用全角/半角空格）
- 段落中的 `{}`、`（）` 包含字段定义

### 2. 图片 OCR 识别
当文档包含评分表图片（如 SOFA、APACHE、GCS、诊断标准）时：
- 从 docx 中提取图片（word/media/ 目录）
- 使用 `image` 工具识别图片内容
- 将识别结果转换为结构化字段

### 3. 括号兼容性
文档可能混用 ASCII 和全角括号：
- ASCII: `{单选，是，否}`
- 全角: `｛单选，是，否｝`
- 处理时需同时检查两种格式

### 4. 分支逻辑处理
分支逻辑写在 Choices 中，通过 `[字段] = "值"` 格式标注：

```python
choices = "1, 是 | 0, 否"
branching = '[dm_10] = "7"'  # 当选择"其他"时显示备注文本
```

## CDISC 变量命名建议

| 前缀 | 表单 | 示例 |
|------|------|------|
| `ie_` | inclusion_exclusion 入排标准 | `ie_1`, `ie_2` |
| `dm_` | demography 患者基本信息 | `dm_1`, `dm_3` |
| `meld_` | pre_meld MELD评分 | `meld_inr`, `meld_score` |
| `sofa_p_` | pre_sofa 术前SOFA | `sofa_p_gcs`, `sofa_p_total` |
| `apach_` | pre_apache APACHE评分 | `apach_p_temp`, `apach_p_total` |
| `cci_` | pre_cci Charlson合并症 | `cci_1`, `cci_total` |
| `infrf_` | preop_infrf 术前感染因素 | `infrf_1`, `infrf_3_detail` |
| `op_` | op_info 手术信息 | `op_date`, `op_blood_rbc` |
| `don_` | donor_info 供体信息 | `don_age`, `don_hbsag` |
| `inf_` | infection_info 感染信息 | `inf_date`, `inf_site` |
| `sofa_i_` | infection_sofa 感染时SOFA | `sofa_i_pf`, `sofa_i_total` |
| `apach_i_` | infection_apache 感染时APACHE | `apach_i_gcs`, `apach_i_total` |
| `bsi_` | bsi_criteria 血流感染标准 | `bsi_1`, `bsi_2_symptom` |
| `abi_` | abi_criteria 腹腔感染标准 | `abi_ssi`, `abi_ia_clinical` |
| `pulm_` | pulm_criteria 肺部感染标准 | `pulm_img_1`, `pulm_symptom` |
| `fu_` | treatment_fu 随访 | `fu_date`, `fu_abx` |
| `out_` | outcome 结局 | `out_clinical`, `out_survive_90d` |

## 使用方式

当用户上传文档并要求生成数据字典时：

```
1. 读取文档（markitdown 转换为 Markdown）
2. 提取并识别文档中的图片（如有评分表）
3. 解析表单结构和字段定义
4. 按上述规则生成数据字典
5. 确保 record_id 为第一行
6. 通过飞书发送 CSV 文件
```

## 依赖

```bash
pip install python-docx lxml markitdown
```
