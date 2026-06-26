#!/usr/bin/env python3
"""
小弟团队切换器 - 核心切换逻辑
根据用户输入自动识别并切换到合适的功能团队
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# 配置路径
SKILL_DIR = Path(__file__).parent
CONFIG_FILE = SKILL_DIR / "config.json"


class TeamSwitcher:
    """团队切换器"""
    
    def __init__(self):
        self.config = self._load_config()
        self.teams = self.config.get("teams", {})
        self.settings = self.config.get("settings", {})
        self.current_team = None
        self.confidence_history = []
    
    def _load_config(self) -> dict:
        """加载配置文件"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"teams": {}, "settings": {}}
    
    def analyze_intent(self, user_input: str) -> Dict[str, float]:
        """
        分析用户意图，返回各团队置信度
        
        Args:
            user_input: 用户输入文本
            
        Returns:
            Dict[team_id, confidence]: 各团队置信度 (0-1)
        """
        scores = {}
        user_input_lower = user_input.lower()
        
        for team_id, team_config in self.teams.items():
            if team_config.get("status") != "available":
                scores[team_id] = 0.0
                continue
            
            score = 0.0
            keywords = team_config.get("keywords", {})
            
            # 强关键词 (权重 0.5)
            strong_matches = sum(1 for kw in keywords.get("strong", []) 
                                if kw.lower() in user_input_lower)
            score += min(strong_matches * 0.5, 1.0)
            
            # 中等关键词 (权重 0.2)
            medium_matches = sum(1 for kw in keywords.get("medium", []) 
                                if kw.lower() in user_input_lower)
            score += min(medium_matches * 0.2, 0.5)
            
            # 弱关键词 (权重 0.1)
            weak_matches = sum(1 for kw in keywords.get("weak", []) 
                              if kw.lower() in user_input_lower)
            score += min(weak_matches * 0.1, 0.2)
            
            scores[team_id] = min(score, 1.0)
        
        return scores
    
    def switch_team(self, user_input: str) -> Tuple[Optional[str], float, str]:
        """
        根据用户输入切换团队
        
        Args:
            user_input: 用户输入文本
            
        Returns:
            Tuple[team_id, confidence, team_name]: 目标团队ID、置信度、团队名称
        """
        # 1. 检查手动切换指令
        manual_switch = self._check_manual_switch(user_input)
        if manual_switch:
            team_id = manual_switch
            team_name = self.teams[team_id]["name"]
            self.current_team = team_id
            return team_id, 1.0, team_name
        
        # 2. 分析意图
        scores = self.analyze_intent(user_input)
        
        if not scores:
            return None, 0.0, ""
        
        # 3. 找到最高置信度
        best_team = max(scores, key=scores.get)
        best_score = scores[best_team]
        
        # 4. 检查是否达到阈值
        min_confidence = self.settings.get("min_confidence", 0.6)
        
        if best_score >= min_confidence:
            team_name = self.teams[best_team]["name"]
            self.current_team = best_team
            self.confidence_history.append({
                "input": user_input[:50],
                "team": best_team,
                "confidence": best_score
            })
            return best_team, best_score, team_name
        
        # 5. 置信度不足
        fallback = self.settings.get("fallback_action", "ask")
        if fallback == "ask":
            return None, best_score, ""
        else:
            # 使用默认团队
            default = self.settings.get("default_team", "financial")
            team_name = self.teams[default]["name"]
            self.current_team = default
            return default, best_score, team_name
    
    def _check_manual_switch(self, user_input: str) -> Optional[str]:
        """检查是否是手动切换指令"""
        user_input_lower = user_input.lower()
        
        # 切换指令模式
        patterns = [
            r"切换到(.{2,10})团队",
            r"用(.{2,10})团队",
            r"(.{2,10})团队处理",
            r"切换到\s*(金融|电商|多媒体|办公)",
            r"用\s*(金融|电商|多媒体|办公)",
        ]
        
        team_aliases = {
            "金融": "financial",
            "金融分析": "financial",
            "股票": "financial",
            "电商": "ecom",
            "选品": "ecom",
            "多媒体": "media",
            "视频": "media",
            "办公": "office",
            "秘书": "office",
        }
        
        for pattern in patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                keyword = match.group(1).strip()
                for alias, team_id in team_aliases.items():
                    if alias in keyword:
                        if self.teams.get(team_id, {}).get("status") == "available":
                            return team_id
        
        return None
    
    def get_team_info(self, team_id: str) -> dict:
        """获取团队信息"""
        return self.teams.get(team_id, {})
    
    def get_current_team(self) -> Optional[str]:
        """获取当前团队"""
        return self.current_team
    
    def list_teams(self) -> List[dict]:
        """列出所有可用团队"""
        result = []
        for team_id, team_config in self.teams.items():
            result.append({
                "id": team_id,
                "name": team_config.get("name", ""),
                "icon": team_config.get("icon", ""),
                "status": team_config.get("status", "unknown"),
                "description": team_config.get("description", ""),
                "agents": team_config.get("agents", [])
            })
        return result


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python switch.py <用户输入>")
        print("      python switch.py --list")
        sys.exit(1)
    
    switcher = TeamSwitcher()
    
    if sys.argv[1] == "--list":
        # 列出所有团队
        teams = switcher.list_teams()
        print("📊 可用团队:")
        for team in teams:
            status_icon = "✅" if team["status"] == "available" else "🔄"
            print(f"  {status_icon} {team['icon']} {team['name']} ({team['id']})")
            print(f"      {team['description']}")
        sys.exit(0)
    
    # 分析用户输入
    user_input = " ".join(sys.argv[1:])
    team_id, confidence, team_name = switcher.switch_team(user_input)
    
    if team_id:
        team_info = switcher.get_team_info(team_id)
        print(json.dumps({
            "success": True,
            "team_id": team_id,
            "team_name": team_name,
            "confidence": confidence,
            "icon": team_info.get("icon", ""),
            "agents": team_info.get("agents", [])
        }, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({
            "success": False,
            "confidence": confidence,
            "message": "无法确定目标团队，请明确指定"
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()