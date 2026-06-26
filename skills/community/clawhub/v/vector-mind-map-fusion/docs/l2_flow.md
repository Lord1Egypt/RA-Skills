# L2 整理流程

## 入口
`src/l2/l2_cron.py`

## 流程

```
load_l2a_chunks()  # 扫描所有日期 L2A 文件
    ↓
L2Processor.process()
    ↓
Step1: session 分组
Step2: sliding_windows(window_size=200, overlap=100)
Step3: _dedup_window() ← 四级去重（先执行！）
Step4: build_session_graph() ← 基于去重后 unique chunks
Step5: transitive_closure() ← 完整图上做
    ↓
apply_dynamic_priority()  # session 内引用≥3 → priority+2
    ↓
mark_l2a_processed() ← 先 mark（防 crash）
save_to_l2() ← 再 save（atomic rename）
```

## 四级去重

| 级别 | 方法 | 说明 |
|------|------|------|
| Level 1 | content_hash 精确匹配 | 完全相同 |
| Level 2 | Type 协同 cosine | boundary=0.85, default=0.90 |
| Level 3 | simhash 近似去重 | 相似内容 |
| Level 4 | hnsw 向量 | threshold=0.95 |

## 关键修复

| 修复 | 内容 |
|------|------|
| 顺序 | dedup→建图→closure（之前是建图→closure→dedup） |
| mark→save | mark 先执行，再 save（防 crash 重复写入） |
| atomic | save_to_l2 用 rename |
| session graph | N-gram 中文分词（之前用 split() 对中文无效） |
| overlap | ≥3 + 停用词过滤（之前≥2 false positive） |
| content_hash_index | 每 run 新实例（之前跨 run 污染） |

## 配置

- window_size: 200
- overlap: 100
- SQLITE_BATCH_SIZE: 200
- MAX_CHUNKS_PER_RUN: 5000