# Typecho 博客发布技能 v2.0

## 🎯 快速开始

### 方式 1: 手动指定配图（推荐⭐）

```bash
cd /home/jiliang/.openclaw/workspace/skills/typecho-blog-publish/scripts

# 精准配图发布
python3 publish_v2_full.py "AI 如何改变生活" "AI" "人工智能，科技" \
  --image "https://images.pexels.com/photos/373543/pexels-photo-373543.jpeg"
```

### 方式 2: 使用本地图片

```bash
python3 publish_v2_full.py "AI 实战指南" "AI" "人工智能" \
  --image-file "/path/to/screenshot.png"
```

### 方式 3: 自动配图（不推荐）

```bash
python3 publish_v2_full.py "AI 改变生活" "AI" "人工智能"
```

---

## 📋 完整流程

```
1. 找图（Pexels/Pixabay）→ 复制图片 URL
2. 调用脚本（--image 参数指定 URL）
3. 自动处理（上传、生成文案、直接发布）
4. 检查结果（访问文章链接）
5. 确认效果（公开可见）
```

**注意**: v2.0 起默认直接发布（不再存草稿），文章会立即公开可见。

---

## ⚠️ 铁律：发布后必须检查！

**发布完成≠工作完成！必须像真实用户一样检查实际效果！**

### 检查清单
- [ ] 标题正确显示（不是文件名）
- [ ] 配图正常显示（不是裂开图标）
- [ ] 配图 URL 为完整路径
- [ ] 分类正确
- [ ] 标签正确
- [ ] 内容格式正常
- [ ] 摘要正常

---

## 📚 详细文档

- `README_USE.md` - 完整使用指南
- `CHECKLIST.md` - 发布检查清单
- `PUBLISH.md` - 发布流程详解

---

*维护者：团子 🌟*  
*版本：v2.0*  
*更新时间：2026-04-03*
