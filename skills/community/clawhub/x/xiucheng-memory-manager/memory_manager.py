#!/usr/bin/env python3
"""Memory Manager - Long-term memory management for OpenClaw agents.

Author: xiucheng
Version: 1.0.0
License: MIT
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any


class MemoryManager:
    """Manages long-term memory for OpenClaw agents."""
    
    def __init__(self, workspace: str = "/root/.openclaw/workspace"):
        """Initialize memory manager with workspace path.
        
        Args:
            workspace: Path to OpenClaw workspace
        """
        self.workspace = Path(workspace)
        self.memory_dir = self.workspace / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        self.memory_file = self.workspace / "MEMORY.md"
        
    def save_conversation(self, content: str, metadata: Optional[Dict] = None) -> str:
        """Save conversation to daily memory file.
        
        Args:
            content: Conversation content to save
            metadata: Optional metadata dict
            
        Returns:
            Path to saved file
        """
        today = datetime.now().strftime("%Y-%m-%d")
        daily_file = self.memory_dir / f"{today}.md"
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"\n## [{timestamp}]\n\n{content}\n"
        
        if metadata:
            entry += f"\n_Meta: {json.dumps(metadata, ensure_ascii=False)}_\n"
        
        with open(daily_file, "a", encoding="utf-8") as f:
            f.write(entry)
        
        return str(daily_file)
    
    def update_longterm(self, key_insights: str, category: str = "general") -> None:
        """Update long-term memory with key insights.
        
        Args:
            key_insights: Insights to save
            category: Category for organization
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if not self.memory_file.exists():
            with open(self.memory_file, "w", encoding="utf-8") as f:
                f.write("# MEMORY.md - Long-term Memory Archive\n\n")
        
        with open(self.memory_file, "a", encoding="utf-8") as f:
            f.write(f"\n## [{timestamp}] {category}\n\n")
            f.write(f"{key_insights}\n")
    
    def search_memory(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search memories using keyword matching.
        
        Args:
            query: Search query
            max_results: Maximum results to return
            
        Returns:
            List of matching memory entries
        """
        results = []
        query_lower = query.lower()
        
        # Search daily memory files
        for mem_file in sorted(self.memory_dir.glob("*.md"), reverse=True):
            try:
                with open(mem_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    if query_lower in content.lower():
                        # Extract relevant sections
                        sections = content.split("\n## ")
                        for section in sections[1:]:  # Skip header
                            if query_lower in section.lower():
                                results.append({
                                    "date": mem_file.stem,
                                    "content": section[:500] + "..." if len(section) > 500 else section,
                                    "file": str(mem_file)
                                })
                                if len(results) >= max_results:
                                    return results
            except Exception as e:
                print(f"Error reading {mem_file}: {e}")
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics.
        
        Returns:
            Dict with memory stats
        """
        daily_files = list(self.memory_dir.glob("*.md"))
        total_size = sum(f.stat().st_size for f in daily_files)
        
        return {
            "daily_files": len(daily_files),
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "memory_dir": str(self.memory_dir),
            "longterm_exists": self.memory_file.exists()
        }


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memory Manager CLI")
    parser.add_argument("--search", "-s", help="Search query")
    parser.add_argument("--save", help="Save content to memory")
    parser.add_argument("--stats", action="store_true", help="Show stats")
    
    args = parser.parse_args()
    
    mm = MemoryManager()
    
    if args.search:
        results = mm.search_memory(args.search)
        print(f"Found {len(results)} results:")
        for r in results:
            print(f"\n[{r['date']}] {r['content'][:200]}...")
    elif args.save:
        path = mm.save_conversation(args.save)
        print(f"Saved to: {path}")
    elif args.stats:
        stats = mm.get_stats()
        print(json.dumps(stats, indent=2))
    else:
        print("Memory Manager initialized successfully!")
        print(f"Stats: {mm.get_stats()}")


if __name__ == "__main__":
    main()
