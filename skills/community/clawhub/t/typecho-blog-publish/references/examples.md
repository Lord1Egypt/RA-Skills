# Typecho 博客发布技能 - 完整使用示例

## 快速开始

### 1. 环境检查

```bash
cd /home/jiliang/.openclaw/workspace/skills/typecho-blog-publish
bash scripts/setup_runtime.sh
```

确保输出显示所有检查通过。

### 2. 准备文章

在 `articles/` 目录创建文章：

```markdown
---
title: 我的第一篇文章
categories: 生活，随笔
tags: 心情，日记
---

# 我的第一篇文章

这是正文内容...
```

### 3. 发布文章

```bash
# 保存为草稿
python3 scripts/publish_post.py --file articles/my-first-post.md --draft

# 立即发布
python3 scripts/publish_post.py --file articles/my-first-post.md
```

## 完整工作流示例

### 场景 1：日常发文

```bash
# 1. 写文章
cat > articles/2026-03-26.md << 'EOF'
---
title: 2026-03-26 日记
categories: 日记
tags: 日常
---

# 今天天气不错

心情很好，写点什么...
EOF

# 2. 发布
python3 scripts/publish_post.py --file articles/2026-03-26.md

# 3. 验证
python3 scripts/manage.py list 5
```

### 场景 2：批量发布系列文章

```bash
# 1. 准备多篇文章
articles/
├── ai-tutorial-1.md
├── ai-tutorial-2.md
├── ai-tutorial-3.md

# 2. 批量发布（草稿模式）
python3 scripts/batch_publish.py articles --draft --delay=3

# 3. 查看草稿
python3 scripts/manage.py list 10

# 4. 在博客后台审核后，手动发布
```

### 场景 3：检查博客状态

```bash
# 查看统计
python3 scripts/manage.py stats

# 输出示例：
# 📊 博客统计：
#   总文章数：15
#   已发布：10
#   草稿：5
```

### 场景 4：清理不需要的文章

```bash
# 1. 查看文章列表
python3 scripts/manage.py list 20

# 2. 删除测试文章
python3 scripts/manage.py delete 917
python3 scripts/manage.py delete 916

# ⚠️ 注意：删除操作不可恢复！
```

## 高级用法

### 1. 使用模板

```bash
# 复制模板
cp references/article-template.md articles/new-post.md

# 编辑内容
# 发布
python3 scripts/publish_post.py --file articles/new-post.md
```

### 2. 定时发布（需配合系统定时任务）

```bash
# 添加到 crontab
# 每天早上 8 点发布
0 8 * * * cd /path/to/skill && python3 scripts/batch_publish.py articles --delay=10
```

### 3. 日志查看

```bash
# 查看发布日志
cat scripts/publish_log.txt

# 实时查看日志
tail -f scripts/publish_log.txt
```

## 常见问题

### Q1: 提示"密码错误"
**解决**：检查 `.env` 文件是否存在且包含正确的 `BLOG_PASSWORD`

### Q2: Markdown 渲染不正常
**解决**：
1. 查看 `references/markdown-guide.md`
2. 确保标题、列表、代码块前后有空行
3. 使用测试文章验证：`articles/markdown-test.md`

### Q3: 无法上传图片
**解决**：当前版本不支持自动上传图片，需手动上传后插入链接

### Q4: 批量发布失败
**解决**：
1. 检查文章格式是否正确
2. 增加延迟时间：`--delay=5`
3. 逐个发布排查问题文章

## 最佳实践

1. **先草稿后发布**：始终先用 `--draft` 测试
2. **定期清理**：删除不需要的测试文章
3. **备份习惯**：重要文章保留原始 Markdown 文件
4. **日志检查**：发布后查看日志确认成功
5. **逐步优化**：根据渲染效果调整 Markdown 格式

## 下一步计划

- [ ] 图片自动上传（等待 browser-use 技能）
- [ ] 定时发布功能
- [ ] 一键同步到多平台
- [ ] 文章数据分析

---

*最后更新：2026-03-26*
