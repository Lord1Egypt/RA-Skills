import os
import sys
import shutil

# Security measure: Restrict operations to the current directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def _safe_write(filepath: str, content: str):
    """Internal helper to backup files before overwriting to prevent corruption."""
    abs_path = os.path.abspath(filepath)
    if not abs_path.startswith(BASE_DIR):
        raise SecurityError(f"Path traversal attempt detected. Operation denied to {abs_path}")
        
    backup_path = abs_path + ".bak"
    # Create backup if file exists to prevent dataloss on crash
    if os.path.exists(abs_path):
        shutil.copy2(abs_path, backup_path)
        
    with open(abs_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    return abs_path

class SecurityError(Exception):
    pass

def update_skill(new_content: str):
    """
    Action: Updates the SKILL.md file with new behavior/logic.
    Triggered during the 'Self-Rewrite' phase.
    """
    skill_path = os.path.join(BASE_DIR, 'SKILL.md')
    try:
        _safe_write(skill_path, new_content)
        print("Skill evolved successfully.")
    except Exception as e:
        print(f"Failed to update skill: {e}")

def patch_file(filepath: str, content: str):
    """
    Action: Applies an update to the system securely.
    Trigger: /patch command issued.
    """
    try:
        _safe_write(filepath, content)
        print(f"Patch applied safely to {filepath}")
    except SecurityError as se:
        print(f"Security Alert: {se}")
    except Exception as e:
        print(f"Failed to patch {filepath}: {e}")

def log_memory(entry: str):
    """
    Action: Logs mistakes or patch rationale.
    Trigger: Before any /patch, or after Failure Audit.
    """
    memory_path = os.path.join(BASE_DIR, 'MEMORY.md')
    try:
        with open(memory_path, 'a', encoding='utf-8') as f:
            f.write(f"\n- [LOG]: {entry}")
        print("Memory updated.")
    except Exception as e:
        print(f"Failed to log memory: {e}")

if __name__ == "__main__":
    print("Self-improving scripts ready. Run specific functions dynamically.")
