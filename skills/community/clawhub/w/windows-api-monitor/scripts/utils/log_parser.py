"""
日志解析工具模块
用于解析OpenClaw在Windows环境下的日志文件
"""

import os
import json
import re
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class LogParser:
    """OpenClaw日志解析器"""
    
    def __init__(self, log_dir: Optional[str] = None):
        """初始化日志解析器"""
        if log_dir is None:
            self.log_dir = os.path.join(os.path.expanduser("~"), ".openclaw", "logs")
        else:
            self.log_dir = log_dir
            
        self.supported_formats = ['.log', '.json', '.jsonl']
        
    def find_logs_by_date(self, date_str: str) -> List[str]:
        """按日期查找日志文件"""
        log_files = []
        log_path = Path(self.log_dir)
        
        if not log_path.exists():
            return log_files
            
        # 支持多种日期格式匹配
        patterns = [
            f"*{date_str}*.log",
            f"*{date_str.replace('-', '')}*.log",
            f"session_*{date_str}*.json",
        ]
        
        for pattern in patterns:
            for log_file in log_path.glob(pattern):
                log_files.append(str(log_file))
                
        return sorted(log_files)
    
    def parse_jsonl_file(self, file_path: str) -> List[Dict]:
        """解析JSONL格式的日志文件"""
        entries = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        entry = json.loads(line)
                        entries.append({
                            "line": line_num,
                            "data": entry,
                            "source": os.path.basename(file_path),
                        })
                    except json.JSONDecodeError as e:
                        continue
                        
        except Exception as e:
            print(f"解析JSONL文件失败 {file_path}: {e}")
            
        return entries
    
    def parse_text_log(self, file_path: str) -> List[Dict]:
        """解析文本格式的日志文件"""
        entries = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    # 尝试提取时间戳和内容
                    timestamp_match = re.match(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\](.*)', line)
                    if timestamp_match:
                        timestamp, content = timestamp_match.groups()
                        entries.append({
                            "line": line_num,
                            "timestamp": timestamp.strip(),
                            "content": content.strip(),
                            "source": os.path.basename(file_path),
                        })
                    else:
                        entries.append({
                            "line": line_num,
                            "content": line,
                            "source": os.path.basename(file_path),
                        })
                        
        except Exception as e:
            print(f"解析文本日志失败 {file_path}: {e}")
            
        return entries
    
    def extract_api_calls(self, entries: List[Dict]) -> List[Dict]:
        """从日志条目中提取API调用记录"""
        api_calls = []
        
        for entry in entries:
            data = entry.get("data", {}) if "data" in entry else {}
            content = entry.get("content", "")
            
            # 检查是否为API调用
            if self._is_api_call(data, content):
                call_info = self._parse_api_call_info(data, content)
                if call_info:
                    api_calls.append({
                        **call_info,
                        "source": entry.get("source"),
                        "line": entry.get("line"),
                        "timestamp": entry.get("timestamp", ""),
                    })
                    
        return api_calls
    
    def _is_api_call(self, data: Dict, content: str) -> bool:
        """判断是否为API调用记录"""
        # 检查JSON数据中的API调用标志
        if isinstance(data, dict):
            api_keys = ['model', 'provider', 'agent', 'usage', 'tokens']
            return any(key in data for key in api_keys)
        
        # 检查文本内容中的API调用标志
        text_indicators = [
            'model:', 'provider:', 'tokens:', 'api call',
            'model_usage', 'generation', 'completion',
        ]
        
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in text_indicators)
    
    def _parse_api_call_info(self, data: Dict, content: str) -> Optional[Dict]:
        """解析API调用信息"""
        info = {}
        
        # 从JSON数据解析
        if isinstance(data, dict):
            info.update({
                "model": data.get("model"),
                "provider": data.get("provider"),
                "agent": data.get("agent"),
                "usage": data.get("usage"),
                "session": data.get("session"),
            })
            
            # 提取令牌信息
            if "usage" in data and isinstance(data["usage"], dict):
                usage = data["usage"]
                info.update({
                    "prompt_tokens": usage.get("prompt_tokens"),
                    "completion_tokens": usage.get("completion_tokens"),
                    "total_tokens": usage.get("total_tokens"),
                })
        
        # 从文本内容解析（正则表达式）
        if content:
            # 提取模型名称
            model_match = re.search(r'model[:\s]+([\w-]+)', content, re.IGNORECASE)
            if model_match:
                info["model"] = model_match.group(1)
                
            # 提取令牌数
            tokens_match = re.search(r'tokens[:\s]+(\d+)', content, re.IGNORECASE)
            if tokens_match:
                info["total_tokens"] = int(tokens_match.group(1))
                
            # 提取成本信息
            cost_match = re.search(r'cost[:\s]+([\d.]+)', content, re.IGNORECASE)
            if cost_match:
                info["cost"] = float(cost_match.group(1))
        
        return info if info else None
    
    def get_session_stats(self, session_id: str) -> Dict[str, Any]:
        """获取指定会话的统计信息"""
        stats = {
            "session_id": session_id,
            "total_calls": 0,
            "total_tokens": 0,
            "models": {},
            "start_time": None,
            "end_time": None,
        }
        
        # 查找会话相关的日志文件
        session_pattern = f"*session*{session_id}*"
        log_path = Path(self.log_dir)
        
        for log_file in log_path.glob(session_pattern):
            entries = self.parse_jsonl_file(str(log_file)) if str(log_file).endswith('.json') else self.parse_text_log(str(log_file))
            api_calls = self.extract_api_calls(entries)
            
            for call in api_calls:
                stats["total_calls"] += 1
                stats["total_tokens"] += call.get("total_tokens", 0)
                
                model = call.get("model", "unknown")
                if model not in stats["models"]:
                    stats["models"][model] = {
                        "calls": 0,
                        "tokens": 0,
                    }
                stats["models"][model]["calls"] += 1
                stats["models"][model]["tokens"] += call.get("total_tokens", 0)
                
                # 更新时间范围
                timestamp = call.get("timestamp")
                if timestamp:
                    try:
                        dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                        if stats["start_time"] is None or dt < stats["start_time"]:
                            stats["start_time"] = dt
                        if stats["end_time"] is None or dt > stats["end_time"]:
                            stats["end_time"] = dt
                    except ValueError:
                        pass
        
        return stats