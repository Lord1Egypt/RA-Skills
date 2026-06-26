#!/usr/bin/env python3
"""
通用任务结果推送器
使用统一的标准数据格式推送到负一屏
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

try:
    from task_pusher import TaskPusher
    from config import Config
    from logger import setup_logger
except ImportError:
    # 如果模块不存在，创建简化版本
    pass

# 导入更新检查模块
update_checker_available = False
try:
    from update_checker import check_update
    update_checker_available = True
except ImportError:
    # 如果模块不存在，跳过更新检查
    pass
    print("警告：某些模块未找到，使用简化版本")
    
    class SimpleConfig:
        def __init__(self, config_path=None):
            # 简化版本：混合配置（auth_code和hiboard_url从OpenClaw全局配置，其他从本地文件）
            import os
            import json
            
            # 初始化默认值
            self.auth_code = 'NOT_SET_IN_OPENCLAW'
            self.hiboard_url = 'NOT_SET_IN_OPENCLAW'
            
            # 尝试从OpenClaw全局配置读取（模拟）
            # 在实际OpenClaw环境中，这些值会由运行时注入
            try:
                # 这里模拟从OpenClaw全局配置读取
                # 实际OpenClaw会通过环境变量或其他方式传递这些值
                openclaw_config = self._load_openclaw_global_config()
                
                if openclaw_config.get('authCode'):
                    self.auth_code = openclaw_config['authCode']
                    print(f"从OpenClaw全局配置读取auth_code: {self.auth_code[:4]}***")
                
                # 注意：推送URL已硬编码，不再从配置读取
                self.hiboard_url = "硬编码在hiboards_client.py中"
                print("推送URL已硬编码，不再支持配置")
            except:
                pass  # 如果无法读取OpenClaw配置，继续使用默认值
            
            # 从本地配置文件读取其他配置
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
                    
                    # 只从本地文件读取其他配置，不覆盖auth_code和hiboard_url
                    self.timeout = config_data.get('timeout', 30)
                    self.max_content_length = config_data.get('max_content_length', 5000)
                    self.auto_generate_id = config_data.get('auto_generate_id', True)
                    self.default_result = config_data.get('default_result', '任务已完成')
                    
                    print(f"从本地配置文件读取其他配置: {config_file}")
                    
                except Exception as e:
                    print(f"读取本地配置文件失败: {str(e)}")
                    # 使用默认值
                    self.timeout = 30
                    self.max_content_length = 5000
                    self.auto_generate_id = True
                    self.default_result = '任务已完成'
            else:
                # 使用默认值
                self.timeout = 30
                self.max_content_length = 5000
                self.auto_generate_id = True
                self.default_result = '任务已完成'
                print(f"本地配置文件不存在: {config_file}")
            
            # 验证必需配置是否已设置
            # 注意：推送URL已硬编码，不再需要验证
            if self.auth_code == 'NOT_SET_IN_OPENCLAW':
                error_msg = "配置中缺少必需字段\n"
                error_msg += "注意：云端会自动获取授权码，不再需要配置"
                raise ValueError(error_msg)
        
        def _load_openclaw_global_config(self):
            """从OpenClaw全局配置读取"""
            import json
            import os
            
            try:
                # 读取OpenClaw全局配置文件
                openclaw_config_path = os.path.join(os.path.expanduser("~"), ".openclaw", "openclaw.json")
                
                if os.path.exists(openclaw_config_path):
                    with open(openclaw_config_path, 'r', encoding='utf-8') as f:
                        openclaw_config = json.load(f)
                    
                    # 获取技能配置
                    skill_config = openclaw_config.get('skills', {}).get('entries', {}).get('today-task', {})
                    
                    return skill_config.get('config', {})
                else:
                    print(f"警告: OpenClaw配置文件不存在: {openclaw_config_path}")
                    return {}
                    
            except Exception as e:
                print(f"读取OpenClaw全局配置失败: {str(e)}")
                return {}
    
    Config = SimpleConfig
    
    # 简化版授权码管理器
    class SimpleAuthCodeManager:
        def detect_auth_code(self, text):
            return None
        
        def update_auth_code(self, auth_code):
            return False, "简化版本不支持授权码更新"
    
    AuthCodeManager = SimpleAuthCodeManager
    
    def setup_logger(name):
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

# 配置日志
logger = setup_logger(__name__)

def load_task_data(input_source: str) -> Dict[str, Any]:
    """加载任务数据"""
    try:
        # 处理空字符串输入
        if not input_source or not input_source.strip():
            logger.debug("输入为空字符串，返回空字典")
            return {}
        
        # 检查是否是文件路径
        if os.path.exists(input_source):
            logger.info(f"从文件读取数据: {input_source}")
            with open(input_source, 'r', encoding='utf-8') as f:
                raw_content = f.read()
                logger.debug(f"文件原始内容长度: {len(raw_content)}")
                data = json.loads(raw_content)
        else:
            # 尝试解析为JSON字符串
            logger.info("解析JSON字符串数据")
            logger.debug(f"输入字符串长度: {len(input_source)}")
            data = json.loads(input_source)
        
        # 调试：检查内容字段
        if 'task_content' in data:
            content = data['task_content']
            logger.debug(f"加载的内容字段长度: {len(content)}")
            logger.debug(f"内容前100字符: {repr(content[:100])}")
            
            # 检查是否有转义的换行符
            if isinstance(content, str):
                if '\\n' in content:
                    logger.debug("检测到转义的换行符 (\\n)")
                if '\n' in content:
                    logger.debug("检测到实际的换行符")
                if '\\\\n' in content:
                    logger.warning("检测到双重转义的换行符 (\\\\n)")
        
        return data
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析失败: {str(e)}")
        raise ValueError(f"JSON解析失败: {str(e)}")
    except Exception as e:
        logger.error(f"数据加载失败: {str(e)}")
        raise ValueError(f"数据加载失败: {str(e)}")

def validate_task_data(task_data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证任务数据"""
    try:
        # 检查必需字段
        required_fields = ['task_name', 'task_content']
        
        for field in required_fields:
            if field not in task_data:
                return False, f"缺少必需字段: {field}"
        
        # 检查内容长度
        content = task_data.get('task_content', '')
        if len(content) > 5000:  # 简单长度检查
            logger.warning(f"内容长度({len(content)})超过建议值(5000)")
        
        return True, "数据验证通过"
        
    except Exception as e:
        return False, f"数据验证异常: {str(e)}"

def format_for_display(task_data: Dict[str, Any]) -> str:
    """格式化数据用于显示"""
    display = []
    display.append(f"任务名称: {task_data.get('task_name', '未命名')}")
    display.append(f"周期性任务ID: {task_data.get('schedule_task_id', '未指定')}")
    display.append(f"执行结果: {task_data.get('task_result', '未指定')}")
    
    # 显示内容预览
    content = task_data.get('task_content', '')
    if content:
        preview = content[:100] + "..." if len(content) > 100 else content
        display.append(f"内容预览: {preview}")
    
    return "\n".join(display)

def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(description='通用任务结果推送器')
    
    # 数据输入方式
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument('--data', type=str, default='',
                           help='任务数据（JSON字符串或文件路径）')
    input_group.add_argument('--name', type=str,
                           help='任务名称（与--content一起使用）')
    
    # 其他参数
    parser.add_argument('--content', type=str,
                       help='任务内容（markdown格式，与--name一起使用）')
    parser.add_argument('--result', type=str, default='任务已完成',
                       help='任务执行结果，默认"任务已完成"')
    parser.add_argument('--schedule-id', type=str,
                       help='周期性任务ID，对于周期性任务此ID需要保持一致')
    # 注意：云端会自动获取授权码，不再需要auth-code参数
    
    parser.add_argument('--config', type=str,
                       help='配置文件路径')
    parser.add_argument('--dry-run', action='store_true',
                       help='试运行，不实际推送')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='详细输出')
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    logger.info("=" * 60)
    logger.info("通用任务结果推送器")
    logger.info(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        # 注意：云端会自动获取授权码，不再需要授权码检测和更新逻辑
        
        # 1. 准备任务数据
        task_data = {}
        
        if args.data and args.data.strip():  # 只有提供了非空的data参数才处理
            # 从文件或JSON字符串加载
            task_data = load_task_data(args.data)
        elif args.name and args.content:
            # 从命令行参数构建
            task_data = {
                'task_name': args.name,
                'task_content': args.content,
                'task_result': args.result
            }
            
            if args.schedule_id:
                task_data['schedule_task_id'] = args.schedule_id
            # 注意：云端会自动获取授权码，不再需要auth_code字段
        else:
            logger.error("必须提供--data或--name+--content参数")
            sys.exit(1)
        
        # 2. 数据验证
        logger.info("验证任务数据...")
        is_valid, validation_msg = validate_task_data(task_data)
        if not is_valid:
            logger.error(f"数据验证失败: {validation_msg}")
            sys.exit(1)
        logger.info(f"{validation_msg}")
        
        # 3. 显示任务信息
        logger.info("任务信息:")
        print(format_for_display(task_data))
        
        # 4. 初始化推送器
        pusher = TaskPusher(args.config)
        
        # 5. 试运行检查
        if args.dry_run:
            logger.info("试运行模式，不实际推送")
            logger.info("推送数据预览:")
            
            # 显示格式化后的数据
            formatted_data = pusher.format_task_data(task_data)
            print(json.dumps(formatted_data, ensure_ascii=False, indent=2))
            
            logger.info("试运行完成，数据验证通过")
            sys.exit(0)
        
        # 6. 执行推送
        logger.info("开始负一屏推送...")
        result = pusher.push(task_data)
        
        # 7. 获取更新检查信息
        update_info = get_update_check_info()
        
        # 8. 将更新信息添加到结果中
        result["update_check"] = update_info
        
        # 9. 生成显示消息
        display_message = generate_display_message(result, update_info)
        result["display_message"] = display_message
        
        # 10. 输出结果
        print("\n" + "=" * 60)
        print("推送结果")
        print("=" * 60)
        
        # 显示格式化消息
        if "display_message" in result:
            print(result["display_message"])
            print("-" * 40)
        
        # 显示完整结果
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # 11. 根据结果设置退出码
        if result.get('success', False):
            logger.info("[SUCCESS] 任务推送完成!")
            sys.exit(0)
        else:
            logger.error("[ERROR] 任务推送失败!")
            sys.exit(1)
            
    except ValueError as e:
        logger.error(f"数据错误: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"执行失败: {str(e)}")
        
        # 尝试从task_data中获取task_id（如果存在）
        task_id = None
        try:
            if 'task_data' in locals():
                task_id = task_data.get('task_id') or task_data.get('schedule_task_id')
        except:
            pass
        
        error_result = {
            "success": False,
            "message": f"执行失败: {str(e)}",
            "task_id": task_id,  # 添加task_id字段
            "push_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 检查是否是授权码相关的错误
        error_str = str(e).lower()
        if 'authcode' in error_str or 'authorization' in error_str or '0000900034' in error_str:
            error_result['suggestion'] = "请您到负一屏 -> 我的页 -> 动态管理 -> 关联账号 -> 点击Claw智能体去获取授权码"
            error_result['error_type'] = 'auth'
        else:
            error_result['error_type'] = 'system'
        
        # 添加更新检查信息
        update_info = get_update_check_info()
        error_result["update_check"] = update_info
        
        # 生成显示消息
        display_message = generate_display_message(error_result, update_info)
        error_result["display_message"] = display_message
        
        print("\n执行失败:")
        
        # 显示格式化消息
        if "display_message" in error_result:
            print(error_result["display_message"])
            print("-" * 40)
        
        # 显示完整结果
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        sys.exit(1)

def get_update_check_info():
    """
    获取更新检查信息
    返回: dict 包含更新检查状态和信息
    """
    if not update_checker_available:
        # 模块不存在，跳过更新检查
        return {
            "status": "module_not_found",
            "message": "更新检查模块未找到，跳过检查",
            "should_notify": False
        }
    
    try:
        # 执行更新检查
        update_result = check_update()
        
        if update_result is None:
            # 这里需要区分：是配置未开启/时间间隔未满足，还是真正的检查异常？
            # 由于check_update()返回None时打印了"[信息] 更新检查异常，请稍后重试"
            # 我们可以假设这是检查异常
            return {
                "status": "check_error",
                "message": "更新检查异常，无法从ClawHub获取版本信息",
                "should_notify": True  # 异常时提示用户
            }
        elif update_result is False:
            # 已是最新版本
            return {
                "status": "up_to_date", 
                "message": "已是最新版本",
                "should_notify": False
            }
        elif update_result is True:
            # 有更新可用
            return {
                "status": "update_available",
                "message": "发现新版本可用",
                "should_notify": True,
                "update_command": "clawhub update today-task"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"更新检查异常: {str(e)}",
            "should_notify": True  # 异常时也提示
        }

def generate_display_message(push_result, update_info):
    """
    根据SKILL.md格式生成显示消息
    """
    base_message = ""
    
    if push_result.get('success', False):
        base_message = "任务推送成功！\n"
    else:
        base_message = "任务推送失败！\n"
        base_message += f"{push_result.get('message', '')}\n"
        return base_message
    
    # 根据更新检查状态添加信息
    update_status = update_info.get("status", "")
    
    if update_status == "module_not_found":
        # 模块不存在，按照SKILL.md不提示
        pass  # 不添加任何信息
    
    elif update_status == "update_available":
        # 有更新可用
        base_message += "\n技能更新检查：\n"
        base_message += f"发现新版本可用！\n"
        base_message += f"\n更新命令: `{update_info.get('update_command', 'clawhub update today-task')}`"
    
    elif update_status == "check_error" or update_status == "error":
        # 更新检查异常 - 按照SKILL.md应该提示用户
        base_message += f"\n更新检查异常：{update_info.get('message', '')}"
    
    elif update_status == "skipped_or_error":
        # 检查异常或不需要检查，按照SKILL.md不提示
        pass  # 不添加任何信息
    
    elif update_status == "up_to_date":
        # 已是最新版本，按照SKILL.md不提示
        pass  # 不添加任何信息
    
    return base_message

if __name__ == "__main__":
    main()