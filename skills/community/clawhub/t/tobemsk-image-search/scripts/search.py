"""
图片AI搜索 - 搜索脚本
通过关键词搜索本地图片
"""
import os
import sys

# 自动设置 HuggingFace 缓存目录
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ.setdefault('HF_HOME', os.path.join(os.path.expanduser('~'), '.cache', 'huggingface'))

# 添加脚本目录到路径，以便导入 config
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

import pickle
import torch
from pathlib import Path

from config import MODEL_NAME, DB_DIR, IMAGE_LIST_FILE, INDEX_FILE

def load_index():
    """加载索引和图片列表"""
    if not os.path.exists(INDEX_FILE):
        print("未找到索引文件，请先运行 scan.py 建库")
        return None, None
    
    import faiss
    index = faiss.read_index(INDEX_FILE)
    
    with open(IMAGE_LIST_FILE, 'rb') as f:
        images = pickle.load(f)
    
    return index, images

def load_clip_model():
    """加载CLIP模型"""
    print(f"加载模型: {MODEL_NAME}")
    from transformers import ChineseCLIPModel, ChineseCLIPProcessor
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"使用设备: {device}")
    
    # 尝试本地加载，如果失败则联网下载
    try:
        model = ChineseCLIPModel.from_pretrained(MODEL_NAME, local_files_only=True)
        processor = ChineseCLIPProcessor.from_pretrained(MODEL_NAME, local_files_only=True)
    except:
        print("本地模型不存在，正在下载...")
        model = ChineseCLIPModel.from_pretrained(MODEL_NAME)
        processor = ChineseCLIPProcessor.from_pretrained(MODEL_NAME)
    
    model = model.to(device)
    model.eval()
    
    return model, processor, device

def search(query, top_k=20):
    """搜索图片"""
    # 加载模型
    model, processor, device = load_clip_model()
    
    # 加载索引
    index, images = load_index()
    if index is None:
        return []
    
    # 提取查询文本的特征
    print(f"搜索: \"{query}\"")
    inputs = processor(text=[query], return_tensors="pt", padding=True, truncation=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model.get_text_features(**inputs)
        text_features = outputs.pooler_output
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
    
    query_vector = text_features.cpu().numpy().astype('float32')
    
    # 搜索（内积索引，值越大越相似）
    similarities, indices = index.search(query_vector, top_k)
    
    results = []
    for sim, idx in zip(similarities[0], indices[0]):
        if idx < len(images):
            path = images[idx]
            sim_pct = min(sim * 100, 99.9)
            results.append((path, sim_pct))
    
    return results

def main():
    if len(sys.argv) < 2:
        print("用法: python search.py <关键词> [数量]")
        print("示例: python search.py 猫 30")
        print("示例: python search.py \"日落海滩\"")
        return
    
    query = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    
    results = search(query, top_k)
    
    if not results:
        print("未找到相关图片")
        return
    
    print(f"\n找到 {len(results)} 张相关图片:\n")
    print("=" * 80)
    
    for i, (path, sim) in enumerate(results, 1):
        print(f"{i:2d}. [{sim:5.1f}%] {path}")
    
    print("=" * 80)
    print(f"\n提示: 路径可以直接复制到资源管理器打开")
    
    # 自动保存到桌面
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_query = safe_query.replace(' ', '_')[:20]
    output_file = os.path.join(desktop, f"搜索结果_{safe_query}.txt")
    
    try:
        from datetime import datetime
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"搜索词: {query}\n")
            f.write(f"时间: {datetime.now()}\n")
            f.write(f"结果数量: {len(results)}\n")
            f.write("=" * 60 + "\n")
            for i, (path, sim) in enumerate(results, 1):
                f.write(f"{i:2d}. [{sim:5.1f}%] {path}\n")
        print(f"\n✅ 结果已保存到: {output_file}")
    except Exception as e:
        print(f"\n❌ 保存文件失败: {e}")

if __name__ == "__main__":
    main()