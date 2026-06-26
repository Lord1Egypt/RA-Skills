"""
知识库管理模块（内部使用，不对外暴露解密细节）
"""
import os
import json
import zipfile
import hashlib
from pathlib import Path
from typing import Optional, Dict, List


class KnowledgeBaseManager:
    """
    知识库管理器 - 内部封装解密逻辑
    """
    
    def __init__(self, kb_path: Optional[str] = None):
        if kb_path is None:
            kb_path = Path.home() / ".zhang-xuefeng" / "knowledge_base"
        else:
            kb_path = Path(kb_path)
        
        self.kb_path = kb_path
        self.index_dir = kb_path / "index"
        self.raw_dir = kb_path / "raw"
        self._index = None
        
        # 尝试自动加载已解密的知识库
        self._try_load_index()
    
    def _try_load_index(self):
        """尝试加载索引文件"""
        index_file = self.index_dir / "index.json"
        if index_file.exists():
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    self._index = json.load(f)
            except Exception:
                self._index = None
    
    def is_activated(self) -> bool:
        """检查知识库是否已激活"""
        return self._index is not None
    
    def _decrypt_and_extract(self, encrypted_file: str, password: str) -> bool:
        """
        内部解密方法 - 不对外暴露
        """
        try:
            from Crypto.Cipher import AES
            from Crypto.Util.Padding import unpad
            
            # 从密码生成密钥
            key = hashlib.sha256(password.encode()).digest()
            
            # 读取加密文件
            with open(encrypted_file, 'rb') as f:
                iv = f.read(16)
                encrypted = f.read()
            
            # 解密
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            decrypted = cipher.decrypt(encrypted)
            data = unpad(decrypted, AES.block_size)
            
            # 保存临时 zip 文件
            temp_zip = self.kb_path / ".temp_package.zip"
            with open(temp_zip, 'wb') as f:
                f.write(data)
            
            # 解压到知识库目录
            with zipfile.ZipFile(temp_zip, 'r') as zf:
                zf.extractall(self.kb_path)
            
            # 删除临时文件
            os.remove(temp_zip)
            
            return True
            
        except Exception:
            return False
    
    def activate(self, password: str, package_file: Optional[str] = None) -> Dict:
        """
        激活知识库 - 用户只需提供密码
        """
        if self.is_activated():
            return {
                "success": True,
                "message": "知识库已经激活",
                "activated": True
            }
        
        # 查找加密包
        if package_file is None:
            for ext in ['.enc', '.zip.enc', '.encrypted']:
                candidate = self.kb_path / f"zhang-xuefeng-kb{ext}"
                if candidate.exists():
                    package_file = str(candidate)
                    break
        
        if not package_file or not os.path.exists(package_file):
            return {
                "success": False,
                "message": "未找到加密知识库包",
                "activated": False
            }
        
        # 解密
        if self._decrypt_and_extract(package_file, password):
            self._try_load_index()
            return {
                "success": True,
                "message": "知识库激活成功",
                "activated": self.is_activated()
            }
        else:
            return {
                "success": False,
                "message": "激活失败，密码错误",
                "activated": False
            }
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        搜索知识库
        """
        if not self.is_activated():
            return []
        
        # 简单的关键词匹配
        query_lower = query.lower()
        documents = self._index.get("documents", [])
        keyword_index = self._index.get("keyword_index", {})
        
        # 计算相关性得分
        doc_scores = {}
        
        # 关键词匹配
        for category, doc_ids in keyword_index.items():
            if category in query_lower:
                for doc_id in doc_ids:
                    doc_scores[doc_id] = doc_scores.get(doc_id, 0) + 1
        
        # 文本匹配
        for i, doc in enumerate(documents):
            text = (doc.get("text", "") + " " + doc.get("title", "")).lower()
            for word in query_lower.split():
                if len(word) > 1:
                    count = text.count(word)
                    if count > 0:
                        doc_scores[i] = doc_scores.get(i, 0) + count * 0.5
        
        # 排序并返回前 top_k
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for doc_id, score in sorted_docs[:top_k]:
            if 0 <= doc_id < len(documents):
                doc = documents[doc_id].copy()
                doc["score"] = score
                results.append(doc)
        
        return results
    
    def get_context(self, query: str, max_length: int = 1000) -> str:
        """
        获取查询相关的上下文
        """
        results = self.search(query, top_k=3)
        
        if not results:
            return ""
        
        context_parts = []
        current_length = 0
        
        for doc in results:
            text = doc.get("text", "").strip()
            if not text:
                continue
            
            if len(text) > 200:
                text = text[:200] + "..."
            
            part = f"[参考内容] {text}\n"
            
            if current_length + len(part) > max_length:
                break
            
            context_parts.append(part)
            current_length += len(part)
        
        return "\n".join(context_parts)


# 全局管理器实例
_kb_manager = None


def get_kb_manager() -> KnowledgeBaseManager:
    """获取知识库管理器单例"""
    global _kb_manager
    if _kb_manager is None:
        _kb_manager = KnowledgeBaseManager()
    return _kb_manager


def activate_kb(password: str) -> Dict:
    """便捷函数：激活知识库"""
    manager = get_kb_manager()
    return manager.activate(password)


def is_kb_activated() -> bool:
    """便捷函数：检查知识库是否已激活"""
    manager = get_kb_manager()
    return manager.is_activated()


def search_kb(query: str, top_k: int = 5) -> List[Dict]:
    """便捷函数：搜索知识库"""
    manager = get_kb_manager()
    return manager.search(query, top_k)


def get_kb_context(query: str) -> str:
    """便捷函数：获取知识库上下文"""
    manager = get_kb_manager()
    return manager.get_context(query)
