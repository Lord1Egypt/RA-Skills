#!/usr/bin/env python3
"""后台计算向量"""
import sys, json, numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from encrypt import EncryptManager

print("📐 计算向量...")
MODEL_NAME = 'shibing624/text2vec-base-chinese'

# 读取场景库
manager = EncryptManager()
with open('data/scenario_library.json.enc', 'r') as f:
    scenarios = json.loads(manager.decrypt_data(f.read()))

print(f"场景数：{len(scenarios):,}")

# 加载模型
print(f"加载模型：{MODEL_NAME}")
model = SentenceTransformer(MODEL_NAME)

# 生成文本
texts = []
for s in scenarios:
    parts = []
    if s.get('用户具体场景'): parts.append(f"场景：{s['用户具体场景']}")
    if s.get('任务'): parts.append(f"任务：{s['任务']}")
    if s.get('痛点'): parts.append(f"痛点：{s['痛点']}")
    if s.get('底层需求'): parts.append(f"需求：{s['底层需求']}")
    texts.append(" | ".join(parts))

# 计算向量
print(f"计算 {len(texts):,} 条向量...")
embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)

# 保存
np.save('data/scenario_embeddings.npy', embeddings)
print(f"✅ 完成！向量形状：{embeddings.shape}")
