#!/usr/bin/env python3
"""分批计算向量，避免超时"""
import sys, json, numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from encrypt import EncryptManager

MODEL_NAME = 'shibing624/text2vec-base-chinese'
BATCH_SIZE = 10000

print("📐 分批计算向量")
print("=" * 60)

# 读取场景库
manager = EncryptManager()
with open('data/scenario_library.json.enc', 'r') as f:
    scenarios = json.loads(manager.decrypt_data(f.read()))

print(f"总场景数：{len(scenarios):,} 条")

# 加载模型
print(f"\n🤖 加载模型：{MODEL_NAME}")
model = SentenceTransformer(MODEL_NAME)

# 分批计算
all_embeddings = []
total_batches = (len(scenarios) + BATCH_SIZE - 1) // BATCH_SIZE

for i in range(0, len(scenarios), BATCH_SIZE):
    batch_num = i // BATCH_SIZE + 1
    batch = scenarios[i:i+BATCH_SIZE]
    
    print(f"\n[{batch_num}/{total_batches}] 计算批次 {i}-{min(i+BATCH_SIZE, len(scenarios))}...")
    
    texts = []
    for s in batch:
        parts = []
        if s.get('用户具体场景'): parts.append(f"场景：{s['用户具体场景']}")
        if s.get('任务'): parts.append(f"任务：{s['任务']}")
        if s.get('痛点'): parts.append(f"痛点：{s['痛点']}")
        if s.get('底层需求'): parts.append(f"需求：{s['底层需求']}")
        texts.append(" | ".join(parts))
    
    embeddings = model.encode(texts, show_progress_bar=False, batch_size=32)
    all_embeddings.append(embeddings)
    print(f"   ✅ 完成，形状：{embeddings.shape}")

# 合并所有向量
print("\n📊 合并向量...")
final_embeddings = np.vstack(all_embeddings)
print(f"最终形状：{final_embeddings.shape}")

# 保存
np.save('data/scenario_embeddings.npy', final_embeddings)
print(f"\n✅ 保存完成：data/scenario_embeddings.npy")
print(f"文件大小：{final_embeddings.nbytes / 1024 / 1024:.1f}MB")
