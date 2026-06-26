---
name: xtranslate
description_zh: 多格式文档智能翻译工具，支持PDF/Word/Excel/PPT/TXT/RTF等格式，保留原文档格式并进行自动排版优化，集成智能监控和性能优化系统
description_en: Multi-format document intelligent translation tool supporting PDF/Word/Excel/PPT/TXT/RTF formats, preserving original document formatting with automatic layout optimization, integrated with smart monitoring and performance optimization system
version: 3.2
---

# Xtranslate 智能翻译工具 / Intelligent Translation Tool

## OpenClaw调用方式 / OpenClaw Invocation Method

当用户在OpenClaw中提出以下需求时，调用本技能：
When users request the following in OpenClaw, invoke this skill:

| 用户指令 / User Commands | 执行动作 / Execution Actions |
|---------|---------|
| "翻译文档" / "翻译文件" / "翻译PDF/Word"<br>"Translate document" / "Translate file" / "Translate PDF/Word" | 调用程序自动翻译指定文件<br>Invoke program to automatically translate specified file |
| "批量翻译" / "翻译文件夹"<br>"Batch translation" / "Translate folder" | 批量处理文件夹内所有支持格式的文件<br>Batch process all supported format files in folder |


### 调用示例 / Invocation Examples

**用户说 / User says**："帮我翻译这个PDF文件"<br>"Help me translate this PDF file"

**Claude执行 / Claude executes**：
```bash
python src/main.py --file document.pdf --engine cloud
```

**用户说 / User says**："批量翻译这个文件夹"<br>"Batch translate this folder"

**Claude执行 / Claude executes**：
```bash
python src/main.py --dir ./documents --engine cloud --model "DeepSeek (V3/R1)"
```

## 核心指令 / Core Commands

当用户需要翻译文档时，执行以下流程：<br>When users need to translate documents, execute the following process:

1. **配置翻译引擎** → 云端模型 / Ollama本地 / Python内置<br>**Configure translation engine** → Cloud model / Ollama local / Python built-in
2. **指定文件** → 支持PDF/DOCX/XLSX/PPTX/TXT/RTF等格式<br>**Specify file** → Support PDF/DOCX/XLSX/PPTX/TXT/RTF and other formats
3. **执行翻译** → 程序自动提取文本、翻译、保留格式、优化排版<br>**Execute translation** → Program automatically extracts text, translates, preserves format, optimizes layout
4. **输出结果** → 生成翻译后的文件到指定目录<br>**Output results** → Generate translated files to specified directory

## 快速使用 / Quick Start

```bash
# 翻译单个文件 / Translate single file
python src/main.py --file document.pdf --engine cloud

# 批量翻译文件夹 / Batch translate folder
python src/main.py --dir ./documents --output ./translated

# 指定模型和语言方向 / Specify model and language direction
python src/main.py --file doc.docx --model "GPT-4o" --sl en --tl zh-CN

# 使用Ollama本地模型 / Use Ollama local model
python src/main.py --file doc.pdf --engine ollama
```

## 配置说明 / Configuration Guide

### 环境变量配置 / Environment Variable Configuration
```bash
# DeepSeek API密钥 / API Key
$env:DEEPSEEK_API_KEY="your-api-key-here"

# OpenAI API密钥 / API Key
$env:OPENAI_API_KEY="your-api-key-here"

# Anthropic API密钥 / API Key
$env:ANTHROPIC_API_KEY="your-api-key-here"

# SiliconFlow API密钥 / API Key
$env:SILICONFLOW_API_KEY="your-api-key-here"
```

### 支持的翻译引擎 / Supported Translation Engines

| 引擎 / Engine | 说明 / Description | 适用场景 / Use Cases |
|------|------|---------|
| cloud | 云端大模型(DeepSeek/GPT-4o/Claude等)<br>Cloud large models (DeepSeek/GPT-4o/Claude, etc.) | 高质量翻译，推荐<br>High-quality translation, recommended |
| ollama | 本地Ollama模型<br>Local Ollama model | 隐私保护，离线使用<br>Privacy protection, offline use |
| python | 内置translate库<br>Built-in translate library | 紧急备用，质量一般<br>Emergency backup, average quality |

### 支持的云端模型 / Supported Cloud Models
- DeepSeek (V3/R1)
- GPT-4o
- Claude 3.5 Sonnet
- SiliconFlow (Qwen2.5)
- 自定义 (OpenAI兼容接口)<br>Custom (OpenAI compatible interface)

### 性能优化配置 / Performance Optimization Configuration
- **智能批次优化**: 自动调整批次大小以平衡速度和质量<br>**Smart Batch Optimization**: Automatically adjust batch size to balance speed and quality
- **并发处理**: 支持多批次并行翻译（可配置）<br>**Concurrent Processing**: Support multi-batch parallel translation (configurable)
- **参数调优**: temperature=0.3 平衡准确性和创造性<br>**Parameter Tuning**: temperature=0.3 balances accuracy and creativity
- **大文档优化**: 针对90页以上文档的特殊优化配置<br>**Large Document Optimization**: Special optimization configuration for documents over 90 pages

## 输出结构 / Output Structure

```
output/                          # 输出文件夹（自动创建）<br># Output folder (automatically created)
├── translated_原文件名.docx     # 翻译后的Word文档<br># Translated Word document
├── translated_原文件名.pdf      # 翻译后的PDF（通过Word转换）<br># Translated PDF (converted from Word)
├── translated_原文件名.xlsx     # 翻译后的Excel<br># Translated Excel
├── translated_原文件名.pptx     # 翻译后的PPT<br># Translated PPT
tmp/                             # 临时文件夹<br># Temporary folder
└── [PDF转Word临时文件]          # 自动清理<br># [PDF to Word temporary files]  # Auto cleanup
```

### 文件说明 / File Description
- **自动排版** - Word文档自动设置宋体/Times New Roman字体，1.25倍行距<br>**Automatic Layout** - Word documents automatically set SimSun/Times New Roman font, 1.25 line spacing
- **格式保留** - 保留原文档的表格、段落、样式等格式<br>**Format Preservation** - Preserve tables, paragraphs, styles and other formats of original documents
- **关键词引导** - 自动提取文档关键词，提升专业术语翻译准确性<br>**Keyword Guidance** - Automatically extract document keywords to improve professional term translation accuracy

## 功能特点 / Features

- ✅ **多格式支持** - PDF/DOCX/XLSX/PPTX/TXT/RTF/WPS<br>**Multi-format Support** - PDF/DOCX/XLSX/PPTX/TXT/RTF/WPS
- ✅ **格式保留** - 翻译后保留原文档结构和样式<br>**Format Preservation** - Preserve original document structure and style after translation
- ✅ **智能排版** - 自动优化Word字体和行距<br>**Smart Layout** - Automatically optimize Word fonts and line spacing
- ✅ **批量处理** - 支持文件夹批量翻译<br>**Batch Processing** - Support folder batch translation
- ✅ **多引擎支持** - 云端/本地/内置三种引擎可选<br>**Multi-engine Support** - Three engines available: cloud/local/built-in
- ✅ **关键词提取** - 使用jieba提取专业术语提升翻译质量<br>**Keyword Extraction** - Use jieba to extract professional terms to improve translation quality

- ✅ **API加密** - API Key加密存储，确保安全<br>**API Encryption** - Encrypt API Key storage to ensure security
- ✅ **智能监控** - 全程记录翻译过程，自动性能分析<br>**Smart Monitoring** - Record translation process throughout, automatic performance analysis
- ✅ **自动优化** - 基于历史数据提供优化建议<br>**Auto Optimization** - Provide optimization suggestions based on historical data
- ✅ **JSON批量** - 云模型采用JSON格式批量翻译，提升效率<br>**JSON Batch** - Cloud model uses JSON format for batch translation, improving efficiency
- ✅ **性能优化** - 智能批次调整，大文档处理速度提升25-30%<br>**Performance Optimization** - Smart batch adjustment, large document processing speed improved by 25-30%
- ✅ **并发加速** - 支持多批次并行处理，进一步提升效率<br>**Concurrent Acceleration** - Support multi-batch parallel processing, further improve efficiency

## 文件结构 / File Structure

```
Xtranslate/
├── SKILL.md                  # 核心指令 + 元数据<br># Core instructions + metadata
├── requirements.txt          # Python依赖列表<br># Python dependency list
├── Xtranslate.spec           # PyInstaller打包配置<br># PyInstaller packaging configuration
│
├── src/                      # 源代码目录<br># Source code directory
│   ├── config.py             # 全局配置（引擎、模型、语言等）<br># Global configuration (engines, models, languages, etc.)
│   ├── main.py               # 命令行入口程序<br># Command line entry program
│   ├── translator.py         # 翻译引擎模块<br># Translation engine module
│   ├── file_handler.py       # 文件读写处理器<br># File read/write processor
│   ├── analyzer.py           # 文本分析与关键词提取<br># Text analysis and keyword extraction
│   ├── formatter.py          # Word排版优化器<br># Word layout optimizer

│   ├── crypto_utils.py       # API Key加密工具<br># API Key encryption tool
│   ├── translation_monitor.py # 翻译过程监控器<br># Translation process monitor
│   └── ...
│
├── templates/                # 代码模板<br># Code templates
│   ├── module.py.md          # Python模块模板<br># Python module template
│   └── translator_engine.py.md # 新增引擎模板<br># New engine template
│
├── examples/                 # 代码示例<br># Code examples
│   ├── good.md               # 优秀代码示例<br># Excellent code examples
│   └── anti-pattern.md       # 反模式示例<br># Anti-pattern examples
│
├── references/               # 规范参考<br># Specification references
│   ├── naming-convention.md  # 命名规范<br># Naming convention
│   └── project-structure.md  # 项目结构规范<br># Project structure specification
│
├── scripts/                  # 辅助脚本<br># Auxiliary scripts
│   └── check-deps.py         # 依赖检查脚本<br># Dependency check script
│
├── translation_monitor.json  # 翻译监控记录文件<br># Translation monitoring record file
├── analyze_performance.py    # 性能分析脚本<br># Performance analysis script
├── view_monitor.py           # 监控记录查看脚本<br># Monitoring record viewing script
├── view_detail.py            # 详细记录查看脚本<br># Detailed record viewing script
│
├── build/                    # 构建文件<br># Build files
├── dist/                     # 可执行文件输出<br># Executable file output
│   └── Xtranslate.exe        # Windows可执行文件<br># Windows executable file
├── output/                   # 翻译结果输出<br># Translation result output
└── tmp/                      # 临时文件<br># Temporary files
```

## 模块说明 / Module Description

| 模块 / Module | 功能 / Function |
|------|------|
| config.py | 全局配置管理，包含模型配置、API设置、批次参数<br>Global configuration management, including model configuration, API settings, batch parameters |
| main.py | 命令行入口，支持参数解析和批量处理<br>Command line entry, supports parameter parsing and batch processing |
| translator.py | 翻译核心，支持cloud/ollama/python三种引擎<br>Translation core, supports cloud/ollama/python three engines |
| file_handler.py | 多格式文件读写（Word/Excel/PPT/PDF/TXT等）<br>Multi-format file read/write (Word/Excel/PPT/PDF/TXT, etc.) |
| analyzer.py | 使用jieba进行中文关键词提取<br>Use jieba for Chinese keyword extraction |
| formatter.py | Word文档自动排版优化<br>Word document automatic layout optimization |

| crypto_utils.py | Fernet加密API Key<br>Fernet encrypt API Key |
| translation_monitor.py | 翻译过程全程监控，性能统计与自动分析<br>Full-process monitoring of translation, performance statistics and automatic analysis |

## 依赖安装 / Dependency Installation

```bash
pip install -r requirements.txt
```

### 主要依赖 / Main Dependencies
- openai - 云端模型API调用<br>Cloud model API calls
- ollama - 本地Ollama模型<br>Local Ollama model
- python-docx - Word文档处理<br>Word document processing
- pdf2docx - PDF转Word<br>PDF to Word conversion
- openpyxl - Excel处理<br>Excel processing
- python-pptx - PPT处理<br>PPT processing

- jieba - 中文分词和关键词提取<br>Chinese word segmentation and keyword extraction
- cryptography - API Key加密<br>API Key encryption
- translate - Python内置翻译库<br>Python built-in translation library
- striprtf - RTF文件处理<br>RTF file processing

## 智能监控系统 / Smart Monitoring System

### 监控功能 / Monitoring Functions
- **全程记录** - 自动记录每次翻译的详细过程<br>**Full Process Recording** - Automatically record detailed process of each translation
- **性能统计** - 精确测量各阶段耗时<br>**Performance Statistics** - Accurately measure time consumption of each stage
- **自动分析** - 每10次翻译后生成性能报告<br>**Automatic Analysis** - Generate performance report after every 10 translations
- **优化建议** - 基于历史数据提供针对性优化方案<br>**Optimization Suggestions** - Provide targeted optimization solutions based on historical data

### 监控文件 / Monitoring Files
- `translation_monitor.json` - 存储所有翻译记录<br>`translation_monitor.json` - Store all translation records
- `analyze_performance.py` - 性能深度分析脚本<br>`analyze_performance.py` - Performance deep analysis script
- `view_monitor.py` - 查看记录概览<br>`view_monitor.py` - View record overview
- `view_detail.py` - 查看详细记录<br>`view_detail.py` - View detailed records

### 使用示例 / Usage Examples
```bash
# 查看翻译记录概览 / View translation record overview
python view_monitor.py

# 查看详细记录 / View detailed records
python view_detail.py

# 性能深度分析 / Performance deep analysis
python analyze_performance.py
```

## 故障排除 / Troubleshooting

| 问题 / Issues | 解决方案 / Solutions |
|------|----------|
| API Key错误 / API Key error | 检查环境变量是否正确设置<br>Check if environment variables are correctly set |
| PDF转换失败 / PDF conversion failed | 确保PDF非扫描件，有可选中文字<br>Ensure PDF is not scanned and has selectable text |

| Ollama连接失败 / Ollama connection failed | 确保Ollama服务已启动<br>Ensure Ollama service is started |
| 翻译质量差 / Poor translation quality | 尝试切换云端模型，或使用关键词引导<br>Try switching cloud models, or use keyword guidance |
| 排版错乱 / Layout disorder | 检查原文档格式是否过于复杂<br>Check if original document format is too complex |
| 翻译速度慢 / Slow translation speed | 使用analyze_performance.py分析性能瓶颈<br>Use analyze_performance.py to analyze performance bottlenecks |
| 监控记录异常 / Monitoring record exception | 检查translation_monitor.json文件权限<br>Check translation_monitor.json file permissions |
| 大文档处理过慢 / Large document processing too slow | 检查是否启用了性能优化配置<br>Check if performance optimization configuration is enabled |
| 并发处理失败 / Concurrent processing failed | 降低concurrent参数或检查API限制<br>Reduce concurrent parameter or check API limits |

---

**注意**：本工具仅供个人学习研究使用，请遵守相关平台规则。
