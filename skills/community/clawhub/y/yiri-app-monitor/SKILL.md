---
name: yiri-app-monitor
description: "查询一日记账 App 版本信息。当用户问起一日记账版本、版本更新、app最新版本时使用。使用 Playwright 从华为 AppGallery 抓取实时版本信息。"
homepage: https://github.com/taobaoaz/astrbot_plugin_harmony_app_monitor
metadata:
  {
    "openclaw": {
      "emoji": "📱",
      "requires": ["python", "playwright", "chromium"]
    }
  }
---

# 一日记账 App 版本监控 Skill

## 使用场景

当 QQ 用户询问以下内容时自动触发：
- "一日记账版本"
- "一日记账更新"
- "一日记账最新版本"
- "一日记账 app 版本"
- "一日记账有更新吗"

## 触发关键词

- 一日记账 + 版本
- 一日记账 + 更新
- 一日记账 app
- 一日记账最新

## 命令格式

无需命令，直接询问即可。示例：

```
Q: 一记账版本多少？
A: 📱 一日记账 当前版本：8.0.1
   🔗 https://appgallery.huawei.com/app/detail?id=com.ericple.onebill
   ⏰ 2026-04-03 10:45:37
```

## 技术实现

- 使用 Playwright + Chromium headless 浏览器
- 访问华为 AppGallery 页面
- CSS 选择器：`span.content-value`
- 超时：30秒（页面加载）+ 20秒（选择器等待）

## 脚本路径

```
yiri-app-monitor/scripts/check_version.py
```

## 返回格式

```json
{
  "app_name": "一日记账",
  "app_id": "com.ericple.onebill",
  "version": "8.0.1",
  "url": "https://appgallery.huawei.com/app/detail?id=com.ericple.onebill",
  "checked_at": "2026-04-03 10:45:37"
}
```

## 依赖安装

如 Playwright 或 Chromium 未安装：

```bash
pip install playwright
playwright install chromium
```

## 备注

- 版本数据来源于华为 AppGallery 官方页面
- 无需 API Key，完全免费
- 支持定时检查（可结合 cron）
