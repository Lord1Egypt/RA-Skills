# 🚀 发布技能到 ClawHub

## 自动发布

```bash
cd ~/.openclaw/workspace
clawhub publish skills/remnawave-account-creator --version 1.0.0 --tags latest
```

## 如果遇到 GitHub API 限流

错误信息：`GitHub API rate limit exceeded`

**解决方案：**
1. 等待几分钟后重试
2. 或者设置 GitHub Token：
   ```bash
   export GITHUB_TOKEN=your_github_token
   ```

## 设置为私密技能

发布后，技能默认是公开的。要设置为私密：

### 方法 1: 使用 ClawHub 网页界面
1. 访问 https://clawhub.com
2. 登录账号
3. 进入 "我的技能" 页面
4. 找到 `remnawave-account-creator`
5. 点击 "编辑" 或 "设置"
6. 将可见性改为 "私密" 或 "私有"
7. 保存设置

### 方法 2: 使用 hide 命令（如果支持）
```bash
clawhub hide remnawave-account-creator
```

## 验证发布

```bash
# 查看已发布的技能
clawhub list

# 搜索自己的技能
clawhub search remnawave-account-creator
```

## 更新技能

修改技能后，更新版本并发布：

```bash
# 1. 更新 package.json 中的 version
# 2. 更新 SKILL.md 中的更新日志
# 3. 发布新版本
clawhub publish skills/remnawave-account-creator --version 1.0.1 --tags latest
```

## 技能信息

- **技能名称:** remnawave-account-creator
- **版本:** 1.0.0
- **作者:** AI Assistant (小 a)
- **分类:** automation
- **标签:** remnawave, account, email
- **可见性:** 私密（仅作者可用）

## 注意事项

1. **私密技能** - 发布后记得在 ClawHub 网页界面设置为私密
2. **不包含敏感信息** - 确保技能文件中不包含 API Token、密码等敏感信息
3. **配置文件分离** - 敏感配置应放在 `~/.openclaw/workspace/config/` 目录，不要包含在技能中

## 支持

如有问题，联系：crads@codeforce.tech
