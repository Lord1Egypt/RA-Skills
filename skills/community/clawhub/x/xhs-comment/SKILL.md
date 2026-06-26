---
name: xhs-comment-scraper
description: 小红书评论爬虫。当用户在聊天中发送一个小红书博主主页链接时，自动抓取该博主所有笔记下的评论区数据，保存为本地JSON文件，并生成分析可视化报告。触发条件：用户发送的链接包含 xiaohongshu.com/user/profile 或类似博主主页链接。
readme: README.zh.md
metadata:
  language: zh
  tags: [xiaohongshu, scraper, chinese, comments, browser]
  platform: windows
  requirements:
    bins: []
    npm: []
---

# 小红书评论爬虫 Skill

> ⚠️ **使用前必读**：本文档包含大量踩坑经验，执行前务必通读一遍"关键经验"章节。

---

## 工具选择（重要！）

**必须使用 `profile="openclaw"`，不要用 `profile="chrome"`！**

原因：Browser Relay 依赖 Gateway token，Gateway 重启后 token 失效，扩展无法重连，需要用户手动重新配对，体验差且不稳定。

正确方式：
```
browser(action=start, profile="openclaw")          # 启动独立Chrome
browser(action=navigate, profile="openclaw", ...)  # 操作小红书
```

用户需要在这个独立的 Chrome 窗口里扫码登录小红书一次，之后全程自动。

---

## 数据格式

每篇笔记输出一个 JSON 文件，文件名格式：`xhs_comments_{博主名}_{note_id}_{timestamp}.json`

JSON 结构：
```json
{
  "blogger": { "name": "博主昵称", "profile_url": "主页URL" },
  "note": {
    "id": "笔记ID（URL末尾那段）",
    "title": "笔记标题",
    "url": "笔记详情页URL"
  },
  "comments": [
    {
      "author": "评论者昵称",
      "content": "评论内容原文（原文保留，不做截断）",
      "time": "评论时间字符串，如'3天前'或'2025-10-23'",
      "likes": 42
    }
  ],
  "scraped_at": "2026-03-24T15:00:00",
  "total_comments": 100
}
```

保存路径：`C:\Users\Downloads\xhs_comments\`

---

## ⚠️ 关键经验（踩坑总结，执行前必读）

### 1. Vue 渲染：DOM 选择器全部失效

小红书是 Vue 动态渲染，JS 的 `querySelector` / `getElementById` 等 DOM API 全部无效。

**唯一可靠的方式：`innerText`**

```javascript
// ✅ 正确：用 innerText 获取渲染后的纯文本
browser(action=act, kind=evaluate, fn="document.body.innerText")

// ❌ 错误：DOM 选择器全部返回空
document.querySelector('.comment-item')  // 无效
```

获取文本后，按固定格式解析评论——用户名、评论内容、时间、点赞数都在文本流中按固定顺序排列。

### 2. "展开N条回复"按钮必须主动点击

小红书评论有折叠，只有展开才会加载完整嵌套评论链。

```javascript
// 点击所有"展开N条回复"按钮
var btns = Array.from(document.querySelectorAll('*')).filter(
  e => e.textContent.match(/^展开 \d+ 条回复$/)
);
btns.forEach(b => { try { b.click(); } catch(e) {} });
```

### 3. 笔记 URL 格式

- **图文笔记**：`/explore/{noteId}` 可直接访问
- **视频笔记**：URL 格式不同，部分可能需要 `navigate` 后 JS 点击
- **置顶笔记**：在笔记列表 `a[href*="/user/profile/{userId}/"]` 中的前几条

### 4. 验证码是常态

高频访问小红书必然触发风控验证码。此时：
- 页面 URL 会变成 `/website-login/captcha?`
- **不要强求自动通过**——提示用户在浏览器窗口中手动完成验证
- 完成后继续，无需刷新页面

### 5. PowerShell 粘符问题

PowerShell 不支持 `&&` 语法，会报 `Unexpected token` 错误。

**所有命令行全部用 `;` 分隔，或直接用 Python 执行：**
```
# ❌ 错误
python script.py && echo done

# ✅ 正确
python script.py; echo done

# 最佳：直接用 Python
python script.py
```

### 6. Python 文件写入编码

PowerShell 重定向和 subprocess 调用默认 GBK，会导致中文文件名乱码。

**所有文件操作必须显式指定 UTF-8：**
```python
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
```

读取时加 `errors='replace'` 容忍乱码：
```python
with open(path, 'r', encoding='utf-8', errors='replace') as f:
    data = json.load(f)
```

### 7. matplotlib 不支持 emoji

STSong / SimHei 等中文字体均不含 emoji 字形，图表中会出现字形缺失警告（`Glyph missing`）。

**解决：matplotlib 图用纯文字标签，emoji 只用于 HTML 页面。**

---

## 完整工作流

### 第1步：初始化浏览器

```
browser(action=start, target=host, profile=openclaw)
browser(action=navigate, target=host, profile=openclaw,
        url=<用户发送的主页链接>)
```

告知用户：需要在打开的 Chrome 窗口中用小红书 App 扫码登录。

### 第2步：获取笔记列表

页面加载完成后，用 JS 提取所有笔记链接：

```javascript
var noteLinks = document.querySelectorAll(
  'a[href*="/user/profile/{userId}/"]'
);
// 遍历，提取 href 和 noteId
noteLinks.forEach(link => {
  var href = link.getAttribute('href');
  // href 格式：/user/profile/59757acd.../69bf6c43000000002800807a
  var parts = href.split('/');
  var noteId = parts[parts.length - 1].split('?')[0];
  // 获取标题（附近元素的文本）
  var parent = link.closest('[class*="note"], div');
});
```

注意：置顶笔记在列表最前面，`index=0` 对应第一条。

### 第3步：逐篇抓取评论

对每篇笔记：

1. **进入笔记详情**
   - `browser(action=act, kind=evaluate, fn="noteLinks[i].click()")`
   - 等待 5 秒：`browser(action=act, kind=wait, timeMs=5000)`

2. **验证是否正确进入**
   - 检查 URL 是否变为 `/explore/{noteId}` 或笔记详情页
   - 若 URL 仍为主页，说明点击未生效，重试

3. **展开回复 + 滚动**
   ```javascript
   // 展开所有回复
   var btns = Array.from(document.querySelectorAll('*')).filter(
     e => e.textContent.match(/^展开 \d+ 条回复$/)
   );
   btns.forEach(b => { try { b.click(); } catch(e) {} });
   // 滚动加载
   window.scrollBy(0, 800);
   ```

4. **提取评论**（核心！）
   ```javascript
   var bodyText = document.body.innerText;
   // bodyText 格式示例：
   // 评论者昵称
   // 评论内容...
   // 3天前
   // 赞 42
   // ---
   // 评论者2
   // 评论内容2...
   ```
   用换行符 `\n` 分割，按固定模式解析（用户名 → 内容 → 时间 → 点赞 → 分隔线）。

5. **返回笔记列表**
   ```javascript
   history.back();  // 或重新 navigate 到主页
   ```

### 第4步：保存 JSON

```python
import json, os
from datetime import datetime

data = {
    "blogger": {"name": "...", "profile_url": "..."},
    "note": {"id": "...", "title": "...", "url": "..."},
    "comments": [...],
    "scraped_at": datetime.now().isoformat(),
    "total_comments": len(comments)
}

out_dir = os.path.join(os.path.expanduser("~"), "Downloads", "xhs_comments")
os.makedirs(out_dir, exist_ok=True)
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"xhs_comments_{博主名}_{note_id}_{ts}.json"
with open(os.path.join(out_dir, filename), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"Saved: {filepath}")
```

### 第5步：生成分析报告（扩展任务）

用户可能会要求生成可视化分析。在 `Downloads\xhs_comments_analysis\` 目录生成：

1. **分析脚本**（写到临时路径，执行后清理）：
   ```python
   # -*- coding: utf-8 -*-
   import os, json, re
   from collections import Counter
   import jieba
   import matplotlib; matplotlib.use('Agg')
   import matplotlib.pyplot as plt
   from wordcloud import WordCloud
   # 中文字体
   FONT = r"C:\Windows\Fonts\STSONG.TTF"
   plt.rcParams['font.sans-serif'] = ['STSong', 'SimHei']
   plt.rcParams['axes.unicode_minus'] = False
   ```

2. **HTML 报告**（纯 JS，无 Python 模板引擎）：
   - 嵌入评论数据为 `ALL_NOTES` JSON 变量
   - 双笔记对照阅读：两个 `<select>` 下拉框
   - 关键词搜索：用 `data-content` 属性存储原文，JS 高亮匹配

3. **生成顺序**：
   - 先生成图表 PNG（matplotlib / WordCloud）
   - 再生成 HTML（引用本地图片路径）
   - 最后用 `Start-Process` 打开

---

## 错误处理

| 场景 | 处理方式 |
|------|---------|
| 页面加载失败 | 重试 2 次，每次等待 5 秒 |
| 评论数量为 0 | 记录，跳过，继续下一篇 |
| 验证码拦截 | 提示用户在浏览器窗口中完成，任务暂停等待 |
| 笔记已删除（404） | 跳过，继续下一篇 |
| 滚动后内容不变 | 判定为已加载完毕，停止滚动 |
| URL 格式不对 | JS 点击进入，不用直接 navigate |
| innerText 提取为空 | 等待更长时间，或截图排查 |
| Python 脚本报错 | 用 Python 重写逻辑，避免 shell 转义 |

---

## 依赖

- browser tool (`profile="openclaw"`，**不是 "chrome"**）
- Python 3（jieba + matplotlib + wordcloud）
- 中文字体：`C:\Windows\Fonts\STSONG.TTF`
- 用户需要在弹出的 Chrome 窗口中扫码登录小红书一次

---

## 快速检查清单（每次执行前）

- [ ] 使用 `profile="openclaw"` 而非 `profile="chrome"`
- [ ] 提取笔记列表用 JS `querySelectorAll` + `href` 解析
- [ ] 进入笔记详情用 JS `element.click()`，不用直接 navigate
- [ ] 提取评论用 `document.body.innerText`，不用 DOM 选择器
- [ ] 展开回复：主动点击所有"展开N条回复"按钮
- [ ] 验证码：告知用户手动完成，不要自动重试
- [ ] JSON 保存：`encoding='utf-8'` 显式指定
- [ ] PowerShell 命令用 `;` 而非 `&&`
- [ ] 截图备选：每篇笔记首次进入时截图，提取失败时排查
