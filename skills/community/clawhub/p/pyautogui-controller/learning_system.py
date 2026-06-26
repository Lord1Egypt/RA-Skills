#!/usr/bin/env python3
"""
学习系统 - 上下文记忆和自适应学习
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

@dataclass
class ExecutionRecord:
    record_id: str
    timestamp: float
    command: str
    intent_type: str
    success: bool
    duration: float
    steps_count: int
    failed_steps: List[str]
    notes: str = ""

@dataclass
class SiteConfig:
    site_id: str
    url_pattern: str
    first_seen: float
    last_used: float
    use_count: int
    element_positions: Dict[str, Dict[str, Any]]
    success_rate: float = 0.0

class LearningSystem:
    def __init__(self, workspace_path: str = None):
        if workspace_path is None:
            workspace_path = Path.home() / ".pyautogui-controller"
        
        self.workspace = Path(workspace_path)
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        self.history_file = self.workspace / "execution_history.json"
        self.sites_file = self.workspace / "site_configs.json"
        
        self.execution_history: List[ExecutionRecord] = []
        self.site_configs: Dict[str, SiteConfig] = {}
        
        self._load_data()
    
    def _load_data(self):
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.execution_history = [ExecutionRecord(**record) for record in data]
            except:
                pass
        
        if self.sites_file.exists():
            try:
                with open(self.sites_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.site_configs = {k: SiteConfig(**v) for k, v in data.items()}
            except:
                pass
    
    def _save_data(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(record) for record in self.execution_history], 
                     f, ensure_ascii=False, indent=2)
        
        with open(self.sites_file, 'w', encoding='utf-8') as f:
            json.dump({k: asdict(v) for k, v in self.site_configs.items()}, 
                     f, ensure_ascii=False, indent=2)
    
    def record_execution(self, command: str, intent_type: str, 
                        success: bool, duration: float,
                        steps_count: int, failed_steps: List[str]) -> str:
        record_id = f"exec_{int(time.time())}"
        
        record = ExecutionRecord(
            record_id=record_id,
            timestamp=time.time(),
            command=command,
            intent_type=intent_type,
            success=success,
            duration=duration,
            steps_count=steps_count,
            failed_steps=failed_steps
        )
        
        self.execution_history.append(record)
        
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]
        
        self._save_data()
        return record_id
    
    def learn_site(self, site_id: str, url_pattern: str, 
                   element_positions: Dict[str, Dict[str, Any]]):
        if site_id in self.site_configs:
            config = self.site_configs[site_id]
            config.last_used = time.time()
            config.use_count += 1
            config.element_positions.update(element_positions)
        else:
            config = SiteConfig(
                site_id=site_id,
                url_pattern=url_pattern,
                first_seen=time.time(),
                last_used=time.time(),
                use_count=1,
                element_positions=element_positions
            )
            self.site_configs[site_id] = config
        
        self._save_data()
    
    def get_site_config(self, url: str) -> Optional[SiteConfig]:
        for site_id, config in self.site_configs.items():
            if config.url_pattern in url:
                return config
        return None
    
    def get_execution_stats(self) -> Dict:
        if not self.execution_history:
            return {"total": 0, "success": 0, "failed": 0, "success_rate": 0.0}
        
        total = len(self.execution_history)
        success = sum(1 for r in self.execution_history if r.success)
        failed = total - success
        success_rate = success / total if total > 0 else 0.0
        
        return {
            "total": total,
            "success": success,
            "failed": failed,
            "success_rate": success_rate
        }


if __name__ == "__main__":
    print("学习系统测试")
    print("=" * 50)
    
    learning = LearningSystem()
    
    # 测试记录
    learning.record_execution(
        command="打开记事本",
        intent_type="open_program",
        success=True,
        duration=2.5,
        steps_count=3,
        failed_steps=[]
    )
    
    # 测试学习网站
    learning.learn_site(
        site_id="freegpt",
        url_pattern="freegpt.es",
        element_positions={
            "input_box": {"x": 960, "y": 980}
        }
    )
    
    # 显示统计
    stats = learning.get_execution_stats()
    print(f"执行统计: {stats}")
    
    # 获取网站配置
    config = learning.get_site_config("https://freegpt.es/#/chat")
    if config:
        print(f"网站配置: {config.site_id}, 使用次数: {config.use_count}")
    
    print("\n测试完成!")
