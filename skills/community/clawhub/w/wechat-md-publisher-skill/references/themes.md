# WeChat Publisher - 主题使用指南

## 6 个内置主题

`wechat-md-publisher` 提供 6 个专为微信公众号优化的内置主题，开箱即用。

### 1. default - 默认主题

**风格**：简洁清爽，适合各类文章

**适用场景**：
- 企业公告、正式通知
- 技术文档、学术文章
- 通用内容

**使用**：
```bash
wechat-pub publish create --file article.md --theme default
```

---

### 2. blackink - Black Ink

**风格**：深色模式，靛蓝点缀，适合夜间阅读

**适用场景**：
- 夜间阅读类内容
- 科技、极客风格文章
- 深色调品牌内容

**使用**：
```bash
wechat-pub publish create --file article.md --theme blackink
```

---

### 3. orangesun - Orange Sun

**风格**：温暖明亮，橙色阳光系

**适用场景**：
- 生活类、旅行类文章
- 轻松活泼的内容
- 节日推送

**使用**：
```bash
wechat-pub publish create --file article.md --theme orangesun
```

---

### 4. redruby - Red Ruby

**风格**：优雅大气，宝石红点缀

**适用场景**：
- 品牌介绍、时尚类文章
- 重要公告、活动推广
- 视觉冲击力强的内容

**使用**：
```bash
wechat-pub publish create --file article.md --theme redruby
```

---

### 5. greenmint - Green Mint

**风格**：清新自然，薄荷绿色调

**适用场景**：
- 健康、环保类文章
- 教程指南
- 清新风格内容

**使用**：
```bash
wechat-pub publish create --file article.md --theme greenmint
```

---

### 6. purplerain - Purple Rain

**风格**：梦幻浪漫，紫色渐变

**适用场景**：
- 文艺类、情感类文章
- 个人博客
- 创意内容

**使用**：
```bash
wechat-pub publish create --file article.md --theme purplerain
```

---

## 主题选择建议

### 按内容类型选择

| 内容类型 | 推荐主题 | 备选主题 |
|---------|---------|---------|
| 技术文章 | default | blackink |
| 生活分享 | orangesun | greenmint |
| 品牌时尚 | redruby | purplerain |
| 教育内容 | greenmint | default |
| 文艺情感 | purplerain | orangesun |
| 正式公告 | default | redruby |
| 夜间/深色 | blackink | - |

### 按品牌调性选择

- **专业简洁**：default
- **温暖活力**：orangesun、greenmint
- **优雅大气**：redruby、purplerain
- **深色极简**：blackink

---

## 查看可用主题

```bash
wechat-pub theme list
```

输出示例：
```
┌─────────────┬──────────────┬──────────┬────────────────────────────┐
│ ID          │ 名称         │ 类型     │ 描述                       │
├─────────────┼──────────────┼──────────┼────────────────────────────┤
│ default     │ 默认主题     │ builtin  │ 简洁清爽的默认样式         │
│ blackink    │ Black Ink    │ builtin  │ 深色模式，靛蓝点缀         │
│ orangesun   │ Orange Sun   │ builtin  │ 温暖明亮的橙色系主题       │
│ redruby     │ Red Ruby     │ builtin  │ 优雅的宝石红风格           │
│ greenmint   │ Green Mint   │ builtin  │ 清新薄荷绿，轻松舒适       │
│ purplerain  │ Purple Rain  │ builtin  │ 梦幻紫色渐变               │
└─────────────┴──────────────┴──────────┴────────────────────────────┘
```

---

## 测试所有主题

```bash
# 创建测试文章
cat > test.md << 'EOF'
---
title: 主题测试
---

# 标题一

这是正文内容。

## 标题二

- 列表项 1
- 列表项 2

**粗体文本** 和 *斜体文本*
EOF

# 测试所有主题（创建草稿对比）
for theme in default blackink orangesun redruby greenmint purplerain; do
    echo "测试主题: $theme"
    wechat-pub draft create --file test.md --theme $theme
done
```

然后在微信公众平台查看对比效果。

---

## 自定义主题

如果内置主题不满足需求，可以创建自定义主题：

### 1. 创建 CSS 文件

```css
/* my-theme.css */
#wenyan {
    font-size: 16px;
    line-height: 1.8;
    color: #2c3e50;
}

#wenyan h1 {
    color: #ff6b6b;
    border-bottom: 3px solid #ff6b6b;
}
```

### 2. 添加主题

```bash
wechat-pub theme add-local --name my-theme --path ./my-theme.css
```

### 3. 使用主题

```bash
wechat-pub publish create --file article.md --theme my-theme
```

---

## 常见问题

### Q: 如何查看所有可用主题？

```bash
wechat-pub theme list
```

### Q: 主题可以修改吗？

内置主题不可修改，但可以创建自定义主题，基于内置主题的 CSS 另存为新主题。

### Q: 发布后可以更换主题吗？

不可以。已发布的文章主题无法更改，需要删除原文章后用新主题重新发布。
