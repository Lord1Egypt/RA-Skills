# 小红书舆情爬虫技能

> 爬取小红书笔记内容，分析舆情

## 概述

本技能用于爬取小红书（XHS）上的笔记内容，支持关键词搜索、评论采集和简单的舆情分析。

## 项目来源

基于 GitHub 开源项目:
- **redbooks** (推荐): https://github.com/xiaofuqing13/redbooks
- **jiang-xiaohongshu-crawler** (含AI分析): https://github.com/upJiang/jiang-xiaohongshu-crawler  
- **TikHub** (API SDK): https://github.com/TikHub/TikHub-API-Python-SDK

## 环境要求

### 本地运行 (Windows)
```bash
# Python 3.8+
pip install -r requirements.txt
python crawler_ultimate.py
```

### 依赖
- DrissionPage (浏览器自动化)
- pandas (数据处理)
- openpyxl (Excel导出)
- requests (HTTP请求)
- Pillow (图片处理)
- customtkinter (GUI界面)

## 当前状态

### ❌ 环境限制

经过测试发现:
1. **小红书 API 需要登录凭证** - 直接调用接口返回 `-101 无登录信息`
2. **无浏览器环境** - 当前沙箱没有 Chromium/Chrome 浏览器
3. **无 GUI 环境** - redbooks 需要 Windows + customtkinter

### ✅ 可行方案

1. **本地运行** - 在有浏览器和账号的本地电脑运行
2. **TikHub API** - 使用付费 API 服务 (需要注册获取 token)

---

## 快速开始 (本地环境)

### 1. 安装依赖
```bash
# 克隆项目
git clone https://github.com/xiaofuqing13/redbooks.git
cd redbooks

# 创建虚拟环境 (推荐)
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行程序
```bash
python crawler_ultimate.py
```

### 3. 登录小红书
首次运行会弹出浏览器窗口，用小红书账号登录

### 4. 开始爬取
- 输入关键词: `摩比爱识字` 或 `摩比点读笔`
- 选择爬取模式: 标准模式
- 设置爬取数量: 50-100 条

---

## 技术限制说明

| 方式 | 需要登录 | 需要浏览器 | 费用 |
|------|---------|-----------|------|
| 网页 API | ✅ | ❌ | 免费但有限制 |
| 浏览器自动化 | ✅ | ✅ | 免费 |
| TikHub API | ❌ | ❌ | 付费 |

---

**更新日期**: 2026-03-15

## 功能特性

| 功能 | redbooks | jiang-xiaohongshu-crawler | TikHub API |
|------|----------|---------------------------|------------|
| 关键词搜索 | ✅ | ✅ | ✅ |
| 笔记内容 | ✅ | ✅ | ✅ |
| 评论采集 | ✅ | ✅ | ✅ |
| 图片下载 | ✅ | ❌ | ✅ |
| 视频下载 | ✅ | ❌ | ✅ |
| AI舆情分析 | ❌ | ✅ | ❌ |
| GUI界面 | ✅ | ❌ | ❌ |
| 免费 | ✅ | ✅ | 付费 |

## 爬取字段

- title (标题)
- author (作者)
- content (正文内容)
- tags (标签)
- publish_time (发布时间)
- ip_region (IP地区)
- like_count (点赞数)
- collect_count (收藏数)
- comment_count (评论数)
- comments (评论列表)

## 注意事项

1. **遵守平台规则**: 仅供学习研究使用
2. **登录要求**: 首次使用需要登录小红书账号
3. **频率限制**: 建议设置爬取间隔 (如 3-5秒)
4. **反爬风险**: 频繁爬取可能导致账号被封禁

## 摩比产品搜索关键词

- 摩比爱识字
- 摩比点读笔
- 摩比思维机
- mobby
- 摩比英语
- 摩比中文

## 输出示例

爬取结果会保存为:
- Excel 文件: `data/关键词_时间.xlsx`
- SQLite 数据库: `data/xiaohongshu.db`
- 图片/视频: `images/关键词_时间/`

---

**更新日期**: 2026-03-15
