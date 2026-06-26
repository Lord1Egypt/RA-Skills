---
name: test-case-generator
description: 专业的测试用例生成技能。支持文本/文档输入，自动生成高质量测试用例。内置依赖检测、质量评分、多格式导出、测试数据生成、用例评审、增量更新等高级功能。支持自定义 prompt 和配置。
---

# 测试用例生成技能（完整版）

## 核心功能

根据用户提供的需求描述或需求文档，自动生成专业、全面的测试用例。

### 支持的输入方式

1. **直接文本描述** - 输入需求文字
2. **上传文档** - 支持 .txt / .docx / .pdf

### 内置高级功能

| 功能 | 说明 | 脚本 |
|------|------|------|
| 🔍 依赖检测 | 自动检测并提示安装依赖 | `check_dependencies.py` |
| 📤 多格式导出 | CSV/Markdown/JSON/XMind/TestLink | `export_testcases.py` |
| 📊 质量评分 | 5 维度评估用例质量 | `quality_score.py` |
| 📋 测试数据生成 | 自动生成配套测试数据 | `generate_testdata.py` |
| 🔎 用例评审 | 去重检测、批量修改 | `review_testcases.py` |
| 🔄 增量更新 | 需求变更对比分析 | `diff_requirements.py` |
| ⚙️ 配置管理 | 查看/修改技能配置 | `config_manager.py` |

## 快速开始

### 1. 检查依赖

```bash
python scripts/check_dependencies.py
```

### 2. 生成测试用例

提供需求描述，技能自动生成用例。

### 3. 导出用例

```bash
# 导出为 Markdown
python scripts/export_testcases.py markdown output.md < testcases.json

# 导出为 XMind
python scripts/export_testcases.py xmind output.xmind < testcases.json

# 导出为 TestLink
python scripts/export_testcases.py testlink output.xml < testcases.json
```

### 4. 质量评估

```bash
python scripts/quality_score.py testcases.json
```

### 5. 生成测试数据

```bash
python scripts/generate_testdata.py testcases.json testdata.json
```

## 使用示例

### 示例 1：基本用法

```
请帮我生成测试用例：

【需求描述】
用户登录功能：支持邮箱/手机号登录，密码长度 8-20 位...
```

### 示例 2：指定高级提示词

```
请帮我生成测试用例：

【需求描述】
[需求内容]

【特殊要求】
- 提示词配置：advanced-prompt
- 格式：CSV
```

### 示例 3：上传文档

```
请帮我从这个文档生成测试用例：
[上传：requirements.docx]
```

## 脚本工具说明

### check_dependencies.py - 依赖检测

```bash
# 检查依赖
python scripts/check_dependencies.py

# 输出：
# ✅ openpyxl - Excel 导出
# ❌ python-docx - Word 文档解析
# ⚠️  检测到缺失的依赖，请运行：pip install python-docx
```

### export_testcases.py - 多格式导出

```bash
# 导出为 Markdown
python scripts/export_testcases.py markdown output.md < testcases.json

# 导出为 XMind（思维导图）
python scripts/export_testcases.py xmind output.xmind < testcases.json

# 导出为 JSON
python scripts/export_testcases.py json output.json < testcases.json

# 导出为 TestLink XML
python scripts/export_testcases.py testlink output.xml < testcases.json
```

### quality_score.py - 质量评分

```bash
# 评估用例质量
python scripts/quality_score.py testcases.json

# 输出：
# 📊 覆盖率：   95.0/100
# ✅ 可执行性： 88.0/100
# 🔗 独立性：   92.0/100
# 📝 可维护性： 90.0/100
# 📋 完备性：   85.0/100
# 🎯 综合评分：90.0/100 - A (良好)
```

### generate_testdata.py - 测试数据生成

```bash
# 生成 JSON 格式测试数据
python scripts/generate_testdata.py testcases.json testdata.json

# 生成 CSV 格式测试数据
python scripts/generate_testdata.py testcases.json testdata.csv csv
```

### review_testcases.py - 用例评审

```bash
# 显示统计信息
python scripts/review_testcases.py testcases.json stats

# 检测相似用例
python scripts/review_testcases.py testcases.json duplicates

# 批量修改优先级
python scripts/review_testcases.py testcases.json update-priority 功能测试 P1

# 按优先级筛选
python scripts/review_testcases.py testcases.json filter-priority P0
```

### diff_requirements.py - 增量更新

```bash
# 对比需求变更
python scripts/diff_requirements.py old_req.txt new_req.txt testcases.json

# 输出增量更新计划
```

### config_manager.py - 配置管理

```bash
# 查看配置
python scripts/config_manager.py view

# 修改配置
python scripts/config_manager.py set default_format markdown

# 重置配置
python scripts/config_manager.py reset
```

## 导出格式说明

| 格式 | 适用场景 | 工具支持 |
|------|----------|----------|
| **CSV** | Excel 导入、测试管理工具 | ✅ |
| **Markdown** | 文档、Git 仓库 | ✅ |
| **JSON** | API 集成、自动化测试 | ✅ |
| **XMind** | 思维导图、评审展示 | ✅ |
| **TestLink XML** | TestLink 导入 | ✅ |

## 质量评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 覆盖率 | 20% | 需求点覆盖百分比 |
| 可执行性 | 20% | 步骤清晰度、可重复性 |
| 独立性 | 20% | 用例间依赖程度 |
| 可维护性 | 20% | 命名规范、结构清晰 |
| 完备性 | 20% | 测试类型分布 |

## 配置项说明

```json
{
  "default_prompt": "default-prompt",        // 默认提示词
  "default_format": "csv",                   // 默认导出格式
  "default_priority_rules": {...},           // 优先级规则
  "required_fields": [...],                  // 必填字段
  "min_cases_per_feature": 3,                // 每功能点最少用例数
  "enable_quality_check": true,              // 启用质量检查
  "auto_generate_testdata": true             // 自动生成测试数据
}
```

## 最佳实践

### 1. 生成前检查依赖
```bash
python scripts/check_dependencies.py
```

### 2. 生成后评估质量
```bash
python scripts/quality_score.py testcases.json
```

### 3. 根据评分改进
- 覆盖率<80：增加用例数量
- 可执行性<80：优化步骤描述
- 独立性<80：减少用例依赖
- 完备性<80：补充测试类型

### 4. 导出合适格式
- 团队评审 → XMind
- 导入工具 → CSV/TestLink
- 文档归档 → Markdown
- 自动化 → JSON

## 文件结构

```
test-case-generator/
├── SKILL.md                          # 技能说明
├── config.json                       # 配置文件
├── scripts/
│   ├── check_dependencies.py         # 依赖检测
│   ├── export_testcases.py           # 多格式导出
│   ├── quality_score.py              # 质量评分
│   ├── generate_testdata.py          # 测试数据生成
│   ├── review_testcases.py           # 用例评审
│   ├── diff_requirements.py          # 增量更新
│   └── config_manager.py             # 配置管理
└── references/
    ├── default-prompt.md             # 默认提示词
    ├── advanced-prompt.md            # 高级提示词
    ├── prompt-templates.md           # 提示词模板
    └── format-examples.md            # 格式示例
```

## 故障排查

### 问题 1：依赖缺失
```
❌ python-docx - Word 文档解析
```
**解决**：`pip install python-docx pdfplumber openpyxl`

### 问题 2：质量评分低
**解决**：查看评分报告，按建议改进用例

### 问题 3：导出的中文乱码
**解决**：使用 UTF-8 编码打开文件

## 版本信息

- **版本**：2.0（完整版）
- **更新**：新增 8 项高级功能
- **兼容**：Python 3.7+

