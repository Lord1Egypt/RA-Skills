#!/usr/bin/env python3
"""
统一云同步脚本 v2.1
首次使用自动引导 - 无需用户主动说任何话

核心逻辑：
1. 运行即自动检测
2. 未配置 → 首次即引导
3. 已配置 → 直接同步
"""

import argparse
import sys
import json
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(__file__).rsplit("/", 1)[0])

from cloud_adapter import AdapterFactory


# ============================================================================
# 常量
# ============================================================================

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
EXPORT_DIR = MEMORY_DIR / "exports"
STATE_FILE = MEMORY_DIR / ".cloud_sync_state.json"


# ============================================================================
# 首次引导界面
# ============================================================================

def print_first_time_guide():
    """打印首次使用引导界面"""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     ☁️  云备份服务 - 首次配置向导                          ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║   🔍 检测到您还没有配置任何云备份服务                     ║
║                                                          ║
║   📋 选择您想使用的云服务（输入编号 1-5）：              ║
║                                                          ║
║   [1] 🥜 坚果云                                          ║
║        国内可用，稳定可靠，免费额度够用                   ║
║        → 推荐：大多数国内用户                             ║
║                                                          ║
║   [2] ☁️ 阿里云 OSS                                      ║
║        企业级存储，低成本，国内高速                       ║
║        → 推荐：有技术背景的用户                           ║
║                                                          ║
║   [3] 🖥️ Samba/NAS                                      ║
║        局域网高速传输，适合 NAS 用户                     ║
║        → 推荐：有 NAS 的用户                             ║
║                                                          ║
║   [4] 📡 SFTP                                           ║
║        SSH 加固，安全可靠                                ║
║        → 推荐：有自己服务器的用户                         ║
║                                                          ║
║   [5] 📚 IMA 知识库                                      ║
║        腾讯生态，与记忆系统无缝集成                       ║
║        → 推荐：已使用 IMA 的用户                         ║
║                                                          ║
║   ───────────────────────────────────────────────────    ║
║   输入编号（如 1）查看详细配置步骤                        ║
║   输入 "skip" 退出，稍后再说                             ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")


# ============================================================================
# 安装向导
# ============================================================================

SERVICES_GUIDE = {
    "1": {
        "name": "坚果云",
        "provider": "webdav",
        "steps": [
            "访问 https://www.jianguoyun.com/ 注册账号",
            "登录后进入「账户信息」→「安全设置」",
            "点击「第三方应用管理」",
            "创建应用密码（注意：是应用密码，不是登录密码）",
            "复制你注册的邮箱和应用密码",
        ],
        "config_template": """
# 复制以下配置到 ~/.openclaw/credentials/secrets.env：

WEBDAV_URL=https://dav.jianguoyun.com/dav/
WEBDAV_USERNAME=你的坚果云邮箱
WEBDAV_PASSWORD=你的应用密码
""",
    },
    "2": {
        "name": "阿里云 OSS",
        "provider": "s3",
        "steps": [
            "访问 https://www.aliyun.com/product/oss 开通服务",
            "进入控制台 → 右上角头像 → AccessKey 管理",
            "创建 AccessKey（推荐使用子用户 AccessKey）",
            "记住 AccessKey ID 和 AccessKey Secret",
            "进入 OSS 控制台 → 创建 Bucket（存储桶）",
            "记住 Bucket 名称和地域（如 oss-cn-hangzhou）",
        ],
        "config_template": """
# 复制以下配置到 ~/.openclaw/credentials/secrets.env：

S3_ENDPOINT=https://oss-cn-hangzhou.aliyuncs.com
S3_ACCESS_KEY=你的 AccessKey ID
S3_SECRET_KEY=你的 AccessKey Secret
S3_BUCKET=你的 bucket 名称
""",
    },
    "3": {
        "name": "Samba/NAS",
        "provider": "samba",
        "steps": [
            "确保你的 NAS 已开启 SMB/Samba 服务",
            "在 NAS 上创建一个共享文件夹（如 memory）",
            "确保电脑能通过局域网访问 NAS",
            "记住 NAS 的 IP 地址（如 192.168.1.100）",
            "记住登录 NAS 的用户名和密码",
        ],
        "config_template": """
# 复制以下配置到 ~/.openclaw/credentials/secrets.env：

SAMBA_HOST=192.168.1.100
SAMBA_USER=你的 NAS 用户名
SAMBA_PASSWORD=你的 NAS 密码
SAMBA_SHARE=/memory
""",
    },
    "4": {
        "name": "SFTP",
        "provider": "sftp",
        "steps": [
            "确保你的服务器已开启 SSH 服务",
            "记住服务器的 IP 地址或域名",
            "记住 SSH 端口（默认 22）",
            "记住登录用户名和密码（或 SSH 密钥）",
        ],
        "config_template": """
# 复制以下配置到 ~/.openclaw/credentials/secrets.env：

SFTP_HOST=你的服务器地址
SFTP_PORT=22
SFTP_USERNAME=你的用户名
SFTP_PASSWORD=你的密码
""",
    },
    "5": {
        "name": "IMA 知识库",
        "provider": "ima",
        "steps": [
            "访问 https://ima.qq.com/ 注册",
            "创建知识库",
            "在设置中找到 API 凭证",
        ],
        "config_template": """
# 复制以下配置到 ~/.openclaw/credentials/secrets.env：

IMA_OPENAPI_CLIENTID=你的 Client ID
IMA_OPENAPI_APIKEY=你的 API Key
""",
    },
}


def print_install_guide(service_id: str):
    """打印指定服务的安装指南"""
    service = SERVICES_GUIDE.get(service_id)
    if not service:
        print(f"❌ 无效选择：{service_id}")
        print("\n请输入 1-5 之间的编号")
        return
    
    print(f"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     📦 {service['name']} 配置指南                          ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║   📝 配置步骤：                                          ║
""")
    
    for i, step in enumerate(service['steps'], 1):
        print(f"║   {i}. {step:<54} ║")
    
    print("""║                                                          ║
║   ───────────────────────────────────────────────────    ║
║                                                          ║
║   📋 配置模板：                                          ║""")
    
    print(f"║{service['config_template']}║")
    
    print("""║                                                          ║
║   ✅ 配置完成后，重新运行本脚本即可自动使用               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")


# ============================================================================
# 状态管理
# ============================================================================

def load_state() -> dict:
    """加载同步状态"""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_sync": None, "versions": {}, "adapters": {}}


def save_state(state: dict):
    """保存同步状态"""
    state["last_sync"] = datetime.now().isoformat()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


# ============================================================================
# 来源标记
# ============================================================================

def add_source_marker(data: dict, adapter_name: str) -> dict:
    """添加来源标记"""
    return {
        **data,
        "_source": f"yaoyao-cloud-backup:{adapter_name}",
        "_sync_time": datetime.now().isoformat(),
        "_version": data.get("_version", 0) + 1,
    }


def should_sync(remote_data: dict) -> bool:
    """检查是否应该同步（防死循环）"""
    return "yaoyao-cloud-backup" not in remote_data.get("_source", "")


# ============================================================================
# 上传
# ============================================================================

def upload_export(adapters: dict, dry_run: bool = False) -> dict:
    """上传导出文件到所有云服务"""
    results = {}
    
    if not EXPORT_DIR.exists():
        print(f"⚠️  导出目录不存在: {EXPORT_DIR}")
        return results
    
    files = list(EXPORT_DIR.glob("*"))
    if not files:
        print("⚠️  没有需要同步的文件（请先运行 memory_exporter.py 导出）")
        return results
    
    print(f"📤 正在上传 {len(files)} 个文件到 {len(adapters)} 个云服务...\n")
    
    for name, adapter in adapters.items():
        print(f"☁️  {name} ({adapter.get_name()})...")
        
        if dry_run:
            for f in files:
                print(f"   [DRY RUN] {f.name}")
            results[name] = {"status": "dry_run", "count": len(files)}
            continue
        
        success = failed = 0
        for f in files:
            remote_path = f"/yaoyao-memory/{datetime.now().strftime('%Y%m')}/{f.name}"
            try:
                data = json.loads(f.read_text())
                data = add_source_marker(data, name)
                temp_file = f.parent / f".tmp_{f.name}"
                temp_file.write_text(json.dumps(data, indent=2, ensure_ascii=False))
                
                if adapter.upload(temp_file, remote_path):
                    success += 1
                else:
                    failed += 1
                temp_file.unlink()
            except Exception as e:
                print(f"      ❌ {f.name}: {e}")
                failed += 1
        
        icon = "✅" if failed == 0 else "⚠️" if success > 0 else "❌"
        print(f"   {icon} {success}/{len(files)} 成功")
        results[name] = {"status": "ok" if failed == 0 else "partial", "success": success, "failed": failed}
    
    return results


# ============================================================================
# 下载
# ============================================================================

def download_from_cloud(adapters: dict, dry_run: bool = False) -> dict:
    """从所有云服务下载"""
    results = {}
    
    for name, adapter in adapters.items():
        print(f"☁️  {name} ({adapter.get_name()})...")
        
        if dry_run:
            print("   [DRY RUN] 预览下载...")
            continue
        
        try:
            files = adapter.list("/yaoyao-memory/")
            if not files:
                print("   ℹ️  没有文件")
                results[name] = {"status": "empty", "count": 0}
                continue
            
            print(f"   📥 发现 {len(files)} 个文件")
            
            success = skipped = 0
            state = load_state()
            
            for f in files:
                remote_path = f["name"]
                local_name = Path(remote_path).name
                local_path = EXPORT_DIR / local_name
                
                remote_version = f.get("version", 0)
                local_version = state["versions"].get(name, {}).get(local_name, 0)
                
                if remote_version <= local_version:
                    print(f"   ⏭️  已是最新: {local_name}")
                    skipped += 1
                    continue
                
                if adapter.download(remote_path, local_path):
                    try:
                        data = json.loads(local_path.read_text())
                        if not should_sync(data):
                            print(f"   ⏭️  跳过（云端修改由本程序触发）: {local_name}")
                            local_path.unlink()
                            skipped += 1
                            continue
                    except:
                        pass
                    
                    state["versions"].setdefault(name, {})[local_name] = remote_version
                    success += 1
                    print(f"   ✅ {local_name}")
                else:
                    print(f"   ❌ {local_name}")
            
            save_state(state)
            icon = "✅" if success > 0 else "ℹ️"
            print(f"   {icon} 下载 {success}，跳过 {skipped}")
            results[name] = {"status": "ok", "downloaded": success, "skipped": skipped}
        except Exception as e:
            print(f"   ❌ 错误: {e}")
            results[name] = {"status": "error", "error": str(e)}
    
    return results


# ============================================================================
# 状态查看
# ============================================================================

def show_status(adapters: dict):
    """显示配置状态"""
    print("\n☁️  云同步配置状态")
    print("=" * 50)
    
    if not adapters:
        print("\n⚠️  未配置任何云服务\n")
        print("💡 运行本脚本将自动引导配置")
        return
    
    print(f"\n✅ 已配置 {len(adapters)} 个云服务：\n")
    state = load_state()
    
    for name, adapter in adapters.items():
        icon = "📚" if "ima" in name else "🌐" if "webdav" in name else "🪣" if "s3" in name else "🖥️"
        print(f"  {icon} {name}")
        print(f"     类型: {adapter.get_name()}")
        versions = state.get("versions", {}).get(name, {})
        if versions:
            print(f"     已同步: {len(versions)} 个文件")
        print()
    
    print(f"最后同步: {state.get('last_sync', '从未')}")


# ============================================================================
# 主函数
# ============================================================================

def main():
    # 自动检测云服务
    adapters = AdapterFactory.create_all()
    
    # 解析参数
    parser = argparse.ArgumentParser(description="云备份同步工具")
    parser.add_argument("--upload", action="store_true", help="上传到云服务")
    parser.add_argument("--download", action="store_true", help="从云服务下载")
    parser.add_argument("--status", action="store_true", help="查看配置状态")
    parser.add_argument("--guide", type=str, help="显示安装指南")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")
    args = parser.parse_args()
    
    # 显示状态
    if args.status:
        show_status(adapters)
        return
    
    # 显示安装指南
    if args.guide:
        print_install_guide(args.guide)
        return
    
    # 未配置云服务时，显示首次引导
    if not adapters:
        print_first_time_guide()
        
        # 简单交互
        choice = input("\n请输入编号（1-5）或 skip：").strip().lower()
        
        if choice == "skip":
            print("\n👋 好的，稍后再说")
            print("   随时运行本脚本可以重新配置")
            return
        
        if choice in SERVICES_GUIDE:
            print_install_guide(choice)
            return
        
        if choice:
            print(f"\n❌ 无效选择：{choice}")
        
        return
    
    # 已配置云服务，执行同步
    if args.upload:
        upload_export(adapters, dry_run=args.dry_run)
        print("\n✅ 上传完成")
        return
    
    if args.download:
        download_from_cloud(adapters, dry_run=args.dry_run)
        print("\n✅ 下载完成")
        return
    
    # 默认显示状态
    show_status(adapters)


if __name__ == "__main__":
    main()
