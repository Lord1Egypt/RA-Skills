---
name: wechat-article-scraper
description: 微信公众号文章批量抓取工具，支持批量抓取公众号历史文章、导出为Markdown/HTML格式、自动提取封面图、标签、阅读量等数据。集成SkillPay支付接口，每次调用收0.001USDT。
license: MIT
---

# 微信公众号文章抓取工具

## 功能概述
专为内容创作者、运营人员打造的公众号文章批量采集工具：
1. **批量抓取**：输入公众号主页链接，自动抓取全部历史文章
2. **多格式导出**：支持导出为Markdown、HTML、纯文本格式
3. **完整数据提取**：自动提取文章标题、发布时间、阅读量、点赞、在看、封面图、标签、作者等元数据
4. **自动去重**：已抓取过的文章不会重复抓取
5. **批量下载**：支持批量下载所有文章的图片资源
6. **全中文界面**，操作简单易用
7. **数据本地存储**，安全可靠

## 支付说明
每次使用本工具将收取0.001 USDT，支付接口由SkillPay.me提供，API Key：`sk_d11f398e77b6e892eb7a7d421fe912dde27322cf1792366b776b72bd459d3c2e`

## 使用流程
1. 完成支付验证
2. 输入公众号主页链接
3. 选择抓取范围（全部/最近N篇）
4. 等待抓取完成
5. 选择导出格式下载

## 依赖要求
- Python 3.8+
- Flask: Web框架
- requests: HTTP请求
- beautifulsoup4: HTML解析
- sqlite3: 本地数据存储
- pandas: 数据处理

## 部署说明
1. 安装依赖：`pip install flask requests beautifulsoup4 pandas`
2. 启动服务：`python scripts/app.py`
3. 访问 http://localhost:5002 即可使用