#!/usr/bin/env python3
"""
Sum2Slides v1.0.1 演示幻灯片生成 - 简化版本
创建展示Sum2Slides使用方法的演示幻灯片
"""

import os
import sys
from datetime import datetime

def create_demo_content():
    """创建演示内容"""
    
    demo_content = f"""# Sum2Slides v1.0.1
## 🎉 正式版本演示

**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**版本**: Sum2Slides v1.0.1

---

## 📋 目录
1. 简介
2. 安装
3. 使用
4. 功能
5. 场景
6. 资源

---

## 1️⃣ 简介

### 什么是Sum2Slides？
- 🚀 文本转幻灯片工具
- 🎯 自动生成专业演示文稿
- 📊 支持PPTX格式输出

### 核心价值
- ✅ 节省时间
- ✅ 保持一致性
- ✅ 提高质量

---

## 2️⃣ 安装

### 推荐方式
```bash
openclaw skill install sum2slides
```

### 其他方式
```bash
pip install sum2slides
```

### 验证安装
```bash
sum2slides --version
```

---

## 3️⃣ 使用

### 命令行
```bash
sum2slides "你的文本" --output demo.pptx
```

### Python API
```python
from sum2slides import Sum2Slides
converter = Sum2Slides()
presentation = converter.convert("文本内容")
presentation.save("output.pptx")
```

---

## 4️⃣ 功能

### 模板
- 默认模板
- 商务模板
- 学术模板

### 主题
- 浅色主题
- 深色主题
- 彩色主题

### 配置
- 字体大小
- 颜色方案
- 布局选项

---

## 5️⃣ 使用场景

### 会议纪要
```bash
sum2slides --input meeting.txt --output meeting.pptx
```

### 项目报告
```bash
sum2slides --input report.md --template business --output report.pptx
```

### 学术汇报
```bash
sum2slides --input paper.md --template academic --output paper.pptx
```

---

## 6️⃣ 资源

### 文档
- 用户手册: README.md
- 新手教程: TUTORIAL.md
- 常见问题: FAQ.md

### 社区
- 本地化版本
- Issues: 本地化技能版本/issues
- Discord: https://discord.gg/clawd

---

## 🎉 感谢使用！

### 下一步
1. 安装: openclaw skill install sum2slides
2. 试用: sum2slides "测试" --output test.pptx
3. 学习: 阅读TUTORIAL.md

**Happy Presenting!** 🚀
"""
    
    return demo_content

def create_demo_files():
    """创建演示文件"""
    
    # 创建输出目录
    os.makedirs("demo", exist_ok=True)
    
    # 创建演示内容文件
    demo_content = create_demo_content()
    demo_file = "demo/sum2slides_demo_content.txt"
    
    with open(demo_file, "w", encoding="utf-8") as f:
        f.write(demo_content)
    
    print(f"✅ 演示内容已保存: {demo_file}")
    print(f"📝 内容长度: {len(demo_content)} 字符")
    
    # 创建使用说明
    instruction = f"""# Sum2Slides v1.0.1 演示使用说明

## 如何生成演示幻灯片

### 方法1：直接生成（需安装sum2slides）
```bash
# 确保已安装
openclaw skill install sum2slides

# 生成演示幻灯片
sum2slides --input demo/sum2slides_demo_content.txt --template business --theme colorful --output demo/sum2slides_demo.pptx
```

### 方法2：手动生成（无sum2slides）
如果您还没有安装sum2slides，可以使用以下步骤：

1. **安装依赖**:
```bash
pip install python-pptx markdown pydantic click pyyaml
```

2. **从源码安装sum2slides**:
```bash
cd {os.getcwd()}
pip install -e .
```

3. **运行演示**:
```python
from sum2slides import Sum2Slides

with open("demo/sum2slides_demo_content.txt", "r") as f:
    content = f.read()

converter = Sum2Slides(template="business", theme="colorful")
presentation = converter.convert(content)
presentation.save("demo/sum2slides_demo.pptx")
```

## 演示内容结构

1. **简介** - Sum2Slides基本介绍
2. **安装** - 3种安装方式
3. **使用** - 命令行和Python API
4. **功能** - 模板、主题、配置
5. **场景** - 实际使用案例
6. **资源** - 文档和社区链接

## 自定义演示

要自定义演示内容：
1. 编辑 `demo/sum2slides_demo_content.txt`
2. 修改文本内容
3. 重新运行生成命令

## 演示用途

生成的演示幻灯片可以用于：
1. 产品介绍和演示
2. 团队培训和分享
3. 技术文档和教程
4. 社区展示和推广

## 问题解决

如果遇到问题：
1. 检查sum2slides是否安装成功
2. 查看README.md中的安装说明
3. 参考FAQ.md中的常见问题
4. 在GitHub Issues中搜索解决方案

## 联系和支持

- **GitHub**: 本地化技能版本
- **Issues**: 本地化技能版本/issues
- **Discord**: https://discord.gg/clawd

**感谢使用Sum2Slides v1.0.1！** 🚀
"""
    
    # 保存使用说明
    instruction_file = "demo/demo_instructions.md"
    with open(instruction_file, "w", encoding="utf-8") as f:
        f.write(instruction)
    
    print(f"✅ 使用说明已保存: {instruction_file}")
    
    return True

def main():
    """主函数"""
    
    print("🎬 Sum2Slides v1.0.1 演示材料生成")
    print("=" * 50)
    
    # 创建演示文件
    success = create_demo_files()
    
    if success:
        print("\n✅ 演示材料生成完成！")
        print("\n📁 生成的文件:")
        print("  ✅ demo/sum2slides_demo_content.txt - 演示内容文本")
        print("  ✅ demo/demo_instructions.md - 使用说明")
        
        print("\n🎯 下一步:")
        print("1. 安装sum2slides: openclaw skill install sum2slides")
        print("2. 生成幻灯片: 按照demo_instructions.md的说明")
        print("3. 查看演示: 打开生成的PPTX文件")
        print("4. 学习更多: 阅读TUTORIAL.md")
        
        print("\n📊 演示内容摘要:")
        print(f"   - 章节: 6个主要部分")
        print(f"   - 代码示例: 命令行和Python API")
        print(f"   - 使用场景: 会议、报告、学术")
        print(f"   - 资源链接: GitHub、文档、社区")
    else:
        print("❌ 演示材料生成失败")
    
    print("\n🚀 演示准备完成！")

if __name__ == "__main__":
    main()