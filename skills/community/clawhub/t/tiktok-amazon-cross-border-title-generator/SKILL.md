# TikTok & Amazon 跨境电商爆款标题生成器

## 功能概述
专为 TikTok 创作者和 Amazon/亚马逊卖家打造的英文标题生成工具。基于平台算法偏好和竞品数据分析，生成高点击率、高搜索排名的跨境电商标题。

## 核心功能

### 1. TikTok 视频标题生成
- 趋势标签推荐（#fyp #viralshopping 等）
- 悬念式/数字型/情感型多风格切换
- SEO 优化关键词植入
- emoji 图标点缀

### 2. Amazon 产品标题生成
- A9 算法优化（字符数 ≤ 200）
- 核心关键词前置
- 规格参数规范嵌入
- 品牌名 + 产品名 + 核心卖点结构

### 3. 竞品分析模式
- 输入 ASIN 或竞品标题
- 系统解析其关键词结构
- 生成 5 个差异化标题方案

## 使用方式

用户输入：
```
/跨境标题
类型：TikTok
产品：wireless bluetooth earbuds
核心卖点：30H续航 / IPX7防水 / 佩戴舒适
风格：悬念型
数量：10个
```

系统输出：
```
1. 🔥 These Earbuds Changed Everything – 30H Battery Life!
2. Wait Until You See What Happens Next 😱 #fyp #tech
3. I Used These for 30 Hours Straight – Here's the Truth
4. IPX7 Waterproof Earbuds That Won't Fall Out. Period.
5. The Most Comfortable Earbuds Ever? We Tested Them
...
```

## 输出格式
- 10 个标题（可自定义数量）
- 每个标题附带标签建议
- 关键 SEO 关键词高亮
- 字符数统计（Amazon 标题 ≤ 200 字符）

## 定价
- 单次生成：14.9 元
- 包月：79 元（不限次使用）

## 技术实现
- 使用 OpenClaw 原生能力（无需第三方 API）
- 读取 memory/ 目录中用户偏好设置
- 记录生成历史到 memory/cross-border-history.md
