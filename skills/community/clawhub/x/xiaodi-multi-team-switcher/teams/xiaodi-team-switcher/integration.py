#!/usr/bin/env python3
"""
团队切换器集成脚本
在 OpenClaw 会话中使用，根据用户意图自动切换团队
"""

import json
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from switch import TeamSwitcher


def get_team_prompt(team_id: str, switcher: TeamSwitcher) -> str:
    """获取团队的系统提示"""
    team_info = switcher.get_team_info(team_id)
    
    if not team_info:
        return ""
    
    prompt = f"""你现在已切换到 **{team_info.get('name', team_id)}** {team_info.get('icon', '')}

## 团队信息
- 名称: {team_info.get('name', '')}
- 描述: {team_info.get('description', '')}
- 可用角色: {', '.join(team_info.get('agents', []))}

## 使用方式
根据用户需求，选择合适的角色来处理任务。每个角色都有专业能力，协作完成任务。

"""
    return prompt


def process_user_input(user_input: str) -> dict:
    """
    处理用户输入，返回切换结果
    
    Args:
        user_input: 用户输入内容
    
    Returns:
        切换结果字典
    """
    switcher = TeamSwitcher()
    team_id, confidence, team_name = switcher.switch_team(user_input)
    
    result = {
        "input": user_input[:100],
        "switched": team_id is not None,
        "team_id": team_id,
        "team_name": team_name,
        "confidence": confidence,
        "prompt": ""
    }
    
    if team_id:
        result["prompt"] = get_team_prompt(team_id, switcher)
        result["agents"] = switcher.get_team_info(team_id).get("agents", [])
    
    return result


def interactive_mode():
    """交互模式"""
    print("=" * 50)
    print("🔄 小弟团队切换器 - 交互模式")
    print("=" * 50)
    print("\n输入你的需求，系统会自动识别并切换到合适的团队。")
    print("输入 'quit' 或 'exit' 退出。\n")
    
    switcher = TeamSwitcher()
    current_team = None
    
    while True:
        try:
            user_input = input("👤 你: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 再见！")
                break
            
            if not user_input:
                continue
            
            # 执行切换
            team_id, confidence, team_name = switcher.switch_team(user_input)
            
            if team_id:
                if current_team != team_id:
                    print(f"\n🔄 切换到: {switcher.get_team_info(team_id).get('icon', '')} {team_name}")
                    print(f"   置信度: {confidence:.2f}")
                    print(f"   可用角色: {', '.join(switcher.get_team_info(team_id).get('agents', []))}")
                    current_team = team_id
                print(f"\n🤖 {team_name} 已就绪，请继续描述你的需求。\n")
            else:
                print(f"\n❓ 无法确定目标团队 (置信度: {confidence:.2f})")
                print("   请尝试更明确地描述你的需求，或手动指定团队。")
                print("   可用团队: 金融, 电商, 多媒体, 办公\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break


def main():
    """主入口"""
    if len(sys.argv) < 2:
        # 交互模式
        interactive_mode()
        return
    
    if sys.argv[1] == "--list":
        # 列出团队
        switcher = TeamSwitcher()
        teams = switcher.list_teams()
        print(json.dumps(teams, ensure_ascii=False, indent=2))
        return
    
    if sys.argv[1] == "--json":
        # JSON 输出模式
        if len(sys.argv) < 3:
            print("用法: python integration.py --json <用户输入>")
            sys.exit(1)
        
        user_input = " ".join(sys.argv[2:])
        result = process_user_input(user_input)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    # 普通模式
    user_input = " ".join(sys.argv[1:])
    result = process_user_input(user_input)
    
    if result["switched"]:
        print(f"✅ 已切换到: {result['team_name']}")
        print(f"   置信度: {result['confidence']:.2f}")
        print(f"   可用角色: {', '.join(result.get('agents', []))}")
    else:
        print(f"❓ 无法确定目标团队 (置信度: {result['confidence']:.2f})")


if __name__ == "__main__":
    main()