import os
import yaml
import json
import re

SKILLS_DIR = "/home/ubuntu/skills"

def scan_skills():
    skills_data = []
    if not os.path.exists(SKILLS_DIR):
        return []
    
    for skill_name in os.listdir(SKILLS_DIR):
        skill_path = os.path.join(SKILLS_DIR, skill_name)
        skill_md_path = os.path.join(skill_path, "SKILL.md")
        
        if os.path.isdir(skill_path) and os.path.exists(skill_md_path):
            try:
                with open(skill_md_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract YAML frontmatter
                    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                    if match:
                        metadata = yaml.safe_load(match.group(1))
                        metadata['id'] = skill_name
                        # Basic capability mapping (heuristic)
                        desc = metadata.get('description', '').lower()
                        capabilities = {
                            "Data": 0, "Creative": 0, "Technical": 0, "Logic": 0, "Communication": 0
                        }
                        if any(w in desc for w in ['data', 'analyze', 'table', 'excel', 'csv']): capabilities["Data"] = 80
                        if any(w in desc for w in ['write', 'create', 'design', 'video', 'image']): capabilities["Creative"] = 80
                        if any(w in desc for w in ['code', 'api', 'dev', 'script', 'technical']): capabilities["Technical"] = 80
                        if any(w in desc for w in ['logic', 'math', 'reason', 'workflow']): capabilities["Logic"] = 80
                        if any(w in desc for w in ['email', 'chat', 'hr', 'social']): capabilities["Communication"] = 80
                        
                        metadata['capabilities'] = capabilities
                        skills_data.append(metadata)
            except Exception as e:
                print(f"Error parsing {skill_name}: {e}")
    
    return skills_data

if __name__ == "__main__":
    data = scan_skills()
    print(json.dumps(data, indent=2, ensure_ascii=False))
