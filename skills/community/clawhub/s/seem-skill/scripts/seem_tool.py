#!/usr/bin/env python3
"""
SEEM Memory Tool for OpenClaw Agent

This script provides a simple interface for the agent to store and recall memories.

Usage:
    python seem_tool.py store "message text" --speaker user
    python seem_tool.py recall "query text" --top-k 3
    python seem_tool.py stats
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add skill root to path
script_dir = Path(__file__).parent.absolute()
skill_root = script_dir.parent  # SEEM directory
sys.path.insert(0, str(skill_root))

from SEEM import SEEMSkill, SEEMConfig


def get_config() -> SEEMConfig:
    """Load configuration from environment variables"""
    return SEEMConfig(
        llm_api_key=os.getenv("LLM_API_KEY", ""),
        llm_base_url=os.getenv("LLM_BASE_URL", "https://api.xiaomimimo.com/v1"),
        llm_model=os.getenv("LLM_MODEL", "mimo-v2-flash"),
        mm_encoder_api_key=os.getenv("MM_ENCODER_API_KEY", ""),
        mm_encoder_base_url=os.getenv("MM_ENCODER_BASE_URL", "https://api.siliconflow.cn/v1"),
        mm_encoder_model=os.getenv("MM_ENCODER_MODEL", "Qwen/Qwen3-Embedding-8B"),
        enable_integration=True,
        enable_fact_graph=True,
        enable_cache=True,
    )


def get_skill() -> SEEMSkill:
    """Initialize and return SEEM skill"""
    config = get_config()
    
    if not config.llm_api_key or not config.mm_encoder_api_key:
        raise ValueError("Missing API keys. Set LLM_API_KEY and MM_ENCODER_API_KEY.")
    
    return SEEMSkill(config)


def store_message(text: str, speaker: str = "user") -> dict:
    """Store a message to memory"""
    skill = get_skill()
    
    memory_id = skill.store({
        "text": text,
        "speaker": speaker,
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "success": True,
        "memory_id": memory_id,
        "speaker": speaker,
        "text_preview": text[:100]
    }


def recall_memories(query: str, top_k: int = 3) -> dict:
    """Recall relevant memories"""
    skill = get_skill()
    
    results = skill.recall({"text": query}, top_k=top_k)
    
    return {
        "success": True,
        "query": query,
        "count": len(results),
        "memories": results
    }


def get_stats() -> dict:
    """Get memory statistics"""
    skill = get_skill()
    stats = skill.get_stats()
    return {
        "success": True,
        **stats
    }


def main():
    parser = argparse.ArgumentParser(description="SEEM Memory Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command")
    
    # Store command
    store_parser = subparsers.add_parser("store", help="Store a message")
    store_parser.add_argument("text", type=str, help="Message text")
    store_parser.add_argument("--speaker", type=str, default="user", help="Speaker (user/assistant)")
    
    # Recall command
    recall_parser = subparsers.add_parser("recall", help="Recall memories")
    recall_parser.add_argument("query", type=str, help="Search query")
    recall_parser.add_argument("--top-k", type=int, default=3, help="Number of results")
    
    # Stats command
    subparsers.add_parser("stats", help="Show statistics")
    
    args = parser.parse_args()
    
    try:
        if args.command == "store":
            result = store_message(args.text, args.speaker)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
        elif args.command == "recall":
            result = recall_memories(args.query, args.top_k)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
        elif args.command == "stats":
            result = get_stats()
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
        else:
            parser.print_help()
            
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
