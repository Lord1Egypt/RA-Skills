# -*- coding: utf-8 -*-
"""verify_archive.py — 无人值守备份类任务的产物验证参考实现

固化自真实事故（两次备份损坏上传）的验证链：
  打包 → 本地双重验证 → 验证不过不上传不写状态 → "已存在"产物先验证后复用

可直接嵌入任何 backup/pipeline 脚本，或作为独立校验工具调用。
脱敏说明：所有路径/凭据均为占位符，替换后使用。
"""
import os
import subprocess
import json
from datetime import datetime

# ===== 配置区（按需替换） =====
STATE_FILE = "/path/to/backup_state.json"   # 状态文件：只在产物验证+上传双成功后更新
STATE_KEY = "last_backup"                    # 状态键名


def verify_archive(archive_path):
    """产物双重验证：gzip 流完整性 + tar 归档结构。
    返回 (ok, reason)。截断文件在 gzip -t 暴露；tar 头损坏在 -tzf 暴露。"""
    rc1 = subprocess.run(["gzip", "-t", archive_path],
                         capture_output=True).returncode
    if rc1 != 0:
        return False, f"gzip -t failed (rc={rc1}): truncated or corrupt"
    rc2 = subprocess.run(["tar", "-tzf", archive_path],
                         capture_output=True).returncode
    if rc2 != 0:
        return False, f"tar -tzf failed (rc={rc2}): archive structure corrupt"
    return True, "ok"


def get_or_rebuild(archive_path, rebuild_fn):
    """'已存在则跳过'短路的安全版：存在先验证，损坏删掉重建（自愈）。
    rebuild_fn: 无参函数，执行真正的打包，返回 archive_path。
    返回 (archive_path, reused: bool)"""
    if os.path.exists(archive_path):
        ok, reason = verify_archive(archive_path)
        if ok:
            print(f"  今日产物已存在(验证通过): {os.path.basename(archive_path)}")
            return archive_path, True
        # 坑位实录：直接 return 会把坏文件当合法产物传给下游
        print(f"  ⚠️ 产物存在但损坏({reason})，删除重打包")
        os.remove(archive_path)
    return rebuild_fn(), False


def update_state_on_success():
    """状态更新纪律：只在验证+上传双成功后调用。
    失败路径不写状态 → 下一轮调度自然重试，不会因状态已标记而跳过。"""
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            state = json.load(f)
    state[STATE_KEY] = datetime.now().isoformat()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def run_backup_task(archive_path, rebuild_fn, upload_fn):
    """完整链路编排：验证不过不上传；上传失败不写状态。
    upload_fn: 无参函数，执行上传，返回 bool。"""
    archive, _ = get_or_rebuild(archive_path, rebuild_fn)

    ok, reason = verify_archive(archive)
    if not ok:
        print(f"  ❌ 验证失败({reason})，跳过上传，state 不更新（下轮重试）")
        return False

    if not upload_fn():
        print("  ❌ 上传失败，state 不更新（下轮重试）")
        return False

    update_state_on_success()
    print("  ✅ 验证+上传双成功，state 已更新")
    return True


if __name__ == "__main__":
    # 独立使用：python verify_archive.py <archive.tar.gz>
    import sys
    if len(sys.argv) != 2:
        print("用法: python verify_archive.py <archive.tar.gz>")
        sys.exit(2)
    ok, reason = verify_archive(sys.argv[1])
    print(f"{sys.argv[1]}: {'OK' if ok else 'BROKEN — ' + reason}")
    sys.exit(0 if ok else 1)
