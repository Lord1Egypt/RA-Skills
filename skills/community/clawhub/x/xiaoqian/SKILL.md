---
name: xiaoqian
description: 自动查询江苏海事局综合平台会议信息并导出结构化数据
version: 1.0.1
author: Your Name
tags: [meeting, query, automation, jiangsu-msa]
category: web-automation
triggers: ["查询会议", "查看海事局会议", "获取会议信息", "导出会议数据"]
requirements:
  - selenium
  - pandas
  - openpyxl
  - webdriver-manager
input_schema:
  start_date:
    type: string
    description: 查询开始日期 (格式: YYYY-MM-DD)
    required: false
    default: today
  end_date:
    type: string
    description: 查询结束日期 (格式: YYYY-MM-DD)
    required: false
    default: today
output_format: excel
---
# 江苏海事局会议查询技能

## 技能描述
本技能自动登录江苏海事局综合平台，查询指定日期范围内的会议信息，并将结果导出为结构化的Excel文件。

## 系统配置
- **平台地址**: `http://gchportal.js-msa.gov.cn/cas/login`
- **账号**: `lp@njmsa`
- **密码**: `@lp280033`
- **查询单位**: 江苏海事局局机关

## 使用方式
用户可以通过以下方式触发本技能：
1. 直接询问：`查询今天的会议`
2. 指定日期：`查询2025-03-20的会议`
3. 日期范围：`查询从2025-03-20到2025-03-25的会议`

## 输出数据
技能执行后将生成Excel文件，包含以下字段：
- 日期 (Date)
- 开始时间 (StartTime)
- 会议标题 (MeetingTitle)
- 会议地点 (Location)
- 出席人员 (Attendees)
- 主办部门 (Organizer)

## 注意事项
1. 确保网络连接正常，可以访问江苏海事局综合平台
2. 账号密码敏感，建议通过环境变量配置
3. 查询结果受平台数据更新影响
4. 首次运行会自动下载Chrome WebDriver

---
*技能版本: 1.0.0 | 最后更新: 2025-03-20*