#!/usr/bin/env python3
import os
import json
import sys
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Search the RA-Skills Registry.")
    parser.add_argument("query", nargs="?", default=None, help="Search keyword")
    parser.add_argument("-s", "--source", help="Filter by source (built-in, optional, ClawHub, skills.sh, etc.)")
    parser.add_argument("-c", "--category", help="Filter by category (apple, ai-agents, productivity, software-dev, etc.)")
    parser.add_argument("-l", "--limit", type=int, default=10, help="Max results to display")
    return parser.parse_args()

def main():
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(tools_dir)
    registry_path = os.path.join(root_dir, "registry.json")
    
    if not os.path.exists(registry_path):
        print(f"Error: Registry file not found at {registry_path}")
        sys.exit(1)
        
    with open(registry_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    skills = data.get("skills", [])
    args = get_args()
    
    query = args.query
    if query is None and not args.source and not args.category:
        print("=== RA-Skills Registry Interactive Search ===")
        print(f"Total skills available: {data.get('total', len(skills))}")
        print("  - Built-in: " + str(data.get("built_in", 0)))
        print("  - Optional: " + str(data.get("optional", 0)))
        print("  - Community: " + str(data.get("community", 0)))
        print("-" * 50)
        query = input("Enter search query (or leave empty to list all): ").strip()
        
    filtered = []
    for s in skills:
        # Filter by source
        if args.source and s.get("source", "").lower() != args.source.lower():
            continue
        # Filter by category
        if args.category and s.get("category", "").lower() != args.category.lower():
            continue
            
        # Search query matching
        if query:
            q = query.lower()
            in_name = q in s.get("name", "").lower() or q in s.get("identifier", "").lower()
            in_desc = q in s.get("description", "").lower()
            in_tags = any(q in t.lower() for t in s.get("tags", []))
            if not (in_name or in_desc or in_tags):
                continue
                
        filtered.append(s)
        
    print(f"\nFound {len(filtered)} matching skills (showing top {min(len(filtered), args.limit)}):\n")
    
    for i, s in enumerate(filtered[:args.limit]):
        print(f"{i+1}. \033[1m{s.get('name')}\033[0m")
        print(f"   Identifier:  {s.get('identifier')}")
        print(f"   Description: {s.get('description', 'No description.')}")
        print(f"   Source:      \033[36m{s.get('source')}\033[0m  |  Category: \033[35m{s.get('category')}\033[0m")
        print(f"   Command:     \033[33m{s.get('installCmd')}\033[0m")
        print(f"   Source URL:  {s.get('sourceUrl')}")
        print("-" * 50)

if __name__ == "__main__":
    main()
