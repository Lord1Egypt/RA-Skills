#!/usr/bin/env python3
"""
LLM Memory Integration - L3 长期画像更新脚本
使用 LLM_GLM5 提取长期特征，更新知识图谱和知识库
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 路径配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
ONTOLOGY_DIR = MEMORY_DIR / "ontology"
BRAIN_DIR = WORKSPACE / "brain"

def read_file(filepath):
    """读取文件内容"""
    if filepath.exists():
        return filepath.read_text(encoding="utf-8")
    return ""

def write_file(filepath, content):
    """写入文件"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")

def append_to_ontology(entity_type, entity_name, attributes):
    """追加实体到知识图谱"""
    graph_file = ONTOLOGY_DIR / "graph.jsonl"
    
    # 构建实体记录
    entity = {
        "type": entity_type,
        "name": entity_name,
        "attributes": attributes,
        "updated": datetime.now().isoformat()
    }
    
    # 追加到 JSONL 文件
    with open(graph_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entity, ensure_ascii=False) + "\n")
    
    print(f"✅ 已更新知识图谱: {entity_name}")

def create_brain_entry(category, title, content):
    """创建 2nd-brain 条目"""
    # 确定目录
    category_dir = BRAIN_DIR / category
    category_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{title.replace(' ', '_')}.md"
    filepath = category_dir / filename
    
    # 构建内容
    entry_content = f"""# {title}

**创建时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**分类**: {category}

---

{content}

---

*此条目由 LLM Memory Integration 自动生成*
"""
    
    write_file(filepath, entry_content)
    print(f"✅ 已创建知识库条目: {filepath}")

def main():
    """主函数"""
    if len(sys.argv) < 4:
        print("用法: python3 update_l3_profile.py <实体类型> <实体名称> <属性JSON>")
        print("示例: python3 update_l3_profile.py 'Preference' '回复风格' '{\"style\": \"简洁\", \"reason\": \"效率优先\"}'")
        sys.exit(1)
    
    entity_type = sys.argv[1]
    entity_name = sys.argv[2]
    attributes_json = sys.argv[3]
    
    try:
        attributes = json.loads(attributes_json)
    except json.JSONDecodeError:
        attributes = {"raw": attributes_json}
    
    # 更新知识图谱
    append_to_ontology(entity_type, entity_name, attributes)
    
    # 创建 2nd-brain 条目
    category = "preferences" if entity_type == "Preference" else "knowledge"
    create_brain_entry(category, entity_name, json.dumps(attributes, ensure_ascii=False, indent=2))
    
    print("L3 长期画像更新完成")

if __name__ == "__main__":
    main()
