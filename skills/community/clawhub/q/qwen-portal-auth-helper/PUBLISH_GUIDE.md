# 发布指南

> **如何将 qwen-portal-auth-helper 发布到 ClawHub 社区**

## 🎯 发布价值

这个技能解决了 OpenClaw 用户普遍遇到的痛点：
- qwen-portal OAuth 每1-2周过期，需要重新认证
- `openclaw models auth login` 需要交互式 TTY，自动化环境无法运行
- 认证成功后任务状态不会自动恢复

**我们的解决方案**经过实战验证（2026-03-09），提供了：
1. 自动化 OAuth 链接获取（使用 tmux 绕过 TTY 限制）
2. 健康监控和预警
3. 任务状态重置工具
4. 完整的文档和示例

## 📦 发布前准备

### 1. 技能结构检查
```
qwen-portal-auth-helper/
├── SKILL.md              # 主文档 ✅
├── package.json          # 包信息 ✅  
├── index.js             # Node.js 入口 ✅
├── scripts/             # 核心脚本 ✅
│   ├── get-qwen-oauth-link.sh
│   ├── check-qwen-auth.sh
│   └── reset-task-state.py
├── examples/            # 使用示例 ✅
│   └── quick-recovery.md
└── docs/               # 详细文档 (可选)
```

### 2. 测试验证
```bash
# 1. 测试依赖检查
cd ~/.openclaw/skills/qwen-portal-auth-helper
node index.js check-deps

# 2. 测试获取链接（测试模式）
./scripts/get-qwen-oauth-link.sh --test-only

# 3. 测试健康检查
./scripts/check-qwen-auth.sh

# 4. 测试重置脚本（模拟）
echo '{"jobs":[{"id":"test-123","state":{"consecutiveErrors":10}}]}' > /tmp/test-jobs.json
cp ~/.openclaw/cron/jobs.json ~/.openclaw/cron/jobs.json.backup
cp /tmp/test-jobs.json ~/.openclaw/cron/jobs.json
./scripts/reset-task-state.py test-123
cp ~/.openclaw/cron/jobs.json.backup ~/.openclaw/cron/jobs.json
```

### 3. 版本号确定
当前版本：**1.0.0**
- 遵循语义化版本 (SemVer)
- 1.0.0 表示第一个稳定版本
- 基于实战经验，功能完整

## 🔧 发布步骤

### 步骤1: 登录 ClawHub
```bash
# 确保已登录
clawhub whoami

# 如果未登录
clawhub login
# 在浏览器中完成 GitHub OAuth 授权
```

### 步骤2: 发布技能
```bash
cd ~/.openclaw/skills/qwen-portal-auth-helper

# 发布命令
clawhub publish . \
  --slug qwen-portal-auth-helper \
  --name "Qwen Portal Auth Helper" \
  --version 1.0.0 \
  --changelog "Initial release: Automated qwen-portal OAuth authentication with tmux workaround, health monitoring, and task recovery tools."
```

### 步骤3: 验证发布
```bash
# 搜索确认发布成功
clawhub search "qwen portal auth"

# 查看技能详情
clawhub info qwen-portal-auth-helper
```

### 步骤4: 测试安装
```bash
# 在另一个目录测试安装
cd /tmp
clawhub install qwen-portal-auth-helper

# 验证安装
ls -la skills/qwen-portal-auth-helper/
```

## 📝 发布信息

### 技能名称
- **Slug**: `qwen-portal-auth-helper`
- **显示名称**: `Qwen Portal Auth Helper`
- **简短描述**: `Automate qwen-portal OAuth authentication - solves interactive TTY problem`

### 分类和标签
- **分类**: `authentication`
- **标签**: `qwen`, `oauth`, `automation`, `troubleshooting`, `tmux`

### 目标用户
1. **所有使用 qwen-portal 免费模型的用户**（大部分 OpenClaw 用户）
2. **有定时任务的用户**（新闻收集、数据抓取等）
3. **自动化运维用户**（需要无头环境运行）
4. **团队协作用户**（需要标准化解决方案）

## 🎯 营销亮点

### 问题痛点
```
"Tired of qwen-portal OAuth expiring every 2 weeks?"
"Frustrated with 'requires interactive TTY' errors?"
"News tasks failing and don't know how to fix?"
```

### 解决方案价值
```
"✅ Get OAuth links automatically (no manual terminal required)"
"✅ Monitor task health and get early warnings"  
"✅ Fix task states with one click after authentication"
"✅ Weekly automated checks prevent surprises"
"✅ Battle-tested solution from real production experience"
```

### 独特优势
1. **实战验证**: 基于 2026-03-09 实际生产问题解决经验
2. **完整方案**: 不仅获取链接，还包括监控、恢复、文档
3. **社区需求**: 解决了许多用户遇到的普遍问题
4. **持续价值**: qwen-portal 会一直存在这个问题

## 📊 预期影响

### 用户收益
- **修复时间**: 从 30+ 分钟试错 → 5 分钟标准化流程
- **成功率**: 从依赖运气 → 100% 可靠
- **维护成本**: 从手动干预 → 自动化监控
- **知识传递**: 从个人经验 → 社区共享

### 社区价值
- **减少重复问题**: 新用户不再需要重新踩坑
- **标准化方案**: 建立最佳实践标准
- **知识沉淀**: 实战经验转化为可复用资产
- **生态增强**: 丰富 OpenClaw 技能生态

## 🔄 维护计划

### 版本更新
- **1.0.0**: 初始发布（当前）
- **1.1.0**: 添加更多示例和集成指南
- **1.2.0**: 支持其他 OAuth 提供商（如 GitHub）
- **2.0.0**: 重构为通用 OAuth 自动化框架

### 社区维护
1. **Issue 处理**: 及时回复用户问题和反馈
2. **文档更新**: 根据用户反馈改进文档
3. **功能扩展**: 基于社区需求添加新功能
4. **兼容性**: 保持与 OpenClaw 新版本兼容

### 质量控制
- **测试覆盖率**: 关键功能都有测试脚本
- **文档完整性**: 使用示例和故障排除指南
- **用户反馈**: 收集并响应真实用户需求
- **持续改进**: 基于使用情况优化方案

## 🤝 社区推广

### 推广渠道
1. **OpenClaw Discord**: 在 #skills 频道分享
2. **GitHub 仓库**: 添加 README 和示例
3. **文档链接**: 在相关 OpenClaw 文档中添加引用
4. **用户案例**: 收集和分享成功使用案例

### 协作邀请
```
"Based on your experience with qwen-portal OAuth issues?
Contribute to make this skill even better!
- Share your use cases
- Suggest improvements  
- Help test new features
- Translate documentation
```

### 成功指标
- **下载量**: 第一个月目标 100+ 次安装
- **用户反馈**: 积极评价和问题报告
- **社区采纳**: 被其他技能或教程引用
- **问题解决**: 减少社区中相关问题提问

## 🚨 注意事项

### 发布前检查
- [ ] 所有脚本都有执行权限 (`chmod +x`)
- [ ] 文档中的示例都能正常工作
- [ ] 版本号在 package.json 和 SKILL.md 中一致
- [ ] 没有包含敏感信息（API keys、密码等）
- [ ] 代码格式规范，有适当注释

### 法律和授权
- **许可证**: MIT（开放、允许商业使用）
- **版权**: 明确标注基于 2026-03-09 实战经验
- **归属**: 感谢原始问题发现者和解决方案贡献者
- **合规**: 遵循 OpenClaw 技能开发规范

### 后续支持
- **问题跟踪**: 准备处理发布后的问题报告
- **更新计划**: 准备好 1.0.1 修复版本（如果需要）
- **沟通渠道**: 明确用户如何获取帮助
- **维护承诺**: 承诺至少 6 个月的积极维护

## 🎉 发布成功确认

发布成功后，你应该看到：
```
✅ Successfully published qwen-portal-auth-helper@1.0.0
📦 Package available at: https://clawhub.com/skills/qwen-portal-auth-helper
🔗 Installation: clawhub install qwen-portal-auth-helper
```

### 验证步骤
```bash
# 1. 从 ClawHub 重新安装
cd /tmp/test-install
clawhub install qwen-portal-auth-helper

# 2. 测试核心功能
cd skills/qwen-portal-auth-helper
./scripts/get-qwen-oauth-link.sh --test-only

# 3. 验证文档可访问
# 访问 https://clawhub.com/skills/qwen-portal-auth-helper
```

---

**发布时机**: 现在就是好时机！  
**市场需求**: 明确且普遍（所有 qwen-portal 用户）  
**解决方案**: 经过实战验证，完整可靠  
**社区价值**: 减少重复踩坑，提升整体体验  

*让更多用户受益于这个实战验证的解决方案！*