# 配图生成使用说明

## 已生成的 Prompts

1. **封面图**: `cover-prompt.txt`
2. **正文配图**: `inline-prompts.txt`

## 使用 nano-banana-pro 生成图片

### 生成封面图

```bash
# 使用 nano-banana-pro 技能
"根据以下 prompt 生成封面图：$(cat images/cover-prompt.txt)"

# 保存为
images/cover.jpg
```

### 生成正文配图

```bash
# 为每个 section 生成配图
"根据以下 prompt 生成技术说明图：$(cat images/inline-prompts.txt)"

# 保存为
images/img1.jpg, img2.jpg, img3.jpg...
```

## 更新文章图片路径

生成图片后，更新文章中的图片路径：

```markdown
# 封面图
cover: /absolute/path/to/article/images/cover.jpg

# 正文配图
![描述](/absolute/path/to/article/images/img1.jpg)
```

**重要**：必须使用**绝对路径**！

## 自动更新（推荐）

运行以下命令自动更新文章中的图片路径：

```bash
node scripts/update-images.js article.md images/
```
