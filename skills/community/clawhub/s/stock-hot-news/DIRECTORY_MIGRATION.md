# 目录结构迁移文档

## 概述

根据用户要求，已完成 stock-hot-news 技能的目录结构统一迁移。所有中间文档现在都存放在 `system_settings.temp_dir` 指定的目录中，最终报告存放在 `system_settings.reports_dir` 指定的目录中。

## 配置文件更新 (url_config.json)

### 新增字段：
```json
"system_settings": {
  "temp_dir": "c:/SelfData/claw_temp/temp",
  "reports_dir": "c:/SelfData/claw_temp/reports"
}
```

### 修改字段：
```json
"wallstreetcn_module": {
  "output_directory": "c:/SelfData/claw_temp/temp/wallstreetcn_news"
}
```

## 模块路径配置更新

### Module 1: 主力网站热点新闻爬取器 (module1_main_sites.py)
- **旧配置**: 使用 `title_news_crawl` 字段
- **新配置**: 使用 `temp_dir` 字段，输出到 `temp_dir/title_news_crawl`
- **临时目录**: `temp_dir/title_news_crawl/temp`

### Module 2: 热点新闻话题归纳器 (module2_summarize_filtered.py)
- **旧配置**: 基于 `title_news_crawl` 构建路径
- **新配置**: 基于 `temp_dir` 构建路径
- **输入目录**: `temp_dir/title_news_crawl/temp` (Module 1输出)
- **输出目录**: `temp_dir/title_news_crawl/summarized`

### Module 3: 华尔街见闻快讯采集器 (module3_news_flash.py)
- **旧配置**: 使用 `wallstreetcn_module.output_directory`
- **新配置**: `wallstreetcn_module.output_directory` 已更新为 `temp_dir/wallstreetcn_news`
- **后备逻辑**: 如果未配置，从 `temp_dir` 构建

### Module 4: 完整财经热点新闻报告生成器 (module4_report_generator.py)
- **旧配置**: 使用 `summarized_dir` 和 `final_reports_dir`
- **新配置**:
  - Module 2输入: `temp_dir/title_news_crawl/summarized`
  - Module 3输入: `temp_dir/wallstreetcn_news`
  - 报告输出: `reports_dir`

### Main Scheduler (main.py)
- **报告目录**: `reports_dir`
- **日志目录**: `reports_dir/logs`
- **清理函数**: 更新为清理 `temp_dir` 和 `reports_dir`

### 网站抓取器 (cls_hot_news.py, jrj_hot_news.py, stcn_hot_news.py)
- **默认输出目录**: 更新为 `temp_dir/title_news_crawl`
- **注意**: 这些抓取器从 Module 1 接收 `output_dir` 参数，因此实际使用时使用 Module 1 传递的路径

## 目录结构示例

```
c:/SelfData/claw_temp/
├── temp/                          # 所有中间文档
│   ├── title_news_crawl/          # Module 1 输出
│   │   ├── temp/                  # 临时文件
│   │   └── summarized/            # Module 2 输出
│   └── wallstreetcn_news/         # Module 3 输出
└── reports/                       # 最终报告
    ├── logs/                      # 系统日志
    └── *.html, *.txt, *.png       # 生成报告
```

## 兼容性保障

1. **向后兼容**: 配置文件缺失时使用合理的默认值
2. **路径验证**: 所有目录自动创建
3. **优雅降级**: 配置无效时使用回退方案
4. **默认路径**: 使用 `c:/SelfData/claw_temp/temp` 和 `c:/SelfData/claw_temp/reports`

## 验证结果

✅ **配置文件加载**: 成功  
✅ **Module 1路径**: 正确 (`temp_dir/title_news_crawl`)  
✅ **Module 2路径**: 正确 (`temp_dir/title_news_crawl/summarized`)  
✅ **Module 3路径**: 正确 (`temp_dir/wallstreetcn_news`)  
✅ **Module 4路径**: 正确  
✅ **Main Scheduler路径**: 正确  
✅ **网站抓取器默认路径**: 正确  

## 用户配置指南

### 自定义目录结构：
1. 编辑 `url_config.json` 文件
2. 修改 `system_settings.temp_dir` 和 `system_settings.reports_dir`
3. 确保目录存在或系统有权限创建

### 示例自定义配置：
```json
"system_settings": {
  "temp_dir": "E:/MyData/finance/temp",
  "reports_dir": "E:/MyData/finance/reports"
}
```

### 运行系统：
```bash
cd skills/stock-hot-news
python main.py --module3-mode playwright
```

## 技术支持

- **微信**: quant_village_dog
- **QQ**: 13620658
- **邮箱**: 13620658@qq.com
- **QQ群**: 1057968391

---

**迁移完成时间**: 2026-03-28 19:46 (Asia/Shanghai)  
**迁移状态**: ✅ **完全迁移，所有路径统一到url_config.json配置**  
**系统状态**: ✅ **生产就绪，支持自定义目录结构**