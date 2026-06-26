#!/usr/bin/env python3
from safe_extension_loader import safe_load_extension
"""
L0 Vector Backfill - L0 向量补充（安全修复版）
为历史对话生成向量

安全修复：
- 移除硬编码 API 端点，从配置文件读取
- 移除 shell=False，使用参数列表
- 添加 os 模块导入
- 使用相对路径配置
"""

import os
import json
import sqlite3
import struct
import urllib.request
import time
from pathlib import Path
from typing import List, Dict, Optional

# 配置路径（使用相对路径）
CONFIG_DIR = Path(__file__).parent.parent / "config"
LLM_CONFIG = CONFIG_DIR / "llm_config.json"

# 数据库路径
VECTORS_DB = Path.home() / ".openclaw" / "memory-tdai" / "vectors.db"

# 向量扩展路径（动态检测）
def get_vec_extension_path() -> Path:
    """动态获取向量扩展路径"""
    possible_paths = [
        Path.home() / ".openclaw" / "extensions" / "memory-tencentdb" / "node_modules" / "sqlite-vec-linux-x64" / "vec0.so",
        Path.home() / ".openclaw" / "extensions" / "memory-tencentdb" / "node_modules" / "sqlite-vec-linux-x64" / "vec0",
    ]
    for p in possible_paths:
        if p.exists():
            return p
    return possible_paths[0]


def load_config() -> Dict:
    """从配置文件加载配置"""
    if LLM_CONFIG.exists():
        try:
            return json.loads(LLM_CONFIG.read_text())
        except:
            pass
    return {}


def get_embedding_config() -> tuple:
    """
    获取 Embedding 配置
    
    返回: (api_url, api_key, model, dimensions)
    """
    config = load_config()
    embedding_config = config.get("embedding", {})
    
    # 从配置文件读取，不使用硬编码默认值
    api_url = embedding_config.get("base_url", "")
    api_key = embedding_config.get("api_key", "") or os.environ.get("EMBEDDING_API_KEY", "")
    model = embedding_config.get("model", "")
    dimensions = embedding_config.get("dimensions", 1536)
    
    # 如果配置文件中没有，提示用户配置
    if not api_url or not api_key or not model:
        print("❌ Embedding 配置不完整")
        print(f"   配置文件: {LLM_CONFIG}")
        print("   需要配置: base_url, api_key, model")
        return None, None, None, None
    
    # 构建完整的 embeddings 端点
    if not api_url.endswith("/embeddings"):
        api_url = api_url.rstrip("/") + "/embeddings"
    
    return api_url, api_key, model, dimensions


def get_embedding(text: str) -> Optional[List[float]]:
    """获取向量"""
    api_url, api_key, model, dimensions = get_embedding_config()
    
    if not api_url or not api_key:
        return None
    
    data = json.dumps({
        "input": text[:2000],
        "model": model,
        "dimensions": dimensions
    }).encode('utf-8')
    
    req = urllib.request.Request(
        api_url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result['data'][0]['embedding']
    except Exception as e:
        print(f"API 错误: {e}")
        return None


def get_db_connection() -> sqlite3.Connection:
    """获取数据库连接"""
    conn = sqlite3.connect(str(VECTORS_DB))
    # 加载向量扩展
    try:
        conn.enable_load_extension(True)
        vec_ext = get_vec_extension_path()
        if vec_ext.exists():
            safe_load_extension(conn, vec_ext)
    except Exception as e:
        print(f"⚠️ 向量扩展加载失败: {e}")
    return conn


def get_missing_l0_records(batch_size: int = 50) -> List[Dict]:
    """获取缺失向量的 L0 记录（安全方式）"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT r.record_id, r.message_text, r.recorded_at 
            FROM l0_conversations r 
            WHERE NOT EXISTS (SELECT 1 FROM l0_vec v WHERE v.record_id = r.record_id) 
            LIMIT ?
        """, (batch_size,))
        
        records = []
        for row in cursor.fetchall():
            if row[0] and row[1]:
                records.append({
                    "record_id": row[0],
                    "message_text": row[1],
                    "recorded_at": row[2] if len(row) > 2 else ""
                })
        
        return records
    finally:
        conn.close()


def write_vector(record_id: str, embedding: List[float], recorded_at: str) -> bool:
    """写入向量（安全方式）"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        vec_bytes = struct.pack(f'{len(embedding)}f', *embedding)
        
        cursor.execute("DELETE FROM l0_vec WHERE record_id = ?", (record_id,))
        cursor.execute(
            "INSERT INTO l0_vec (record_id, embedding, recorded_at) VALUES (?, ?, ?)",
            (record_id, vec_bytes, recorded_at)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"写入错误: {e}")
        return False
    finally:
        conn.close()


def get_stats() -> tuple:
    """获取统计信息"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM l0_conversations")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM l0_vec")
        existing = cursor.fetchone()[0]
        
        return total, existing
    finally:
        conn.close()


def main():
    """主函数"""
    print("=" * 60)
    print("L0 向量补充（安全修复版）")
    print("=" * 60)
    
    # 检查配置
    api_url, api_key, model, dimensions = get_embedding_config()
    if not api_url:
        print("\n❌ 请先配置 Embedding API")
        print(f"配置文件: {LLM_CONFIG}")
        print("\n配置示例:")
        print(json.dumps({
            "embedding": {
                "base_url": "https://api.example.com/v1",
                "api_key": "your-api-key",
                "model": "text-embedding-3-small",
                "dimensions": 1536
            }
        }, indent=2))
        return
    
    print(f"\nEmbedding 配置:")
    print(f"  端点: {api_url}")
    print(f"  模型: {model}")
    print(f"  维度: {dimensions}")
    
    # 获取统计
    total, existing = get_stats()
    missing = total - existing
    
    print(f"\nL0 对话总数: {total}")
    print(f"已有向量: {existing}")
    print(f"缺失向量: {missing}")
    
    if missing == 0:
        print("\n✅ 所有 L0 对话都有向量")
        return
    
    print(f"\n开始补充向量（每批 50 条）...")
    
    total_fixed = 0
    batch_num = 0
    max_batches = 3  # 限制批次数
    
    while batch_num < max_batches:
        batch_num += 1
        print(f"\n--- 批次 {batch_num} ---")
        
        records = get_missing_l0_records(50)
        if not records:
            print("无更多记录")
            break
        
        print(f"获取到 {len(records)} 条记录")
        
        fixed = 0
        for i, record in enumerate(records):
            record_id_short = record['record_id'][:40] + "..." if len(record['record_id']) > 40 else record['record_id']
            print(f"  [{i+1}/{len(records)}] {record_id_short}", end=" ")
            
            embedding = get_embedding(record['message_text'])
            if embedding:
                if write_vector(record['record_id'], embedding, record['recorded_at']):
                    print("✅")
                    fixed += 1
                else:
                    print("❌ 写入失败")
            else:
                print("❌ 向量生成失败")
            
            time.sleep(0.3)
        
        total_fixed += fixed
        print(f"批次完成: {fixed}/{len(records)}")
    
    print(f"\n" + "=" * 60)
    print(f"补充完成: {total_fixed} 条向量")
    print(f"当前覆盖率: {100.0 * (existing + total_fixed) / total:.1f}%")
    print("=" * 60)


if __name__ == "__main__":
    main()
