#!/usr/bin/env python3
"""
负一屏推送客户端
适配新的标准数据格式
"""

import json
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Tuple, Optional
from urllib.parse import urljoin

# 延迟导入requests，仅在需要时导入
try:
    import requests
    import urllib3
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("requests库未安装，网络功能将不可用")

logger = logging.getLogger(__name__)

class HiboardsClient:
    """Hiboards客户端（适配新格式）"""
    
    # 硬编码推送URL，不再支持配置
    BASE_URL = "https://lfhagmirror.hwcloudtest.cn:18449/celia-claw/v1/rest-api/skill/execute"
    
    def __init__(self, config):
        """初始化客户端"""
        self.config = config
        self.base_url = self.BASE_URL  # 使用硬编码的URL
        self.timeout = self.config.timeout
        
        # 检查requests库是否可用
        if not REQUESTS_AVAILABLE:
            logger.warning("requests库未安装，网络推送功能将不可用")
        
        # 配置默认请求头（必须使用ASCII字符）
        self.default_headers = {
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "OpenClaw-TaskPusher/2.0"
        }
        
        logger.info(f"Hiboards客户端初始化完成")
        logger.info(f"目标URL: {self.base_url} (硬编码)")
        logger.info(f"超时设置: {self.timeout}秒")

    def read_xiaoyienv(self, file_path):
        """
        读取 .xiaoyienv 文件并解析为键值对象

        Args:
            file_path: 文件路径

        Returns:
            dict: 解析后的属性对象
        """
        result = {}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 按行分割
            lines = content.split('\n')

            for line in lines:
                # 跳过空行或注释行（以 # 或 ! 开头的行）
                if not line or line.strip() == '' or line.strip().startswith('#') or line.strip().startswith('!'):
                    continue

                # 使用等号分割
                if '=' in line:
                    key, value = line.split('=', 1)
                    result[key.strip()] = value.strip()

            print('[OK] .xiaoyienv 文件解析成功')
        except Exception as err:
            print(f'[ERROR] 读取或解析 .xiaoyienv 文件失败：{err}')
            return {}

        return result

    def push(self, push_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """推送数据到负一屏"""
        url = self.base_url
        
        # 生成追踪ID
        trace_id = f"task-push-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        # 对接小艺 --- start
        # 读取并校验配置
        xiaoyi_path = "/home/sandbox/.openclaw/.xiaoyienv"
        config = self.read_xiaoyienv(xiaoyi_path)

        required_keys = ['PERSONAL-API-KEY', 'PERSONAL-UID']
        check_result = True

        for key in required_keys:
            if key in config:
                print(f'key "{key}" 存在：{config[key]}')
            else:
                print(f'key "{key}" 不存在：失败...')
                check_result = False

        if not check_result:
            return False, '缺少必填配置，PERSONAL-API-KEY或PERSONAL-UID配置'
        # 构建请求头
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'x-hag-trace-id': trace_id,
            'x-api-key': config['PERSONAL-API-KEY'],
            'x-request-from': 'openclaw',
            'x-uid': config['PERSONAL-UID'],
            'x-skill-id': 'hiboard_today_task',
            'x-prd-pkg-name': 'com.huawei.hag',
            "x-trace-id": trace_id
        }
        push_data['userId'] = config['PERSONAL-UID']
        push_data['appPackage'] = 'com.huawei.hag'
        # 对接小艺 --- end
        
        try:
            logger.info(f"发送数据到负一屏: {url}")
            logger.debug(f"请求头: {headers}")

            wrapped_data = push_data
            
            # 记录数据摘要（不记录完整内容）
            data_summary = self._get_data_summary(push_data)
            logger.debug(f"请求数据摘要: {data_summary}")
            
            # 发送请求
            # 使用json参数，requests会自动处理编码
            response = requests.post(
                url, 
                json=wrapped_data, 
                headers=headers, 
                stream=True,
                timeout=self.timeout
            )
            
            # 记录响应状态
            logger.info(f"[RECEIVE] 收到响应，状态码: {response.status_code}")
            
            # 检查HTTP状态码
            response.raise_for_status()
            
            # 解析响应
            try:
                result = response.json()
                logger.debug(f"响应数据: {json.dumps(result, ensure_ascii=False)[:500]}...")
            except json.JSONDecodeError:
                result = {"raw_response": response.text}
                logger.warning("响应不是有效的JSON格式")
            
            # 检查业务状态码
            success, message = self._check_business_status(result)
            
            if success:
                logger.info(f"[SUCCESS] 负一屏推送成功: {message}")
                return True, result
            else:
                logger.error(f"[ERROR] 负一屏业务错误: {message}")
                return False, message
                
        except requests.exceptions.Timeout:
            error_msg = f"请求超时 ({self.timeout}秒)"
            logger.error(f"[ERROR] {error_msg}")
            return False, error_msg
            
        except requests.exceptions.ConnectionError as e:
            error_msg = f"连接失败: {str(e)}"
            logger.error(f"[ERROR] {error_msg}")
            return False, error_msg
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP错误 ({response.status_code}): {str(e)}"
            logger.error(f"[ERROR] {error_msg}")
            
            # 尝试获取错误详情
            try:
                error_detail = response.json()
                error_msg = f"{error_msg} - {json.dumps(error_detail)}"
            except:
                error_msg = f"{error_msg} - {response.text[:200]}"
            
            return False, error_msg
            
        except Exception as e:
            error_msg = f"未知错误: {str(e)}"
            logger.error(f"[ERROR] {error_msg}")
            import traceback
            logger.error(f"[ERROR] 详细堆栈: {traceback.format_exc()}")
            return False, error_msg
    
    def _get_data_summary(self, push_data: Dict[str, Any]) -> Dict[str, Any]:
        """获取数据摘要（用于日志记录）"""
        summary = {
            "msg_count": len(push_data.get('msgContent', [])),
            "has_content": False
        }
        
        if push_data.get('msgContent'):
            first_msg = push_data['msgContent'][0]
            summary.update({
                "msg_id": first_msg.get('msgId', ''),
                "summary": first_msg.get('summary', ''),
                "result": first_msg.get('result', ''),
                "content_length": len(first_msg.get('content', ''))
            })
            summary["has_content"] = bool(first_msg.get('content'))
        
        return summary
    
    def _check_business_status(self, response: Dict[str, Any]) -> Tuple[bool, str]:
        """检查业务状态码"""
        # 检查常见的成功状态码
        success_codes = ['0000000000', '0', 0, '200', 200, 'success', 'SUCCESS']
        
        # 优先检查code字段
        if 'code' in response:
            code = response['code']
            if str(code) in [str(sc) for sc in success_codes]:
                message = response.get('message', response.get('desc', '成功'))
                return True, message
            else:
                message = response.get('message', response.get('desc', f'错误代码: {code}'))
                
                # 根据错误码提供详细的用户提示
                detailed_message = self._get_detailed_error_message(str(code), message, response)
                return False, detailed_message
        
        # 检查status字段
        elif 'status' in response:
            status = response['status']
            if str(status) in [str(sc) for sc in success_codes]:
                message = response.get('message', '成功')
                return True, message
            else:
                message = response.get('message', f'错误状态: {status}')
                return False, message
        
        # 检查success字段
        elif 'success' in response:
            if response['success']:
                return True, response.get('message', '成功')
            else:
                message = response.get('message', '失败')
                return False, message
        
        # 如果没有明确的业务状态字段，但HTTP状态码是200，默认成功
        logger.warning("响应中没有找到业务状态字段，默认视为成功")
        return True, "成功"
    
    def _get_detailed_error_message(self, code: str, original_message: str, response: Dict[str, Any]) -> str:
        """获取详细的错误信息，包含用户友好的提示"""
        
        # 错误码映射表
        error_mappings = {
            # 授权码无效或未关联
            '0000900034': {
                'title': '授权码无效或未关联',
                'solution': '请您到负一屏 -> 我的页 -> 动态管理 -> 关联账号 -> 点击Claw智能体去获取授权码',
                'steps': [
                    '1. 从手机桌面右滑进入负一屏',
                    '2. 点击左上角头像',
                    '3. 进入"我的"页面，点击右上角设置图标',
                    '4. 选择"动态管理"',
                    '5. 点击"关联账号"',
                    '6. 找到"Claw智能体"并点击获取授权码'
                ]
            },
            
            # 负一屏云推送到服务动态云有报错
            '0200100004': {
                'title': '负一屏云推送服务异常',
                'solution': '请检查返回的desc字段获取具体错误信息',
                'steps': []
            }
        }
        
        # 构建基础错误信息
        error_info = f"错误代码: {code}\n错误描述: {original_message}"
        
        # 检查是否有对应的错误码映射
        if code in error_mappings:
            mapping = error_mappings[code]
            error_info += f"\n\n[问题分析] {mapping['title']}"
            
            # 特殊处理0200100004错误码
            if code == '0200100004':
                desc = response.get('desc', '')
                if 'Receive error code' in desc:
                    # 提取CP错误码
                    import re
                    cp_error_match = re.search(r'Receive error code (\d+) from CP', desc)
                    if cp_error_match:
                        cp_error_code = cp_error_match.group(1)
                        error_info += f"\nCP错误码: {cp_error_code}"
                        
                        # 根据CP错误码提供具体建议
                        cp_error_suggestions = {
                            '82600017': {
                                'title': '设备未联网或未登录华为账号',
                                'solution': '请确保设备网络连接正常，并已登录华为账号',
                                'steps': [
                                    '1. 检查设备Wi-Fi或移动数据是否已连接',
                                    '2. 打开"设置"应用',
                                    '3. 进入"华为账号"或"帐号中心"',
                                    '4. 确保已登录华为账号',
                                    '5. 如未登录，请使用华为账号登录'
                                ]
                            },
                            '82600013': {
                                'title': '服务动态推送开关已关闭',
                                'solution': '请打开服务动态推送开关',
                                'steps': [
                                    '1. 从手机桌面右滑进入负一屏',
                                    '2. 点击左上角头像',
                                    '3. 进入"我的"页面，点击右上角设置图标',
                                    '4. 选择"动态管理"',
                                    '5. 找到"AI任务完成通知"',
                                    '6. 打开"场景开关"和"服务提供方开关"'
                                ]
                            },
                            '82600005': {
                                'title': '服务动态云服务异常',
                                'solution': '服务动态云服务暂时不可用，请稍后重试',
                                'steps': [
                                    '1. 等待几分钟后重试',
                                    '2. 如问题持续，可能是服务端维护',
                                    '3. 可稍后再试或联系技术支持'
                                ]
                            }
                        }
                        
                        if cp_error_code in cp_error_suggestions:
                            cp_info = cp_error_suggestions[cp_error_code]
                            error_info += f"\n\n[具体问题] {cp_info['title']}"
                            error_info += f"\n[解决方案] {cp_info['solution']}"
                            if cp_info['steps']:
                                error_info += "\n\n[操作步骤]"
                                for step in cp_info['steps']:
                                    error_info += f"\n{step}"
                        else:
                            error_info += f"\n\n[注意] 未知的CP错误码，请检查网络连接或稍后重试"
            
            # 添加通用解决方案
            if mapping['solution']:
                error_info += f"\n\n[解决方案] {mapping['solution']}"
            
            # 添加操作步骤
            if mapping['steps']:
                error_info += "\n\n[操作步骤]"
                for step in mapping['steps']:
                    error_info += f"\n{step}"
        
        else:
            # 未知错误码的通用建议
            error_info += "\n\n[通用建议]"
            error_info += "\n1. 检查网络连接是否正常"
            error_info += "\n2. 确认授权码是否正确"
            error_info += "\n3. 稍后重试"
            error_info += "\n4. 如问题持续，请联系技术支持"
        
        # 添加技术支持信息
        error_info += "\n\n[技术支持]"
        error_info += "\n- 如问题无法解决，请记录错误代码并提供给技术支持"
        error_info += "\n- 错误发生时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return error_info
    
    def test_connection(self) -> Tuple[bool, str]:
        """测试连接"""
        try:
            # 发送一个简单的测试请求
            test_data = {
                "authCode": self.config.auth_code or "test",
                "msgContent": [
                    {
                        "msgId": "test_connection",
                        "scheduleTaskId": "test_connection",
                        "summary": "连接测试",
                        "result": "测试中",
                        "content": "# 连接测试\n\n这是一个连接测试消息。"
                    }
                ]
            }
            
            success, result = self.push(test_data)
            if success:
                return True, "连接测试成功"
            else:
                return False, f"连接测试失败: {result}"
                
        except Exception as e:
            return False, f"连接测试异常: {str(e)}"
    
    def get_status(self) -> Dict[str, Any]:
        """获取服务状态"""
        try:
            # 尝试访问状态端点（如果存在）
            status_url = self.base_url.replace('/upload', '/status')
            
            response = requests.get(status_url, verify=True, timeout=10)
            response.raise_for_status()
            
            return response.json()
        except:
            # 如果状态端点不存在，返回基本状态
            return {
                "status": "unknown",
                "message": "无法获取详细状态",
                "url": self.base_url,
                "config_loaded": bool(self.config.auth_code)
            }

# 简化的客户端（用于模块导入失败时）
class SimpleHiboardsClient:
    """简化版Hiboards客户端"""
    
    def __init__(self, config):
        self.base_url = config.hiboards_url
        self.timeout = config.timeout
    
    def push(self, push_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """简化版推送"""
        import requests
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        url = self.base_url
        headers = {
            "Content-Type": "application/json",
            "x-trace-id": f"simple-push-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }
        
        try:
            response = requests.post(url, json=push_data, headers=headers, verify=True, timeout=self.timeout)
            response.raise_for_status()
            
            result = response.json()
            
            # 检查状态码
            if "code" in result:
                code = result["code"]
                if code == '0000000000' or code == '0' or code == 0:
                    return True, result
                else:
                    error_msg = result.get("message", result.get("desc", "未知错误"))
                    return False, f"错误: {error_msg} (code: {code})"
            
            return True, result
            
        except Exception as e:
            return False, f"推送失败: {str(e)}"

# 测试代码
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.DEBUG)
    
    # 测试配置
    class TestConfig:
        def __init__(self):
            self.hiboards_url = "https://lfhagmirror.hwcloudtest.cn:18449/celia-claw/v1/sse-api/skill/execute"
            self.timeout = 10
            self.auth_code = "test_auth_code"
    
    # 测试客户端
    config = TestConfig()
    client = HiboardsClient(config)
    
    # 测试数据
    test_data = {
        "authCode": "test_auth_code",
        "msgContent": [
            {
                "msgId": "test_123",
                "scheduleTaskId": "test_123",
                "summary": "测试任务",
                "result": "测试完成",
                "content": "# 测试任务\n\n这是一个测试任务。"
            }
        ]
    }
    
    print("测试Hiboards客户端...")
    print(f"URL: {config.hiboards_url}")
    print(f"原始测试数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
    
    # 显示实际发送的数据结构
    print(f"\n实际发送的数据结构:")
    wrapped_data = {"data": test_data}
    print(json.dumps(wrapped_data, ensure_ascii=False, indent=2))
    
    print(f"\n完整请求URL: {config.hiboards_url}")
    print("注意: 由于是测试代码，不实际发送请求")