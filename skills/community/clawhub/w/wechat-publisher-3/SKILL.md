---
name: 微信公众号发布器
description: 当用户需要发布微信公众号文章、查看热点、配置公众号参数、生成文章内容、或运营微信公众号相关任务时，自动激活此技能。触发词包括：发公众号、微信推文、草稿箱、AppID、AppSecret、公众号运营、热点文章、wx-publish。
version: 1.0.0
---

# 微信公众号发布器技能

## 核心能力

本插件为 WorkBuddy 提供完整的微信公众号内容生产和发布能力，包括：

1. **热点抓取与过滤**：实时获取微博/百度/知乎热搜，按用户关键词白名单评分
2. **AI文章生成**：基于选定热点自动生成1200-2000字高质量文章
3. **微信排版**：自动转换为微信公众号标准 HTML 排版
4. **一键发布**：调用微信草稿箱 API 直接发布
5. **定时任务**：支持每日定时自动运行

## 可用命令

| 命令 | 功能 |
|------|------|
| `/wx-setup` | 初始化配置（首次使用必须先运行） |
| `/wx-publish` | 自动抓取热点 → 生成文章 → 发布草稿箱 |
| `/wx-hotspot` | 查看今日热点排行，选题参考 |
| `/wx-diary` | 将自定义文字/Markdown 发布为公众号文章 |

## 配置文件说明

配置文件位于 `${CODEBUDDY_PLUGIN_ROOT}/config/user-config.json`，包含：

```json
{
  "wechat": {
    "appId": "wx...",           // 公众号AppID
    "appSecret": "...",         // 公众号AppSecret  
    "thumbMediaId": "...",      // 封面图素材ID
    "author": "WorkBuddy"       // 作者名（最多8字）
  },
  "keywords": {
    "primary": ["人工智能","AI","机器人"],   // 主关键词（高权重）
    "secondary": ["互联网","通信"],           // 次关键词（低权重）
    "exclude": ["明星","娱乐"]               // 排除关键词
  },
  "publish": {
    "targetTime": "07:00",       // 定时发布时间
    "minHeat": 50000,            // 最低热度门槛
    "contentStyle": "深度分析型" // 文章风格
  }
}
```

## 文章写作规范

每篇文章必须包含以下结构：

### 开头（钩子段）
用高亮引用块（蓝色左边框）引入话题，直接点出与读者的关联。不超过80字。

### 正文（3-5个章节）
每章节使用 `##` 二级标题，格式：蓝色左边框标题。章节内容类型：
- **事件还原**：发生了什么，数字化事实
- **深度分析**：为什么会这样，背后逻辑
- **对比/案例**：与其他行业/国家/时期对比
- **影响评估**：对目标读者（中小企业/个人）的实际影响

### 实用建议块
使用蓝绿渐变背景框，给出3条以上具体可操作的建议。

### 结尾（金句）
一句有力的话收尾，可以是：
- 行动呼吁型："早点下水，早点学会游泳"
- 哲理总结型："时代抛弃你时，不会打招呼"
- 反问升华型："你准备好了吗？"

## 排版样式规范

所有HTML内容使用以下基础样式：

```css
/* 容器 */
font-family: -apple-system,'PingFang SC','Microsoft YaHei',sans-serif;
max-width: 680px; margin: 0 auto; color: #1e293b;

/* 正文段落 */
font-size: 15px; line-height: 1.9; color: #374151;
margin: 12px 0; text-indent: 2em;

/* 二级标题 */
font-size: 19px; font-weight: 700; color: #1d4ed8;
border-left: 4px solid #3b82f6; padding-left: 12px;

/* 引用块 */
border-left: 4px solid #7c3aed; background: #faf5ff;
padding: 14px 20px; border-radius: 0 10px 10px 0;

/* 提示框（橙色） */
background: #fff7ed; border: 1px solid #fed7aa;
border-radius: 12px; padding: 16px 20px;

/* 建议框（蓝绿渐变） */
background: linear-gradient(135deg,#eff6ff,#f0fdf4);
border: 1px solid #bfdbfe; border-radius: 12px;
```

## 错误处理规范

| 错误类型 | 处理方式 |
|---------|---------|
| Token 获取失败 | 提示检查 AppID/AppSecret，输出完整错误码 |
| 无匹配热点 | 展示全部热点候选，让用户手动选择 |
| 作者名超长 | 自动截断到8字，告知用户 |
| 封面图ID无效 | 发布时给出友好提示，建议重新上传素材 |
| 网络超时 | 重试一次，再失败则报错退出 |
