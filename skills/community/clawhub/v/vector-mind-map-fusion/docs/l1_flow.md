# L1 提取流程

## 入口
`src/l1/l1_cron.py`

## 流程

```
ByteOffsetScanner.scan()
    ↓
_stage1_filter() 过滤规则:
    1. too_short (<10字符且无4中文) → DROP
    2. cron_system_command → DROP
    3. pure_system_instruction → DROP
    4. pure_uuid → DROP
    5. empty_code_block → DROP
    6. metadata_label → DROP
    7. content_empty_after_filter → DROP
    ↓ 通过
_parse_user_message()
    ↓
L1Classifier.process()
    ↓
Step1: denoise_content()  ← 先去噪
Step2: content_quality_check() ← 去噪后质量检查
Step3: classify_memory_type() ← 去噪后分类
Step4: assign_priority_tier() ← 基于去噪后 type
Step5: chunk_content() ← 50字 overlap 防断裂
Step6: content_hash 精确去重（第1级）
Step7: Ollama bge-m3 向量编码
Step8: cosine > 0.85 近似去重（第2级）
    ↓
save_to_l2a()
    - valid_chunks = _dropped=False AND dedup_level=0
    - atomic write (rename)
```

## 关键修复

| 修复 | 内容 |
|------|------|
| 顺序 | denoise→quality→classify→priority |
| encoder 失败 | _dropped=True，不写入 L2A |
| dedup_level>0 | 过滤，不写入 L2A |
| overlap | 50字，防止内容断裂 |

## 配置

- MAX_CHUNK_CHARS: 250
- OVERLAP_CHARS: 50
- COSINE_THRESHOLD_L1: 0.85
- MAX_CONTENT_LENGTH: 5000
- TTL_DAYS: 7