import requests
import time
import random
import string
import json
import base64
from datetime import datetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# 配置参数
API_LIST_URL = "https://shop.chuanshatiyuchang.cn/gym/miniprogram/venue/listAreaLease"
API_ORDER_URL = "https://shop.chuanshatiyuchang.cn/gym/miniprogram/areaOrder/createOrder"
VENUE_DATE = "2026-04-25"
TARGET_START_TIME = "10:00"
TARGET_END_TIME = "11:00"
POLL_INTERVAL = 5
TOKEN = "0cd5cb6b21fc410dbd81bc3e6a066614"
AUTO_BOOK = True

with open("rsa_private_key.pem", "r", encoding="utf-8") as f:
    RSA_PRIVATE_KEY = f.read()

BASE_HEADERS = {
    "Host": "shop.chuanshatiyuchang.cn",
    "Connection": "keep-alive",
    "token-user": TOKEN,
    "content-type": "application/json",
    "x-gym-client-id": "1",
    "Accept-Encoding": "gzip,compress,br,deflate",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 26_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.70(0x1800463a) NetType/4G Language/zh_CN",
    "Referer": "https://servicewechat.com/wx2fdf924861911ddc/18/page-frame.html"
}


def generate_nonce():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))


def generate_rsa_signature(sign_string):
    try:
        private_key = serialization.load_pem_private_key(
            RSA_PRIVATE_KEY.encode('utf-8'),
            password=None,
            backend=default_backend()
        )

        signature = private_key.sign(
            sign_string.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        return base64.b64encode(signature).decode('utf-8')
    except Exception as e:
        print(f"签名生成失败: {e}")
        return ""


def build_sign_headers(order_data):
    timestamp = str(int(time.time()))
    nonce = generate_nonce()

    sign_parts = []
    sign_parts.append(f"areaItems={json.dumps(order_data['areaItems'], separators=(',', ':'), ensure_ascii=False)}")
    sign_parts.append(f"venueSportId={order_data['venueSportId']}")
    sign_parts.append(f"nonce={nonce}")
    sign_parts.append(f"timestamp={timestamp}")

    sign_string = '&'.join(sign_parts)

    print(f"\n签名调试信息:")
    print(f"  Timestamp: {timestamp}")
    print(f"  Nonce: {nonce}")
    print(f"  签名字符串: {sign_string}")

    signature = generate_rsa_signature(sign_string)

    print(f"  生成签名: {signature}")

    return {
        "X-Ca-Timestamp": timestamp,
        "X-Ca-Nonce": nonce,
        "X-Ca-Signature": signature
    }


def create_order(venue_item):
    try:
        print(f"\n正在尝试自动下单: {venue_item['areaName']} {venue_item['startTime']}-{venue_item['endTime']}")

        order_data = {
            "venueSportId": 1,
            "areaItems": [{
                "areaDate": venue_item["areaDate"],
                "areaId": venue_item["areaId"],
                "areaName": venue_item["areaName"],
                "endTime": venue_item["endTime"],
                "packageId": None,
                "price": venue_item["price"],
                "showStatus": venue_item["showStatus"],
                "sportId": venue_item["sportId"],
                "sportName": venue_item["sportName"],
                "startTime": venue_item["startTime"],
                "status": venue_item["status"],
                "uniqNo": venue_item["uniqNo"],
                "checked": True,
                "row": venue_item.get("row", 0),
                "col": venue_item.get("col", 0)
            }]
        }

        headers = BASE_HEADERS.copy()
        sign_headers = build_sign_headers(order_data)
        headers.update(sign_headers)

        response = requests.post(API_ORDER_URL, headers=headers, json=order_data, timeout=15)
        result = response.json()

        if result.get("code") == 200 and result.get("success"):
            order_id = result["data"]["areaOrderId"]
            amount = result["data"]["actualAmount"]
            expire_time = result["data"]["expireTime"]
            print(f"下单成功! 订单号: {order_id}")
            print(f"金额: {amount}元")
            print(f"支付截止时间: {expire_time}")
            print("请尽快前往小程序完成支付")
            return True
        else:
            print(f"下单失败: {result.get('message', '未知错误')}")
            return False

    except Exception as e:
        print(f"下单出错: {str(e)}")
        return False


def check_venue_availability():
    try:
        params = {
            "venueSportId": 1,
            "date": VENUE_DATE
        }

        response = requests.get(API_LIST_URL, headers=BASE_HEADERS, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("code") != 200:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 请求失败: {data.get('message')}")
            return

        available_venues = []
        all_venues = []

        for area in data["data"]["areas"]:
            area_name = area["areaName"]
            for item in area["items"]:
                if item["startTime"] == TARGET_START_TIME and item["endTime"] == TARGET_END_TIME:
                    status = item["status"]
                    show_status = item["showStatus"]
                    price = item["price"]

                    venue_info = f"{area_name} | 价格: {price}元 | 状态: {status}({show_status})"
                    all_venues.append(venue_info)

                    if status not in ["PAYED", "LOCK"] and show_status != "UNAVAILABLE":
                        available_venues.append(venue_info)
                        if AUTO_BOOK:
                            success = create_order(item)
                            if success:
                                print("\n自动抢票成功! 程序即将退出")
                                exit(0)

        print(f"\n===== {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 查询结果 =====")
        print(f"查询日期: {VENUE_DATE} 时间段: {TARGET_START_TIME}-{TARGET_END_TIME}\n")

        if available_venues:
            print("发现可预订场地:")
            print("=" * 60)
            for venue in available_venues:
                print(f"  {venue}")
            print("=" * 60)
        else:
            print("暂无可用场地，所有场地状态如下:")
            for venue in all_venues:
                print(f"  {venue}")

        return available_venues

    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 请求出错: {str(e)}")
        return None


def main():
    print("羽毛球场地轮询监控启动")
    print(f"监控日期: {VENUE_DATE}")
    print(f"监控时段: {TARGET_START_TIME} - {TARGET_END_TIME}")
    print(f"轮询间隔: {POLL_INTERVAL}秒")
    print(f"{'='*60}")

    count = 0
    while True:
        count += 1
        print(f"\n[第 {count} 次查询]")

        available = check_venue_availability()

        if available:
            print("\n检测到可用场地，停止轮询")
            break

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
