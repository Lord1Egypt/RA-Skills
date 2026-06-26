from typing import Dict, List, Optional
"""结果解释 - LLM 生成结果解释"""
import json
import urllib.request
from typing import List, Dict, Optional

class ResultExplainer:
    def __init__(self, url: str, key: str, uid: str, model: str = "LLM_GLM5"):
        self.url = url
        self.key = key
        self.uid = uid
        self.model = model
    
    def explain(self, query: str, results: List[Dict]) -> Optional[str]:
        """生成结果解释"""
        if not results:
            return "未找到相关记忆。"
        
        # 构建结果摘要
        results_text = "\n".join([
            f"{i+1}. [{r.get('type', '?')}] {r.get('content', '')[:80]}..."
            for i, r in enumerate(results[:5])
        ])
        
        prompt = f"""请用一句话解释为什么以下记忆与查询"{query}"相关：

{results_text}

解释（一句话）："""
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100,
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
            
            return content if content else None
        except:
            return None
    
    @staticmethod
    def format_explanation(query: str, results: List[Dict], explanation: Optional[str]) -> str:
        """格式化解释"""
        if explanation:
            return f"💡 {explanation}"
        
        # 简单解释
        if results:
            types = set(r.get('type', 'unknown') for r in results)
            return f"💡 找到 {len(results)} 条相关记忆，类型：{', '.join(types)}"
        
        return "💡 未找到相关记忆"
