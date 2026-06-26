# 🚀 发布指南

## 发布到 ClawHub

### 1. 登录 ClawHub

```bash
# 方式 A: 使用浏览器登录（推荐）
npx clawhub login

# 方式 B: 使用 API Token
npx clawhub login --token <your-api-token>
```

**登录后会提示**:
```
✅ Logged in as <your-username>
```

---

### 2. 发布 Skill

```bash
cd /Users/zihui/.openclaw/workspace/skills/tour-compare

# 发布新版本
npx clawhub publish . \
  --name "线路对比分析师" \
  --version "0.3.0" \
  --changelog "初始发布：支持 8 大 OTA 平台、URL 抓取、截图 OCR、可视化报告"
```

**发布成功后会提示**:
```
✅ Published tour-compare@0.3.0
🔗 https://clawhub.com/skills/tour-compare
```

---

### 3. 更新版本

```bash
# 修改 package.json 中的 version
# 然后运行：
npx clawhub publish . \
  --version "0.3.1" \
  --changelog "修复 URL 抓取 bug，优化输出格式"
```

---

## 📦 发布前检查清单

### 必需文件
- [ ] `SKILL.md` - 技能文档
- [ ] `package.json` - 依赖配置
- [ ] `README.md` - 使用说明
- [ ] `src/` - 源代码目录

### 推荐文件
- [ ] `CHANGELOG.md` - 更新日志
- [ ] `FEATURES.md` - 功能总结
- [ ] `QUICKSTART.md` - 快速入门
- [ ] `docs/` - 详细文档

### 检查项
- [ ] 所有依赖已安装
- [ ] 代码可以正常运行
- [ ] 文档已更新
- [ ] 版本号已更新（semver）

---

## 🏷️ 标签建议

**默认标签**: `latest`

**可选标签**:
- `travel` - 旅游相关
- `compare` - 对比工具
- `ota` - OTA 平台
- `ux-design` - UX 设计
- `ocr` - OCR 识别

**添加标签**:
```bash
npx clawhub publish . --tags "latest,travel,compare,ota"
```

---

## 📝 版本命名规范

遵循 [SemVer](https://semver.org/) 规范：

- **MAJOR.MINOR.PATCH** (例如：0.3.0)
- **MAJOR**: 不兼容的 API 变更
- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的问题修复

**示例**:
- `0.1.0` - 初始版本
- `0.2.0` - 新增 URL 抓取功能
- `0.2.1` - 修复 URL 抓取 bug
- `0.3.0` - 新增截图 OCR 功能
- `1.0.0` - 稳定版本

---

## 🔧 常见问题

### Q: 发布失败，提示 "Not logged in"
**A**: 先运行 `npx clawhub login` 登录

### Q: 发布失败，提示 "Path must be a folder"
**A**: 确保路径是目录，使用 `.` 或完整路径

### Q: 发布失败，提示 "Version already exists"
**A**: 版本号已存在，需要升级版本号

### Q: 如何删除已发布的版本？
**A**: 联系 ClawHub 支持或等待下一版本覆盖

---

## 📖 相关文档

- [ClawHub 文档](https://clawhub.com/docs)
- [Skill 规范](https://docs.openclaw.ai/skills/spec)
- [发布指南](https://docs.openclaw.ai/skills/publish)

---

**Made with 🦐 by 小虾**

最后更新：2026-04-01
