# 更新日志 (CHANGELOG)

本文档记录项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

---

## [1.1.0] - 2026-03-16

### 变更

#### 架构调整
- **移除API依赖**: 完全移除WPS开放平台API依赖，改为纯本地处理模式
- **本地化处理**: 所有功能现在都在本地执行，无需网络连接和API密钥

#### 删除的文件
- `utils/api_client.py` - WPS API客户端
- `utils/auth.py` - API认证管理
- `test_api_auth.py` - API认证测试
- `test_auth_explore.py` - API探索测试
- `API_AUTH_DIAGNOSIS.md` - API诊断文档
- `API_CHECKLIST.md` - API检查清单
- `API_VALIDATION.json` - API验证配置
- `.env` - 环境变量配置
- `.env.example` - 环境变量示例
- `PROJECT_SUMMARY.md` - 项目总结
- `TEST_REPORT.md` - 测试报告
- `api_specs/` - API规格文档目录

#### 修改的模块

**main.py**
- 移除 `WPSAPIClient` 和 `AuthManager` 导入
- 移除API客户端初始化逻辑
- 简化为纯本地处理模式

**modules/document.py**
- 移除API调用，改为本地模板生成
- `_generate_content_with_ai()` 改为 `_generate_template_content()`
- `polish_document()` 改为本地基础润色
- `review_contract()` 改为本地关键词检测

**modules/spreadsheet.py**
- 移除API调用
- `smart_analysis()` 改为返回提示信息

**modules/presentation.py**
- 移除API调用
- `generate_outline()` 改为本地模板生成

**modules/pdf.py**
- 移除API调用
- `_extract_summary()` 改为截取前500字符
- `_extract_key_points()` 改为提取前10行

**requirements.txt**
- 移除 `aiohttp>=3.9.0`
- 移除 `python-dotenv>=1.0.0`
- 移除 `tenacity>=8.2.3`
- 添加 `reportlab>=4.0.0`

**test_basic.py**
- 移除 `python-dotenv` 导入和 `.env` 加载
- 修正测试用例以匹配新的意图解析规则

**test_complete.py**
- 移除 `python-dotenv` 导入和 `.env` 加载
- 修正测试用例以匹配新的意图解析规则

**README.md**
- 更新为本地化工具文档
- 移除API配置说明
- 更新架构设计说明

### 新增特性
- 无需外部API密钥即可使用
- 完全离线运行能力
- 数据隐私保护（所有处理在本地完成）

### 修复
- 修复合同审查结果返回类型错误
- 修复意图解析测试用例

---

## [1.0.0] - 2026-03-16

### 新增

#### 核心功能
- **文档处理模块** (`modules/document.py`)
  - 公文生成：支持通知、报告、会议纪要、合同、函件
  - 智能润色：正式化、精简化、商务化三种风格
  - 合同审查：风险条款识别、风险评分、修改建议

- **表格处理模块** (`modules/spreadsheet.py`)
  - 数据清洗：去重、缺失值处理、异常值移除
  - 智能分析：求和、平均值、计数、最大值、最小值、筛选、透视
  - 图表生成：柱状图、折线图、饼图、散点图

- **演示处理模块** (`modules/presentation.py`)
  - 大纲生成：根据主题自动生成PPT大纲
  - 智能排版：商务、创意、简约、科技四种风格
  - 批量生成：从Excel数据批量生成PPT

- **PDF处理模块** (`modules/pdf.py`)
  - 格式转换：PDF转Word、PDF转Excel
  - 内容提取：文本提取、表格提取、摘要生成、要点提取
  - 批量处理：合并、拆分、水印

#### 自然语言接口
- 意图解析器 (`IntentParser`)
- 支持12种操作类型的自然语言识别
- 自动路由到对应处理模块

#### 项目结构
```
wps-office-automation/
├── __init__.py
├── skill.yaml
├── requirements.txt
├── main.py
├── modules/
│   ├── document.py
│   ├── spreadsheet.py
│   ├── presentation.py
│   └── pdf.py
├── utils/
│   ├── api_client.py
│   └── auth.py
└── examples/
    ├── document_examples.py
    ├── spreadsheet_examples.py
    ├── presentation_examples.py
    └── pdf_examples.py
```

#### 测试
- `test_basic.py` - 基础功能测试
- `test_complete.py` - 完整功能测试

#### 文档
- `README.md` - 完整使用文档
- `PROJECT_SUMMARY.md` - 项目总结
- `TEST_REPORT.md` - 测试报告
- `.env.example` - 环境变量示例

---

## 版本说明

- **[1.1.0]** - 本地化版本，移除所有API依赖
- **[1.0.0]** - 初始版本，支持WPS API集成

---

## 升级指南

### 从 1.0.0 升级到 1.1.0

1. **删除环境变量文件**
   ```bash
   rm .env .env.example
   ```

2. **更新依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **更新代码调用**
   - 无需修改调用方式，API保持兼容
   - 部分AI增强功能改为本地基础处理

4. **注意事项**
   - 文档润色功能改为基础替换处理
   - 合同审查改为关键词检测
   - PDF摘要提取改为截取前500字符
   - PPT大纲生成改为模板生成

---

## 路线图

### 计划功能
- [ ] 集成本地LLM模型（如Ollama）
- [ ] 增强文档润色算法
- [ ] 添加更多公文模板
- [ ] 支持更多图表类型
- [ ] PDF OCR文字识别
- [ ] 批量文件处理优化

---

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License
