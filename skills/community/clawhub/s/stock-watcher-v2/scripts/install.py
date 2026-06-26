#!/usr/bin/env python3
"""
stock-push 一键安装脚本
用法: python3 install_stock_push.py

目标：全新设备上运行，自动完成 skill 安装 + cron/logrotate 配置
"""
import urllib.request, json, os, sys, stat

SKILL_URL = "https://github.com/your-repo/stock-push/raw/main/stock-push.skill"
SKILL_DIR = "/root/.openclaw/workspace/skills/stock-push"
CRON_CONF = "/etc/cron.d/stock-monitor"
LOGROTATE_CONF = "/etc/logrotate.d/stock-monitor"

def run(cmd):
    r = os.system(cmd)
    if r != 0:
        print(f"❌ 命令失败: {cmd}")
        sys.exit(r)
    print(f"  ✅ {cmd[:60]}...")

def main():
    print("📦 开始安装 A股股票定时推送...")

    # 1. 创建目录
    run(f"mkdir -p {os.path.dirname(SKILL_DIR)}")

    # 2. 下载/复制 skill 文件
    skill_file = "/tmp/stock-push.skill"
    if os.path.exists("/root/.openclaw/workspace/stock-push.skill"):
        print("  📂 发现本地 skill 文件，跳过下载")
        run(f"cp /root/.openclaw/workspace/stock-push.skill {skill_file}")
    else:
        print(f"  ⬇️  下载 skill 文件...")
        try:
            req = urllib.request.Request(SKILL_URL, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                with open(skill_file, "wb") as f:
                    f.write(r.read())
        except Exception as e:
            print(f"  ⚠️  下载失败: {e}")
            print("  请手动上传 /root/.openclaw/workspace/stock-push.skill 到目标设备")
            sys.exit(1)

    # 3. 解压 skill
    run(f"cd /tmp && unzip -o stock-push.skill -d stock-push-extract")
    run(f"cp -r /tmp/stock-push-extract/stock-push /root/.openclaw/workspace/skills/")

    # 4. 写 cron
    cron_content = """SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# 股票推送 cron（系统级，不依赖 Gateway）
# 盘前推荐：9:20（周一~五）
20 9 * * 1-5 root python3 /root/.openclaw/workspace/skills/stock-push/scripts/stock_pre.py >> /tmp/stock_pre.log 2>&1

# 收盘复盘：15:05（周一~五）
5 15 * * 1-5 root python3 /root/.openclaw/workspace/skills/stock-push/scripts/stock_after.py >> /tmp/stock_after.log 2>&1

# 次日关注：20:00（周一~四）
0 20 * * 1-4 root python3 /root/.openclaw/workspace/skills/stock-push/scripts/stock_next.py >> /tmp/stock_next.log 2>&1
"""
    with open(CRON_CONF, "w") as f:
        f.write(cron_content)
    os.chmod(CRON_CONF, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    print(f"  ✅ cron 配置写入 {CRON_CONF}")

    # 5. 写 logrotate
    logrotate_content = """# 股票推送日志轮转
/tmp/stock_pre.log /tmp/stock_after.log /tmp/stock_next.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    missingok
    create 0644 root root
}
"""
    with open(LOGROTATE_CONF, "w") as f:
        f.write(logrotate_content)
    print(f"  ✅ logrotate 配置写入 {LOGROTATE_CONF}")

    # 6. 验证脚本语法
    for script in ["stock_pre.py", "stock_after.py", "stock_next.py"]:
        path = f"/root/.openclaw/workspace/skills/stock-push/scripts/{script}"
        r = os.system(f"python3 -m py_compile {path}")
        if r != 0:
            print(f"  ❌ {script} 语法检查失败")
        else:
            print(f"  ✅ {script} 语法 OK")

    print()
    print("=" * 50)
    print("安装完成！")
    print()
    print("⚠️  安装后需修改脚本中的配置：")
    print("  1. 打开 /root/.openclaw/workspace/skills/stock-push/scripts/")
    print("  2. 修改 USER_ID 为你的微信 ID")
    print("  3. 修改 HOLDINGS/WATCH_LIST 为你的持仓")
    print()
    print("测试发送：")
    print('  openclaw message send --channel openclaw-weixin --target <USER_ID> --message "测试"')
    print()
    print("查看 cron 状态：")
    print("  systemctl status cron")
    print("  systemctl restart cron")
    print()
    print("查看日志：")
    print("  tail -f /tmp/stock_pre.log")
    print("=" * 50)

if __name__ == "__main__":
    main()
