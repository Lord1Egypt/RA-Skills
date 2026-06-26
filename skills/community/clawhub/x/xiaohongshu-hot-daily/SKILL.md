---
name: xiaohongshu-hot-daily
description: "📕 小红书热榜日报 v3.1 - 使用浏览器获取真实数据！支持定时任务和数据分析。自媒体运营必备！免费使用，定制开发请联系作者。"
homepage: https://github.com/openclaw/xiaohongshu-hot-daily
metadata:
  {
    "openclaw":
      {
        "emoji": "📕",
        "requires": { "bins": ["python3", "agent-browser"] },
      },
  }
---

# 📕 小红书热榜日报 v3.1

使用浏览器方式获取小红书真实热门笔记数据！

## ✨ v3.1 新功能

- ✅ **真实数据获取** - 使用 agent-browser 浏览器方式
- ✅ **无需登录** - 直接获取探索页公开数据
- ✅ **智能分类** - 自动识别笔记分类
- ✅ **定时任务支持** - 每日自动收集数据
- ✅ **备用方案** - 浏览器不可用时使用模拟数据

## 📦 安装

```bash
# 安装技能
npx clawhub@latest install xiaohongshu-hot-daily

# 安装依赖 (agent-browser)
npm install -g agent-browser
agent-browser install
```

## 🚀 使用

```bash
# 获取 Top 10 热门笔记
python3 fetch_hot.py --top 10

# 生成摘要
python3 fetch_hot.py --top 20 --summary

# 导出 JSON
python3 fetch_hot.py --summary --output hot.json
```

## 📊 数据示例

```
[HOT] 小红书热榜 - 2026-03-29 11:36
================================================================================

#1 盘点我家那些收纳能力爆棚的柜子～
   [AUTHOR] 徐星星 | [CAT] 家居
   [LIKE] 9050
   [LINK] https://www.xiaohongshu.com/explore/63dba581000000001d01d5a7

#2 🔥台剧居然这么敢拍❗️一集一案❗️太生猛了
   [AUTHOR] 小叮做事小叮当 | [CAT] 娱乐
   [LIKE] 1.8万
   [LINK] https://www.xiaohongshu.com/explore/64a3e966000000003102ca49

#3 近日☘️一切和花相关🌷
   [AUTHOR] 杨采钰ORA | [CAT] 其他
   [LIKE] 8596
   [LINK] https://www.xiaohongshu.com/explore/63eb60fe000000001203d244
```

## 🔧 技术说明

### 数据获取方式

1. **优先使用 agent-browser** - 无头浏览器方式
2. **备用模拟数据** - 浏览器不可用时自动切换

### 支持的分类

| 分类 | 关键词 |
|------|--------|
| 穿搭 | 穿搭、搭配、服装、衣服、裙子 |
| 美食 | 美食、食谱、做饭、早餐、减脂 |
| 旅行 | 旅行、旅游、攻略、城市、景点 |
| 健身 | 健身、运动、瑜伽、锻炼、减肥 |
| 美妆 | 美妆、化妆、护肤、口红 |
| 家居 | 家居、装修、收纳、柜子 |
| 娱乐 | 明星、电视剧、电影、综艺 |

## ⚠️ 注意事项

- 需要安装 agent-browser CLI
- 首次运行会自动下载 Chromium 浏览器
- 数据来自小红书公开探索页，无需登录

## ⏰ 定时任务配置

使用 OpenClaw cron 功能设置自动收集：

```
任务名：📕 小红书热榜收集
时间：每天 09:30
功能：使用浏览器自动获取小红书热榜数据
保存位置：hot_reports/xiaohongshu_report_日期.json
```

## 💰 定制服务

**如需更多小红书数据服务，请联系作者：**

- 🔧 **数据采集**：定时采集、历史数据
- 📊 **数据分析**：爆款分析、竞品监控
- 🤖 **自动化部署**：多平台数据聚合

**联系方式：**
- 📱 QQ：2595075878
- 📧 邮箱：2595075878@qq.com

## ⚖️ 免责声明

本技能所获取的数据来自小红书公开网页内容，仅用于个人学习和技术研究目的。

- 📌 **数据来源**：小红书公开探索页面（无需登录）
- 📌 **非商业性质**：本技能为开源免费工具，不涉及任何商业引导
- 📌 **版权说明**：所有数据内容的版权归小红书所有
- 📌 **使用限制**：请遵守小红书用户协议，禁止用于非法用途
- 📌 **免责条款**：本技能按"现状"提供，使用者需自行承担使用风险

## 📄 许可证

MIT License
