import os
import json
import time
import hashlib
import http.client
from typing import Dict, Any, Optional, List

# 允许调用的安全端点白名单
ALLOWED_ENDPOINTS = {
    "/api/open/product/create",      # 创建商品
    "/api/open/product/detail",      # 查询商品
    "/api/open/product/list",        # 商品列表
    "/api/open/product/edit",        # 编辑商品
    "/api/open/product/del",         # 删除商品
    "/api/open/product/onshelf",     # 上架
    "/api/open/product/offshelf",    # 下架
    "/api/open/order/detail",        # 订单详情
    "/api/open/order/list",          # 订单列表
    "/api/open/order/modifyprice",   # 改价
    "/api/open/order/logistics",     # 发货
    "/api/open/user/shopinfo",       # 店铺信息
    "/api/open/category/query",      # 类目查询
    "/api/open/express/companies",   # 快递公司
    "/api/open/area/geo",            # 地区数据
}

# 默认需要用户确认的高风险操作端点
HIGH_RISK_ENDPOINTS = {
    "/api/open/product/create",
    "/api/open/product/del",
    "/api/open/product/edit",
    "/api/open/product/onshelf",
    "/api/open/product/offshelf",
    "/api/open/order/modifyprice",
    "/api/open/order/logistics",
}


class XianYuAPIClient:
    """闲鱼管家API客户端

    安全设计原则：
    1. 所有写操作（创建/删除/编辑/上架/下架/改价/发货）默认需要用户确认
    2. 提供 _unsafe 后缀的方法供自动化脚本使用，跳过确认
    3. 端点白名单防止调用未授权的API
    4. dry_run 模式用于预览请求数据
    """

    def __init__(self, app_key: Optional[str] = None, app_secret: Optional[str] = None):
        """
        初始化API客户端

        Args:
            app_key: 闲鱼应用Key，如果为None则从环境变量读取
            app_secret: 闲鱼应用密钥，如果为None则从环境变量读取
        """
        self.app_key = app_key or os.getenv('XIAN_YU_APP_KEY')
        self.app_secret = app_secret or os.getenv('XIAN_YU_APP_SECRET')
        self.domain = "https://open.goofish.pro"

        if not self.app_key or not self.app_secret:
            raise ValueError("XIAN_YU_APP_KEY and XIAN_YU_APP_SECRET must be provided or set as environment variables")

    def _generate_sign(self, body_json: str, timestamp: int) -> str:
        """生成API签名"""
        m = hashlib.md5()
        m.update(body_json.encode('utf-8'))
        body_md5 = m.hexdigest()

        sign_string = f"{self.app_key},{body_md5},{timestamp},{self.app_secret}"

        m = hashlib.md5()
        m.update(sign_string.encode('utf-8'))
        return m.hexdigest()

    def _do_request(self, endpoint: str, data: Dict[str, Any], confirm: bool = True) -> Dict[str, Any]:
        """内部请求执行方法

        Args:
            endpoint: API端点路径
            data: 请求数据
            confirm: 如果为False，跳过用户确认（仅供 _unsafe 方法内部调用）
        """
        # 端点白名单检查
        if endpoint not in ALLOWED_ENDPOINTS:
            raise ValueError(f"Endpoint '{endpoint}' is not allowed. Allowed: {ALLOWED_ENDPOINTS}")

        # 高风险操作确认（仅在 confirm=True 时执行）
        if endpoint in HIGH_RISK_ENDPOINTS and confirm:
            print(f"\n[高风险操作确认] 即将调用: {endpoint}")
            print(f"请求数据预览:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
            confirm_input = input("是否继续? [y/N]: ")
            if confirm_input.strip().lower() != 'y':
                return {"code": -1, "msg": "用户取消操作", "data": {}}

        # 将json对象转成json字符串，去除空格
        body = json.dumps(data, separators=(',', ':'))

        # 时间戳（秒）
        timestamp = int(time.time())

        # 生成签名
        sign = self._generate_sign(body, timestamp)

        # 构建完整URL
        url = f"{endpoint}?appid={self.app_key}&timestamp={timestamp}&sign={sign}"

        # 设置请求头
        headers = {"Content-Type": "application/json"}

        # 发送HTTPS请求
        conn = http.client.HTTPSConnection("open.goofish.pro")
        conn.request("POST", url, body, headers)
        response = conn.getresponse()
        response_data = response.read().decode('utf-8')
        conn.close()

        # 解析JSON响应
        result = json.loads(response_data)

        # 验证响应格式
        if 'code' not in result:
            raise Exception(f"Invalid API response format: {response_data}")

        return result

    def request(self, endpoint: str, data: Dict[str, Any], dry_run: bool = False) -> Dict[str, Any]:
        """
        发送API请求（默认安全模式：高风险操作需要确认）

        Args:
            endpoint: API端点路径，如 "/api/open/product/create"
            data: 请求数据字典
            dry_run: 如果为True，只打印请求数据不实际发送

        Returns:
            API响应数据字典
        """
        if dry_run:
            print(f"\n[Dry Run] 端点: {endpoint}")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return {"code": 0, "msg": "dry_run", "data": data}

        return self._do_request(endpoint, data, confirm=True)

    def request_unsafe(self, endpoint: str, data: Dict[str, Any], dry_run: bool = False) -> Dict[str, Any]:
        """
        发送API请求（不安全模式：跳过所有确认）

        警告：此方法跳过用户确认，适合自动化脚本使用。
        调用前请确保已通过 dry_run 预览请求数据。

        Args:
            endpoint: API端点路径
            data: 请求数据字典
            dry_run: 如果为True，只打印请求数据不实际发送

        Returns:
            API响应数据字典
        """
        if dry_run:
            print(f"\n[Dry Run (unsafe)] 端点: {endpoint}")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return {"code": 0, "msg": "dry_run", "data": data}

        return self._do_request(endpoint, data, confirm=False)

    def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建商品（默认需要用户确认）"""
        self._validate_product_data(product_data)
        return self.request("/api/open/product/create", product_data)

    def create_product_unsafe(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建商品（跳过确认，供自动化使用）"""
        self._validate_product_data(product_data)
        return self.request_unsafe("/api/open/product/create", product_data)

    def _validate_product_data(self, product_data: Dict[str, Any]) -> None:
        """验证商品数据必需字段"""
        if 'publish_shop' not in product_data or not product_data['publish_shop']:
            raise ValueError("Missing required field: publish_shop")

        for shop in product_data['publish_shop']:
            required_fields = ['user_name', 'images', 'title', 'content']
            for field in required_fields:
                if field not in shop:
                    raise ValueError(f"Missing required field in publish_shop: {field}")

            if not isinstance(shop['images'], list) or len(shop['images']) == 0:
                raise ValueError("images must be a non-empty list of image URLs")

            if len(shop['title']) > 60:
                raise ValueError("title must not exceed 60 characters")

            import re
            emoji_pattern = re.compile(
                "["
                "\U0001F600-\U0001F64F"
                "\U0001F300-\U0001F5FF"
                "\U0001F680-\U0001F6FF"
                "\U0001F1E0-\U0001F1FF"
                "]+", flags=re.UNICODE)
            if emoji_pattern.search(shop['title']):
                raise ValueError("title must not contain emoji characters")

    def get_product_detail(self, product_id: str) -> Dict[str, Any]:
        """获取商品详情（只读操作，无需确认）"""
        return self.request("/api/open/product/detail", {"product_id": product_id})

    def delete_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """删除商品（默认需要用户确认）"""
        return self.request("/api/open/product/del", product_data)

    def delete_product_unsafe(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """删除商品（跳过确认，供自动化使用）"""
        return self.request_unsafe("/api/open/product/del", product_data)

    def modify_order_price(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """修改订单价格（默认需要用户确认）"""
        return self.request("/api/open/order/modifyprice", order_data)

    def modify_order_price_unsafe(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """修改订单价格（跳过确认，供自动化使用）"""
        return self.request_unsafe("/api/open/order/modifyprice", order_data)
