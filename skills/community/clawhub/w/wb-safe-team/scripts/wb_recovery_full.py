#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wb_recovery_full.py —— 全量/换机恢复演练脚本（WB-SAFE 灾备恢复官）
=====================================================================
⚠️ 执行约束（来自实战红线）：
  * 默认 --dry-run：只估算复制范围与大小，**不碰任何真实数据**。
  * 真执行需显式 --execute，且会占用 C 盘磁盘（全量比子集大很多）。
  * 平台托管的 OAuth 凭据（kdocs/lexiang/wecom/...）恢复后须通过平台重授权，
    本机无法自动完成 —— 这是演练的已知差距，脚本会显式标注。
  * 单进程内完成 复制→验证→清理，规避 Temp 跨 Bash 调用被清空的坑。
  * 绝不拿真实生产数据试恢复；冲突文件只报不改。

复制范围（代表性全量，排除二进制/缓存噪声）：
  身份 SOUL/IDENTITY/USER · 长期记忆 MEMORY · 自建专家团包（wb-safe-team/medxpert-ops-team）
  连接器元数据目录（只读存在性，不含密钥值）· 工作区配置快照文档

用法：
  python3 wb_recovery_full.py            # dry-run（默认，安全）
  python3 wb_recovery_full.py --execute  # 真执行（需用户授权，占磁盘）
"""
import os, sys, io, json, glob, hashlib, shutil, time, argparse

HOME   = os.path.expanduser("~").replace("\\", "/")
WB     = os.environ.get("WB_WS", "") or \
         sorted(glob.glob(os.path.join(HOME, "WorkBuddy", "20*")), reverse=True)[0]
SRC    = os.path.join(HOME, ".workbuddy")
TEAMS  = ["wb-safe-team"]
SB     = os.path.join(os.environ.get("TEMP", "/tmp"), "wb_recovery_full_sandbox")

# 复制清单（源 -> 沙箱子路径）
def plan():
    P = []
    for f in ["SOUL.md", "IDENTITY.md", "USER.md", "MEMORY.md"]:
        s = os.path.join(SRC, f)
        if os.path.isfile(s): P.append((s, "identity/" + f))
    for t in TEAMS:
        s = os.path.join(SRC, "plugins/marketplaces/my-experts/plugins", t)
        if os.path.isdir(s): P.append((s, "experts/" + t))  # 整目录
    # 连接器元数据（只读存在性，不含密钥值；排除 .master.key 等真实密钥）
    for root, dirs, files in os.walk(os.path.join(SRC, "connectors")):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if f.endswith(".key") or f == ".master.key":
                continue  # 跳过真实密钥文件
            P.append((os.path.join(root, f), "connectors_meta/" + f))
    # 工作区配置快照文档
    for rel in glob.glob(os.path.join(WB, "配置快照_*.md")) + \
               glob.glob(os.path.join(WB, "专家团_*安全配置.md")):
        P.append((rel, "snapshots/" + os.path.basename(rel)))
    return P

def h16(p):
    return hashlib.sha256(io.open(p, "rb").read()).hexdigest()[:16]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--execute", action="store_true", help="真执行（占磁盘，需授权）")
    args = ap.parse_args()
    P = plan()
    print("复制项: %d | 估算大小: %.1f MB" % (len(P), sum(os.path.getsize(s) for s, _ in P if os.path.isfile(s))/1e6))

    if not args.execute:
        print("[dry-run] 未执行任何复制。真实执行需 --execute（将占用 C 盘磁盘）。")
        for s, d in P[:8]:
            print("   将复制: %s -> %s" % (s.replace(HOME, "~"), d))
        if len(P) > 8: print("   ... 其余 %d 项略" % (len(P)-8))
        print("[差距] 平台托管 OAuth 凭据恢复后须平台重授权，本机无法自动完成。")
        return

    # ---- 真执行（单进程内 复制→验证→清理）----
    t0 = time.time()
    if os.path.exists(SB): shutil.rmtree(SB)
    for sub in ["identity", "experts", "connectors_meta", "snapshots"]:
        os.makedirs(os.path.join(SB, sub), exist_ok=True)
    copied = 0
    for s, d in P:
        dst = os.path.join(SB, d)
        try:
            if os.path.isdir(s):
                shutil.copytree(s, dst)
            else:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy(s, dst)
            copied += 1
        except Exception as e:
            print("  复制失败 %s: %s" % (s, e))
    RTO = round(time.time() - t0, 2)

    # 验证：团包结构
    for t in TEAMS:
        base = os.path.join(SB, "experts", t)
        pj = os.path.join(base, ".codebuddy-plugin", "plugin.json")
        ok = os.path.isfile(pj)
        ag = len(glob.glob(os.path.join(base, "agents", "*.md")))
        print("  验证 %s: plugin.json=%s agents=%d" % (t, ok, ag))
    # 对账：团包 SHA256 vs 源
    mismatch = 0; checked = 0
    for t in TEAMS:
        sdir = os.path.join(SRC, "plugins/marketplaces/my-experts/plugins", t)
        tdir = os.path.join(SB, "experts", t)
        for f in glob.glob(os.path.join(sdir, "agents", "*.md")) + [os.path.join(sdir, ".codebuddy-plugin", "plugin.json")]:
            rel = os.path.basename(f); tf = os.path.join(tdir, rel if not rel.endswith("plugin.json") else ".codebuddy-plugin/plugin.json")
            if os.path.isfile(f) and os.path.isfile(tf):
                checked += 1
                if h16(f) != h16(tf): mismatch += 1
    print("RTO(复制耗时)= %s 秒 | 对账文件=%d 不一致=%d" % (RTO, checked, mismatch))
    print("[差距] 平台托管 OAuth 重授权预案需在平台侧实测，不在本机范围。")
    shutil.rmtree(SB)
    print("[清理] 沙箱已删除:", not os.path.exists(SB))

if __name__ == "__main__":
    main()
