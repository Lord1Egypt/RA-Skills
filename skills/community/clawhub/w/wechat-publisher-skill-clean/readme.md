# 智能微信公众号发布技能

> 🦞 基于 OpenClaw 的微信公众号自动发布技能

[![ClawHub](https://img.shields.io/badge/clawhub-smart--wechat--publisher-blue)](https://clawhub.com/skills/smart-wechat-publisher)
[![Version](https://img.shields.io/badge/version-1.1.2-green)](https://github.com/403914291/wechat-publisher-skill)
[![License](https://img.shields.io/badge/license-Commercial-orange)]()

---

## 📋 功能特性

- ✅ **自动收集** 15 条 AI 新闻
- ✅ **自动生成** HTML 格式内容
- ✅ **自动发布** 到公众号草稿箱
- ✅ **5 套专业模板** 可选
- ✅ **50 次免费试用**（约 1 个月）
- ✅ **8.8 元永久买断**

---

## 🚀 快速开始

### 安装技能

```bash
# 使用 ClawHub 安装
clawhub install smart-wechat-publisher

# 或使用 OpenClaw
openclaw skill install smart-wechat-publisher
```

### 配置技能

```bash
# 交互式配置
openclaw skill config smart-wechat-publisher

# 或命令行配置
openclaw skill config smart-wechat-publisher \
  --app-id wxebff9eadface1489 \
  --app-secret 44c10204ceb1bfb3f7ac096754976454
```

### 设置发布时间

```bash
# 每天早上 6 点自动发布
openclaw schedule smart-wechat-publisher 06:00
```

---

## 📁 项目结构

```
wechat-publisher-skill/
├── scripts/
│   └── publish.py          # Python 发布脚本
├── templates/
│   └── v5-simple.html      # HTML 模板
├── config/
│   └── default.json        # 配置文件
├── docs/
│   └── user_guide.md       # 用户使用手册
├── skill.md                # 技能定义
└── changelog.md           # 更新日志
```

---

## 💰 授权说明

| 版本 | 价格 | 功能 |
|------|------|------|
| **试用版** | 免费 | 50 次使用（约 1 个月） |
| **专业版** | 8.8 元 | 无限次使用 + 全部模板 + 优先支持 |

### 购买专业版

```bash
openclaw skill buy smart-wechat-publisher
```

### 激活专业版

```bash
openclaw skill activate smart-wechat-publisher YOUR_LICENSE_CODE
```

---

## 📞 技术支持

| 渠道 | 联系方式 | 响应时间 |
|------|----------|----------|
| **微信** | lylovejava | 1 小时内 |
| **公众号** | 心识孤独的猎手 | 2 小时内 |
| **邮箱** | 403914291@qq.com | 24 小时内 |
| **GitHub** | Issues | 24 小时内 |

---

## 📖 文档

- [用户使用手册](docs/user_guide.md) - 完整的安装、配置、使用教程
- [技能定义](skill.md) - 技能功能和配置说明
- [更新日志](changelog.md) - 版本更新记录

---

## 🔐 配置说明

### 必需配置

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `app_id` | 公众号 AppID | `wxebff9eadface1489` |
| `app_secret` | 公众号密钥 | `44c10204ceb1bfb3f7ac096754976454` |

### 可选配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `schedule` | 发布时间 | `06:00` |
| `template` | 发布模板 | `v5-simple` |
| `news_count` | 新闻条数 | `15` |
| `timezone` | 时区 | `Asia/Shanghai` |
| `trial_count` | 试用次数 | `50` |

---

## 📊 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.1.2 | 2026-03-27 | 更新联系方式 |
| 1.1.1 | 2026-03-27 | 更新联系方式 |
| 1.1.0 | 2026-03-27 | 试用次数增加到 50 次 |
| 1.0.0 | 2026-03-26 | 初始版本 |

---

## ⚠️ 注意事项

1. **API 限制**: 微信公众号 API 需要认证
2. **Token 有效期**: 2 小时，自动刷新
3. **封面图**: 必须使用永久素材的 media_id
4. **发布频率**: 建议每天发布 1 次，避免频繁操作

---

## 📝 常见问题

### Q: 试用次数用完后怎么办？

A: 运行 `openclaw skill buy smart-wechat-publisher` 购买专业版，8.8 元永久买断。

### Q: 发布失败提示 Token 无效？

A: Token 有效期 2 小时，会自动刷新。如持续失败，检查 AppID 和 AppSecret 是否正确。

### Q: 如何修改发布时间？

A: 运行 `openclaw schedule smart-wechat-publisher 07:00` 修改为早上 7 点。

---

## 📄 许可证

本技能为商业软件，未经授权不得用于商业用途。

---

**作者：** 小蛋蛋  
**技术支持：** 403914291@qq.com  
**公众号：** 心识孤独的猎手
