import time
import math
import argparse
import sys
import os

# 尝试导入 Chroma
try:
    import chromadb
    from chromadb.config import Settings
    HAS_CHROMA = True
except ImportError:
    HAS_CHROMA = False

WORKSPACE_ROOT = os.path.expanduser(r"~/.openclaw/workspace")
CHROMA_PATH = os.path.join(WORKSPACE_ROOT, r"database\chroma_store")

def perform_nightly_consolidation():
    """
    执行"梦境整理"：
    1. 扫描所有活跃记忆
    2. 计算当前衰减后的分数
    3. 将低分记忆归档
    """
    if not HAS_CHROMA:
        print("[ERROR] 缺少 Chroma，无法执行维护。")
        return

    print("[START] 开始梦境整理...")
    
    try:
        # 适配 Chroma API
        if hasattr(chromadb, 'PersistentClient'):
            client = chromadb.PersistentClient(path=CHROMA_PATH)
        else:
            client = chromadb.Client(Settings(persist_directory=CHROMA_PATH))
            
        collection = client.get_or_create_collection(name="fluid_memory")
    except Exception as e:
        print(f"[ERROR] 连接数据库失败: {e}")
        return

    # 获取所有活跃记忆 (Metadata)
    # Chroma get() 不支持复杂的 filtering logic，我们需要把 metadata 拉出来算
    results = collection.get(
        where={"status": "active"},
        include=["metadatas", "documents"]
    )
    
    if not results['ids']:
        print("[INFO] 大脑是空的，无需整理。")
        return

    ids = results['ids']
    metas = results['metadatas']
    docs = results['documents']
    
    archived_count = 0
    now = time.time()
    LAMBDA_DECAY = 0.05
    ALPHA_BOOST = 0.2
    ARCHIVE_THRESHOLD = 0.15 # 低于 0.15 分归档 (比较激进)

    for i, mem_id in enumerate(ids):
        meta = metas[i]
        created_at = meta.get('created_at', now)
        access_count = meta.get('access_count', 0)
        
        # 计算当前分数
        # 注意：这里我们只计算"时间+频率"的基础分，不包含相似度
        # 这代表这段记忆在"真空"中的绝对价值
        days_passed = (now - created_at) / 86400
        decay = math.exp(-LAMBDA_DECAY * days_passed)
        boost = ALPHA_BOOST * math.log(1 + access_count)
        
        # 基础存在感 = 1.0 * decay + boost
        base_score = decay + boost
        
        if base_score < ARCHIVE_THRESHOLD:
            print(f"   [ARCHIVE] 记忆褪色: '{docs[i][:20]}...' (Score: {base_score:.3f})")
            
            # 更新状态为 archive
            meta['status'] = 'archive'
            collection.update(ids=[mem_id], metadatas=[meta])
            archived_count += 1

    print(f"[DONE] 整理完成。共归档 {archived_count} 条记忆。")

    # 2. 硬删除逻辑 (Hard Delete)
    # 查找所有 archive 状态且归档超过 120 天的记忆
    archive_results = collection.get(
        where={"status": "archive"},
        include=["metadatas"]
    )
    
    hard_delete_ids = []
    HARD_DELETE_DAYS = 120
    
    if archive_results['ids']:
        ids = archive_results['ids']
        metas = archive_results['metadatas']
        
        for i, mem_id in enumerate(ids):
            meta = metas[i]
            last_accessed = meta.get('last_accessed', now)
            days_inactive = (now - last_accessed) / 86400
            
            if days_inactive > HARD_DELETE_DAYS:
                hard_delete_ids.append(mem_id)
    
    if hard_delete_ids:
        print(f"[CLEANUP] 发现 {len(hard_delete_ids)} 条长期归档记忆，正在物理删除...")
        collection.delete(ids=hard_delete_ids)
        print(f"[DONE] 物理删除完成。释放空间。")

if __name__ == "__main__":
    perform_nightly_consolidation()
