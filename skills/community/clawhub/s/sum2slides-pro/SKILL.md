# Sum2Slides v1.5.0

## 描述
Sum2Slides 是一个将文本摘要自动转换为结构化的幻灯片演示文稿的技能。它可以帮助用户快速从会议纪要、研究报告、项目总结等文本内容生成专业的演示文稿。

## 功能特性
- ✅ 纯文本输入解析
- ✅ 自动生成结构化幻灯片
- ✅ 支持多种模板和主题
- ✅ 导出为 PowerPoint (.pptx) 格式
- ✅ 命令行和 Python API 两种使用方式
- ✅ 可配置的布局和样式

## 使用方法

### 安装
```bash
# 通过 pip 安装
pip install sum2slides

# 或从源码安装
git clone https://github.com/openclaw/sum2slides.git
cd sum2slides
pip install -e .
```

### 命令行使用
```bash
# 基本使用：从文本生成幻灯片
sum2slides "你的文本内容" --output presentation.pptx

# 从文件输入
sum2slides --input notes.txt --output slides.pptx

# 使用特定模板
sum2slides --input summary.md --template business --output report.pptx

# 配置主题和字体
sum2slides --input data.txt --theme dark --font-size 16 --output output.pptx

# 查看帮助
sum2slides --help
```

### Python API 使用
```python
from sum2slides import Sum2Slides

# 基本使用
converter = Sum2Slides()
presentation = converter.convert("你的文本内容")
presentation.save("output.pptx")

# 高级配置
converter = Sum2Slides(
    template="business",
    theme="dark",
    max_slides=10,
    font_size=16
)

# 批量处理
converter.batch_convert(["input1.txt", "input2.md"], "output_dir/")
```

## 配置

### 配置文件
默认配置文件位置：`~/.config/sum2slides/config.yaml`

```yaml
# 默认配置
defaults:
  template: "default"
  theme: "light"
  max_slides: 10
  font_size: 14
  output_format: "pptx"

# 模板配置
templates:
  default:
    path: "templates/default.pptx"
    description: "默认模板"
  business:
    path: "templates/business.pptx"
    description: "商务模板"
  academic:
    path: "templates/academic.pptx"
    description: "学术模板"

# 主题配置
themes:
  light:
    primary_color: "#2c3e50"
    secondary_color: "#3498db"
    background_color: "#ffffff"
    text_color: "#333333"
  dark:
    primary_color: "#ecf0f1"
    secondary_color: "#3498db"
    background_color: "#2c3e50"
    text_color: "#ecf0f1"
```

### 环境变量
```bash
# 设置默认模板
export SUM2SLIDES_TEMPLATE=business

# 设置输出目录
export SUM2SLIDES_OUTPUT_DIR=~/presentations

# 设置日志级别
export SUM2SLIDES_LOG_LEVEL=INFO
```

## 示例

### 示例 1：会议纪要转幻灯片
```bash
# 输入文件：meeting_notes.txt
sum2slides --input meeting_notes.txt --template business --output meeting_slides.pptx
```

### 示例 2：研究报告转演示文稿
```bash
# 输入文件：research_summary.md (Markdown格式)
sum2slides --input research_summary.md --template academic --theme light --output research_presentation.pptx
```

### 示例 3：项目总结快速展示
```bash
# 直接输入文本
sum2slides "项目名称：AI助手开发
项目目标：开发智能助手系统
关键成果：1. 完成核心架构 2. 实现基础功能 3. 通过测试验证
下一步计划：1. 优化性能 2. 增加功能 3. 准备发布" --output project_update.pptx
```

## 输入格式支持

### 纯文本
```
项目总结报告

一、项目概述
本项目旨在开发一个智能助手系统...

二、关键成果
1. 完成核心架构设计
2. 实现基础功能模块
3. 通过测试验证

三、下一步计划
1. 性能优化
2. 功能扩展
3. 发布准备
```

### Markdown
```markdown
# 项目总结报告

## 项目概述
本项目旨在开发一个智能助手系统...

## 关键成果
- 完成核心架构设计
- 实现基础功能模块  
- 通过测试验证

## 下一步计划
1. 性能优化
2. 功能扩展
3. 发布准备
```

## 输出格式

### PowerPoint (.pptx)
- 支持所有 PowerPoint 功能
- 保持模板样式和布局
- 可编辑和进一步定制

### 未来支持（计划中）
- PDF 导出
- HTML 预览
- 图片格式导出

## 依赖

### 核心依赖
- `python-pptx>=0.6.21` - PowerPoint 文件生成
- `markdown>=3.4.4` - Markdown 解析
- `pydantic>=2.0.0` - 数据验证
- `click>=8.1.0` - 命令行界面

### 可选依赖
1. **开发依赖**: pytest, flake8, black, mypy
2. **文档依赖**: sphinx, sphinx-rtd-theme

## 开发

### 环境设置
```bash
# 克隆仓库
git clone https://github.com/openclaw/sum2slides.git
cd sum2slides

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装开发依赖
pip install -e ".[dev]"
```

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/unit/test_parser.py

# 带覆盖率测试
pytest --cov=src --cov-report=html
```

### 代码质量检查
```bash
# 代码格式化
black src/ tests/

# 代码检查
flake8 src/

# 类型检查
mypy src/
```

### 构建和发布
```bash
# 构建包
python -m build

# 发布到 PyPI
twine upload dist/*

# 发布到 ClawHub
clawhub publish sum2slides
```

## 许可证
MIT License

## 贡献
欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与。

## 支持
- 问题报告: [GitHub Issues](https://github.com/openclaw/sum2slides/issues)
- 文档: [Read the Docs](https://sum2slides.readthedocs.io/)
- 讨论: [GitHub Discussions](https://github.com/openclaw/sum2slides/discussions)

---

**版本**: v1.5.0  
**最后更新**: 2026-03-21  
**状态**: 稳定版  
**兼容性**: Python 3.10+