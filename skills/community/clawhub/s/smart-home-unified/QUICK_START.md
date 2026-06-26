# Smart Home Unified - 快速发布指南

## ⚡ 3 步完成发布

### 步骤 1: 登录 ClawHub

**方式 A: 浏览器登录（推荐）**
```bash
clawhub login
```
- 会自动打开浏览器
- 使用 GitHub/Google 账号登录
- 授权 CLI 访问权限

**方式 B: API Token 登录**
```bash
clawhub login --token <YOUR_API_TOKEN>
```
- 登录 https://clawhub.ai/settings/tokens 获取 Token
- 适合 CI/CD 或无头环境

---

### 步骤 2: 发布技能

```bash
clawhub publish "D:\openclaw\workspace\skills\smart-home-unified" \
  --changelog "v1.0.0 - 智能家居统一控制，支持小米/华为/HomeKit/Alexa/Google 等多平台集成"
```

**可选参数**:
```bash
# 指定版本
clawhub publish <path> --version 1.0.0

# 指定显示名
clawhub publish <path> --name "Smart Home Unified"

# 指定标签
clawhub publish <path> --tags "latest,smart-home,iot"

# 完整命令
clawhub publish "D:\openclaw\workspace\skills\smart-home-unified" \
  --name "Smart Home Unified" \
  --version 1.0.0 \
  --tags "latest,smart-home,iot,automation" \
  --changelog "v1.0.0 - 智能家居统一控制，支持小米/华为/HomeKit/Alexa/Google 等多平台集成"
```

---

### 步骤 3: 验证上线

**检查技能页面**:
```bash
# 查看已发布的技能
clawhub list

# 查看技能详情
clawhub info smart-home-unified
```

**浏览器访问**:
```
https://clawhub.ai/skills/smart-home-unified
```

**测试安装**:
```bash
# 在新环境测试安装
clawhub install smart-home-unified

# 验证命令可用
smart-home --help
smart-home devices list
```

---

## ✅ 发布前检查清单

### 文件完整性
- [ ] clawhub.json 存在且配置正确
- [ ] package.json 存在且版本匹配
- [ ] README.md 包含使用说明
- [ ] SKILL.md 包含技能描述
- [ ] bin/cli.js 可执行
- [ ] 所有依赖文件完整

### 配置验证
- [ ] 技能名称：smart-home-unified
- [ ] 版本号：1.0.0（符合 semver）
- [ ] 描述清晰准确
- [ ] 许可证正确（MIT-0）
- [ ] 定价策略合理

### 文档质量
- [ ] README 包含快速开始
- [ ] 有使用示例
- [ ] 有故障排除指南
- [ ] 有联系方式/支持渠道

### 代码质量
- [ ] CLI 命令可正常运行
- [ ] 错误处理完善
- [ ] 有基本的测试用例
- [ ] 无敏感信息（密码、密钥等）

---

## 🐛 常见问题

### Q1: 发布失败 "Not logged in"
**解决**:
```bash
# 重新登录
clawhub login

# 检查登录状态
clawhub whoami
```

### Q2: 发布失败 "Skill name already exists"
**解决**:
- 说明该名称已被占用
- 更换名称或联系原作者
- 或者发布为新版本（如果技能是你的）

```bash
# 更新现有技能
clawhub publish <path> --version 1.0.1
```

### Q3: 发布失败 "Invalid clawhub.json"
**解决**:
- 检查 clawhub.json 格式
- 确保必填字段存在（name, version, description）
- 验证 JSON 语法

```bash
# 验证 JSON 格式
cat clawhub.json | jq .
```

### Q4: 技能上线后找不到
**解决**:
- 等待 1-2 分钟（缓存刷新）
- 检查标签是否为 "latest"
- 尝试直接访问 URL

### Q5: 用户安装失败
**解决**:
```bash
# 查看详细错误
clawhub install smart-home-unified --verbose

# 清除缓存重试
clawhub cache clean
clawhub install smart-home-unified
```

---

## 📊 发布后监控

### 关键指标
| 指标 | 查看方式 | 频率 |
|------|----------|------|
| 下载量 | ClawHub 后台 | 每日 |
| 安装量 | ClawHub 后台 | 每日 |
| 活跃用户 | 内置分析 | 每周 |
| 用户评价 | 技能页面 | 每日 |
| 问题反馈 | GitHub/邮件 | 每日 |

### 数据看板
```bash
# 查看技能统计
clawhub stats smart-home-unified

# 查看下载趋势
clawhub analytics smart-home-unified --period 7d
```

---

## 🔄 版本更新

### 发布新版本
```bash
# 1. 更新版本号
# 编辑 clawhub.json 和 package.json

# 2. 更新 changelog
# 编辑 CHANGELOG.md 或在发布时指定

# 3. 发布
clawhub publish <path> \
  --version 1.0.1 \
  --changelog "v1.0.1 - 修复了 Xiaomi 平台连接问题，新增 HUAWEI 支持"

# 4. 打标签（可选）
git tag v1.0.1
git push origin v1.0.1
```

### 版本策略
- **Patch (1.0.x)**: Bug 修复，小改进
- **Minor (1.x.0)**: 新功能，向后兼容
- **Major (x.0.0)**: 破坏性变更

---

## 📞 获取帮助

### 官方文档
- ClawHub Docs: https://docs.clawhub.com
- 技能开发指南：https://docs.clawhub.com/skills
- 发布流程：https://docs.clawhub.com/publish

### 社区支持
- Discord: https://discord.gg/clawhub
- GitHub Issues: https://github.com/clawhub/cli/issues
- 邮件：support@clawhub.com

### 紧急联系
- 发布问题：@clawhub-support (Discord)
- 商务咨询：business@clawhub.com

---

## 🎉 发布成功后的下一步

1. **庆祝一下** 🎊
2. **开始推广** - 参考 MARKETING_PLAN.md
3. **收集反馈** - 关注用户评价和问题
4. **快速迭代** - 根据反馈发布新版本
5. **持续优化** - 改进文档和功能

---

**最后更新**: 2026-03-15  
**文档版本**: v1.0
