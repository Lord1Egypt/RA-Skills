---
name: save-report
description: Save medical test reports from images with AI-powered data extraction, supporting both biochemical tests and imaging studies.
argument-hint: <图片路径> [检查日期(YYYY-MM-DD)]>
allowed-tools: Read, Write, mcp__4_5v_mcp__analyze_image
schema: save-report/schema.json
---

# Save Medical Test Report Skill

Save user-provided medical test reports to the personal medical data center.

## 核心流程

```
用户输入图片 -> 读取并分析图片 -> 提取数据 -> 生成JSON -> 保存图片和数据 -> 更新索引 -> 确认输出
```

## 步骤 1: 检查参数

- **image_path（必填）**：检查单图片的本地路径
- **exam_date（可选）**：检查日期，格式 YYYY-MM-DD

## 步骤 2: 日期确定规则（重要）

**优先级顺序：**
1. **用户提供的 exam_date**（最高优先级）
2. 图片中的采样时间
3. 图片中的送样时间
4. 图片中的检测时间/报告时间
5. 图片中的其他日期标识
6. 当前日期（仅作备选）

## 步骤 3: 读取并分析图片

### 图片分析提示词模板

**生化检查提示词：**
```
请详细识别这张医疗检验报告单中的所有信息，包括：
1. 日期时间信息（采样/送检/检测/报告时间）
2. 医院/检验机构名称
3. 检验项目和结果（项目名、数值、单位、参考范围、异常标识）
```

**影像检查提示词：**
根据检查类型使用对应的提示词模板：
- B超/彩超检查
- X光检查
- CT检查
- MRI检查
- 内窥镜检查
- 病理检查
- 心电图检查
- 乳腺钼靶检查
- PET-CT检查

## 步骤 4: 生成数据文件

### File Path Format

- Biochemical tests: `data/biochemical-tests/YYYY-MM/YYYY-MM-DD_test-type.json`
- Imaging studies: `data/imaging-studies/YYYY-MM/YYYY-MM-DD_exam-type_body-part.json`

### 数据结构定义

完整的数据结构定义请参考 `schema.json` 文件。该文件使用 JSON Schema 格式定义了两种报告类型：

#### 生化检查 (BiochemicalTestReport)
- `id`: 唯一标识符
- `type`: 固定值 "生化检查"
- `date`: 检查日期 (YYYY-MM-DD)
- `hospital`: 医院/检验机构名称
- `original_image`: 原始图片路径
- `items`: 检验项目数组
  - `name`: 项目名称
  - `value`: 检查值
  - `unit`: 单位
  - `min_ref`: 参考区间最小值
  - `max_ref`: 参考区间最大值
  - `is_abnormal`: 是否异常

#### 影像检查 (ImagingTestReport)
- `id`: 唯一标识符
- `type`: 固定值 "影像检查"
- `subtype`: 检查类型（B超/CT/MRI/X光/内窥镜/病理/心电图/乳腺钼靶/PET-CT）
- `date`: 检查日期 (YYYY-MM-DD)
- `hospital`: 医院/检验机构名称
- `body_part`: 检查部位
- `findings`: 检查结果
  - `description`: 检查所见描述
  - `targets`: 目标病灶数组（可选）
    - `name`: 病灶名称
    - `location`: 位置
    - `size`: 尺寸（长/宽/高/单位）
    - `characteristics`: 特征（形态/边界/密度）
  - `conclusion`: 检查结论
- `original_image`: 原始图片路径

## 步骤 5: 保存数据

1. 创建月份目录（如不存在）
2. 创建 images 子目录（如不存在）
3. 复制原始图片到对应目录
4. 保存 JSON 数据文件
5. 更新全局索引 `data/index.json`

## 步骤 6: 更新索引

在 `data/index.json` 中添加新记录的索引信息。

## 执行指令

```
1. 验证图片路径
2. 读取 schema.json 确认数据结构定义
3. 使用 mcp__4_5v_mcp__analyze_image 分析图片
4. 提取数据（优先使用用户提供的日期）
5. 根据 schema.json 生成符合规范的JSON数据文件
6. 复制图片到images目录
7. 保存JSON文件
8. 更新index.json
9. 显示确认信息
```

## Schema 验证

生成的 JSON 数据必须符合 `schema.json` 中定义的结构。Schema 使用 `oneOf` 关键字区分两种报告类型：
- 生化检查报告 (`type: "生化检查"`)
- 影像检查报告 (`type: "影像检查"`)

## 示例交互

### 自动提取日期
```
用户: @医疗报告/血液检查.jpg

输出:
✅ 检查单保存成功！
类型：生化检查（血液常规）
日期：2025-10-07（从图片提取）
提取到 15 项检查指标
文件路径：data/生化检查/2025-10/2025-10-07_血液常规.json
```

### 手动指定日期
```
用户: @医疗报告/血液检查.jpg 2025-10-07

输出:
✅ 检查单保存成功！
类型：生化检查（血液常规）
日期：2025-10-07（使用用户指定日期）
```
