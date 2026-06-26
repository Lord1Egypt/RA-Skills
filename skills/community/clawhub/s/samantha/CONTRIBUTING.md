# 贡献指南 | Contributing Guide

感谢您对Samantha项目的关注！我们欢迎所有形式的贡献。

## 🎯 如何贡献 | How to Contribute

### 1. **报告问题 | Reporting Issues**
- 使用GitHub Issues报告bug或提出功能建议
- 提供详细的问题描述、复现步骤和期望结果
- 如果是bug，请提供环境信息和错误日志

### 2. **提交代码 | Submitting Code**
1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### 3. **编写文档 | Writing Documentation**
- 完善现有文档
- 添加使用教程
- 翻译文档到其他语言
- 编写技术博客或案例研究

### 4. **设计贡献 | Design Contributions**
- UI/UX设计改进
- 图标和视觉元素
- 交互设计优化
- 用户体验研究

## 📋 开发规范 | Development Standards

### **代码规范 | Code Standards**
- 遵循PEP 8 (Python)或相应语言的编码规范
- 添加有意义的注释
- 编写单元测试
- 保持代码简洁可读

### **提交信息 | Commit Messages**
- 使用英文提交信息
- 遵循Conventional Commits规范
- 简要描述更改内容
- 关联Issue编号（如适用）

### **测试要求 | Testing Requirements**
- 新功能必须包含测试用例
- 确保现有测试通过
- 测试覆盖率不低于80%
- 集成测试和单元测试并重

## 🏗️ 项目结构 | Project Structure

```
samantha/
├── src/                    # 源代码
│   ├── core/              # 核心引擎
│   ├── memory/            # 记忆系统
│   ├── emotion/           # 情感模块
│   ├── mbti/              # MBTI分析
│   └── voice/             # 语音集成
├── tests/                 # 测试代码
├── docs/                  # 文档
├── examples/              # 使用示例
└── tools/                 # 开发工具
```

## 🔧 开发环境设置 | Development Environment Setup

### **Python环境 | Python Environment**
```bash
# 克隆仓库
git clone https://github.com/leilei926524-tech/samantha.git
cd samantha

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### **数据库设置 | Database Setup**
```bash
# 初始化数据库
python scripts/init_db.py

# 运行迁移（如有）
python scripts/migrate.py
```

### **运行测试 | Running Tests**
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_core.py

# 生成测试覆盖率报告
pytest --cov=src tests/
```

## 🎨 设计原则 | Design Principles

### **情感优先 | Emotion First**
- 所有功能设计都要考虑情感影响
- 用户体验要温暖、自然、人性化
- 避免冰冷的工具感

### **隐私保护 | Privacy Protection**
- 默认本地存储
- 明确的数据使用说明
- 用户完全的数据控制权

### **可访问性 | Accessibility**
- 支持多种交互方式
- 考虑不同用户群体的需求
- 国际化支持

## 📚 学习资源 | Learning Resources

### **技术文档 | Technical Documentation**
- [OpenClaw文档](https://docs.openclaw.ai)
- [Python官方文档](https://docs.python.org)
- [SQLite文档](https://www.sqlite.org/docs.html)

### **相关技术 | Related Technologies**
- 情感计算
- 自然语言处理
- 多模态AI
- 物联网集成
- 隐私保护技术

### **社区资源 | Community Resources**
- [OpenClaw社区](https://discord.com/invite/clawd)
- [GitHub Discussions](https://github.com/leilei926524-tech/samantha/discussions)
- [项目Wiki](https://github.com/leilei926524-tech/samantha/wiki)

## 🤝 行为准则 | Code of Conduct

### **我们的承诺 | Our Pledge**
我们致力于为所有人提供友好、安全和包容的环境，无论年龄、体型、残疾、民族、性别认同和表达、经验水平、国籍、个人外貌、种族、宗教或性取向如何。

### **我们的标准 | Our Standards**
可接受行为示例：
- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

不可接受行为示例：
- 使用性暗示语言或图像，以及不受欢迎的性关注或挑逗
- 挑衅、侮辱/贬损评论，以及个人或政治攻击
- 公开或私下骚扰
- 未经明确许可发布他人的私人信息
- 其他在专业环境中不适当的行为

## 📞 联系我们 | Contact Us

### **技术问题 | Technical Questions**
- GitHub Issues: [问题跟踪](https://github.com/leilei926524-tech/samantha/issues)
- Discord: OpenClaw社区 #samantha频道

### **一般咨询 | General Inquiries**
- 邮箱: leilei926524@gmail.com
- Twitter: [@charlie88931442](https://twitter.com/charlie88931442)

### **安全漏洞 | Security Vulnerabilities**
如果您发现安全漏洞，请通过邮箱直接联系项目维护者。

---

感谢您的贡献！让我们一起让Samantha变得更加温暖和智能。

Thank you for contributing! Let's work together to make Samantha warmer and smarter.