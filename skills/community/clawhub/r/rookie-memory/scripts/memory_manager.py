#!/usr/bin/env python3
"""
Memory Manager - 三级记忆管理系统
Three-Tier Memory Management System

Usage:
    python3 memory_manager.py init                    # 初始化记忆系统
    python3 memory_manager.py bootstrap              # 启动时加载记忆（L1→L2→L0）
    python3 memory_manager.py autosave               # 会话结束时自动保存记忆
    python3 memory_manager.py add --type short --content "内容"   # 添加短期记忆
    python3 memory_manager.py add --type medium --content "内容"  # 添加中期记忆
    python3 memory_manager.py add --type long --content "内容"   # 添加长期记忆
    python3 memory_manager.py search "查询内容"       # 搜索长期记忆
    python3 memory_manager.py summary                # 手动触发摘要
    python3 memory_manager.py status                 # 查看记忆状态
    python3 memory_manager.py window                  # 查看短期记忆窗口
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime
from pathlib import Path

# 从环境变量或配置文件获取 API 配置
ZHIYI_BASE_URL = os.environ.get('ZHIYI_BASE_URL', 'https://open.bigmodel.cn/api/paas/v4')
ZHIYI_API_KEY = os.environ.get('ZHIYI_API_KEY', '')  # 需要从 openclaw config 获取


def get_embedding(text: str) -> list:
    """
    调用 GLM embedding API 生成向量
    使用 embedding-3 模型
    """
    global ZHIYI_API_KEY
    
    # 尝试从 OpenClaw 配置获取 API Key
    if not ZHIYI_API_KEY:
        config_path = Path('/root/.openclaw/openclaw.json')
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
                # 从 zhiyi provider 获取 API key
                if 'auth' in config and 'profiles' in config['auth']:
                    for profile_name, profile in config['auth']['profiles'].items():
                        if 'zhiyi' in profile_name.lower() or profile.get('provider') == 'zhiyi':
                            ZHIYI_API_KEY = profile.get('apiKey', '')
                            break
                # 或者从 zhiyi provider 的 models 配置获取
                if not ZHIYI_API_KEY and 'models' in config and 'providers' in config['models']:
                    zhiyi_cfg = config['models']['providers'].get('zhiyi', {})
                    ZHIYI_API_KEY = zhiyi_cfg.get('apiKey', '')
    
    if not ZHIYI_API_KEY:
        print("✗ 无法获取 ZHIYI API Key")
        return None
    
    url = f"{ZHIYI_BASE_URL}/embeddings"
    headers = {
        "Authorization": f"Bearer {ZHIYI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "embedding-3",
        "input": text
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        if 'data' in result and len(result['data']) > 0:
            return result['data'][0]['embedding']
        else:
            print(f"✗ Embedding API 返回格式异常: {result}")
            return None
    except Exception as e:
        print(f"✗ 调用 embedding API 失败: {e}")
        return None

# 配置路径
WORKSPACE_DIR = Path(os.environ.get('WORKSPACE_DIR', '/root/.openclaw/workspace'))
MEMORY_DIR = WORKSPACE_DIR / 'memory'
CONFIG_FILE = MEMORY_DIR / 'config.yaml'
SLIDING_WINDOW_FILE = MEMORY_DIR / 'sliding-window.json'
SUMMARIES_DIR = MEMORY_DIR / 'summaries'
VECTOR_STORE_DIR = MEMORY_DIR / 'vector-store'
L1_DIR = MEMORY_DIR / 'l1'

# 默认配置
DEFAULT_CONFIG = {
    'memory': {
        'short_term': {
            'enabled': True,
            'window_size': 10,
            'max_tokens': 2000,
            'warning_threshold': 3000  # 压缩前提醒阈值
        },
        'medium_term': {
            'enabled': True,
            'summary_threshold': 4000,
            'summary_model': 'glm-4-flash'
        },
        'long_term': {
            'enabled': True,
            'backend': 'chromadb',
            'top_k': 3,
            'min_relevance': 0.7,
            'search_mode': 'hybrid'  # hybrid/keyword/semantic
        },
        'cleanup': {
            'enabled': True,
            'max_age_days': 90,  # 超过N天未检索的记忆
            'min_relevance': 0.6,  # 相关性阈值
            'duplicate_threshold': 0.95  # 相似度阈值（超过则视为重复）
        }
    }
}


def ensure_dirs():
    """确保必要的目录存在"""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    """加载配置文件"""
    config_json = CONFIG_FILE.with_suffix('.json')
    if config_json.exists():
        with open(config_json, 'r') as f:
            return json.load(f)
    return DEFAULT_CONFIG


def save_config(config: dict):
    """保存配置文件"""
    # 使用 JSON 而非 YAML，减少依赖
    config_json = CONFIG_FILE.with_suffix('.json')
    with open(config_json, 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"✓ 已保存配置: {config_json}")


def init_memory_system():
    """初始化记忆系统"""
    ensure_dirs()
    
    # 创建配置文件
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        print(f"✓ 已创建配置文件: {CONFIG_FILE}")
    
    # 创建短期记忆文件
    if not SLIDING_WINDOW_FILE.exists():
        with open(SLIDING_WINDOW_FILE, 'w') as f:
            json.dump({'messages': [], 'updated_at': datetime.now().isoformat()}, f, indent=2, ensure_ascii=False)
        print(f"✓ 已创建短期记忆: {SLIDING_WINDOW_FILE}")
    
    print(f"✓ 记忆系统初始化完成")
    print(f"  短期记忆: {SLIDING_WINDOW_FILE}")
    print(f"  中期记忆: {SUMMARIES_DIR}")
    print(f"  长期记忆: {VECTOR_STORE_DIR}")
    return True


def add_short_term_memory(content: str, metadata: dict = None):
    """添加短期记忆（滑动窗口）"""
    config = load_config()
    window_size = config['memory']['short_term']['window_size']
    
    with open(SLIDING_WINDOW_FILE, 'r') as f:
        data = json.load(f)
    
    messages = data.get('messages', [])
    
    # 添加新消息
    new_message = {
        'content': content,
        'timestamp': datetime.now().isoformat(),
        'metadata': metadata or {}
    }
    messages.append(new_message)
    
    # 滑动窗口：保持最近 N 条
    if len(messages) > window_size:
        messages = messages[-window_size:]
    
    data['messages'] = messages
    data['updated_at'] = datetime.now().isoformat()
    
    with open(SLIDING_WINDOW_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 已添加短期记忆，当前窗口: {len(messages)}/{window_size}")
    return True


def get_short_term_memory() -> list:
    """获取短期记忆"""
    if not SLIDING_WINDOW_FILE.exists():
        return []
    with open(SLIDING_WINDOW_FILE, 'r') as f:
        data = json.load(f)
    return data.get('messages', [])


def add_medium_term_memory(content: str, summary_type: str = 'auto'):
    """添加中期记忆（摘要）"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    summary_file = SUMMARIES_DIR / f'{date_str}.json'
    
    if summary_file.exists():
        with open(summary_file, 'r') as f:
            data = json.load(f)
    else:
        data = {'summaries': [], 'date': date_str}
    
    new_summary = {
        'content': content,
        'type': summary_type,
        'timestamp': datetime.now().isoformat()
    }
    data['summaries'].append(new_summary)
    
    with open(summary_file, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 已添加中期记忆: {summary_file}")
    return True


def get_medium_term_memory(days: int = 7) -> list:
    """获取中期记忆（最近 N 天）"""
    summaries = []
    cutoff = datetime.now().timestamp() - (days * 24 * 3600)
    
    for f in SUMMARIES_DIR.glob('*.json'):
        if f.stat().st_mtime > cutoff:
            with open(f, 'r') as fp:
                data = json.load(fp)
                summaries.extend(data.get('summaries', []))
    
    return summaries


def init_vector_store():
    """初始化向量存储"""
    try:
        import chromadb
        from chromadb.config import Settings
    except ImportError:
        print("✗ 需要安装 chromadb: pip install chromadb")
        return False
    
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
    
    # 创建或获取集合
    try:
        collection = client.get_collection("memory")
    except:
        collection = client.create_collection("memory", metadata={"description": "Long-term memory store"})
    
    return client, collection


def add_long_term_memory(content: str, metadata: dict = None, source: str = 'manual'):
    """
    添加长期记忆（向量存储）
    Args:
        content: 记忆内容
        metadata: 额外的元数据
        source: 来源标记（chat/summary/manual/autosave）
    """
    try:
        import chromadb
        from chromadb.config import Settings
    except ImportError:
        print("✗ 需要安装 chromadb: pip install chromadb")
        return False
    
    # 在 autosave 模式下检查是否已存在相似记忆
    if source == 'autosave':
        # 使用语义搜索检查是否已存在
        existing = semantic_search_long_term(content, top_k=1)
        if existing:
            similarity = 1.0 - existing[0].get('distance', 1.0)
            if similarity > 0.98:  # 98% 以上相似度视为重复
                print(f"⏭️  跳过重复记忆: {content[:50]}...")
                return True

    # 生成 embedding 向量
    embedding = get_embedding(content)
    if not embedding:
        print("✗ 无法生成 embedding，向量存储失败")
        return False

    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))

    try:
        collection = client.get_collection("memory")
    except:
        collection = client.create_collection("memory")
    
    # 生成 ID
    memory_id = f"mem_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    # 自动添加 source 和 timestamp
    full_metadata = metadata or {}
    full_metadata['source'] = source
    full_metadata['timestamp'] = datetime.now().isoformat()
    
    # 添加到向量库，使用真实的 embedding
    collection.add(
        documents=[content],
        ids=[memory_id],
        metadatas=[full_metadata],
        embeddings=[embedding]
    )
    
    print(f"✓ 已添加长期记忆: {memory_id} (source: {source})")
    return True


def keyword_search_long_term(query: str, top_k: int = 10) -> list:
    """
    关键词搜索长期记忆（在所有记忆中搜索）
    Args:
        query: 查询内容（关键词）
        top_k: 返回结果数量
    """
    try:
        import chromadb
    except ImportError:
        print("✗ 需要安装 chromadb: pip install chromadb")
        return []
    
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
    
    try:
        collection = client.get_collection("memory")
    except:
        return []
    
    # 获取所有记忆
    results = collection.get()
    
    if not results or not results.get('documents'):
        return []
    
    # 关键词匹配
    query_lower = query.lower()
    matched_memories = []
    
    for i, doc in enumerate(results['documents']):
        if query_lower in doc.lower():
            memory = {
                'content': doc,
                'id': results['ids'][i],
                'score': 1.0  # 关键词匹配得分为 1.0
            }
            if results.get('metadatas'):
                memory['metadata'] = results['metadatas'][i]
            matched_memories.append(memory)
    
    # 返回前 top_k 条
    return matched_memories[:top_k]


def hybrid_search_long_term(query: str, top_k: int = 5, candidate_multiplier: int = 3) -> list:
    """
    混合检索长期记忆（关键词 + 语义）
    流程：
    1. 关键词匹配，获取候选集（top_k * candidate_multiplier）
    2. 在候选集上进行语义检索
    3. 合并结果，去重，排序
    
    Args:
        query: 查询内容
        top_k: 返回结果数量
        candidate_multiplier: 候选集倍数（默认 3 倍）
    """
    config = load_config()
    min_relevance = config['memory']['long_term'].get('min_relevance', 0.7)
    
    # 步骤 1: 关键词匹配获取候选集
    candidate_size = top_k * candidate_multiplier
    keyword_results = keyword_search_long_term(query, top_k=candidate_size)
    
    if not keyword_results:
        # 如果没有关键词匹配结果，退回到纯语义检索
        return semantic_search_long_term(query, top_k)
    
    # 步骤 2: 在候选集上进行语义检索
    candidate_ids = [m['id'] for m in keyword_results]
    semantic_results = semantic_search_long_term(query, top_k=candidate_size, filter_ids=candidate_ids)
    
    # 步骤 3: 合并结果
    # 为每个记忆添加综合得分（关键词匹配 + 语义相似度）
    merged = {}
    
    # 关键词结果权重: 0.4
    for m in keyword_results:
        memory_id = m['id']
        if memory_id not in merged:
            merged[memory_id] = m.copy()
            merged[memory_id]['keyword_score'] = 1.0
            merged[memory_id]['semantic_score'] = 0.0
            merged[memory_id]['combined_score'] = 0.4
    
    # 语义结果权重: 0.6
    for m in semantic_results:
        memory_id = m['id']
        if memory_id in merged:
            merged[memory_id]['semantic_score'] = 1.0 - (m.get('distance', 1.0))
        else:
            merged[memory_id] = m.copy()
            merged[memory_id]['keyword_score'] = 0.0
            merged[memory_id]['semantic_score'] = 1.0 - (m.get('distance', 1.0))
        
        # 计算综合得分
        merged[memory_id]['combined_score'] = (
            merged[memory_id]['keyword_score'] * 0.4 +
            merged[memory_id]['semantic_score'] * 0.6
        )
    
    # 过滤低相关性结果
    filtered = {
        k: v for k, v in merged.items()
        if v['combined_score'] >= min_relevance
    }
    
    # 按综合得分排序
    sorted_memories = sorted(filtered.values(), key=lambda x: x['combined_score'], reverse=True)
    
    return sorted_memories[:top_k]


def semantic_search_long_term(query: str, top_k: int = 5, filter_ids: list = None) -> list:
    """
    纯语义检索长期记忆
    Args:
        query: 查询内容
        top_k: 返回结果数量
        filter_ids: 可选，只在指定 ID 范围内检索
    """
    try:
        import chromadb
    except ImportError:
        print("✗ 需要安装 chromadb: pip install chromadb")
        return []
    
    # 生成查询的 embedding
    query_embedding = get_embedding(query)
    if not query_embedding:
        print("✗ 无法生成查询 embedding，搜索失败")
        return []
    
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
    
    try:
        collection = client.get_collection("memory")
    except:
        return []
    
    # 使用 embedding 向量搜索
    if filter_ids:
        # 获取所有候选记忆
        candidate_results = collection.get(ids=filter_ids, include=['documents', 'metadatas', 'embeddings'])
        
        if not candidate_results or not candidate_results.get('documents'):
            return []
        
        # 手动计算每个候选记忆的相似度
        memories = []
        for i, doc in enumerate(candidate_results['documents']):
            doc_embedding = candidate_results['embeddings'][i]
            similarity = compute_cosine_similarity(query_embedding, doc_embedding)
            memories.append({
                'content': doc,
                'id': candidate_results['ids'][i],
                'distance': 1.0 - similarity  # distance = 1 - similarity
            })
        
        # 按相似度排序
        memories.sort(key=lambda x: x['distance'])
        
        # 返回前 top_k 个结果
        return memories[:top_k]
    else:
        # 无需过滤，直接使用 ChromaDB 的语义搜索
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        memories = []
        if results and results.get('documents'):
            for i, doc in enumerate(results['documents'][0]):
                memory = {
                    'content': doc,
                    'id': results['ids'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                }
                # 添加元数据
                if results.get('metadatas'):
                    memory['metadata'] = results['metadatas'][0][i]
                memories.append(memory)
        
        return memories


def search_long_term_memory(query: str, top_k: int = 3, detect_conflicts: bool = True, mode: str = None) -> list:
    """
    搜索长期记忆
    Args:
        query: 查询内容
        top_k: 返回结果数量
        detect_conflicts: 是否检测冲突
        mode: 检索模式 (hybrid/keyword/semantic)，默认从配置读取
    """
    # 从配置获取默认模式
    if not mode:
        config = load_config()
        mode = config['memory']['long_term'].get('search_mode', 'hybrid')
    
    print(f"🔍 检索模式: {mode}")
    
    # 根据模式执行不同的检索策略
    if mode == 'keyword':
        memories = keyword_search_long_term(query, top_k)
    elif mode == 'semantic':
        memories = semantic_search_long_term(query, top_k)
    elif mode == 'hybrid':
        memories = hybrid_search_long_term(query, top_k)
    else:
        print(f"✗ 未知的检索模式: {mode}，使用默认混合检索")
        memories = hybrid_search_long_term(query, top_k)
    
    # 冲突检测：检查相似度极高但来源不同的记忆
    if detect_conflicts and len(memories) > 1:
        conflicts = []
        for i in range(len(memories)):
            for j in range(i + 1, len(memories)):
                score_i = memories[i].get('combined_score', memories[i].get('score', 1.0))
                score_j = memories[j].get('combined_score', memories[j].get('score', 1.0))
                # 如果得分非常接近（< 0.1），可能存在冲突
                if abs(score_i - score_j) < 0.1:
                    meta_i = memories[i].get('metadata', {})
                    meta_j = memories[j].get('metadata', {})
                    if meta_i.get('source') != meta_j.get('source'):
                        conflicts.append({
                            'i': i,
                            'j': j,
                            'reason': f"来源冲突: {meta_i.get('source')} vs {meta_j.get('source')}"
                        })
        
        if conflicts:
            print("\n⚠️ 检测到潜在冲突:")
            for conflict in conflicts:
                print(f"  • 冲突 {conflict['i']}: {conflict['reason']}")
    
    return memories


def search_short_term_memory(query: str) -> list:
    """搜索短期记忆"""
    messages = get_short_term_memory()
    results = []
    
    query_lower = query.lower()
    for i, msg in enumerate(messages):
        content = msg.get('content', '')
        if query_lower in content.lower():
            results.append({
                'content': content,
                'timestamp': msg.get('timestamp', ''),
                'index': i
            })
    
    return results


def search_medium_term_memory(query: str, days: int = 7) -> list:
    """搜索中期记忆"""
    summaries = get_medium_term_memory(days)
    results = []
    
    query_lower = query.lower()
    for i, summary in enumerate(summaries):
        content = summary.get('content', '')
        if query_lower in content.lower():
            results.append({
                'content': content,
                'timestamp': summary.get('timestamp', ''),
                'type': summary.get('type', 'auto')
            })
    
    return results


def search_l0_memory(query: str) -> list:
    """搜索 L0 永久记忆（文件系统）"""
    results = []
    
    l1_files = ['identity.md', 'technical-stack.md', 'key-decisions.md', 'working-directory.md']
    
    for filename in l1_files:
        file_path = L1_DIR / filename
        if not file_path.exists():
            continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 搜索关键词
        if query.lower() in content.lower():
            # 提取相关行
            lines = content.split('\n')
            relevant_lines = [
                (i + 1, line) for i, line in enumerate(lines)
                if query.lower() in line.lower()
            ]
            
            results.append({
                'filename': filename,
                'path': str(file_path),
                'matches': relevant_lines[:5]  # 只返回前5个匹配
            })
    
    return results


def generate_summary(messages: list) -> str:
    """
    生成摘要（调用 LLM）
    注意：这里需要接入实际的 LLM API
    """
    # TODO: 接入实际 LLM
    # 示例使用本地简单实现
    if not messages:
        return ""
    
    content_preview = "\n".join([m.get('content', '')[:100] for m in messages])
    summary = f"[自动摘要] {len(messages)} 条消息的总结。预览: {content_preview[:200]}..."
    
    return summary


def estimate_tokens(text: str) -> int:
    """估算文本的 token 数量（简单估算：中文约 1.5 字符/token，英文约 0.75 单词/token）"""
    # 检测是否有中文
    has_chinese = any('\u4e00' <= char <= '\u9fff' for char in text)
    
    if has_chinese:
        # 中文：约 1.5 字符/token
        return int(len(text) / 1.5)
    else:
        # 英文：约 0.75 单词/token（按空格分词）
        words = len(text.split())
        return int(words / 0.75)


def autosave():
    """
    会话结束时自动保存记忆
    1. 分析滑动窗口中的对话内容
    2. 生成摘要（如果 token 超过阈值）
    3. 将对话内容向量化存入 ChromaDB
    4. 更新 L1 的 key-decisions.md（如有新决策）
    5. 生成当日日志
    """
    print("\n=== 💾 自动保存记忆 ===\n")
    
    config = load_config()
    summary_threshold = config['memory']['medium_term']['summary_threshold']
    
    # 1. 读取滑动窗口
    short_memories = get_short_term_memory()
    
    if not short_memories:
        print("✓ 没有需要保存的短期记忆")
        return True
    
    print(f"📝 短期记忆: {len(short_memories)} 条")
    
    # 计算总 token 数
    total_text = "\n".join([m.get('content', '') for m in short_memories])
    total_tokens = estimate_tokens(total_text)
    
    print(f"   Token 估算: {total_tokens} (阈值: {summary_threshold})")
    
    saved_count = 0
    summary_generated = False
    
    # 2. 检查是否需要生成摘要
    if total_tokens >= summary_threshold:
        print(f"   → Token 超过阈值，生成摘要...")
        summary = generate_summary(short_memories)
        add_medium_term_memory(summary, 'autosave-summary')
        saved_count += 1
        summary_generated = True
        print(f"   ✓ 已生成摘要")
    else:
        print(f"   → Token 未超过阈值，跳过摘要")
    
    # 3. 将重要内容存入向量库
    print(f"\n🧠 存入长期记忆...")
    for i, msg in enumerate(short_memories):
        content = msg.get('content', '')
        if not content.strip():
            continue
        
        # 过滤掉太短的内容（< 10 字符）
        if len(content) < 10:
            continue
        
        metadata = {
            'index': i
        }
        
        # 合并原始 metadata
        if msg.get('metadata'):
            metadata.update(msg['metadata'])
        
        if add_long_term_memory(content, metadata, source='autosave'):
            saved_count += 1
    
    print(f"   ✓ 已存入 {saved_count - (1 if summary_generated else 0)} 条长期记忆")
    
    # 4. 更新 L1 的 key-decisions.md（简单实现：检测包含"决定"、"决策"等关键词的消息）
    print(f"\n📋 更新关键决策...")
    l1_decisions_file = L1_DIR / 'key-decisions.md'
    
    # 确保 L1 目录存在
    L1_DIR.mkdir(parents=True, exist_ok=True)
    
    decision_keywords = ['决定', '决策', '选择', '确定', '计划']
    decisions_found = []
    
    for msg in short_memories:
        content = msg.get('content', '')
        for keyword in decision_keywords:
            if keyword in content:
                timestamp = msg.get('timestamp', '')
                decisions_found.append(f"- [{timestamp[:19]}] {content[:200]}...")
                break
    
    if decisions_found:
        # 读取现有内容
        existing_content = ""
        if l1_decisions_file.exists():
            with open(l1_decisions_file, 'r', encoding='utf-8') as f:
                existing_content = f.read().strip()
        
        # 添加新决策
        date_str = datetime.now().strftime('%Y-%m-%d')
        new_entry = f"\n\n## {date_str} (自动保存)\n\n"
        new_entry += "\n".join(decisions_found)
        
        with open(l1_decisions_file, 'a', encoding='utf-8') as f:
            f.write(new_entry)
        
        print(f"   ✓ 已更新 key-decisions.md (新增 {len(decisions_found)} 条)")
        saved_count += 1
    else:
        print(f"   ⚠ 未发现关键决策")
    
    # 5. 生成当日日志
    print(f"\n📄 生成当日日志...")
    date_str = datetime.now().strftime('%Y-%m-%d')
    log_file = MEMORY_DIR / f'{date_str}.log'
    
    log_entry = f"\n{'='*60}\n"
    log_entry += f"自动保存 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    log_entry += f"{'='*60}\n"
    log_entry += f"短期记忆: {len(short_memories)} 条\n"
    log_entry += f"Token 总计: {total_tokens}\n"
    if summary_generated:
        log_entry += f"摘要生成: 是\n"
    else:
        log_entry += f"摘要生成: 否 (未超过阈值)\n"
    log_entry += f"长期记忆: {saved_count - (1 if summary_generated else 0)} 条\n"
    if decisions_found:
        log_entry += f"关键决策: {len(decisions_found)} 条\n"
    log_entry += f"\n对话摘要:\n"
    log_entry += "\n".join([f"  • {m.get('content', '')[:100]}..." for m in short_memories[-5:]])
    log_entry += "\n"
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    print(f"   ✓ 已生成日志: {log_file}")
    
    # 6. 清空短期记忆（避免重复保存）
    with open(SLIDING_WINDOW_FILE, 'w') as f:
        json.dump({'messages': [], 'updated_at': datetime.now().isoformat()}, f, indent=2, ensure_ascii=False)
    print(f"\n🗑️ 已清空短期记忆窗口")

    # 输出保存摘要
    print(f"\n{'='*60}")
    print(f"✓ 自动保存完成")
    print(f"  短期记忆: {len(short_memories)} 条")
    print(f"  摘要生成: {'是' if summary_generated else '否'}")
    print(f"  长期记忆: {saved_count - (1 if summary_generated else 0)} 条")
    print(f"  关键决策: {len(decisions_found)} 条")
    print(f"  日志文件: {log_file}")
    print(f"{'='*60}\n")

    return True


def trigger_summary():
    """手动触发摘要"""
    config = load_config()
    
    if not config['memory']['medium_term']['enabled']:
        print("✗ 中期记忆未启用")
        return False
    
    # 获取短期记忆
    short_memories = get_short_term_memory()
    
    if not short_memories:
        print("没有需要摘要的短期记忆")
        return True
    
    # 生成摘要
    summary = generate_summary(short_memories)
    
    # 存储为中期记忆
    add_medium_term_memory(summary, 'auto-summary')
    
    # 清空短期记忆（可选）
    with open(SLIDING_WINDOW_FILE, 'w') as f:
        json.dump({'messages': [], 'updated_at': datetime.now().isoformat()}, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 摘要生成完成，已归档 {len(short_memories)} 条短期记忆")
    return True


def show_status():
    """显示记忆状态"""
    config = load_config()
    
    print("\n=== 记忆系统状态 ===\n")
    
    # 短期记忆
    short_memories = get_short_term_memory()
    window_size = config['memory']['short_term']['window_size']
    print(f"📝 短期记忆: {len(short_memories)}/{window_size} 条")
    if short_memories:
        latest = short_memories[-1]
        print(f"   最新: {latest.get('content', '')[:50]}...")
    
    # 中期记忆
    medium_memories = get_medium_term_memory()
    print(f"\n📋 中期记忆: {len(medium_memories)} 条 (最近7天)")
    
    # 长期记忆
    try:
        import chromadb
        client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
        collection = client.get_collection("memory")
        long_count = collection.count()
        print(f"\n🧠 长期记忆: {long_count} 条")
    except:
        print(f"\n🧠 长期记忆: 0 条")
    
    print()
    return True


def show_window():
    """显示短期记忆窗口"""
    messages = get_short_term_memory()
    
    if not messages:
        print("短期记忆为空")
        return True
    
    print(f"\n=== 短期记忆窗口 ({len(messages)} 条) ===\n")
    for i, msg in enumerate(messages):
        content = msg.get('content', '')
        timestamp = msg.get('timestamp', '')
        preview = content[:80] + '...' if len(content) > 80 else content
        print(f"{i+1}. [{timestamp[:19]}] {preview}")
    
    print()
    return True


def extract_decisions():
    """手动提取关键决策"""
    print("\n=== 📋 提取关键决策 ===\n")
    
    # 从短期记忆提取
    short_memories = get_short_term_memory()
    decision_keywords = ['决定', '决策', '选择', '确定', '计划']
    decisions_found = []
    
    for msg in short_memories:
        content = msg.get('content', '')
        for keyword in decision_keywords:
            if keyword in content:
                timestamp = msg.get('timestamp', '')
                decisions_found.append(f"- [{timestamp[:19]}] {content[:200]}...")
                break
    
    # 从长期记忆提取
    print("从长期记忆中搜索包含关键词的内容...")
    all_decisions = search_long_term_memory("决定 决策 选择 确定", top_k=10, detect_conflicts=False)
    
    if all_decisions:
        for memory in all_decisions:
            content = memory['content']
            metadata = memory.get('metadata', {})
            timestamp = metadata.get('timestamp', '')
            decisions_found.append(f"- [{timestamp[:19]}] {content[:200]}...")
    
    # 更新 key-decisions.md
    l1_decisions_file = L1_DIR / 'key-decisions.md'
    L1_DIR.mkdir(parents=True, exist_ok=True)
    
    if not decisions_found:
        print("✗ 未发现关键决策")
        return False
    
    # 读取现有内容
    existing_content = ""
    if l1_decisions_file.exists():
        with open(l1_decisions_file, 'r', encoding='utf-8') as f:
            existing_content = f.read().strip()
    
    # 添加新决策
    date_str = datetime.now().strftime('%Y-%m-%d')
    new_entry = f"\n\n## {date_str} (手动提取)\n\n"
    new_entry += "\n".join(decisions_found)
    
    with open(l1_decisions_file, 'a', encoding='utf-8') as f:
        f.write(new_entry)
    
    print(f"✓ 已更新 key-decisions.md (新增 {len(decisions_found)} 条)")
    print(f"  文件路径: {l1_decisions_file}")
    return True


def check_warning():
    """检查是否接近压缩阈值"""
    print("\n=== ⚠️ Token 预警检查 ===\n")
    
    config = load_config()
    warning_threshold = config['memory']['short_term'].get('warning_threshold', 3000)
    summary_threshold = config['memory']['medium_term']['summary_threshold']
    
    short_memories = get_short_term_memory()
    
    if not short_memories:
        print("✓ 短期记忆为空，无需预警")
        return True
    
    total_text = "\n".join([m.get('content', '') for m in short_memories])
    total_tokens = estimate_tokens(total_text)
    
    print(f"当前 Token 数: {total_tokens}")
    print(f"预警阈值: {warning_threshold}")
    print(f"摘要阈值: {summary_threshold}")
    
    if total_tokens >= summary_threshold:
        print(f"\n🔴 已超过摘要阈值！建议立即执行摘要")
        print(f"   运行: python3 scripts/memory_manager.py summary")
        return False
    elif total_tokens >= warning_threshold:
        remaining = summary_threshold - total_tokens
        print(f"\n🟡 接近摘要阈值！剩余 {remaining} tokens")
        print(f"   建议考虑生成摘要")
        return False
    else:
        remaining = warning_threshold - total_tokens
        print(f"\n✓ Token 数量安全，剩余 {remaining} tokens 到达预警阈值")
        return True


def show_daily_log():
    """显示当日工作日志"""
    print("\n=== 📄 当日工作日志 ===\n")
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    log_file = MEMORY_DIR / f'{date_str}.log'
    
    if not log_file.exists():
        print(f"✗ 当日日志不存在: {log_file}")
        return False
    
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(content)
    return True


def bootstrap_memory():
    """
    启动时按固定顺序加载记忆
    L0（预加载）: 读取 L1 的 4 个文件
    L1（短期）: 读取 sliding-window.json
    L2（中期）: 读取当日 summaries（如有）
    """
    print("\n=== 🚀 记忆启动加载 ===\n")
    
    total_files = 0
    total_memories = 0
    
    # L0: 加载 L1 永久记忆文件
    l1_files = ['identity.md', 'technical-stack.md', 'key-decisions.md', 'working-directory.md']
    l1_loaded = []
    
    print("📂 L0 永久记忆:")
    if L1_DIR.exists():
        for filename in l1_files:
            file_path = L1_DIR / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                l1_loaded.append({
                    'filename': filename,
                    'path': str(file_path),
                    'content': content
                })
                total_files += 1
                # 估算行数作为记忆条数
                lines = len([line for line in content.split('\n') if line.strip()])
                total_memories += lines
                print(f"  ✓ {filename} ({lines} 行)")
            else:
                print(f"  ✗ {filename} (不存在)")
    else:
        print(f"  ✗ L1 目录不存在: {L1_DIR}")
    
    if l1_loaded:
        print(f"\n  → 已加载 {len(l1_loaded)} 个文件")
    else:
        print(f"\n  ⚠ 未加载 L1 记忆文件")
    
    # L1: 加载短期记忆（滑动窗口）
    print(f"\n📝 L1 短期记忆:")
    short_memories = get_short_term_memory()
    if short_memories:
        print(f"  ✓ 滑动窗口 ({len(short_memories)} 条)")
        total_files += 1
        total_memories += len(short_memories)
        
        # 显示最新 3 条
        print(f"\n  最新 {min(3, len(short_memories))} 条:")
        for msg in short_memories[-3:]:
            content = msg.get('content', '')
            timestamp = msg.get('timestamp', '')
            preview = content[:60] + '...' if len(content) > 60 else content
            print(f"    [{timestamp[:19]}] {preview}")
    else:
        print(f"  ⚠ 滑动窗口为空")
    
    # L2: 加载中期记忆（当日 summaries）
    print(f"\n📋 L2 中期记忆:")
    date_str = datetime.now().strftime('%Y-%m-%d')
    summary_file = SUMMARIES_DIR / f'{date_str}.json'
    
    if summary_file.exists():
        with open(summary_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        summaries = data.get('summaries', [])
        if summaries:
            print(f"  ✓ 当日摘要 ({len(summaries)} 条)")
            total_files += 1
            total_memories += len(summaries)
            
            # 显示最新 2 条摘要
            print(f"\n  最新 {min(2, len(summaries))} 条:")
            for summary in summaries[-2:]:
                content = summary.get('content', '')
                preview = content[:60] + '...' if len(content) > 60 else content
                print(f"    • {preview}")
        else:
            print(f"  ⚠ 当日摘要为空")
    else:
        print(f"  ⚠ 当日摘要文件不存在")
    
    # 输出汇总
    print(f"\n{'='*40}")
    print(f"✓ 启动加载完成")
    print(f"  文件总数: {total_files}")
    print(f"  记忆条数: {total_memories}")
    print(f"{'='*40}\n")
    
    return True


def compute_cosine_similarity(embedding1: list, embedding2: list) -> float:
    """计算两个向量的余弦相似度"""
    import math
    
    if len(embedding1) != len(embedding2):
        return 0.0
    
    dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
    norm1 = math.sqrt(sum(a * a for a in embedding1))
    norm2 = math.sqrt(sum(b * b for b in embedding2))
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)


def analyze_health():
    """
    分析记忆库健康状态
    检查项：
    1. 记忆总数和分布
    2. 过时记忆（超过配置天数）
    3. 低相关性记忆
    4. 重复记忆（相似度超过阈值）
    """
    print("\n=== 🏥 记忆库健康分析 ===\n")
    
    config = load_config()
    cleanup_config = config.get('cleanup', {})
    max_age_days = cleanup_config.get('max_age_days', 90)
    min_relevance = cleanup_config.get('min_relevance', 0.6)
    duplicate_threshold = cleanup_config.get('duplicate_threshold', 0.95)
    
    try:
        import chromadb
        from datetime import timedelta
    except ImportError:
        print("✗ 需要安装 chromadb: pip install chromadb")
        return False
    
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
    
    try:
        collection = client.get_collection("memory")
    except:
        print("✗ 长期记忆集合不存在")
        return False
    
    # 获取所有记忆
    results = collection.get(include=['documents', 'metadatas', 'embeddings'])
    
    if not results or not results.get('documents'):
        print("✗ 长期记忆为空")
        return False
    
    total_count = len(results['documents'])
    print(f"📊 记忆总数: {total_count}")
    
    # 按来源统计
    source_stats = {}
    for metadata in results.get('metadatas', []):
        source = metadata.get('source', 'unknown')
        source_stats[source] = source_stats.get(source, 0) + 1
    
    print(f"\n📂 按来源分布:")
    for source, count in sorted(source_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {source}: {count} 条")
    
    # 检查过时记忆
    now = datetime.now()
    cutoff_date = now - timedelta(days=max_age_days)
    outdated_memories = []
    
    for i, metadata in enumerate(results.get('metadatas', [])):
        timestamp_str = metadata.get('timestamp', '')
        if timestamp_str:
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
                if timestamp < cutoff_date:
                    outdated_memories.append({
                        'id': results['ids'][i],
                        'content': results['documents'][i][:100],
                        'timestamp': timestamp_str
                    })
            except:
                pass
    
    print(f"\n📅 过时记忆 (超过 {max_age_days} 天): {len(outdated_memories)} 条")
    if outdated_memories:
        print(f"  最新 3 条:")
        for mem in outdated_memories[-3:]:
            print(f"    • [{mem['timestamp'][:19]}] {mem['content']}...")
    
    # 检查低相关性记忆（通过随机采样检查）
    print(f"\n⚠️  低相关性记忆检查:")
    sample_size = min(10, total_count)
    print(f"  随机采样 {sample_size} 条记忆进行相关性检查...")
    
    low_relevance_count = 0
    for i in range(min(sample_size, len(results['documents']))):
        doc = results['documents'][i]
        # 使用文档的前 50 个字符作为查询进行语义检索
        query = doc[:50] if len(doc) > 50 else doc
        search_results = semantic_search_long_term(query, top_k=5)
        
        # 如果第一条结果不是自己且相似度低于阈值，则标记为低相关性
        if search_results:
            first_result = search_results[0]
            if first_result['id'] != results['ids'][i]:
                similarity = 1.0 - first_result.get('distance', 1.0)
                if similarity < min_relevance:
                    low_relevance_count += 1
                    if low_relevance_count <= 3:
                        print(f"    • {doc[:50]}... (相似度: {similarity:.2f})")
    
    if low_relevance_count > 3:
        print(f"    ... 还有 {low_relevance_count - 3} 条")
    
    # 检查重复记忆
    print(f"\n🔄 重复记忆检查 (相似度 >= {duplicate_threshold}):")
    embeddings = results.get('embeddings', [])
    duplicate_pairs = []
    
    # 安全地检查 embeddings 是否存在且不为空（支持 list 和 numpy array）
    has_embeddings = hasattr(embeddings, '__len__') and len(embeddings) > 0
    if has_embeddings:
        # 两两比较（限制比较次数以避免性能问题）
        max_comparisons = 5000
        comparison_count = 0
        
        for i in range(min(100, len(embeddings))):  # 限制检查数量
            for j in range(i + 1, min(100, len(embeddings))):
                similarity = compute_cosine_similarity(embeddings[i], embeddings[j])
                if similarity >= duplicate_threshold:
                    duplicate_pairs.append({
                        'id1': results['ids'][i],
                        'id2': results['ids'][j],
                        'similarity': similarity,
                        'content1': results['documents'][i][:80],
                        'content2': results['documents'][j][:80]
                    })
                
                comparison_count += 1
                if comparison_count >= max_comparisons:
                    break
            if comparison_count >= max_comparisons:
                break
        
        print(f"  共比较 {comparison_count} 对，发现 {len(duplicate_pairs)} 对重复")
        
        if duplicate_pairs:
            print(f"  前 5 对:")
            for pair in duplicate_pairs[:5]:
                print(f"    • {pair['id1']} ↔ {pair['id2']} (相似度: {pair['similarity']:.3f})")
    else:
        print(f"  ⚠️ 无法获取 embedding 数据或数据类型不支持")
    
    # 生成健康评分
    health_score = 100
    health_score -= (len(outdated_memories) / total_count) * 20  # 过时记忆最多扣 20 分
    health_score -= (low_relevance_count / sample_size) * 15    # 低相关性最多扣 15 分
    health_score -= min((len(duplicate_pairs) / max(1, total_count)) * 100, 20)  # 重复记忆最多扣 20 分
    health_score = max(0, min(100, health_score))
    
    # 输出健康评级
    if health_score >= 90:
        rating = "优秀"
        emoji = "🟢"
    elif health_score >= 70:
        rating = "良好"
        emoji = "🟡"
    elif health_score >= 50:
        rating = "一般"
        emoji = "🟠"
    else:
        rating = "较差"
        emoji = "🔴"
    
    print(f"\n{'='*40}")
    print(f"🏥 健康评分: {health_score:.1f}/100")
    print(f"{emoji} 健康评级: {rating}")
    print(f"{'='*40}\n")
    
    return True


def cleanup_memory(dry_run: bool = False):
    """
    清理记忆库
    清理项：
    1. 过时记忆（超过配置天数）
    2. 重复记忆（保留最新的）
    
    Args:
        dry_run: 预览模式，不实际删除
    """
    mode = "预览" if dry_run else "清理"
    print(f"\n=== 🧹 记忆库{mode} ===\n")
    
    config = load_config()
    cleanup_config = config.get('cleanup', {})
    max_age_days = cleanup_config.get('max_age_days', 90)
    duplicate_threshold = cleanup_config.get('duplicate_threshold', 0.95)
    
    try:
        import chromadb
        from datetime import timedelta
    except ImportError:
        print("✗ 需要安装 chromadb: pip install chromadb")
        return False
    
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
    
    try:
        collection = client.get_collection("memory")
    except:
        print("✗ 长期记忆集合不存在")
        return False
    
    # 获取所有记忆
    results = collection.get(include=['documents', 'metadatas', 'embeddings'])
    
    if not results or not results.get('documents'):
        print("✗ 长期记忆为空")
        return False
    
    total_count = len(results['documents'])
    print(f"📊 当前记忆总数: {total_count}")
    
    ids_to_delete = []
    
    # 1. 检查过时记忆
    print(f"\n📅 检查过时记忆 (超过 {max_age_days} 天)...")
    now = datetime.now()
    cutoff_date = now - timedelta(days=max_age_days)
    outdated_ids = []
    
    for i, metadata in enumerate(results.get('metadatas', [])):
        timestamp_str = metadata.get('timestamp', '')
        if timestamp_str:
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
                if timestamp < cutoff_date:
                    outdated_ids.append(results['ids'][i])
            except:
                pass
    
    if outdated_ids:
        print(f"  发现 {len(outdated_ids)} 条过时记忆")
        ids_to_delete.extend(outdated_ids)
    else:
        print(f"  ✓ 未发现过时记忆")
    
    # 2. 检查重复记忆
    print(f"\n🔄 检查重复记忆 (相似度 >= {duplicate_threshold})...")
    embeddings = results.get('embeddings', [])
    duplicate_ids_to_delete = []
    
    # 安全地检查 embeddings 是否存在且不为空（支持 list 和 numpy array）
    has_embeddings = hasattr(embeddings, '__len__') and len(embeddings) > 0
    if has_embeddings:
        # 两两比较
        max_comparisons = 5000
        comparison_count = 0
        
        for i in range(len(embeddings)):
            if results['ids'][i] in ids_to_delete:
                continue  # Skip if already marked for deletion
            
            for j in range(i + 1, len(embeddings)):
                if results['ids'][j] in ids_to_delete:
                    continue  # Skip if already marked for deletion
                
                similarity = compute_cosine_similarity(embeddings[i], embeddings[j])
                if similarity >= duplicate_threshold:
                    # Delete the earlier one
                    timestamp_i = results['metadatas'][i].get('timestamp', '')
                    timestamp_j = results['metadatas'][j].get('timestamp', '')
                    
                    try:
                        dt_i = datetime.fromisoformat(timestamp_i) if timestamp_i else now
                        dt_j = datetime.fromisoformat(timestamp_j) if timestamp_j else now
                        
                        if dt_i < dt_j:
                            duplicate_ids_to_delete.append(results['ids'][i])
                        else:
                            duplicate_ids_to_delete.append(results['ids'][j])
                    except:
                        # Delete the one with smaller ID if timestamp parsing fails
                        if results['ids'][i] < results['ids'][j]:
                            duplicate_ids_to_delete.append(results['ids'][i])
                        else:
                            duplicate_ids_to_delete.append(results['ids'][j])
                
                comparison_count += 1
                if comparison_count >= max_comparisons:
                    break
            if comparison_count >= max_comparisons:
                break
        
        if duplicate_ids_to_delete:
            print(f"  发现 {len(duplicate_ids_to_delete)} 条重复记忆")
            ids_to_delete.extend(duplicate_ids_to_delete)
        else:
            print(f"  ✓ 未发现重复记忆")
    else:
        print(f"  ⚠️ 无法获取 embedding 数据或数据类型不支持")
    
    # 去重
    ids_to_delete = list(set(ids_to_delete))
    
    # 输出清理摘要
    print(f"\n{'='*40}")
    print(f"📋 清理摘要:")
    print(f"  过时记忆: {len(outdated_ids)} 条")
    print(f"  重复记忆: {len(duplicate_ids_to_delete)} 条")
    print(f"  总计删除: {len(ids_to_delete)} 条")
    print(f"  剩余记忆: {total_count - len(ids_to_delete)} 条")
    print(f"{'='*40}")
    
    if dry_run:
        print(f"\n⚠️  预览模式 - 未实际删除")
        print(f"   如需执行清理，运行: python3 scripts/memory_manager.py cleanup")
        return True
    
    # 执行删除
    if ids_to_delete:
        print(f"\n🗑️  正在删除 {len(ids_to_delete)} 条记忆...")
        try:
            collection.delete(ids=ids_to_delete)
            print(f"✓ 删除完成")
        except Exception as e:
            print(f"✗ 删除失败: {e}")
            return False
    else:
        print(f"\n✓ 无需删除")
    
    return True


def main():
    parser = argparse.ArgumentParser(description='Memory Manager - 三级记忆管理系统')
    parser.add_argument('command', choices=['init', 'bootstrap', 'autosave', 'add', 'search', 'summary', 'status', 'window', 'extract-decisions', 'check-warning', 'daily-log', 'analyze-health', 'cleanup'],
                        help='命令')
    parser.add_argument('--type', choices=['short', 'medium', 'long'], default='short',
                        help='记忆类型')
    parser.add_argument('--tier', choices=['short', 'medium', 'long'], default='long',
                        help='检索层级（仅用于 search）')
    parser.add_argument('--mode', choices=['hybrid', 'keyword', 'semantic'], default=None,
                        help='检索模式（仅用于 search）：hybrid(混合)/keyword(关键词)/semantic(语义)')
    parser.add_argument('--content', '-c', type=str,
                        help='记忆内容')
    parser.add_argument('--query', '-q', type=str,
                        help='搜索查询')
    parser.add_argument('--top-k', type=int, default=3,
                        help='返回结果数量')
    parser.add_argument('--days', type=int, default=7,
                        help='查询天数（中期记忆）')
    parser.add_argument('--dry-run', action='store_true',
                        help='预览模式（仅用于 cleanup）')
    
    args = parser.parse_args()
    
    ensure_dirs()
    
    if args.command == 'init':
        return init_memory_system()
    
    elif args.command == 'bootstrap':
        return bootstrap_memory()
    
    elif args.command == 'autosave':
        return autosave()
    
    elif args.command == 'add':
        if not args.content:
            print("✗ 需要指定 --content")
            return False
        
        if args.type == 'short':
            return add_short_term_memory(args.content)
        elif args.type == 'medium':
            return add_medium_term_memory(args.content)
        elif args.type == 'long':
            return add_long_term_memory(args.content)
    
    elif args.command == 'search':
        if not args.query:
            print("✗ 需要指定 --query")
            return False
        
        # 分层检索
        if args.tier == 'short':
            results = search_short_term_memory(args.query)
            tier_name = "L1 短期记忆"
        elif args.tier == 'medium':
            results = search_medium_term_memory(args.query, args.days)
            tier_name = "L2 中期记忆"
        elif args.tier == 'long':
            results = search_long_term_memory(args.query, args.top_k, mode=args.mode)
            tier_name = "L3 长期记忆"
        else:
            results = []
            tier_name = "未知层级"
        
        if not results:
            print(f"未找到相关 {tier_name}")
            return True
        
        print(f"\n=== {tier_name} 搜索结果 ({len(results)} 条) ===\n")
        for i, r in enumerate(results):
            # 显示得分信息
            if 'combined_score' in r:
                score_info = f" (综合得分: {r['combined_score']:.2f})"
            elif 'distance' in r and r['distance']:
                score_info = f" (相似度: {1-r['distance']:.2f})"
            elif 'score' in r:
                score_info = f" (得分: {r['score']:.2f})"
            else:
                score_info = ""
            
            print(f"{i+1}.{score_info}")
            if 'content' in r:
                print(f"   {r['content'][:200]}...")
            if 'timestamp' in r:
                print(f"   时间: {r['timestamp']}")
            if 'filename' in r:
                print(f"   文件: {r['filename']}")
                if 'matches' in r:
                    for line_num, line in r['matches']:
                        print(f"     行{line_num}: {line}")
            print()
        
        return True
    
    elif args.command == 'summary':
        return trigger_summary()
    
    elif args.command == 'status':
        return show_status()
    
    elif args.command == 'window':
        return show_window()
    
    elif args.command == 'extract-decisions':
        return extract_decisions()
    
    elif args.command == 'check-warning':
        return check_warning()
    
    elif args.command == 'daily-log':
        return show_daily_log()
    
    elif args.command == 'analyze-health':
        return analyze_health()
    
    elif args.command == 'cleanup':
        return cleanup_memory(dry_run=args.dry_run)
    
    return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
