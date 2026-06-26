import json
import os
import platform
import sqlite3
import yaml
import base64
import hashlib
from datetime import datetime


def get_skills_dir() -> str:
    """获取技能目录路径。"""
    home_dir = os.path.expanduser("~")
    return os.path.join(home_dir, ".hermes", "skills", "skill-factory")


def get_config_path() -> str:
    """获取配置文件路径。"""
    return os.path.join(get_skills_dir(), "configs", "config.yaml")


def get_db_path() -> str:
    """获取 SQLite 数据库路径。"""
    return os.path.join(get_skills_dir(), "data", "clawpraise.db")


def load_config() -> dict:
    """加载用户配置文件。"""
    config_path = get_config_path()
    if not os.path.isfile(config_path):
        raise RuntimeError(f"配置文件不存在: {config_path}，请先配置你的收款信息")
    
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_orders_base_dir(indicator: str) -> str:
    """
    根据操作系统返回固定的订单存储目录。
    Linux/macOS: ~/.openclaw/skills/orders/{indicator}/
    Windows:     ~/openclaw/skills/orders/{indicator}/
    """
    home_dir = os.path.expanduser("~")
    if platform.system() == "Windows":
        return os.path.join(home_dir, "openclaw", "skills", "orders", indicator)
    else:
        return os.path.join(home_dir, ".openclaw", "skills", "orders", indicator)


def load_order(indicator: str, order_no: str) -> dict:
    """根据 indicator 和 order_no 从固定目录读取订单 JSON 文件。"""
    base_dir = get_orders_base_dir(indicator)
    json_path = os.path.join(base_dir, f"{order_no}.json")
    if not os.path.isfile(json_path):
        raise RuntimeError(f"订单文件不存在: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_order(indicator: str, order_no: str, order_data: dict) -> str:
    """
    将订单数据写入固定目录: ~/.openclaw/skills/orders/{indicator}/{order_no}.json
    返回写入的文件完整路径。
    """
    base_dir = get_orders_base_dir(indicator)
    os.makedirs(base_dir, exist_ok=True)

    json_path = os.path.join(base_dir, f"{order_no}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(order_data, f, ensure_ascii=False, indent=2)

    return json_path


def get_db_connection():
    """获取 SQLite 数据库连接。"""
    db_path = get_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    # 创建订单表
    conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_no TEXT PRIMARY KEY,
            question TEXT,
            style TEXT,
            amount INTEGER,
            pay_to TEXT,
            order_status TEXT DEFAULT 'INIT',
            fulfill_status TEXT DEFAULT 'UNFULFILLED',
            finished_time TEXT,
            client_ip TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    # 创建履约记录表
    conn.execute('''
        CREATE TABLE IF NOT EXISTS fulfillment_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT,
            service_result TEXT,
            service_type TEXT,
            created_at TEXT,
            FOREIGN KEY (order_no) REFERENCES orders(order_no)
        )
    ''')
    conn.commit()
    return conn


def compute_indicator(slug: str) -> str:
    """根据 slug 计算 MD5 作为 indicator。"""
    return hashlib.md5(slug.encode("utf-8")).hexdigest()
