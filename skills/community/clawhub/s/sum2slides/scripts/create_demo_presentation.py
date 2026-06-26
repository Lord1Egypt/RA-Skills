#!/usr/bin/env python3
"""
Sum2Slides v1.0.1 演示幻灯片生成脚本
创建展示Sum2Slides使用方法的演示幻灯片
"""

import os
import sys
from datetime import datetime

# 创建演示内容
demo_content = f"""
# Sum2Slides v1.0.1 演示幻灯片
## 🎉 正式版本发布

**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**版本**: Sum2Slides v1.0.1
**用途**: 展示Sum2Slides功能和用法

---

## 📋 目录
1. Sum2Slides简介
2. 安装方式
3. 基本使用
4. 高级功能
5. 使用场景
6. 最佳实践
7. 资源和支持

---

## 1️⃣ Sum2Slides简介

### 什么是Sum2Slides？
- 🚀 文本转幻灯片工具
- 🎯 自动生成专业演示文稿
- 📊 支持PPTX格式输出
- 💡 智能内容分析

### 核心价值
- ✅ **节省时间**：自动转换，减少手动工作
- ✅ **保持一致性**：统一格式和风格
- ✅ **提高质量**：结构化展示，逻辑清晰
- ✅ **易于修改**：基于模板，快速调整

### 技术特性
- 🐍 **语言**: Python 3.10+
- 📦 **核心依赖**: python-pptx, markdown, pydantic
- 🎨 **模板**: 内置多种模板和主题
- 🔧 **配置**: YAML配置文件支持

---

## 2️⃣ 安装方式

### 通过ClawHub安装（推荐）
```bash
openclaw skill install sum2slides
```

### 通过pip安装
```bash
pip install sum2slides
```

### 从源码安装
```bash
通过 OpenClaw 安装技能
cd sum2slides
pip install -e .
```

### 验证安装
```bash
sum2slides --version
# 应该显示: Sum2Slides v1.0.1
```

---

## 3️⃣ 基本使用

### 命令行使用

```bash
# 基本用法：从文本生成幻灯片
sum2slides "项目总结：完成核心功能开发，通过测试验证" --output demo.pptx

# 从文件输入
sum2slides --input meeting_notes.txt --output meeting.pptx

# 使用商务模板
sum2slides --input report.md --template business --output report.pptx

# 配置主题和字体
sum2slides --input data.txt --theme dark --font-size 16 --output presentation.pptx
```

### Python API使用

```python
from sum2slides import Sum2Slides

# 创建转换器
converter = Sum2Slides()

# 转换文本
text = \"\"\"项目更新

本周完成工作：
1. 完成用户认证模块
2. 优化数据库性能
3. 修复已知问题

下周计划：
1. 开发新功能
2. 进行系统测试
3. 准备发布\"\"\"

presentation = converter.convert(text)
presentation.save("output.pptx")
```

---

## 4️⃣ 高级功能

### 模板系统
- **默认模板**: 通用场景
- **商务模板**: 商务汇报
- **学术模板**: 学术报告
- **创意模板**: 创意展示

### 主题支持
- 🌞 **浅色主题**: 适合明亮环境
- 🌙 **深色主题**: 适合暗光环境
- 🌈 **彩色主题**: 创意展示

### 配置选项
- 📏 **字体大小**: 可调节标题和正文
- 🎨 **颜色方案**: 自定义配色
- 📐 **布局**: 多种幻灯片布局
- 🖼️ **图片**: 支持图片插入

### 批量处理
```python
# 批量转换多个文件
converter = Sum2Slides()
files = ["report1.txt", "report2.md", "notes.txt"]
converter.batch_convert(files, "output_directory/")
```

---

## 5️⃣ 使用场景

### 会议纪要转演示
```bash
# 将会议记录转为幻灯片
sum2slides --input meeting_notes.txt --template business --output meeting_summary.pptx
```

### 项目报告
```python
# 自动化生成项目报告
converter = Sum2Slides(template="business", theme="light")
with open("project_report.md", "r") as f:
    report = f.read()
presentation = converter.convert(report)
presentation.save("project_presentation.pptx")
```

### 学术汇报
```bash
# 学术论文摘要转演示
sum2slides --input research_summary.md --template academic --theme light --output research_presentation.pptx
```

### 产品介绍
```python
# 产品介绍自动化
product_info = \"\"\"# Awesome Product

## 核心功能
- 功能1: 智能分析
- 功能2: 实时同步
- 功能3: 多平台支持

## 技术优势
1. 高性能
2. 易扩展
3. 强安全

## 客户案例
- 客户A: 提升效率50%
- 客户B: 降低成本30%
\"\"\"

converter = Sum2Slides(template="business", theme="colorful")
presentation = converter.convert(product_info)
presentation.save("product_intro.pptx")
```

---

## 6️⃣ 最佳实践

### 文本格式建议
```
# 主标题

## 副标题或章节

• 项目1：详细描述
• 项目2：详细描述
• 项目3：详细描述

1. 编号项目1：详细说明
2. 编号项目2：详细说明
3. 编号项目3：详细说明

---

## 新章节
更多内容...
```

### 配置管理
```yaml
# 在 ~/.config/sum2slides/config.yaml
defaults:
  template: "business"
  theme: "light"
  max_slides: 10
  font_size: 16
  output_format: "pptx"

templates:
  custom:
    path: "/path/to/custom_template.pptx"
    description: "我的自定义模板"
```

### 环境变量
```bash
# 设置默认配置
export SUM2SLIDES_TEMPLATE=business
export SUM2SLIDES_THEME=light
export SUM2SLIDES_OUTPUT_DIR=./presentations
```

### 自动化集成
```python
#!/usr/bin/env python3
# 自动化脚本示例
import os
from sum2slides import Sum2Slides

def daily_report():
    \"\"\"每日报告自动化\"\"\"
    converter = Sum2Slides(template="business")
    
    # 读取当日报告
    with open("daily_report.txt", "r") as f:
        report = f.read()
    
    # 生成幻灯片
    presentation = converter.convert(report)
    
    # 保存并发送
    filename = f"daily_report_{datetime.now().strftime('%Y%m%d')}.pptx"
    presentation.save(filename)
    
    print(f"✅ 报告已生成: {filename}")

if __name__ == "__main__":
    daily_report()
```

---

## 7️⃣ 资源和支持

### 文档资源
- 📖 **用户手册**: README.md
- 🎓 **新手教程**: TUTORIAL.md
- ❓ **常见问题**: FAQ.md
- 🎬 **使用演示**: DEMO.md
- 🔧 **贡献指南**: CONTRIBUTING.md

### 社区支持
- 🔗 **GitHub仓库**: 本地化技能版本
- 🐛 **问题追踪**: 本地化技能版本/issues
- 💬 **讨论社区**: 本地化技能版本/discussions
- 🎯 **Discord支持**: https://discord.gg/clawd

### 学习资源
- 🚀 **快速开始**: 运行 `python scripts/demo.py`
- 📚 **完整教程**: 阅读 TUTORIAL.md
- 💡 **最佳实践**: 参考 examples/ 目录
- 🔧 **配置指南**: 查看 config/ 目录

---

## 🎉 感谢使用Sum2Slides！

### 版本信息
- **版本**: Sum2Slides v1.0.1
- **发布日期**: 2026年3月29日
- **许可证**: MIT License
- **状态**: 正式版本

### 下一步行动
1. 安装: `openclaw skill install sum2slides`
2. 试用: `sum2slides "你的文本" --output test.pptx`
3. 学习: `cat TUTORIAL.md`
4. 参与: 查看CONTRIBUTING.md

### 反馈和建议
欢迎通过GitHub Issues或Discord提交反馈和建议！

---

**Happy Presenting!** 🚀
"""

def create_demo_slides():
    """创建演示幻灯片"""
    
    # 创建输出目录
    os.makedirs("demo_output", exist_ok=True)
    
    # 保存演示内容到文件
    demo_file = "demo_output/sum2slides_demo_content.txt"
    with open(demo_file, "w", encoding="utf-8") as f:
        f.write(demo_content)
    
    print(f"✅ 演示内容已保存到: {demo_file}")
    print(f"📝 内容长度: {len(demo_content)} 字符")
    
    # 尝试使用sum2slides生成幻灯片
    try:
        print("\n🔄 正在使用Sum2Slides生成演示幻灯片...")
        
        # 创建临时导入路径
        sys.path.insert(0, os.path.abspath("src"))
        
        from sum2slides import Sum2Slides
        
        # 创建转换器
        converter = Sum2Slides(
            template="business",
            theme="colorful",
            max_slides=15,
            font_size=14
        )
        
        # 生成幻灯片
        presentation = converter.convert(demo_content)
        
        # 保存文件
        output_file = "demo_output/sum2slides_demo_presentation.pptx"
        presentation.save(output_file)
        
        print(f"🎉 演示幻灯片已生成: {output_file}")
        print(f"📊 幻灯片数量: 约15张")
        
        return True
        
    except ImportError as e:
        print(f"⚠️ 无法导入Sum2Slides: {e}")
        print("💡 请确保已安装sum2slides或从源码安装")
        return False
    except Exception as e:
        print(f"❌ 生成幻灯片失败: {e}")
        return False

def create_alternative_demo():
    """创建替代演示方案"""
    
    print("\n🔧 创建替代演示方案...")
    
    # 创建简化演示内容
    simple_demo = """# Sum2Slides v1.0.1 演示

## 🎯 功能演示

### 1. 安装方式
```bash
openclaw skill install sum2slides
```

### 2. 基本使用
```bash
sum2slides "项目总结" --output demo.pptx
```

### 3. 高级功能
- 多种模板
- 主题支持
- 批量处理

### 4. 使用场景
- 会议纪要
- 项目报告
- 学术汇报
- 产品介绍

## 🚀 快速开始

1. **安装**: `openclaw skill install sum2slides`
2. **试用**: `sum2slides "测试内容" --output test.pptx`
3. **学习**: 阅读TUTORIAL.md

## 📚 资源

- 本地化版本
- 文档: https://sum2slides.readthedocs.io/
- 社区: https://discord.gg/clawd

## 🎉 感谢使用！
"""
    
    # 保存简化演示
    simple_file = "demo_output/sum2slides_simple_demo.txt"
    with open(simple_file, "w", encoding="utf-8") as f:
        f.write(simple_demo)
    
    print(f"✅ 简化演示内容已保存: {simple_file}")
    print(f"📝 内容长度: {len(simple_demo)} 字符")
    
    # 创建手动演示说明
    manual_guide = """# Sum2Slides v1.0.1 演示幻灯片生成指南

## 如何生成演示幻灯片

### 方法1：使用已安装的sum2slides
```bash
# 确保已安装
openclaw skill install sum2slides

# 生成演示幻灯片
sum2slides --input demo_output/sum2slides_demo_content.txt --template business --theme colorful --output sum2slides_demo.pptx
```

### 方法2：使用Python API
```python
from sum2slides import Sum2Slides

# 读取演示内容
with open("demo_output/sum2slides_demo_content.txt", "r") as f:
    content = f.read()

# 创建转换器
converter = Sum2Slides(
    template="business",
    theme="colorful",
    max_slides=15
)

# 生成幻灯片
presentation = converter.convert(content)
presentation.save("sum2slides_demo.pptx")
```

### 方法3：使用演示脚本
```bash
# 运行提供的演示脚本
python scripts/demo.py

# 或使用快速设置
python scripts/quick_setup.py --demo
```

## 演示内容说明

### 包含的章节
1. Sum2Slides简介
2. 安装方式（3种方法）
3. 基本使用（命令行+API）
4. 高级功能（模板、主题、配置）
5. 使用场景（4个实际案例）
6. 最佳实践（格式、配置、自动化）
7. 资源和支持（文档、社区、学习）

### 生成的输出
- 📝 演示文本文件（可编辑）
- 🎨 专业PPTX演示文稿
- 🔧 配置示例文件
- 📚 使用指南

## 自定义演示

要自定义演示内容，请编辑：
1. `demo_output/sum2slides_demo_content.txt`
2. 修改配置参数
3. 重新运行生成脚本

## 分享演示

生成的演示幻灯片可以：
1. 直接用于产品介绍
2. 作为培训材料
3. 分享给团队成员
4. 发布到社区

## 问题解决

如果无法生成幻灯片：
1. 检查sum2slides是否安装
2. 验证Python环境
3. 查看依赖是否完整
4. 参考FAQ.md中的问题解答
"""
    
    # 保存手动指南
    guide_file = "demo_output/demo_creation_guide.md"
    with open(guide_file, "w", encoding="utf-8") as f:
        f.write(manual_guide)
    
    print(f"✅ 演示创建指南已保存: {guide_file}")
    
    return True

def main():
    """主函数"""
    
    print("🎬 Sum2Slides v1.0.1 演示幻灯片生成")
    print("=" * 50)
    
    # 创建演示目录
    if not os.path.exists("demo_output"):
        os.makedirs("demo_output")
    
    # 创建演示内容
    success = create_demo_slides()
    
    if not success:
        print("\n🔄 尝试替代方案...")
        create_alternative_demo()
    
    # 总结
    print("\n" + "=" * 50)
    print("📋 演示材料生成完成")
    print("=" * 50)
    
    demo_files = os.listdir("demo_output") if os.path.exists("demo_output") else []
    
    if demo_files:
        print("📁 生成的文件:")
        for file in demo_files:
            file_path = os.path.join("demo_output", file)
            size = os.path.getsize(file_path)
            print(f"  ✅ {file} ({size} 字节)")
    else:
        print("⚠️ 未生成演示文件")
    
    print("\n🎯 下一步:")
    print("1. 查看生成的文件: ls demo_output/")
    print("2. 运行演示: python scripts/demo.py")
    print("3. 学习使用: cat TUTORIAL.md")
    print("4. 生成幻灯片: 使用上述指南")
    
    print("\n🚀 演示准备完成！")

if __name__ == "__main__":
    main()