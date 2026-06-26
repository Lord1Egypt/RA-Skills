# 修复清单

所有已修复的 bug 和改进。

## L1 修复（5 项）

| # | 问题 | 修复 | 验证 |
|---|------|------|------|
| 1 | quality_check 在 denoise 之前 | ✅ 改为先 denoise，再 quality_check | ✓ |
| 2 | classify_memory_type 在 denoise 之前 | ✅ 改为去噪后分类 | ✓ |
| 3 | assign_priority_tier 用去噪前 type | ✅ 改为基于去噪后 type | ✓ |
| 4 | Ollama 编码失败时零向量写入 L2A | ✅ 改为 `_dropped=True` | ✓ |
| 5 | save_to_l2a 不过滤 dedup_level>0 | ✅ 只写 dedup_level=0 | ✓ |

## L2 修复（6 项）

| # | 问题 | 修复 | 验证 |
|---|------|------|------|
| 1 | session_graph 在 dedup 前构建 | ✅ 改为先 dedup，再建图 | ✓ |
| 2 | save_to_l2 在 mark_l2a_processed 之前 | ✅ 改为先 mark，再 save | ✓ |
| 3 | save_to_l2 用 `a` 模式追加 | ✅ 改为 atomic write (rename) | ✓ |
| 4 | session_graph 用 split() 分词 | ✅ 改用 N-gram + 停用词过滤 | ✓ |
| 5 | overlap≥2 false positive 严重 | ✅ 提高到 overlap≥3 + 停用词 | ✓ |
| 6 | content_hash_index 跨 run 隔离 | ✅ 每 cron run 新建实例 | ✓ |

## L3 修复（9 项）

| # | 问题 | 修复 | 验证 |
|---|------|------|------|
| A | OllamaEncoder 逐条编码，batch_size 失效 | ✅ 批量 input:texts | ✓ |
| C | 零向量写入 Brain.db + InfinityDB + HNSW | ✅ 零向量跳过 | ✓ |
| D | generate_schema_neuron 阈值≥10 过高 | ✅ 改为 ≥5 | ✓ |
| E | SCHEMA priority=6 高于普通 chunks | ✅ 改为 priority=4 | ✓ |
| G | load_l2_chunks 只加载当天文件 | ✅ 改为扫描所有 .jsonl | ✓ |
| H | encode_batch 过滤后不对齐原始顺序 | ✅ id() 映射 + None 保留位置 | ✓ |
| I | mark_l2_graph_written 只删当天文件 | ✅ 改为扫描所有日期 | ✓ |
| J | written_ids 包含零向量 chunk | ✅ 只包含成功写入的 id | ✓ |

## 五项保证

| 保证 | 实现 |
|------|------|
| 防断裂 | 50字 overlap、atomic write、byte offset |
| 防丢失 | tmp 保护、written_ids 追踪、graph_written 标记 |
| 防质量下降 | denoise→quality→classify 顺序、零向量过滤 |
| 防关系错乱 | session graph + transitive closure |
| 防索引混乱 | 四级去重、content_hash_index 隔离 |