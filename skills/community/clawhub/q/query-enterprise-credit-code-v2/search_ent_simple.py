import requests
import json

# 配置参数 - 使用测试环境地址
config = {
    "host": "http://agent-data.ihdwork.com",
    "base_path": "/handi-ai",
    "endpoint": "/common-api/search-ent"
}

def search_ent(ent_name, count=10):
    """模糊查询企业列表"""
    # 构建完整URL
    url = f"{config['host']}{config['base_path']}{config['endpoint']}"
    
    print(f"=== 查询企业名称: {ent_name} (返回前{count}条) ===")
    
    params = {
        "ent_name": ent_name,
        "count": count
    }
    
    try:
        print(f"URL: {url}")
        print(f"查询参数: {params}")
        
        response = requests.get(url, params=params, timeout=10)
        
        print(f"状态码: {response.status_code}")
        print(f"响应文本: {response.text}")
        
        try:
            result = response.json()
            print("\n解析结果:")
            if isinstance(result, list):
                print(f"共 {len(result)} 条记录")
                for i, item in enumerate(result, 1):
                    print(f"{i}. 企业ID: {item.get('ent_id', 'N/A')}, 企业名称: {item.get('ent_name', 'N/A')}")
            else:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            return result
        except json.JSONDecodeError:
            print("响应不是JSON格式")
            return response.text
            
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return None

if __name__ == "__main__":
    # 直接测试，无需用户输入
    search_ent("小米", 10)