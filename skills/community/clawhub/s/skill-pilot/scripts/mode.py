# -*- coding: utf-8 -*-
"""
SkillPilot - 智能技能路由引擎
模式管理模块

支持全量模式和默认模式两种执行模式
"""

import os
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path


class ModeManager:
    """模式管理器"""
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file or os.path.expanduser(
            "~/.openclaw/workspace/skills/skill-pilot/config/mode_config.json"
        )
        
        # 当前模式
        self.current_mode = "default"  # default | full
        
        # 默认工具配置 (按类别)
        self.default_tools: Dict[str, str] = {
            "search": "multi-search-engine",
            "fetch": "web_fetch",
            "summarize": "summarize",
            "analyze": "tavily-search",
        }
        
        # 工具池 (按类别)
        self.tool_pools: Dict[str, List[str]] = {
            "search": ["multi-search-engine", "exa-web-search-free", "tavily-search"],
            "fetch": ["web_fetch", "scrapling-fetch"],
            "summarize": ["summarize"],
            "analyze": ["tavily-search", "exa-web-search-free"],
        }
        
        # 工具表现记录 (用于自动选择最优)
        self.tool_performance: Dict[str, Dict] = {}
        
        # 加载配置
        self.load_config()
    
    def load_config(self) -> bool:
        """加载模式配置"""
        if not os.path.exists(self.config_file):
            return False
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if 'default_tools' in config:
                self.default_tools.update(config['default_tools'])
            if 'tool_pools' in config:
                self.tool_pools.update(config['tool_pools'])
            if 'tool_performance' in config:
                self.tool_performance = config['tool_performance']
            if 'current_mode' in config:
                self.current_mode = config['current_mode']
            
            return True
        except Exception as e:
            print(f"加载模式配置失败：{e}")
            return False
    
    def save_config(self):
        """保存模式配置"""
        config = {
            'current_mode': self.current_mode,
            'default_tools': self.default_tools,
            'tool_pools': self.tool_pools,
            'tool_performance': self.tool_performance,
            'last_updated': datetime.now().isoformat(),
        }
        
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存模式配置失败：{e}")
            return False
    
    def set_mode(self, mode: str):
        """
        设置当前模式
        
        Args:
            mode: "default" | "full"
        """
        if mode not in ["default", "full"]:
            print(f"⚠️ 无效模式：{mode}，使用默认模式")
            mode = "default"
        
        self.current_mode = mode
        self.save_config()
        print(f"✓ 模式已切换：{mode}")
    
    def get_mode(self) -> str:
        """获取当前模式"""
        return self.current_mode
    
    def get_tools_for_task(self, category: str, mode: str = None) -> List[str]:
        """
        获取某类别任务的工具列表
        
        Args:
            category: 任务类别 (search/fetch/summarize/analyze)
            mode: 执行模式 (default/full)，None 表示使用当前模式
        
        Returns:
            工具列表
        """
        if mode is None:
            mode = self.current_mode
        
        # 获取工具池
        pool = self.tool_pools.get(category, [])
        
        if mode == "full":
            # 全量模式：返回所有工具
            return pool.copy()
        else:
            # 默认模式：只返回默认工具
            default = self.default_tools.get(category)
            if default and default in pool:
                return [default]
            elif pool:
                # 如果没有配置默认工具，返回工具池第一个
                return [pool[0]]
            else:
                return []
    
    def set_default_tool(self, category: str, tool_name: str):
        """
        设置某类别的默认工具
        
        Args:
            category: 任务类别
            tool_name: 工具名称
        """
        if category not in self.tool_pools:
            self.tool_pools[category] = []
        
        if tool_name not in self.tool_pools[category]:
            self.tool_pools[category].append(tool_name)
        
        self.default_tools[category] = tool_name
        self.save_config()
        print(f"✓ 已设置 {category} 类别默认工具：{tool_name}")
    
    def record_performance(self, category: str, tool_name: str, 
                          success: bool, response_time: float, 
                          quality_score: float = None):
        """
        记录工具表现
        
        Args:
            category: 任务类别
            tool_name: 工具名称
            success: 是否成功
            response_time: 响应时间 (ms)
            quality_score: 质量评分 (0-1)，可选
        """
        if tool_name not in self.tool_performance:
            self.tool_performance[tool_name] = {
                'category': category,
                'total_calls': 0,
                'success_count': 0,
                'total_response_time': 0,
                'total_quality_score': 0,
                'quality_count': 0,
                'last_used': None,
            }
        
        perf = self.tool_performance[tool_name]
        perf['total_calls'] += 1
        
        if success:
            perf['success_count'] += 1
        
        perf['total_response_time'] += response_time
        perf['last_used'] = datetime.now().isoformat()
        
        if quality_score is not None:
            perf['total_quality_score'] += quality_score
            perf['quality_count'] += 1
        
        self.save_config()
    
    def get_best_tool(self, category: str) -> Optional[str]:
        """
        获取某类别表现最好的工具
        
        评分规则:
        - 成功率 50%
        - 响应时间 30%
        - 质量评分 20%
        
        Args:
            category: 任务类别
        
        Returns:
            最优工具名称
        """
        pool = self.tool_pools.get(category, [])
        if not pool:
            return None
        
        if len(pool) == 1:
            return pool[0]
        
        # 计算每个工具的得分
        scores = []
        for tool in pool:
            if tool not in self.tool_performance:
                # 无历史数据，给中等分数
                scores.append((tool, 50.0))
                continue
            
            perf = self.tool_performance[tool]
            
            # 成功率 (0-100)
            success_rate = perf['success_count'] / max(1, perf['total_calls']) * 100
            
            # 响应时间得分 (越快越好，0-100)
            avg_time = perf['total_response_time'] / max(1, perf['total_calls'])
            time_score = max(0, 100 - avg_time / 100)  # 10 秒以上得 0 分
            
            # 质量得分 (0-100)
            if perf['quality_count'] > 0:
                quality_score = perf['total_quality_score'] / perf['quality_count'] * 100
            else:
                quality_score = 50  # 无数据给中等分数
            
            # 综合得分
            total_score = (
                success_rate * 0.5 +
                time_score * 0.3 +
                quality_score * 0.2
            )
            
            scores.append((tool, total_score))
        
        # 按得分排序
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return scores[0][0] if scores else None
    
    def auto_update_default(self, category: str):
        """
        自动更新某类别的默认工具为表现最好的
        
        Args:
            category: 任务类别
        """
        best_tool = self.get_best_tool(category)
        if best_tool and best_tool != self.default_tools.get(category):
            old_default = self.default_tools.get(category)
            self.set_default_tool(category, best_tool)
            print(f"✓ 自动更新 {category} 默认工具：{old_default} → {best_tool}")
            return True
        return False
    
    def compare_tools(self, category: str) -> List[Dict]:
        """
        比较某类别所有工具的表现
        
        Args:
            category: 任务类别
        
        Returns:
            工具表现列表 (按得分排序)
        """
        pool = self.tool_pools.get(category, [])
        results = []
        
        for tool in pool:
            if tool in self.tool_performance:
                perf = self.tool_performance[tool]
                success_rate = perf['success_count'] / max(1, perf['total_calls'])
                avg_time = perf['total_response_time'] / max(1, perf['total_calls'])
                avg_quality = (
                    perf['total_quality_score'] / perf['quality_count']
                    if perf['quality_count'] > 0 else None
                )
                
                results.append({
                    'tool': tool,
                    'total_calls': perf['total_calls'],
                    'success_rate': success_rate,
                    'avg_response_time': avg_time,
                    'avg_quality_score': avg_quality,
                    'last_used': perf['last_used'],
                })
            else:
                results.append({
                    'tool': tool,
                    'total_calls': 0,
                    'success_rate': None,
                    'avg_response_time': None,
                    'avg_quality_score': None,
                    'last_used': None,
                })
        
        # 按调用次数排序
        results.sort(key=lambda x: x['total_calls'], reverse=True)
        
        return results
    
    def get_status(self) -> Dict:
        """获取模式状态"""
        return {
            'current_mode': self.current_mode,
            'default_tools': self.default_tools,
            'tool_pools': {k: len(v) for k, v in self.tool_pools.items()},
            'tools_tracked': len(self.tool_performance),
        }
    
    def reset_to_defaults(self):
        """重置为默认配置"""
        self.default_tools = {
            "search": "multi-search-engine",
            "fetch": "web_fetch",
            "summarize": "summarize",
            "analyze": "tavily-search",
        }
        
        self.tool_pools = {
            "search": ["multi-search-engine", "exa-web-search-free", "tavily-search"],
            "fetch": ["web_fetch", "scrapling-fetch"],
            "summarize": ["summarize"],
            "analyze": ["tavily-search", "exa-web-search-free"],
        }
        
        self.tool_performance = {}
        self.current_mode = "default"
        
        self.save_config()
        print("✓ 已重置为默认配置")


# 单例
_mode_manager = None

def get_mode_manager() -> ModeManager:
    """获取模式管理器单例"""
    global _mode_manager
    if _mode_manager is None:
        _mode_manager = ModeManager()
    return _mode_manager


if __name__ == '__main__':
    # 命令行测试
    import sys
    
    manager = ModeManager()
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == 'set':
            mode = sys.argv[2] if len(sys.argv) > 2 else 'default'
            manager.set_mode(mode)
        
        elif action == 'get':
            print(f"当前模式：{manager.get_mode()}")
        
        elif action == 'status':
            status = manager.get_status()
            print("模式状态:")
            print(json.dumps(status, indent=2, ensure_ascii=False))
        
        elif action == 'tools':
            category = sys.argv[2] if len(sys.argv) > 2 else 'search'
            mode = sys.argv[3] if len(sys.argv) > 3 else None
            tools = manager.get_tools_for_task(category, mode)
            print(f"{category} 类别工具 ({mode or manager.current_mode}模式):")
            print(tools)
        
        elif action == 'set-default':
            category = sys.argv[2] if len(sys.argv) > 2 else 'search'
            tool = sys.argv[3] if len(sys.argv) > 3 else None
            if tool:
                manager.set_default_tool(category, tool)
            else:
                print("请指定工具名称")
        
        elif action == 'compare':
            category = sys.argv[2] if len(sys.argv) > 2 else 'search'
            results = manager.compare_tools(category)
            print(f"{category} 类别工具对比:")
            print(json.dumps(results, indent=2, ensure_ascii=False))
        
        elif action == 'best':
            category = sys.argv[2] if len(sys.argv) > 2 else 'search'
            best = manager.get_best_tool(category)
            print(f"{category} 类别最优工具：{best or '无数据'}")
        
        elif action == 'auto-update':
            category = sys.argv[2] if len(sys.argv) > 2 else 'search'
            manager.auto_update_default(category)
        
        elif action == 'reset':
            manager.reset_to_defaults()
        
        else:
            print("用法:")
            print("  python mode.py set [default|full]     - 设置模式")
            print("  python mode.py get                    - 获取当前模式")
            print("  python mode.py status                 - 查看状态")
            print("  python mode.py tools [category]       - 查看工具列表")
            print("  python mode.py set-default [cat] [tool] - 设置默认工具")
            print("  python mode.py compare [category]     - 对比工具表现")
            print("  python mode.py best [category]        - 获取最优工具")
            print("  python mode.py auto-update [category] - 自动更新默认工具")
            print("  python mode.py reset                  - 重置为默认配置")
    else:
        # 默认：显示状态
        print(f"当前模式：{manager.get_mode()}")
        status = manager.get_status()
        print("\n模式状态:")
        print(json.dumps(status, indent=2, ensure_ascii=False))
