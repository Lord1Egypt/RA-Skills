import os, sys, json, io, stat, shutil, time

# Force UTF-8 for console output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def stiffen():
    print("👹 OniBoniBot Stiffener: Always Backup First...")
    
    # 0. Backup Policy (Sienna Protocol)
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    backup_dir = os.path.expanduser("~/.openclaw/backups")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"openclaw.json.{timestamp}.bak")
    
    if os.path.exists(config_path):
        shutil.copy2(config_path, backup_path)
        print(f"✅ Created Backup: {backup_path}")
    else:
        print("❌ Error: No openclaw.json to stiffen.")
        return

    # 1. Stiffen Logic
    print("👹 Hardening the Vault...")
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Action: Tighten Proxy (Fix Audit WARN)
        if 'gateway' not in config: config['gateway'] = {}
        config['gateway']['trustedProxies'] = ["127.0.0.1"]
        print("🔒 Network Fix: Locked trustedProxies to localhost.")
            
        # Action: Hardened Tool Policy (Clear INFO)
        if 'tools' not in config: config['tools'] = {}
        config['tools']['elevated'] = { "enabled": False }
        # Add high-risk tools to deny list
        if 'deny' not in config['tools']: config['tools']['deny'] = []
        for t in ["sessions_spawn", "sessions_send"]:
            if t not in config['tools']['deny']:
                config['tools']['deny'].append(t)
        print("🔒 Tool Fix: Set elevated tools to 'enabled: false' and added to deny list.")

        # Action: Fix Ineffective Deny Commands (Fix Audit WARN)
        if 'nodes' not in config['gateway']: config['gateway']['nodes'] = {}
        # Only use VALID command names
        config['gateway']['nodes']['denyCommands'] = [
            "canvas.eval", "canvas.present"
        ]
        print("🔒 Device Fix: Applied strict DenyCommands for valid node commands.")

        # Save it
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print("✅ Config Stiffened.")

    except Exception as e:
        print(f"❌ Error during stiffen: {e}")
        return

    # 2. Lock File
    with open(".stiffened", "w") as f:
        f.write(f"Stiffened by OniBoniBot on {timestamp}\n")

    print(f"👹 Done. UNDO: copy {backup_path} {config_path}")

def restore():
    print("👹 OniBoniBot: Reversing the Hex-Stiff...")
    backup_dir = os.path.expanduser("~/.openclaw/backups")
    if not os.path.exists(backup_dir):
        print("❌ No backups found.")
        return
    
    backups = sorted([f for f in os.listdir(backup_dir) if f.startswith("openclaw.json")], reverse=True)
    if not backups:
        print("❌ No openclaw.json backups found.")
        return
        
    latest_backup = os.path.join(backup_dir, backups[0])
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    
    shutil.copy2(latest_backup, config_path)
    print(f"✅ Restored latest backup from {latest_backup}.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "apply":
            stiffen()
        elif sys.argv[1] == "restore":
            restore()
    else:
        print("Usage: python stiffen.py [apply|restore]")
