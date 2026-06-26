#!/usr/bin/env python3
"""
通用任务结果推送器 - 简化版
使用统一的标准数据格式推送到负一屏
已移除版本检查更新功能，专为小艺claw skill市场适配
"""

import sys
import json
import os
import argparse
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Tuple, Optional, List
from pathlib import Path

# 添加技能目录到路径
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 定义SimpleConfig类（无论模块是否导入都可用）
class SimpleConfig:
    def __init__(self, config_path=None):
        # 简化版本：仅从本地config.json文件读取配置
        import os
        import json
        
        # 设置默认值
        self.timeout = 30
        self.max_content_length = 5000
        self.auto_generate_id = True
        self.default_result = '任务已完成'
        
        # 从本地配置文件读取配置（可选）
        if config_path and os.path.exists(config_path):
            config_file = config_path
        else:
            # 使用技能目录的config.json
            script_dir = os.path.dirname(os.path.abspath(__file__))
            skill_dir = os.path.dirname(script_dir)
            config_file = os.path.join(skill_dir, 'config.json')
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # 从配置文件读取配置，覆盖默认值
                self.timeout = config_data.get('timeout', self.timeout)
                self.max_content_length = config_data.get('max_content_length', self.max_content_length)
                self.auto_generate_id = config_data.get('auto_generate_id', self.auto_generate_id)
                self.default_result = config_data.get('default_result', self.default_result)
                
                print(f"从本地配置文件读取配置: {config_file}")
                
            except Exception as e:
                print(f"读取本地配置文件失败，使用默认配置: {str(e)}")
        else:
            print("本地配置文件不存在，使用默认配置")

# 尝试导入其他模块
try:
    from task_pusher import TaskPusher
    from config import Config
    from logger import setup_logger
except ImportError:
    # 如果模块不存在，使用SimpleConfig
    Config = SimpleConfig
    print("警告：某些模块未找到，使用简化版本")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='通用任务结果推送器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python task_push.py --data task.json
  python task_push.py --data task.json --dry-run
  python task_push.py --data task.json --verbose
        """
    )
    
    # 参数组
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--data', help='任务数据，JSON字符串或文件路径')
    
    # 可选参数
    parser.add_argument('--name', help='任务名称（与--content一起使用）')
    parser.add_argument('--content', help='任务内容，markdown格式（与--name一起使用）')
    parser.add_argument('--result', help='任务执行结果，默认"任务已完成"')
    parser.add_argument('--schedule-id', help='周期性任务ID，非周期性任务时等于task_id')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行，不实际推送')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 设置日志
    log_level = 'DEBUG' if args.verbose else 'INFO'
    logger = setup_logger(__name__, level=log_level)
    
    logger.info("=" * 60)
    logger.info("通用任务结果推送器 - 小艺claw适配版")
    logger.info("执行时间: %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("=" * 60)
    
    try:
        # 加载配置
        config = SimpleConfig(args.config)
        
        # 加载任务数据
        task_data = load_task_data(args)
        logger.info("验证任务数据...")
        
        # 验证数据
        validated_data = validate_task_data(task_data, config)
        logger.info("数据验证通过")
        
        # 显示任务信息
        logger.info("任务信息:")
        logger.info("任务名称: %s", validated_data.get('task_name'))
        logger.info("任务ID: %s", validated_data.get('task_id'))
        logger.info("执行结果: %s", validated_data.get('task_result'))
        
        content_preview = validated_data.get('task_content', '')[:100]
        if len(validated_data.get('task_content', '')) > 100:
            content_preview += "..."
        logger.info("内容预览: %s", content_preview)
        
        if args.dry_run:
            logger.info("模拟模式，不实际推送")
            
            # 生成推送数据
            push_data = generate_push_data(validated_data)
            logger.info("推送数据预览:")
            print(json.dumps(push_data, ensure_ascii=False, indent=2))
            
            logger.info("模拟运行完成，数据验证通过")
            return
        
        # 执行推送
        logger.info("开始推送任务...")
        # 传递配置路径字符串，而不是配置对象
        pusher = TaskPusher(args.config)
        
        logger.info("开始推送任务: %s", validated_data.get('task_name'))
        result = pusher.push(validated_data)
        
        if result.get('success', False):
            # 推送成功
            success_result = {
                "success": True,
                "message": "任务结果推送成功",
                "task_id": validated_data.get('task_id'),
                "task_name": validated_data.get('task_name'),
                "push_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "record_id": result.get('record_id', ''),
                "hiboard_response": result.get('hiboard_response', {})
            }
            
            print("\n执行成功:")
            print("[成功] 任务推送成功！")
            print("-" * 40)
            print(json.dumps(success_result, ensure_ascii=False, indent=2))
            
        else:
            # 推送失败
            error_result = {
                "success": False,
                "message": "负一屏推送失败",
                "task_id": validated_data.get('task_id'),
                "task_name": validated_data.get('task_name'),
                "error_type": "network",
                "error_detail": result.get('error', '未知错误'),
                "push_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "suggestion": "请检查网络连接或稍后重试"
            }
            
            print("\n执行失败:")
            print("[失败] 任务推送失败！")
            print(f"{result.get('error', '未知错误')}")
            print("-" * 40)
            print(json.dumps(error_result, ensure_ascii=False, indent=2))
            
            sys.exit(1)
            
    except ValueError as e:
        # 数据验证错误
        error_result = {
            "success": False,
            "message": "数据验证失败",
            "error_type": "validation",
            "error_detail": str(e),
            "push_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "suggestion": "请检查任务数据格式是否正确"
        }
        
        print("\n执行失败:")
        print("[失败] 任务推送失败！")
        print(f"数据验证失败: {str(e)}")
        print("-" * 40)
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        
        sys.exit(1)
        
    except Exception as e:
        # 其他错误
        error_result = {
            "success": False,
            "message": "系统错误",
            "error_type": "system",
            "error_detail": str(e),
            "push_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "suggestion": "请检查系统配置或联系技术支持"
        }
        
        print("\n执行失败:")
        print("[失败] 任务推送失败！")
        print(f"系统错误: {str(e)}")
        print("-" * 40)
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        
        sys.exit(1)

def load_task_data(args):
    """加载任务数据"""
    if args.data:
        # 从文件或JSON字符串加载
        data_str = args.data
        
        # 检查是否是文件路径
        if os.path.exists(data_str):
            with open(data_str, 'r', encoding='utf-8') as f:
                data_str = f.read()
        
        try:
            return json.loads(data_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON解析失败: {str(e)}")
    
    elif args.name and args.content:
        # 从命令行参数构建
        return {
            "task_name": args.name,
            "task_content": args.content,
            "task_result": args.result or "任务已完成",
            "schedule_task_id": args.schedule_id or f"{args.name}_{int(datetime.now().timestamp())}"
        }
    
    else:
        raise ValueError("必须提供--data参数或--name和--content参数")

def validate_task_data(data, config):
    """验证任务数据"""
    required_fields = ['task_name', 'task_content', 'task_result']
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"缺少必需字段: {field}")
    
    # 检查内容长度
    content = data.get('task_content', '')
    if len(content) > config.max_content_length:
        raise ValueError(f"任务内容过长，最大允许{config.max_content_length}字符，当前{len(content)}字符")
    
    # 生成或验证task_id
    if 'task_id' not in data or not data['task_id']:
        if config.auto_generate_id:
            data['task_id'] = f"{data['task_name']}_{int(datetime.now().timestamp())}"
        else:
            raise ValueError("缺少task_id字段且未启用自动生成")
    
    # 设置schedule_task_id
    if 'schedule_task_id' not in data or not data['schedule_task_id']:
        data['schedule_task_id'] = data['task_id']
    
    return data

def generate_push_data(task_data):
    """生成推送数据"""
    import time
    
    return {
        "msgContent": [{
            "scheduleTaskId": task_data['schedule_task_id'],
            "scheduleTaskName": task_data['task_name'],
            "summary": task_data['task_name'],
            "result": task_data['task_result'],
            "content": task_data['task_content'],
            "source": "小艺 Claw",
            "taskFinishTime": int(time.time())
        }]
    }

if __name__ == "__main__":
    main()