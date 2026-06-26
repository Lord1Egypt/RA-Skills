---
name: daily-report-generator
version: "1.5.0"
description: "本地日报/周报生成工具。输入JSON格式工作数据，生成结构化的Markdown格式工作报告，支持日报、周报、数据指标表格和风险提示。"
metadata:
  openclaw:
    emoji: "📊"
    category: productivity

## 功能
- 生成日报或周报
- 完成事项、进行中事项、计划事项分类展示
- 风险/阻塞提示标记
- 支持数据指标表格（周报）
- 输出Markdown格式，可直接复制到任何平台

## 使用方法
```bash
# 生成日报
python3 scripts/generate_report.py --type daily

# 生成周报
python3 scripts/generate_report.py --type weekly

# 指定日期
python3 scripts/generate_report.py --type daily --date 2026-04-10

# 从JSON数据文件生成
python3 scripts/generate_report.py --data my_data.json
```

## 数据输入（可选）
支持JSON格式数据文件，示例：
```json
{
  "completed": ["完成用户调研报告", "上线新功能A"],
  "in_progress": ["优化登录流程"],
  "planned": ["编写技术文档"],
  "risks": ["第三方API不稳定"],
  "metrics": [{"name": "DAU", "value": "1000", "change": "+5%"}]
}
```

无数据文件时自动使用空模板，可手动填充。

## 参数
- `--type`：报告类型，daily 或 weekly（默认 daily）
- `--date`：目标日期 YYYY-MM-DD（可选，默认今天）
- `--data`：JSON数据文件路径（可选）
- `--output`：输出方式，doc/chat/both（默认 doc）

## 依赖
- Python 3.7+（纯标准库：datetime, json, argparse）

## 更新说明
- v1.5.0: 彻底移除飞书相关描述，重命名为daily-report-generator
- v1.4.1: 移除飞书API集成声明，修正功能描述为实际能力
- v1.4.0: 精简描述，移除未实现功能
