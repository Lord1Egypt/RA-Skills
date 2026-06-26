# Sum2Slides 使用演示指南

## 🎬 演示概览

本演示展示了Sum2Slides v1.0.1的主要功能和输出效果。通过多个实际场景示例，您可以快速了解如何使用这个工具将文本转换为专业的幻灯片演示文稿。

## 📁 演示文件结构

```
demo_outputs/              # 演示输出目录
├── basic_demo.pptx       # 基本文本转换演示
├── business_demo.pptx    # 商务模板演示
├── academic_demo.pptx    # 学术模板演示
├── file_demo.pptx        # 文件转换演示
└── advanced_demo.pptx    # 高级配置演示
```

## 🚀 运行演示

### 方法1：使用演示脚本
```bash
# 进入项目目录
cd sum2slides

# 运行演示脚本
python scripts/demo.py
```

### 方法2：手动运行演示
```bash
# 安装依赖（如果尚未安装）
pip install -e .

# 运行Python交互式演示
python -c "
from sum2slides import Sum2Slides
converter = Sum2Slides()
text = '示例文本内容'
presentation = converter.convert(text)
presentation.save('demo.pptx')
print('演示文件已生成: demo.pptx')
"
```

## 📊 演示内容详解

### 1. 基本文本转换演示
**文件**: `basic_demo.pptx`
**输入文本**: 项目总结报告
**特点**:
- 自动识别标题和内容结构
- 生成合适的幻灯片数量
- 应用默认样式和布局

**效果预览**:
```
幻灯片1: 标题页 - "项目总结报告"
幻灯片2: 项目概述
幻灯片3: 关键成果
幻灯片4: 技术亮点
幻灯片5: 下一步计划
```

### 2. 商务模板演示
**文件**: `business_demo.pptx`
**输入文本**: 季度业务报告
**配置**:
- 模板: `business`
- 主题: `light`
- 样式: 专业商务风格

**特点**:
- 商务风格的配色方案
- 专业的数据展示布局
- 适合商务汇报场景

### 3. 学术模板演示
**文件**: `academic_demo.pptx`
**输入文本**: 研究论文摘要
**配置**:
- 模板: `academic`
- 主题: `light`
- 最大幻灯片数: 8

**特点**:
- 学术风格的排版
- 规范的文献引用格式
- 适合学术报告场景

### 4. 文件转换演示
**文件**: `file_demo.pptx`
**输入文件**: `sample_input.txt`
**特点**:
- 从文件读取内容
- 自动处理文件编码
- 支持多种文本格式

### 5. 高级配置演示
**文件**: `advanced_demo.pptx`
**输入文本**: 技术分享内容
**配置**:
- 主题: `dark`
- 字体大小: 16
- 标题大小: 32
- 项目符号样式: `circle`

**特点**:
- 深色主题设计
- 自定义字体大小
- 特殊项目符号样式

## 🎨 输出效果展示

### 视觉设计
- **配色方案**: 根据模板和主题自动应用
- **字体选择**: 清晰易读的字体组合
- **布局优化**: 智能调整内容布局
- **图片占位符**: 为图片添加预留位置

### 内容结构
- **自动分页**: 根据内容长度自动分页
- **层次结构**: 保持原文的层次关系
- **重点突出**: 突出关键信息和数据
- **逻辑连贯**: 确保幻灯片之间的逻辑连贯

### 格式兼容性
- **PowerPoint兼容**: 完全兼容Microsoft PowerPoint
- **可编辑性**: 生成的文件可进一步编辑
- **跨平台**: 支持Windows、macOS、Linux
- **版本兼容**: 支持PowerPoint 2010及以上版本

## 🔧 自定义演示

### 修改演示内容
```python
from sum2slides import Sum2Slides

# 创建自定义转换器
converter = Sum2Slides(
    template="business",      # 使用商务模板
    theme="dark",            # 使用深色主题
    max_slides=10,           # 最大10张幻灯片
    font_size=14             # 字体大小14
)

# 自定义文本内容
custom_text = """
# 我的演示文稿

## 第一部分
这是我的自定义内容...

## 第二部分
更多详细说明...

## 总结
演示结束。
"""

# 生成演示文稿
presentation = converter.convert(custom_text)
presentation.save("my_presentation.pptx")
```

### 创建自己的模板
1. 在`config/templates.yaml`中添加新模板配置
2. 创建对应的PPTX模板文件
3. 在代码中引用新模板

## 📈 性能指标

### 处理速度
- 小型文本（<1000字符）: <2秒
- 中型文本（1000-5000字符）: <5秒
- 大型文本（>5000字符）: <10秒

### 输出质量
- 幻灯片数量: 根据内容自动调整（3-15张）
- 文件大小: 50-500KB（取决于内容）
- 兼容性: 100%兼容Microsoft PowerPoint

### 内存使用
- 基础内存: <50MB
- 处理内存: <100MB
- 峰值内存: <150MB

## 🎯 最佳实践

### 输入文本优化
1. **使用清晰的结构**: 使用标题和列表
2. **控制文本长度**: 每张幻灯片100-300字
3. **突出重点**: 使用粗体或项目符号
4. **保持简洁**: 避免过于冗长的段落

### 模板选择建议
1. **商务汇报**: 使用`business`模板
2. **学术报告**: 使用`academic`模板
3. **技术分享**: 使用`default`或`business`模板
4. **创意展示**: 使用`creative`模板（如可用）

### 配置优化
1. **字体大小**: 根据观众距离调整（14-18pt）
2. **主题选择**: 根据环境光线选择`light`或`dark`
3. **幻灯片数量**: 根据演讲时间控制（每张1-2分钟）

## 🆘 常见问题

### Q1: 演示文件无法打开？
A: 请确保已安装Microsoft PowerPoint或兼容的办公软件。也可以使用LibreOffice Impress打开。

### Q2: 中文显示异常？
A: 确保系统已安装中文字体。可以在配置中指定中文字体。

### Q3: 如何调整幻灯片布局？
A: 在配置文件中修改布局参数，或直接编辑生成的PPTX文件。

### Q4: 支持哪些输入格式？
A: 支持纯文本(.txt)和Markdown(.md)格式。未来版本将支持更多格式。

## 📚 进一步学习

### 文档资源
- [用户手册](USER_GUIDE.md) - 详细使用说明
- [API参考](API.md) - 完整的API文档
- [配置指南](CONFIG_GUIDE.md) - 配置选项详解

### 示例代码
- [基本使用示例](examples/basic_usage.py)
- [高级功能示例](examples/advanced_features.py)
- [批量处理示例](examples/batch_processing.py)

### 视频教程
- [快速入门视频](https://example.com/tutorial1)
- [高级功能演示](https://example.com/tutorial2)
- [实战案例分享](https://example.com/case_study)

---

## 🎉 开始使用吧！

现在您已经了解了Sum2Slides的演示功能，可以：

1. **运行演示脚本**查看实际效果
2. **修改演示内容**尝试自定义
3. **阅读文档**了解更多功能
4. **分享反馈**帮助我们改进

祝您使用愉快！ 🚀