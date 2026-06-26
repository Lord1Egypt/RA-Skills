#!/usr/bin/env python3
"""顺丰速运助手 - 专为顺丰用户提供深度集成的快递服务"""

import argparse
import asyncio
import json
import os
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

_secure_storage: Optional[object] = None
LOCAL_ENDPOINT_HOSTS = {"127.0.0.1", "localhost", "::1"}

# 配置
CONFIG_DIR = Path.home() / ".openclaw" / "data" / "sf-express"
DB_FILE = CONFIG_DIR / "sfexpress.db"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# 顺丰产品类型
SF_PRODUCTS = {
    'standard': {'name': '顺丰标快', 'code': 'S1', 'time': '1-2天', 'desc': '普通文件、包裹'},
    'express': {'name': '顺丰特快', 'code': 'S2', 'time': '次日达', 'desc': '紧急文件、时效要求高'},
    'same_day': {'name': '顺丰即日', 'code': 'S3', 'time': '当日达', 'desc': '同城急件'},
    'cold_chain': {'name': '顺丰冷链', 'code': 'S4', 'time': '1-2天', 'desc': '生鲜、医药'},
    'heavy': {'name': '顺丰重货', 'code': 'S5', 'time': '2-3天', 'desc': '大件物品'},
    'international': {'name': '顺丰国际', 'code': 'S6', 'time': '3-7天', 'desc': '跨境快递'},
    'economy': {'name': '顺丰特惠', 'code': 'S7', 'time': '2-3天', 'desc': '非紧急、经济型'},
}

# 顺丰单号规则
SF_PATTERN = r'^[A-Z]{2}\d{10,}$|^\d{12,15}$'


@dataclass
class TrackingEvent:
    """物流事件"""
    time: str
    description: str
    location: str
    status: str


@dataclass
class TrackingResult:
    """查询结果"""
    tracking_number: str
    product_name: str
    status: str
    events: List[TrackingEvent]
    estimated_delivery: Optional[str] = None
    last_updated: Optional[str] = None
    sender: Optional[str] = None
    receiver: Optional[str] = None
    source: str = "unknown"


@dataclass
class TimeEstimate:
    """时效预估"""
    product: str
    product_name: str
    estimated_time: str
    price_range: str
    cutoff_time: str


@dataclass
class PriceEstimate:
    """运费估算"""
    product: str
    product_name: str
    weight: float
    base_price: float
    fuel_surcharge: float
    total_price: float
    delivery_time: str


class SFExpressClient:
    """顺丰客户端"""
    
    def __init__(self):
        self.db = self._init_db()
    
    def _init_db(self) -> sqlite3.Connection:
        """初始化数据库"""
        conn = sqlite3.connect(str(DB_FILE))
        cursor = conn.cursor()
        
        # 查询历史表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracking_number TEXT NOT NULL,
                product_name TEXT,
                status TEXT,
                result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 订阅表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracking_number TEXT NOT NULL UNIQUE,
                last_status TEXT,
                notify_enabled BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 寄件地址表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS addresses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                is_default BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        return conn
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
    
    def is_sf_number(self, tracking_number: str) -> bool:
        """检查是否为顺丰单号"""
        return bool(re.match(SF_PATTERN, tracking_number.upper()))
    
    async def query(self, tracking_number: str, allow_mock: bool = False) -> TrackingResult:
        """查询物流信息"""
        if not self.is_sf_number(tracking_number):
            raise ValueError(f"{tracking_number} 不是有效的顺丰单号")

        endpoint = os.environ.get("SF_EXPRESS_TRACKING_ENDPOINT", "").strip()
        if endpoint:
            result = await self._query_live_endpoint(tracking_number, endpoint)
            self._save_history(result)
            return result

        if not allow_mock:
            raise RuntimeError(
                "未配置真实顺丰查询端点。请设置 SF_EXPRESS_TRACKING_ENDPOINT，"
                "或仅在演示/测试时加 --mock 使用明确标记的模拟数据。"
            )

        # 显式模拟结果。只能在 --mock 下使用，不能冒充真实顺丰轨迹。
        result = TrackingResult(
            tracking_number=tracking_number,
            product_name="顺丰标快（模拟）",
            status="mock_in_transit",
            events=[
                TrackingEvent(
                    time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    description="模拟事件：快件已到达【北京顺义集散中心】",
                    location="北京市",
                    status="mock_in_transit"
                ),
                TrackingEvent(
                    time=(datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
                    description="模拟事件：快件已从【上海虹桥集散中心】发出",
                    location="上海市",
                    status="mock_in_transit"
                ),
            ],
            estimated_delivery=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            sender="上海市",
            receiver="北京市",
            source="mock"
        )

        self._save_history(result)
        return result

    async def _query_live_endpoint(self, tracking_number: str, endpoint: str) -> TrackingResult:
        """Query a user-configured live endpoint.

        The endpoint may contain `{tracking_number}` or accept `tracking_number`
        as a query parameter. The response must be JSON with either a top-level
        `events` list or a `data.events` list.
        """
        if "{tracking_number}" in endpoint:
            url = endpoint.replace("{tracking_number}", tracking_number)
        else:
            separator = "&" if "?" in endpoint else "?"
            url = endpoint + separator + urlencode({"tracking_number": tracking_number})

        self._validate_live_endpoint_url(url)
        try:
            payload = await asyncio.to_thread(self._fetch_live_json, url)
        except Exception as exc:
            raise RuntimeError(f"真实顺丰查询端点请求失败: {exc}") from exc

        data = payload.get("data", payload) if isinstance(payload, dict) else {}
        events_raw = data.get("events") if isinstance(data, dict) else None
        if not isinstance(events_raw, list):
            raise RuntimeError("真实查询端点返回格式无效：缺少 events 列表")

        events: List[TrackingEvent] = []
        for item in events_raw:
            if not isinstance(item, dict):
                continue
            events.append(TrackingEvent(
                time=str(item.get("time") or item.get("timestamp") or ""),
                description=str(item.get("description") or item.get("desc") or item.get("status") or ""),
                location=str(item.get("location") or ""),
                status=str(item.get("status") or data.get("status") or "unknown"),
            ))

        if not events:
            raise RuntimeError("真实查询端点返回格式无效：events 为空")

        return TrackingResult(
            tracking_number=str(data.get("tracking_number") or tracking_number),
            product_name=str(data.get("product_name") or data.get("product") or "顺丰"),
            status=str(data.get("status") or events[0].status or "unknown"),
            events=events,
            estimated_delivery=data.get("estimated_delivery"),
            last_updated=str(data.get("last_updated") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            sender=data.get("sender"),
            receiver=data.get("receiver"),
            source="live_endpoint",
        )

    def _validate_live_endpoint_url(self, url: str) -> None:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise RuntimeError("SF_EXPRESS_TRACKING_ENDPOINT 必须是绝对 http(s) URL")
        if parsed.scheme == "https":
            return
        if parsed.hostname in LOCAL_ENDPOINT_HOSTS:
            return
        raise RuntimeError("真实查询端点必须使用 HTTPS；HTTP 仅允许 127.0.0.1/localhost 本地开发")

    def _fetch_live_json(self, url: str) -> Dict:
        request = Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "sf-express-skill/1.1.2",
            },
        )
        with urlopen(request, timeout=10) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return json.loads(response.read().decode(charset))

    async def batch_query(self, tracking_numbers: List[str], allow_mock: bool = False) -> List[TrackingResult]:
        """批量查询"""
        tasks = [self.query(number, allow_mock=allow_mock) for number in tracking_numbers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if not isinstance(r, Exception)]
    
    def estimate_time(self, origin: str, destination: str, product: str = 'standard') -> TimeEstimate:
        """时效预估"""
        product_info = SF_PRODUCTS.get(product, SF_PRODUCTS['standard'])
        
        if product == 'same_day':
            estimated = "今日 18:00 前"
        elif product == 'express':
            estimated = "次日 12:00 前"
        else:
            estimated = f"{product_info['time']}"
        
        return TimeEstimate(
            product=product,
            product_name=product_info['name'],
            estimated_time=estimated,
            price_range="¥18-35",
            cutoff_time="当日 16:00"
        )
    
    def estimate_price(self, origin: str, destination: str, weight: float, product: str = 'standard') -> PriceEstimate:
        """运费估算"""
        product_info = SF_PRODUCTS.get(product, SF_PRODUCTS['standard'])
        
        base_price = 18.0
        if weight > 1:
            base_price += (weight - 1) * 5
        
        if product == 'express':
            base_price *= 1.5
        elif product == 'same_day':
            base_price *= 2.0
        elif product == 'cold_chain':
            base_price *= 1.3
        elif product == 'heavy':
            base_price = weight * 3
        
        fuel_surcharge = base_price * 0.1
        total = base_price + fuel_surcharge
        
        return PriceEstimate(
            product=product,
            product_name=product_info['name'],
            weight=weight,
            base_price=round(base_price, 2),
            fuel_surcharge=round(fuel_surcharge, 2),
            total_price=round(total, 2),
            delivery_time=product_info['time']
        )
    
    def _save_history(self, result: TrackingResult):
        """保存查询历史"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO history (tracking_number, product_name, status, result)
            VALUES (?, ?, ?, ?)
        ''', (
            result.tracking_number,
            result.product_name,
            result.status,
            json.dumps(result.__dict__, default=lambda x: x.__dict__ if hasattr(x, '__dict__') else str(x))
        ))
        self.db.commit()
    
    def get_history(self, limit: int = 10, search: Optional[str] = None) -> List[dict]:
        """获取查询历史"""
        cursor = self.db.cursor()
        
        if search:
            cursor.execute('''
                SELECT * FROM history 
                WHERE tracking_number LIKE ? 
                ORDER BY created_at DESC LIMIT ?
            ''', (f'%{search}%', limit))
        else:
            cursor.execute('''
                SELECT * FROM history 
                ORDER BY created_at DESC LIMIT ?
            ''', (limit,))
        
        columns = [description[0] for description in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    
    def subscribe(self, tracking_number: str):
        """订阅物流提醒"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO subscriptions (tracking_number, last_status)
            VALUES (?, ?)
        ''', (tracking_number, 'pending'))
        self.db.commit()
        return True
    
    def unsubscribe(self, tracking_number: str):
        """取消订阅"""
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM subscriptions WHERE tracking_number = ?', (tracking_number,))
        self.db.commit()
        return True
    
    def get_subscriptions(self) -> List[dict]:
        """获取所有订阅"""
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM subscriptions ORDER BY created_at DESC')
        columns = [description[0] for description in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    
    def format_tracking_result(self, result: TrackingResult) -> str:
        """格式化查询结果"""
        source_label = {
            "live_endpoint": "真实查询端点",
            "mock": "模拟演示数据（非真实物流）",
        }.get(result.source, result.source)
        lines = [
            f"📦 顺丰速运 ({result.tracking_number})",
            f"数据来源: {source_label}",
            f"产品: {result.product_name}",
            f"状态: {self._format_status(result.status)}",
            f"预计送达: {result.estimated_delivery or '未知'}",
            f"更新时间: {result.last_updated or '未知'}",
            "",
            "物流轨迹:",
        ]
        
        for event in result.events:
            lines.append(f"  [{event.time}] {event.location} - {event.description}")
        
        return "\n".join(lines)
    
    def format_time_estimate(self, estimate: TimeEstimate) -> str:
        """格式化工时效预估"""
        return f"""📋 时效预估
产品: {estimate.product_name}
预计时效: {estimate.estimated_time}
价格区间: {estimate.price_range}
截单时间: {estimate.cutoff_time}"""
    
    def format_price_estimate(self, estimate: PriceEstimate) -> str:
        """格式化运费估算"""
        return f"""💰 运费估算
产品: {estimate.product_name}
重量: {estimate.weight}kg
基础运费: ¥{estimate.base_price}
燃油附加费: ¥{estimate.fuel_surcharge}
预估总价: ¥{estimate.total_price}
配送时效: {estimate.delivery_time}"""
    
    def _format_status(self, status: str) -> str:
        """格式化状态"""
        status_map = {
            'pending': '⏳ 待揽收',
            'picked_up': '📦 已揽收',
            'in_transit': '🚚 运输中',
            'mock_in_transit': '🚚 模拟运输中',
            'delivered': '✅ 已签收',
            'exception': '⚠️ 异常',
        }
        return status_map.get(status, status)


def print_products():
    """打印顺丰产品列表"""
    print("顺丰产品类型:\n")
    print(f"{'代码':<15} {'名称':<12} {'时效':<10} {'说明'}")
    print("-" * 60)
    for code, info in SF_PRODUCTS.items():
        print(f"{code:<15} {info['name']:<12} {info['time']:<10} {info['desc']}")


def print_history(client: SFExpressClient, limit: int = 10, search: Optional[str] = None):
    """打印查询历史"""
    history = client.get_history(limit, search)
    if not history:
        print("暂无查询记录")
        return
    
    print(f"最近 {len(history)} 条查询记录:\n")
    print(f"{'单号':<20} {'产品':<12} {'状态':<10} {'查询时间':<20}")
    print("-" * 70)
    
    for record in history:
        print(f"{record['tracking_number']:<20} {record['product_name'] or '-':<12} "
              f"{record['status']:<10} {record['created_at']:<20}")


def print_subscriptions(client: SFExpressClient):
    """打印订阅列表"""
    subs = client.get_subscriptions()
    if not subs:
        print("暂无订阅")
        return
    
    print(f"共 {len(subs)} 个订阅:\n")
    print(f"{'单号':<20} {'最后状态':<12} {'订阅时间':<20}")
    print("-" * 60)
    
    for sub in subs:
        print(f"{sub['tracking_number']:<20} {sub['last_status']:<12} {sub['created_at']:<20}")


def print_privacy_info():
    """打印隐私信息"""
    info = get_secure_storage().get_storage_info()
    print("存储信息:\n")
    print(f"存储目录: {info['base_dir']}")
    print(f"文件数量: {info['total_files']}\n")
    
    if info['files']:
        print("文件列表:")
        for f in info['files']:
            print(f"  - {f['name']} ({f['size']} bytes, 权限: {f['permissions']})")


def get_secure_storage():
    """Lazily initialize encrypted storage to avoid creating key files on import."""
    global _secure_storage
    if _secure_storage is None:
        try:
            from security import SecureStorage
        except ImportError as exc:
            raise RuntimeError("隐私加密功能需要 cryptography，请先安装 requirements.txt") from exc
        _secure_storage = SecureStorage(app_name="sf-express")
    return _secure_storage


def clear_local_data() -> Dict[str, int]:
    """Clear local SQLite records and encrypted storage files."""
    removed = {"history": 0, "subscriptions": 0, "addresses": 0, "secure_files": 0}
    if DB_FILE.exists():
        conn = sqlite3.connect(str(DB_FILE))
        try:
            cursor = conn.cursor()
            for table in ("history", "subscriptions", "addresses"):
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                removed[table] = int(cursor.fetchone()[0])
                cursor.execute(f"DELETE FROM {table}")
            conn.commit()
        finally:
            conn.close()

    storage = get_secure_storage()
    removed["secure_files"] = len(storage.list_files())
    storage.clear_all()

    export_file = CONFIG_DIR / "privacy_export.json"
    if export_file.exists():
        export_file.unlink()
    return removed


async def main():
    parser = argparse.ArgumentParser(description='顺丰速运助手')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 单号查询
    query_parser = subparsers.add_parser('query', help='查询顺丰快递')
    query_parser.add_argument('tracking_number', help='顺丰单号')
    query_parser.add_argument('--mock', action='store_true',
                              help='使用明确标记的模拟数据；默认不伪造实时轨迹')
    
    # 批量查询
    batch_parser = subparsers.add_parser('batch', help='批量查询')
    batch_parser.add_argument('tracking_numbers', nargs='+', help='顺丰单号列表')
    batch_parser.add_argument('--mock', action='store_true',
                              help='使用明确标记的模拟数据；默认不伪造实时轨迹')
    
    # 时效查询
    time_parser = subparsers.add_parser('time', help='时效预估')
    time_parser.add_argument('origin', help='寄件地')
    time_parser.add_argument('destination', help='收件地')
    time_parser.add_argument('--product', '-p', default='standard', 
                            choices=list(SF_PRODUCTS.keys()),
                            help='产品类型')
    
    # 运费估算
    price_parser = subparsers.add_parser('price', help='运费估算')
    price_parser.add_argument('origin', help='寄件地')
    price_parser.add_argument('destination', help='收件地')
    price_parser.add_argument('--weight', '-w', type=float, default=1.0, help='重量(kg)')
    price_parser.add_argument('--product', '-p', default='standard',
                            choices=list(SF_PRODUCTS.keys()),
                            help='产品类型')
    
    # 产品列表
    subparsers.add_parser('products', help='查看顺丰产品类型')
    
    # 历史记录
    history_parser = subparsers.add_parser('history', help='查询历史')
    history_parser.add_argument('--limit', '-l', type=int, default=10, help='显示数量')
    history_parser.add_argument('--search', '-s', help='搜索单号')
    
    # 订阅
    sub_parser = subparsers.add_parser('subscribe', help='订阅物流提醒')
    sub_parser.add_argument('tracking_number', help='顺丰单号')
    
    # 取消订阅
    unsub_parser = subparsers.add_parser('unsubscribe', help='取消订阅')
    unsub_parser.add_argument('tracking_number', help='顺丰单号')
    
    # 订阅列表
    subparsers.add_parser('subscriptions', help='查看所有订阅')
    
    # 隐私控制
    privacy_parser = subparsers.add_parser('privacy', help='隐私控制')
    privacy_parser.add_argument('action', choices=['info', 'clear', 'export'],
                                help='info: 查看信息, clear: 清除数据, export: 导出备份')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 显示产品列表
    if args.command == 'products':
        print_products()
        return
    
    # 隐私控制
    if args.command == 'privacy':
        try:
            if args.action == 'info':
                print_privacy_info()
            elif args.action == 'clear':
                removed = clear_local_data()
                print(
                    "✅ 已清除本地数据: "
                    f"history={removed['history']}, subscriptions={removed['subscriptions']}, "
                    f"addresses={removed['addresses']}, secure_files={removed['secure_files']}"
                )
            elif args.action == 'export':
                storage = get_secure_storage()
                info = storage.get_storage_info()
                export_file = CONFIG_DIR / 'privacy_export.json'
                payload = {
                    'config_dir': str(CONFIG_DIR),
                    'db_file': str(DB_FILE),
                    'db_exists': DB_FILE.exists(),
                    'secure_storage': info,
                }
                with open(export_file, 'w') as f:
                    json.dump(payload, f, indent=2)
                print(f"✅ 已导出到: {export_file}")
        except RuntimeError as e:
            print(f"❌ {e}")
        return
    
    # 初始化客户端
    async with SFExpressClient() as client:
        # 单号查询
        if args.command == 'query':
            try:
                result = await client.query(args.tracking_number, allow_mock=args.mock)
                print(client.format_tracking_result(result))
            except Exception as e:
                print(f"❌ 查询失败: {e}")
        
        # 批量查询
        elif args.command == 'batch':
            results = await client.batch_query(args.tracking_numbers, allow_mock=args.mock)
            for result in results:
                print(client.format_tracking_result(result))
                print("\n" + "="*50 + "\n")
        
        # 时效查询
        elif args.command == 'time':
            estimate = client.estimate_time(args.origin, args.destination, args.product)
            print(client.format_time_estimate(estimate))
        
        # 运费估算
        elif args.command == 'price':
            estimate = client.estimate_price(args.origin, args.destination, args.weight, args.product)
            print(client.format_price_estimate(estimate))
        
        # 历史记录
        elif args.command == 'history':
            print_history(client, args.limit, args.search)
        
        # 订阅
        elif args.command == 'subscribe':
            if client.subscribe(args.tracking_number):
                print(f"✅ 已订阅 {args.tracking_number} 的物流提醒")
        
        # 取消订阅
        elif args.command == 'unsubscribe':
            if client.unsubscribe(args.tracking_number):
                print(f"✅ 已取消 {args.tracking_number} 的订阅")
        
        # 订阅列表
        elif args.command == 'subscriptions':
            print_subscriptions(client)


if __name__ == '__main__':
    asyncio.run(main())
