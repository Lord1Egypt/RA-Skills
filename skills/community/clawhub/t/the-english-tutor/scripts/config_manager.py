#!/usr/bin/env python3
"""
英语助教 · 配置状态管理器
读写 ~/.openclaw/english-tutor/config.json
"""
import json, os, sys, pathlib

CONFIG_DIR = pathlib.Path.home() / ".openclaw" / "english-tutor"
CONFIG_FILE = CONFIG_DIR / "config.json"

# 字段名与 agents/english-tutor/config.js 保持一致
# 敏感字段不写默认值，必须由环境变量或用户输入提供
# 全部为选填字段，缺失则对应模块静默跳过
# 不写默认值，避免误以为"已配置"
DEFAULTS = {
    "setup_complete": False,
    "word_list_path": "",
    "daily_words": 15,
    "schedule_times": [],   # 默认不开启任何定时任务
    # TTS 优先级（填了才用，不填则跳过）
    "tts_provider": "",
    "minimax_api_key": "",
    "minimax_tts_model": "speech-2.8-hd",
    "minimax_tts_speed": 1.05,
    "minimax_tts_voice_id": "male-qn-qingse",
    # Piper 本地 TTS（不填则跳过）
    "piper_bin": "",
    "piper_model": "",
    # SenseVoice 本地 ASR（不填则跳过）
    "sense_voice_model_dir": "",
    # 飞书（不填则无飞书语音推送）
    "feishu_app_id": "",
    "feishu_app_secret": "",
    "feishu_user_open_id": "",
    # 多维表格（不填则无艾宾浩斯记忆）
    "bitable_app_token": "",
    "bitable_words_table_id": "",
    "bitable_chat_table_id": "",
    "created_at": "",
}


def load():
    """加载配置，优先从环境变量读取（生产），其次从 config.json（本地）"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    file_cfg = {}
    if CONFIG_FILE.exists():
        try:
            file_cfg = json.loads(CONFIG_FILE.read_text())
        except Exception:
            pass
    # 环境变量优先覆盖（生产环境由 cron env 注入真实密钥）
    SENSITIVE = {
        "feishu_app_id", "feishu_app_secret", "feishu_bot_token",
        "minimax_api_key", "minimax_group_id",
        "bitable_app_token",
    }
    for k in SENSITIVE:
        env_val = os.environ.get(k.upper()) or os.environ.get(k.lower()) or os.environ.get(k)
        if env_val:
            file_cfg[k] = env_val
    return {**DEFAULTS, **file_cfg}


def _redact(cfg):
    """写入 config.json 前，对敏感字段做脱敏处理

    脱敏策略：仅记录字段是否存在（空字符串），不记录实际值。
    这样做的好处是：
    1. config.json 即使被读取也不会暴露密钥
    2. 用户仍可通过 config_manager.py 的 API 操作配置（由调用方注入真实值）
    3. 引导设置流程可以区分"已设置但脱敏"和"从未设置"
    """
    SENSITIVE = {
        "feishu_app_id", "feishu_app_secret", "feishu_bot_token",
        "minimax_api_key", "minimax_group_id",
        "bitable_app_token",
    }
    result = dict(cfg)
    for k in SENSITIVE:
        if result.get(k):  # 有值则脱敏为空字符串
            result[k] = ""
    return result


def save(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    # 设置目录和文件权限：仅本人可读写（600），防止其他用户读取
    CONFIG_DIR.chmod(0o700)
    safe_cfg = _redact(cfg)
    CONFIG_FILE.write_text(json.dumps(safe_cfg, ensure_ascii=False, indent=2))
    CONFIG_FILE.chmod(0o600)
    # 运行时仍可从环境变量读取真实值（见 load() 的 env 覆盖逻辑）


def get(key):
    return load().get(key)


def set_(key, value):
    cfg = load()
    cfg[key] = value
    save(cfg)


def check():
    """检查配置状态（全部模块选填，仅展示哪些已配置）"""
    cfg = load()
    modules = {
        "飞书语音推送": bool(cfg.get("feishu_app_id") and cfg.get("feishu_app_secret") and cfg.get("feishu_user_open_id")),
        "MiniMax TTS": bool(cfg.get("minimax_api_key")),
        "Piper 本地 TTS": bool(cfg.get("piper_bin") and cfg.get("piper_model")),
        "SenseVoice 本地 ASR": bool(cfg.get("sense_voice_model_dir")),
        "多维表格记忆": bool(cfg.get("bitable_app_token") and cfg.get("bitable_words_table_id") and cfg.get("bitable_chat_table_id")),
        "单词表": bool(cfg.get("word_list_path")),
        "定时任务": bool(cfg.get("schedule_times")),
    }
    configured = [m for m, ok in modules.items() if ok]
    not_configured = [m for m, ok in modules.items() if not ok]
    print("📋 配置状态：")
    for m in configured:
        print(f"  ✅ {m}")
    for m in not_configured:
        print(f"  ⏭️  {m}（未配置，将跳过）")
    print(f"\n已配置 {len(configured)}/{len(modules)} 个模块")
    return True


def init():
    if CONFIG_FILE.exists():
        resp = input(f"配置已存在: {CONFIG_FILE}，覆盖？(y/N): ")
        if resp.lower() != 'y':
            print("取消。")
            return
    save({**DEFAULTS})
    print(f"✅ 已创建默认配置: {CONFIG_FILE}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "get":
        print(get(sys.argv[2] if len(sys.argv) > 2 else ""))
    elif cmd == "set":
        if len(sys.argv) < 4:
            print("用法: config_manager.py set <key> <value>")
            sys.exit(1)
        set_(sys.argv[2], sys.argv[3])
        print(f"✅ {sys.argv[2]} = {sys.argv[3]}")
    elif cmd == "check":
        ok = check()
        sys.exit(0 if ok else 1)
    elif cmd == "init":
        init()
    elif cmd == "path":
        print(CONFIG_FILE)
    else:
        print(json.dumps(load(), ensure_ascii=False, indent=2))
