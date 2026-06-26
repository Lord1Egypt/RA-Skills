# ClawHub 发布指南

_wecom-user-manager v1.0.0_

---

## 📦 发布信息

| 项目 | 值 |
|------|-----|
| **Skill 名称** | wecom-user-manager |
| **版本** | 1.0.0 |
| **描述** | 企业微信用户管理技能 |
| **作者** | 杨广伟 |
| **许可证** | MIT |
| **发布日期** | 2026-03-28 |

---

## 🚀 发布步骤

### 方式 1：通过 ClawHub 网站（推荐）

1. **访问 ClawHub**
   ```
   https://clawhub.ai/skills/publish
   ```

2. **登录账号**
   - 使用 GitHub 或邮箱登录

3. **上传 Skill**
   - 点击"New Skill"
   - 填写 Skill 信息：
     - Name: `wecom-user-manager`
     - Version: `1.0.0`
     - Description: 企业微信用户管理技能。支持管理员添加用户权限，用户首次登录自动激活。
     - Category: `Enterprise` 或 `Productivity`
     - Tags: `wecom`, `企业微信`, `用户管理`, `权限管理`

4. **上传文件**
   - 上传 `wecom-user-manager-1.0.0.tar.gz`
   - 或上传整个 `wecom-user-manager/` 目录

5. **填写元数据**
   ```json
   {
     "name": "wecom-user-manager",
     "version": "1.0.0",
     "description": "企业微信用户管理技能",
     "author": "杨广伟",
     "license": "MIT",
     "keywords": ["wecom", "企业微信", "用户管理"],
     "emoji": "👤",
     "requires": {
       "bins": ["python3"]
     }
   }
   ```

6. **提交审核**
   - 检查所有信息
   - 点击"Submit for Review"
   - 等待审核通过（通常 1-2 个工作日）

7. **发布成功**
   - 审核通过后自动发布
   - 获得发布 URL: `https://clawhub.ai/skills/wecom-user-manager`

---

### 方式 2：通过 CLI（如果可用）

```bash
# 安装 ClawHub CLI
npm install -g @openclaw/clawhub

# 登录
clawhub login

# 发布
cd /opt/openclaw/oc-b/workspace/skills/wecom-user-manager
clawhub publish

# 或使用发布包
clawhub publish wecom-user-manager-1.0.0.tar.gz
```

---

## 📋 发布清单

### 必需文件
- ✅ SKILL.md - 技能文档
- ✅ handler.py - 消息处理器
- ✅ auto_activate.py - 自动激活脚本
- ✅ references/api-user-manager.md - API 文档
- ✅ README.md - 使用说明
- ✅ .clawhub/manifest.json - 发布清单
- ✅ .clawhub/origin.json - ClawHub 配置

### 可选文件
- ✅ LICENSE - 许可证文件
- ✅ .clawhub/PUBLISH-INSTRUCTIONS.md - 发布指南
- ✅ .clawhub/CHANGELOG.md - 更新日志

---

## 🔍 审核要点

ClawHub 审核团队会检查：

1. **功能完整性**
   - ✅ Skill 功能正常
   - ✅ 文档完整
   - ✅ 示例可用

2. **代码质量**
   - ✅ 无安全漏洞
   - ✅ 无恶意代码
   - ✅ 遵循最佳实践

3. **文档质量**
   - ✅ README 清晰
   - ✅ 使用示例完整
   - ✅ 配置说明详细

4. **兼容性**
   - ✅ 与 OpenClaw 兼容
   - ✅ 与依赖技能兼容
   - ✅ 跨平台支持

---

## 📊 发布后

### 安装链接
```
https://clawhub.ai/skills/wecom-user-manager
```

### 安装命令
```bash
openclaw skill install wecom-user-manager
```

### 分享链接
- Twitter: https://twitter.com/intent/tweet?text=Check%20out%20this%20OpenClaw%20skill:%20wecom-user-manager
- GitHub: https://github.com/xunrong-tech/wecom-openclaw-plugin

---

## 🎯 推广建议

1. **社交媒体**
   - Twitter 分享
   - LinkedIn 分享
   - 技术社区分享

2. **文档链接**
   - 添加到项目 README
   - 添加到公司文档
   - 添加到个人博客

3. **示例演示**
   - 创建演示视频
   - 编写使用教程
   - 分享最佳实践

---

## 📞 联系支持

如有问题，请联系：

- **邮箱**: guangwei.yang@xtechmerge.com
- **GitHub**: https://github.com/xunrong-tech/wecom-openclaw-plugin/issues
- **Discord**: https://discord.com/invite/clawd

---

## ✅ 发布前检查清单

- [ ] 所有文件已准备
- [ ] manifest.json 已填写
- [ ] README.md 已完善
- [ ] 测试通过
- [ ] 版本号正确
- [ ] 许可证文件存在
- [ ] 文档完整
- [ ] 示例可用
- [ ] 打包完成
- [ ] 准备发布

---

**准备就绪！可以开始发布了！** 🎉

**最后更新**: 2026-03-28  
**版本**: 1.0.0
