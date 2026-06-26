#!/usr/bin/env python3
"""
团队协作启动脚本
用于初始化一个新的团队协作项目
"""

import os
import json
from datetime import datetime

def create_project(project_name, project_type="general"):
    """创建项目目录结构"""
    
    base_dir = os.path.join(os.getcwd(), project_name)
    
    # 创建目录
    dirs = [
        "",
        "docs",
        "src",
        "tests",
        "assets"
    ]
    
    for d in dirs:
        path = os.path.join(base_dir, d)
        os.makedirs(path, exist_ok=True)
    
    # 创建项目信息文件
    project_info = {
        "name": project_name,
        "type": project_type,
        "created": datetime.now().isoformat(),
        "status": "需求分析",
        "team": {
            "product_manager": "Qwen-Plus",
            "developer": "GLM-5",
            "designer": "Qwen3.5-Plus",
            "tester": "DeepSeek-Coder",
            "reviewer": "Qwen-Max"
        },
        "phases": [
            {"name": "需求分析", "status": "进行中", "role": "product_manager"},
            {"name": "开发实现", "status": "待开始", "role": "developer"},
            {"name": "测试验收", "status": "待开始", "role": "tester"},
            {"name": "代码审查", "status": "待开始", "role": "reviewer"},
            {"name": "交付", "status": "待开始", "role": "all"}
        ]
    }
    
    with open(os.path.join(base_dir, "project.json"), "w", encoding="utf-8") as f:
        json.dump(project_info, f, ensure_ascii=False, indent=2)
    
    # 创建需求文档模板
    readme_content = f"""# {project_name}

## 项目状态
- 当前阶段：需求分析
- 当前角色：产品经理（Qwen-Plus）

## 需求分析（产品经理）

### 项目背景
[待填写]

### 核心需求
1. [待填写]
2. [待填写]

### 功能列表
| 功能 | 优先级 | 验收标准 |
|------|--------|----------|
| 功能1 | P0 | [待填写] |

---
*创建时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    
    with open(os.path.join(base_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"✅ 项目 '{project_name}' 创建成功！")
    print(f"📁 位置：{base_dir}")
    print(f"\n📋 下一步：")
    print(f"   1. 以【产品经理】身份开始需求分析")
    print(f"   2. 填写 README.md 中的需求部分")
    print(f"   3. 完成后切换到【程序员】开始开发")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python start-project.py <项目名称> [项目类型]")
        print("示例：python start-project.py my-app web")
        sys.exit(1)
    
    name = sys.argv[1]
    ptype = sys.argv[2] if len(sys.argv) > 2 else "general"
    
    create_project(name, ptype)