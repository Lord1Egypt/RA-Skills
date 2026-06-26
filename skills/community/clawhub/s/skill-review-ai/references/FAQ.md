# 常见问题解答

## 一般问题

### Q: 什么是 skill-review？

A: skill-review 是一个用于审查 Agent Skills 规范性、完整性和代码质量的工具。它帮助开发者在安装或发布 skills 前进行质量检查。

### Q: 为什么需要审查 skills？

A: 审查 skills 可以：
- 确保符合 Agent Skills 规范
- 发现潜在的安全问题
- 提高代码质量
- 保证用户体验一致性

### Q: 审查工具会修改我的 skill 吗？

A: 不会。skill-review 是只读工具，它只会分析你的 skill 并生成报告，不会修改任何文件。

## 使用问题

### Q: 如何运行审查？

A: 使用以下命令：
```bash
bash scripts/review.sh /path/to/your-skill
```

### Q: 如何生成 JSON 格式的报告？

A: 添加 `--json` 参数：
```bash
bash scripts/review.sh /path/to/your-skill --json
```

### Q: 如何查看详细的代码分析？

A: 添加 `--verbose` 参数：
```bash
bash scripts/review.sh /path/to/your-skill --verbose
```

### Q: 审查失败怎么办？

A: 根据报告中的问题逐一修复：
1. 优先修复 ERROR 级别的问题
2. 评估并修复 WARN 级别的问题
3. 参考 SKILL.md 中的示例进行修复

## SKILL.md 问题

### Q: name 字段有什么限制？

A: name 字段必须：
- 1-64 字符
- 仅小写字母、数字、连字符
- 不能以连字符开头或结尾
- 不能包含连续连字符
- 与目录名匹配

### Q: description 应该多长？

A: 建议：
- 最少 10 字符
- 最多 1024 字符
- 描述功能和使用场景
- 包含相关关键词

### Q: 可以省略 license 字段吗？

A: 可以。license 是可选字段，但建议添加以明确许可证信息。

### Q: metadata 字段可以包含什么？

A: metadata 是键值对映射，可以包含任意字符串键值，例如：
```yaml
metadata:
  author: your-name
  version: "1.0"
  category: utility
```

## 目录结构问题

### Q: 必须包含 scripts 目录吗？

A: 不是必需的。scripts 目录是可选的，只有当 skill 需要可执行代码时才需要。

### Q: 目录可以嵌套多深？

A: 建议不超过 2 层深度。过深的嵌套会增加维护难度。

### Q: 目录名必须与 name 字段完全匹配吗？

A: 是的。目录名必须与 SKILL.md 中的 name 字段完全一致。

## 脚本代码问题

### Q: 支持哪些脚本语言？

A: 审查工具支持：
- Bash (.sh)
- Python (.py)
- JavaScript (.js)

### Q: 为什么需要 shebang？

A: shebang 告诉系统使用哪个解释器执行脚本，是良好的实践。

### Q: 什么是敏感信息？

A: 敏感信息包括：
- 密码
- API Keys
- 密钥
- Tokens
- 其他机密信息

### Q: 如何避免硬编码敏感信息？

A: 建议：
- 使用环境变量
- 使用配置文件
- 使用密钥管理服务

### Q: 为什么建议添加 `set -e`？

A: `set -e` 使脚本在命令失败时立即退出，避免错误被忽略。

## 文件引用问题

### Q: 如何引用其他文件？

A: 使用相对路径，从 skill 根目录开始：
```markdown
See [reference](references/REFERENCE.md)
Run [script](scripts/helper.sh)
```

### Q: 可以引用外部 URL 吗？

A: 可以。外部 URL 不会被检查存在性。

### Q: 文件大小有限制吗？

A: 建议单个文件不超过 1MB。大文件会影响加载性能。

## 评分问题

### Q: 多少分算通过？

A: 通过线是 75 分。但建议尽可能获得更高分数。

### Q: 为什么我的 skill 得分很低？

A: 常见原因：
- 缺少必需字段
- 格式错误
- 硬编码敏感信息
- 引用的文件不存在

### Q: 可以忽略警告吗？

A: 警告不会导致失败，但建议评估并修复，以提高 skill 质量。

### Q: 如何提高评分？

A: 建议：
1. 确保所有必需字段正确
2. 添加适当的注释
3. 处理好错误情况
4. 验证所有文件引用
5. 保持文件大小合理

## 集成问题

### Q: 可以在 CI/CD 中使用吗？

A: 可以。建议使用 `--json` 参数获取结构化输出，便于自动化处理。

### Q: 如何集成到 GitHub Actions？

A: 示例 workflow：
```yaml
name: Skill Review
on: [push, pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run skill review
        run: bash scripts/review.sh . --json
```

### Q: 可以自定义审查规则吗？

A: 当前版本不支持自定义规则，但可以通过修改 Python 脚本实现。

## 其他问题

### Q: 发现 bug 怎么办？

A: 请提交反馈：
1. 描述问题
2. 提供复现步骤
3. 提供相关文件

### Q: 如何贡献代码？

A: 欢迎贡献：
1. Fork 仓库
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request

### Q: 有示例 skill 吗？

A: 可以参考：
- 官方示例 skills
- 社区贡献的 skills
- 本仓库的测试用例
