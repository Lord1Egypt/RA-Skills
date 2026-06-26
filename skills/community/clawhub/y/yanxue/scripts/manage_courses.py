import os
import json
import sys
from datetime import datetime

STORAGE_DIR = "/home/ubuntu/yanxue_courses"

def init_storage():
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

def save_course(name, content, metadata=None):
    init_storage()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.md"
    filepath = os.path.join(STORAGE_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        if metadata:
            f.write("---\n")
            f.write(json.dumps(metadata, ensure_ascii=False, indent=2))
            f.write("\n---\n\n")
        f.write(content)
    
    print(f"Course saved to: {filepath}")
    return filepath

def list_courses():
    init_storage()
    files = [f for f in os.listdir(STORAGE_DIR) if f.endswith('.md')]
    if not files:
        print("No courses found.")
        return []
    
    print("Available courses:")
    for f in files:
        print(f"- {f}")
    return files

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 manage_courses.py <action> [args...]")
        sys.exit(1)
    
    action = sys.argv[1]
    if action == "list":
        list_courses()
    elif action == "save":
        if len(sys.argv) < 4:
            print("Usage: python3 manage_courses.py save <name> <content_path>")
            sys.exit(1)
        name = sys.argv[2]
        content_path = sys.argv[3]
        with open(content_path, 'r', encoding='utf-8') as f:
            content = f.read()
        save_course(name, content)
