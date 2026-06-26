# ClawHub 提交指南

## 📤 提交方式

### 方式1: 通过 ClawHub 网站提交（推荐）

1. **访问 ClawHub**
   - 打开 https://clawhub.com
   - 注册/登录账号

2. **创建新技能**
   - 点击 "Publish Skill" 或 "Submit Skill"
   - 选择 "Manual Upload"

3. **填写基本信息**
   ```
   Skill ID: skill-usage-analyzer
   Name: Skill Usage Analyzer
   Version: 1.0.0
   Description: 智能分析 OpenClaw 技能，生成使用指南、创意用法和组合推荐
   ```

4. **上传文件**
   - 上传 `skill-usage-analyzer-v1.0.0.tar.gz`
   - 或上传 `.clawhub/publish.json`

5. **填写详细信息**
   - 复制 `CLAWHUB_SUBMISSION.md` 的内容到描述框
   - 选择分类: Development, Productivity, Documentation
   - 添加标签: skill, analyzer, usage, documentation

6. **提交审核**
   - 点击 "Submit for Review"
   - 等待审核通过

### 方式2: 通过 ClawHub CLI 提交

```bash
# 安装 ClawHub CLI
npm install -g clawhub

# 登录
clawhub login

# 提交技能
cd /root/.openclaw/workspace/skills/skill-usage-analyzer
clawhub publish

# 或指定文件
clawhub publish --file .clawhub/publish.json
```

### 方式3: 通过 GitHub 自动发布

1. **创建 GitHub Release**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **GitHub Actions 自动执行**
   - 自动创建 Release
   - 上传 tar.gz 包

3. **在 ClawHub 关联 GitHub**
   - 在 ClawHub 设置中关联 GitHub 仓库
   - 自动同步 Release

## 📋 提交前检查清单

- [x] 技能ID唯一（skill-usage-analyzer）
- [x] 版本号正确（1.0.0）
- [x] SKILL.md 完整
- [x] README.md 包含使用说明
- [x] LICENSE 文件存在
- [x] .clawhub/meta.json 正确
- [x] 所有脚本可执行
- [x] 无外部依赖
- [x] 测试通过

## 📦 打包命令

```bash
cd /root/.openclaw/workspace/skills
tar -czvf skill-usage-analyzer-v1.0.0.tar.gz \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  skill-usage-analyzer/
```

## 🔍 审核流程

1. **自动检查**
   - 文件完整性
   - 元数据格式
   - 代码安全扫描

2. **人工审核**
   - 功能测试
   - 文档审查
   - 质量评估

3. **发布时间**
   - 通常 1-3 个工作日
   - 通过邮件通知

## 📝 更新技能

```bash
# 修改版本号
# 更新 CHANGELOG.md
# 重新打包
tar -czvf skill-usage-analyzer-v1.0.1.tar.gz skill-usage-analyzer/

# 提交新版本
clawhub publish --version 1.0.1
```

## ❓ 常见问题

**Q: 技能ID被占用了怎么办？**
A: 使用更具体的ID，如 `yourname-skill-usage-analyzer`

**Q: 审核被拒绝怎么办？**
A: 查看拒绝原因，修改后重新提交

**Q: 如何更新已发布的技能？**
A: 增加版本号，重新打包提交

**Q: 可以删除已发布的技能吗？**
A: 联系 ClawHub 支持团队

## 📞 联系支持

- ClawHub 支持: support@clawhub.com
- GitHub Issues: https://github.com/clawhub/clawhub/issues
- Discord: https://discord.gg/clawhub

---

**提交日期**: 2026-03-21
**技能版本**: 1.0.0
