---
name: 热点新闻Excel
description: "当用户发送热点新闻Excel文件时，自动：。触发词：skill, 优化, 数据, data。"
---

# SKILL: 热点新闻Excel处理

## 功能
当用户发送热点新闻Excel文件时，自动：
1. 解析Excel文件（按Sheet分类）
2. 提取热点内容并总结
3. 保存完整数据到 `/workspace/data/hotnews_YYYY-MM-DD.json`
4. 提供分类热点汇总

## 触发条件
- 用户发送 `.xlsx` 文件且文件名包含"热点"

## 执行流程

### 步骤1: 解析Excel
```bash
python3 /workspace/scripts/read_hotnews.py
```

### 步骤2: 读取数据
```python
# 读取保存的JSON
with open('/workspace/data/hotnews_YYYY-MM-DD.json', 'r') as f:
    data = json.load(f)
```

### 步骤3: 分类汇总
按Sheet分类输出：
- 其他: 84条
- 国际: 191条  
- 市场: 66条
- 公司: 38条
- 观点: 15条
- A股: 6条
- 宏观: 11条
- 数据: 4条
- 央行: 4条

### 步骤4: 提取重点
识别关键热点：
- 中东局势/伊朗
- 能源/油价
- A股市场
- 国内宏观
- 国际关系

## 输出格式

### 简要版
```
## 热点汇总 (YYYY-MM-DD)

### 重点
- 热点1
- 热点2

### 详细分类
[按Sheet分类列出]
```

### 完整版
保存到: `/workspace/data/hotnews_YYYY-MM-DD.json`

## 定时任务
配置cron每天早上8点检查并处理：

```bash
# 每天8点自动处理昨日热点
0 8 * * * cd /workspace && python3 scripts/read_hotnews.py >> /workspace/logs/hotnews.log 2>&1
```

## 依赖
- Python: zipfile, xml.etree.ElementTree, json
- 输入: Excel (.xlsx)
- 输出: JSON + Markdown汇总
