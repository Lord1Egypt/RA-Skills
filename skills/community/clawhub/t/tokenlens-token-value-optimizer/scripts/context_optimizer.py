#!/usr/bin/env python3
"""
TokenLens Context Optimizer
Simple rule-based context loading optimizer.
"""

import re
import sys
from typing import List, Dict, Set

def analyze_prompt(prompt: str) -> Dict[str, List[str]]:
    """
    Analyze prompt and recommend which files to load.
    Returns dict with 'load', 'optional', 'skip' lists.
    """
    prompt_lower = prompt.lower()
    
    # Always load these (identity/personality)
    always_load = ["SOUL.md", "IDENTITY.md"]
    
    # Files to consider loading based on triggers
    conditional_files = {
        "AGENTS.md": ["workflow", "process", "how do i", "remember", "what should", "agent"],
        "USER.md": ["user", "human", "owner", "about you", "who are you", "wing"],
        "TOOLS.md": ["tool", "camera", "ssh", "voice", "tts", "device", "exec", "run"],
        "MEMORY.md": ["remember", "recall", "history", "past", "before", "last time", "memory"],
        "HEARTBEAT.md": ["heartbeat", "check", "monitor", "alert", "status"],
    }
    
    # Skills that might be needed
    skill_triggers = {
        "github": ["github", "git", "repo", "repository", "pr", "issue"],
        "summarize": ["summarize", "summary", "brief", "tl;dr"],
        "web-browsing": ["browser", "web", "search", "url", "http"],
        "gog": ["google", "gmail", "calendar", "drive", "docs", "sheet"],
        "n8n-workflow-automation": ["workflow", "automation", "n8n", "trigger"],
    }
    
    # Determine which conditional files to load
    load_files = set(always_load)
    optional_files = set()
    
    for file_name, triggers in conditional_files.items():
        for trigger in triggers:
            if trigger in prompt_lower:
                load_files.add(file_name)
                break
    
    # Check for skill usage
    skill_files = []
    for skill, triggers in skill_triggers.items():
        for trigger in triggers:
            if trigger in prompt_lower:
                skill_files.append(f"skills/{skill}/SKILL.md")
                break
    
    # Simple conversation detection
    simple_phrases = ["hi", "hello", "hey", "thanks", "thank you", "ok", "yes", "no", "bye"]
    is_simple = any(phrase in prompt_lower for phrase in simple_phrases) or len(prompt_lower.split()) < 5
    
    if is_simple:
        # For simple conversations, only load identity files
        load_files = set(always_load)
        optional_files = set()
    
    # Files to skip (never load automatically)
    skip_files = [
        "docs/**/*.md",
        "memory/20*.md",  # Old daily logs
        "knowledge/**/*",
        "tasks/**/*",
    ]
    
    return {
        "load": sorted(list(load_files)),
        "optional": sorted(list(optional_files)),
        "skills": sorted(skill_files),
        "skip": skip_files,
        "is_simple": is_simple,
        "estimated_tokens_saved": estimate_savings(load_files, is_simple)
    }

def estimate_savings(load_files: Set[str], is_simple: bool) -> int:
    """
    Estimate token savings compared to loading everything.
    Very rough estimation.
    """
    # Typical token counts per file (approximate)
    file_token_estimates = {
        "SOUL.md": 500,
        "IDENTITY.md": 300,
        "AGENTS.md": 2000,
        "USER.md": 400,
        "TOOLS.md": 600,
        "MEMORY.md": 800,
        "HEARTBEAT.md": 200,
        "skills/*/SKILL.md": 1500,  # Average skill
    }
    
    # Estimate full load (worst case)
    full_load_tokens = sum(file_token_estimates.values()) + 10000  # + docs, knowledge, etc
    
    # Estimate optimized load
    optimized_tokens = 0
    for file in load_files:
        optimized_tokens += file_token_estimates.get(file, 500)
    
    if is_simple:
        optimized_tokens = file_token_estimates["SOUL.md"] + file_token_estimates["IDENTITY.md"]
    
    savings = full_load_tokens - optimized_tokens
    savings_percent = int((savings / full_load_tokens) * 100) if full_load_tokens > 0 else 0
    
    return {
        "optimized_tokens": optimized_tokens,
        "full_load_tokens": full_load_tokens,
        "tokens_saved": savings,
        "percent_saved": savings_percent
    }

def generate_agents_md_optimization() -> str:
    """Generate optimized AGENTS.md content snippet."""
    return """# AGENTS.md - Token-Optimized Workspace

## 🎯 Context Loading Strategy (OPTIMIZED)

**Default: Minimal context, load on-demand**

### Every Session (Always Load)
1. Read `SOUL.md` — Who you are (identity/personality)
2. Read `IDENTITY.md` — Your role/name

**Stop there.** Don't load anything else unless needed.

### Load On-Demand Only

**When user mentions memory/history:**
- Read `MEMORY.md`
- Read `memory/YYYY-MM-DD.md` (today only)

**When user asks about workflows/processes:**
- Read `AGENTS.md` (this file)

**When user asks about tools/devices:**
- Read `TOOLS.md`

**When user asks about themselves:**
- Read `USER.md`

## 🔥 Model Selection (Optimized)

**Simple conversations → Use cheapest model**
- Greetings, acknowledgments, simple questions
- Examples: "hi", "thanks", "yes", "no"

**Standard work → Use balanced model**
- Code writing, file edits, explanations
- Most common tasks

**Complex reasoning → Use powerful model**
- Architecture design, deep analysis
- Use sparingly
"""

def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="TokenLens Context Optimizer")
    parser.add_argument("prompt", nargs="?", help="User prompt to analyze")
    parser.add_argument("--generate-agents", action="store_true", help="Generate optimized AGENTS.md content")
    parser.add_argument("--recommend", action="store_true", help="Show file loading recommendations")
    
    args = parser.parse_args()
    
    if args.generate_agents:
        print(generate_agents_md_optimization())
    elif args.prompt:
        result = analyze_prompt(args.prompt)
        
        print("TokenLens Context Optimization")
        print("=" * 50)
        print(f"Prompt: {args.prompt}")
        print(f"Simple conversation: {result['is_simple']}")
        print()
        
        print("Recommended files to LOAD:")
        for file in result["load"]:
            print(f"  • {file}")
        
        if result["skills"]:
            print("\nSkills that might be needed:")
            for skill in result["skills"]:
                print(f"  • {skill}")
        
        print("\nFiles to SKIP:")
        for file in result["skip"][:5]:  # Show first 5
            print(f"  • {file}")
        
        print("\nToken Savings Estimate:")
        savings = result["estimated_tokens_saved"]
        print(f"  Optimized load: {savings['optimized_tokens']} tokens")
        print(f"  Full load: {savings['full_load_tokens']} tokens")
        print(f"  Tokens saved: {savings['tokens_saved']} tokens")
        print(f"  Savings: {savings['percent_saved']}%")
        
        print("\nRecommendation:")
        if result['is_simple']:
            print("  This is a simple conversation. Only load identity files.")
        else:
            print("  Load recommended files only. Skip documentation and old logs.")
    elif args.recommend and not args.prompt:
        print("Usage: context_optimizer.py '<prompt>' --recommend")
        print("Example: context_optimizer.py 'hi there' --recommend")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()