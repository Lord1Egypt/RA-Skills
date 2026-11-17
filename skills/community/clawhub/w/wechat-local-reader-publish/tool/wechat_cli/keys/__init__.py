"""密钥提取模块 — 根据平台调用对应的 scanner"""

import platform


def extract_keys(db_dir, output_path, pid=None, allow_resign=False):
    """提取微信数据库密钥并保存到 output_path。

    Args:
        db_dir: 微信数据库目录（db_storage）
        output_path: all_keys.json 输出路径
        pid: 可选，指定微信进程 PID（默认自动检测）
        allow_resign: macOS 下是否允许自动重签微信（仅 macOS 生效）

    Returns:
        dict: salt_hex -> enc_key_hex 的映射

    Raises:
        RuntimeError: 提取失败
    """
    system = platform.system().lower()
    if system == "darwin":
        from .scanner_macos import extract_keys as _extract
        return _extract(db_dir, output_path, pid=pid, allow_resign=allow_resign)
    elif system == "windows":
        from .scanner_windows import extract_keys as _extract
        return _extract(db_dir, output_path, pid=pid)
    elif system == "linux":
        from .scanner_linux import extract_keys as _extract
        return _extract(db_dir, output_path, pid=pid)
    else:
        raise RuntimeError(f"不支持的平台: {platform.system()}")
