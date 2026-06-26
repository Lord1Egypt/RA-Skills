#!/usr/bin/env python3
"""
Self-Improving Agent - Main CLI Entry Point

A self-improving agent system for OpenClaw that learns from interactions
and continuously improves its performance.
"""

import argparse
import sys
from pathlib import Path

from src.agent import SelfImprovingAgent
from src.hooks import HookManager
from src.memory import LearningMemory


def main():
    """Main entry point for the self-improving-agent CLI."""
    parser = argparse.ArgumentParser(
        description='Self-Improving Agent - Continuous learning agent for OpenClaw'
    )
    
    parser.add_argument(
        'command',
        choices=['run', 'learn', 'review', 'export'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--workspace',
        type=str,
        default=Path.home() / '.openclaw' / 'workspace',
        help='Path to OpenClaw workspace'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Initialize components
    agent = SelfImprovingAgent(workspace=args.workspace)
    hooks = HookManager(workspace=args.workspace)
    memory = LearningMemory(workspace=args.workspace)
    
    # Execute command
    if args.command == 'run':
        run_agent(agent, hooks, memory, verbose=args.verbose)
    elif args.command == 'learn':
        learn_from_session(agent, memory, verbose=args.verbose)
    elif args.command == 'review':
        review_learnings(memory, verbose=args.verbose)
    elif args.command == 'export':
        export_learnings(memory, verbose=args.verbose)
    else:
        parser.print_help()
        sys.exit(1)


def run_agent(agent, hooks, memory, verbose=False):
    """Run the self-improving agent."""
    print("🧤 Starting Self-Improving Agent...")
    
    # Load learnings
    memory.load()
    
    # Apply hooks
    hooks.apply_all()
    
    # Run agent
    agent.run()
    
    print("✅ Agent completed successfully")


def learn_from_session(agent, memory, verbose=False):
    """Learn from the last session."""
    print("📚 Analyzing last session...")
    
    # Extract learnings
    learnings = agent.extract_learnings()
    
    # Store learnings
    memory.store(learnings)
    
    print(f"✅ Stored {len(learnings)} learnings")


def review_learnings(memory, verbose=False):
    """Review all stored learnings."""
    print("📖 Reviewing learnings...")
    
    learnings = memory.get_all()
    
    for i, learning in enumerate(learnings, 1):
        print(f"\n{i}. {learning['title']}")
        print(f"   Category: {learning['category']}")
        print(f"   Date: {learning['date']}")
        if verbose:
            print(f"   Content: {learning['content']}")
    
    print(f"\n✅ Total: {len(learnings)} learnings")


def export_learnings(memory, verbose=False):
    """Export learnings to a file."""
    print("📤 Exporting learnings...")
    
    output_file = Path.cwd() / 'learnings_export.md'
    memory.export(output_file)
    
    print(f"✅ Exported to {output_file}")


if __name__ == '__main__':
    main()
