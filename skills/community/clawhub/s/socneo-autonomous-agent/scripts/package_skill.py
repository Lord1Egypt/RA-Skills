#!/usr/bin/env python3
"""
Package Skill - Utilities
Author: Socneo
Created with Claude Code
Version: 1.0.0

Skill packaging for distribution.
"""

import zipfile
import os
from datetime import datetime

def package_skill():
    """Package the autonomous-agent skill."""

    skill_dir = "os.path.expanduser('~/.claude/skills/autonomous-agent')"
    output_file = "autonomous-agent.skill"

    print("Packaging autonomous-agent skill...")
    print(f"Source directory: {skill_dir}")
    print(f"Output file: {output_file}")

    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, skill_dir)
                print(f"  Adding: {arcname}")
                zipf.write(file_path, arcname)

    print(f"✅ Skill packaged successfully: {output_file}")

    # Create package manifest
    manifest = {
        "skill_name": "autonomous-agent",
        "version": "1.0.0",
        "description": "AI Autonomous Agent Framework with self-driven capabilities",
        "author": "AI Team",
        "created_at": datetime.now().isoformat(),
        "components": [
            "smart_heartbeat.py - Perception layer component",
            "task_decomposer.py - Execution layer component",
            "auto_reflection.py - Reflection layer component",
            "pattern_recognizer.py - Pattern recognition engine",
            "memory_system.py - Four-layer memory system",
            "self_correction.py - Self-correction mechanism"
        ],
        "features": [
            "Four-layer autonomous architecture",
            "Adaptive perception and monitoring",
            "Intelligent task decomposition",
            "Automated reflection and learning",
            "Pattern recognition and optimization",
            "Persistent memory system",
            "Self-correction and improvement"
        ]
    }

    # Save manifest
    import json
    with open("package_manifest.json", "w", encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("✅ Package manifest created")
    return output_file

if __name__ == "__main__":
    package_skill()
