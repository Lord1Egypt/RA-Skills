"""搜索引擎 - 向量 + FTS（安全修复版）"""
import sqlite3
import struct
import re
from pathlib import Path
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor

class SearchEngine:
    def __init__(self, db_path: str, vec_ext: str):
        self.db_path = db_path
        self.vec_ext = vec_ext
    
    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接（安全方式）"""
        conn = sqlite3.connect(self.db_path)
        conn.enable_load_extension(True)
        # 验证扩展路径
        if not Path(self.vec_ext).exists():
            raise ValueError(f"Invalid extension path: {self.vec_ext}")
        conn.load_extension(self.vec_ext)
        return conn
    
    def vector_search(self, embedding: List[float], top_k: int = 20, max_distance: float = 0.8) -> List[dict]:
        """向量搜索（安全修复：使用 sqlite3 直接连接）"""
        if not embedding:
            return []
        
        # 验证 top_k
        if not isinstance(top_k, int) or top_k < 1 or top_k > 100:
            top_k = 20
        
        vec_hex = struct.pack(f'{len(embedding)}f', *embedding).hex()
        
        # 使用参数化查询（安全）
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # 使用参数化查询
            sql = """
                SELECT v.record_id, r.content, r.type, r.scene_name, v.distance 
                FROM l1_vec v 
                JOIN l1_records r ON v.record_id = r.record_id 
                WHERE v.embedding MATCH ? AND k = ? 
                ORDER BY v.distance ASC
            """
            cursor.execute(sql, (f"X'{vec_hex}'", top_k))
            results = cursor.fetchall()
            
            return self._parse_vector_results_safe(results, max_distance)
        except Exception as e:
            print(f"Vector search error: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def fts_search(self, query: str, top_k: int = 10) -> List[dict]:
        """FTS 搜索（安全修复：输入验证 + 参数化查询）"""
        # 输入验证：只允许安全字符
        query = re.sub(r'[^\w\u4e00-\u9fff\s]', '', query)
        
        # 验证 top_k
        if not isinstance(top_k, int) or top_k < 1 or top_k > 100:
            top_k = 10
        
        tokens = query.replace('，', ' ').replace('、', ' ').split()
        tokens = [t for t in tokens if len(t) > 0]  # 过滤空字符串
        
        if not tokens:
            return []
        
        fts_query = " OR ".join(tokens)
        
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 使用参数化查询（安全）
            sql = """
                SELECT record_id, content, type, scene_name 
                FROM l1_fts 
                WHERE l1_fts MATCH ? 
                ORDER BY rank 
                LIMIT ?
            """
            cursor.execute(sql, (fts_query, top_k))
            results = cursor.fetchall()
            
            return self._parse_fts_results_safe(results)
        except Exception as e:
            print(f"FTS search error: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def parallel_search(self, embedding: List[float], query: str) -> tuple:
        """并行搜索"""
        with ThreadPoolExecutor(max_workers=2) as executor:
            f1 = executor.submit(self.vector_search, embedding)
            f2 = executor.submit(self.fts_search, query)
            return f1.result(), f2.result()
    
    def _parse_vector_results_safe(self, results: List[tuple], max_distance: float = 0.8) -> List[dict]:
        """解析向量结果（安全版本）"""
        parsed = []
        for row in results:
            if len(row) >= 5:
                try:
                    dist = float(row[4])
                    if dist < max_distance:
                        parsed.append({
                            "record_id": str(row[0]),
                            "content": str(row[1]),
                            "type": str(row[2]),
                            "scene": str(row[3]),
                            "distance": dist,
                            "score": 1.0 - dist,
                            "source": "vector"
                        })
                except (ValueError, TypeError):
                    pass
        return parsed
    
    def _parse_fts_results_safe(self, results: List[tuple]) -> List[dict]:
        """解析 FTS 结果（安全版本）"""
        parsed = []
        for row in results:
            if len(row) >= 4:
                parsed.append({
                    "record_id": str(row[0]),
                    "content": str(row[1]),
                    "type": str(row[2]),
                    "scene": str(row[3]),
                    "source": "fts"
                })
        return parsed
    
    @staticmethod
    def merge(vector_results: List[dict], fts_results: List[dict]) -> List[dict]:
        """合并去重"""
        seen = set()
        merged = []
        
        for r in vector_results:
            if r["record_id"] not in seen:
                merged.append(r)
                seen.add(r["record_id"])
        
        for r in fts_results:
            if r["record_id"] not in seen:
                merged.append(r)
                seen.add(r["record_id"])
        
        merged.sort(key=lambda x: x.get("score", 0), reverse=True)
        return merged
