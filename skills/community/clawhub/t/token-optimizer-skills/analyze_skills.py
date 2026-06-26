import os
import sys
import glob
import re

def analyze_skills_directory(skills_dir: str):
    print(f"Analyzing skills in: {skills_dir}\n")
    
    sk_files = glob.glob(os.path.join(skills_dir, "*", "SKILL.md"))
    # Also check flat directory structure if openclaw dumps them directly
    sk_files.extend(glob.glob(os.path.join(skills_dir, "SKILL.md")))
    sk_files = list(set(sk_files))
    
    if not sk_files:
        print("No SKILL.md files found in this directory.")
        sys.exit(1)
    
    total_skills = len(sk_files)
    total_frontmatter_chars = 0
    bloated_skills = []
    
    for skill_file in sk_files:
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract YAML frontmatter block
        match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if match:
            frontmatter = match.group(1)
            char_len = len(frontmatter)
            total_frontmatter_chars += char_len

            # --- FIX: Parse 'name:' from frontmatter, fall back to folder name ---
            name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
            if name_match:
                skill_name = name_match.group(1).strip()
            else:
                skill_name = os.path.basename(os.path.dirname(skill_file))
            folder_name = os.path.basename(os.path.dirname(skill_file))

            # Heuristic: > 500 chars total frontmatter = bloated metadata
            if char_len > 500:
                bloated_skills.append((skill_name, folder_name, char_len))
                
    print("--- Skill Context Audit ---")
    print(f"Total Skills Analyzed: {total_skills}")
    
    # Precise estimate based on 4-chars-per-token heuristic
    est_total_tokens = total_frontmatter_chars // 4
    print(f"Estimated Token Cost of Loaded Skill Database: ~{est_total_tokens} tokens")
    
    if bloated_skills:
        print("\n🚨 Bloated Skills Detected (Metadata > 500 chars):")
        for skill_name, folder_name, size in sorted(bloated_skills, key=lambda x: x[2], reverse=True):
            label = skill_name
            if skill_name != folder_name:
                label = f"{skill_name}  (folder: {folder_name})"
            print(f"  - {label}: {size} chars (~{size//4} tokens)")
        print("\n💡 Recommendation: Edit the description in these SKILL.md files to be concise.")
        print("💡 Use Token Genome routing: only inject heavy SKILL descriptions when requested.")
    else:
        print("\n✅ Skill metadata footprint looks healthy.")

if __name__ == "__main__":
    # Robust path resolution for OpenClaw and VPS environments
    possible_paths = [
        os.environ.get("SKILLS_DIR"),
        os.path.join(os.getcwd(), "skills"),
        os.path.expanduser("~/.openclaw/skills"),
        os.path.expanduser("~/.gemini/antigravity/skills"),
        "/app/skills" # common docker container path
    ]
    
    target_dir = None
    for p in possible_paths:
        if p and os.path.isdir(p):
            target_dir = p
            break
            
    if target_dir:
        analyze_skills_directory(target_dir)
    else:
        print("Error: Could not locate skills directory.")
        print("Consider setting the SKILLS_DIR environment variable.")
        sys.exit(1)
