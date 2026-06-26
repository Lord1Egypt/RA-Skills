import os
import json
import uuid
from datetime import datetime
import threading

# 配置
LOG_DIR = r"D:\code\openclaw_lakeskill\water-knowledge-assistant\logs"
LOG_FILE_PREFIX = "water_knowledge_assistant_"
LOG_FILE_EXTENSION = ".jsonl"
LOG_LEVELS = ["debug", "info", "warning", "error", "critical"]
DEFAULT_LOG_LEVEL = "info"

# 线程锁，确保日志写入的原子性
log_lock = threading.Lock()


class AuditLogger:
    """审计日志记录器"""
    
    def __init__(self, log_level=DEFAULT_LOG_LEVEL):
        """初始化日志记录器"""
        self.log_level = log_level.lower()
        self.log_level_index = LOG_LEVELS.index(self.log_level)
        
        # 确保日志目录存在
        os.makedirs(LOG_DIR, exist_ok=True)
        
        # 获取当前日期的日志文件路径
        self.log_file_path = self._get_log_file_path()
        
    def _get_log_file_path(self):
        """获取当前日期的日志文件路径"""
        today = datetime.now().strftime("%Y%m%d")
        return os.path.join(LOG_DIR, f"{LOG_FILE_PREFIX}{today}{LOG_FILE_EXTENSION}")
    
    def _should_log(self, level):
        """检查是否应该记录该级别的日志"""
        return LOG_LEVELS.index(level.lower()) >= self.log_level_index
    
    def _write_log(self, log_entry):
        """将日志条目写入文件"""
        # 确保日志文件路径是最新的（跨日时自动切换）
        current_log_file = self._get_log_file_path()
        if current_log_file != self.log_file_path:
            self.log_file_path = current_log_file
        
        # 使用线程锁确保原子写入
        with log_lock:
            try:
                with open(self.log_file_path, "a", encoding="utf-8") as f:
                    json.dump(log_entry, f, ensure_ascii=False)
                    f.write("\n")
                return True
            except Exception as e:
                print(f"写入日志失败: {e}")
                return False
    
    def log(self, action_type, input_data=None, output_data=None, tool_name=None, risk_level="low", session_id=None, user_id=None, trace_id=None):
        """记录日志"""
        # 生成唯一ID
        if trace_id is None:
            trace_id = str(uuid.uuid4())
        
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        # 构建日志条目
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "session_id": session_id,
            "user_id": user_id,
            "action_type": action_type,
            "tool_name": tool_name,
            "input": input_data,
            "output": output_data,
            "risk_level": risk_level,
            "trace_id": trace_id
        }
        
        # 写入日志
        self._write_log(log_entry)
        return trace_id
    
    def debug(self, action_type, input_data=None, output_data=None, tool_name=None, risk_level="low", session_id=None, user_id=None, trace_id=None):
        """记录debug级别的日志"""
        if self._should_log("debug"):
            return self.log(action_type, input_data, output_data, tool_name, risk_level, session_id, user_id, trace_id)
        return trace_id
    
    def info(self, action_type, input_data=None, output_data=None, tool_name=None, risk_level="low", session_id=None, user_id=None, trace_id=None):
        """记录info级别的日志"""
        if self._should_log("info"):
            return self.log(action_type, input_data, output_data, tool_name, risk_level, session_id, user_id, trace_id)
        return trace_id
    
    def warning(self, action_type, input_data=None, output_data=None, tool_name=None, risk_level="medium", session_id=None, user_id=None, trace_id=None):
        """记录warning级别的日志"""
        if self._should_log("warning"):
            return self.log(action_type, input_data, output_data, tool_name, risk_level, session_id, user_id, trace_id)
        return trace_id
    
    def error(self, action_type, input_data=None, output_data=None, tool_name=None, risk_level="high", session_id=None, user_id=None, trace_id=None):
        """记录error级别的日志"""
        if self._should_log("error"):
            return self.log(action_type, input_data, output_data, tool_name, risk_level, session_id, user_id, trace_id)
        return trace_id
    
    def critical(self, action_type, input_data=None, output_data=None, tool_name=None, risk_level="critical", session_id=None, user_id=None, trace_id=None):
        """记录critical级别的日志"""
        if self._should_log("critical"):
            return self.log(action_type, input_data, output_data, tool_name, risk_level, session_id, user_id, trace_id)
        return trace_id
    
    def log_user_input(self, user_input, session_id=None, user_id=None, trace_id=None):
        """记录用户输入"""
        return self.info("user_input", input_data=user_input, session_id=session_id, user_id=user_id, trace_id=trace_id)
    
    def log_ai_decision(self, decision, session_id=None, user_id=None, trace_id=None):
        """记录AI决策"""
        return self.info("ai_decision", output_data=decision, session_id=session_id, user_id=user_id, trace_id=trace_id)
    
    def log_tool_call(self, tool_name, input_data, session_id=None, user_id=None, trace_id=None):
        """记录工具调用"""
        return self.info("tool_call", input_data=input_data, tool_name=tool_name, session_id=session_id, user_id=user_id, trace_id=trace_id)
    
    def log_tool_result(self, tool_name, output_data, session_id=None, user_id=None, trace_id=None):
        """记录工具返回结果"""
        return self.info("tool_result", output_data=output_data, tool_name=tool_name, session_id=session_id, user_id=user_id, trace_id=trace_id)
    
    def log_retrieval_result(self, query, results, session_id=None, user_id=None, trace_id=None):
        """记录检索结果"""
        return self.info(
            "retrieval_result",
            input_data=query,
            output_data={
                "results_count": len(results),
                "results": [{
                    "page_content": r.page_content[:100] + "..." if len(r.page_content) > 100 else r.page_content,
                    "metadata": r.metadata
                } for r in results]
            },
            tool_name="vector_search",
            session_id=session_id,
            user_id=user_id,
            trace_id=trace_id
        )
    
    def log_error(self, error_message, action_type="unknown", session_id=None, user_id=None, trace_id=None):
        """记录错误信息"""
        return self.error(
            action_type,
            output_data={"error": True, "message": error_message},
            risk_level="high",
            session_id=session_id,
            user_id=user_id,
            trace_id=trace_id
        )


# 创建全局日志记录器实例
global_logger = AuditLogger()


def get_logger():
    """获取全局日志记录器"""
    return global_logger


def log_user_input(user_input, session_id=None, user_id=None, trace_id=None):
    """便捷函数：记录用户输入"""
    return global_logger.log_user_input(user_input, session_id, user_id, trace_id)


def log_ai_decision(decision, session_id=None, user_id=None, trace_id=None):
    """便捷函数：记录AI决策"""
    return global_logger.log_ai_decision(decision, session_id, user_id, trace_id)


def log_tool_call(tool_name, input_data, session_id=None, user_id=None, trace_id=None):
    """便捷函数：记录工具调用"""
    return global_logger.log_tool_call(tool_name, input_data, session_id, user_id, trace_id)


def log_tool_result(tool_name, output_data, session_id=None, user_id=None, trace_id=None):
    """便捷函数：记录工具返回结果"""
    return global_logger.log_tool_result(tool_name, output_data, session_id, user_id, trace_id)


def log_retrieval_result(query, results, session_id=None, user_id=None, trace_id=None):
    """便捷函数：记录检索结果"""
    return global_logger.log_retrieval_result(query, results, session_id, user_id, trace_id)


def log_error(error_message, action_type="unknown", session_id=None, user_id=None, trace_id=None):
    """便捷函数：记录错误信息"""
    return global_logger.log_error(error_message, action_type, session_id, user_id, trace_id)


if __name__ == "__main__":
    # 测试审计日志功能
    logger = get_logger()
    
    # 记录用户输入
    trace_id = log_user_input("RL-1000 的防护等级是多少？")
    print(f"记录用户输入，trace_id: {trace_id}")
    
    # 记录工具调用
    log_tool_call("vector_search", {"query": "RL-1000 防护等级"}, trace_id=trace_id)
    
    # 记录AI决策
    log_ai_decision("RL-1000 的防护等级为 IP68", trace_id=trace_id)
    
    print("审计日志测试完成")