# 贡献指南

感谢您对Sum2Slides项目的关注！我们欢迎各种形式的贡献。

## 🎯 贡献方式

### 1. 报告问题
- 使用GitHub Issues报告bug或问题
- 提供详细的复现步骤
- 包括环境信息和版本号

### 2. 功能建议
- 提出新的功能想法
- 描述使用场景和价值
- 可选的实现思路

### 3. 代码贡献
- 修复已知bug
- 实现新功能
- 改进代码质量

### 4. 文档改进
- 修复文档错误
- 添加使用示例
- 改进文档结构

## 📋 贡献流程

### 第一步：准备工作
1. Fork项目仓库
2. 克隆到本地
```bash
通过 OpenClaw 安装技能
cd sum2slides
```

3. 创建开发环境
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### 第二步：开发流程
1. 创建功能分支
```bash
git checkout -b feature/your-feature-name
```

2. 实现功能或修复问题
3. 添加或更新测试
4. 运行测试确保通过
```bash
pytest
```

5. 格式化代码
```bash
black src/ tests/
flake8 src/
mypy src/
```

### 第三步：提交代码
1. 提交更改
```bash
git add .
git commit -m "描述你的更改"
```

2. 推送到你的仓库
```bash
git push origin feature/your-feature-name
```

3. 创建Pull Request
   - 描述你的更改
   - 关联相关问题
   - 说明测试情况

## 🧪 测试要求

### 单元测试
- 覆盖核心功能
- 测试边界条件
- 模拟错误情况

### 集成测试
- 测试完整流程
- 验证输出结果
- 确保兼容性



## 📚 代码规范

### 风格指南
1. 遵循PEP 8规范
2. 使用类型提示
3. 添加文档字符串
4. 保持代码简洁

### 提交信息格式
```
类型: 简短描述

详细描述（可选）

修复 #问题编号
```

类型包括：
- feat: 新功能
- fix: 修复问题
- docs: 文档更新
- style: 代码格式
- refactor: 代码重构
- test: 测试相关
- chore: 构建工具



## 🔧 开发工具

### 推荐工具
1. **Python 3.10+**: 运行环境
2. **pytest**: 测试框架
3. **black**: 代码格式化
4. **flake8**: 代码检查
5. **mypy**: 类型检查

### 环境变量
```bash
# 开发环境变量
export PYTHONPATH=$(pwd)/src
export SUM2SLIDES_LOG_LEVEL=DEBUG
```



## 🚀 快速开始开发

### 设置开发环境
```bash
# 1. 克隆仓库
通过 OpenClaw 安装技能
cd sum2slides

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -e ".[dev]"

# 4. 运行测试
pytest
```

### 添加新功能示例
1. 创建功能分支
2. 实现功能代码
3. 添加单元测试
4. 运行测试套件
5. 格式化代码
6. 提交Pull Request



## 🤝 社区规范

### 行为准则
1. **尊重他人**: 保持专业和友善的态度
2. **开放包容**: 欢迎不同背景的贡献者
3. **建设性反馈**: 提供有建设性的意见
4. **耐心和理解**: 理解他人的限制和困难



### 沟通渠道
1. **GitHub Issues**: 问题报告和功能建议
2. **Pull Requests**: 代码贡献和讨论
3. **Discussions**: 社区讨论和问答



## 📞 获取帮助

### 常见问题
查看 [FAQ.md](FAQ.md) 获取常见问题解答



### 联系维护者
- 通过GitHub Issues提问
- 参与Discussions讨论
- 关注项目更新



## 🙏 感谢

感谢所有贡献者的努力和支持！
- 报告问题的用户
- 提交代码的开发者
- 改进文档的撰稿人
- 测试反馈的用户

---

**保持更新**: 定期查看本指南获取最新贡献信息。