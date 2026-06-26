# Sum2Slides 新手教程

## 🎯 欢迎使用Sum2Slides！

欢迎使用Sum2Slides v1.0.1！本教程将引导您从零开始，快速掌握如何将文本转换为专业的幻灯片演示文稿。

---

## 📚 教程大纲

### 第一课：快速入门（5分钟）
- 安装和配置
- 第一次转换
- 查看输出结果

### 第二课：基本使用（10分钟）
- 理解文本结构
- 使用模板和主题
- 自定义输出

### 第三课：进阶技巧（15分钟）
- 高级配置功能
- 批量处理
- 集成到工作流

---

## 🎓 第一课：快速入门

### 步骤1：安装Sum2Slides

#### 方法A：通过ClawHub安装（推荐）
```bash
# 使用OpenClaw技能管理器
openclaw skill install sum2slides
```

#### 方法B：通过pip安装
```bash
# 通过pip安装
pip install sum2slides
```

**安装验证**：
```bash
# 检查安装是否成功
sum2slides --version

# 应该显示：Sum2Slides v1.0.1
```

### 步骤2：快速配置

```bash
# 运行一键配置脚本
python scripts/quick_setup.py --all
```

这个命令会：
- ✅ 创建必要的配置目录
- ✅ 复制默认配置文件
- ✅ 创建输出目录
- ✅ 检查依赖安装
- ✅ 测试基本功能

### 步骤3：第一次转换

让我们用一个简单的例子来尝试：

```bash
# 方法1：命令行直接输入
sum2slides "项目总结：完成核心功能开发，通过测试验证，准备发布" --output my_first_slide.pptx
```

或者创建一个文本文件：

```bash
# 方法2：从文件转换
echo "项目总结
完成的工作：
1. 完成核心功能开发
2. 通过测试验证
3. 准备发布

下一步计划：
1. 功能扩展
2. 性能优化
3. 用户培训" > meeting.txt

sum2slides --input meeting.txt --output my_first_slide.pptx
```

### 步骤4：查看输出结果

**打开生成的文件**：
- 使用Microsoft PowerPoint打开`my_first_slide.pptx`
- 或使用LibreOffice Impress
- 或在线的PowerPoint查看器

**你应该看到**：
- 📄 标题幻灯片：显示"项目总结"
- 📄 内容幻灯片：显示"完成的工作"
- 📄 内容幻灯片：显示"下一步计划"

### 🎉 恭喜！你完成了第一次转换！

---

## 📖 第二课：基本使用

### 理解文本结构

Sum2Slides通过分析文本结构来生成幻灯片。了解如何组织文本很重要：

#### 基本文本格式

**标题格式**：
```
主标题
```

**段落格式**：
```
主标题

这是段落内容，会自动分页到合适的位置。
```

**列表格式**：
```
主标题

• 项目1
• 项目2
• 项目3

1. 编号项目1
2. 编号项目2
3. 编号项目3
```

**多段文本**：
```
主标题

第一部分内容
• 要点1
• 要点2

第二部分内容
• 要点1
• 要点2

总结部分
总结内容...
```

#### Markdown格式（推荐）

```markdown
# 主标题

## 副标题

内容描述...

- 列表项目1
- 列表项目2

### 小标题

更多内容...
```

### 使用模板和主题

#### 模板选择

```bash
# 使用默认模板
sum2slides --input text.txt --output output.pptx

# 使用商务模板
sum2slides --input text.txt --template business --output output.pptx

# 使用学术模板
sum2slides --input text.txt --template academic --output output.pptx
```

#### 主题选择

```bash
# 使用浅色主题（适合明亮环境）
sum2slides --input text.txt --theme light --output output.pptx

# 使用深色主题（适合暗光环境）
sum2slides --input text.txt --theme dark --output output.pptx

# 使用彩色主题（适合创意展示）
sum2slides --input text.txt --theme colorful --output output.pptx
```

### 自定义输出

#### 配置字体大小

```bash
# 设置正文字体大小
sum2slides --input text.txt --font-size 16 --output output.pptx

# 设置标题字体大小
sum2slides --input text.txt --title-size 32 --output output.pptx
```

#### 控制幻灯片数量

```bash
# 限制最大幻灯片数量
sum2slides --input text.txt --max-slides 8 --output output.pptx
```

#### 指定输出目录

```bash
# 指定输出目录
sum2slides --input text.txt --output-dir ./presentations --output output.pptx
```

### 💡 实战练习

创建一个实际的会议纪要文件：

```bash
cat << 'EOF' > meeting_notes.txt
周会纪要 2026-03-29

会议主题：项目进度评审
主持人：张经理
参会人员：开发团队全体成员

本周完成工作：

1. 功能开发
   - 完成用户认证模块
   - 实现数据导入功能
   - 优化界面响应速度

2. 质量保证
   - 修复3个重要bug
   - 完成单元测试
   - 通过集成测试

3. 文档更新
   - 更新API文档
   - 编写用户手册
   - 完善开发文档

下周工作计划：

1. 新功能开发
   - 开发报表功能
   - 实现数据导出
   - 添加消息通知

2. 性能优化
   - 优化数据库查询
   - 减少内存占用
   - 提升响应速度

3. 准备发布
   - 完成最终测试
   - 准备发布材料
   - 安排用户培训

风险和问题：

1. 技术风险：无重大技术风险
2. 资源需求：需要增加测试资源
3. 时间安排：建议增加2天缓冲时间

下一步行动：
1. 按计划执行下周工作
2. 密切跟踪进度
3. 及时协调资源
EOF
```

**转换为幻灯片**：
```bash
sum2slides --input meeting_notes.txt --template business --theme light --max-slides 8 --output weekly_meeting.pptx
```

---

## 🔧 第三课：进阶技巧

### 高级配置功能

#### 使用配置文件

创建自定义配置文件 `my_config.yaml`：

```yaml
quick_start:
  enabled: true
  template: "business"
  theme: "light"
  max_slides: 10
  font_size: 16
  title_size: 32
  output_dir: "./presentations"
```

**使用配置文件**：
```bash
sum2slides --config my_config.yaml --input text.txt --output output.pptx
```

#### 环境变量配置

```bash
# 设置默认模板
export SUM2SLIDES_TEMPLATE=business

# 设置默认主题
export SUM2SLIDES_THEME=light

# 设置输出目录
export SUM2SLIDES_OUTPUT_DIR=./presentations

# 现在可以直接运行
sum2slides --input text.txt --output output.pptx
```

### 批量处理

#### 批量转换多个文件

```bash
# 创建脚本批量转换
cat << 'EOF' > batch_convert.sh
#!/bin/bash

# 输入目录
input_dir="./texts"
# 输出目录  
output_dir="./presentations"

# 确保输出目录存在
mkdir -p "$output_dir"

# 批量转换
for file in "$input_dir"/*.txt; do
    filename=$(basename "$file" .txt)
    echo "转换: $file -> $filename.pptx"
    
    sum2slides --input "$file" --template business --theme light --output "$output_dir/$filename.pptx"
done

echo "批量转换完成！"
EOF

chmod +x batch_convert.sh
./batch_convert.sh
```

#### 使用通配符

```bash
# 转换所有.txt文件
sum2slides --input *.txt --output-dir ./presentations

# 转换所有.md文件
sum2slides --input *.md --template academic --output-dir ./academic_presentations
```

### 集成到工作流

#### Python API集成

创建自动化脚本 `auto_generate.py`：

```python
#!/usr/bin/env python3
from sum2slides import Sum2Slides
import os
import datetime

# 创建转换器
converter = Sum2Slides(
    template="business",
    theme="light",
    max_slides=8,
    output_dir="./auto_presentations"
)

def generate_weekly_report():
    """自动生成本周报告"""
    
    # 读取周报数据
    with open("weekly_data.txt", "r", encoding="utf-8") as f:
        text = f.read()
    
    # 生成文件名（包含日期）
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    output_file = f"weekly_report_{date_str}.pptx"
    
    # 转换文本
    presentation = converter.convert(text)
    presentation.save(f"./auto_presentations/{output_file}")
    
    print(f"✅ 周报已生成: {output_file}")

def generate_meeting_slides(meeting_notes):
    """生成会议幻灯片"""
    
    presentation = converter.convert(meeting_notes)
    output_file = f"meeting_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pptx"
    presentation.save(f"./auto_presentations/{output_file}")
    
    print(f"✅ 会议幻灯片已生成: {output_file}")

# 运行自动化任务
if __name__ == "__main__":
    generate_weekly_report()
```

#### 定时任务

```bash
# 添加到crontab，每周一早上9点自动生成周报
# 0 9 * * 1 cd /path/to/project && python auto_generate.py
```

### 🎯 最佳实践

1. **文本组织**：
   - 使用清晰的标题层次
   - 每张幻灯片内容不要超过300字
   - 使用项目符号和编号列表

2. **模板选择**：
   - 商务汇报 → business模板
   - 学术报告 → academic模板
   - 技术分享 → default模板

3. **主题选择**：
   - 明亮环境 → light主题
   - 暗光环境 → dark主题
   - 创意展示 → colorful主题

4. **输出优化**：
   - 控制幻灯片数量（6-12张最佳）
   - 使用合适的字体大小（14-18pt）
   - 定期测试不同配置效果

---

## 🆘 需要帮助？

### 常见问题
查看 [FAQ.md](FAQ.md) 获取常见问题解答。

### 文档资源
- [用户手册](USER_GUIDE.md) - 详细使用说明
- [API文档](API.md) - 完整API参考
- [配置指南](CONFIG_GUIDE.md) - 配置选项详解

### 社区支持
- [GitHub Issues](本地化技能版本/issues)
- [Discord社区](https://discord.gg/clawd)

---

## 🎉 恭喜完成教程！

你现在应该能够：
- ✅ 安装和配置Sum2Slides
- ✅ 基本文本转换
- ✅ 使用模板和主题
- ✅ 自定义输出配置
- ✅ 批量处理文件
- ✅ 集成到工作流

**下一步**：
1. 运行演示脚本查看更多示例
2. 查看完整文档了解高级功能
3. 开始在实际项目中使用Sum2Slides

**祝你使用愉快！** 🚀