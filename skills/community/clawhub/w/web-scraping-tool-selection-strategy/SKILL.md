---
name: "web-scraping-tool-selection-strategy"
description: "如何选择合适的网页抓取工具进行数据采集。当用户提到网页抓取、数据采集、爬虫、自动化测试、浏览器自动化、网站监控、竞品分析、价格监控、评论抓取、社交媒体数据分析、电商数据采集、小红书/知乎/京东/淘宝/1688抓取、结构化数据提取、反爬绕过、浏览器复用、API抓取、实时数据监控等场景时使用此技能。包含opencli和playwright-cli两种工具的选择策略。"
metadata: { "openclaw": { "emoji": "🕷️" } }
---

# 网页抓取工具选型策略

建立高效的网页数据采集策略，通过合理选择工具最大化抓取成功率和数据质量。

## When to use this skill
- 当你需要从不同网站抓取数据但不确定使用哪种工具时
- 面对反爬机制需要绕过的复杂网站抓取场景
- 需要结构化数据输出或快速API级访问时
- 要复用已登录浏览器状态抓取私有数据时

## Steps
1. **优先使用opencli进行有适配器的平台抓取**
   - 对于小红书、知乎、微博、B站等有官方适配器的平台，使用`opencli <platform> <action> --limit <number> -f json`
   - 例如：`opencli xiaohongshu search "关键词" --limit 3 -f json`
   - 为什么：提供结构化JSON输出，速度快，稳定性高，包含作者、标题、点赞数、发布时间等完整字段

2. **使用playwright-cli作为兜底方案**
   - 对于京东、淘宝、1688、抖音、拼多多等复杂电商网站，使用`playwright-cli goto "<URL>"`
   - 例如：`playwright-cli goto "https://item.jd.com/44541018110.html#comment"`
   - 为什么：能够复用已登录的Chrome浏览器状态，绕过反爬机制，支持动态加载内容和登录后可见数据

3. **根据平台特性选择工具**
   - 社交媒体平台（小红书/知乎/微博/B站）→ 优先使用opencli
   - 电商平台（京东/淘宝/1688/抖音/拼多多）→ 使用playwright-cli
   - 为什么：opencli针对特定平台有优化适配器，playwright-cli提供通用浏览器级解决方案

4. **验证工具连通性和状态**
   - 在正式抓取前测试工具是否正常运行
   - 检查Chrome浏览器是否已正确连接
   - 为什么：避免在演示或生产环境中出现连接失败的问题

## Pitfalls and solutions
❌ 盲目使用单一工具 → 无法适应不同网站的反爬机制和结构差异 → ✅ 根据平台特性选择合适工具
❌ 忽略已登录浏览器状态 → 错过登录后数据和增加登录验证步骤 → ✅ 优先复用已登录Chrome标签页
❌ 不区分API级和浏览器级抓取 → 效率低下或数据不准确 → ✅ 结构化数据用opencli，复杂页面用playwright-cli
❌ 缺乏工具状态检查 → 演示时出现意外故障 → ✅ 演示前进行最小检查验证

## Key code and configuration
```bash
# opencli小红书搜索示例
opencli xiaohongshu search "宠物猫" --limit 3 -f json

# opencli知乎热榜示例  
opencli zhihu hot --limit 5 -f json

# playwright-cli京东评论抓取示例
playwright-cli goto "https://item.jd.com/44541018110.html#comment"

# playwright-cli 1688供应链抓取示例
playwright-cli goto "https://s.1688.com/selloffer/offer_search.htm?keywords=静脉曲张袜"
```

## Environment and prerequisites
- opencli工具已安装并配置
- playwright-cli工具已安装并配置
- Chrome浏览器已安装且可被工具访问
- 网络连接稳定，能够访问目标网站
- 目标网站账号已登录（用于playwright-cli复用登录态）

## Companion files
- `scripts/web_scraping_validator` — 工具连通性验证脚本
- `references/platform_mapping_table` — 平台与工具对应关系参考表