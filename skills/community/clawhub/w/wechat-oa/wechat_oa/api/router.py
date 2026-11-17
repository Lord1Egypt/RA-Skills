from functools import wraps
from typing import Callable


def _is_ip_whitelist_error(e: Exception) -> bool:
    err_msg = str(e).lower()
    ip_keywords = ["ip", "whitelist", "白名单", "40164", "40013", "invalid ip"]
    return any(kw in err_msg for kw in ip_keywords)


def hybrid_route(direct_func: Callable, relay_func: Callable) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            from wechat_oa.core.config import load_config
            
            cfg = load_config()
            push_mode = cfg.get("PUSH_MODE", "direct")
            
            if push_mode == "hybrid":
                try:
                    return direct_func(*args, **kwargs)
                except Exception as e:
                    if _is_ip_whitelist_error(e):
                        return relay_func(*args, **kwargs)
                    raise
            
            if push_mode == "relay":
                return relay_func(*args, **kwargs)
            
            return direct_func(*args, **kwargs)
        
        return wrapper
    return decorator
