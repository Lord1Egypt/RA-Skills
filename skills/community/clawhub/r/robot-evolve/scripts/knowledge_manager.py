#!/usr/bin/env python3
"""
robot-evolve 知识管理模块
从对话中提取知识，存入 ChromaDB 向量库
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

# Windows UTF-8兼容（仅在直接运行时生效，import时不执行）
if __name__ == "__main__" and sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 工作区路径
WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path(__file__).parent.parent.parent))
KNOWLEDGE_DIR = WORKSPACE / "knowledge"
CHROMA_DIR = KNOWLEDGE_DIR / "chroma_db"
LIBRARY_DIR = KNOWLEDGE_DIR / "library"
SESSION_STATE = WORKSPACE / "SESSION-STATE.md"

# ChromaDB 路径（延迟导入，未安装时优雅降级）
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

def get_chroma_client():
    """获取 ChromaDB 客户端（未安装时返回None）"""
    if not CHROMADB_AVAILABLE:
        return None
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.Client(Settings(
        persist_directory=str(CHROMA_DIR),
        anonymized_telemetry=False
    ))
    return client

def get_or_create_collection(client, name="skill_dev_knowledge"):
    """获取或创建 collection"""
    try:
        return client.get_collection(name=name)
    except:
        return client.create_collection(name=name)

def extract_knowledge_from_session():
    """从 SESSION-STATE.md 提取知识"""
    if not SESSION_STATE.exists():
        return []
    
    try:
        with open(SESSION_STATE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 简单的知识提取逻辑
        # 实际应该调用大模型 API，这里做基础解析
        knowledge_items = []
        
        # 检测"先生说了/先生决定/先生纠正"等模式
        lines = content.split("\n")
        for line in lines:
            if any(keyword in line for keyword in ["先生", "先生说了", "先生决定", "先生纠正"]):
                if len(line) > 10:
                    knowledge_items.append({
                        "content": line.strip(),
                        "topic": "对话记录",
                        "created_at": datetime.now().strftime("%Y-%m-%d"),
                        "version": "1"
                    })
        
        return knowledge_items[:10]  # 最多取10条
        
    except Exception as e:
        print(f"提取知识失败: {e}")
        return []

def check_duplicate(client, content):
    """检查是否重复"""
    collection = get_or_create_collection(client)
    try:
        results = collection.query(
            query_texts=[content],
            n_results=1
        )
        if results and results.get("documents") and results["documents"][0]:
            # 计算相似度
            if len(results["documents"][0]) > 0:
                # 简单判断：内容相似度超过80%视为重复
                if self_similarity(content, results["documents"][0]) > 0.8:
                    return True
    except:
        pass
    return False

def self_similarity(text1, text2):
    """简单相似度计算"""
    set1 = set(text1)
    set2 = set(text2)
    if not set1 or not set2:
        return 0
    return len(set1 & set2) / len(set1 | set2)

def add_knowledge(client, topic, content, version="1", supersedes=None):
    """添加知识到向量库"""
    collection = get_or_create_collection(client)
    
    metadata = {
        "topic": topic,
        "version": version,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "type": "knowledge_card"
    }
    if supersedes:
        metadata["supersedes"] = supersedes
    
    collection.add(
        documents=[content],
        metadatas=[metadata],
        ids=[f"kb_{datetime.now().strftime('%Y%m%d%H%M%S')}"]
    )
    
    # 同时保存到文件库
    LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    kb_file = LIBRARY_DIR / f"{datetime.now().strftime('%Y%m%d')}_{topic.replace(' ', '_')}.md"
    with open(kb_file, "w", encoding="utf-8") as f:
        f.write(f"# 知识卡片\n\n")
        f.write(f"- **主题**: {topic}\n")
        f.write(f"- **版本**: {version}\n")
        f.write(f"- **创建时间**: {metadata['created_at']}\n")
        if supersedes:
            f.write(f"- **取代**: {supersedes}\n")
        f.write(f"\n## 内容\n\n{content}\n")
    
    return kb_file

def generate_knowledge_cards():
    """生成知识卡片主函数"""
    results = []
    
    try:
        client = get_chroma_client()
        collection = get_or_create_collection(client)
        
        # 提取知识
        knowledge_items = extract_knowledge_from_session()
        
        if not knowledge_items:
            return ["ℹ️ 本次无可提取的新知识"]
        
        added = 0
        for item in knowledge_items:
            content = item.get("content", "")
            topic = item.get("topic", "未分类")
            
            # 检查重复
            if check_duplicate(client, content):
                continue
            
            # 添加知识
            kb_file = add_knowledge(
                client,
                topic=topic,
                content=content,
                version=item.get("version", "1")
            )
            added += 1
            results.append(f"✅ 已存入: {topic}")
        
        if added == 0:
            results.append("ℹ️ 没有新增知识（全部重复）")
        else:
            results.append(f"✅ 共新增 {added} 条知识")
            
    except ImportError:
        results.append("⚠️ ChromaDB 未安装，跳过知识卡片生成")
    except Exception as e:
        results.append(f"❌ 知识卡片生成失败: {e}")
    
    return results

if __name__ == "__main__":
    results = generate_knowledge_cards()
    for r in results:
        print(r)
