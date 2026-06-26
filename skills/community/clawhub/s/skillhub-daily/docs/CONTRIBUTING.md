# Contributing to SkillHub Daily

我们欢迎任何形式的贡献！无论是 bug 报告、功能建议、文档改进还是代码 PR。

We welcome all forms of contributions! Bug reports, feature requests, documentation improvements, and code PRs are all welcome.

## 🐛 Bug 报告

在 [Issues](https://github.com/skillhub-community/skillhub-daily/issues) 提交 bug 时，请包含：

1. **环境信息**：Python 版本、Node.js 版本、操作系统、Agent 平台
2. **使用模式**：A 常规 / B Cron
3. **复现步骤**：触发词 / 痛点列表 / 存储通道
4. **预期 vs 实际**：
5. **错误日志**：完整堆栈

## 💡 功能建议

在 [Issues](https://github.com/skillhub-community/skillhub-daily/issues) 提交 feature request：

1. **使用场景**：你为什么需要这个功能？
2. **期望行为**：详细描述期望的输入/输出
3. **替代方案**：你考虑过哪些其他实现？

## 🔧 Pull Request

### 开发流程

1. Fork 仓库
2. 创建 feature 分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m "feat: add amazing feature"`
4. 推送分支：`git push origin feature/amazing-feature`
5. 创建 Pull Request

### 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/)：

```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建/工具
```

### 代码风格

- Python: 遵循 PEP 8
- Markdown: 遵循 CommonMark
- YAML: 2 空格缩进

### 测试

提交前请运行：

```bash
python -m py_compile scripts/skillhub_daily.py
python -m py_compile scripts/push_to_ima.py
```

## 📄 License

提交代码即表示你同意按 MIT 许可证发布。
By submitting code, you agree to release it under the MIT License.
