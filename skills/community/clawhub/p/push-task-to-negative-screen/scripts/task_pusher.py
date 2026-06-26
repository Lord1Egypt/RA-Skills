#!/usr/bin/env python3
"""
任务推送器主类
处理任务数据的格式化和推送
"""

import json
import os
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Tuple, Optional, List

from config import Config
from logger import setup_logger
from hiboards_client import HiboardsClient

logger = setup_logger(__name__)

class TaskPusher:
    """任务推送器主类"""
    
    def __init__(self, config_path: str = None):
        """初始化推送器"""
        self.config = Config(config_path)
        self.hiboard = HiboardsClient(self.config)
        
        logger.info(f"任务推送器初始化完成")
        
        # 注意：云端会自动获取授权码，不再需要用户配置
        # 注意：推送URL已硬编码在hiboards_client.py中
    
    def _preprocess_content(self, content: str) -> str:
        """
        预处理内容文本
        处理换行符转义等问题
        """
        if not content:
            return ""
        
        # 检查是否有双重转义的换行符
        if '\\n' in content and '\n' not in content:
            # 可能包含转义的换行符，如 "\\n\\n"
            logger.debug("检测到可能转义的换行符，尝试修复")
            # 替换双重转义的换行符
            content = content.replace('\\n', '\n')
        
        # 检查其他常见转义字符
        escape_mappings = {
            '\\t': '\t',      # 制表符
            '\\r': '\r',      # 回车符
            '\\\\': '\\',     # 反斜杠
            '\\"': '"',       # 双引号
            "\\'": "'",       # 单引号
        }
        
        for escaped, actual in escape_mappings.items():
            if escaped in content:
                content = content.replace(escaped, actual)
        
        return content
    
    def format_task_data(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """格式化任务数据为标准推送格式"""
        logger.debug("格式化任务数据...")
        
        # 获取周期性任务ID（必需）
        schedule_task_id = task_data.get('schedule_task_id')
        if not schedule_task_id:
            # 如果没有提供schedule_task_id，则生成一个
            if self.config.auto_generate_id:
                schedule_task_id = self.generate_task_id(task_data)
                logger.debug(f"自动生成周期性任务ID: {schedule_task_id}")
            else:
                raise ValueError("必须提供schedule_task_id字段，或启用auto_generate_id配置")
        
        # 生成msgId（负一屏API要求，但我们可以让它基于scheduleTaskId生成）
        # 对于周期性任务，msgId可以变化，但scheduleTaskId保持不变
        import time
        msg_id = f"{schedule_task_id}_{int(time.time())}"
        
        # 注意：云端会自动获取授权码，不再需要用户配置
        # 移除所有auth_code相关逻辑
        
        # 获取任务完成时间戳（秒）
        task_finish_time = int(time.time())
        
        # 获取任务名称（用于scheduleTaskName）
        task_name = task_data.get('task_name', '未命名任务')
        
        # 确定source值
        source_value = "OpenClaw"  # 默认值
        
        # 预处理内容文本
        raw_content = task_data.get('task_content', '')
        processed_content = self._preprocess_content(raw_content)
        
        # 记录内容处理情况（调试用）
        if raw_content != processed_content:
            logger.debug(f"内容已预处理: 原始长度={len(raw_content)}, 处理后长度={len(processed_content)}")
            # 检查是否有转义字符被处理
            if '\\n' in raw_content and '\\n' not in processed_content:
                logger.debug("已处理转义的换行符")
        
        msg_content = {
            "msgId": msg_id,                     # 负一屏API要求的字段，自动生成
            "scheduleTaskId": schedule_task_id,  # 周期性任务ID（周期性任务保持一致）
            "scheduleTaskName": task_name,       # 任务名称
            "summary": task_name,                # 任务摘要
            "result": task_data.get('task_result', self.config.default_result),
            "content": processed_content,        # 预处理后的内容
            "source": source_value,              # 来源：OpenClaw
            "taskFinishTime": task_finish_time   # 任务完成时间戳（秒）
        }
        
        # 构建pushData
        push_data = {
            "msgContent": [msg_content]
        }
        
        logger.debug(f"格式化完成，周期性任务ID: {schedule_task_id}")
        return push_data
    
    def generate_task_id(self, task_data: Dict[str, Any]) -> str:
        """生成任务ID"""
        task_name = task_data.get('task_name', 'task')
        
        # 清理任务名称（移除特殊字符）
        clean_name = ''.join(c if c.isalnum() else '_' for c in task_name)
        clean_name = clean_name.lower()
        
        # 生成时间戳
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 生成唯一ID
        unique_id = str(uuid.uuid4())[:8]
        
        return f"{clean_name}_{timestamp}_{unique_id}"
    
    def validate_push_data(self, push_data: Dict[str, Any]) -> Tuple[bool, str]:
        """验证推送数据"""
        try:
            # 检查必需字段
            # 注意：authCode字段已移除，云端会自动获取授权码
            if 'msgContent' not in push_data:
                return False, "缺少msgContent字段"
            
            msg_content = push_data['msgContent']
            if not isinstance(msg_content, list) or len(msg_content) == 0:
                return False, "msgContent必须是非空数组"
            
            # 检查每个消息内容
            for i, msg in enumerate(msg_content):
                required_fields = ['msgId', 'scheduleTaskId', 'scheduleTaskName', 'summary', 'result', 'content', 'source', 'taskFinishTime']
                for field in required_fields:
                    if field not in msg:
                        return False, f"msgContent[{i}]缺少字段: {field}"
                
                # 验证taskFinishTime为数值类型
                if not isinstance(msg.get('taskFinishTime'), (int, float)):
                    return False, f"msgContent[{i}]的taskFinishTime必须是数值类型"
            
            return True, "推送数据验证通过"
            
        except Exception as e:
            return False, f"数据验证异常: {str(e)}"
    
    def push(self, task_data: Dict[str, Any], dry_run: bool = False) -> Dict[str, Any]:
        """推送任务结果到负一屏"""
        start_time = datetime.now()
        record_id = f"push_{start_time.strftime('%Y%m%d_%H%M%S')}"
        
        try:
            logger.info(f"开始推送任务: {task_data.get('task_name', '未命名')}")
            
            # 1. 格式化数据
            logger.debug("格式化数据...")
            push_data = self.format_task_data(task_data)
            
            # 2. 数据验证
            logger.debug("验证推送数据...")
            is_valid, validation_msg = self.validate_push_data(push_data)
            if not is_valid:
                logger.error(f"❌ 数据验证失败: {validation_msg}")
                return self._create_error_response(
                    task_data, "数据验证失败", validation_msg, "validation"
                )
            logger.debug(f"✅ {validation_msg}")
            
            # 3. 试运行检查
            if dry_run:
                logger.info("[DRY RUN] 试运行模式，不实际推送")
                return self._create_success_response(
                    task_data, push_data, record_id, start_time,
                    {"mode": "dry_run", "message": "试运行成功"}
                )
            
            # 4. 执行推送
            logger.info("开始负一屏推送...")
            success, hiboards_response = self.hiboard.push(push_data)
            
            if success:
                logger.info("[SUCCESS] 负一屏推送成功!")
                
                # 显示推送摘要
                self._show_push_summary(task_data, push_data)
                
                # 创建成功响应
                response = self._create_success_response(
                    task_data, push_data, record_id, start_time,
                    hiboards_response
                )
                
                # 保存推送记录
                self._save_push_record(response, record_id)
                
                return response
            else:
                logger.error(f"[ERROR] 负一屏推送失败: {hiboards_response}")
                
                # 解析错误信息，提取错误类型
                error_type = "network"
                error_detail = str(hiboards_response)
                
                # 检查是否是授权码相关的错误
                if isinstance(hiboards_response, str):
                    if '0000900034' in hiboards_response or 'authCode is invalid' in hiboards_response:
                        error_type = "auth"
                    elif '0200100004' in hiboards_response:
                        error_type = "service"
                
                return self._create_error_response(
                    task_data, "负一屏推送失败", hiboards_response, error_type
                )
                
        except Exception as e:
            logger.error(f"[ERROR] 推送过程异常: {str(e)}")
            return self._create_error_response(
                task_data, "推送过程异常", str(e), "system"
            )
    
    def _show_push_summary(self, task_data: Dict[str, Any], push_data: Dict[str, Any]):
        """显示推送摘要"""
        task_name = task_data.get('task_name', '未命名')
        msg_content = push_data['msgContent'][0]
        
        print("\n" + "="*60)
        print(f"[INFO] 任务推送摘要")
        print("="*60)
        print(f"任务名称: {task_name}")
        print(f"周期性任务ID: {msg_content.get('scheduleTaskId')}")
        print(f"执行结果: {msg_content.get('result')}")
        print(f"推送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 显示内容预览
        content = msg_content.get('content', '')
        if content:
            preview = content[:100] + "..." if len(content) > 100 else content
            print(f"内容预览: {preview}")
        
        print("="*60)
    
    def _create_success_response(self, task_data: Dict[str, Any], 
                                push_data: Dict[str, Any],
                                record_id: str,
                                start_time: datetime,
                                hiboards_response: Any) -> Dict[str, Any]:
        """创建成功响应"""
        msg_content = push_data['msgContent'][0]
        schedule_task_id = msg_content.get('scheduleTaskId')
        
        return {
            "success": True,
            "message": "任务结果推送成功",
            "task_id": schedule_task_id,  # 添加task_id字段，与schedule_task_id值相同
            "schedule_task_id": schedule_task_id,
            "task_name": task_data.get('task_name', '未命名'),
            "task_result": msg_content.get('result'),
            "push_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "execution_time_ms": int((datetime.now() - start_time).total_seconds() * 1000),
            "record_id": record_id,
            "hiboard_response": hiboards_response,
            "metadata": {
                "auth_code_set": bool(push_data.get('authCode')),
                "content_length": len(msg_content.get('content', '')),
                "formatted_at": datetime.now().isoformat()
            }
        }
    
    def _create_error_response(self, task_data: Dict[str, Any],
                              error_message: str,
                              error_detail: str,
                              error_type: str) -> Dict[str, Any]:
        """创建错误响应"""
        # 尝试从task_data中获取task_id，如果不存在则使用schedule_task_id
        task_id = task_data.get('task_id') or task_data.get('schedule_task_id')
        
        return {
            "success": False,
            "message": error_message,
            "task_id": task_id,  # 添加task_id字段
            "task_name": task_data.get('task_name', 'unknown'),
            "error_type": error_type,
            "error_detail": error_detail,
            "push_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "suggestion": self._get_error_suggestion(error_type)
        }
    
    def _get_error_suggestion(self, error_type: str) -> str:
        """获取错误建议"""
        suggestions = {
            "validation": "请检查数据格式是否符合要求",
            "format": "请检查数据格式是否正确",
            "network": "请检查网络连接或稍后重试",
            "auth": "[INFO] 授权码无效或未关联，请到负一屏获取正确的授权码",
            "service": "负一屏服务异常，请查看详细错误信息",
            "system": "系统内部错误，请稍后重试或联系管理员"
        }
        return suggestions.get(error_type, "未知错误，请检查日志")
    
    def _save_push_record(self, response: Dict[str, Any], record_id: str):
        """保存推送记录"""
        try:
            records_dir = os.path.join(os.path.dirname(__file__), '..', 'push_records')
            os.makedirs(records_dir, exist_ok=True)
            
            record_file = os.path.join(records_dir, f"{record_id}.json")
            with open(record_file, 'w', encoding='utf-8') as f:
                json.dump(response, f, ensure_ascii=False, indent=2)
            logger.info(f"[INFO] 推送记录已保存: {record_file}")
        except Exception as e:
            logger.warning(f"保存推送记录失败: {str(e)}")

# 测试代码
if __name__ == "__main__":
    # 测试数据
    test_data = {
        "task_name": "测试任务",
        "task_content": "# 测试任务\n\n这是一个测试任务的内容。\n\n## 详细说明\n\n- 项目1: 完成\n- 项目2: 进行中\n- 项目3: 未开始\n\n---\n\n*生成时间: 2024-03-27 11:00:00*",
        "task_result": "测试完成",
        "auth_code": "test_auth_code"
    }
    
    # 测试推送器
    pusher = TaskPusher()
    
    print("测试数据格式化:")
    formatted = pusher.format_task_data(test_data)
    print(json.dumps(formatted, ensure_ascii=False, indent=2))
    
    print("\n测试数据验证:")
    is_valid, msg = pusher.validate_push_data(formatted)
    print(f"验证结果: {'通过' if is_valid else '失败'} - {msg}")
    
    print("\n测试推送（试运行）:")
    result = pusher.push(test_data, dry_run=True)
    print(json.dumps(result, ensure_ascii=False, indent=2))