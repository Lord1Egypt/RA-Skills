#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票监控定时任务健康检查脚本
由 OpenClaw heartbeat 或定时调用
自动检查 + 自动修复常见问题
"""

import os
import sys
import json
import subprocess
from datetime import datetime

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SKILL_DIR, 'config.local.yaml')
LAUNCHD_LABEL = 'com.openclaw.stock-monitor'

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def check_launchd():
    """检查 LaunchAgent 运行状态"""
    try:
        result = subprocess.run(
            ['launchctl', 'list', LAUNCHD_LABEL],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and '\t0\t' not in result.stdout:
            # 状态不是 - ，说明在运行
            log(f"✅ LaunchAgent 运行正常: {LAUNCHD_LABEL}")
            return True
        else:
            log(f"⚠️ LaunchAgent 未运行，尝试启动...")
            return start_launchd()
    except Exception as e:
        log(f"⚠️ 检查 LaunchAgent 失败: {e}")
        return False

def start_launchd():
    """尝试启动 LaunchAgent"""
    plist = os.path.expanduser('~/Library/LaunchAgents/com.openclaw.stock-monitor.plist')
    if not os.path.exists(plist):
        log(f"⚠️ LaunchAgent plist 不存在: {plist}")
        return False
    
    try:
        # 加载服务
        result = subprocess.run(
            ['launchctl', 'bootstrap', 'gui/$UID', plist],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            log(f"✅ LaunchAgent 启动成功")
            return True
        else:
            log(f"⚠️ LaunchAgent 启动失败: {result.stderr[:200]}")
            return False
    except Exception as e:
        log(f"⚠️ 启动 LaunchAgent 异常: {e}")
        return False

def check_config():
    """检查配置文件"""
    # config.local.yaml 是个人配置，不存在时检查 config.yaml 是否存在
    local_exists = os.path.exists(CONFIG_FILE)
    default_path = os.path.join(SKILL_DIR, 'config.yaml')
    default_exists = os.path.exists(default_path)

    if not local_exists and not default_exists:
        log(f"❌ 配置文件不存在！请先创建 config.yaml 或 config.local.yaml")
        log(f"   参考 SKILL.md 填写您的股票和飞书凭证")
        return False

    # 优先读 local，备读取 default
    config_path = CONFIG_FILE if local_exists else default_path

    # 检查关键字段
    try:
        import yaml
        with open(config_path) as f:
            config = yaml.safe_load(f)

        stocks = config.get('stocks', [])
        feishu = config.get('push', {}).get('feishu', {})

        if not stocks:
            log(f"⚠️ 股票池为空，请编辑 {config_path} 添加股票")
            return False

        # 检查凭证是否为明显的占位符值
        placeholder_ids = {'YOUR_FEISHU_APP_ID', 'YOUR_APP_ID', 'cli_xxxxxxxx'}
        if feishu.get('app_id', '') in placeholder_ids:
            log(f"⚠️ 飞书凭证未填写，请编辑 {config_path} 填入真实凭证")
            return False

        if not feishu.get('app_id') or not feishu.get('chat_id'):
            log(f"⚠️ 飞书凭证不完整，请检查 {config_path}")
            return False

        log(f"✅ 配置文件正常 ({len(stocks)} 只股票)")
        return True
    except Exception as e:
        log(f"⚠️ 配置文件读取失败: {e}")
        return False

def rebuild_config():
    """
    生成最小配置模板（不含任何私密数据/凭证）
    仅用于引导首次安装，用户需自行填入真实的股票代码和飞书凭证
    """
    template = """# 股票监控配置模板 - 请根据实际情况修改
stocks: []

push:
  channel: "feishu"
  feishu:
    app_id: "YOUR_FEISHU_APP_ID"
    app_secret: "YOUR_FEISHU_APP_SECRET"
    chat_id: "YOUR_CHAT_ID"
  times:
    - "09:15"
    - "10:00"
    - "13:00"
    - "14:50"

advanced:
  history_days: 60
"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            f.write(template)
        log(f"✅ 配置模板已生成到 config.local.yaml")
        log(f"⚠️ 请编辑配置文件填入您的股票和飞书凭证")
        return True
    except Exception as e:
        log(f"⚠️ 配置模板生成失败: {e}")
        return False

def check_network():
    """检查股票数据接口"""
    try:
        import requests
        resp = requests.get(
            'https://qt.gtimg.cn/q=sh000001',
            timeout=10
        )
        if resp.status_code == 200 and '000001' in resp.text:
            log(f"✅ 网络接口正常")
            return True
        log(f"⚠️ 网络接口异常")
        return False
    except Exception as e:
        log(f"⚠️ 网络检查失败: {e}")
        return False

def test_push():
    """测试飞书推送（发一条简短测试）"""
    try:
        import requests
        import json as json_lib
        
        with open(CONFIG_FILE) as f:
            import yaml
            config = yaml.safe_load(f)
        
        feishu = config.get('push', {}).get('feishu', {})
        app_id = feishu.get('app_id')
        app_secret = feishu.get('app_secret')
        chat_id = feishu.get('chat_id')
        
        # 获取 token
        resp = requests.post(
            'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
            json={'app_id': app_id, 'app_secret': app_secret},
            timeout=10
        )
        token = resp.json().get('tenant_access_token')
        if not token:
            log(f"⚠️ 飞书 token 获取失败")
            return False
        
        # 发送测试
        msg = f"✅ 股票监控定时任务健康检查\n时间: {datetime.now().strftime('%H:%M:%S')}\n状态: 一切正常"
        resp = requests.post(
            'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'receive_id': chat_id,
                'msg_type': 'text',
                'content': json_lib.dumps({'text': msg})
            },
            timeout=10
        )
        
        if resp.status_code == 200 and resp.json().get('code') == 0:
            log(f"✅ 飞书推送测试成功")
            return True
        log(f"⚠️ 飞书推送失败: {resp.text[:100]}")
        return False
    except Exception as e:
        log(f"⚠️ 飞书推送测试异常: {e}")
        return False

def main():
    log(f"=== 股票监控健康检查 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    results = {}
    
    # 1. 检查配置文件
    results['config'] = check_config()
    
    # 2. 检查 LaunchAgent
    results['launchd'] = check_launchd()
    
    # 3. 检查网络
    results['network'] = check_network()
    
    # 4. 测试推送（仅在交易日 09:00-15:00 执行）
    hour = datetime.now().hour
    if 9 <= hour <= 15:
        results['push'] = test_push()
    else:
        log(f"⏭️ 非交易时段，跳过推送测试")
        results['push'] = True
    
    # 总结
    log(f"=== 检查完成 ===")
    all_ok = all(results.values())
    if all_ok:
        log(f"✅ 所有检查通过")
        return 0
    else:
        failed = [k for k, v in results.items() if not v]
        log(f"⚠️ 以下项目异常: {', '.join(failed)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
