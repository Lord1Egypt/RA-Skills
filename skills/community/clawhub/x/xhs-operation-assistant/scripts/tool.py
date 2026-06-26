import base64
import time
def get_dynamic_key():
    """
    使用 UTC Unix 时间戳生成 Key。
    无论用户在美国还是中国，只要系统时间大致准确，算出来的 Seed 就是一样的。
    """
    # 86400 是一天的秒数
    # 使用 UTC 时间戳，彻底消除时区差异
    seed = int(time.time()) // 86400
    # 这里的 base_key 是你的私有盐值
    base_key = "sardinesinqianhai"
    # 混合生成最终密钥
    dynamic_part = str(seed * 31)
    return (base_key + dynamic_part).encode('utf-8')

def xor_encrypt(text: str) -> str:
    data = text.encode('utf-8')
    key = get_dynamic_key()
    encrypted = bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
    return base64.b64encode(encrypted).decode('utf-8')

def xor_decrypt(encoded: str) -> str:
    try:
        encrypted = base64.b64decode(encoded)
        key = get_dynamic_key()
        decrypted = bytes([encrypted[i] ^ key[i % len(key)] for i in range(len(encrypted))])
        return decrypted.decode('utf-8')
    except Exception as e:
        return f"解密失败: {e}"