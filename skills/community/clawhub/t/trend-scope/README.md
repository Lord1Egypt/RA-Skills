# TrendScope - 舆情趋势洞察

基于 Feedax API 的舆情分析报告生成工具。

本 Skill 可实现全网内容智能分析与专业报告自动生成，具备多源信息归集、情感研判、热点挖掘等能力。

## 功能特性

- 📊 **多维度数据分析**: 情感分布、地域分布、媒体分布、关键词分析、时间趋势等
- 📝 **自动生成报告**: 支持 JSON 原始数据 + Markdown + Html 可视化报告
- 🎯 **多条件筛选**: 支持媒体平台、情感倾向、时间范围、地域等多维度筛选
- ⚡ **一键调用**: AI Agent 可直接调用，快速生成专业报告

## 适用场景

- 品牌动态监测
- 市场分析报告
- 竞品追踪分析
- 热点事件分析
- 舆情趋势研判

## 快速开始

### 1. 安装

用户对智能体说：

> 帮我安装并学习这个技能: https://gitee.com/feedax/trend-scope.git

### 2. 配置 API Key

在宿主环境设置 `FEEDAX_REPORT_API_KEY`，或使用项目内 `.env`（**勿在对话中粘贴密钥**）：

```bash
cp .env.example .env
# 编辑 .env，设置 FEEDAX_REPORT_API_KEY=你的密钥
```

### 3. 生成报告

```bash
# 基础报告
python3 scripts/report_cli.py --query "比亚迪"

# 指定时间范围和地域
python3 scripts/report_cli.py --query "南京 教育" --area "南京" --days 7

# 全维度分析
python3 scripts/report_cli.py --query "医疗问题" --full-analysis

# 指定平台和情感
python3 scripts/report_cli.py --query "315投诉" --media "微博,抖音" --sentiment negative
```

## 输出文件

报告文件默认保存至 `~/Desktop/舆情分析报告/` 目录：

- `{查询词}_{时间戳}.json` - 原始数据（JSON格式）
- `{查询词}_{时间戳}.md` - 可视化报告（Markdown格式）
- `{查询词}_{时间戳}.html` - 可视化报告（HTML格式）

## 文档

详见 `skill.md` 获取完整的参数说明和使用指南。
