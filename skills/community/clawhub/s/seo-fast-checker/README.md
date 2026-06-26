# 🔍 SEO 优化检查器

> **¥19.9 | 一次购买，永久使用 | 输入网址，即刻诊断**

## 🎯 这个工具是干什么的？

你的网站为什么搜不到？排名上不去？流量少得可怜？

可能问题就出在：标题写得不对、图片没有 alt 标签、没有结构化数据...这些 SEO 细节在不知不觉中让你流失了大量搜索流量。

**SEO 优化检查器** 就是你的私人 SEO 审计师。输入网址，一键输出完整的 SEO 诊断报告：

- ✅ 标题标签（Title Tag）检查
- ✅ Meta Description 检查
- ✅ Heading 层级结构（H1-H6）分析
- ✅ 关键词密度统计
- ✅ 图片 Alt 属性检测
- ✅ Canonical URL 设置检查
- ✅ Open Graph / Twitter Card 检测
- ✅ 页面大小与加载速度
- ✅ 移动端 viewport 适配
- ✅ Robots / noindex 指令
- ✅ 结构化数据（JSON-LD）
- ✅ 链接统计（内链/外链）
- 🤖 AI 增强分析（可选）

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install requests beautifulsoup4
```

### 2. 检查你的网站

```bash
# 基础检查
python3 seo_checker.py https://你的网站.com

# 带AI增强分析（推荐）
export OPENAI_API_KEY="sk-your-api-key-here"
python3 seo_checker.py --ai https://你的网站.com
```

## 📖 详细用法

### 参数说明

| 参数 | 说明 |
|------|------|
| `urls` | 要检查的网址（支持多个，空格分隔） |
| `--output` / `-o` | 保存报告到文件 |
| `--ai` | 启用 AI 增强分析（需设置 OPENAI_API_KEY） |

### 实用示例

```bash
# 1. 检查一个网站
python3 seo_checker.py https://example.com

# 2. 保存报告
python3 seo_checker.py https://example.com --output seo-report.md

# 3. 同时检查多个页面
python3 seo_checker.py https://example.com https://example.com/about https://example.com/blog

# 4. 启用 AI 增强分析
export OPENAI_API_KEY="sk-xxx"
python3 seo_checker.py --ai https://example.com

# 5. 自动补全协议（如果不输入 https://）
python3 seo_checker.py example.com
```

### 报告示例输出

```
# SEO 诊断报告

**URL**: https://example.com
**检测时间**: 2025-01-15 14:30:22

## 总览

| 严重问题 🔴 | 建议优化 🟡 | 良好 🟢 |
|-----------|------------|--------|
| 2 | 4 | 6 |

## 🔴 严重问题（必须修复）

### 标题标签
- **状态**: 缺失
- **详情**: 页面没有 <title> 标签

### 移动端适配
- **状态**: 缺失
- **详情**: 没有 viewport meta 标签

## 🟡 建议优化

### Canonical URL
- **状态**: 未设置
- **详情**: 没有 canonical 标签
...
```

## 🛠 环境变量

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `OPENAI_API_KEY` | AI模式✅ | — | OpenAI API 密钥 |
| `OPENAI_MODEL` | ❌ | `gpt-4o-mini` | 使用的 AI 模型 |

## ❓ 常见问题

### Q: 需要安装什么依赖？
**A:** 基础模式需要 `requests` 和 `beautifulsoup4`。AI 模式需要额外安装 `openai` 库。

```bash
pip install requests beautifulsoup4 openai
```

### Q: 支持百度 SEO 检测吗？
**A:** 基础的 SEO 检查项（标题、描述、Headings、图片alt、移动端适配等）对百度 SEO 同样适用。AI 增强分析会同时考虑百度 SEO 和 Google SEO 的最佳实践。

### Q: 为什么我的页面加载很慢？
**A:** 工具使用 requests 库从服务器获取页面，如果你检查的是大页面（含大量 JS、图片），加载时间会较长。建议检查纯 HTML 页面效果最好。

### Q: AI 增强分析有什么用？
**A:** AI 模式会分析页面内容质量、给出关键词策略建议、内容优化方向和用户建议提升。适合需要深入优化的场景。

### Q: 检查结果准确吗？
**A:** 基础的 SEO 规则检查（标题、描述、标签等）是 100% 准确的。AI 分析部分提供建议性意见，建议结合你的实际情况判断。

### Q: JS 渲染的 SPA 页面支持吗？
**A:** 基础模式不支持 JS 渲染，只分析服务器返回的 HTML。如果你需要检查 SPA 页面（如 React/Vue），推荐使用 AI 模式或配合 headless 浏览器工具。

## 💰 定价

| 项目 | 价格 |
|------|------|
| SEO 优化检查器 | **¥19.9** |
| 包含 | 源码、文档、终身更新 |
| 退款政策 | 7天无理由 |

## 📄 许可

个人和商业使用均可。禁止转售源码。
