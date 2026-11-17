"""配置加载 — 从 ~/.wechat-cli/ 读取自包含配置"""

import glob as glob_mod
import json
import os
import platform
import sys

_SYSTEM = platform.system().lower()

if _SYSTEM == "linux":
    _DEFAULT_PROCESS = "wechat"
elif _SYSTEM == "darwin":
    _DEFAULT_PROCESS = "WeChat"
else:
    _DEFAULT_PROCESS = "Weixin.exe"

# CLI 状态目录
STATE_DIR = os.path.expanduser("~/.wechat-cli")
CONFIG_FILE = os.path.join(STATE_DIR, "config.json")
KEYS_FILE = os.path.join(STATE_DIR, "all_keys.json")


def _choose_candidate(candidates):
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        if not sys.stdin.isatty():
            return candidates[0]
        print("[!] 检测到多个微信数据目录:")
        for i, c in enumerate(candidates, 1):
            print(f"    {i}. {c}")
        print("    0. 跳过")
        try:
            while True:
                choice = input(f"请选择 [0-{len(candidates)}]: ").strip()
                if choice == "0":
                    return None
                if choice.isdigit() and 1 <= int(choice) <= len(candidates):
                    return candidates[int(choice) - 1]
                print("    无效输入")
        except (EOFError, KeyboardInterrupt):
            print()
            return None
    return None


def _get_known_documents_dir():
    """通过 Win32 Known-Folder API 解析真实“文档”目录。

    Windows 在开启 OneDrive 同步时会把“文档”重定向到 OneDrive 下的本地化目录
    （如 OneDrive/文档），此时 os.path.expanduser('~/Documents') 往往失效。
    用 SHGetKnownFolderPath(FOLDERID_Documents) 才能拿到真实路径。
    """
    try:
        from ctypes import wintypes
        FOLDERID_Documents = "{FDD39AD0-238F-46AF-ADB4-6C85480369C7}"
        shell32 = ctypes.windll.shell32
        SHGetKnownFolderPath = shell32.SHGetKnownFolderPath
        SHGetKnownFolderPath.argtypes = [
            ctypes.c_wchar_p, ctypes.c_uint32, wintypes.HANDLE,
            ctypes.POINTER(ctypes.c_wchar_p),
        ]
        SHGetKnownFolderPath.restype = ctypes.c_int32
        p_path = ctypes.c_wchar_p()
        hr = SHGetKnownFolderPath(FOLDERID_Documents, 0, None, ctypes.byref(p_path))
        if hr == 0 and p_path.value:
            path = p_path.value
            ctypes.windll.ole32.CoTaskMemFree(p_path)
            return path
    except Exception:
        pass
    return None


def _auto_detect_db_dir_windows():
    appdata = os.environ.get("APPDATA", "")
    config_dir = os.path.join(appdata, "Tencent", "xwechat", "config")
    data_roots = []

    # 1) 读取微信本地 ini 配置定位数据根目录
    if os.path.isdir(config_dir):
        for ini_file in glob_mod.glob(os.path.join(config_dir, "*.ini")):
            try:
                content = None
                for enc in ("utf-8", "gbk"):
                    try:
                        with open(ini_file, "r", encoding=enc) as f:
                            content = f.read(1024).strip()
                        break
                    except UnicodeDecodeError:
                        continue
                if not content or any(c in content for c in "\n\r\x00"):
                    continue
                # 微信在“我的文档”模式下 ini 可能只写占位符（如 `MyDocument:`），
                # 此时回退到 Known-Folder 解析出的真实文档目录
                if content.lower().startswith("mydocument"):
                    doc = _get_known_documents_dir()
                    if doc and os.path.isdir(doc) and doc not in data_roots:
                        data_roots.append(doc)
                elif os.path.isdir(content) and content not in data_roots:
                    data_roots.append(content)
            except OSError:
                continue

    # 2) 兜底：直接搜索常见文档根（含 OneDrive 同步目录与本地化“文档”）
    fallback_roots = []
    doc = _get_known_documents_dir()
    if doc:
        fallback_roots.append(doc)
    onedrive = os.environ.get("OneDrive", "")
    if onedrive:
        fallback_roots.append(onedrive)
        fallback_roots.append(os.path.join(onedrive, "Documents"))
    legacy_doc = os.path.expanduser("~/Documents")
    if legacy_doc:
        fallback_roots.append(legacy_doc)
    for r in fallback_roots:
        if r and os.path.isdir(r) and r not in data_roots:
            data_roots.append(r)

    seen = set()
    candidates = []
    for root in data_roots:
        # 同时支持两种布局：
        #   <root>/xwechat_files/<账号>/db_storage        （文档重定向未生效时）
        #   <root>/<本地化文档目录>/xwechat_files/<账号>/db_storage  （OneDrive 重定向，如 文档）
        for pattern in (
            os.path.join(root, "xwechat_files", "*", "db_storage"),
            os.path.join(root, "*", "xwechat_files", "*", "db_storage"),
        ):
            for match in glob_mod.glob(pattern):
                normalized = os.path.normcase(os.path.normpath(match))
                if os.path.isdir(match) and normalized not in seen:
                    seen.add(normalized)
                    candidates.append(match)
    return _choose_candidate(candidates)


def _auto_detect_db_dir_linux():
    seen = set()
    candidates = []
    search_roots = [os.path.expanduser("~/Documents/xwechat_files")]
    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        import pwd
        try:
            sudo_home = pwd.getpwnam(sudo_user).pw_dir
        except KeyError:
            sudo_home = None
        if sudo_home:
            fallback = os.path.join(sudo_home, "Documents", "xwechat_files")
            if fallback not in search_roots:
                search_roots.append(fallback)
    for root in search_roots:
        if not os.path.isdir(root):
            continue
        pattern = os.path.join(root, "*", "db_storage")
        for match in glob_mod.glob(pattern):
            normalized = os.path.normcase(os.path.normpath(match))
            if os.path.isdir(match) and normalized not in seen:
                seen.add(normalized)
                candidates.append(match)
    old_path = os.path.expanduser("~/.local/share/weixin/data/db_storage")
    if os.path.isdir(old_path):
        normalized = os.path.normcase(os.path.normpath(old_path))
        if normalized not in seen:
            candidates.append(old_path)

    def _mtime(path):
        msg_dir = os.path.join(path, "message")
        target = msg_dir if os.path.isdir(msg_dir) else path
        try:
            return os.path.getmtime(target)
        except OSError:
            return 0
    candidates.sort(key=_mtime, reverse=True)
    return _choose_candidate(candidates)


def _auto_detect_db_dir_macos():
    base = os.path.expanduser("~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files")
    if not os.path.isdir(base):
        return None
    seen = set()
    candidates = []
    pattern = os.path.join(base, "*", "db_storage")
    for match in glob_mod.glob(pattern):
        normalized = os.path.normcase(os.path.normpath(match))
        if os.path.isdir(match) and normalized not in seen:
            seen.add(normalized)
            candidates.append(match)
    return _choose_candidate(candidates)


def auto_detect_db_dir():
    if _SYSTEM == "windows":
        return _auto_detect_db_dir_windows()
    if _SYSTEM == "linux":
        return _auto_detect_db_dir_linux()
    if _SYSTEM == "darwin":
        return _auto_detect_db_dir_macos()
    return None


def load_config(config_path=None):
    """加载配置。默认从 ~/.wechat-cli/config.json 读取。"""
    if config_path is None:
        config_path = CONFIG_FILE

    cfg = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, encoding="utf-8") as f:
                cfg = json.load(f)
        except json.JSONDecodeError:
            cfg = {}

    # db_dir 缺失时，自动检测
    db_dir = cfg.get("db_dir", "")
    if not db_dir:
        detected = auto_detect_db_dir()
        if detected:
            cfg["db_dir"] = detected
        else:
            raise FileNotFoundError(
                "未找到微信数据目录。\n"
                "请运行: wechat-cli init"
            )

    # 设置默认值
    state_dir = os.path.dirname(os.path.abspath(config_path))
    cfg.setdefault("keys_file", os.path.join(state_dir, "all_keys.json"))
    cfg.setdefault("decrypted_dir", os.path.join(state_dir, "decrypted"))
    cfg.setdefault("decoded_image_dir", os.path.join(state_dir, "decoded_images"))
    cfg.setdefault("wechat_process", _DEFAULT_PROCESS)

    # 所有路径确保为绝对路径
    for key in ("db_dir", "keys_file", "decrypted_dir", "decoded_image_dir"):
        if key in cfg and not os.path.isabs(cfg[key]):
            cfg[key] = os.path.join(state_dir, cfg[key])

    # 推导微信数据根目录
    db_dir = cfg.get("db_dir", "")
    if db_dir and os.path.basename(db_dir) == "db_storage":
        cfg["wechat_base_dir"] = os.path.dirname(db_dir)
    else:
        cfg["wechat_base_dir"] = db_dir

    return cfg
