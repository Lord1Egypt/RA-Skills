# 🚀 发布到 ClawHub 指南

## 前置要求

1. 安装 ClawHub CLI
```bash
npm i -g clawhub
```

2. 登录 ClawHub
```bash
clawhub login
# 按提示输入账号信息

clawhub whoami
# 验证登录状态
```

---

## 📦 发布步骤

### 方式一：使用 ClawHub CLI 发布

```bash
# 进入 skill 目录
cd /root/.openclaw/workspace/skills/code-analyzer

# 发布到 ClawHub
clawhub publish . \
  --slug code-analyzer \
  --name "Code Analyzer" \
  --version 1.0.0 \
  --changelog "Initial release: Python code analysis and optimization tool"
```

### 方式二：使用脚本发布

已为你生成发布脚本：

```bash
chmod +x publish.sh
./publish.sh
```

---

## 🔧 手动打包上传（备用方案）

如果 CLI 发布失败，可以手动打包：

```bash
# 创建发布包
cd /root/.openclaw/workspace/skills
tar -czvf code-analyzer-v1.0.0.tar.gz code-analyzer/

# 上传到 ClawHub 网站
# 访问 https://clawhub.com/upload
# 选择打包文件上传
```

---

## 📋 发布前检查清单

- [ ] 版本号已更新（package.json + skill.yaml）
- [ ] CHANGELOG.md 已更新
- [ ] README.md 内容完整
- [ ] 代码测试通过
- [ ] 敏感信息已移除（API密钥等）
- [ ] LICENSE 文件存在

---

## 🏷️ 版本管理

### 发布新版本

```bash
# 1. 更新版本号
# 编辑 package.json 和 skill.yaml 中的 version

# 2. 更新 CHANGELOG.md

# 3. 提交更改
git add .
git commit -m "Release v1.1.0: Add new features"
git tag v1.1.0
git push origin main --tags

# 4. 发布到 ClawHub
clawhub publish . \
  --slug code-analyzer \
  --version 1.1.0 \
  --changelog "Add X feature, fix Y bug"
```

### 版本号规范（Semantic Versioning）

- `MAJOR.MINOR.PATCH`
- `1.0.0` - 初始版本
- `1.1.0` - 新增功能（向后兼容）
- `1.1.1` - 修复 bug
- `2.0.0` - 破坏性变更

---

## 🔍 验证发布

发布后验证：

```bash
# 搜索你的 skill
clawhub search "code analyzer"

# 安装测试
clawhub install code-analyzer

# 查看已安装列表
clawhub list
```

---

## 🐛 故障排除

### 问题：登录失败
```bash
# 清除缓存重试
clawhub logout
clawhub login
```

### 问题：发布被拒绝
- 检查 skill.yaml 格式是否正确
- 确认版本号比之前的高
- 检查是否有敏感信息泄露

### 问题：找不到 skill
```bash
# 更新索引
clawhub update --all
```

---

## 📚 相关资源

- ClawHub 官网: https://clawhub.com
- OpenClaw 文档: https://docs.openclaw.ai
- 技能开发指南: https://docs.openclaw.ai/skills/development

---

## 💡 推广建议

发布后可以在以下渠道分享：

1. **GitHub** - 完善 README，添加截图和示例
2. **Twitter/X** - 分享 skill 功能亮点
3. **Discord** - OpenClaw 社区分享
4. **博客** - 写一篇使用教程

祝发布顺利！🎉
