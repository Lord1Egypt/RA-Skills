#!/usr/bin/env bash
# linux_extra.sh — 补充真实测试（在 linux_e2e.sh 之外）
#  1) 网页端「管理员权限」真实 apply：非 root 启动 UI，用 sudo 提权改 /etc/ssh/sshd_config
#  2) 真实封禁与回滚：iptables 添加 DROP 规则 → 校验存在 → --rollback → 校验已移除
# 需 root：sudo bash tests/linux_extra.sh
# 依赖 ${SKILL:-/home/ubuntu/ssg} 下的 skill（如路径不同，改下面的 SKILL 变量）
set -u
SKILL="${SKILL:-/home/ubuntu/ssg}"
PASS=0; FAIL=0
ok(){ PASS=$((PASS+1)); echo "  PASS $1"; }
bad(){ FAIL=$((FAIL+1)); echo "  FAIL $1  ${2:-}"; }
h(){ echo; echo "== $1 =="; }

WORK=$(mktemp -d)
SSHD=/etc/ssh/sshd_config
BAKS_BEFORE="$(ls -1 "$SSHD".guard-bak.* 2>/dev/null || true)"
cleanup(){
    pkill -f "web_ui.py --port 18444" 2>/dev/null
    if [ -f "$WORK/sshd.orig" ]; then cp -a "$WORK/sshd.orig" "$SSHD"; systemctl reload ssh 2>/dev/null; fi
    for f in "$SSHD".guard-bak.*; do
        [ -e "$f" ] || continue
        printf '%s\n' "$BAKS_BEFORE" | grep -qxF "$f" || rm -f "$f"
    done
    iptables -D INPUT -s 203.0.113.66 -j DROP 2>/dev/null
    rm -rf "$WORK"
}
trap cleanup EXIT

h "1) 网页端 + sudo 真实 apply"
cp -a "$SSHD" "$WORK/sshd.orig"
cat > "$SSHD" <<EOF
Port 22
PermitRootLogin yes
PasswordAuthentication yes
PermitEmptyPasswords yes
UsePAM yes
EOF
systemctl reload ssh 2>/dev/null
grep -q '^PermitRootLogin yes' "$SSHD" && ok "弱配置已就绪" || bad "弱配置写入失败"

python3 ${SKILL:-/home/ubuntu/ssg}/scripts/web_ui.py --port 18444 > "$WORK/web.log" 2>&1 &
for _ in $(seq 1 40); do grep -q 'Local-only UI' "$WORK/web.log" && break; sleep 0.25; done
TOK=$(grep -o 'https://127.0.0.1:[0-9]*/#[A-Za-z0-9_-]*' "$WORK/web.log" | head -1 | sed 's/.*#//')
[ -n "$TOK" ] && ok "网页端启动（非 root 用户 ubuntu）" || { bad "网页端未启动"; tail -5 "$WORK/web.log"; }

if [ -n "$TOK" ]; then
python3 - "$TOK" "$WORK/result.json" <<'PY'
import json, ssl, sys, urllib.request, urllib.error
tok, out = sys.argv[1], sys.argv[2]
ctx = ssl._create_unverified_context()
op = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPSHandler(context=ctx))
B = "https://127.0.0.1:18444"
def post(p, b):
    r = urllib.request.Request(B+p, data=json.dumps(b).encode(), method="POST",
        headers={"Authorization": "Bearer "+tok, "Content-Type": "application/json"})
    try:
        with op.open(r, timeout=120) as x: return x.status, json.loads(x.read())
    except urllib.error.HTTPError as e: return e.code, json.loads(e.read())
res = {}
c, scan = post("/api/scan", {"target":"local","scope":"config"})
res["scan"] = c
ids = [f["id"] for f in scan.get("findings", []) if f.get("auto_fixable") and f["id"] != "CFG-06"]
res["cfg06_autofix"] = [f.get("auto_fixable") for f in scan.get("findings", []) if f["id"]=="CFG-06"][:5]
res["ids"] = ids
if not ids:
    print(json.dumps(res)); raise SystemExit(0)
# 关键：勾选管理员权限 + 密码（该机 NOPASSWD，sudo -S 会忽略密码但仍走 sudo 路径）
c, prev = post("/api/preview", {"scan_id":scan["scan_id"],"items":ids[:2],
                                "use_sudo":True,"sudo_password":"x"})
res["preview"] = c
res["preview_status"] = [r["status"] for r in prev.get("results", [])]
if c == 200:
    c, app = post("/api/apply", {"scan_id":scan["scan_id"],"items":ids[:2],"confirmation":"APPLY",
                                 "confirm_token":prev["confirm_token"],
                                 "use_sudo":True,"sudo_password":"x"})
    res["apply"] = c
    res["elevated"] = app.get("elevated")
    res["statuses"] = [r["status"] for r in app.get("results", [])]
    res["summary"] = app.get("summary")
open(out,"w").write(json.dumps(res, ensure_ascii=False))
print(json.dumps(res, ensure_ascii=False))
PY
    R="$WORK/result.json"
    [ -f "$R" ] || echo '{}' > "$R"
    python3 - "$R" <<'PY' && ok "网页端 scan→preview→apply（sudo）链路全通" || bad "网页端链路未通过"
import json,sys
d=json.load(open(sys.argv[1]))
ok = (d.get("scan")==200 and d.get("preview")==200 and d.get("apply")==200
      and d.get("elevated") is True and all(s=="fixed" for s in d.get("statuses",[])))
sys.exit(0 if ok else 1)
PY
    R_IDS=$(python3 -c "import json;print(json.load(open('$R')).get('ids'))" 2>/dev/null)
    echo "     命中并可修复: $R_IDS"
    grep -q '^PermitRootLogin no' "$SSHD" && ok "sudo 路径确实改到了 /etc/ssh/sshd_config" || bad "文件未被修改"
    # 前两个可修复项是 CFG-01/CFG-02，故校验 PasswordAuthentication
    grep -qE '^PasswordAuthentication no' "$SSHD" && ok "第二项（CFG-02 密码登录）同样生效" || bad "第二项未生效"
fi
pkill -f "web_ui.py --port 18444" 2>/dev/null
cp -a "$WORK/sshd.orig" "$SSHD"; systemctl reload ssh 2>/dev/null
ok "已还原 sshd_config"

h "2) 真实封禁 + 回滚（iptables）"
cat > "$WORK/monitor.json" <<'EOF'
{"target":"local","window":"24h","events":[
 {"type":"brute_force","source_ip":"203.0.113.66","severity":"HIGH","failed_count":9,
  "evidence":["test"],"target_users":["root"]}]}
EOF
python3 ${SKILL:-/home/ubuntu/ssg}/scripts/attack_defend.py --target local --input "$WORK/monitor.json" \
    --action block --ips 203.0.113.66 --apply --output "$WORK/defend.json" >/dev/null 2>"$WORK/defend.err"
if [ $? -eq 0 ]; then
    ok "封禁命令执行成功"
    iptables -C INPUT -s 203.0.113.66 -j DROP 2>/dev/null && ok "iptables 规则确实存在" || bad "规则不存在"
    RB=$(python3 -c "import json;print(len(json.load(open('$WORK/defend.json')).get('rollback_commands',[])))")
    [ "$RB" -ge 1 ] && ok "生成回滚命令 ($RB 条)" || bad "无回滚命令"
    python3 ${SKILL:-/home/ubuntu/ssg}/scripts/attack_defend.py --target local --rollback "$WORK/defend.json" \
        --apply --output "$WORK/rollback.json" >/dev/null 2>&1
    if iptables -C INPUT -s 203.0.113.66 -j DROP 2>/dev/null; then bad "回滚后规则仍存在"; else ok "回滚后规则已移除"; fi
else
    bad "封禁失败" "$(tail -3 "$WORK/defend.err")"
fi

h "汇总"
echo "  PASS=$PASS FAIL=$FAIL"
[ "$FAIL" -eq 0 ] && echo "  结果: 通过" || echo "  结果: 有失败"
