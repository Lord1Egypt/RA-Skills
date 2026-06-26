#!/usr/bin/env python3
"""Interactive setup wizard and config manager for WHOOP Connect."""

import json
import os
import sys

CONFIG_DIR = os.path.expanduser("~/.whoop")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "language": "en",
    "push_recovery": True,
    "push_sleep": True,
    "push_workout": True,
    "detail_level": "compact",
    "trend_comparison": True,
    "training_advice": True,
    "units": "metric",
    "webhook_enabled": False,
    "webhook_port": 9876,
    "sync_interval": 5,
    "sync_interval_webhook": 20,
    "daily_api_limit": 10000,
}

LABELS = {
    "en": {
        "welcome": "WHOOP Connect Setup",
        "language": "Language",
        "push_recovery": "Push Recovery notifications",
        "push_sleep": "Push Sleep notifications",
        "push_workout": "Push Workout notifications",
        "detail_level": "Notification detail level",
        "trend_comparison": "Include 7-day trend comparison in push messages",
        "training_advice": "Auto-suggest training intensity based on Recovery",
        "units": "Units",
        "webhook_enabled": "Webhook enabled (requires public HTTPS endpoint)",
        "webhook_port": "Webhook server port",
        "sync_interval": "Sync interval (minutes, used when webhook is off)",
        "sync_interval_webhook": "Sync interval when webhook is on (minutes, fallback)",
        "daily_api_limit": "Daily API call limit",
        "saved": "Configuration saved to",
        "current": "Current configuration:",
        "choose": "Choose",
        "yes_no": "(y/n)",
        "enter_port": "Enter port number",
        "default": "default",
    },
    "zh": {
        "welcome": "WHOOP Connect 设置",
        "language": "语言",
        "push_recovery": "推送 Recovery 通知",
        "push_sleep": "推送睡眠通知",
        "push_workout": "推送运动通知",
        "detail_level": "通知详细程度",
        "trend_comparison": "推送消息中包含 7 天趋势对比",
        "training_advice": "根据 Recovery 自动建议训练强度",
        "units": "单位制",
        "webhook_enabled": "启用 Webhook（需要公网 HTTPS 端点）",
        "webhook_port": "Webhook 服务端口",
        "sync_interval": "同步间隔（分钟，Webhook 未启用时使用）",
        "sync_interval_webhook": "Webhook 启用时的同步间隔（分钟，兜底）",
        "daily_api_limit": "每日 API 调用上限",
        "saved": "配置已保存到",
        "current": "当前配置：",
        "choose": "选择",
        "yes_no": "(y/n)",
        "enter_port": "输入端口号",
        "default": "默认",
    },
}


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            stored = json.load(f)
        config = {**DEFAULT_CONFIG, **stored}
        return config
    return dict(DEFAULT_CONFIG)


def save_config(config):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    os.chmod(CONFIG_PATH, 0o600)


def get_label(lang, key):
    return LABELS.get(lang, LABELS["en"]).get(key, LABELS["en"].get(key, key))


def ask_choice(prompt, options, default=None):
    """Ask user to pick from numbered options."""
    print(f"\n{prompt}")
    for i, (value, label) in enumerate(options, 1):
        marker = " *" if value == default else ""
        print(f"  {i}. {label}{marker}")
    while True:
        raw = input(f"  [{1 if default is None else next(i for i,(v,_) in enumerate(options,1) if v==default)}]: ").strip()
        if not raw and default is not None:
            return default
        try:
            idx = int(raw)
            if 1 <= idx <= len(options):
                return options[idx - 1][0]
        except ValueError:
            pass
        print(f"  Please enter 1-{len(options)}")


def ask_bool(prompt, default=True):
    """Ask a yes/no question."""
    hint = "Y/n" if default else "y/N"
    raw = input(f"\n{prompt} [{hint}]: ").strip().lower()
    if not raw:
        return default
    return raw in ("y", "yes")


def ask_int(prompt, default):
    """Ask for an integer."""
    raw = input(f"\n{prompt} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        print(f"  Invalid number, using default: {default}")
        return default


def run_wizard():
    config = load_config()

    print("=" * 40)
    print("  WHOOP Connect Setup")
    print("=" * 40)

    # Language first (always in English since it's the initial choice)
    config["language"] = ask_choice(
        "Language / 语言:",
        [("en", "English"), ("zh", "中文")],
        default=config["language"],
    )

    lang = config["language"]
    L = lambda key: get_label(lang, key)

    # Push notifications
    config["push_recovery"] = ask_bool(
        L("push_recovery") + "?", default=config["push_recovery"]
    )
    config["push_sleep"] = ask_bool(
        L("push_sleep") + "?", default=config["push_sleep"]
    )
    config["push_workout"] = ask_bool(
        L("push_workout") + "?", default=config["push_workout"]
    )

    # Detail level
    config["detail_level"] = ask_choice(
        L("detail_level") + ":",
        [
            ("compact", "Compact — key numbers only" if lang == "en" else "精简 — 只显示关键数字"),
            ("detailed", "Detailed — full analysis" if lang == "en" else "详细 — 完整分析"),
        ],
        default=config["detail_level"],
    )

    # Trend comparison
    config["trend_comparison"] = ask_bool(
        L("trend_comparison") + "?", default=config["trend_comparison"]
    )

    # Training advice
    config["training_advice"] = ask_bool(
        L("training_advice") + "?", default=config["training_advice"]
    )

    # Units
    config["units"] = ask_choice(
        L("units") + ":",
        [
            ("metric", "Metric (kg, m, °C)" if lang == "en" else "公制 (kg, m, °C)"),
            ("imperial", "Imperial (lbs, ft, °F)" if lang == "en" else "英制 (lbs, ft, °F)"),
        ],
        default=config["units"],
    )

    # Webhook
    config["webhook_enabled"] = ask_bool(
        L("webhook_enabled") + "?", default=config["webhook_enabled"]
    )

    if config["webhook_enabled"]:
        config["webhook_port"] = ask_int(
            (L("enter_port") if lang == "zh" else "Webhook server port") + f" ({L('default')}: {DEFAULT_CONFIG['webhook_port']})",
            default=config["webhook_port"],
        )

    # Sync interval
    config["sync_interval"] = ask_int(
        L("sync_interval") + f" ({L('default')}: {DEFAULT_CONFIG['sync_interval']})",
        default=config["sync_interval"],
    )

    if config["webhook_enabled"]:
        config["sync_interval_webhook"] = ask_int(
            L("sync_interval_webhook") + f" ({L('default')}: {DEFAULT_CONFIG['sync_interval_webhook']})",
            default=config["sync_interval_webhook"],
        )

    # Daily API limit
    config["daily_api_limit"] = ask_int(
        L("daily_api_limit") + f" ({L('default')}: {DEFAULT_CONFIG['daily_api_limit']})",
        default=config["daily_api_limit"],
    )

    save_config(config)
    print(f"\n✓ {L('saved')} {CONFIG_PATH}")
    show_config(config)


def show_config(config=None):
    if config is None:
        config = load_config()
    lang = config.get("language", "en")
    L = lambda key: get_label(lang, key)
    print(f"\n{L('current')}")
    for key, value in config.items():
        label = L(key) if key in LABELS["en"] else key
        print(f"  {label}: {value}")


def set_value(pair):
    """Set a single config value from key=value string."""
    if "=" not in pair:
        print(f"Error: expected key=value, got: {pair}")
        sys.exit(1)
    key, value = pair.split("=", 1)
    key = key.strip()
    config = load_config()
    if key not in DEFAULT_CONFIG:
        print(f"Error: unknown config key: {key}")
        print(f"Valid keys: {', '.join(DEFAULT_CONFIG.keys())}")
        sys.exit(1)
    expected_type = type(DEFAULT_CONFIG[key])
    if expected_type == bool:
        value = value.lower() in ("true", "1", "yes", "on")
    elif expected_type == int:
        value = int(value)
    config[key] = value
    save_config(config)
    print(f"✓ {key} = {value}")


def init_config():
    """Create config with defaults if it doesn't exist. Idempotent."""
    if os.path.exists(CONFIG_PATH):
        print(f"Config already exists: {CONFIG_PATH}")
        show_config()
        return
    config = dict(DEFAULT_CONFIG)
    save_config(config)
    print(f"✓ Created default config at {CONFIG_PATH}")
    show_config(config)


def main():
    if len(sys.argv) < 2:
        run_wizard()
    elif sys.argv[1] == "--init":
        init_config()
    elif sys.argv[1] == "--show":
        show_config()
    elif sys.argv[1] == "--set" and len(sys.argv) >= 3:
        set_value(sys.argv[2])
    elif sys.argv[1] == "--json":
        config = load_config()
        print(json.dumps(config, indent=2, ensure_ascii=False))
    else:
        print("Usage:")
        print("  setup.py           Run interactive setup wizard")
        print("  setup.py --init    Create default config (non-interactive)")
        print("  setup.py --show    Show current configuration")
        print("  setup.py --set k=v Set a single config value")
        print("  setup.py --json    Output config as JSON")


if __name__ == "__main__":
    main()
