# 📦 闲鱼搜索技能 - ClawHub 发布指南

## 发布方式

### 方式 1：通过 ClawHub CLI（推荐）

```bash
# 1. 安装 ClawHub CLI
npm install -g @openclaw/clawhub

# 2. 登录 ClawHub
clawhub login

# 3. 进入技能目录
cd ~/.openclaw/workspace/skills/xianyu-search

# 4. 发布技能
clawhub publish

# 5. 验证发布
clawhub info xianyu-search
```

---

### 方式 2：手动提交到 ClawHub 仓库

1. **Fork ClawHub 技能仓库**
   - 访问：https://github.com/openclaw/skills
   - Fork 到你的 GitHub 账号

2. **克隆仓库**
   ```bash
   git clone https://github.com/YOUR_USERNAME/skills.git
   cd skills
   ```

3. **复制技能文件**
   ```bash
   cp -r ~/.openclaw/workspace/skills/xianyu-search skills/xianyu-search/
   ```

4. **提交 PR**
   ```bash
   git add xianyu-search/
   git commit -m "feat: add xianyu-search skill"
   git push origin main
   ```

5. **在 GitHub 上创建 Pull Request**
   - 访问你的 fork 仓库
   - 点击 "Pull requests" → "New pull request"
   - 等待审核合并

---

### 方式 3：直接分享压缩包

技能已打包在：
```
~/.openclaw/workspace/skills/xianyu-search.tar.gz
```

用户安装方法：
```bash
# 下载压缩包
tar -xzvf xianyu-search.tar.gz -C ~/.openclaw/skills/
```

---

## 发布前检查清单

- [x] `SKILL.md` - 技能配置完整
- [x] `README.md` - 使用说明清晰
- [x] `package.json` - 包信息完整
- [x] `clawhub.json` - ClawHub 元数据
- [x] `test.js` - 测试通过
- [x] 代码无敏感信息（API 密钥等）
- [x] 许可证明确（MIT）

---

## 技能信息

**名称**: xianyu-search  
**版本**: 1.0.0  
**分类**: shopping  
**标签**: 闲鱼，二手，搜索，购物，xianyu, goofish  
**图标**: 🔍  

**功能特性**:
- 🎯 自然语言解析
- 📊 格式化输出
- 🏆 信用筛选
- 🔋 电池筛选
- 📍 地区筛选
- 💡 购买建议
- 🔗 多平台支持

**使用示例**:
```
帮我找闲鱼上的 MacBook Air M1 预算 2300
搜索二手 iPhone 13 预算 3000 电池 85 以上
闲鱼上有没有 9 成新的 PS5
帮我看看闲鱼相机 预算 5000 北京
```

---

## 发布后验证

```bash
# 安装技能
clawhub install xianyu-search

# 测试技能
node cli.js "帮我找闲鱼上的 MacBook Air M1 预算 2300"
```

---

## 维护

**更新版本**:
```bash
# 修改版本号
vim package.json  # 修改 version 字段

# 重新发布
clawhub publish --bump
```

---

## 联系方式

- **作者**: OpenClaw Community
- **仓库**: https://github.com/openclaw/skills/tree/main/xianyu-search
- **问题反馈**: https://github.com/openclaw/skills/issues

---

## 许可证

MIT License - 自由使用、修改和分发
