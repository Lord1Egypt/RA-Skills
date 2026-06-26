# 数据库分析与报告生成技能

## 技能名称
db-analyst

## 触发关键词
- 分析数据库
- 查询数据
- 生成报告
- 分析报告
- 数据库查询

## 功能描述
通过curl调用数据库API接口，查询指定表的数据，进行数据分析，并生成Word文档分析报告。

## 使用方法

### 1. 查询数据
```bash
curl -X POST --max-time 300 -H "Content-Type: application/json" \
  -d '{"sql": "SELECT * FROM <表名> LIMIT 100 OFFSET 0"}' \
  "http://192.168.5.85:8000/query"
```

### 2. 使用关键词映射表查询
先查阅 `表名关键词映射.txt` 找到对应的表名和查询示例。

### 3. 分析数据并生成报告
运行 Python 脚本:
```bash
python3 /root/.openclaw/workspace/skills/db-analyst/analyze_data.py
```

## 包含文件
- `analyze_data.py` - 数据分析并生成Word报告的Python脚本
- `表名关键词映射.txt` - 关键词到表名的映射表

## 数据分析报告内容
- 数据概览（总条数）
- 纠纷类型分析
- 纠纷原因分析
- 发生地点分析
- 时间分布
- 处置单位与联系方式
- 总结
- 原始数据表格

## 示例
查询婚姻纠纷数据并生成报告:
1. 查看映射表找到表名: chujingxinxibiao_Sheet1_1732674000130
2. 执行查询: curl -X POST ... 
3. 运行分析脚本生成报告