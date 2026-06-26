#!/usr/bin/env python3
"""
TaskFlow 项目交互式修改工具

流程：
1. 读取 PROJECT.yaml
2. 展示当前配置
3. 用户提出修改
4. Agent 生成修改提案
5. 用户确认
6. 执行修改
"""
import json
import sys
from pathlib import Path

WORKSPACE = Path.home() / '.openclaw' / 'workspace'
PROJECTS_DIR = WORKSPACE / 'projects'


def load_project(project_id: str) -> dict:
    """加载项目"""
    project_file = PROJECTS_DIR / project_id / 'PROJECT.yaml'
    if not project_file.exists():
        return None
    with open(project_file, 'r') as f:
        return json.load(f)


def save_project(project_id: str, data: dict):
    """保存项目"""
    project_file = PROJECTS_DIR / project_id / 'PROJECT.yaml'
    with open(project_file, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def show_current(project_id: str):
    """展示当前配置"""
    data = load_project(project_id)
    if not data:
        print(f"✗ 项目不存在: {project_id}")
        return
    
    print(f"\n📁 当前项目配置: {project_id}")
    print("=" * 50)
    print(f"\n【元数据】")
    for k, v in data.get('meta', {}).items():
        print(f"  {k}: {v}")
    
    print(f"\n【描述】")
    print(data.get('description', '（无）'))
    print()


def interactive_edit(project_id: str):
    """交互式编辑"""
    data = load_project(project_id)
    if not data:
        print(f"✗ 项目不存在: {project_id}")
        return
    
    show_current(project_id)
    
    print("📝 请输入你的修改需求（自然语言描述）：")
    print("例如：'每天发8篇就行'、'增加午间时段'、'禁止写代码细节'等")
    print("输入 'quit' 退出\n")
    
    user_input = input("> ").strip()
    
    if user_input.lower() in ('quit', 'exit', 'q'):
        print("已退出")
        return
    
    # Agent 理解并生成提案
    print("\n🤖 我理解你的需求是：")
    print(f"  '{user_input}'")
    print("\n正在生成修改提案...\n")
    
    # 这里模拟 Agent 理解并生成提案
    # 实际应该用 LLM 分析用户输入
    proposal = generate_proposal(data, user_input)
    
    print("📋 修改提案：")
    print("=" * 50)
    print(proposal)
    print("=" * 50)
    
    # 用户确认
    confirm = input("\n确认修改？(yes/no/重新描述): ").strip().lower()
    
    if confirm == 'yes' or confirm == 'y':
        # 执行修改
        new_data = apply_proposal(data, user_input)
        save_project(project_id, new_data)
        print(f"\n✅ 已保存到 {project_id}/PROJECT.yaml")
        show_current(project_id)
    elif confirm == '重新描述':
        interactive_edit(project_id)
    else:
        print("已取消修改")


def generate_proposal(data: dict, user_input: str) -> str:
    """
    根据用户输入生成修改提案
    实际应该用 LLM，这里模拟
    """
    current_desc = data.get('description', '')
    
    # 模拟理解用户意图
    if '8' in user_input or '八' in user_input:
        # 修改数量
        old_count = "每天10篇左右（最少8篇，最多12篇）"
        new_count = "每天8篇左右（最少6篇，最多10篇）"
        
        return f"""
修改内容：
- 原：{old_count}
- 新：{new_count}

新的 description 将更新为：
...
- 每天8篇左右（最少6篇，最多10篇）
- ...
"""
    
    elif '午间' in user_input or '12点' in user_input:
        old_times = "8:00左右、12:00左右、20:00-24:00"
        
        return f"""
修改内容：
- 当前时段：{old_times}
- 你说"增加午间时段"，但当前已有 12:00左右
- 是否需要调整？比如改为：
  - 8:00左右
  - 12:00-13:00（扩展为时段）
  - 20:00-24:00
"""
    
    elif '代码' in user_input or '技术' in user_input:
        return """
修改内容：
在【内容要求】中增加：
- 禁止写代码片段、API调用、配置文件等技术细节
- 用通俗语言解释技术概念

示例：
  ❌ 不好："我用 Python 写了 requests.get() 调用"
  ✅ 更好："我查看了外部网站的信息"
"""
    
    else:
        return f"""
我理解你想修改：{user_input}

但我需要更明确的信息。请告诉我：
1. 具体要改什么约束？（数量/时段/字数/风格）
2. 改成什么样？

或者你可以直接编辑 description。
"""


def apply_proposal(data: dict, user_input: str) -> dict:
    """
    应用修改到数据
    实际应该用 LLM 生成完整 description
    """
    # 这里简化处理，实际应该解析用户意图并修改 description
    # 暂时只做简单替换示例
    
    if '8' in user_input:
        data['description'] = data['description'].replace(
            '每天10篇左右（最少8篇，最多12篇）',
            '每天8篇左右（最少6篇，最多10篇）'
        )
    
    return data


def main():
    if len(sys.argv) < 2:
        print("用法: edit-project.py <project-id>")
        print("示例: edit-project.py zsxq-rockman-blog")
        return
    
    project_id = sys.argv[1]
    interactive_edit(project_id)


if __name__ == "__main__":
    main()
