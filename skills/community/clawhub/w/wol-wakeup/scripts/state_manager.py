#!/usr/bin/env python3
"""
状态管理器 - 工作流引擎核心组件
负责会话状态的存储、检索和超时检查
"""

import json
import os
import time
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime

# 配置
STATE_DIR = Path.home() / ".openclaw" / "wol" / "workflows"
STATE_FILE = STATE_DIR / "sessions.json"
DEFAULT_TIMEOUT = 60  # 默认超时时间（秒）

@dataclass
class SessionState:
    """会话状态数据模型"""
    session_id: str          # 会话 ID（微信用户 ID）
    workflow_type: str       # 工作流类型（如 "add_device", "remove_device"）
    current_step: int        # 当前步骤索引
    step_data: Dict[str, Any]  # 已收集的步骤数据（如 MAC 地址、备注）
    created_at: float        # 创建时间戳
    updated_at: float        # 最后更新时间戳
    timeout_seconds: int     # 超时时间（秒）
    active: bool             # 是否激活
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SessionState':
        return cls(**data)


class StateManager:
    """状态管理器 - 单例模式"""
    
    _instance = None
    _states: Dict[str, SessionState] = {}
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._ensure_state_dir()
            self._load_states()
            self._initialized = True
    
    def _ensure_state_dir(self):
        """确保状态目录存在"""
        STATE_DIR.mkdir(parents=True, exist_ok=True)
    
    def _load_states(self):
        """从文件加载状态"""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._states = {
                        k: SessionState.from_dict(v) 
                        for k, v in data.items()
                    }
            except (json.JSONDecodeError, IOError):
                self._states = {}
        else:
            self._states = {}
    
    def _save_states(self):
        """保存状态到文件"""
        self._ensure_state_dir()
        data = {k: v.to_dict() for k, v in self._states.items()}
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def create_session(
        self,
        session_id: str,
        workflow_type: str,
        timeout_seconds: int = DEFAULT_TIMEOUT
    ) -> SessionState:
        """创建新会话"""
        # 清理已存在的会话（如果有）
        self.clear_session(session_id)
        
        now = time.time()
        state = SessionState(
            session_id=session_id,
            workflow_type=workflow_type,
            current_step=0,
            step_data={},
            created_at=now,
            updated_at=now,
            timeout_seconds=timeout_seconds,
            active=True
        )
        
        self._states[session_id] = state
        self._save_states()
        return state
    
    def get_session(self, session_id: str) -> Optional[SessionState]:
        """获取会话状态"""
        state = self._states.get(session_id)
        if not state or not state.active:
            return None
        
        # 检查超时
        if self._is_timeout(state):
            self.clear_session(session_id)
            return None
        
        return state
    
    def update_session(self, session_id: str, **kwargs) -> Optional[SessionState]:
        """更新会话状态"""
        state = self.get_session(session_id)
        if not state:
            return None
        
        # 更新字段
        for key, value in kwargs.items():
            if hasattr(state, key):
                setattr(state, key, value)
        
        state.updated_at = time.time()
        self._save_states()
        return state
    
    def advance_step(self, session_id: str, step_data: Dict[str, Any] = None) -> Optional[SessionState]:
        """推进到下一步"""
        state = self.get_session(session_id)
        if not state:
            return None
        
        state.current_step += 1
        if step_data:
            state.step_data.update(step_data)
        state.updated_at = time.time()
        
        self._save_states()
        return state
    
    def clear_session(self, session_id: str) -> bool:
        """清除会话"""
        if session_id in self._states:
            del self._states[session_id]
            self._save_states()
            return True
        return False
    
    def _is_timeout(self, state: SessionState) -> bool:
        """检查是否超时"""
        now = time.time()
        return (now - state.updated_at) > state.timeout_seconds
    
    def check_timeouts(self) -> list:
        """检查所有会话的超时状态，返回超时的会话 ID 列表"""
        timed_out = []
        for session_id, state in list(self._states.items()):
            if state.active and self._is_timeout(state):
                timed_out.append(session_id)
                state.active = False
        if timed_out:
            self._save_states()
        return timed_out
    
    def list_active_sessions(self) -> list:
        """列出所有活跃会话"""
        # 先检查超时
        self.check_timeouts()
        return [
            state.to_dict() 
            for state in self._states.values() 
            if state.active
        ]
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """获取会话信息（用于调试）"""
        state = self._states.get(session_id)
        if not state:
            return None
        
        return {
            'session_id': state.session_id,
            'workflow_type': state.workflow_type,
            'current_step': state.current_step,
            'step_data': state.step_data,
            'active': state.active,
            'created_at': datetime.fromtimestamp(state.created_at).isoformat(),
            'updated_at': datetime.fromtimestamp(state.updated_at).isoformat(),
            'timeout_seconds': state.timeout_seconds,
            'age_seconds': int(time.time() - state.updated_at)
        }


# 单例实例
state_manager = StateManager()


if __name__ == '__main__':
    # 测试代码
    import sys
    
    if len(sys.argv) < 2:
        print("用法：state_manager.py <command> [args]")
        print("命令:")
        print("  list                    - 列出活跃会话")
        print("  info <session_id>       - 查看会话信息")
        print("  clear <session_id>      - 清除会话")
        print("  check-timeouts          - 检查超时")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'list':
        sessions = state_manager.list_active_sessions()
        if not sessions:
            print("暂无活跃会话")
        else:
            print(f"活跃会话数：{len(sessions)}")
            for s in sessions:
                print(f"  - {s['session_id']}: {s['workflow_type']} (步骤 {s['current_step']})")
    
    elif cmd == 'info' and len(sys.argv) >= 3:
        session_id = sys.argv[2]
        info = state_manager.get_session_info(session_id)
        if info:
            print(json.dumps(info, ensure_ascii=False, indent=2))
        else:
            print(f"未找到会话：{session_id}")
    
    elif cmd == 'clear' and len(sys.argv) >= 3:
        session_id = sys.argv[2]
        if state_manager.clear_session(session_id):
            print(f"已清除会话：{session_id}")
        else:
            print(f"会话不存在：{session_id}")
    
    elif cmd == 'check-timeouts':
        timed_out = state_manager.check_timeouts()
        if timed_out:
            print(f"超时会话：{', '.join(timed_out)}")
        else:
            print("无超时会话")
    
    else:
        print("未知命令或参数不足")
        sys.exit(1)
