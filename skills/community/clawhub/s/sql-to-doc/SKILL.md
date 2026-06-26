---
name: sql-to-doc
description: 执行SQL查询并将结果按照指定模板整理后写入飞书云文档。适用于数据周报、数据汇总、统计报告等场景。
metadata: {
  "openclaw": {
    "requires": {
      "env": ["META_CENTER_TOKEN", "DATAWORKS_PROJECT"]
    }
  }
}
---

## 功能
将「SQL查询 → 数据整理 → 写入文档」全流程封装为可复用的 skill：
1. 连接 MaxCompute/DataWorks 执行 SQL 查询
2. 按照 Jinja2 模板格式整理数据
3. 在飞书知识库或云空间中创建文档
4. 返回文档链接

## 使用场景
- 定期数据周报自动生成
- 业务数据汇总统计
- 一次性数据查询并生成报告
- 将 SQL 结果导出为可读文档

## 配置参数
| 参数 | 说明 | 示例 |
|------|------|------|
| sql_query | 要执行的 SQL 语句 | SELECT * FROM table_name WHERE ... |
| template | 数据整理模板（Jinja2格式） | 详见下方模板语法 |
| doc_title | 生成的文档标题 | 收钱吧周报2026年第15周 |
| target_location | 目标位置 | wiki:space_id:node_token 或 folder:folder_token |
| notify_user | 完成后通知的用户 open_id | ou_xxx（可选） |

## 模板语法
使用 Jinja2 模板语法整理数据：

```jinja
## {{ title }}

### 数据汇总

| 指标 | 数值 | 环比 |
|------|------|------|
{% for row in data %}
| {{ row.indicator }} | {{ row.value }} | {{ row.change }} |
{% endfor %}

### 详细数据

{{ data_table }}
```

## 使用方式

### 1. 简单查询
```
帮我执行 SQL：SELECT * FROM wosai_hz_bi.ads_sqb_comprehensive_business_data_statistics_w
并把结果写入文档
```

### 2. 带模板的数据整理
```
查询 wosai_hz_bi.ads_sqb_comprehensive_business_data_statistics_w 近五周数据，
按照收钱吧周报格式整理，写入知识库
```

### 3. 完整参数指定
```
执行 SQL: SELECT stat_week, total_trans_cnt FROM table
模板：按周汇总表格
文档标题：交易周报
目标：知识库 space_id=7396876397862764545, node=Dv3YwcsXEimpeokAORkc7K8fnhh
```

## 执行流程
1. **SQL 执行**：使用 maxcompute 连接查询数据
2. **数据处理**：将 SQL 结果转换为 Python 对象（列表/字典）
3. **模板渲染**：使用 Jinja2 渲染模板 + 数据
4. **文档创建**：调用 feishu_create_doc 创建云文档
5. **通知用户**（可选）：发送文档链接给指定用户

## 输出
- 飞书云文档链接
- 文档创建状态

## 相关工具
- maxcompute SQL 执行（通过 exec 调用 DataWorks OpenAPI）
- feishu_create_doc - 创建云文档
- feishu_im_user_message - 发送通知
