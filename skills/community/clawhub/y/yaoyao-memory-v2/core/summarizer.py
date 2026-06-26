"""结果摘要生成"""
import json
import urllib.request
from typing import List, Dict, Optional

class ResultSummarizer:
    def __init__(self, url: str, key: str, uid: str, model: str = "LLM_GLM5"):
        self.url = url
        self.key = key
        self.uid = uid
        self.model = model
    
    def summarize(self, query: str, results: List[Dict], max_length: int = 200) -> Optional[str]:
        """生成结果摘要"""
        if not results:
            return None
        
        # 构建内容摘要
        contents = []
        for i, r in enumerate(results[:5], 1):
            content = r.get("content", "")[:150]
            contents.append(f"{i}. {content}")
        
        prompt = f"""请为以下搜索结果生成一个简洁摘要（{max_length}字以内）：

查询: {query}

结果:
{chr(10).join(contents)}

摘要:"""
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 150,
            "temperature": 0.3,
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
            with urllib.request.urlopen(req, timeout=20) as resp:
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
            
            return content[:max_length] if content else None
        except:
            return None
    
    @staticmethod
    def quick_summary(results: List[Dict]) -> str:
        """快速摘要（无LLM）"""
        if not results:
            return "未找到相关记忆"
        
        types = {}
        for r in results:
            t = r.get("type", "unknown")
            types[t] = types.get(t, 0) + 1
        
        type_str = ", ".join([f"{t}({c}条)" for t, c in types.items()])
        
        return f"找到{len(results)}条记忆: {type_str}"
