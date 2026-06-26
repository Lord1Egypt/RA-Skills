# 知乎数据采集

## 概述

通过浏览器自动化方式采集知乎创作者中心数据，包括内容数据、收益数据等核心指标。

## 数据采集页面

### 内容数据

| 页面 | URL | 数据内容 |
|-----|-----|---------|
| 内容总览 | `https://www.zhihu.com/creator/analytics/work/all` | 综合数据、播放量、阅读量、互动 |
| 回答数据 | `https://www.zhihu.com/creator/analytics/work/answer` | 回答阅读、点赞、评论、收藏 |
| 想法数据 | `https://www.zhihu.com/creator/analytics/work/pin` | 想法浏览、互动数据 |
| 文章数据 | `https://www.zhihu.com/creator/analytics/work/article` | 文章阅读、点赞、评论、收藏 |
| 视频数据 | `https://www.zhihu.com/creator/analytics/work/zvideo` | 视频播放、点赞、评论、分享 |

### 收益数据

| 页面 | URL | 数据内容 |
|-----|-----|---------|
| 收益分析 | `https://www.zhihu.com/creator/income-analysis` | 总收益、昨日收益、本月收益、收益趋势 |

## 采集流程

### 前置检查

1. 检测可用浏览器（Chrome/Safari）
2. 检测浏览器 AppleScript 权限
3. 检测知乎登录状态

### Chrome 采集脚本

#### 内容总览

```bash
osascript <<'EOF'
tell application "Google Chrome"
    set URL of active tab of front window to "https://www.zhihu.com/creator/analytics/work/all"
    delay 4
    set pageText to execute active tab of front window javascript "document.body.innerText"
    return pageText
end tell
EOF
```

#### 回答数据

```bash
osascript <<'EOF'
tell application "Google Chrome"
    set URL of active tab of front window to "https://www.zhihu.com/creator/analytics/work/answer"
    delay 4
    set pageText to execute active tab of front window javascript "document.body.innerText"
    return pageText
end tell
EOF
```

#### 想法数据

```bash
osascript <<'EOF'
tell application "Google Chrome"
    set URL of active tab of front window to "https://www.zhihu.com/creator/analytics/work/pin"
    delay 4
    set pageText to execute active tab of front window javascript "document.body.innerText"
    return pageText
end tell
EOF
```

#### 文章数据

```bash
osascript <<'EOF'
tell application "Google Chrome"
    set URL of active tab of front window to "https://www.zhihu.com/creator/analytics/work/article"
    delay 4
    set pageText to execute active tab of front window javascript "document.body.innerText"
    return pageText
end tell
EOF
```

#### 视频数据

```bash
osascript <<'EOF'
tell application "Google Chrome"
    set URL of active tab of front window to "https://www.zhihu.com/creator/analytics/work/zvideo"
    delay 4
    set pageText to execute active tab of front window javascript "document.body.innerText"
    return pageText
end tell
EOF
```

#### 收益数据

```bash
osascript <<'EOF'
tell application "Google Chrome"
    set URL of active tab of front window to "https://www.zhihu.com/creator/income-analysis"
    delay 4
    set pageText to execute active tab of front window javascript "document.body.innerText"
    return pageText
end tell
EOF
```

### Safari 采集脚本

#### 内容总览

```bash
osascript <<'EOF'
tell application "Safari"
    set URL of front document to "https://www.zhihu.com/creator/analytics/work/all"
    delay 4
    set pageText to do JavaScript "document.body.innerText" in front document
    return pageText
end tell
EOF
```

#### 回答数据

```bash
osascript <<'EOF'
tell application "Safari"
    set URL of front document to "https://www.zhihu.com/creator/analytics/work/answer"
    delay 4
    set pageText to do JavaScript "document.body.innerText" in front document
    return pageText
end tell
EOF
```

#### 想法数据

```bash
osascript <<'EOF'
tell application "Safari"
    set URL of front document to "https://www.zhihu.com/creator/analytics/work/pin"
    delay 4
    set pageText to do JavaScript "document.body.innerText" in front document
    return pageText
end tell
EOF
```

#### 文章数据

```bash
osascript <<'EOF'
tell application "Safari"
    set URL of front document to "https://www.zhihu.com/creator/analytics/work/article"
    delay 4
    set pageText to do JavaScript "document.body.innerText" in front document
    return pageText
end tell
EOF
```

#### 视频数据

```bash
osascript <<'EOF'
tell application "Safari"
    set URL of front document to "https://www.zhihu.com/creator/analytics/work/zvideo"
    delay 4
    set pageText to do JavaScript "document.body.innerText" in front document
    return pageText
end tell
EOF
```

#### 收益数据

```bash
osascript <<'EOF'
tell application "Safari"
    set URL of front document to "https://www.zhihu.com/creator/income-analysis"
    delay 4
    set pageText to do JavaScript "document.body.innerText" in front document
    return pageText
end tell
EOF
```

## 登录检测

访问知乎创作者中心检测登录状态：

```bash
# Chrome
osascript <<'EOF'
tell application "Google Chrome"
    set URL of active tab of front window to "https://www.zhihu.com/creator"
    delay 3
    set pageText to execute active tab of front window javascript "document.body.innerText"
    if pageText contains "登录" or pageText contains "注册" then
        return "NOT_LOGGED_IN"
    else
        return "LOGGED_IN"
    end if
end tell
EOF

# Safari
osascript <<'EOF'
tell application "Safari"
    set URL of front document to "https://www.zhihu.com/creator"
    delay 3
    set pageText to do JavaScript "document.body.innerText" in front document
    if pageText contains "登录" or pageText contains "注册" then
        return "NOT_LOGGED_IN"
    else
        return "LOGGED_IN"
    end if
end tell
EOF
```

## 数据提取

### 内容总览页面提取

页面包含：
- 播放量/阅读量总计
- 互动数据（点赞、评论、收藏、分享）
- 关注转化数据
- 近期内容表现趋势

### 分类内容数据提取

**回答数据：**
- 回答总数
- 总阅读量
- 总点赞数
- 总评论数
- 高赞回答列表

**想法数据：**
- 想法总数
- 总浏览量
- 互动数据

**文章数据：**
- 文章总数
- 总阅读量
- 总点赞数
- 总评论数
- 总收藏数
- 热门文章列表

**视频数据：**
- 视频总数
- 总播放量
- 总点赞数
- 总评论数
- 总分享数

### 收益数据提取

页面包含：
- 累计收益
- 可提现金额
- 昨日收益
- 本月收益
- 收益构成（致知计划、好物推荐、品牌任务等）
- 收益趋势

## 数据示例

```json
{
  "overview": {
    "total_read": 1234567,
    "total_play": 890123,
    "total_like": 23456,
    "total_comment": 1234,
    "total_favorite": 5678,
    "total_share": 890
  },
  "answers": {
    "total_count": 234,
    "total_read": 567890,
    "total_like": 12345,
    "total_comment": 567
  },
  "articles": {
    "total_count": 45,
    "total_read": 345678,
    "total_like": 8901,
    "total_comment": 234,
    "total_favorite": 4567
  },
  "pins": {
    "total_count": 89,
    "total_view": 123456,
    "total_like": 2345
  },
  "videos": {
    "total_count": 12,
    "total_play": 123456,
    "total_like": 3456,
    "total_comment": 123,
    "total_share": 456
  },
  "income": {
    "total": 1234.56,
    "available": 567.89,
    "yesterday": 12.34,
    "this_month": 234.56
  }
}
```

## 频率限制

- 每次请求间隔 ≥ 3 秒
- 避免频繁刷新，可能触发风控

## 错误处理

| 情况 | 说明 | 处理方式 |
|-----|------|---------|
| 未登录 | 页面显示登录按钮 | 引导用户登录知乎 |
| 权限不足 | 部分数据需要创作者等级 | 提示用户升级创作者等级 |
| 页面加载失败 | 网络问题 | 重试或提示检查网络 |

## 实现步骤

当用户请求查看知乎数据时：

1. **检查登录状态**
   - 访问 `https://www.zhihu.com/creator`
   - 检测页面是否包含登录/注册按钮

2. **引导登录**（如未登录）
   - 打开知乎登录页面
   - 等待用户完成登录

3. **采集数据**
   - 按顺序访问内容总览、分类内容、收益页面
   - 每次请求间隔 3 秒

4. **生成报告**
   - 整合数据生成 Markdown 报告
   - 对比历史数据（如有）

## 安全提示

- 不要存储用户密码
- 数据仅保存在用户本地
- 提醒用户不要分享登录凭证
