"""
图片AI搜索 - 增量更新脚本
只处理新增的图片，追加到现有索引，无需全量重建
"""
import os
import sys

# 自动设置 HuggingFace 缓存目录
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ.setdefault('HF_HOME', os.path.join(os.path.expanduser('~'), '.cache', 'huggingface'))

# 添加脚本目录到路径，以便导入 config
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

import json
import pickle
import numpy as np
from pathlib import Path
from tqdm import tqdm
import torch
from PIL import Image
import faiss

from config import (
    SCAN_ROOTS, EXCLUDE_DIRS, EXCLUDE_KEYWORDS,
    IMAGE_EXTENSIONS, MODEL_NAME, BATCH_SIZE,
    DB_DIR, INDEX_FILE, IMAGE_LIST_FILE
)

def get_all_drives():
    """自动检测所有可用盘符"""
    drives = []
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        path = f"{letter}:\\"
        if os.path.exists(path):
            drives.append(path)
    return drives

def find_images(roots):
    """递归扫描所有图片"""
    images = []
    roots = roots if roots else get_all_drives()
    exclude_dirs_set = set(EXCLUDE_DIRS)
    
    print(f"开始扫描 {len(roots)} 个根目录...")
    for root in roots:
        print(f"  -> 扫描 {root}")
        try:
            for dirpath, dirnames, filenames in os.walk(root):
                # 跳过排除的目录
                dirnames[:] = [d for d in dirnames if d not in exclude_dirs_set and not d.startswith('.')]
                
                for filename in filenames:
                    ext = Path(filename).suffix.lower()
                    if ext in IMAGE_EXTENSIONS:
                        if any(kw in filename.lower() for kw in EXCLUDE_KEYWORDS):
                            continue
                        full_path = os.path.join(dirpath, filename)
                        images.append(full_path)
        except PermissionError:
            print(f"  -> 跳过 {root} (无权限)")
    
    return images

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
        print("本地模型不存在，正在下载（首次运行需要网络连接）...")
        model = ChineseCLIPModel.from_pretrained(MODEL_NAME)
        processor = ChineseCLIPProcessor.from_pretrained(MODEL_NAME)
    
    model = model.to(device)
    model.eval()
    
    return model, processor, device

def extract_features(images, model, processor, device):
    """批量提取图片特征"""
    features = []
    failed = 0
    
    for i in tqdm(range(0, len(images), BATCH_SIZE), desc="提取特征"):
        batch_paths = images[i:i+BATCH_SIZE]
        batch_images = []
        valid_mask = []
        
        for path in batch_paths:
            try:
                img = Image.open(path).convert('RGB')
                batch_images.append(img)
                valid_mask.append(True)
            except Exception:
                failed += 1
                batch_images.append(Image.new('RGB', (224, 224), color='black'))
                valid_mask.append(False)
        
        try:
            inputs = processor(images=batch_images, return_tensors="pt", padding=True)
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = model.get_image_features(**inputs)
                image_features = outputs.pooler_output
                image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            
            for j, valid in enumerate(valid_mask):
                if valid:
                    features.append(image_features[j].cpu().numpy())
                else:
                    features.append(np.zeros(512, dtype=np.float32))
                    
        except Exception as e:
            print(f"\n处理批次失败: {e}")
            for _ in batch_paths:
                features.append(np.zeros(512, dtype=np.float32))
    
    print(f"\n处理完成: 成功 {len(images) - failed}, 失败 {failed}")
    return features, failed

def load_existing_index():
    """加载现有索引"""
    if not os.path.exists(INDEX_FILE) or not os.path.exists(IMAGE_LIST_FILE):
        return None, []
    
    index = faiss.read_index(INDEX_FILE)
    
    with open(IMAGE_LIST_FILE, 'rb') as f:
        existing_paths = pickle.load(f)
    
    return index, existing_paths

def append_to_index(index, new_features, new_paths, existing_paths):
    """将新特征追加到索引"""
    if not new_features:
        return index
    
    features_array = np.array(new_features).astype('float32')
    index.add(features_array)
    all_paths = existing_paths + new_paths
    
    return index, all_paths

def save_index(index, all_paths):
    """保存更新后的索引"""
    faiss.write_index(index, INDEX_FILE)
    
    with open(IMAGE_LIST_FILE, 'wb') as f:
        pickle.dump(all_paths, f)
    
    meta = {
        "model": MODEL_NAME,
        "count": len(all_paths),
        "dimension": index.d
    }
    with open(os.path.join(DB_DIR, "meta.json"), 'w') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

def main():
    print("=" * 50)
    print("图片AI搜索 - 增量更新")
    print("=" * 50)
    
    # 检查是否存在现有索引
    index, existing_paths = load_existing_index()
    
    if index is None:
        print("\n⚠️  未找到现有索引，请先运行: python scan.py")
        return
    
    print(f"\n当前索引: {len(existing_paths)} 张图片")
    
    # 扫描所有图片
    print("\n[1/3] 扫描图片文件...")
    all_images = find_images(SCAN_ROOTS)
    print(f"找到 {len(all_images)} 张图片")
    
    # 找出新增图片
    existing_set = set(existing_paths)
    new_images = [img for img in all_images if img not in existing_set]
    
    print(f"\n新增图片: {len(new_images)} 张")
    
    if not new_images:
        print("\n✅ 没有新增图片，索引已是最新！")
        return
    
    # 加载模型
    print("\n[2/3] 加载AI模型...")
    model, processor, device = load_clip_model()
    
    # 提取新图片特征
    print(f"\n[3/3] 提取 {len(new_images)} 张新图片的特征...")
    new_features, failed = extract_features(new_images, model, processor, device)
    
    # 追加到索引
    print("\n更新索引...")
    index, all_paths = append_to_index(index, new_features, new_images, existing_paths)
    
    # 保存
    save_index(index, all_paths)
    
    print(f"\n✅ 完成！索引已更新，共 {len(all_paths)} 张图片")
    print(f"   新增: {len(new_images)} 张")
    print(f"   失败: {failed} 张")

if __name__ == "__main__":
    main()