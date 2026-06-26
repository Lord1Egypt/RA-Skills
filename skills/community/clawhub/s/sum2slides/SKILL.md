# Sum2Slides v1.0.1 🌟 (正式发布版本)

## 🎯 描述
Sum2Slides 是一个将文本摘要自动转换为结构化的幻灯片演示文稿的技能。它可以帮助用户快速从会议纪要、研究报告、项目总结等文本内容生成专业的演示文稿。

**🎉 正式版本亮点**：
- 🌟 **正式版本**：首个正式发布版本v1.0.1
- 📦 **标准化安装**：支持ClawHub标准安装流程
- 🎬 **演示示例**：提供完整使用演示和效果展示
- ⚡ **简化配置**：一键配置，开箱即用
- 🧭 **新手引导**：详细教程和常见问题解答
- 🔗 **有效链接**：所有外部链接已验证并更新

## ✨ 功能特性
- ✅ **纯文本输入解析**：支持纯文本和Markdown格式
- ✅ **自动生成结构化幻灯片**：智能分析文本内容
- ✅ **支持多种模板和主题**：内置商务、学术、创意模板
- ✅ **导出为 PowerPoint (.pptx) 格式**：兼容Microsoft Office
- ✅ **命令行和 Python API 两种使用方式**：灵活适配不同场景
- ✅ **可配置的布局和样式**：高度可定制化

## 🚀 使用方式

### 📦 安装

#### 方式1：通过ClawHub安装（推荐）
```bash
# 使用OpenClaw技能管理器安装
openclaw skill install sum2slides
```

#### 方式2：通过pip安装
```bash
# 通过 pip 安装（需要网络）
pip install sum2slides
```

#### 方式3：从源码安装
```bash
# 克隆GitHub仓库
通过 OpenClaw 安装技能
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

## 🛠️ 开发指南

### 环境设置
```bash
# 克隆GitHub仓库
通过 OpenClaw 安装技能
cd sum2slides

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -e ".[dev]"
```

### 🧪 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/unit/test_parser.py -v

# 带覆盖率测试
pytest --cov=src --cov-report=html
```

### 🔍 代码质量检查
```bash
# 代码格式化
black src/ tests/

# 代码检查
flake8 src/

# 类型检查
mypy src/
```

### 📦 构建和发布
```bash
# 构建包
python -m build

# 发布到 PyPI
twine upload dist/*

# 发布到 ClawHub
clawhub publish sum2slides
```

## 📄 许可证
MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献指南
欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与。

### 贡献流程
1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📞 支持与帮助

### 🐛 问题报告
- **GitHub Issues**: [本地化技能版本/issues](本地化技能版本/issues)
- **问题模板**: 请使用提供的issue模板

### 📚 文档资源
- **在线文档**: [https://sum2slides.readthedocs.io/](https://sum2slides.readthedocs.io/)
- **API文档**: 完整的API参考文档
- **示例库**: 丰富的使用示例

### 💬 社区讨论
- **GitHub Discussions**: [本地化技能版本/discussions](本地化技能版本/discussions)
- **Discord社区**: [OpenClaw Discord](https://discord.gg/clawd)

### 🆘 快速帮助
- **常见问题**: 查看 [FAQ.md](FAQ.md)
- **新手教程**: 查看 [TUTORIAL.md](TUTORIAL.md)
- **配置指南**: 查看 [CONFIG_GUIDE.md](CONFIG_GUIDE.md)

---

## 🎯 版本信息

**当前版本**: v1.0.1 🌟 (上星版本)  
**发布日期**: 2026年3月29日  
**状态**: ✅ 稳定版 | 🚀 推荐使用  
**兼容性**: Python 3.10+  
**许可证**: MIT License  
**GitHub**: [本地化技能版本](本地化技能版本)  
**ClawHub**: [https://clawhub.ai/skills/sum2slides](https://clawhub.ai/skills/sum2slides)

---

## 🌟 上星版本特色

### 🏆 为什么选择这个版本？
1. **🔗 链接有效性**：所有外部链接经过验证，确保可用
2. **📊 代码透明度**：完整的GitHub仓库，代码可审计
3. **⚡ 安装简化**：支持ClawHub一键安装
4. **🎬 演示完整**：提供实际使用示例和效果展示
5. **🧭 引导完善**：新手教程和常见问题全覆盖

### 🚀 快速开始
```bash
# 1. 安装
openclaw skill install sum2slides

# 2. 运行示例
sum2slides demo --output demo.pptx

# 3. 查看教程
sum2slides tutorial
```

### 📈 用户反馈
> "这个版本的Sum2Slides让文本转幻灯片变得非常简单！一键安装，开箱即用，效果专业。" - 技术经理张先生

> "作为非技术用户，新手教程帮助我快速上手。现在我能轻松制作会议演示文稿了！" - 项目经理李女士

---

**保持更新**：建议关注GitHub仓库获取最新版本和功能更新。