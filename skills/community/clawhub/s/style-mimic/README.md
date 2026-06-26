# style-mimic 技能使用指南

## 技能简介

**style-mimic** 是一个帮助用户模仿社会洞察类文章风格进行写作的AI助手。它提供了完整的写作方法论、模板系统和辅助工具，帮助您创作出既有深度又有影响力的文章。

## 核心功能

### 1. 模板系统
- **5种专业模板**: 分析文、评论文、报告文、故事文、访谈文
- **结构化指导**: 每步写作的具体指导
- **风格要点**: 每种文体的风格特征

### 2. 写作助手
- **开头生成**: 根据主题生成合适的文章开头
- **结尾建议**: 提供升华收束的结尾建议
- **结构规划**: 帮助规划文章整体结构
- **常用句式**: 提供典型的社会洞察类句式

### 3. 风格检测
- **特征分析**: 分析文本的9个风格特征
- **匹配度评分**: 给出总体风格匹配度
- **改进建议**: 针对不足提供具体改进建议

## 快速开始

### 安装依赖
```bash
# 确保有Python3环境
python3 --version

# 安装必要依赖（如果需要）
pip3 install -r requirements.txt
```

### 基本使用

#### 使用写作助手
```bash
# 列出所有模板
python3 scripts/writing_assistant.py --list-templates

# 生成文章开头
python3 scripts/writing_assistant.py --topic "数字化转型" --type analysis --action opening

# 生成文章结构
python3 scripts/writing_assistant.py --topic "知识焦虑" --type analysis --action structure

# 获取常用句式
python3 scripts/writing_assistant.py --action phrase
```

#### 使用风格检测
```bash
# 分析文本文件
python3 scripts/style_analyzer.py --file your_article.txt

# 分析直接输入的文本
python3 scripts/style_analyzer.py --text "你的文章内容..."

# 简要输出
python3 scripts/style_analyzer.py --file your_article.txt --output brief
```

## 详细使用指南

### 1. 选择模板
根据写作目的选择合适的模板：

| 文章类型 | 适用场景 | 模板文件 |
|----------|----------|----------|
| **分析文** | 深度分析复杂问题 | `templates/analysis-template.md` |
| **评论文** | 评论热点事件现象 | `templates/commentary-template.md` |
| **报告文** | 撰写研究报告总结 | `templates/report-template.md` |
| **故事文** | 叙述人物经历故事 | `templates/story-template.md` |
| **访谈文** | 整理对话访谈内容 | `templates/interview-template.md` |

### 2. 按模板写作
1. 打开对应的模板文件
2. 按照模板的结构逐步写作
3. 替换`[ ]`中的占位符为具体内容
4. 注意保持风格特征

### 3. 使用助手优化
```bash
# 生成开头和结尾
python3 scripts/writing_assistant.py --topic "你的主题" --action opening
python3 scripts/writing_assistant.py --topic "你的主题" --action closing

# 检查风格
python3 scripts/style_analyzer.py --file 你的文章.md

# 根据建议改进
# 重新运行风格检测，直到满意
```

## 风格特征详解

### 核心特征
1. **结构化思维** - 使用框架、坐标系分析问题
2. **概念创新** - 创造新概念准确定义现象
3. **二元对立** - 通过对比揭示本质
4. **系统视角** - 从宏观把握微观

### 论证方式
1. **先立后破** - 先承认合理性，再指出问题
2. **层层递进** - 现象→原因→影响→解决方案
3. **数据支撑** - 关键观点要有数据支持
4. **案例引用** - 用具体案例让抽象变具体

### 语言风格
1. **术语化但不晦涩** - 专业但易懂
2. **短句有力** - 增强节奏感和力量感
3. **排比结构** - 增强气势和记忆点
4. **金句收尾** - 每节结尾有记忆点

## 示例学习

### 完整示例
查看 `examples/full-demo.md`，这是一个完整的写作示例，展示了：
- 完整的文章结构
- 风格特征的运用
- 论证技巧的体现
- 语言风格的把握

### 分步学习
1. 先阅读 `references/style-guide.md` 了解风格特征
2. 查看 `examples/full-demo.md` 学习完整写作
3. 选择模板开始实践
4. 使用工具检测和改进

## 常见问题

### Q: 如何判断文章是否符合风格？
A: 使用 `style_analyzer.py` 工具进行检测，得分超过0.7为优秀。

### Q: 模板太死板怎么办？
A: 模板是指导不是束缚，可以根据需要调整。关键是保持核心风格特征。

### Q: 如何提高风格匹配度？
A: 多使用典型句式、加强结构化表达、增加数据案例、注意批判与建设的平衡。

### Q: 适合什么类型的文章？
A: 适合需要深度分析、理性批判、建设性建议的社会洞察类文章。

## 进阶技巧

### 1. 概念创新技巧
- 观察新现象，创造新概念
- 用简单语言解释复杂概念
- 概念要能准确描述现象本质

### 2. 框架构建技巧
- 建立简单的分析框架（如2×2矩阵）
- 框架要能涵盖主要维度
- 用框架组织分析内容

### 3. 数据运用技巧
- 关键数据要具体准确
- 数据要有来源和时效性
- 用数据支撑核心观点

### 4. 案例选择技巧
- 案例要有代表性
- 案例要具体生动
- 案例要能说明问题

## 更新日志

### v1.0.0 (2026-04-01)
- 初始版本发布
- 5种专业写作模板
- 写作助手工具
- 风格检测工具
- 完整示例和指南

## 技术支持

如有问题或建议：
1. 查看详细文档
2. 参考完整示例
3. 实践练习改进

---

**开始你的社会洞察写作之旅吧！**