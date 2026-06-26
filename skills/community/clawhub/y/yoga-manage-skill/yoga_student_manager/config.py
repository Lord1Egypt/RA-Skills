import json
import os
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"

DEFAULT_URGENT = 3
DEFAULT_WARN = 5

def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def get_email_config():
    config = load_config()
    return config.get('email', {})

def set_email_config(smtp_server, smtp_port, email, password, use_ssl=True):
    config = load_config()
    config['email'] = {
        'smtp_server': smtp_server,
        'smtp_port': smtp_port,
        'email': email,
        'password': password,
        'use_ssl': use_ssl
    }
    save_config(config)

def is_configured():
    email = get_email_config()
    return bool(email.get('email') and email.get('password') and email.get('smtp_server'))

def get_alert_thresholds():
    config = load_config()
    alerts = config.get('alerts', {})
    return {
        'urgent': alerts.get('urgent', DEFAULT_URGENT),
        'warn': alerts.get('warn', DEFAULT_WARN)
    }

def set_alert_thresholds(urgent, warn):
    config = load_config()
    config['alerts'] = {
        'urgent': int(urgent),
        'warn': int(warn)
    }
    save_config(config)

def prompt_email_config():
    print("=" * 50)
    print("瑜伽学员管理系统 - 邮箱配置")
    print("=" * 50)
    print("\n请配置您的邮箱信息，用于发送课时扣除记录：")
    print("(支持 Gmail、QQ邮箱、163邮箱、Outlook等)\n")

    print("常用邮箱SMTP设置：")
    print("  Gmail:    smtp.gmail.com:587")
    print("  QQ邮箱:   smtp.qq.com:587")
    print("  163邮箱:  smtp.163.com:25")
    print("  Outlook:  smtp.office365.com:587")
    print("")

    smtp = input("SMTP服务器: ").strip()
    port = input("SMTP端口 (默认587): ").strip() or "587"
    email = input("邮箱账号: ").strip()
    password = input("邮箱密码/授权码: ").strip()
    ssl = input("使用SSL/TLS? (y/n, 默认y): ").strip().lower() != 'n'

    set_email_config(smtp, int(port), email, password, ssl)
    print("\n邮箱配置已保存！")

def prompt_alert_config():
    thresholds = get_alert_thresholds()
    print("=" * 50)
    print("瑜伽学员管理系统 - 提醒阈值配置")
    print("=" * 50)
    print(f"\n当前设置：")
    print(f"  紧急提醒（红色）: 剩余 ≤ {thresholds['urgent']} 次")
    print(f"  普通提醒（黄色）: 剩余 ≤ {thresholds['warn']} 次")
    print("\n请设置新的提醒阈值：\n")

    urgent_input = input(f"紧急提醒阈值 (默认 {DEFAULT_URGENT}): ").strip()
    warn_input = input(f"普通提醒阈值 (默认 {DEFAULT_WARN}): ").strip()

    urgent = int(urgent_input) if urgent_input.isdigit() else thresholds['urgent']
    warn = int(warn_input) if warn_input.isdigit() else thresholds['warn']

    if warn <= urgent:
        print("\n注意：普通提醒阈值应大于紧急提醒阈值，已自动调整。")
        warn = max(warn, urgent + 2)

    set_alert_thresholds(urgent, warn)
    print(f"\n提醒阈值已保存！")
    print(f"  紧急提醒: 剩余 ≤ {urgent} 次")
    print(f"  普通提醒: 剩余 ≤ {warn} 次")
