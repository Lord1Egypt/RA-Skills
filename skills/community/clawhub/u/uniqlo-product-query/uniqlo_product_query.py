#!/usr/bin/env python3
"""
优衣库商品查询Skill实现

功能：
- 关键词识别与意图判断
- API调用（支持分页获取所有数据）
- 数据处理与折扣筛选
- 生成Markdown格式报告

安全特性：
- 尺码白名单验证
- 请求超时控制
- 异常处理与重试机制
- API调用频率限制（2秒间隔）
"""

import os
import json
import time
import logging
from typing import Optional, Tuple, List, Dict, Any
from urllib.parse import quote
from datetime import datetime

import requests

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 常量定义
API_BASE_URL = "https://i.uniqlo.cn/p/hmall-sc-service/search/searchWithCategoryCodeAndConditions/zh_CN"
API_TIMEOUT = 30
REQUEST_DELAY = 2  # 请求间隔（秒）
MAX_RETRIES = 3
DISCOUNT_THRESHOLD = 60  # 折扣率阈值
PAGE_SIZE = 20

# 尺码映射表：显示名称 -> sizeCode（白名单）
SIZE_CODE_MAP = {
    'XXS': 'SMA001', 'XS': 'SMA002', 'S': 'SMA003', 'M': 'SMA004',
    'L': 'SMA005', 'XL': 'SMA006', 'XXL': 'SMA007',
    '150/76A': 'SMA001', '155/80A': 'SMA002', '160/84A': 'SMA003',
    '165/88A': 'SMA004', '170/92A': 'SMA005', '175/96A': 'SMA006',
    '180/100A': 'SMA007',
}

# 类别配置
CATEGORY_CONFIG = {
    'men': {'code': 'SALE_M', 'need_size_filter': True, 'gender_text': 'UNIQLO TOP'},
    'women': {'code': 'SALE_W', 'need_size_filter': True, 'gender_text': '女装'},
    'kids': {'code': 'SALE_K', 'need_size_filter': False, 'gender_text': None},
    'baby': {'code': 'SALE_B', 'need_size_filter': False, 'gender_text': None},
}

# 类别中文映射
CATEGORY_NAMES = {'men': '男装', 'women': '女装', 'kids': '童装', 'baby': '婴幼儿装'}


def identify_size(user_input: str) -> Optional[str]:
    """
    从用户输入中提取尺码
    
    Args:
        user_input: 用户输入的文本
        
    Returns:
        尺码显示名称，如果没有则返回 None
    """
    # 按长度降序匹配，优先匹配更长的尺码名（如 XXL 优先于 XL）
    for size in sorted(SIZE_CODE_MAP.keys(), key=len, reverse=True):
        if size.upper() in user_input.upper():
            return size
    return None


def get_size_info(size_name: Optional[str]) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    根据尺码显示名称获取完整的尺码信息
    
    Args:
        size_name: 尺码显示名称，如果为 None 则不进行尺码过滤
        
    Returns:
        (size_value, size_code, size_no_suffix)，如果 size_name 为 None 则返回 (None, None, None)
    """
    if size_name is None:
        return None, None, None
    
    size_code = SIZE_CODE_MAP.get(size_name)
    if size_code is None:
        logger.warning(f"未知的尺码: {size_name}")
        return None, None, None
    
    return size_name, size_code, size_code.replace('SMA', '')


def identify_intent(user_input: str) -> bool:
    """
    识别用户输入的意图
    
    Args:
        user_input: 用户输入的文本
        
    Returns:
        是否为优衣库商品查询意图
    """
    keywords = [
        '查询优衣库男装', '优衣库男装', '男装折扣',
        '查询优衣库女装', '优衣库女装', '女装折扣',
        '查询优衣库童装', '优衣库童装', '童装折扣',
        '查询优衣库婴幼儿装', '优衣库婴幼儿装', '婴幼儿装折扣',
        '优衣库服装', '优衣库折扣', '优衣库促销', '优衣库特价'
    ]
    return any(keyword in user_input for keyword in keywords)


def identify_category(user_input: str) -> str:
    """
    识别用户查询的商品类别
    
    Args:
        user_input: 用户输入的文本
        
    Returns:
        类别代码：'men', 'women', 'kids', 或 'baby'
    """
    if '童装' in user_input:
        return 'kids'
    elif '婴幼儿' in user_input:
        return 'baby'
    elif '女装' in user_input:
        return 'women'
    else:
        return 'men'  # 默认男装


def _build_exist_params(category: str, size_value: Optional[str] = None, 
                        size_code: Optional[str] = None, size_no_suffix: Optional[str] = None) -> List[Dict]:
    """
    构建API请求的exist参数
    
    Args:
        category: 商品类别
        size_value: 尺码显示值
        size_code: 尺码代码
        size_no_suffix: 尺码数字后缀
        
    Returns:
        exist参数列表
    """
    config = CATEGORY_CONFIG[category]
    exist_params = [
        {"title": "适用性别", "items": [config['gender_text']]},
        {"sexCode": config['gender_text']},
    ]
    
    # 仅在需要时添加尺码过滤
    if config['need_size_filter'] and size_code:
        exist_params.append({
            "title": "尺码",
            "items": [{
                "sizeValue": size_value,
                "sizeCode": size_code,
                "sizeNoSuffix": size_no_suffix
            }]
        })
    
    exist_params.append({
        "categoryFilter": {
            "top": "SALE",
            "second": config['code'],
            "third": ""
        }
    })
    
    return exist_params


def _build_payload(category: str, page: int, page_size: int, 
                   size_code: Optional[str] = None, size_value: Optional[str] = None,
                   size_no_suffix: Optional[str] = None) -> Dict[str, Any]:
    """
    构建API请求payload
    
    Args:
        category: 商品类别
        page: 页码
        page_size: 每页数量
        size_code: 尺码代码
        size_value: 尺码显示值
        size_no_suffix: 尺码数字后缀
        
    Returns:
        请求payload字典
    """
    config = CATEGORY_CONFIG[category]
    category_code = config['code']
    need_size = config['need_size_filter'] and size_code
    
    # 构建exist参数
    if need_size:
        exist_param = _build_exist_params(category, size_value, size_code, size_no_suffix)
        exist = [
            {"title": "适用性别", "items": [config['gender_text']]},
            {"sexCode": config['gender_text']},
            {"title": "尺码", "items": [{
                "sizeValue": size_value,
                "sizeCode": size_code,
                "sizeNoSuffix": size_no_suffix
            }]}
        ]
        url_path = (
            f'/c/{category_code}.html?exist='
            f'{quote(json.dumps(exist_param, separators=(",", ":")))}'
            f'&lineUpCode=&rank=overall&signChoose=%5B%22concessional_rate%22%5D'
        )
        payload_size = [size_code]
    else:
        # 童装/婴幼儿装或无尺码：简单格式
        url_path = f'/c/{category_code}.html'
        exist = []
        payload_size = []
    
    return {
        "url": url_path,
        "pageInfo": {"page": page, "pageSize": page_size, "withSideBar": "Y"},
        "belongTo": "pc",
        "rank": "overall",
        "priceRange": {"low": 0, "high": 0},
        "color": [],
        "size": payload_size,
        "season": [],
        "material": [],
        "sex": [],
        "categoryFilter": {
            "top": "UNIQLOTOP",
            "second": "SALE",
            "third": category_code
        },
        "identity": ["concessional_rate"],
        "insiteDescription": "",
        "exist": exist,
        "categoryCode": category_code,
        "searchFlag": False,
        "description": ""
    }


def _parse_product(product: Dict[str, Any]) -> Dict[str, Any]:
    """
    解析单个商品数据
    
    Args:
        product: 原始商品数据
        
    Returns:
        解析后的商品信息
    """
    product_code = product.get("productCode", "")
    original_price = product.get("originPrice", 0)
    current_price = product.get("minPrice", 0)
    
    # 计算折扣率
    discount_rate = round((current_price / original_price) * 100, 2) if original_price > 0 else 0
    
    return {
        "name": product.get("name", ""),
        "original_price": original_price,
        "current_price": current_price,
        "discount_rate": discount_rate,
        "image": f"https://www.uniqlo.cn{product.get('mainPic', '')}",
        "url": f"https://www.uniqlo.cn/product-detail.html?productCode={product_code}"
    }


def fetch_single_page(category: str = 'men', size_code: Optional[str] = None,
                     size_value: Optional[str] = None, size_no_suffix: Optional[str] = None,
                     page: int = 1, page_size: int = PAGE_SIZE) -> Dict[str, Any]:
    """
    获取单页优衣库折扣商品数据
    
    Args:
        category: 商品类别
        size_code: 尺码代码，为 None 时不过滤尺码
        size_value: 尺码显示值
        size_no_suffix: 尺码数字后缀
        page: 页码
        page_size: 每页数量
        
    Returns:
        包含商品数据的字典
    """
    payload = _build_payload(category, page, page_size, size_code, size_value, size_no_suffix)
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(API_BASE_URL, json=payload, headers=headers, timeout=API_TIMEOUT)
        response.raise_for_status()
        api_response = response.json()
        
        # 解析商品数据
        products = []
        if "resp" in api_response and isinstance(api_response["resp"], list) and len(api_response["resp"]) > 1:
            products_data = api_response["resp"][1]
            if isinstance(products_data, list):
                products = [_parse_product(p) for p in products_data]
        
        return {
            "success": True,
            "data": {
                "products": products,
                "page": page,
                "page_size": page_size
            }
        }
    except requests.exceptions.Timeout:
        logger.error(f"请求超时（第{page}页）")
        return {"success": False, "error": "请求超时，请稍后重试"}
    except requests.exceptions.RequestException as e:
        logger.error(f"请求失败（第{page}页）: {e}")
        return {"success": False, "error": f"网络请求失败: {str(e)}"}
    except (KeyError, TypeError, ValueError) as e:
        logger.error(f"数据解析失败（第{page}页）: {e}")
        return {"success": False, "error": f"数据解析失败: {str(e)}"}
    except Exception as e:
        logger.error(f"未知错误（第{page}页）: {e}")
        return {"success": False, "error": f"获取数据失败: {str(e)}"}


def fetch_all_pages(category: str = 'men', size_code: Optional[str] = None,
                   size_value: Optional[str] = None, size_no_suffix: Optional[str] = None,
                   page_size: int = PAGE_SIZE, max_retries: int = MAX_RETRIES) -> Dict[str, Any]:
    """
    获取所有分页的优衣库折扣商品数据
    
    Args:
        category: 商品类别
        size_code: 尺码代码，为 None 时不过滤尺码
        size_value: 尺码显示值
        size_no_suffix: 尺码数字后缀
        page_size: 每页数量
        max_retries: 最大重试次数
        
    Returns:
        包含所有商品数据的字典
    """
    all_products = []
    page = 1
    retry_count = 0
    
    while True:
        result = fetch_single_page(category, size_code, size_value, size_no_suffix, page, page_size)
        
        if not result.get('success'):
            if retry_count < max_retries:
                logger.warning(f"获取第{page}页失败，正在重试... ({retry_count + 1}/{max_retries})")
                retry_count += 1
                time.sleep(REQUEST_DELAY)
                continue
            else:
                return {"success": False, "error": f"获取数据失败: {result.get('error', '未知错误')}"}
        
        retry_count = 0
        current_products = result.get('data', {}).get('products', [])
        
        if not current_products:
            break
        
        all_products.extend(current_products)
        
        # 检查是否还有下一页
        if len(current_products) < page_size:
            break
        
        page += 1
        time.sleep(REQUEST_DELAY)  # 避免请求过快
    
    # 筛选折扣率 <= 60% 的商品并排序
    filtered_products = [p for p in all_products if p["discount_rate"] <= DISCOUNT_THRESHOLD]
    filtered_products.sort(key=lambda x: (x["discount_rate"], x["current_price"]))
    
    return {
        "success": True,
        "data": {
            "products": filtered_products,
            "total": len(filtered_products),
            "original_total": len(all_products)
        }
    }


def get_output_dir() -> str:
    """
    获取输出目录路径
    
    Returns:
        输出目录路径（当前目录下的 unique/）
    """
    output_dir = os.path.join(os.getcwd(), 'unique')
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def generate_markdown_file(products: List[Dict], category: str, 
                          size_value: Optional[str] = None) -> str:
    """
    生成包含商品图片和详情的Markdown文件
    
    Args:
        products: 商品列表
        category: 商品类别
        size_value: 尺码显示值，为 None 时表示不过滤尺码
        
    Returns:
        生成的文件路径
    """
    output_dir = get_output_dir()
    category_name = CATEGORY_NAMES.get(category, '男装')
    
    # 生成文件名和筛选文本
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if size_value:
        filename = f"优衣库{category_name}{size_value}尺码折扣商品清单_{timestamp}.md"
        size_filter_text = f"尺码：{size_value}"
    else:
        filename = f"优衣库{category_name}折扣商品清单_{timestamp}.md"
        size_filter_text = "不过滤尺码"
    
    filepath = os.path.join(output_dir, filename)
    
    # 计算统计信息
    discount_rates = [p['discount_rate'] for p in products]
    current_prices = [p['current_price'] for p in products]
    original_prices = [p['original_price'] for p in products]
    
    # 生成Markdown内容
    md_content = f"""# 优衣库{category_name}折扣商品清单（含图片）

> 数据更新时间：{datetime.now().strftime("%Y年%m月%d日 %H:%M")}
> 筛选条件：折扣率 ≤ {DISCOUNT_THRESHOLD}%，{size_filter_text}
> 商品总数：{len(products)}件

---

"""
    
    # 添加商品详情
    for i, p in enumerate(products, 1):
        md_content += f"""## {i}. {p['name']}

<img src="{p['image']}" width="200" alt="{p['name']}">

- **原价**：¥{p['original_price']:.1f}
- **现价**：¥{p['current_price']:.1f}
- **折扣率**：{p['discount_rate']:.2f}%
- **商品链接**：[点击查看详情]({p['url']})

---

"""
    
    # 添加汇总信息
    md_content += f"""## 汇总信息

| 统计项 | 数值 |
|-------|------|
| 商品总数 | {len(products)}件 |
| 最低折扣 | {min(discount_rates):.2f}% |
| 最高折扣 | {max(discount_rates):.2f}% |
| 最低价格 | ¥{min(current_prices):.1f} |
| 最高价格 | ¥{max(current_prices):.1f} |
| 总原价 | ¥{sum(original_prices):.1f} |
| 总现价 | ¥{sum(current_prices):.1f} |
| 总节省 | ¥{sum(original_prices) - sum(current_prices):.1f} |

**超值推荐**：
- 折扣最低（{min(discount_rates):.2f}%）：最划算的商品
- 性价比最高（¥{min(current_prices):.1f}）：价格最低的商品

---

*注：点击图片可查看大图，点击"点击查看详情"可跳转到商品购买页面*
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    logger.info(f"Markdown文件已生成: {filepath}")
    return filepath


def format_response(result: Dict, category: str, 
                   size_value: Optional[str] = None) -> str:
    """
    格式化响应结果，生成Markdown文件并返回文件路径
    
    Args:
        result: API调用结果
        category: 商品类别
        size_value: 尺码显示值，为 None 时表示不过滤尺码
        
    Returns:
        响应文本（包含文件路径）
    """
    try:
        if not result.get('success'):
            cat_name = CATEGORY_NAMES.get(category, '男装')
            return f"抱歉，查询优衣库{cat_name}失败：{result.get('error', '未知错误')}"
        
        data = result.get('data', {})
        products = data.get('products', [])
        total = data.get('total', 0)
        
        if total == 0:
            cat_name = CATEGORY_NAMES.get(category, '男装')
            if size_value:
                return f"抱歉，未找到优衣库{cat_name}尺码{size_value}的折扣商品"
            else:
                return f"抱歉，未找到优衣库{cat_name}的折扣商品"
        
        # 生成Markdown文件
        filepath = generate_markdown_file(products, category, size_value)
        
        # 计算统计信息
        discount_rates = [p['discount_rate'] for p in products]
        current_prices = [p['current_price'] for p in products]
        
        # 生成响应文本
        cat_name = CATEGORY_NAMES.get(category, '男装')
        size_info = f"尺码{size_value}" if size_value else "所有尺码"
        
        return f"""找到 **{total} 件**优衣库{cat_name}（{size_info}）折扣商品！

**汇总信息：**
- 最低折扣：{min(discount_rates):.2f}%
- 最高折扣：{max(discount_rates):.2f}%
- 最低价格：¥{min(current_prices):.1f}
- 最高价格：¥{max(current_prices):.1f}

**已生成完整商品清单文件：**
📄 {filepath}

该文件包含：
- 全部 {total} 件商品的图片
- 原价、现价、折扣率
- 可点击的商品链接

请查看上方文件获取完整信息！"""
        
    except Exception as e:
        logger.error(f"处理响应时出错: {e}")
        return f"抱歉，处理商品数据时出错：{str(e)}"


def process_query(user_input: str) -> str:
    """
    处理用户查询
    
    Args:
        user_input: 用户输入的文本
        
    Returns:
        响应结果
    """
    # 识别意图
    if not identify_intent(user_input):
        return "抱歉，我不理解您的请求。请尝试输入'查询优衣库男装'或'优衣库女装'等相关指令。"
    
    # 识别类别和尺码
    category = identify_category(user_input)
    size_value = identify_size(user_input)
    size_value, size_code, size_no_suffix = get_size_info(size_value)
    
    logger.info(f"查询类别: {category}, 尺码: {size_value or '所有尺码'}")
    
    # 获取数据并格式化响应
    result = fetch_all_pages(category, size_code, size_value, size_no_suffix)
    return format_response(result, category, size_value)


if __name__ == "__main__":
    # 测试示例
    test_queries = [
        "查询优衣库男装",
        "优衣库女装特价",
        "优衣库服装折扣"
    ]
    
    for query in test_queries:
        print(f"\n测试查询：{query}")
        print("=" * 50)
        print(process_query(query))
        print("=" * 50)
