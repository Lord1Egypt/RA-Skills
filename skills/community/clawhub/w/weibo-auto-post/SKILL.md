---
name: weibo-auto-post
description: 微博自动发布 skill。通过 PIL 生成配图（温暖风/科技感/深夜风/对比卡）→ 剪贴板粘贴图片 → 浏览器自动化发布。触发场景：帮我发微博、发布定时微博、生成微博配图、设置微博定时发布任务。
---

# Weibo Auto Post

全自动微博发布 workflow：**内容创作 → 配图生成 → 浏览器发布 → 临时文件清理**。

## 发布流程

### Step 1：生成配图

```bash
python <skill_dir>/scripts/make_card.py --text "微博文案内容" --style warmth --output "C:\Users\13113\Pictures\weibo_card.png"
```

支持的风格（`--style`）：
- `warmth`：温暖生活风，橙色调，1080×1350，适合日常/职场话题
- `tech`：科技感深色风，深蓝底+金色字，适合AI工具/身份标签内容
- `midnight`：深夜风，深色背景+蓝绿渐变，适合深夜互动话题
- `contrast`：左右对比卡（红vs绿），适合工具实测/辩论话题，1080×675

### Step 2：发布到微博（浏览器自动化）

```bash
python <skill_dir>/scripts/publish.py --image "C:\Users\13113\Pictures\weibo_card.png"
```

**前置要求**：
- Chrome/Edge 已安装且已安装 Playwright：`playwright install chromium`
- 微博账号已登录，发布框（`weibo.com/compose`）可正常访问

**工作原理**：截图定位发布框坐标 → 剪贴板粘贴图片 → Ctrl+V → 等待验证 → 输入文字 → 点击发布。

**如果坐标偏移**，可在 cron job prompt 中用 `session_status` 确认当天浏览器窗口位置，或手动微调坐标参数。

### Step 3：清理临时文件

发布完成后自动执行：
```powershell
Get-ChildItem "C:\Users\13113\Pictures\weibo_*.png" | Remove-Item -Force
Get-ChildItem "$env:TEMP\openclaw_screenshot_*.png" -EA SilentlyContinue | Remove-Item -Force
```

## 内容策略模板

### 三层话题标签体系
- **常驻**：`#AI科普#` `#AI生活观察#`
- **流量**：`#AI时代#` `#职场#` `#效率#` `#日常#` `#科技#`
- **互动**：`#看法#` `#battle#` `#分享#`

### 内容类型（见 `references/content_types.md`）

| 时间段 | 类型 | 核心目标 |
|--------|------|---------|
| 8:00 | 早间热点速评 | 抢热搜流量，观点鲜明 |
| 11:00 | AI×生活 | 场景共鸣，语言生活化 |
| 14:00 | 身份标签型 | 引发转发，显示读者身份 |
| 15:30 | AI工具实战 | 实操教程，收藏率高 |
| 17:00 | 争议辩论型 | AB投票，评论区battle |
| 21:00 | 深夜互动 | 开放式问题，轻松语气 |

## 定时任务配置

用 cron 创建定时任务（见 `references/cron_guide.md`）。每次发布需指定：
- 内容类型（从上面表格选）
- 具体话题（搜索当天热点确定）
- 配图风格

## 常见问题

**Q: 图片无法粘贴？**
→ 检查剪贴板是否有图片内容；确认微博页面已加载完成。

**Q: 坐标点击不准？**
→ 微博页面窗口位置因人而异，首次使用需要手动校准坐标。cron job prompt 中加入"发布前截图确认发布框可见"。

**Q: 账号被风控限制？**
→ 微博触发安全机制时页面会跳转提示，需在手机/网页端解除限制后再发布。

## 脚本说明

- `scripts/make_card.py`：生成微博配图，支持4种风格
- `scripts/publish.py`：浏览器自动化发布（截图定位 → 粘贴 → 验证 → 发布）
- `scripts/cleanup.py`：清理临时图片文件
- `references/content_types.md`：各内容类型的写作要点
- `references/cron_guide.md`：定时任务配置参考
