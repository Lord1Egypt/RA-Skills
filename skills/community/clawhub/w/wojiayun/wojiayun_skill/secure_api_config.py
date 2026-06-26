"""
安全 API 配置管理器
加密存储 base_url 和 API 接口信息
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional

try:
    # 作为包的一部分导入
    from .crypto_utils import encrypt_value, decrypt_value
except ImportError:
    # 独立运行时导入
    from crypto_utils import encrypt_value, decrypt_value


class SecureAPIConfig:
    """安全 API 配置管理器"""
    
    # 配置文件路径
    CONFIG_FILE = "e:\\workbuddy\\wy\\.secure_api_config"
    
    # 默认 API 配置（加密前）
    DEFAULT_CONFIG = {
        "base_url": "https://wy.wojiacloud.com",
        "endpoints": {
            "token_refresh": "/thirdUser/apiKeyAuth",
            "get_equipments": "/equipments/getAllEquipMents",
            "get_equipment_detail": "/equipments/getEquipMentDetail",
            "create_equipment": "/equipments/createEquipMent",
            "update_equipment": "/equipments/updateEquipMent",
            "delete_equipment": "/equipments/deleteEquipMent",
            "get_public_area_paging": "/publicArea/getPublicAreaPaging",
            "get_current_user_info": "/users/getCurrentUserInfo",
            "get_projects": "/projects/getProjectsByUserIDAndName",
            "set_default_project": "/employees/setDefaultProject",
            "get_equip_ins_list": "/equipIns/selectAllEquipInsEntryList",
            "get_device_maintain_list": "/equMaiPlanEntrys/getDeviceViewList",
            "upload_files": "/api/file/uploadFiles",
            "get_work_type": "/workorders/getWorkType",
            "search_rooms": "/rooms/getRoomsByBuildInfoV3",
            "get_room_customers": "/workorders/getAllCustomerByRoomId",
            "create_workorder": "/workorders/insertWorkorder",
            "get_pending_workorders": "/workCustomer/getWoprocessPagingList",
            "get_my_workorders": "/workorders/getAllWorkorder",
            "query_workorders": "/workCustomer/getWoprocessPagingList",
            "get_equipment_repairs": "/equMaintenance/pageEquMaintenanceList",
        },
        "api_version": "v1",
        "timeout": 30,
    }
    
    # API 白名单（只允许调用的接口，不可修改）
    _WHITELIST = (
        "get_equipments",
        "get_equipment_detail",
        "get_public_area_paging",
        "get_current_user_info",
        "get_projects",
        "set_default_project",
        "get_equip_ins_list",
        "get_device_maintain_list",
        "upload_files",
        "get_work_type",
        "search_rooms",
        "get_room_customers",
        "create_workorder",
        "get_pending_workorders",
        "get_my_workorders",
        "query_workorders",
        "get_equipment_repairs",
    )
    
    # 黑名单（明确禁止的接口，不可修改）
    _BLACKLIST = (
        "create_equipment",    # 创建设备
        "update_equipment",    # 更新设备
        "delete_equipment",    # 删除设备
    )
    
    def __init__(self):
        """初始化配置管理器"""
        self._config = {}
        self._load_config()
    
    def _load_config(self):
        """从文件加载配置"""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
            except:
                self._config = {}
        
        # 如果没有配置，初始化默认值
        if not self._config:
            self._init_default_config()
    
    def _save_config(self):
        """保存配置到文件"""
        with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, ensure_ascii=False, indent=2)
    
    def _init_default_config(self):
        """初始化默认配置（加密存储）"""
        # 静默初始化，不打印敏感信息
        for key, value in self.DEFAULT_CONFIG.items():
            if isinstance(value, dict):
                # 嵌套字典逐个加密
                encrypted_value = {}
                for k, v in value.items():
                    encrypted_value[k] = encrypt_value(str(v))
            else:
                encrypted_value = encrypt_value(str(value))
            
            self._config[key] = {
                "encrypted": encrypted_value,
                "created_at": datetime.now().isoformat(),
            }
        
        self._save_config()
    
    def get_base_url(self) -> str:
        """
        获取 base_url（自动解密）
        
        Returns:
            解密后的 base_url
        """
        if "base_url" not in self._config:
            return ""
        
        try:
            encrypted = self._config["base_url"]["encrypted"]
            return decrypt_value(encrypted)
        except Exception as e:
            print(f"解密 base_url 失败: {e}")
            return ""
    
    def get_endpoint(self, name: str) -> str:
        """
        获取 API 端点（自动解密）
        
        Args:
            name: 端点名称
            
        Returns:
            解密后的端点路径
        """
        if "endpoints" not in self._config:
            return ""
        
        try:
            encrypted_dict = self._config["endpoints"]["encrypted"]
            if name in encrypted_dict:
                return decrypt_value(encrypted_dict[name])
            return ""
        except Exception as e:
            print(f"解密端点失败: {e}")
            return ""
    
    def get_full_url(self, endpoint_name: str) -> str:
        """
        获取完整 API URL（自动解密组合）
        
        Args:
            endpoint_name: 端点名称
            
        Returns:
            完整的 API URL
        """
        base_url = self.get_base_url()
        endpoint = self.get_endpoint(endpoint_name)
        
        if not base_url or not endpoint:
            return ""
        
        return f"{base_url}{endpoint}"
    
    def get_config(self, key: str) -> str:
        """
        获取配置项（自动解密）
        
        Args:
            key: 配置项名称
            
        Returns:
            解密后的配置值
        """
        if key not in self._config:
            return ""
        
        try:
            encrypted = self._config[key]["encrypted"]
            if isinstance(encrypted, dict):
                # 如果是字典，不解密（端点需要单独获取）
                return "***ENCRYPTED_DICT***"
            return decrypt_value(encrypted)
        except Exception as e:
            print(f"解密配置失败: {e}")
            return ""
    
    def update_base_url(self, new_url: str):
        """
        更新 base_url（自动加密）
        
        Args:
            new_url: 新的 base_url
        """
        encrypted = encrypt_value(new_url)
        self._config["base_url"] = {
            "encrypted": encrypted,
            "updated_at": datetime.now().isoformat(),
        }
        self._save_config()
        print("✓ base_url 已更新")
    
    def list_endpoints(self) -> list:
        """
        列出所有端点名称（不显示实际路径）
        
        Returns:
            端点名称列表
        """
        if "endpoints" not in self._config:
            return []
        
        try:
            encrypted_dict = self._config["endpoints"]["encrypted"]
            return list(encrypted_dict.keys())
        except:
            return []
    
    def get_config_info(self) -> dict:
        """
        获取配置信息（不含实际值）
        
        Returns:
            配置元信息
        """
        info = {}
        for key in self._config.keys():
            if key == "endpoints":
                info[key] = {
                    "count": len(self.list_endpoints()),
                    "names": self.list_endpoints(),
                    "status": "***已加密***"
                }
            else:
                info[key] = {
                    "status": "***已加密***",
                    "updated_at": self._config[key].get("updated_at", "N/A")
                }
        return info
    
    def reset_to_default(self):
        """重置为默认配置"""
        self._config = {}
        self._init_default_config()
    
    # ==================== 白名单管理 ====================
    
    def is_endpoint_allowed(self, endpoint_name: str) -> tuple:
        """
        检查端点是否在白名单中
        
        Args:
            endpoint_name: 端点名称
            
        Returns:
            (是否允许, 拒绝原因)
        """
        # 检查是否在黑名单中
        if endpoint_name in self._BLACKLIST:
            return False, f"接口 '{endpoint_name}' 在黑名单中，禁止调用（防止越权）"
        
        # 检查是否在白名单中
        if endpoint_name not in self._WHITELIST:
            return False, f"接口 '{endpoint_name}' 不在白名单中，无权调用"
        
        return True, ""
    
    def get_whitelist(self) -> list:
        """
        获取白名单列表（只读）
        
        Returns:
            允许调用的接口列表（副本）
        """
        return list(self._WHITELIST)
    
    def get_blacklist(self) -> list:
        """
        获取黑名单列表（只读）
        
        Returns:
            禁止调用的接口列表（副本）
        """
        return list(self._BLACKLIST)


# 全局实例
_api_config = None


def get_api_config() -> SecureAPIConfig:
    """获取全局 API 配置实例"""
    global _api_config
    if _api_config is None:
        _api_config = SecureAPIConfig()
    return _api_config


# ==================== 安全的 API 客户端 ====================

class SecureAPIClient:
    """
    安全 API 客户端
    封装所有 API 调用，隐藏底层细节
    """
    
    def __init__(self):
        self.config = get_api_config()
        self._base_url = None
        self._endpoints = {}
        self._load_config()
    
    def _load_config(self):
        """加载配置（内部使用）"""
        # 解密并缓存配置（仅在内存中）
        self._base_url = self.config.get_base_url()
        
        # 加载所有端点
        for name in self.config.list_endpoints():
            self._endpoints[name] = self.config.get_endpoint(name)
    
    def call_api(self, endpoint_name: str, method: str = "GET", 
                 params: dict = None, data: dict = None, 
                 headers: dict = None, retry_on_token_expired: bool = True) -> dict:
        """
        调用 API（安全封装，带白名单校验和 Token 自动刷新）
        
        Args:
            endpoint_name: 端点名称
            method: HTTP 方法
            params: URL 参数
            data: 请求体数据
            headers: 请求头
            retry_on_token_expired: Token 失效时是否自动重试
            
        Returns:
            API 响应数据
        """
        import requests
        from .token_manager import get_token_manager
        
        # 1. 白名单权限校验
        is_allowed, reason = self.config.is_endpoint_allowed(endpoint_name)
        if not is_allowed:
            return {
                "error": "权限不足",
                "message": reason,
                "code": "FORBIDDEN"
            }
        
        # 2. 构建完整 URL（内部解密，不暴露）
        url = self._build_url(endpoint_name, params)
        
        if not url:
            return {"error": "构建 URL 失败"}
        
        # 3. 调用 API
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=30)
            else:
                return {"error": f"不支持的 HTTP 方法: {method}"}
            
            result = response.json()
            
            # 4. 检测 Token 失效并自动刷新
            if retry_on_token_expired:
                tm = get_token_manager()
                if tm.is_token_expired_error(result):
                    # 获取 API Key 用于刷新 token
                    from .key_manager import get_api_key
                    api_key = get_api_key()
                    
                    if api_key:
                        # 刷新 token
                        success, message = tm.refresh_access_token(api_key, self._base_url)
                        
                        if success:
                            # 获取新 token 并重试
                            new_token = tm.get_access_token()
                            if new_token:
                                # 更新 headers 中的 token
                                if headers is None:
                                    headers = {}
                                headers["authorization"] = new_token
                                # 递归调用，但不允许再次重试（避免死循环）
                                return self.call_api(endpoint_name, method, params, data, headers, retry_on_token_expired=False)
                        else:
                            result["token_refresh_failed"] = message
                    else:
                        result["token_refresh_failed"] = "未找到 API Key"
            
            return result
            
        except Exception as e:
            return {"error": str(e)}
    
    def _build_url(self, endpoint_name: str, params: dict = None) -> str:
        """
        构建完整 URL（内部方法）
        
        Args:
            endpoint_name: 端点名称
            params: URL 参数
            
        Returns:
            完整 URL
        """
        if endpoint_name not in self._endpoints:
            return ""
        
        url = f"{self._base_url}{self._endpoints[endpoint_name]}"
        
        # 添加参数
        if params:
            import urllib.parse
            query = urllib.parse.urlencode(params)
            url = f"{url}?{query}"
        
        return url
    
    def get_equipments(self, current: int = 1, row_count: int = 10, 
                       auth_token: str = None) -> dict:
        """
        获取设备列表（安全封装）
        
        Args:
            current: 当前页
            row_count: 每页条数
            auth_token: 认证令牌
            
        Returns:
            设备数据
        """
        import random
        
        random_num = random.randint(1000000000000, 9999999999999)
        
        params = {
            "current": current,
            "rowCount": row_count,
            "searchPhrase": "",
            "random": random_num,
            "_": random_num,
        }
        
        headers = {
            "authorization": auth_token or "",
            "Content-Type": "application/json"
        }
        
        return self.call_api("get_equipments", "GET", params, headers=headers)
    
    def get_api_status(self) -> dict:
        """
        获取 API 状态（安全信息）
        
        Returns:
            API 状态信息（不含敏感数据）
        """
        return {
            "base_url": "***已加密***",
            "endpoints_count": len(self._endpoints),
            "endpoints": list(self._endpoints.keys()),
            "status": "已配置",
            "whitelist": self.config.get_whitelist(),
            "blacklist": self.config.get_blacklist(),
            "security": "白名单模式"
        }


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("安全 API 配置管理器测试")
    print("=" * 60)
    
    # 1. 初始化
    print("\n【1. 初始化 API 配置】")
    config = get_api_config()
    print(f"  配置项: {list(config._config.keys())}")
    
    # 2. 获取配置信息（不显示实际值）
    print("\n【2. 配置信息】")
    info = config.get_config_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # 3. 安全客户端测试
    print("\n【3. 安全 API 客户端】")
    client = SecureAPIClient()
    status = client.get_api_status()
    print(f"  API 状态: {status}")
    
    # 4. 验证 base_url 解密
    print("\n【4. 验证解密】")
    base_url = config.get_base_url()
    print(f"  base_url 长度: {len(base_url)}")
    print(f"  是否包含敏感信息: {'否' if '***' not in base_url else '是'}")
    
    # 5. 验证端点解密
    print("\n【5. 端点验证】")
    for name in config.list_endpoints()[:3]:
        endpoint = config.get_endpoint(name)
        print(f"  {name}: {'✓' if endpoint else '✗'}")
    
    # 6. 白名单测试
    print("\n【6. 白名单权限控制】")
    print(f"  白名单: {config.get_whitelist()}")
    print(f"  黑名单: {config.get_blacklist()}")
    
    # 测试允许调用的接口
    allowed, reason = config.is_endpoint_allowed("get_equipments")
    print(f"  get_equipments: {'✓ 允许' if allowed else '✗ 拒绝'} - {reason}")
    
    # 测试禁止调用的接口（黑名单）
    allowed, reason = config.is_endpoint_allowed("delete_equipment")
    print(f"  delete_equipment: {'✓ 允许' if allowed else '✗ 拒绝'} - {reason}")
    
    # 测试未授权的接口
    allowed, reason = config.is_endpoint_allowed("unknown_api")
    print(f"  unknown_api: {'✓ 允许' if allowed else '✗ 拒绝'} - {reason}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
