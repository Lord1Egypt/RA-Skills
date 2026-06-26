---
name: smart-reporter
description: 智能报告生成器 - 自动分析数据并生成专业报告。支持多种报告类型（日报、周报、月报、分析报告），可输出到飞书文档或本地文件。
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    install:
      - id: python3
        kind: binary
        binary: python3
        label: Install Python 3
---

# 智能报告生成器 (Smart Reporter)

自动分析数据源并生成专业格式的报告，支持多种输出格式和渠道。

## 功能特性

### 1. 多数据源支持
- 飞书多维表格
- CSV/Excel 文件
- JSON 数据
- 数据库查询结果

### 2. 报告类型
- **日报**: 工作进度、任务完成情况
- **周报**: 周期性总结、趋势分析
- **月报**: 业绩回顾、KPI分析
- **分析报告**: 深度数据分析、洞察发现

### 3. 智能分析
- 自动识别数据趋势
- 异常值检测
- 关键指标提取
- 对比分析

### 4. 输出渠道
- 飞书文档
- Markdown 文件
- HTML 页面
- PDF 文档

## 使用方法

```
生成报告:
1. 指定数据源（飞书表格/文件）
2. 选择报告类型
3. 设置时间范围
4. 自动生成并输出
```

## 报告模板

位于 `templates/` 目录，可自定义：
- `daily.md` - 日报模板
- `weekly.md` - 周报模板
- `monthly.md` - 月报模板
- `analysis.md` - 分析报告模板

## 示例场景

- 每日自动生成销售日报
- 每周汇总团队工作进度
- 每月分析业务数据趋势
- 按需生成专项分析报告

## 配置

在 `TOOLS.md` 中添加:

```markdown
### Smart Reporter
- Default Output: feishu_doc
- Report Timezone: Asia/Shanghai
- Auto Send: true
```

---

**版本**: 1.0.0
**作者**: @lijie
**分类**: 数据分析 / 报告生成
