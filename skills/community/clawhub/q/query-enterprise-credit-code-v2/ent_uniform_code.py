import requests
import json

# 配置参数（保持与之前脚本相同的host和base_path）
config = {
    "host": "http://agent-data.ihdwork.com",
    "base_path": "/handi-ai",
    "endpoint": "/ent-analysis/uniform-code"
}

def get_uniform_code(ent_id):
    """获取企业统一社会信用代码
    
    Args:
        ent_id (str): 企业ID（必须）
        
    Returns:
        dict: 包含统一社会信用代码信息的字典
    """
    # 构建完整URL
    url = f"{config['host']}{config['base_path']}{config['endpoint']}"
    
    # 构建请求头
    headers = {
        "Content-Type": "application/json"
    }
    
    # 构建请求体
    payload = {
        "ent_id": ent_id
    }
    
    try:
        print(f"=== 查询企业统一社会信用代码 (企业ID: {ent_id}) ===")
        print(f"URL: {url}")
        print(f"请求头: {headers}")
        print(f"请求体: {json.dumps(payload, ensure_ascii=False)}")
        
        # 发送POST请求
        response = requests.post(
            url=url,
            headers=headers,
            data=json.dumps(payload, ensure_ascii=False),
            timeout=10
        )
        
        print(f"\n状态码: {response.status_code}")
        print(f"响应文本: {response.text}")
        
        # 尝试解析JSON
        try:
            result = response.json()
            print("\n解析后的JSON响应:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
            # 处理返回的数据（可能是直接的字符串或包含在对象中）
            return {
                'data': result,
                'success': True
            }
                
        except json.JSONDecodeError:
            # 响应可能是直接的字符串
            print("响应是直接的字符串格式")
            return {
                'data': response.text.strip(),
                'success': True
            }
            
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return {
            'error': str(e),
            'success': False
        }

def print_uniform_code(result):
    """格式化打印企业统一社会信用代码"""
    if not result.get('success'):
        print("请求未成功")
        return
    
    data = result.get('data')
    if not data:
        print("未获取到统一社会信用代码")
        return
    
    print("\n" + "="*50)
    print("企业统一社会信用代码")
    print("="*50)
    
    # 处理不同类型的返回数据
    if isinstance(data, str):
        # 直接是字符串
        print(f"统一社会信用代码: {data}")
    elif isinstance(data, dict):
        # 包含在对象中
        # 尝试从常见字段中提取
        code = data.get('uniform_code') or data.get('code') or data.get('result') or data
        print(f"统一社会信用代码: {code}")
    else:
        # 其他类型数据
        print(f"统一社会信用代码: {data}")

if __name__ == "__main__":
    # 示例调用：查询企业统一社会信用代码
    test_ent_id = "7xMIsl4IxuG3"  # 企业ID（字符串类型）
    
    # 查询企业统一社会信用代码
    result = get_uniform_code(test_ent_id)
    
    # 打印统一社会信用代码
    if result.get('success'):
        print_uniform_code(result)
    else:
        print("\n查询失败")
        if 'error' in result:
            print(f"错误信息: {result['error']}")
