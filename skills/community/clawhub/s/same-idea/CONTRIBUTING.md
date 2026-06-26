# Contributing to Same Idea Skill

感谢你考虑为 Same Idea Skill 做出贡献！

## 如何贡献

### 报告问题

如果你发现了 bug 或有功能建议，请[创建一个 issue](https://github.com/jianghaidong/same-idea-skill/issues/new)，并包含：

1. **问题描述** - 清楚地描述问题是什么
2. **复现步骤** - 如何重现这个问题
3. **预期行为** - 你期望发生什么
4. **实际行为** - 实际发生了什么
5. **环境信息** - 操作系统、Python 版本等

### 提交代码

1. **Fork 仓库**

   点击页面右上角的 "Fork" 按钮。

2. **克隆你的 fork**

   ```bash
   git clone https://github.com/YOUR_USERNAME/same-idea-skill.git
   cd same-idea-skill
   ```

3. **创建分支**

   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

4. **进行更改**

   确保你的代码：
   - 遵循现有的代码风格
   - 包含必要的注释
   - 不破坏现有功能

5. **测试你的更改**

   ```bash
   # 手动测试搜索功能
   python3 scripts/find_similar.py "测试想法"
   ```

6. **提交更改**

   ```bash
   git add .
   git commit -m "描述你的更改"
   ```

   提交信息格式：
   - `feat: 添加新功能`
   - `fix: 修复某个问题`
   - `docs: 更新文档`
   - `refactor: 重构代码`
   - `test: 添加测试`

7. **推送到你的 fork**

   ```bash
   git push origin feature/your-feature-name
   ```

8. **创建 Pull Request**

   在 GitHub 上创建 Pull Request，描述你的更改内容。

## 开发指南

### 代码风格

- Python 代码遵循 PEP 8 规范
- 使用有意义的变量和函数名
- 添加必要的文档字符串

### 项目结构

```
same-idea/
├── SKILL.md              # OpenClaw 技能定义
├── README.md             # 项目文档
├── CONTRIBUTING.md       # 本文件
├── LICENSE               # MIT 许可证
└── scripts/
    ├── find_similar.py   # 核心搜索逻辑
    └── release.sh        # 发布脚本
```

### 核心模块说明

#### `find_similar.py`

主要函数：

- `extract_keywords(text)` - 从输入文本提取关键词
- `search_vault(vault_path, keywords)` - 搜索指定笔记库
- `rank_results(results, keywords)` - 对搜索结果进行评分排序

### 添加新功能

如果你想添加新功能，考虑以下方向：

- 🔍 改进关键词提取算法
- 📚 支持更多笔记软件（Notion, Roam Research 等）
- 🤖 集成语义搜索（嵌入向量）
- 🌍 多语言支持改进
- 📊 结果可视化

### 改进搜索质量

当前使用简单的关键词匹配，未来可以：

1. **同义词扩展** - 使用词向量扩展关键词
2. **语义搜索** - 使用 embedding 进行语义匹配
3. **上下文理解** - 考虑句子级别的语义
4. **个性化权重** - 根据用户阅读习惯调整评分

## 行为准则

- 尊重所有贡献者
- 保持建设性的讨论
- 接受建设性的批评
- 关注对社区最有利的事情

## 获取帮助

如果你有任何问题，可以：

- 在 [Issues](https://github.com/jianghaidong/same-idea-skill/issues) 中提问
- 查看现有 issues 是否有类似问题

## 许可证

通过贡献代码，你同意你的贡献将根据 MIT 许可证授权。

---

再次感谢你的贡献！🙏