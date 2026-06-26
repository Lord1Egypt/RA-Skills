---
name: xiaohongshu-image-generator
description: 根据用户提示词生成小红书配图。使用 HTML + CSS 设计可视化卡片，通过 Playwright 浏览器截图生成图片。触发场景：(1) 用户要求生成小红书笔记配图 (2) 需要生成竖版封面卡片图 (3) 用 HTML 模板生成营销配图
---

# 小红书配图生成器

根据提示词生成小红书风格的竖版配图（800x1000px）。

## 工作流程

1. **分析提示词** - 理解需要生成的图片内容、风格、配色
2. **生成 HTML** - 用模板动态生成 HTML 页面
3. **启动 HTTP Server** - 在本地托管 HTML 文件
4. **打开并截图** - 用 browser 工具打开页面并截图
5. **返回结果** - 提供截图文件路径

## 使用方法

```bash
# 1. 创建 HTML 文件（参考 assets/templates/ 中的模板）
# 2. 启动 HTTP server
python3 -m http.server <端口号>

# 3. 用 browser 打开并截图
# 先打开页面，等待加载完成
browser action=open url=http://localhost:<端口号>/<filename>.html
# 等待 2 秒让页面完全加载
sleep 2
# 截图
browser action=screenshot targetId=<tab-id>
```

## HTML 模板规范

### 基础结构
- 画布尺寸：800x1000px（小红书竖版比例）
- 使用 flex 居中布局
- body 设置渐变背景
- 卡片使用白色背景 + 圆角 + 阴影

### 必选元素
```css
.card {
    width: 800px;
    height: 1000px;
    border-radius: 32px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}
```

### 配色方案
推荐使用渐变背景：
```css
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

## 注意事项

1. **截图前必须等待加载** - 用 `sleep 2` 或检查页面标题确保页面已加载
2. **先打开再截图** - 使用 browser action=open 打开页面，再进行截图
3. **端口占用** - 使用不常用端口（如 8765），避免冲突

## 模板参考

详见 [assets/templates/](assets/templates/) 目录中的示例模板。
