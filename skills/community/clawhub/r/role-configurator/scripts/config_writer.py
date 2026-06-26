#!/usr/bin/env python3
"""
Config File Writer
- Generate SOUL.md config file
- Write to correct location
"""

import os

def get_soul_path():
    """Get SOUL.md file path"""
    workspace = os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace")
    return os.path.join(workspace, "SOUL.md")

def generate_soul_content(role_name, role_position, core_tasks, communication_style):
    """Generate SOUL.md content"""
    content = f"""# SOUL.md - {role_name}

## Role
{role_position}

## Core Tasks
{core_tasks}

## Communication Style
{communication_style}
"""
    return content

def write_soul_file(content):
    """Write SOUL.md file"""
    soul_path = get_soul_path()
    
    # Backup existing file if exists
    if os.path.exists(soul_path):
        backup_path = soul_path + ".backup"
        os.rename(soul_path, backup_path)
        print(f"Backed up existing config to: {backup_path}")
    
    # Write new file
    with open(soul_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Config written to: {soul_path}")
    return soul_path

def apply_template(template):
    """Apply role template"""
    content = template["soul_content"]
    return write_soul_file(content)

if __name__ == "__main__":
    # Test code
    test_content = generate_soul_content(
        "Test Assistant",
        "A test role",
        "- Test task 1\n- Test task 2",
        "Friendly and professional"
    )
    print("Generated config content:")
    print(test_content)
