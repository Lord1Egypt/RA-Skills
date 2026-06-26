# 📤 发布到 ClawHub 指南

## 🚀 快速发布

### 方法 1：在本地电脑发布（推荐）

由于当前服务器环境没有浏览器，建议在你的**本地电脑**上发布：

```bash
# 1. 在本地电脑上安装 clawhub
npm install -g clawhub

# 2. 登录 ClawHub（会打开浏览器）
clawhub login

# 3. 下载 skill 文件夹
# 从服务器下载 restaurant-review-crosscheck 文件夹

# 4. 进入 skill 目录
cd restaurant-review-crosscheck

# 5. 发布
clawhub publish . \
  --slug restaurant-crosscheck \
  --name "餐厅推荐交叉验证" \
  --version 1.0.0 \
  --changelog "初始版本：支持小红书和大众点评交叉验证餐厅推荐"
```

### 方法 2：在服务器上使用 Token

如果你想直接在服务器上发布，需要：

1. **获取 Token**：
   - 在有浏览器的设备上访问 https://clawhub.ai
   - 登录账号
   - 获取 API token（在设置中）

2. **在服务器上使用 Token 登录**：
   ```bash
   clawhub login --token "YOUR_TOKEN_HERE"
   ```

3. **发布 skill**：
   ```bash
   cd /home/ubuntu/.openclaw/workspace/skills/restaurant-review-crosscheck
   clawhub publish . \
     --slug restaurant-crosscheck \
     --name "餐厅推荐交叉验证" \
     --version 1.0.0 \
     --changelog "初始版本：支持小红书和大众点评交叉验证餐厅推荐"
   ```

---

## 📋 发布元数据

### Skill 信息

- **Slug**: `restaurant-crosscheck`
- **Name**: 餐厅推荐交叉验证
- **Version**: `1.0.0`
- **Category**: Utilities

### 描述（中文）

```
交叉验证小红书和大众点评的餐厅推荐数据。支持按地理位置和菜系查询，自动分析两个平台的一致性，提供可信的餐厅推荐评分。适合用于美食推荐和餐厅决策辅助。
```

### Description (English)

```
Cross-reference restaurant recommendations from Xiaohongshu and Dianping to validate restaurant quality. Query by location and cuisine, analyze cross-platform consistency, and get trustworthy recommendation scores.
```

### Tags

```
restaurant, food, recommendation, dianping, xiaohongshu, china, chinese
```

### Changelog

```
## v1.0.0 (2026-02-09)

Initial release:

Features:
- Cross-platform validation (Dianping + Xiaohongshu)
- Location-based search
- Cuisine type filtering
- Consistency analysis
- Recommendation scoring (0-10)
- Server-friendly command-line tool
- Full documentation

Usage:
- Command line: restaurant-crosscheck "location" "cuisine"
- Dialogue integration: "查询深圳南山区推荐餐厅"
- Server version with mock data
- Full version with real scraping (requires browser)
```

---

## 🔧 完整发布命令

### 基础发布

```bash
clawhub publish . \
  --slug restaurant-crosscheck \
  --name "餐厅推荐交叉验证" \
  --version 1.0.0 \
  --changelog "初始版本"
```

### 完整元数据发布

```bash
clawhub publish . \
  --slug restaurant-crosscheck \
  --name "餐厅推荐交叉验证" \
  --description "Cross-reference restaurant recommendations from Xiaohongshu and Dianping" \
  --version 1.0.0 \
  --changelog "Initial release with cross-platform validation" \
  --tags "restaurant,food,recommendation,chinese"
```

---

## 📦 Skill 文件检查

发布前确保以下文件存在：

```
restaurant-review-crosscheck/
├── SKILL.md                   ✅ 必需
├── README.md                  ✅ 推荐
├── QUICKSTART.md              ✅ 推荐
├── SERVER_GUIDE.md            ✅ 推荐
├── restaurant-crosscheck      ✅ 可执行命令
├── scripts/
│   ├── crosscheck_simple.py   ✅ 服务器版本
│   ├── config.py              ✅ 配置文件
│   └── ...                    (其他脚本)
└── references/                (可选文档)
```

---

## ✅ 发布前检查清单

- [ ] SKILL.md 格式正确
- [ ] README.md 完整
- [ ] 命令行工具有执行权限
- [ ] 测试基本功能
- [ ] 准备好 changelog
- [ ] 确定版本号
- [ ] 登录 ClawHub

---

## 🔄 更新已发布的 Skill

如果需要更新已发布的 skill：

```bash
# 1. 更新版本号（例如 1.0.0 -> 1.0.1）
# 2. 修改 SKILL.md 或其他文件
# 3. 重新发布
clawhub publish . \
  --slug restaurant-crosscheck \
  --version 1.0.1 \
  --changelog "修复：优化匹配算法"
```

---

## 💡 提示

### 版本号规范

- **主版本**（Major）：不兼容的 API 修改
- **次版本**（Minor）：向下兼容的功能新增
- **修订版**（Patch）：向下兼容的问题修正

示例：
- `1.0.0` - 初始版本
- `1.0.1` - Bug 修复
- `1.1.0` - 新增功能
- `2.0.0` - 重大更新

### Changelog 格式

```
## v1.0.0 (YYYY-MM-DD)

Added:
- 新功能 A
- 新功能 B

Changed:
- 修改的功能

Fixed:
- 修复的问题

Docs:
- 文档更新
```

---

## 📖 参考资料

- **ClawHub 文档**: https://clawhub.com/docs
- **Skill 创建指南**: `/home/ubuntu/.npm-global/lib/node_modules/openclaw/skills/skill-creator/SKILL.md`
- **ClawHub CLI**: `clawhub --help`

---

## 🎯 下一步

1. **选择发布方法**：
   - 本地电脑（推荐）
   - 服务器（需要 token）

2. **准备发布信息**：
   - 确定版本号
   - 编写 changelog
   - 准备描述和标签

3. **执行发布**：
   ```bash
   clawhub publish . --slug restaurant-crosscheck --version 1.0.0
   ```

4. **验证发布**：
   ```bash
   clawhub search restaurant-crosscheck
   ```

---

**准备好了吗？开始发布吧！** 🚀
