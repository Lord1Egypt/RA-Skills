#!/usr/bin/env python3
"""
飞书多维表格客户端
处理飞书 API 认证和表格操作
"""

import json
import logging
import aiohttp
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime


class FeishuClient:
    """飞书 API 客户端"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.feishu_config = config.get("feishu", {})
        self.table_config = config.get("table", {})
        self.export_config = config.get("export", {})
        
        # API 端点
        self.base_url = "https://open.feishu.cn/open-apis"
        self.access_token = None
        self.token_expire_time = None
        
        self.logger = logging.getLogger(__name__)
    
    async def initialize(self) -> bool:
        """初始化飞书客户端"""
        try:
            # 获取访问令牌
            success = await self.get_access_token()
            if not success:
                self.logger.error("获取飞书访问令牌失败")
                return False
            
            # 验证表格访问权限
            if not await self.verify_table_access():
                self.logger.error("无法访问飞书多维表格")
                return False
            
            self.logger.info("飞书客户端初始化成功")
            return True
            
        except Exception as e:
            self.logger.error(f"飞书客户端初始化失败: {str(e)}", exc_info=True)
            return False
    
    async def get_access_token(self) -> bool:
        """获取飞书访问令牌"""
        try:
            app_id = self.feishu_config.get("app_id")
            app_secret = self.feishu_config.get("app_secret")
            tenant_access_token = self.feishu_config.get("tenant_access_token")
            
            # 如果已经提供了 tenant_access_token，直接使用
            if tenant_access_token and tenant_access_token != "YOUR_TENANT_ACCESS_TOKEN":
                self.access_token = tenant_access_token
                self.logger.info("使用提供的 tenant_access_token")
                return True
            
            # 否则使用 app_id 和 app_secret 获取
            if not app_id or not app_secret:
                self.logger.error("缺少 app_id 或 app_secret")
                return False
            
            url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
            headers = {"Content-Type": "application/json"}
            data = {
                "app_id": app_id,
                "app_secret": app_secret
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get("code") == 0:
                            self.access_token = result.get("tenant_access_token")
                            expire_time = result.get("expire", 7200)
                            self.token_expire_time = datetime.now().timestamp() + expire_time
                            self.logger.info("成功获取飞书访问令牌")
                            return True
                        else:
                            self.logger.error(f"获取令牌失败: {result}")
                    else:
                        self.logger.error(f"HTTP 错误: {response.status}")
            
            return False
            
        except Exception as e:
            self.logger.error(f"获取访问令牌失败: {str(e)}", exc_info=True)
            return False
    
    async def verify_table_access(self) -> bool:
        """验证表格访问权限"""
        try:
            app_token = self.feishu_config.get("table_app_token")
            table_token = self.feishu_config.get("table_token")
            
            if not app_token or not table_token:
                self.logger.error("缺少表格 app_token 或 table_token")
                return False
            
            url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_token}/records"
            headers = self._get_auth_headers()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params={"page_size": 1}) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get("code") == 0:
                            self.logger.info("表格访问验证成功")
                            return True
                        else:
                            self.logger.error(f"表格访问验证失败: {result}")
                    else:
                        self.logger.error(f"HTTP 错误: {response.status}")
            
            return False
            
        except Exception as e:
            self.logger.error(f"验证表格访问权限失败: {str(e)}", exc_info=True)
            return False
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """获取认证头"""
        if not self.access_token:
            raise Exception("访问令牌未初始化")
        
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    async def batch_add_records(self, records: List[Dict[str, Any]]) -> bool:
        """批量添加记录到表格"""
        try:
            app_token = self.feishu_config.get("table_app_token")
            table_token = self.feishu_config.get("table_token")
            
            if not app_token or not table_token:
                self.logger.error("缺少表格 app_token 或 table_token")
                return False
            
            url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_token}/records/batch_create"
            headers = self._get_auth_headers()
            
            # 格式化记录数据
            formatted_records = []
            for record in records:
                # 根据表格字段结构格式化
                fields = self._format_record_fields(record)
                formatted_records.append({
                    "fields": fields
                })
            
            # 分批处理，避免单次请求过大
            batch_size = 100
            success_count = 0
            
            for i in range(0, len(formatted_records), batch_size):
                batch = formatted_records[i:i+batch_size]
                
                data = {
                    "records": batch
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=data) as response:
                        if response.status == 200:
                            result = await response.json()
                            if result.get("code") == 0:
                                success_count += len(batch)
                                self.logger.info(f"成功添加 {len(batch)} 条记录")
                            else:
                                self.logger.error(f"添加记录失败: {result}")
                                return False
                        else:
                            self.logger.error(f"HTTP 错误: {response.status}")
                            return False
            
            self.logger.info(f"成功添加总计 {success_count} 条记录")
            return True
            
        except Exception as e:
            self.logger.error(f"批量添加记录失败: {str(e)}", exc_info=True)
            return False
    
    def _format_record_fields(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """格式化记录字段为飞书表格格式"""
        fields = {}
        
        # 获取表格字段映射
        table_fields = self.table_config.get("fields", [])
        field_mapping = {field["field_name"]: field for field in table_fields}
        
        # 根据字段类型格式化数据
        for field_name, field_config in field_mapping.items():
            value = record.get(field_name, "")
            field_type = field_config.get("type", 1)  # 默认为文本类型
            
            if field_type == 1:  # 文本类型
                fields[field_name] = str(value) if value else ""
            elif field_type == 3:  # 单选
                fields[field_name] = {"text": str(value)} if value else {"text": ""}
            elif field_type == 5:  # 日期时间
                # 尝试解析日期时间
                try:
                    if isinstance(value, str):
                        # ISO 格式时间戳
                        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                        fields[field_name] = int(dt.timestamp() * 1000)  # 毫秒时间戳
                    elif isinstance(value, (int, float)):
                        # 已经是时间戳
                        fields[field_name] = int(value * 1000) if value < 1000000000000 else int(value)
                    else:
                        fields[field_name] = int(datetime.now().timestamp() * 1000)
                except Exception:
                    fields[field_name] = int(datetime.now().timestamp() * 1000)
            else:
                fields[field_name] = str(value) if value else ""
        
        return fields
    
    async def get_table_info(self) -> Optional[Dict[str, Any]]:
        """获取表格信息"""
        try:
            app_token = self.feishu_config.get("table_app_token")
            table_token = self.feishu_config.get("table_token")
            
            if not app_token or not table_token:
                self.logger.error("缺少表格 app_token 或 table_token")
                return None
            
            url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_token}"
            headers = self._get_auth_headers()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get("code") == 0:
                            return result.get("data", {}).get("table", {})
                        else:
                            self.logger.error(f"获取表格信息失败: {result}")
                    else:
                        self.logger.error(f"HTTP 错误: {response.status}")
            
            return None
            
        except Exception as e:
            self.logger.error(f"获取表格信息失败: {str(e)}", exc_info=True)
            return None
    
    async def list_records(self, page_size: int = 100, page_token: str = None) -> Optional[Dict[str, Any]]:
        """列出表格记录"""
        try:
            app_token = self.feishu_config.get("table_app_token")
            table_token = self.feishu_config.get("table_token")
            
            if not app_token or not table_token:
                self.logger.error("缺少表格 app_token 或 table_token")
                return None
            
            url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_token}/records"
            headers = self._get_auth_headers()
            
            params = {"page_size": page_size}
            if page_token:
                params["page_token"] = page_token
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get("code") == 0:
                            return result.get("data", {})
                        else:
                            self.logger.error(f"列出记录失败: {result}")
                    else:
                        self.logger.error(f"HTTP 错误: {response.status}")
            
            return None
            
        except Exception as e:
            self.logger.error(f"列出记录失败: {str(e)}", exc_info=True)
            return None
    
    async def cleanup(self):
        """清理资源"""
        # 飞书客户端不需要特殊清理
        pass
    
    async def test_connection(self) -> bool:
        """测试连接"""
        try:
            # 测试令牌有效性
            if not await self.get_access_token():
                return False
            
            # 测试表格访问
            if not await self.verify_table_access():
                return False
            
            self.logger.info("飞书连接测试成功")
            return True
            
        except Exception as e:
            self.logger.error(f"飞书连接测试失败: {str(e)}")
            return False