# 📦 闲鱼搜索技能 - 安装说明

## 快速安装

### 方式 1：复制到技能目录

```bash
# 技能已经位于：
~/.openclaw/skills/xianyu-search/

# 或者你的 workspace 目录：
~/openclaw/workspace/skills/xianyu-search/
```

### 方式 2：从 ClawHub 安装（待发布）

```bash
npx clawhub@latest install xianyu-search
```

---

## 使用方法

### 在 OpenClaw 中使用

直接对 AI 说：

```
帮我找闲鱼上的 MacBook Air M1 预算 2300
```

```
搜索二手 iPhone 13 预算 3000 电池 85 以上
```

```
闲鱼上有没有 9 成新的 PS5
```

### 命令行使用

```bash
cd ~/.openclaw/skills/xianyu-search

# 查看帮助
node cli.js

# 搜索商品
node cli.js "帮我找闲鱼上的 MacBook Air M1 预算 2300"

# 搜索其他商品
node cli.js "搜索二手 iPhone 13 预算 3000"
```

### 编程调用

```javascript
const { parseSearchConfig } = require('./utils');
const { SearchConfig } = require('./search');
const { generateFullReport } = require('./templates');

// 解析自然语言
const config = parseSearchConfig('帮我找闲鱼上的 MacBook Air M1 预算 2300');

// 创建搜索配置
const searchConfig = new SearchConfig(config);

// 生成搜索链接
const searchUrl = searchConfig.getSearchUrl();
console.log(searchUrl);
```

---

## 文件结构

```
xianyu-search/
├── SKILL.md          # 技能配置（OpenClaw 读取）
├── README.md         # 详细说明
├── INSTALL.md        # 本文件
├── EXAMPLES.md       # 使用示例
├── search.js         # 主搜索脚本
├── templates.js      # 输出模板
├── utils.js          # 工具函数
├── cli.js            # CLI 入口
├── test.js           # 测试文件
└── package.json      # 包配置
```

---

## 测试

```bash
cd ~/.openclaw/skills/xianyu-search
node test.js
```

预期输出：
```
🧪 开始测试闲鱼搜索技能...

测试 1: 帮我找闲鱼上的 MacBook Air M1 预算 2300
  ✅ 通过

测试 2: 搜索二手 iPhone 13 预算 3000 电池 85 以上
  ✅ 通过

测试 3: 闲鱼上有没有 9 成新的 PS5
  ✅ 通过

测试 4: 帮我看看闲鱼相机 预算 5000 北京
  ✅ 通过

──────────────────────────────────────────────────
测试结果：4 通过，0 失败
```

---

## 更新日志

### v1.0.0 (2026-03-23)
- ✅ 初始版本
- ✅ 支持自然语言解析
- ✅ 支持多平台搜索（闲鱼/转转/拍拍）
- ✅ 支持预算、成色、电池等筛选条件
- ✅ 支持卖家信用筛选
- ✅ 格式化输出（表格 + 建议）
- ✅ 提供验机清单和砍价话术

---

## 常见问题

### Q: 为什么不能直接抓取商品列表？
A: 闲鱼、转转等平台有强反爬虫机制，需要登录才能查看商品详情。技能提供搜索链接，用户自行点击查看。

### Q: 如何搜索其他平台？
A: 在输入中指定平台名称，如"转转上有没有 XXX"或"拍拍上找 XXX"。

### Q: 可以定时监控低价货源吗？
A: 当前版本不支持，可以在未来版本中添加。

---

## 贡献

欢迎提交 Issue 和 Pull Request！

---

## 许可证

MIT License
