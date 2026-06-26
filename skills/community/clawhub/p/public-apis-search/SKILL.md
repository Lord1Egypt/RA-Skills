---
name: public-apis-search
description: 快速搜索和发现公共 API，基于 public-apis/public-apis 仓库（1400+ API，49 个分类），支持关键词搜索、分类浏览、认证方式筛选
argument-hint: "[关键词] [--category 分类] [--auth free|apiKey|OAuth] [--https] [--limit N]"
version: 1.0.0
author: OpenClaw Community
---

# Public APIs Search

基于 [public-apis/public-apis](https://github.com/public-apis/public-apis) 的快速 API 搜索工具。收录 **1400+** 免费/开放 API，覆盖 **49 个分类**。

## 用法

### 关键词搜索
```bash
python search_apis.py "weather"
python search_apis.py "machine learning" --limit 10
python search_apis.py "stock market finance"
```

### 按分类浏览
```bash
python search_apis.py --categories          # 列出所有分类
python search_apis.py "weather" --category Weather
python search_apis.py "code" --category Development
```

### 筛选条件
```bash
python search_apis.py "weather" --auth free       # 仅免费（无需 API Key）
python search_apis.py "email" --auth apiKey       # 需要 API Key
python search_apis.py "map" --https               # 仅 HTTPS
python search_apis.py "data" --limit 20           # 限制结果数
```

### 随机发现
```bash
python search_apis.py --random            # 随机 5 个 API
python search_apis.py --random 10         # 随机 10 个 API
```

### 组合使用
```bash
# 免费 + HTTPS + 天气相关
python search_apis.py "weather" --auth free --https

# 开发工具 + 免费
python search_apis.py "compiler" --category Development --auth free
```

## 数据来源

- 来源：[public-apis/public-apis](https://github.com/public-apis/public-apis)
- 数据库：`apis.json`（本地 JSON 文件，无需联网搜索）
- 更新时间：手动更新（运行 `build_db.py` 重新解析 README）

## 更新数据

```bash
curl -s -L "https://raw.githubusercontent.com/public-apis/public-apis/master/README.md" -o README.md
python build_db.py README.md apis.json
```

## 返回格式

每条结果包含：
- **名称** + **描述**
- **分类** | **认证方式** | **HTTPS** | **CORS**
- **链接**（直达 API 文档）

## 注意事项

- 搜索为本地操作，无需联网（除首次下载/更新数据外）
- 关键词支持多词模糊匹配（按名称、描述、分类综合评分）
- `--auth free` 等价于 `--auth No`，筛选无需认证的 API
