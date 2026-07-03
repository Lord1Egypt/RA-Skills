#!/usr/bin/env python3
"""
Signet Mind - Main CLI Interface
Mental health support companion with Signet AI integration.
"""

import sys
import argparse
from pathlib import Path
from database import initialize, save_conversation, get_conversation_history, save_mood_entry, get_mood_history
from wellness import get_wellness_tools
from signet import get_signet_connection


def main():
    parser = argparse.ArgumentParser(description="Signet Mind - Mental Health Companion")
    parser.add_argument("--init", action="store_true", help="Initialize databases")
    parser.add_argument("--chat", action="store_true", help="Start interactive chat")
    parser.add_argument("--checkin", action="store_true", help="Do a mood check-in")
    parser.add_argument("--exercise", type=str, help="Run a grounding exercise (5-4-3-2-1, box_breathing, body_scan, tensing)")
    parser.add_argument("--breathe", type=str, help="Run a breathing guide (calming, energizing, balanced)")
    parser.add_argument("--gratitude", action="store_true", help="Get a gratitude prompt")
    parser.add_argument("--history", type=int, metavar="N", help="Show last N conversations")
    parser.add_argument("--mood-history", type=int, metavar="N", help="Show mood history for last N days")
    parser.add_argument("--version", action="store_true", help="Show version")
    
    args = parser.parse_args()
    
    if args.version:
        print("Signet Mind v0.1.0")
        return
    
    if args.init:
        initialize()
        print("✓ Signet Mind initialized")
        print(f"  Data directory: ~/SignetMind/data/")
        print("  All conversations stored locally and encrypted.")
        return
    
    if args.chat:
        run_chat()
        return
    
    if args.checkin:
        run_checkin()
        return
    
    if args.exercise:
        run_exercise(args.exercise)
        return
    
    if args.breathe:
        run_breathing(args.breathe)
        return
    
    if args.gratitude:
        run_gratitude()
        return
    
    if args.history is not None:
        show_history(args.history)
        return
    
    if args.mood_history is not None:
        show_mood_history(args.mood_history)
        return
    
    # Default: show help
    parser.print_help()
    print("\nExamples:")
    print("  signet-mind --init              # Initialize for first run")
    print("  signet-mind --chat              # Start chatting")
    print("  signet-mind --checkin           # Do a mood check-in")
    print("  signet-mind --exercise box_breathing")
    print("  signet-mind --breathe calming   # Run calming breathing")
    print("  signet-mind --gratitude         # Get gratitude prompt")
    print("  signet-mind --history 10        # View last 10 conversations")


def run_chat():
    """Run interactive chat."""
    initialize()
    signet = get_signet_connection()
    wellness = get_wellness_tools()
    
    print("=" * 50)
    print("  Signet Mind")
    print("  Your mental health companion")
    print("=" * 50)
    print()
    print("Type 'help' for options, 'quit' to exit.")
    print()
    
    history = get_conversation_history(limit=10)
    
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye. Take care of yourself.")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Goodbye. I'm here when you need me.")
            break
        
        if user_input.lower() == "help":
            print_help()
            continue
        
        if user_input.lower() == "exercise":
            ex = wellness.get_grounding_exercise()
            print(wellness.format_grounding_exercise(ex))
            continue
        
        if user_input.lower() == "breathe":
            guide = wellness.get_breathing_guide()
            print(wellness.format_breathing_guide(guide))
            continue
        
        if user_input.lower() == "checkin":
            run_checkin()
            continue
        
        # Get response
        response = signet.get_personalized_response(user_input, history)
        
        # Save conversation
        save_conversation(user_input, response)
        
        # Update history
        history = get_conversation_history(limit=10)
        
        print(f"Signet Mind: {response}")
        print()


def print_help():
    print("""
Commands:
  exercise   - Do a grounding exercise
  breathe    - Run a breathing guide  
  checkin    - Do a mood check-in
  gratitude  - Get a gratitude prompt
  help       - Show this help
  quit       - Exit
""")


def run_checkin():
    """Run a mood check-in."""
    wellness = get_wellness_tools()
    
    print("\n--- Mood Check-In ---")
    print(wellness.get_checkin_prompt())
    print()
    
    # Show mood scale
    print("Mood scale (1-10):")
    for score, label in wellness.get_mood_scale():
        print(f"  {score}: {label}")
    print()
    
    # In interactive mode, this would capture user input
    # For CLI, just show the option
    print("To log your mood: signet-mind --checkin --mood 7")


def run_exercise(name: str):
    """Run a grounding exercise."""
    wellness = get_wellness_tools()
    
    valid_exercises = ["5-4-3-2-1", "box_breathing", "body_scan", "tensing"]
    
    if name not in valid_exercises:
        print(f"Unknown exercise: {name}")
        print(f"Available: {', '.join(valid_exercises)}")
        return
    
    exercise = wellness.get_grounding_exercise(name)
    print(wellness.format_grounding_exercise(exercise))


def run_breathing(name: str):
    """Run a breathing guide."""
    wellness = get_wellness_tools()
    
    valid_guides = ["calming", "energizing", "balanced"]
    
    if name not in valid_guides:
        print(f"Unknown guide: {name}")
        print(f"Available: {', '.join(valid_guides)}")
        return
    
    guide = wellness.get_breathing_guide(name)
    print(wellness.format_breathing_guide(guide))


def run_gratitude():
    """Show gratitude prompt."""
    wellness = get_wellness_tools()
    print(wellness.get_gratitude_prompt())


def show_history(n: int):
    """Show conversation history."""
    history = get_conversation_history(limit=n)
    
    if not history:
        print("No conversation history yet.")
        return
    
    print(f"\n--- Last {n} Conversations ---")
    for i, entry in enumerate(reversed(history), 1):
        print(f"\n[{entry['timestamp'][:19]}]")
        print(f"  You: {entry['user'][:100]}")
        print(f"  Me:  {entry['ai'][:100]}")


def show_mood_history(days: int):
    """Show mood history."""
    history = get_mood_history(days=days)
    
    if not history:
        print(f"No mood entries in the last {days} days.")
        return
    
    print(f"\n--- Mood History ({days} days) ---")
    for entry in reversed(history):
        print(f"{entry['date']}: {entry['mood']}/10 - {entry.get('notes', '')}")


if __name__ == "__main__":
    main()
