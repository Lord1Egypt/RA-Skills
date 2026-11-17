# 开放平台抓取模板 (Scraper Template)

## 简介

基于企迈(qmai)开放平台抓取经验沉淀的通用模板，支持快速适配各种开放平台的 API 文档抓取。

## 核心文件

```
scraper-template/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── scrape_base.py          # Playwright 抓取基类（抽象方法）
│   └── manage_base.py          # 数据管理工具模板
└── examples/
    └── qmai_scraper.py         # 企迈抓取器（参考实现）
```

## 使用流程

### 1. 创建新平台 Skill

```bash
cp -r scraper-template/ meituan-api-fetcher/
# 或
mkdir -p new-platform-api-fetcher/{scripts,references,docs,solutions}
```

### 2. 实现平台专属抓取器

继承 `scrape_base.OpenPlatformScraper`，实现 3 个抽象方法：

| 方法 | 作用 | 关键 |
|------|------|------|
| `expand_menu(page)` | 展开菜单，发现模块 | 找菜单组件（qm-tree/ant-menu/el-menu） |
| `navigate_to_api(page, key, info)` | 导航到 API 详情 | 点击菜单项或直接跳转 URL |
| `extract_api_detail(page)` | 提取 API 详情 | 解析表格（参数/返回值）|

### 3. 抓取

```bash
python3 scripts/scrape.py
```

### 4. 使用管理工具

```bash
# 统计
python3 scripts/manage.py --stats
# 搜索
python3 scripts/manage.py --search 门店
# 列出模块
python3 scripts/manage.py --modules
```

## 标准化输出格式

每个模块输出一个 JSON 文件：

```json
{
  "module_id": "2.1",
  "module_name": "门店管理",
  "interface_count": 15,
  "interfaces": [
    {
      "id": "2.1.1",
      "name": "根据门店编码查询门店详情",
      "method": "GET",
      "path": "/v3/org/shop/getShopDetail",
      "request_params": [{ "name": "code", "type": "string", "required": true, "description": "门店编码" }],
      "response_params": [{ "name": "id", "type": "long", "description": "门店ID" }],
      "response_example": { "code": "", "id": 0 }
    }
  ]
}
```

## 抓取策略参考

| 平台类型 | 常见菜单组件 | 注意事项 |
|----------|-------------|----------|
| 自研 SPA | qm-tree, custom-menu | 动态加载，需展开后等待 |
| Ant Design | ant-menu, ant-tree | 支持 data-key 定位 |
| Element UI | el-menu, el-tree | el-tree-node 定位 |
| 纯 HTML | ul/li, table | 直接解析，最简单 |

## 已验证的平台

| 平台 | 状态 | 模块数 | 接口数 |
|------|------|--------|--------|
| 企迈(qmai) | ✅ 完成 | 32 | 307 |

## 更新日志

### 2026-04-27
- 🎯 从企迈抓取经验提炼通用框架
- 📦 创建 scrape_base.py 抽象基类
