# Stock Master Pro - ClawHub 上传指南

## 📦 打包文件

**压缩包位置**: `~/.openclaw/workspace/skills/stock-master-pro-v0.0.1.tar.gz`

**文件大小**: 55KB

**包含内容**:
- ✅ 所有脚本（9 个.mjs 文件）
- ✅ Web Dashboard（HTML/JS/CSS）
- ✅ 文档（README/INSTALL/SETUP/USAGE 等）
- ✅ 元数据（_meta.json）
- ✅ 依赖检查脚本

**排除内容**:
- ❌ stocks/ 目录（用户持仓数据）
- ❌ build/ 目录（临时文件）
- ❌ .git/ 目录
- ❌ 测试文件（test*.html, diag.html）
- ❌ *.log 日志文件

---

## 🔒 敏感信息检查

已检查以下敏感信息：

- ✅ **无硬编码 API Key** - 所有脚本通过环境变量读取 QVERIS_API_KEY
- ✅ **无个人配置** - holdings.json 已排除
- ✅ **无本地路径** - 所有路径使用相对路径

**QVeris Key 说明**:
- QVeris API Key 存储在 QVeris 技能的配置中
- Stock Master Pro 通过 `process.env.QVERIS_API_KEY` 读取
- 压缩包中不包含任何 API Key

---

## 📤 上传到 ClawHub

### 步骤 1: 准备技能信息

参考 `_meta.json` 填写以下信息：

```yaml
名称：stock-master-pro
显示名称：A 股大师 Pro
版本：0.0.1
描述：基于 QVeris AI 的 A 股实时持仓监控与深度复盘系统
作者：yaoha
License: MIT
分类：金融、数据分析、可视化
```

### 步骤 2: 上传压缩包

1. 访问 [ClawHub 技能发布页面](https://clawhub.com/skills/create)
2. 上传 `stock-master-pro-v0.0.1.tar.gz`
3. 填写技能信息

### 步骤 3: 设置依赖

**依赖技能**: QVeris

**依赖说明**:
```
本技能依赖 QVeris AI 获取 A 股实时数据，包括行情、资金流向、龙虎榜等。

如果用户未安装 QVeris，安装时会提示：
"请先安装 QVeris 技能：https://clawhub.com/skills/qveris?ref=stock-master-pro"
```

**依赖检查脚本**: `scripts/check_dependency.mjs`

### 步骤 4: 设置分享链接

**QVeris 分享链接**（用于依赖引导）:
```
https://clawhub.com/skills/qveris?ref=stock-master-pro
```

这个链接会：
1. 引导用户安装 QVeris
2. 记录推荐来源（ref=stock-master-pro）
3. 帮助用户快速完成依赖安装

### 步骤 5: 填写功能特性

```
✅ 三时段复盘（午盘 12:30/尾盘 15:30/收盘 16:00）
✅ 板块深度分析（为什么涨、持续性评级、怎么跟进）
✅ 强势股评分推荐（100 分制，含推荐理由）
✅ 持仓监控（主力意图、技术位置、目标价/止损价）
✅ 龙虎榜监控（机构/游资/北向资金分析）
✅ 财报日历提醒
✅ 公告监控（持仓股票重大公告）
✅ 趋势选股器（右侧交易、温和放量、趋势向上）
✅ Web Dashboard（专业金融终端风格，10 秒自动刷新）
```

### 步骤 6: 设置 Crontab 任务

在 ClawHub 后台配置以下定时任务：

| 任务 | Schedule | 脚本 |
|------|----------|------|
| 午盘复盘 | `30 12 * * 1-5` | `scripts/noon_review.mjs` |
| 尾盘复盘 | `30 15 * * 1-5` | `scripts/afternoon_review.mjs` |
| 收盘总结 | `0 16 * * 1-5` | `scripts/close_review.mjs` |
| 公告监控 | `*/10 9-15 * * 1-5` | `scripts/announcement_monitor.mjs` |

---

## 📋 安装流程测试

### 用户安装流程

1. **用户在 ClawHub 发现技能**
   - 搜索 "stock-master-pro" 或 "A 股大师"

2. **点击安装**
   - 系统自动检查依赖（QVeris）

3. **依赖检查**
   - ✅ 已安装 QVeris → 继续安装
   - ❌ 未安装 QVeris → 显示提示：
     ```
     ⚠️ 需要安装 QVeris 技能
     
     本技能依赖 QVeris AI 获取 A 股实时数据。
     
     [安装 QVeris] [取消]
     ```

4. **安装完成**
   - 显示安装成功
   - 显示快速开始指南

5. **用户配置**
   - 编辑 `stocks/holdings.json` 添加持仓
   - 启动 Web Dashboard

---

## 🔗 分享链接

### QVeris 依赖引导链接

```
https://clawhub.com/skills/qveris?ref=stock-master-pro
```

**用途**:
- 安装指南中的依赖安装链接
- 错误提示中的快速安装链接
- 文档中的推荐链接

**参数说明**:
- `ref=stock-master-pro` - 记录推荐来源，用于统计

### Stock Master Pro 分享链接（发布后）

```
https://clawhub.com/skills/stock-master-pro
```

**带推荐的分享链接**:
```
https://clawhub.com/skills/stock-master-pro?ref=yaoha
```

---

## 📊 版本发布检查清单

- [x] 版本号更新（0.0.1）
- [x] _meta.json 元数据完整
- [x] CHANGELOG.md 更新
- [x] INSTALL.md 安装指南
- [x] 敏感信息检查（无 API Key）
- [x] 依赖检查脚本（check_dependency.mjs）
- [x] 打包文件（stock-master-pro-v0.0.1.tar.gz）
- [ ] ClawHub 上传
- [ ] 依赖配置（QVeris）
- [ ] Crontab 任务配置
- [ ] 发布测试（全新环境安装）

---

## 🎯 发布后任务

1. **监控安装反馈**
   - 关注 ClawHub 评论
   - 及时回复用户问题

2. **收集使用数据**
   - 安装量
   - 活跃度
   - 用户反馈

3. **准备 0.0.2 版本**
   - WebSocket 实时推送
   - 多持仓组合管理
   - 导出复盘报告

---

## 📞 联系支持

- **GitHub**: https://github.com/yaoha/stock-master-pro
- **Email**: yaoha@example.com
- **ClawHub**: 技能页面评论区

---

**祝发布顺利！** 🚀
