import os
import argparse
from pathlib import Path

def synthesize_manifesto(name, mode, archetype=None):
    """
    Synthesize a STYLE_MANIFESTO.md for a persona.
    
    Args:
        name: Name of the persona
        mode: One of 'personal', 'legend', 'avatar'
        archetype: Optional archetype for avatar mode
    
    Modes:
        personal: For real people (requires knowledge_base.json)
        legend: For famous/historical figures
        avatar: For fictional characters
    """
    output_dir = Path(f"personas/{name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    manifesto_path = output_dir / "STYLE_MANIFESTO.md"
    
    print(f"Synthesizing manifesto for {name} in {mode} mode...")
    
    if mode == "personal":
        kb_path = output_dir / "knowledge_base.json"
        if not kb_path.exists():
            print(f"Error: knowledge_base.json not found for {name}. Run archivist first.")
            return False
    
    # This script triggers the agent to perform the synthesis.
    print(f"MANIFESTO_PENDING: Agent, please synthesize STYLE_MANIFESTO.md for {name} using {mode} mode.")
    if archetype:
        print(f"ARCHETYPE: {archetype}")
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Synthesize STYLE_MANIFESTO.md for a persona",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python synthesize.py --name "Tesla" --mode legend
  python synthesize.py --name "MyFriend" --mode personal
  python synthesize.py --name "Hero" --mode avatar --archetype "warrior-poet"
        """
    )
    parser.add_argument("--name", required=True, help="Name of the persona")
    parser.add_argument(
        "--mode", 
        choices=["personal", "legend", "avatar"], 
        required=True,
        help="Mode: personal (requires knowledge_base), legend (famous), avatar (fictional)"
    )
    parser.add_argument("--archetype", help="Archetype for avatar mode")
    
    args = parser.parse_args()
    
    success = synthesize_manifesto(args.name, args.mode, args.archetype)
    if not success:
        exit(1)

if __name__ == "__main__":
    main()