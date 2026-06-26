#!/usr/bin/env python3
"""
Routing Configuration Generator for OpenClaw Multi-Agent Deployment

Generates OpenClaw routing configuration based on agent directory structure.
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime

def generate_routing_config(agents_dir, output_file=None):
    """Generate OpenClaw routing configuration."""
    
    agents_dir = Path(agents_dir)
    if not agents_dir.exists():
        print(f"Error: Agents directory not found: {agents_dir}")
        sys.exit(1)
    
    # Find agent directories
    agent_dirs = []
    for item in agents_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name != 'shared':
            agent_dirs.append(item.name)
    
    if not agent_dirs:
        print(f"Warning: No agent directories found in {agents_dir}")
        agent_dirs = ["coordinator", "research", "builder", "auditor", "personal"]
    
    # Base OpenClaw configuration template
    config = {
        "$schema": "https://openclaw.ai/schemas/config/v1.json",
        "version": "2026.2",
        "agents": {},
        "routing": {
            "defaultAgent": "coordinator",
            "rules": []
        },
        "workspaces": {},
        "channels": {
            "telegram": {
                "enabled": True,
                "target": "coordinator"
            }
        }
    }
    
    # Add health probes for 2026.3+
    config["healthCheck"] = {
        "enabled": True,
        "interval": 30,
        "timeout": 10,
        "unhealthyThreshold": 3,
        "healthyThreshold": 2
    }

    # Add each agent
    for agent in agent_dirs:
        agent_path = agents_dir / agent
        
        config["agents"][agent] = {
            "model": "openrouter/deepseek/deepseek-v3.2",
            "thinking": "low",
            "workspace": str(agent_path.absolute()),
            "skills": ["multi-agent-deployment"],
            "healthCheck": {
                "path": str((agent_path / "SOUL.md").absolute()),
                "interval": 30,
                "timeout": 10,
                "maxRetries": 3
            },
            "rateLimit": {
                "requestsPerMinute": 30,
                "concurrency": 5
            }
        }
        
        config["workspaces"][agent] = {
            "path": str((agent_path / "workspace").absolute()),
            "memory": str((agent_path / "memory").absolute())
        }
        
        # Add routing rules based on agent type
        if agent == "coordinator":
            config["routing"]["rules"].append({
                "match": {"text": ["help", "assist", "support"]},
                "target": agent,
                "priority": 10
            })
        elif agent == "research":
            config["routing"]["rules"].append({
                "match": {"text": ["research", "find", "search", "look up", "what is"]},
                "target": agent,
                "priority": 20
            })
        elif agent == "builder":
            config["routing"]["rules"].append({
                "match": {"text": ["build", "create", "write", "code", "script", "develop"]},
                "target": agent,
                "priority": 20
            })
        elif agent == "auditor":
            config["routing"]["rules"].append({
                "match": {"text": ["review", "check", "audit", "validate", "test"]},
                "target": agent,
                "priority": 20
            })
        elif agent == "personal":
            config["routing"]["rules"].append({
                "match": {"text": ["schedule", "remind", "calendar", "email", "message"]},
                "target": agent,
                "priority": 20
            })
    
    # Add fallback rule
    config["routing"]["rules"].append({
        "match": {"text": ["*"]},
        "target": "coordinator",
        "priority": 1
    })
    
    # Add shared memory configuration
    shared_dir = agents_dir / "shared"
    if shared_dir.exists():
        config["sharedMemory"] = {
            "path": str((shared_dir / "memory").absolute()),
            "syncInterval": 30,
            "maxSize": "100MB"
        }
    
    # Generate output
    config_json = json.dumps(config, indent=2, ensure_ascii=False)
    
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(config_json)
        print(f"Configuration written to: {output_path.absolute()}")
        
        # Also write a simplified version for quick reference
        simple_config = {
            "agents": list(config["agents"].keys()),
            "defaultAgent": config["routing"]["defaultAgent"],
            "ruleCount": len(config["routing"]["rules"]),
            "generated": datetime.now().isoformat()
        }
        
        simple_path = output_path.parent / f"{output_path.stem}_simple.json"
        simple_path.write_text(json.dumps(simple_config, indent=2))
        print(f"Simple reference written to: {simple_path.absolute()}")
    else:
        print(config_json)
    
    return config

def main():
    parser = argparse.ArgumentParser(description="Generate OpenClaw routing configuration")
    parser.add_argument("--input", required=True, help="Path to agents directory (created by agent_setup.py)")
    parser.add_argument("--output", help="Output file path (default: print to stdout)")
    
    args = parser.parse_args()
    
    try:
        config = generate_routing_config(args.input, args.output)
        
        if args.output:
            print("\nConfiguration Summary:")
            print(f"  Agents configured: {len(config['agents'])}")
            print(f"  Routing rules: {len(config['routing']['rules'])}")
            print(f"  Default agent: {config['routing']['defaultAgent']}")
            print(f"  Shared memory: {'Yes' if 'sharedMemory' in config else 'No'}")
            
            print("\nNext steps:")
            print(f"1. Copy the configuration to ~/.openclaw/config.json")
            print(f"2. Restart OpenClaw gateway: openclaw gateway restart")
            print(f"3. Test routing with: openclaw agents list")
            
    except Exception as e:
        print(f"Error generating configuration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()