from typing import Optional, List
"""LLM 引擎 - 支持响应缓存"""
import json
import hashlib
import urllib.request
from pathlib import Path
from typing import List, Optional

class LLMEngine:
    def __init__(self, url: str, key: str, uid: str, model: str = "LLM_GLM5"):
        self.url = url
        self.key = key
        self.uid = uid
        self.model = model
        self.cache_dir = Path.home() / ".openclaw" / "memory-tdai" / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _hash(self, text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()
    
    def _get_cache(self, key: str) -> Optional[str]:
        file = self.cache_dir / f"llm_{key}.json"
        if file.exists():
            try:
                data = json.loads(file.read_text())
                return data.get("content")
            except:
                pass
        return None
    
    def _set_cache(self, key: str, content: str):
        file = self.cache_dir / f"llm_{key}.json"
        file.write_text(json.dumps({"content": content}))
    
    def chat(self, prompt: str, max_tokens: int = 100, temperature: float = 0.3, use_cache: bool = True) -> Optional[str]:
        """对话（支持缓存）"""
        key = self._hash(prompt)
        
        if use_cache:
            cached = self._get_cache(key)
            if cached:
                return cached
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "x-request-from": "openclaw",
            "x-uid": self.uid,
            "x-api-key": self.key
        }
        
        try:
            req = urllib.request.Request(
                self.url, data=json.dumps(data).encode('utf-8'),
                headers=headers, method='POST'
            )
            
            content = ""
            with urllib.request.urlopen(req, timeout=30) as resp:
                for line in resp:
                    line = line.decode('utf-8').strip()
                    if line.startswith('data: '):
                        try:
                            chunk = json.loads(line[6:])
                            if 'choices' in chunk:
                                delta = chunk['choices'][0].get('delta', {})
                                content += delta.get('content', '')
                        except:
                            pass
            
            if content and use_cache:
                self._set_cache(key, content)
            
            return content if content else None
        except:
            return None
    
    def expand_query(self, query: str) -> List[str]:
        """查询扩展（优化：更精准的扩展词生成）"""
        prompt = f"""请为以下查询生成3个语义相关的搜索词，用于记忆检索系统。

要求：
1. 保持原查询的核心意图
2. 使用同义词或相关概念
3. 每行一个，不要编号

查询: {query}

搜索词:"""
        result = self.chat(prompt, max_tokens=150, temperature=0.5)
        if result:
            expansions = [l.strip() for l in result.split('\n') if l.strip() and len(l.strip()) > 2][:5]
            return expansions
        return [query]
    
    def rerank(self, query: str, results: List[dict]) -> List[dict]:
        """重排序"""
        if len(results) <= 1:
            return results
        
        text = "\n".join([f"{i+1}. [{r['type']}] {r['content'][:60]}..." for i, r in enumerate(results[:8])])
        prompt = f"根据查询'{query}'对以下结果排序，返回编号列表（逗号分隔）：\n{text}"
        
        result = self.chat(prompt, max_tokens=50, temperature=0.1)
        if result:
            try:
                order = [int(x.strip()) - 1 for x in result.split(',') if x.strip().isdigit()]
                if order and max(order) < len(results):
                    return [results[i] for i in order if i < len(results)]
            except:
                pass
        
        return results
