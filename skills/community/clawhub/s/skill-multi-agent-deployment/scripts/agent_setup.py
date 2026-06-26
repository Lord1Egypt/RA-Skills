#!/usr/bin/env python3
"""
Agent Setup Script for OpenClaw Multi-Agent Deployment

Creates directory structure and template files for specialized agents.
Templates loaded from assets/templates/ — edit those files to change agent output.
"""

import os
import argparse
import sys
from pathlib import Path
from datetime import date

# Load templates from assets/templates/ directory
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATES_DIR = SKILL_DIR / "assets" / "templates"


def load_template(filename: str) -> str:
    """Load a template file from the assets/templates/ directory."""
    template_path = TEMPLATES_DIR / filename
    if not template_path.exists():
        print(f"Warning: Template not found: {template_path}, using fallback.")
        return f"# {filename} template missing — reinstall skill to fix.\n"
    return template_path.read_text(encoding="utf-8")


# Agent type configurations
AGENT_CONFIGS = {
    "coordinator": {
        "mission": "Route requests to appropriate specialist agents and ensure overall system coordination.",
        "responsibilities": [
            "Analyze incoming requests and determine appropriate agent",
            "Monitor agent availability and performance",
            "Resolve conflicts between agent actions",
            "Maintain system-wide coherence"
        ]
    },
    "research": {
        "mission": "Gather, analyze, and synthesize information from web sources and databases.",
        "responsibilities": [
            "Perform targeted web searches",
            "Extract key insights from research materials",
            "Validate information from multiple sources",
            "Present findings in actionable formats"
        ]
    },
    "builder": {
        "mission": "Create, modify, and test code, scripts, and technical artifacts.",
        "responsibilities": [
            "Write and review code in multiple languages",
            "Implement file operations and system commands",
            "Test functionality and debug issues",
            "Document technical decisions and implementations"
        ]
    },
    "auditor": {
        "mission": "Review outputs for quality, security, and compliance with standards.",
        "responsibilities": [
            "Check code for security vulnerabilities",
            "Validate data accuracy and consistency",
            "Ensure compliance with operational guidelines",
            "Provide constructive feedback for improvement"
        ]
    },
    "personal": {
        "mission": "Handle personal assistant tasks, scheduling, and communication.",
        "responsibilities": [
            "Manage calendars and reminders",
            "Handle email and message composition",
            "Coordinate personal workflows",
            "Provide timely notifications and updates"
        ]
    }
}

def create_agent_directory(agent_type, output_dir):
    """Create directory structure and template files for an agent."""
    agent_dir = Path(output_dir) / agent_type
    agent_dir.mkdir(parents=True, exist_ok=True)
    
    config = AGENT_CONFIGS.get(agent_type, AGENT_CONFIGS["coordinator"])
    
    # Load templates from assets/templates/
    soul_template = load_template("SOUL.md")
    agents_template = load_template("AGENTS.md")
    
    # Create SOUL.md with populated placeholders
    soul_content = soul_template.format(
        agent_name=agent_type.title(),
        agent_type=agent_type,
        mission=config["mission"],
        responsibility1=config["responsibilities"][0],
        responsibility2=config["responsibilities"][1],
        responsibility3=config["responsibilities"][2],
        responsibility4=config["responsibilities"][3],
        response_time_target="30",
        accuracy_target="95",
        error_rate_target="5",
        availability_target="99.9",
        version="1.0.0",
        created_date=date.today().isoformat(),
        last_updated_date=date.today().isoformat()
    )
    
    soul_file = agent_dir / "SOUL.md"
    soul_file.write_text(soul_content)
    
    # Create AGENTS.md with populated placeholders
    agents_content = agents_template.format(agent_name=agent_type.title())
    agents_file = agent_dir / "AGENTS.md"
    agents_file.write_text(agents_content)
    
    # Create workspace directory
    workspace_dir = agent_dir / "workspace"
    workspace_dir.mkdir(exist_ok=True)
    
    # Create memory directory
    memory_dir = agent_dir / "memory"
    memory_dir.mkdir(exist_ok=True)
    
    # Create skills directory  
    skills_dir = agent_dir / "skills"
    skills_dir.mkdir(exist_ok=True)
    
    print(f"Created agent: {agent_type}")
    print(f"  Directory: {agent_dir}")
    print(f"  Files: SOUL.md, AGENTS.md")
    print(f"  Subdirectories: workspace/, memory/, skills/")
    print(f"  Templates sourced from: {TEMPLATES_DIR}")
    
    return agent_dir

def main():
    parser = argparse.ArgumentParser(description="Create OpenClaw agent directory structure")
    parser.add_argument("--agents", required=True, help="Comma-separated list of agent types (coordinator,research,builder,auditor,personal)")
    parser.add_argument("--output", default="./agents", help="Output directory (default: ./agents)")
    
    args = parser.parse_args()
    
    agent_types = [agt.strip().lower() for agt in args.agents.split(",")]
    
    # Validate agent types
    for agent_type in agent_types:
        if agent_type not in AGENT_CONFIGS:
            print(f"Error: Unknown agent type '{agent_type}'")
            print(f"Valid types: {', '.join(AGENT_CONFIGS.keys())}")
            sys.exit(1)
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Creating multi-agent deployment structure in: {output_dir.absolute()}")
    print(f"Agents: {', '.join(agent_types)}")
    print("-" * 50)
    
    created_dirs = []
    for agent_type in agent_types:
        agent_dir = create_agent_directory(agent_type, output_dir)
        created_dirs.append(agent_dir)
        print()
    
    # Create shared directory
    shared_dir = output_dir / "shared"
    shared_dir.mkdir(exist_ok=True)
    (shared_dir / "memory").mkdir(exist_ok=True)
    (shared_dir / "events").mkdir(exist_ok=True)
    (shared_dir / "logs").mkdir(exist_ok=True)
    
    print(f"Created shared directory: {shared_dir}")
    print(f"  Subdirectories: memory/, events/, logs/")
    print()
    print("=" * 50)
    print("SETUP COMPLETE")
    print("=" * 50)
    print(f"Next steps:")
    print(f"1. Review agent configurations in {output_dir}/")
    print(f"2. Configure OpenClaw gateway for multi-agent support")
    print(f"3. Implement shared memory synchronization")
    print(f"4. Deploy to your preferred cloud platform")
    print()
    print("For detailed instructions, refer to the SKILL.md documentation.")

if __name__ == "__main__":
    main()