import requests
import re
import json

# API 配置
API_URL = "https://mi.earlydata.com/detail"
API_VERSION = "6.0"

# 检查依赖库
def check_dependencies():
    """检查必要的依赖库是否已安装，如果没有安装则抛出 ImportError"""
    required_packages = ["requests"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        raise ImportError(
            f"缺少必要的依赖库: {', '.join(missing_packages)}\n"
            f"请手动安装依赖库: pip install {' '.join(missing_packages)}"
        )

# 在导入时检查依赖（不自动安装）
check_dependencies()


def extract_item_id(item_url: str) -> str:
    """
    从淘宝/天猫商品链接中提取商品ID
    支持格式：
    - https://item.taobao.com/item.htm?id=123456789
    - https://detail.tmall.com/item.htm?id=123456789
    - 短链接等
    """
    if not item_url:
        return None
    
    # 匹配 id= 后的数字
    patterns = [
        r'[?&]id=(\d+)',           # 标准链接
        r'[?&]itemId=(\d+)',       # 部分变体
        r'/item/(\d+)',            # 短链接格式
    ]
    
    for pattern in patterns:
        match = re.search(pattern, item_url)
        if match:
            return match.group(1)
    
    # 若链接本身就是纯数字ID
    if item_url.strip().isdigit():
        return item_url.strip()
    
    return None


def get_tb_detail(item_id: str = None, item_url: str = None) -> str:
    """
    查询淘宝/天猫商品详情
    
    本函数通过调用第三方API服务提供商 EarlyData (mi.earlydata.com) 获取商品月销量数据。
    
    参数：
    item_id: 商品ID（与 item_url 二选一）
    item_url: 商品链接（支持淘宝/天猫链接，自动解析ID）
    
    返回：
    商品月销量字符串
    """
    
    # 1. 参数校验：提取商品ID
    if not item_id and not item_url:
        return "查询失败：请提供商品ID或商品链接（支持淘宝/天猫）"
    
    if not item_id:
        item_id = extract_item_id(item_url)
        if not item_id:
            return "查询失败：无法识别的链接格式，请提供有效的淘宝/天猫商品链接"
    
    # 确保item_id是纯数字
    item_id = str(item_id).strip()
    if not item_id.isdigit():
        return "查询失败：商品ID格式无效，请提供正确的数字ID"
    
    # 2. 调用API查询
    try:
        params = {
            "itemId": item_id,
            "v": API_VERSION
        }
        
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # 3. 解析返回数据
        if not data:
            return "查询失败：该商品不存在或已下架，请确认商品ID/链接是否正确"
        
        # 检查API返回状态
        if not data.get("success", False):
            error_msg = data.get("message", data.get("code", "未知错误"))
            return f"查询失败：{error_msg}"
        
        return f"商品ID：{item_id} 的信息为：{data}"
    
    except requests.exceptions.Timeout:
        return "查询失败：网络请求超时，请稍后重试"
    except requests.exceptions.ConnectionError:
        return "查询失败：网络连接失败，请检查网络后重试"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return "查询失败：请求过于频繁，请稍后再试"
        return f"查询失败：服务器错误（HTTP {e.response.status_code}）"
    except json.JSONDecodeError:
        return "查询失败：接口返回数据格式异常"
    except Exception as e:
        return f"查询失败：未知错误 - {str(e)}"
