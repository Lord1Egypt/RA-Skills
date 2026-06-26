import json
import re
from typing import Any, Dict, Optional

def safe_parse_json(raw: str, default: Optional[Dict] = None) -> Dict[str, Any]:
    """鲁棒性极强的 JSON 解析器，专门应对 LLM 幻觉格式"""
    if default is None:
        default = {}
    if not raw or not raw.strip():
        return default
    
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        pass

    match = re.search(r'(\{.*\}|\[.*\])', raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except:
            pass

    cleaned = re.sub(r',\s*}', '}', raw)
    cleaned = re.sub(r',\s*]', ']', cleaned)
    cleaned = cleaned.replace("'", '"')
    cleaned = re.sub(r'//.*?[\n\r]', '', cleaned)
    
    try:
        return json.loads(cleaned)
    except:
        return default