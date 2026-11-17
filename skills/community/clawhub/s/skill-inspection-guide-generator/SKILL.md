---
name: 检验指导书（SIP）生成技能
slug: inspection-guide-generator
displayName: 检验指导书（SIP）生成技能
description: 根据产品技术文件自动生成检验指导书；支持多种格式技术文件解析、支持Excel和Word模板定制、自动提取关键信息组织为标准化检验指导书；当用户提供产品技术文件需要生成检验指导书、质量检验标准或供应商检验要求时使用
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# 检验指导书生成器

## 任务目标
- 本 Skill 用于：根据用户提供的产品技术文件自动生成检验指导书
- 能力包含：解析多种格式技术文件、支持模板定制、生成标准化检验指导书
- 触发条件：用户上传产品技术文件并需要生成检验指导书、质量检验标准或供应商检验要求

## 前置准备
- 依赖说明：scripts脚本所需的依赖包及版本
  ```
  openpyxl==3.1.2
  python-docx==1.1.0
  ```

## 操作步骤

### 步骤1：接收并解析技术文件
- 智能体读取用户上传的产品技术文件
- 支持格式：PDF、Word、Excel、图片等
- 提取关键信息：产品名称、技术参数、产品规格、测试报告、质量要求等

### 步骤2：询问用户模板需求
- 智能体向用户询问：**"您是否有检验指导书模板？如有请上传，如无将使用通用格式生成。"**
- 用户响应处理：
  - 回复"有"并上传模板 → 进入步骤3-A
  - 回复"无"或未提供模板 → 进入步骤3-B

### 步骤3-A：有模板模式
- 智能体分析用户上传的模板文件
  - Excel模板：识别表头字段和表格结构
  - Word模板：识别表格结构和字段标记
- 验证模板是否包含必填字段（检验项目、检验方法、检验标准、检验频次）
- 如模板不符合要求，提示用户并建议使用通用格式
- 模板要求详见：[references/template_requirements.md](references/template_requirements.md)

### 步骤3-B：无模板模式
- 智能体使用通用检验指导书格式组织数据
- 必填字段：检验项目、检验方法、检验标准、检验频次
- 可选字段：备注、检验工具、抽样方案、责任部门
- 格式规范详见：[references/inspection_guide_format.md](references/inspection_guide_format.md)

### 步骤4：组织检验数据
- 智能体根据技术文件内容，按以下结构组织检验数据：
  ```json
  {
    "product_name": "产品名称",
    "inspection_items": [
      {
        "item": "检验项目名称",
        "method": "检验方法",
        "standard": "检验标准",
        "frequency": "检验频次",
        "remark": "备注（可选）",
        "tool": "检验工具（可选）",
        "sampling": "抽样方案（可选）",
        "department": "责任部门（可选）"
      }
    ]
  }
  ```
- 对于不明确的检验标准，在`standard`字段标注"需确认"并说明原因

### 步骤5：生成检验指导书
- 调用脚本生成Excel文件：
  ```bash
  python scripts/generate_inspection_guide.py \
    --product_name "产品名称" \
    --inspection_data '<JSON数据>' \
    --template_path "模板路径（可选）" \
    --output_dir "./"
  ```
- 脚本说明详见：[scripts/generate_inspection_guide.py](scripts/generate_inspection_guide.py)
- 生成的文件命名格式：`{产品名称}_检验指导书_{YYYYMMDD}.xlsx`

### 步骤6：返回结果
- 智能体告知用户检验指导书已生成
- 提供文件路径供用户下载
- 如有"需确认"的标准，提醒用户核实

## 资源索引
- 生成脚本：[scripts/generate_inspection_guide.py](scripts/generate_inspection_guide.py)（用途：根据结构化数据生成Excel检验指导书）
- 格式规范：[references/inspection_guide_format.md](references/inspection_guide_format.md)（何时读取：无模板时参考通用格式）
- 模板要求：[references/template_requirements.md](references/template_requirements.md)（何时读取：用户提供模板时验证合规性）
- 默认模板：[assets/default_template.xlsx](assets/default_template.xlsx)（直接用于生成通用格式的检验指导书）

## 注意事项
- 仅在用户提供技术文件后才执行生成流程
- 模板询问是必需步骤，不得跳过
- 必填字段缺失时，智能体应主动提示用户补充
- 对于技术文件中未明确说明的标准，标注"需确认"而非自行推断
- 生成的文件保存在当前工作目录，供用户后续下载
- 充分利用智能体的文档解析能力，无需为内容提取编写脚本

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 9/10 | 输出明确; 文档详尽 |
| **总分** | **46/50** | 通过 |
