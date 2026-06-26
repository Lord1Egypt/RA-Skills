# 调研平台操作指南

> 阶段 0 精准调研和维度 2 定期审美积累的具体操作方法。

---

## 平台 A：Dribbble（设计灵感）

**为什么用**：高质量设计作品聚集地，3D Clay / 插画 / 卡片设计参考最多。

**注意**：Dribbble 审美 ≠ 小红书审美。Dribbble 追求设计完美度，小红书追求"朋友在分享"。

### 操作流程

```bash
# 1. 打开搜索
agent-browser open "https://dribbble.com/search/<关键词>"

# 2. 搜索关键词模板
#    - "3d clay style <主题>"
#    - "social media card <主题>"
#    - "tech product card cover"
#    - "minimal infographic card"
#    - "character illustration cute"
#    - "<品牌名> brand design"

# 3. 浏览 + 截图
agent-browser screenshot "dribbble-<关键词>-1.png"
agent-browser scroll down 500
agent-browser screenshot "dribbble-<关键词>-2.png"
```

### 注意事项
- 关键词**必须用英文**
- 不需要登录
- 每个关键词至少看 2 屏（20-30 个作品）
- 高赞（❤️ 100+）和高浏览（👁 50k+）重点记录
- **陷阱**：Dribbble 的"好看"≠ 小红书的"高赞"

---

## 平台 B：小红书（竞品调研）

**为什么用**：直接看同赛道什么封面数据好 — 最真实的反馈。

> ⚠️ **绝对禁止登录用户的小红书账号！**
> - 无登录状态可以浏览和搜索
> - 登录后 headless 浏览器容易被识别为机器人，有账号风险
> - 弹出登录弹窗 → 直接关闭，继续浏览
> - 不要注入任何小红书相关 cookies

### 操作流程

```bash
# 方法 1（推荐）：web_search 搜索
web_search "site:xiaohongshu.com <关键词>"

# 方法 2：agent-browser 直接访问（不登录！）
agent-browser open "https://www.xiaohongshu.com/search_result?keyword=<关键词>"
# 弹出登录弹窗 → 关闭继续看
# 安全验证/IP 风险 → 放弃，改用方法 1

# 方法 3：web_fetch 抓取特定帖子
web_fetch "https://www.xiaohongshu.com/explore/<帖子ID>" "分析封面设计特征"
```

### 搜索关键词策略
- 直接主题词：如 "AI工具推荐"、"效率工具"
- 赛道泛词：如 "学习方法"、"AI教程"
- 竞品账号名

### 必须记录

| 记录项 | 说明 |
|--------|------|
| 作者 + 赞数 | 数据是最硬的参考 |
| 封面类型 | 真人出镜 / 产品截图 / Logo 矩阵 / 文字卡 / 3D 插画 |
| 封面关键特征 | 颜色、字体、构图、元素 |
| 为什么数据好 | "真实感强" / "信息直给" / "有态度" |
| 能不能借鉴 | 具体可以借鉴哪个元素 |

**数量要求**：至少看 10-15 个帖子，精选 5+ 条

---

## 平台 C：品牌官网（品牌视觉分析）

**为什么用**：如果帖子涉及某个品牌/产品，必须去官网看设计语言。

### 操作流程

```bash
# 1. 打开品牌官网
agent-browser open "https://<品牌官网>"
agent-browser wait 5000
agent-browser screenshot "<品牌>-homepage.png"

# 2. 提取设计语言
agent-browser eval "JSON.stringify({
  fonts: getComputedStyle(document.querySelector('h1')).fontFamily,
  bodyFont: getComputedStyle(document.querySelector('p')).fontFamily,
  bgColor: getComputedStyle(document.body).backgroundColor
})"
```

### 必须提取

| 元素 | 怎么获取 |
|------|---------|
| 品牌主色 | 看 logo、按钮、高亮色 |
| 背景色 | JS 获取 body 背景色 |
| 字体 | JS 获取 h1/p 的 fontFamily |
| Logo 精确描述 | ⚠️ 必须截图确认，不能凭想象 |
| 排版哲学 | 留白 / 信息密度 / 极简 vs 丰富 |
| 情绪/调性 | 冷冰冰 / 温暖 / 科技感 / 人文感 |

---

## 平台 D：Pinterest（补充灵感，可选）

**什么时候用**：Dribbble 搜不到合适的，或需要更贴近"生活感"的灵感。

```bash
agent-browser open "https://pinterest.com/search/pins/?q=<关键词>"
# 不需要登录，弹出登录弹窗 → 关掉继续看
```

**vs Dribbble 的区别**：
- Dribbble = 设计师社区 → 偏"专业设计"
- Pinterest = 混合社区 → 偏"好看的生活方式"
- 小红书审美更接近 Pinterest

---

## 小红书已验证的封面类型（按数据排序）

> 基于 5 轮实战中的竞品调研总结。

| 排名 | 封面类型 | 典型数据 | 特征 |
|------|---------|---------|------|
| 1 | AI 生成的精美产品 UI 展示图 | 200+ 赞 | 产品截图+设计处理 |
| 2 | 真实产品截图 + 好看角度 | 140+ 赞 | 真实感强 |
| 3 | 权威人脸 + 利益点大字 | 115+ 赞 | 人脸吸引注意力 |
| 4 | Logo/工具矩阵 + 干净背景 | 4000+ 赞 | 信息一目了然 |
| 5 | 产品截图 + 手写标注 | 7000+ 赞 | 教程类首选 |
| 6 | 真人出镜 + 产品实拍 | 13000+ 赞 | 最高赞类型 |

**关键发现**：
- 真人出镜 + 产品实拍 = 最高赞
- 产品截图 + 红色/手写标注 = 教程类稳定高赞
- 手写体/课堂笔记风 = 最有"人味儿"
