import os
import requests
from typing import List, Optional, Dict, Any

# 飞书 API 基础配置
FEISHU_API_BASE = "https://open.feishu.cn/open-apis"

def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    """获取飞书 Tenant Access Token"""
    url = f"{FEISHU_API_BASE}/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get('code') != 0:
            raise Exception(f"Feishu Auth Failed: {data.get('msg')}")
        
        return data['tenant_access_token']
    except Exception as e:
        raise Exception(f"Network or Auth Error: {str(e)}")

def submit_to_feishu(
    name: str,
    phone: str,
    destination: str,
    people_count: int,
    departure_date: Optional[str] = "",
    budget: Optional[float] = 0.0,
    preferences: Optional[List[str]] = None,
    special_requirements: Optional[str] = ""
) -> Dict[str, Any]:
    """
    ClawHub 工具函数：将旅游需求提交到飞书多维表格
    此函数名将直接被 SKILL.md 中的定义引用
    """
    # 从环境变量读取配置
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    base_token = os.getenv("FEISHU_BASE_TOKEN")
    table_id = os.getenv("FEISHU_TABLE_ID")

    # 校验配置
    missing_configs = []
    if not app_id: missing_configs.append("FEISHU_APP_ID")
    if not app_secret: missing_configs.append("FEISHU_APP_SECRET")
    if not base_token: missing_configs.append("FEISHU_BASE_TOKEN")
    if not table_id: missing_configs.append("FEISHU_TABLE_ID")
    
    if missing_configs:
        return {
            "status": "error", 
            "message": f"技能配置缺失，请联系管理员配置: {', '.join(missing_configs)}"
        }

    try:
        # 1. 获取 Token
        token = get_tenant_access_token(app_id, app_secret)
        
        # 2. 构建字段映射 (必须与飞书表格列名严格一致)
        fields = {
            "姓名": name,
            "联系电话": phone,
            "意向目的地": destination,
            "出行人数": people_count
        }
        
        if departure_date:
            fields["预计出发日期"] = departure_date
        
        if budget and budget > 0:
            fields["人均预算"] = budget
            
        if preferences and len(preferences) > 0:
            fields["行程偏好"] = preferences
            
        if special_requirements:
            fields["特殊需求"] = special_requirements

        # 3. 调用飞书新增记录 API
        url = f"{FEISHU_API_BASE}/bitable/v1/apps/{base_token}/tables/{table_id}/records"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "records": [{"fields": fields}]
        }
        
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        
        if result.get('code') == 0:
            return {"status": "success", "message": "需求已成功提交至飞书表格！"}
        else:
            return {"status": "error", "message": f"飞书 API 错误: {result.get('msg')}"}

    except Exception as e:
        return {"status": "error", "message": f"系统异常: {str(e)}"}

if __name__ == "__main__":
    # 本地调试用
    print("Tools module loaded successfully.")