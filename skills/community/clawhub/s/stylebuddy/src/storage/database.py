"""
SQLite 数据库模块
管理所有本地数据存储
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any

class Database:
    """SQLite 数据库管理器"""
    
    def __init__(self, db_path: str = "./assets/data/wardrobe.db"):
        self.db_path = db_path
        self._ensure_dir()
        self._init_tables()
    
    def _ensure_dir(self):
        """确保目录存在"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_tables(self):
        """初始化数据表"""
        with self._get_connection() as conn:
            # 单品表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,  -- outer/top/bottom/shoes/accessory
                    color TEXT,
                    style TEXT,
                    season TEXT,
                    material TEXT,
                    image_path TEXT,
                    tags TEXT,  -- JSON array
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 穿搭记录表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS outfits (
                    id TEXT PRIMARY KEY,
                    date DATE NOT NULL,
                    items TEXT NOT NULL,  -- JSON array of item_ids
                    occasion TEXT,
                    weather TEXT,  -- JSON object
                    notes TEXT,
                    rating INTEGER,  -- 1-5 stars
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 用户偏好表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 搭配模板使用记录
            conn.execute("""
                CREATE TABLE IF NOT EXISTS template_usage (
                    template_id TEXT PRIMARY KEY,
                    use_count INTEGER DEFAULT 0,
                    last_used DATE,
                    liked BOOLEAN DEFAULT 0
                )
            """)
            
            # 种草清单表（逛街看中但未购买的衣服）
            conn.execute("""
                CREATE TABLE IF NOT EXISTS wishlist (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT,
                    color TEXT,
                    style TEXT,
                    material TEXT,
                    price TEXT,
                    brand TEXT,
                    image_path TEXT,
                    reason TEXT,  -- 想买的原因/备注
                    store_location TEXT,  -- 店铺位置
                    purchased BOOLEAN DEFAULT 0,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    purchased_at TIMESTAMP
                )
            """)
            
            conn.commit()
    
    # ===== 单品操作 =====
    
    def add_item(self, item: Dict[str, Any]) -> str:
        """添加单品，自动检测重复"""
        import uuid
        
        # 检查是否已存在（根据名称和颜色）
        existing = self._find_duplicate(item)
        if existing:
            # 更新而不是新建
            item_id = existing['id']
            self.update_item(item_id, item)
            return item_id
        
        item_id = item.get('id') or f"item_{uuid.uuid4().hex[:8]}"
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO items (id, name, category, color, style, season, material, image_path, tags, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item_id,
                item.get('name', ''),
                item.get('category', ''),
                item.get('color', ''),
                item.get('style', ''),
                item.get('season', ''),
                item.get('material', ''),
                item.get('image_path', ''),
                json.dumps(item.get('tags', []), ensure_ascii=False),
                datetime.now().isoformat()
            ))
            conn.commit()
        
        return item_id
    
    def _find_duplicate(self, item: Dict) -> Optional[Dict]:
        """查找重复单品"""
        name = item.get('name', '')
        color = item.get('color', '')
        category = item.get('category', '')
        
        with self._get_connection() as conn:
            # 检查名称、颜色、类别完全匹配
            cursor = conn.execute("""
                SELECT * FROM items 
                WHERE name = ? AND color = ? AND category = ?
            """, (name, color, category))
            
            row = cursor.fetchone()
            if row:
                return self._row_to_dict(row)
        
        return None
    
    def get_item(self, item_id: str) -> Optional[Dict]:
        """获取单品详情"""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM items WHERE id = ?", (item_id,)
            ).fetchone()
            
            if row:
                return self._row_to_dict(row)
            return None
    
    def get_all_items(self, category: str = None) -> List[Dict]:
        """获取所有单品"""
        with self._get_connection() as conn:
            if category:
                rows = conn.execute(
                    "SELECT * FROM items WHERE category = ? ORDER BY created_at DESC",
                    (category,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM items ORDER BY created_at DESC"
                ).fetchall()
            
            return [self._row_to_dict(row) for row in rows]
    
    def update_item(self, item_id: str, updates: Dict[str, Any]) -> bool:
        """更新单品"""
        allowed_fields = ['name', 'category', 'color', 'style', 'season', 'material', 'image_path', 'tags']
        fields = []
        values = []
        
        for key, value in updates.items():
            if key in allowed_fields:
                fields.append(f"{key} = ?")
                if key == 'tags':
                    values.append(json.dumps(value, ensure_ascii=False))
                else:
                    values.append(value)
        
        if not fields:
            return False
        
        fields.append("updated_at = ?")
        values.append(datetime.now().isoformat())
        values.append(item_id)
        
        with self._get_connection() as conn:
            conn.execute(
                f"UPDATE items SET {', '.join(fields)} WHERE id = ?",
                values
            )
            conn.commit()
        
        return True
    
    def delete_item(self, item_id: str) -> bool:
        """删除单品"""
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def search_items(self, query: str) -> List[Dict]:
        """搜索单品"""
        with self._get_connection() as conn:
            pattern = f"%{query}%"
            rows = conn.execute("""
                SELECT * FROM items 
                WHERE name LIKE ? OR color LIKE ? OR style LIKE ? OR tags LIKE ?
                ORDER BY created_at DESC
            """, (pattern, pattern, pattern, pattern)).fetchall()
            
            return [self._row_to_dict(row) for row in rows]
    
    # ===== 穿搭记录操作 =====
    
    def add_outfit(self, outfit: Dict[str, Any]) -> str:
        """添加穿搭记录"""
        import uuid
        outfit_id = outfit.get('id') or f"outfit_{uuid.uuid4().hex[:8]}"
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO outfits (id, date, items, occasion, weather, notes, rating)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                outfit_id,
                outfit.get('date', datetime.now().strftime('%Y-%m-%d')),
                json.dumps(outfit.get('items', []), ensure_ascii=False),
                outfit.get('occasion', ''),
                json.dumps(outfit.get('weather', {}), ensure_ascii=False),
                outfit.get('notes', ''),
                outfit.get('rating', 0)
            ))
            conn.commit()
        
        return outfit_id
    
    def get_outfits(self, date: str = None, limit: int = 100) -> List[Dict]:
        """获取穿搭记录"""
        with self._get_connection() as conn:
            if date:
                rows = conn.execute(
                    "SELECT * FROM outfits WHERE date = ? ORDER BY date DESC LIMIT ?",
                    (date, limit)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM outfits ORDER BY date DESC LIMIT ?",
                    (limit,)
                ).fetchall()
            
            return [self._row_to_dict(row) for row in rows]
    
    def get_calendar_outfits(self, year: int, month: int) -> Dict[str, Dict]:
        """获取日历视图穿搭记录"""
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{(month+1):02d}-01"
        
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM outfits 
                WHERE date >= ? AND date < ?
                ORDER BY date
            """, (start_date, end_date)).fetchall()
            
            return {row['date']: self._row_to_dict(row) for row in rows}
    
    # ===== 用户偏好操作 =====
    
    def set_preference(self, key: str, value: str):
        """设置用户偏好"""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO preferences (key, value, updated_at)
                VALUES (?, ?, ?)
            """, (key, value, datetime.now().isoformat()))
            conn.commit()
    
    def get_preference(self, key: str, default: str = None) -> str:
        """获取用户偏好"""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT value FROM preferences WHERE key = ?", (key,)
            ).fetchone()
            
            return row['value'] if row else default
    
    def get_all_preferences(self) -> Dict[str, str]:
        """获取所有偏好"""
        with self._get_connection() as conn:
            rows = conn.execute("SELECT key, value FROM preferences").fetchall()
            return {row['key']: row['value'] for row in rows}
    
    # ===== 统计信息 =====
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self._get_connection() as conn:
            # 单品统计
            item_count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
            
            # 分类统计
            cat_stats = conn.execute(
                "SELECT category, COUNT(*) as count FROM items GROUP BY category"
            ).fetchall()
            
            # 穿搭记录统计
            outfit_count = conn.execute("SELECT COUNT(*) FROM outfits").fetchone()[0]
            
            # 颜色统计
            color_stats = conn.execute(
                "SELECT color, COUNT(*) as count FROM items WHERE color IS NOT NULL GROUP BY color"
            ).fetchall()
            
            return {
                "total_items": item_count,
                "total_outfits": outfit_count,
                "by_category": {row['category']: row['count'] for row in cat_stats},
                "by_color": {row['color']: row['count'] for row in color_stats}
            }
    
    # ===== 备份/恢复 =====
    
    def export_data(self) -> Dict[str, Any]:
        """导出所有数据"""
        return {
            "items": self.get_all_items(),
            "outfits": self.get_outfits(),
            "preferences": self.get_all_preferences(),
            "exported_at": datetime.now().isoformat()
        }
    
    def import_data(self, data: Dict[str, Any]) -> Dict[str, int]:
        """导入数据"""
        counts = {"items": 0, "outfits": 0}
        
        with self._get_connection() as conn:
            # 导入单品
            for item in data.get('items', []):
                try:
                    conn.execute("""
                        INSERT OR REPLACE INTO items 
                        (id, name, category, color, style, season, material, image_path, tags, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        item.get('id'), item.get('name'), item.get('category'),
                        item.get('color'), item.get('style'), item.get('season'),
                        item.get('material'), item.get('image_path'),
                        json.dumps(item.get('tags', [])),
                        item.get('created_at'), item.get('updated_at')
                    ))
                    counts["items"] += 1
                except:
                    pass
            
            # 导入穿搭记录
            for outfit in data.get('outfits', []):
                try:
                    conn.execute("""
                        INSERT OR REPLACE INTO outfits 
                        (id, date, items, occasion, weather, notes, rating, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        outfit.get('id'), outfit.get('date'),
                        json.dumps(outfit.get('items', [])),
                        outfit.get('occasion'),
                        json.dumps(outfit.get('weather', {})),
                        outfit.get('notes'), outfit.get('rating'),
                        outfit.get('created_at')
                    ))
                    counts["outfits"] += 1
                except:
                    pass
            
            conn.commit()
        
        return counts
    
    # ===== 辅助方法 =====
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict:
        """将行转换为字典"""
        result = dict(row)
        
        # 解析 JSON 字段
        for key in ['tags', 'items', 'weather']:
            if key in result and result[key]:
                try:
                    result[key] = json.loads(result[key])
                except:
                    pass
        
        return result


    # ===== 种草清单操作 =====
    
    def add_to_wishlist(self, item: Dict) -> str:
        """添加商品到种草清单"""
        import uuid
        item_id = str(uuid.uuid4())[:8]
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO wishlist (id, name, category, color, style, material,
                                    price, brand, image_path, reason, store_location, added_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item_id,
                item.get('name', ''),
                item.get('category', ''),
                item.get('color', ''),
                item.get('style', ''),
                item.get('material', ''),
                item.get('price', ''),
                item.get('brand', ''),
                item.get('image_path', ''),
                item.get('reason', ''),
                item.get('store_location', ''),
                datetime.now().isoformat()
            ))
            conn.commit()
        
        return item_id
    
    def get_wishlist(self, purchased: bool = None) -> List[Dict]:
        """获取种草清单"""
        with self._get_connection() as conn:
            if purchased is None:
                rows = conn.execute(
                    "SELECT * FROM wishlist ORDER BY added_at DESC"
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM wishlist WHERE purchased = ? ORDER BY added_at DESC",
                    (purchased,)
                ).fetchall()
            
            return [self._row_to_dict(row) for row in rows]
    
    def mark_wishlist_purchased(self, item_id: str) -> bool:
        """标记种草商品为已购买"""
        with self._get_connection() as conn:
            result = conn.execute("""
                UPDATE wishlist 
                SET purchased = 1, purchased_at = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), item_id))
            conn.commit()
            return result.rowcount > 0
    
    def delete_from_wishlist(self, item_id: str) -> bool:
        """从种草清单删除"""
        with self._get_connection() as conn:
            result = conn.execute("DELETE FROM wishlist WHERE id = ?", (item_id,))
            conn.commit()
            return result.rowcount > 0
