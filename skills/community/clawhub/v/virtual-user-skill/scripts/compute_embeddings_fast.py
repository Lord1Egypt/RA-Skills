#!/usr/bin/env python3
"""超小批量计算向量，实时显示进度"""
import sys, json, numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from encrypt import EncryptManager

MODEL_NAME = 'shibing624/text2vec-base-chinese'
BATCH_SIZE = 5000  # 每批 5000 条

print("📐 超小批量计算向量")
print("=" * 60)

# 读取场景库
manager = EncryptManager()
with open('data/scenario_library.json.enc', 'r') as f:
    scenarios = json.loads(manager.decrypt_data(f.read()))

print(f"总场景数：{len(scenarios):,} 条")
print(f"批次大小：{BATCH_SIZE:,} 条/批")
print(f"总批次数：{(len(scenarios) + BATCH_SIZE - 1) // BATCH_SIZE}")

# 加载模型
print(f"\n🤖 加载模型：{MODEL_NAME}...")
model = SentenceTransformer(MODEL_NAME)
print("✅ 模型加载完成")

# 分批计算
all_embeddings = []
total = len(scenarios)
processed = 0

print("\n开始计算：")
for i in range(0, total, BATCH_SIZE):
    batch = scenarios[i:i+BATCH_SIZE]
    batch_num = i // BATCH_SIZE + 1
    total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
    
    # 生成文本
    texts = []
    for s in batch:
        parts = []
        if s.get('用户具体场景'): parts.append(f"场景：{s['用户具体场景'][:50]}")
        if s.get('任务'): parts.append(f"任务：{s['任务'][:30]}")
        if s.get('痛点'): parts.append(f"痛点：{s['痛点'][:30]}")
        if s.get('底层需求'): parts.append(f"需求：{s['底层需求'][:30]}")
        texts.append(" | ".join(parts))
    
    # 计算
    print(f"\n[{batch_num}/{total_batches}] {i+1:,}-{min(i+BATCH_SIZE, total):,}...", end=' ', flush=True)
    embeddings = model.encode(texts, show_progress_bar=False, batch_size=32)
    all_embeddings.append(embeddings)
    
    processed += len(batch)
    pct = processed / total * 100
    print(f"✅ 完成 {len(batch):,}条 (累计 {processed:,}条，{pct:.1f}%)")

# 合并
print("\n\n📊 合并所有向量...")
final_embeddings = np.vstack(all_embeddings)
print(f"最终形状：{final_embeddings.shape}")

# 保存
print("\n💾 保存向量文件...")
np.save('data/scenario_embeddings.npy', final_embeddings)
file_size = final_embeddings.nbytes / 1024 / 1024
print(f"✅ 保存完成：data/scenario_embeddings.npy ({file_size:.1f}MB)")

print("\n" + "=" * 60)
print("🎉 向量计算完成！")
print("=" * 60)
