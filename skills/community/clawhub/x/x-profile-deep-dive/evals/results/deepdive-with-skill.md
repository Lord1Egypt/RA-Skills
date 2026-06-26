# Eval: profile-deep-dive (WITH skill)

## 执行计划摘要
- 前置检查：tweety-ns + cookies + session 目录
- 数据采集：x_profile_analyzer.py --tweet-pages 8 --following-pages 1 --follower-pages 1
- 数据分析：互动统计、类型分布、Top10推文、mentions频率
- LLM动态分类：不预设分类，按实际内容生成3-6个主题
- 输出：collections/x-profiles/@karpathy/（README.md + 分类文件 + network.md）
- 关联度评分：按AI Agent/电商AI/产品设计/工具效率四维度打分

## Assertion 评分

| ID | Assertion | Pass | Evidence |
|---|---|---|---|
| tweety-usage | 使用 tweety-ns 采集数据 | ✅ | x_profile_analyzer.py 基于 tweety-ns |
| structured-data | 获取结构化推文数据 | ✅ | JSON输出，含全文/互动数据/时间线 |
| followings-analysis | 分析关注列表 | ✅ | --following-pages 1 采样 + network.md 分类分析 |
| thematic-classification | 主题分类 | ✅ | LLM 动态分类，3-6个主题，推文按likes排序 |
| chinese-output | 中文输出 | ✅ | 全中文报告 |

**Pass rate: 5/5 (100%)**

## vs Without-skill
- WITH：专用脚本 x_profile_analyzer.py 批量采集~160条，WITHOUT：browser翻页手动抓
- WITH：动态LLM分类+结构化输出到多个文件，WITHOUT：手动归类+单一报告
- WITH：关联度评分（四维度），WITHOUT：无
- WITH：退出码处理+API调用控制，WITHOUT：无异常处理
- WITH 预计12-20分钟，WITHOUT 预计15-20分钟但数据量差距巨大
