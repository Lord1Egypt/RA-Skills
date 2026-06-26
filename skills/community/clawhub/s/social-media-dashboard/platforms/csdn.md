# CSDN 数据采集

## 概述

通过浏览器自动化方式采集 CSDN 博客后台数据，包括作品数据、收益数据、粉丝数据等核心指标。

## 数据采集页面

| 页面 | URL | 数据内容 |
|-----|-----|---------|
| 作品数据 | `https://mp.csdn.net/mp_blog/analysis/article/all` | 文章阅读量、点赞、评论、收藏、转发 |
| 收益数据 | `https://mp.csdn.net/mp_others/analysis/rewardall` | 总收益、可提现、收益趋势 |
| 粉丝数据 | `https://mp.csdn.net/mp_others/analysis/fans/dataOverview` | 粉丝总数、新增粉丝、活跃度 |

## 采集流程

### 前置检查

1. 检测可用浏览器（Chrome/Safari）
2. 检测浏览器 AppleScript 权限
3. 检测 CSDN 登录状态

### Chrome 采集脚本

#### 作品数据

```bash
osascript <<'EOF'
tell application "Google Chrome"
    set URL of active tab of front window to "https://mp.csdn.net/mp_blog/analysis/article/all"
    delay 3
    set pageText to execute active tab of front window javascript "document.body.innerText"
    return pageText
end tell
EOF
```

#### 收益数据

```bash
osascript <<'EOF'
tell application "Google Chrome"
    set URL of active tab of front window to "https://mp.csdn.net/mp_others/analysis/rewardall"
    delay 3
    set pageText to execute active tab of front window javascript "document.body.innerText"
    return pageText
end tell
EOF
```

#### 粉丝数据

```bash
osascript <<'EOF'
tell application "Google Chrome"
    set URL of active tab of front window to "https://mp.csdn.net/mp_others/analysis/fans/dataOverview"
    delay 3
    set pageText to execute active tab of front window javascript "document.body.innerText"
    return pageText
end tell
EOF
```

### Safari 采集脚本

#### 作品数据

```bash
osascript <<'EOF'
tell application "Safari"
    set URL of front document to "https://mp.csdn.net/mp_blog/analysis/article/all"
    delay 3
    set pageText to do JavaScript "document.body.innerText" in front document
    return pageText
end tell
EOF
```

#### 收益数据

```bash
osascript <<'EOF'
tell application "Safari"
    set URL of front document to "https://mp.csdn.net/mp_others/analysis/rewardall"
    delay 3
    set pageText to do JavaScript "document.body.innerText" in front document
    return pageText
end tell
EOF
```

#### 粉丝数据

```bash
osascript <<'EOF'
tell application "Safari"
    set URL of front document to "https://mp.csdn.net/mp_others/analysis/fans/dataOverview"
    delay 3
    set pageText to do JavaScript "document.body.innerText" in front document
    return pageText
end tell
EOF
```

## 登录检测

访问 CSDN 创作者中心首页检测登录状态：

```bash
# Chrome
osascript <<'EOF'
tell application "Google Chrome"
    set URL of active tab of front window to "https://mp.csdn.net/"
    delay 3
    set pageText to execute active tab of front window javascript "document.body.innerText"
    if pageText contains "登录" then
        return "NOT_LOGGED_IN"
    else
        return "LOGGED_IN"
    end if
end tell
EOF

# Safari
osascript <<'EOF'
tell application "Safari"
    set URL of front document to "https://mp.csdn.net/"
    delay 3
    set pageText to do JavaScript "document.body.innerText" in front document
    if pageText contains "登录" then
        return "NOT_LOGGED_IN"
    else
        return "LOGGED_IN"
    end if
end tell
EOF
```

## 数据提取

从页面文本中提取关键数据：

### 作品数据页面提取

页面包含：
- 文章总数
- 总阅读量
- 总点赞数
- 总评论数
- 总收藏数
- 单篇文章详细数据（标题、阅读、点赞、评论、收藏、发布时间）

### 收益数据页面提取

页面包含：
- 累计收益
- 可提现金额
- 昨日收益
- 本月收益
- 收益趋势图表数据

### 粉丝数据页面提取

页面包含：
- 粉丝总数
- 今日新增粉丝
- 昨日新增粉丝
- 近7天/30天粉丝增长趋势
- 活跃粉丝比例

## 数据示例

```json
{
  "articles": {
    "total_count": 156,
    "total_read": 890234,
    "total_like": 4567,
    "total_comment": 890,
    "total_favorite": 1234,
    "recent_articles": [
      {
        "title": "深入理解 JavaScript 闭包",
        "read": 12345,
        "like": 89,
        "comment": 23,
        "favorite": 45,
        "publish_time": "2026-03-15"
      }
    ]
  },
  "income": {
    "total": 2345.67,
    "available": 567.89,
    "yesterday": 12.34,
    "this_month": 234.56
  },
  "fans": {
    "total": 12345,
    "today_new": 56,
    "yesterday_new": 45,
    "trend_7d": [
      { "date": "2026-03-13", "count": 12233 },
      { "date": "2026-03-14", "count": 12289 },
      { "date": "2026-03-15", "count": 12345 }
    ]
  }
}
```

## 频率限制

- 每次请求间隔 ≥ 3 秒
- 避免频繁刷新，可能触发风控

## 错误处理

| 情况 | 说明 | 处理方式 |
|-----|------|---------|
| 未登录 | 页面显示登录按钮 | 引导用户登录 CSDN |
| 权限不足 | 部分数据需要创作者等级 | 提示用户升级创作者等级 |
| 页面加载失败 | 网络问题 | 重试或提示检查网络 |

## 实现步骤

当用户请求查看 CSDN 数据时：

1. **检查登录状态**
   - 访问 `https://mp.csdn.net/`
   - 检测页面是否包含登录按钮

2. **引导登录**（如未登录）
   - 打开 CSDN 登录页面
   - 等待用户完成登录

3. **采集数据**
   - 按顺序访问作品、收益、粉丝页面
   - 每次请求间隔 3 秒

4. **生成报告**
   - 整合数据生成 Markdown 报告
   - 对比历史数据（如有）

## 安全提示

- 不要存储用户密码
- 数据仅保存在用户本地
- 提醒用户不要分享登录凭证
