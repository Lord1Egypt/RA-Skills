# 架构参考

## 核心设计原则

1. **持久化优先**：所有推断结果存 SQLite，NL2SQL 直接读库，零重复推理
2. **增量更新**：schema 指纹变化才重新推断，存量稳定后 API 成本趋近于零
3. **飞轮自进化**：每次人工审核 → 黄金样本 → DSPy 重新优化 → Level1 准确率提升 → 人工减少

## 三级流水线

```
Level1（内部小模型）
  置信度 ≥ 85%  → 自动写回
  置信度 70-84% → Self-Consistency（5次采样，≥60%一致则通过）
                 → 不通过 → Level2
  置信度 < 70%  → 直接入人工队列

Level2（外部超级模型）
  Level2 置信度 ≥ 85% → 自动写回
  Level2 置信度 < 85% → 人工队列

Level3（人工）
  Active Learning 排序（不确定性 + 覆盖度）
  审核结果 → 黄金样本池 → 触发缩写词典挖掘
```

## DSPy 冷启动策略

```
数仓现有备注（哪怕只有 10% 覆盖率）
  ↓ 质量过滤（排除占位符、纯英文、过短）
  ↓ 分层采样（各业务域均衡）→ 400 条 train + 100 条 val
  ↓ MIPROv2 优化（50 次候选）
  ↓ 输出：optimized_annotator.json（固化最优 prompt）
```

评估指标：字符集重叠度（≥ 60% 算通过），不用精确匹配（同一字段可有多种正确表达）

## 数据流

```
Hive Metastore
  └── DESC table          → field_metadata (SQLite)
  └── SELECT LIMIT 20     → 样本（临时，不持久化）
  └── SHOW CREATE VIEW    → dml_expression (持久化)

field_metadata
  └── review_status=approved → 写回 Hive COMMENT
  └── reviewed_by=human     → gold_labels
  └── level1 vs final 有差异 → corrections

gold_labels → mine_abbreviations → abbrev_dict
corrections （积累 200 条）→ evolve_rules → prompt_rules
gold_labels （积累 5000 条）→ dspy_bootstrap → optimized_annotator.json
```

## 扩展新数据栈

继承 `BaseConnector` 并实现 4 个方法：

```python
class BaseConnector:
    def get_tables(self, db) -> list[str]: ...
    def get_schema(self, db, table) -> list[dict]: ...
    def get_samples(self, db, table, field, n=20) -> list: ...
    def get_dml(self, db, table) -> str: ...
    def writeback_comment(self, db, table, field, comment) -> bool: ...
```

已支持：Hive（pyhive）
可扩展：MaxCompute（pyodps）、MySQL（pymysql）、Doris、Spark SQL

## SQLite 表结构

| 表 | 用途 |
|----|------|
| `field_metadata` | 核心：所有字段的推断结果和状态 |
| `gold_labels` | 黄金样本池（人工/Level2 审核通过） |
| `abbrev_dict` | 自动挖掘的缩写映射词典 |
| `prompt_rules` | 从失败案例提炼的标注规则 |
| `corrections` | Level1 vs 最终结果的差异记录 |
| `domain_prompts` | 各业务域专属 prompt 提示 |
| `system_state` | 系统状态（DSPy 编译时间等） |
