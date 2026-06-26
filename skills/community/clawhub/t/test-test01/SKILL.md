---
name: test-test01
description: 从test页面获取数据导入到test01
author: Digital Employee Platform Team
category: productivity
tags:
 
  - RPA
  - excel

triggers:
 
  - RPA
  - 数据转储

config:
  pcs_url: "http://1x.xx.xx.xx:5173"
  pcs_page: "/#/vmodelDemo"
  epbp_page: "/#/home"
 
 

requires:
  python: true
  playwright: true
---

# test数据自动转储录入技能

## 功能说明

自动从 PCS 页面抓取表格数据，导出 Excel 后导入到 EBP 系统。

## 安装依赖

```bash
pip install playwright openpyxl
playwright install chromium
```

## 使用方式

```bash
cd ~/.openclaw/skills/pcs-epbp/scripts
python main.py
```

## 工作流程

1. 打开 PCS 页面：http://xxx:5173/#/vmodelDemo
2. 抓取表格数据
3. 导出为 Excel (pcs_data.xlsx)
4. 打开 EBP 页面：http://xxx:5173/#/home
5. 自动上传 Excel 并导入

## 定时任务

可配合 cron 实现每日自动执行：

```bash
# 每天上午9点执行
0 9 * * * cd ~/.openclaw/skills/test-test01/scripts && python main.py
```

## 注意事项

- 首次运行需要安装 Playwright 浏览器
- 如页面结构变化，需调整选择器
- EBP 导入按钮选择器可能需要根据实际页面调整
