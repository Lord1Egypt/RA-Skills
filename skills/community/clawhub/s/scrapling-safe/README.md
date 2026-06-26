# Scrapling 技能说明

## Scrapling Safe 技能

基于 Scrapling 框架的网页抓取技能，提供：

1. **多种抓取模式**：
   - HTTP 请求（快速，适合静态页面）
   - 隐身模式（绕过反爬虫检测）
   - 浏览器自动化（适合动态内容）

2. **智能元素定位**：
   - 自适应 CSS/XPath 选择器
   - 网站改版后自动调整
   - 支持多种选择方法

3. **数据提取**：
   - CSS 选择器
   - XPath 表达式
   - 文本搜索
   - 正则表达式

4. **结果导出**：
   - JSON/JSONL 格式
   - TXT 文本文件
   - Markdown 格式

## 安全特性

- ✅ 路径验证：输出文件只能保存到用户主目录
- ✅ 无危险函数：不使用 eval/exec
- ✅ 频率限制：默认并发为 1，避免对目标造成压力
- ✅ 超时控制：严格的超时设置
- ❌ 禁止抓取私有内容

## 使用示例

```bash
# 基本抓取
scrapling get 'https://example.com' --output ~/result.json

# 隐身模式
scrapling stealthy 'https://example.com' --output ~/result.json

# 指定选择器
scrapling get 'https://quotes.toscrape.com' --css-selector '.quote' --output ~/quotes.json
```

## 注意事项

- 需要安装 Scrapling 和相关依赖
- 遵守 robots.txt 和网站服务条款
- 仅用于公开可访问的页面
- 输出文件路径必须在用户主目录
