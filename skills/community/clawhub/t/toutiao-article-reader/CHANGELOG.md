# Toutiao Article Reader - 更新日志

## v1.1.0 (2026-05-03) - 增强版

### 新增功能

#### 1. AI 智能总结 ✅
- 自动生成文章概述
- 提取关键点（3-5 条）
- 文章价值评估（可信度/参考价值/推荐建议）
- 字数统计和阅读时间估算

**使用示例**:
```bash
python scripts/read_article.py <URL> --summary
```

#### 2. 缓存机制 ✅
- 避免重复读取同一文章
- 默认缓存 24 小时
- 支持查看缓存统计
- 支持清空缓存

**使用示例**:
```bash
# 查看缓存统计
python scripts/read_article.py --cache-stats

# 清空缓存
python scripts/read_article.py --clear-cache

# 自动使用缓存（第二次读取同一文章）
python scripts/read_article.py <URL>
```

#### 3. 导出功能 ✅
支持导出为多种格式：
- **Markdown** (.md) - 推荐，保留格式
- **TXT** (.txt) - 纯文本
- **JSON** (.json) - 结构化数据
- **HTML** (.html) - 网页格式

**使用示例**:
```bash
# 导出为 Markdown
python scripts/read_article.py <URL> --export markdown

# 导出为 Markdown 并指定输出文件
python scripts/read_article.py <URL> --export markdown -o my_article.md

# 导出为 HTML
python scripts/read_article.py <URL> --export html
```

#### 4. 多平台支持优化 ✅
针对不同平台优化提取规则：
- 今日头条 (toutiao.com) ⭐⭐⭐⭐⭐
- 微信公众号 (mp.weixin.qq.com) ⭐⭐⭐⭐⭐
- 知乎 (zhihu.com) ⭐⭐⭐⭐⭐
- 雪球 (xueqiu.com) ⭐⭐⭐⭐⭐
- 其他平台（通用规则）⭐⭐⭐⭐

#### 5. 内容清洗 ✅
- 去除广告词
- 去除水印
- 去除无关内容
- 智能分段

#### 6. 错误处理增强 ✅
- 完善的重试机制
- 详细的错误信息
- 超时处理优化

---

## v1.0.0 (2026-05-03) - 初始版本

### 基础功能
- ✅ 浏览器自动化阅读（Playwright）
- ✅ 提取标题、作者、发布时间
- ✅ 提取正文内容
- ✅ 支持多平台
- ✅ 基本错误处理

---

## 命令行参数

```bash
# 基本用法
python scripts/read_article.py <URL>

# 输出 JSON 格式
python scripts/read_article.py <URL> --json

# 生成 AI 总结
python scripts/read_article.py <URL> --summary

# 导出为 Markdown
python scripts/read_article.py <URL> --export markdown

# 显示浏览器窗口（调试用）
python scripts/read_article.py <URL> --no-headless

# 查看缓存统计
python scripts/read_article.py --cache-stats

# 清空缓存
python scripts/read_article.py --clear-cache

# 自定义超时时间
python scripts/read_article.py <URL> --timeout 60000
```

---

## 文件结构

```
toutiao-article-reader/
├── scripts/
│   ├── read_article.py      # 主脚本
│   ├── ai_summarizer.py     # AI 总结模块 ✨ 新增
│   ├── cache.py             # 缓存模块 ✨ 新增
│   ├── exporter.py          # 导出模块 ✨ 新增
│   └── test.py              # 测试脚本
├── SKILL.md
├── package.json
├── README.md
├── LICENSE
└── .gitignore
```

---

## 性能对比

| 功能 | v1.0.0 | v1.1.0 | 提升 |
|------|--------|--------|------|
| 读取速度 | 5-10 秒 | 0.1 秒* | 50-100 倍** |
| 内容清洗 | 基础 | 高级 | - |
| AI 总结 | ❌ | ✅ | - |
| 缓存 | ❌ | ✅ | - |
| 导出格式 | 1 种 | 4 种 | 4 倍 |
| 支持平台 | 4 个 | 5+ 个 | - |

*第二次读取（使用缓存）
**相比首次读取

---

## 待开发功能

- [ ] 批量读取（一次处理多个链接）
- [ ] Web 界面
- [ ] 自定义提取规则
- [ ] 更多平台支持
- [ ] PDF 导出
- [ ] 图片提取
- [ ] 视频内容提取

---

## 技术栈

- **Python 3.8+**
- **Playwright** - 浏览器自动化
- **BeautifulSoup4** - HTML 解析
- **MIT License** - 开源许可

---

## 开发者

Your Name - Initial work

## 贡献者

欢迎提交 Issue 和 Pull Request！
