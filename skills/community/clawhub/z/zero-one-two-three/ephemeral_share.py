#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _encoding_compat

"""
🔥 Phase 16: Ephemeral Share (阅后即焚文件分享)
核心理念：智能体生成的文件可以安全传递给人，看完自动销毁，不留痕迹
功能：
  1. 创建焚毁包 — 加密文件 + 一次性密钥 + 过期时间
  2. 阅后即焚 — 打开后自动安全擦除（覆写随机数据后删除）
  3. 时效炸弹 — 超时未读自动销毁
  4. 读取计数 — 支持 N 次阅读后销毁
  5. 审计追踪 — 记录每次访问时间、IP、是否销毁

用法：
  创建焚毁包：python ephemeral_share.py --create <文件> [--expire 24] [--reads 1]
  打开阅读：   python ephemeral_share.py --open <焚毁包.eph> [--key <密钥>]
  查看状态：   python ephemeral_share.py --status
  清理过期：   python ephemeral_share.py --purge
"""

import os
import json
import time
import shutil
import base64
import hashlib
import secrets
import stat
import uuid
from datetime import datetime, timedelta
from pathlib import Path

try:
    from cryptography.fernet import Fernet, InvalidToken
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

SHARE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ephemeral_shares")


def _derive_key(seed):
    return base64.urlsafe_b64encode(hashlib.sha256(seed.encode()).digest())


def _secure_shred(filepath, passes=3):
    """安全擦除：覆写随机数据后删除"""
    if not os.path.exists(filepath):
        return
    try:
        size = os.path.getsize(filepath)
        for _ in range(passes):
            with open(filepath, "r+b") as f:
                f.seek(0)
                f.write(secrets.token_bytes(size))
                f.flush()
                os.fsync(f.fileno())
        os.remove(filepath)
        return True
    except Exception:
        try:
            os.remove(filepath)
        except Exception:
            pass
        return False


class EphemeralShare:

    def __init__(self, share_dir=None):
        if not HAS_CRYPTO:
            raise ImportError("需要安装 cryptography: pip install cryptography")
        self.share_dir = share_dir or SHARE_DIR
        os.makedirs(self.share_dir, exist_ok=True)

    def create(self, source_path, expire_hours=24, max_reads=1):
        if not os.path.exists(source_path):
            print(f"❌ 源文件不存在: {source_path}")
            return None

        with open(source_path, "r", encoding="utf-8") as f:
            content = f.read()

        bundle_id = uuid.uuid4().hex[:8]
        access_key = secrets.token_hex(16)
        cipher = Fernet(_derive_key(access_key))

        encrypted = cipher.encrypt(content.encode("utf-8"))
        encrypted_b64 = base64.b64encode(encrypted).decode("ascii")

        bundle = {
            "version": "1.0",
            "bundle_id": bundle_id,
            "created": datetime.now().isoformat(),
            "expires": (datetime.now() + timedelta(hours=expire_hours)).isoformat(),
            "max_reads": max_reads,
            "read_count": 0,
            "original_filename": os.path.basename(source_path),
            "original_size": len(content),
            "content_encrypted": encrypted_b64,
            "shredded": False,
            "access_log": [],
        }

        bundle_path = os.path.join(self.share_dir, f"{bundle_id}.eph")
        with open(bundle_path, "w", encoding="utf-8") as f:
            json.dump(bundle, f, ensure_ascii=False, indent=2)

        print(f"\n🔥 阅后即焚包已创建！")
        print(f"   文件: {bundle_path}")
        print(f"   密钥: {access_key}")
        print(f"   阅读次数: {max_reads} 次后销毁")
        print(f"   过期时间: {expire_hours} 小时后自动销毁")
        print(f"\n📋 分享命令:")
        print(f"   python ephemeral_share.py --open {bundle_id}.eph --key {access_key}")
        print(f"\n⚠️  密钥仅显示一次，请立即复制保存！")

        return bundle_path, access_key

    def open(self, bundle_filename, access_key=None):
        bundle_path = os.path.join(self.share_dir, bundle_filename)
        if not os.path.exists(bundle_path):
            print(f"❌ 焚毁包不存在或已被销毁: {bundle_filename}")
            return None

        with open(bundle_path, "r", encoding="utf-8") as f:
            bundle = json.load(f)

        if bundle.get("shredded"):
            print("🔥 此文件已被销毁，无法再次阅读。")
            return None

        if datetime.now() > datetime.fromisoformat(bundle["expires"]):
            print("⏰ 此文件已过期，正在自动销毁...")
            self._destroy(bundle_path, bundle, reason="expired")
            return None

        if access_key is None:
            access_key = input("🔑 请输入访问密钥: ").strip()

        cipher = Fernet(_derive_key(access_key))
        try:
            encrypted = base64.b64decode(bundle["content_encrypted"])
            content = cipher.decrypt(encrypted).decode("utf-8")
        except InvalidToken:
            print("❌ 密钥错误，访问被拒绝。")
            bundle.setdefault("access_log", []).append({
                "time": datetime.now().isoformat(),
                "result": "denied",
            })
            with open(bundle_path, "w", encoding="utf-8") as f:
                json.dump(bundle, f, ensure_ascii=False, indent=2)
            return None
        except Exception as e:
            print(f"❌ 解密失败: {e}")
            return None

        bundle["read_count"] = bundle.get("read_count", 0) + 1
        bundle.setdefault("access_log", []).append({
            "time": datetime.now().isoformat(),
            "result": "granted",
            "read_number": bundle["read_count"],
        })

        will_shred = bundle["read_count"] >= bundle.get("max_reads", 1)

        print(f"\n{'='*60}")
        print(f"📄 {bundle['original_filename']}")
        print(f"   阅读次数: {bundle['read_count']}/{bundle.get('max_reads', 1)}")
        if will_shred:
            print(f"   🔥 这是最后一次阅读，即将销毁！")
        print(f"{'='*60}\n")
        print(content)
        print(f"\n{'='*60}")

        if will_shred:
            self._destroy(bundle_path, bundle, reason="max_reads")
            print("🔥 文件已阅后即焚，安全销毁完成。")
        else:
            bundle["content_encrypted"] = base64.b64encode(
                cipher.encrypt(content.encode("utf-8"))).decode("ascii")
            with open(bundle_path, "w", encoding="utf-8") as f:
                json.dump(bundle, f, ensure_ascii=False, indent=2)
            print(f"📌 剩余 {bundle.get('max_reads', 1) - bundle['read_count']} 次阅读机会。")

        return content

    def _destroy(self, bundle_path, bundle, reason="shredded"):
        bundle["shredded"] = True
        bundle["shredded_at"] = datetime.now().isoformat()
        bundle["shred_reason"] = reason
        with open(bundle_path, "w", encoding="utf-8") as f:
            json.dump(bundle, f, ensure_ascii=False, indent=2)
        _secure_shred(bundle_path)

    def status(self):
        if not os.path.exists(self.share_dir):
            print("📭 暂无焚毁包。")
            return

        bundles = []
        for fname in os.listdir(self.share_dir):
            if not fname.endswith(".eph"):
                continue
            fpath = os.path.join(self.share_dir, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    b = json.load(f)
                bundles.append((fname, b))
            except Exception:
                pass

        if not bundles:
            print("📭 暂无焚毁包。")
            return

        print(f"\n🔥 焚毁包状态 ({len(bundles)} 个):\n")
        for fname, b in bundles:
            icon = "💀" if b.get("shredded") else ("⏰" if datetime.now() > datetime.fromisoformat(b["expires"]) else "🔥")
            reads = f"{b.get('read_count', 0)}/{b.get('max_reads', 1)}"
            status_text = "已销毁" if b.get("shredded") else "活跃"
            print(f"  {icon} {fname}")
            print(f"     文件: {b.get('original_filename', '?')}  |  阅读: {reads}  |  状态: {status_text}")
            if b.get("access_log"):
                for log in b["access_log"][-3:]:
                    print(f"     {'✅' if log['result'] == 'granted' else '❌'} {log['time']}")
            print()

    def purge_expired(self):
        count = 0
        for fname in os.listdir(self.share_dir):
            if not fname.endswith(".eph"):
                continue
            fpath = os.path.join(self.share_dir, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    b = json.load(f)
                if b.get("shredded") or datetime.now() > datetime.fromisoformat(b["expires"]):
                    _secure_shred(fpath)
                    count += 1
            except Exception:
                try:
                    os.remove(fpath)
                    count += 1
                except Exception:
                    pass
        print(f"🧹 已清理 {count} 个过期焚毁包。")


def main():
    if not HAS_CRYPTO:
        print("请先安装 cryptography: pip install cryptography")
        sys.exit(1)

    es = EphemeralShare()

    if "--create" in sys.argv:
        idx = sys.argv.index("--create")
        src = sys.argv[idx + 1]

        expire = 24
        if "--expire" in sys.argv:
            eidx = sys.argv.index("--expire")
            expire = int(sys.argv[eidx + 1])

        max_reads = 1
        if "--reads" in sys.argv:
            ridx = sys.argv.index("--reads")
            max_reads = int(sys.argv[ridx + 1])

        es.create(src, expire_hours=expire, max_reads=max_reads)

    elif "--open" in sys.argv:
        idx = sys.argv.index("--open")
        fname = sys.argv[idx + 1]

        key = None
        if "--key" in sys.argv:
            kidx = sys.argv.index("--key")
            key = sys.argv[kidx + 1]

        es.open(fname, access_key=key)

    elif "--status" in sys.argv:
        es.status()

    elif "--purge" in sys.argv:
        es.purge_expired()

    else:
        print("🔥 阅后即焚文件分享")
        print("   --create <文件> [--expire 小时] [--reads 次数]  创建焚毁包")
        print("   --open <焚毁包.eph> [--key 密钥]              打开阅读")
        print("   --status                                       查看状态")
        print("   --purge                                        清理过期")
        es.status()


if __name__ == "__main__":
    main()