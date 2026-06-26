# Sum2Slides 常见问题（FAQ）

## 📋 问题分类

- 🚀 安装和配置问题
- 💻 基本使用问题
- 🎨 模板和主题问题
- 📄 输出和格式问题
- 🔧 高级功能和配置问题
- 🆘 故障排除和错误处理

---

## 🚀 安装和配置问题

### Q1: 如何安装Sum2Slides？

**A:** 有三种安装方式：

```bash
# 方式1：通过ClawHub安装（推荐）
openclaw skill install sum2slides

# 方式2：通过pip安装
pip install sum2slides

# 方式3：从源码安装
通过 OpenClaw 安装技能
cd sum2slides
pip install -e .
```

### Q2: 安装后如何验证是否成功？

**A:** 运行版本检查命令：

```bash
sum2slides --version
# 应该显示：Sum2Slides v1.0.1
```

### Q3: 一键配置脚本在哪里？如何使用？

**A:** 一键配置脚本位于 `scripts/quick_setup.py`：

```bash
# 完整配置（推荐）
python scripts/quick_setup.py --all

# 只快速开始
python scripts/quick_setup.py --quick-start

# 检查依赖
python scripts/quick_setup.py --check-dependencies
```

### Q4: 配置文件在哪里？

**A:** 配置文件位置：

- **默认配置**: `config/default.yaml`
- **简化配置**: `config/simple.yaml`
- **用户配置**: `~/.config/sum2slides/config.yaml`

### Q5: 如何修改默认设置？

**A:** 有三种方式：

1. **编辑用户配置文件**：
```bash
# 编辑用户配置
vim ~/.config/sum2slides/config.yaml
```

2. **使用命令行参数**：
```bash
sum2slides --input text.txt --template business --theme light
```

3. **设置环境变量**：
```bash
export SUM2SLIDES_TEMPLATE=business
export SUM2SLIDES_THEME=light
```

### Q6: 如何更新到最新版本？

**A:**

```bash
# 通过pip更新
pip install --upgrade sum2slides

# 通过ClawHub更新
openclaw skill update sum2slides

# 从源码更新
cd sum2slides
git pull origin main
pip install -e .
```

---

## 💻 基本使用问题

### Q7: 如何快速生成一个演示文稿？

**A:** 使用简单的命令：

```bash
# 直接输入文本
sum2slides "项目总结：完成核心功能开发，通过测试验证" --output demo.pptx

# 从文件生成
sum2slides --input meeting.txt --output meeting.pptx
```

### Q8: 支持哪些输入格式？

**A:** 目前支持：

- ✅ 纯文本文件（`.txt`）
- ✅ Markdown文件（`.md`）
- ✅ 直接输入文本字符串

### Q9: 文本格式有什么要求？

**A:** 推荐的文本格式：

```
主标题

副标题或章节

• 项目1
• 项目2
• 项目3

1. 编号项目1
2. 编号项目2
3. 编号项目3
```

### Q10: 如何处理中文文本？

**A:** Sum2Slides完全支持中文，建议：

```bash
# 确保使用UTF-8编码
sum2slides --input chinese_text.txt --output chinese.pptx

# 在Python API中指定编码
converter = Sum2Slides()
with open("chinese.txt", "r", encoding="utf-8") as f:
    text = f.read()
presentation = converter.convert(text)
```

### Q11: 如何控制生成的幻灯片数量？

**A:** 使用 `--max-slides` 参数：

```bash
# 限制最大幻灯片数量为8张
sum2slides --input long_text.txt --max-slides 8 --output short.pptx
```

### Q12: 如何处理很长的文本？

**A:** 有几种方法：

1. **限制幻灯片数量**：
```bash
sum2slides --input long.txt --max-slides 10 --output short.pptx
```

2. **手动分割文本**：
```bash
# 将长文本分割为多个文件
sum2slides --input part1.txt --output part1.pptx
sum2slides --input part2.txt --output part2.pptx
```

3. **使用自动摘要功能**：
```python
converter = Sum2Slides(auto_summarize=True)
presentation = converter.convert(long_text)
```

---

## 🎨 模板和主题问题

### Q13: 有哪些可用的模板？

**A:** 内置模板：

- **default**: 默认模板，适用于通用场景
- **business**: 商务模板，适用于商务汇报
- **academic**: 学术模板，适用于学术报告

### Q14: 如何使用不同的模板？

**A:** 指定 `--template` 参数：

```bash
# 使用商务模板
sum2slides --input report.txt --template business --output report.pptx

# 使用学术模板
sum2slides --input paper.txt --template academic --output paper.pptx
```

### Q15: 有哪些可用的主题？

**A:** 内置主题：

- **light**: 浅色主题，适合明亮环境
- **dark**: 深色主题，适合暗光环境
- **colorful**: 彩色主题，适合创意展示

### Q16: 如何使用不同的主题？

**A:** 指定 `--theme` 参数：

```bash
# 使用浅色主题
sum2slides --input text.txt --theme light --output output.pptx

# 使用深色主题
sum2slides --input text.txt --theme dark --output output.pptx

# 使用彩色主题
sum2slides --input text.txt --theme colorful --output output.pptx
```

### Q17: 如何自定义模板？

**A:** 创建自定义模板的步骤：

1. **准备PPTX模板文件**：
   - 在PowerPoint中创建模板
   - 保存为 `my_template.pptx`

2. **配置模板**：
```yaml
# 在 config/templates.yaml 中添加
my_template:
  path: "templates/my_template.pptx"
  description: "我的自定义模板"
```

3. **使用自定义模板**：
```bash
sum2slides --input text.txt --template my_template --output output.pptx
```

### Q18: 如何调整字体大小？

**A:** 使用字体大小参数：

```bash
# 设置正文字体大小
sum2slides --input text.txt --font-size 16 --output output.pptx

# 设置标题字体大小
sum2slides --input text.txt --title-size 32 --output output.pptx
```

---

## 📄 输出和格式问题

### Q19: 生成的PPTX文件在哪里？

**A:** 默认情况下：

- 命令行指定：使用 `--output` 参数指定
- 未指定时：保存在当前目录，文件名基于输入文件

### Q20: 生成的文件能直接编辑吗？

**A:** 是的！生成的PPTX文件：

- ✅ 完全兼容Microsoft PowerPoint
- ✅ 可以继续编辑和修改
- ✅ 可以添加图片、图表等元素
- ✅ 支持所有PowerPoint功能

### Q21: 生成的文件能在其他软件中打开吗？

**A:** 是的，支持：

- ✅ Microsoft PowerPoint（推荐）
- ✅ LibreOffice Impress
- ✅ Google Slides（可能需要转换）
- ✅ Keynote（可能需要转换）

### Q22: 如何控制输出文件的大小？

**A:** 几种方法：

1. **限制幻灯片数量**：
```bash
sum2slides --input text.txt --max-slides 6 --output small.pptx
```

2. **使用更小的字体**：
```bash
sum2slides --input text.txt --font-size 14 --output compact.pptx
```

3. **减少文本内容**：精简输入文本

### Q23: 支持导出其他格式吗？

**A:** 当前版本主要支持：

- ✅ **PPTX格式**（主要支持，功能完整）
- ⏳ **PDF格式**（计划中）
- ⏳ **HTML格式**（计划中）
- ⏳ **图片格式**（计划中）

### Q24: 批量转换如何操作？

**A:** 有几种方法：

```bash
# 方法1：使用通配符
sum2slides --input *.txt --output-dir ./presentations

# 方法2：使用脚本
for file in *.txt; do
    sum2slides --input "$file" --output "${file%.txt}.pptx"
done

# 方法3：使用Python API批量处理
```

---

## 🔧 高级功能和配置问题

### Q25: 如何使用Python API？

**A:** 简单的API使用示例：

```python
from sum2slides import Sum2Slides

# 创建转换器
converter = Sum2Slides(
    template="business",
    theme="light",
    max_slides=10
)

# 转换文本
text = """项目总结
完成的工作：
1. 核心功能开发
2. 测试验证
3. 文档更新"""

presentation = converter.convert(text)
presentation.save("output.pptx")
```

### Q26: 如何设置环境变量？

**A:** 可设置以下环境变量：

```bash
# 默认模板
export SUM2SLIDES_TEMPLATE=business

# 默认主题
export SUM2SLIDES_THEME=light

# 输出目录
export SUM2SLIDES_OUTPUT_DIR=./presentations

# 日志级别
export SUM2SLIDES_LOG_LEVEL=INFO
```

### Q27: 如何启用日志记录？

**A:** 配置日志：

```bash
# 通过环境变量
export SUM2SLIDES_LOG_LEVEL=DEBUG

# 通过配置文件
logging:
  level: "DEBUG"
  file: "sum2slides.log"
```

### Q28: 如何集成到自动化脚本？

**A:** 创建自动化脚本：

```python
#!/usr/bin/env python3
from sum2slides import Sum2Slides
import os

def auto_generate_reports():
    """自动生成报告"""
    
    # 创建转换器
    converter = Sum2Slides(template="business")
    
    # 处理目录中的所有文本文件
    for filename in os.listdir("reports"):
        if filename.endswith(".txt"):
            with open(f"reports/{filename}", "r") as f:
                text = f.read()
            
            # 生成幻灯片
            presentation = converter.convert(text)
            output_name = filename.replace(".txt", ".pptx")
            presentation.save(f"presentations/{output_name}")
            
            print(f"✅ 生成: {output_name}")

if __name__ == "__main__":
    auto_generate_reports()
```

### Q29: 如何处理错误和异常？

**A:** 使用try-except处理错误：

```python
from sum2slides import Sum2Slides
from sum2slides.exceptions import ConversionError

try:
    converter = Sum2Slides()
    presentation = converter.convert("文本内容")
    presentation.save("output.pptx")
    
except ConversionError as e:
    print(f"转换错误: {e}")
except IOError as e:
    print(f"文件错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```

---

## 🆘 故障排除和错误处理

### Q30: 安装时提示依赖未找到怎么办？

**A:** 手动安装依赖：

```bash
# 安装所有依赖
pip install python-pptx markdown pydantic click pyyaml

# 验证安装
python -c "import pptx, markdown, pydantic, click, yaml"
```

### Q31: 运行时提示"找不到sum2slides命令"？

**A:** 检查安装和PATH：

```bash
# 检查是否安装
pip show sum2slides

# 手动添加到PATH（如果需要）
export PATH=$PATH:~/.local/bin

# 重新安装
pip uninstall sum2slides
pip install sum2slides
```

### Q32: 生成的幻灯片内容不正确怎么办？

**A:** 检查以下几点：

1. **文本格式**：确保使用正确的格式
2. **编码问题**：确认文件使用UTF-8编码
3. **模板配置**：检查模板是否正确
4. **日志信息**：查看日志了解详细错误

### Q33: 内存使用过高怎么办？

**A:** 优化配置：

```python
# 限制处理范围
converter = Sum2Slides(
    max_text_length=5000,   # 限制文本长度
    max_slides=10            # 限制幻灯片数量
)

# 或分批处理
def batch_process(long_text, chunk_size=5000):
    """分批处理长文本"""
    chunks = [long_text[i:i+chunk_size] for i in range(0, len(long_text), chunk_size)]
    
    for i, chunk in enumerate(chunks):
        presentation = converter.convert(chunk)
        presentation.save(f"output_{i}.pptx")
```

### Q34: 如何获取技术支持？

**A:** 多种获取帮助的方式：

1. **文档资源**：
   - [用户手册](USER_GUIDE.md)
   - [新手教程](TUTORIAL.md)
   - [API文档](API.md)

2. **社区支持**：
   - [GitHub Issues](本地化技能版本/issues)
   - [Discord社区](https://discord.gg/clawd)

3. **调试工具**：
```bash
# 启用调试模式
export SUM2SLIDES_LOG_LEVEL=DEBUG
sum2slides --input test.txt --output test.pptx

# 运行测试
python -m pytest
```

### Q35: 如何贡献代码或报告问题？

**A:** 参与贡献的方式：

1. **报告问题**：
   - 在GitHub创建Issue
   - 提供详细的问题描述
   - 包含错误信息和环境信息

2. **贡献代码**：
   - Fork项目仓库
   - 创建功能分支
   - 提交Pull Request
   - 详见 [CONTRIBUTING.md](CONTRIBUTING.md)

3. **改进文档**：
   - 修正文档错误
   - 添加使用示例
   - 翻译文档

---

## 💡 更多资源

### 📚 学习资源
- [新手教程](TUTORIAL.md) - 从零开始学习
- [使用演示](DEMO.md) - 查看实际效果
- [配置指南](CONFIG_GUIDE.md) - 详细配置说明

### 🛠️ 工具和脚本
- [一键配置脚本](scripts/quick_setup.py) - 快速设置
- [演示脚本](scripts/demo.py) - 功能演示
- [测试脚本](scripts/) - 功能测试

### 🤝 社区和支持
- **GitHub**: [本地化技能版本](本地化技能版本)
- **ClawHub**: [https://clawhub.ai/skills/sum2slides](https://clawhub.ai/skills/sum2slides)
- **Discord**: [https://discord.gg/clawd](https://discord.gg/clawd)

---

## 🎯 没有找到答案？

如果您的问题不在FAQ中，请：

1. **搜索文档**：使用关键词搜索相关文档
2. **查看Issues**：在GitHub搜索相关问题
3. **创建新Issue**：提供详细描述，我们会尽快回复

**感谢您使用Sum2Slides！** 🚀