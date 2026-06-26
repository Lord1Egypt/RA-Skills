# Sum2Slides v1.5.0

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-1.5.0-orange)

**将文本摘要自动转换为结构化的幻灯片演示文稿**

## ✨ 特性

- 🚀 **快速转换**: 几秒钟内将文本转换为专业幻灯片
- 🎨 **多种模板**: 内置商务、学术、创意等多种模板
- 📝 **格式支持**: 支持纯文本和Markdown输入
- 🎯 **智能分析**: 自动识别关键点和结构
- 🔧 **高度可定制**: 可配置主题、字体、布局等
- 📊 **高质量输出**: 生成可编辑的PowerPoint文件

## 📦 安装

### 通过 pip 安装
```bash
pip install sum2slides
```

### 从源码安装
```bash
git clone https://github.com/openclaw/sum2slides.git
cd sum2slides
pip install -e .
```

## 🚀 快速开始

### 命令行使用
```bash
# 从文本生成幻灯片
sum2slides "项目总结：完成核心功能开发，通过测试验证" --output presentation.pptx

# 从文件生成
sum2slides --input meeting_notes.txt --output slides.pptx

# 使用商务模板
sum2slides --input report.md --template business --output report.pptx
```

### Python API
```python
from sum2slides import Sum2Slides

# 创建转换器
converter = Sum2Slides()

# 转换文本
presentation = converter.convert("""
# 项目更新

## 本周完成
- 完成用户认证模块
- 优化数据库性能
- 修复已知问题

## 下周计划
- 开发新功能
- 进行系统测试
- 准备发布
""")

# 保存为PPTX
presentation.save("weekly_update.pptx")
```

## 📋 使用示例

### 示例1：会议纪要转幻灯片
```bash
sum2slides --input meeting_notes.txt --template business --theme light --output meeting_slides.pptx
```

### 示例2：研究报告转演示文稿
```bash
sum2slides --input research.md --template academic --max-slides 15 --output research_presentation.pptx
```

### 示例3：项目进度报告
```bash
sum2slides "项目：AI助手开发
状态：进行中
进度：70%
关键成果：
1. 完成核心架构
2. 实现基础功能
3. 通过初步测试
风险：无重大风险
下一步：性能优化" --output project_update.pptx
```

## 🏗️ 架构

### 核心模块
```
sum2slides/
├── core/           # 核心处理模块
│   ├── parser.py   # 文本解析器
│   ├── analyzer.py # 内容分析器
│   └── generator.py # 幻灯片生成器
├── models/         # 数据模型
├── templates/      # 模板系统
├── exporters/      # 输出器
└── utils/          # 工具函数
```

### 处理流程
1. **输入解析**: 解析文本/Markdown，提取结构
2. **内容分析**: 识别关键点，确定幻灯片结构
3. **幻灯片生成**: 根据模板创建幻灯片
4. **样式应用**: 应用主题和布局
5. **输出生成**: 导出为PPTX格式

## ⚙️ 配置

### 配置文件
创建 `~/.config/sum2slides/config.yaml`:

```yaml
defaults:
  template: "business"
  theme: "light"
  max_slides: 12
  font_size: 14
  language: "zh"

templates:
  business:
    path: "/path/to/business_template.pptx"
  academic:
    path: "/path/to/academic_template.pptx"
```

### 环境变量
```bash
export SUM2SLIDES_TEMPLATE=business
export SUM2SLIDES_THEME=dark
export SUM2SLIDES_OUTPUT_DIR=~/presentations
```

## 🧪 测试

```bash
# 安装测试依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 运行特定测试
pytest tests/unit/test_parser.py -v

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

## 📚 文档

- [完整文档](https://sum2slides.readthedocs.io/)
- [API参考](docs/api/)
- [使用指南](docs/guides/)
- [示例](docs/examples/)

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与。

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 📄 许可证

本项目基于 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [python-pptx](https://github.com/scanny/python-pptx) - PowerPoint文件生成库
- [OpenClaw](https://openclaw.dev) - AI技能开发平台
- 所有贡献者和用户

## 📞 支持

- 问题报告: [GitHub Issues](https://github.com/openclaw/sum2slides/issues)
- 文档: [Read the Docs](https://sum2slides.readthedocs.io/)
- 讨论: [GitHub Discussions](https://github.com/openclaw/sum2slides/discussions)

---

**Sum2Slides v2.0** - 让演示文稿制作变得简单高效！