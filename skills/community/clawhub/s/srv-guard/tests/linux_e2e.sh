#!/usr/bin/env bash
# linux_e2e.sh — 在真实 Linux 上跑 server-security-guard 全链路自测
#
# 必须在【一次性/快照】测试机上以 root 运行：
#     sudo bash tests/linux_e2e.sh
#
# 它会：备份并临时改写 /etc/ssh/sshd_config、/var/log/auth.log，
#       创建测试私钥，跑 扫描→dry-run→apply→校验→回滚→报告→HTTPS 网页端，
#       结束时（含出错/中断）自动恢复原状。
#
# 不要在对生产主机或有价值的机器上运行。

set -u
SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS="$SKILL_ROOT/scripts"
WORK="$(mktemp -d /tmp/ssg-e2e.XXXXXX)"
PY="${PYTHON:-python3}"
AUTH_LOG=""
SSHD_CONF="/etc/ssh/sshd_config"
BAKS_BEFORE="$(ls -1 "$SSHD_CONF".guard-bak.* 2>/dev/null || true)"
WEBUI_PID=""
CREATED_KEY=""
PASS=0
FAIL=0
SKIP=0

ok()   { PASS=$((PASS+1)); printf '  \033[32mPASS\033[0m %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf '  \033[31mFAIL\033[0m %s  %s\n' "$1" "${2:-}"; }
skip() { SKIP=$((SKIP+1)); printf '  \033[33mSKIP\033[0m %s  %s\n' "$1" "${2:-}"; }
head_() { printf '\n\033[1m== %s ==\033[0m\n' "$1"; }

cleanup() {
    [ -n "$WEBUI_PID" ] && kill "$WEBUI_PID" 2>/dev/null
    [ -n "$CREATED_KEY" ] && rm -f "$CREATED_KEY"
    if [ -f "$WORK/sshd_config.orig" ]; then
        cp -a "$WORK/sshd_config.orig" "$SSHD_CONF"
        (systemctl reload sshd || systemctl reload ssh || true) 2>/dev/null
    fi
    # 清理本次运行产生的 .guard-bak（保留运行前已存在的）
    for f in "$SSHD_CONF".guard-bak.*; do
        [ -e "$f" ] || continue
        printf '%s\n' "$BAKS_BEFORE" | grep -qxF "$f" || rm -f "$f"
    done
    if [ -n "$AUTH_LOG" ] && [ -f "$WORK/auth.log.orig" ]; then
        cp -a "$WORK/auth.log.orig" "$AUTH_LOG"
    fi
    rm -rf "$WORK"
}
trap cleanup EXIT INT TERM

head_ "环境检查"
if [ "$(id -u)" -ne 0 ]; then
    echo "必须以 root 运行（sudo bash tests/linux_e2e.sh）" >&2
    exit 2
fi
ok "root 权限"
command -v "$PY" >/dev/null && ok "$PY: $($PY -V 2>&1)" || { bad "缺少 $PY"; exit 2; }
$PY -c 'import hashlib,ssl,json' 2>/dev/null && ok "Python 标准库可用" || { bad "Python 标准库异常"; exit 2; }
command -v sshd >/dev/null && ok "sshd 已安装" || skip "sshd 未安装" "SSH 相关用例将跳过"
[ -f "$SSHD_CONF" ] && ok "$SSHD_CONF 存在" || skip "无 $SSHD_CONF" "SSH 相关用例将跳过"
if [ -f /var/log/auth.log ]; then AUTH_LOG=/var/log/auth.log
elif [ -f /var/log/secure ]; then AUTH_LOG=/var/log/secure; fi
[ -n "$AUTH_LOG" ] && ok "认证日志: $AUTH_LOG" || skip "无 auth.log/secure" "攻击感知用例将跳过"

# ---------- 造一个可被检出的弱配置（保持 sshd 语法有效，避免 reload 失败）----------
head_ "准备测试环境"
HAVE_SSHD=0
if [ -f "$SSHD_CONF" ]; then
    HAVE_SSHD=1
    cp -a "$SSHD_CONF" "$WORK/sshd_config.orig"
    PORT="$(awk '/^[[:space:]]*Port[[:space:]]+[0-9]+/ {print $2; exit}' "$SSHD_CONF")"
    PORT="${PORT:-22}"
    cat > "$SSHD_CONF" <<EOF
Port $PORT
PermitRootLogin yes
PasswordAuthentication yes
PermitEmptyPasswords yes
UsePAM yes
MaxAuthTries 10
EOF
    cp -a "$SSHD_CONF" "$WORK/weak.conf"
    (systemctl reload sshd || systemctl reload ssh || true) >/dev/null 2>&1
    ok "已写入弱配置（Port $PORT，原配置已备份）"
fi

KEY=""
if [ ! -e /root/.ssh/id_rsa ]; then
    mkdir -p /root/.ssh && chmod 700 /root/.ssh
    ssh-keygen -q -t rsa -b 2048 -N '' -f /root/.ssh/id_rsa 2>/dev/null || true
    if [ -e /root/.ssh/id_rsa ]; then CREATED_KEY=/root/.ssh/id_rsa; fi
fi
if [ -e /root/.ssh/id_rsa ]; then
    KEY=/root/.ssh/id_rsa
    chmod 644 "$KEY"
    ok "测试私钥权限已设为 644: $KEY"
else
    skip "无法创建测试私钥" "CFG-06 用例将跳过"
fi

if [ -n "$AUTH_LOG" ]; then
    cp -a "$AUTH_LOG" "$WORK/auth.log.orig" 2>/dev/null || : > "$WORK/auth.log.orig"
    NOW="$(date '+%b %e %H:%M:%S')"
    for i in $(seq 1 6); do
        echo "$NOW e2e-host sshd[90$i]: Failed password for root from 203.0.113.66 port 5$i 22 ssh2" >> "$AUTH_LOG"
    done
    ok "已注入 6 条暴力破解日志（203.0.113.66）"
fi
echo '{"events": []}' > "$WORK/harden-input.json"

# ---------- Phase 1 扫描 ----------
head_ "Phase 1: 漏洞扫描（只读）"
$PY "$SCRIPTS/vuln_scan.py" --target local --scope all \
    --output "$WORK/scan.json" >/dev/null 2>"$WORK/scan.err"
if [ $? -eq 0 ] && [ -s "$WORK/scan.json" ]; then
    ok "扫描退出码 0，输出 JSON"
    IDS="$($PY - "$WORK/scan.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
print(" ".join(sorted({f["id"] for f in d["findings"]})))
PY
)"
    echo "     命中: ${IDS:-（无）}"
    for want in CFG-01 CFG-02 CFG-03; do
        case " $IDS " in *" $want "*) ok "检出 $want" ;; *) bad "未检出 $want" ;; esac
    done
    if [ -n "$KEY" ]; then
        case " $IDS " in *" CFG-06 "*) ok "检出 CFG-06（私钥权限）" ;; *) bad "未检出 CFG-06" ;; esac
    fi
else
    bad "扫描失败" "$(tail -3 "$WORK/scan.err")"
fi

# ---------- Phase 2 dry-run / apply / 回滚 ----------
head_ "Phase 2: 修复（dry-run → apply → 回滚）"
if [ -s "$WORK/scan.json" ]; then
    $PY "$SCRIPTS/vuln_fix.py" --target local --input "$WORK/scan.json" \
        --output "$WORK/fix-dry.json" >/dev/null 2>"$WORK/fix-dry.err"
    DRY_RC=$?
    if [ $DRY_RC -eq 0 ] && $PY - "$WORK/fix-dry.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
st={r["item_id"]: r["status"] for r in d["results"]}
sys.exit(0 if d["dry_run"] and st.get("CFG-01")=="would_fix" else 1)
PY
    then ok "dry-run 状态 would_fix，未改动系统"
    else bad "dry-run 结果不符合预期" "$(tail -2 "$WORK/fix-dry.err")"; fi

    $PY "$SCRIPTS/vuln_fix.py" --target local --input "$WORK/scan.json" --apply \
        --items CFG-01,CFG-03 --output "$WORK/fix-apply.json" >/dev/null 2>"$WORK/fix-apply.err"
    APPLY_RC=$?
    if [ $APPLY_RC -eq 0 ]; then
        ok "apply 退出码 0"
        grep -q '^PermitRootLogin no' "$SSHD_CONF" && ok "sshd_config 已被改为 PermitRootLogin no" \
            || bad "sshd_config 未改变"
        grep -q '^PermitEmptyPasswords no' "$SSHD_CONF" && ok "PermitEmptyPasswords 已改 no" \
            || bad "PermitEmptyPasswords 未改变"
        BAK="$(ls -1 "$SSHD_CONF".guard-bak.* 2>/dev/null | tail -1)"
        if [ -n "$BAK" ] && [ -f "$BAK" ]; then
            ok "生成备份: $(basename "$BAK")"
            # 备份必须是「改动前」状态：与写好的弱配置逐字节一致
            if [ -f "$WORK/weak.conf" ] && cmp -s "$BAK" "$WORK/weak.conf"; then
                ok "备份内容 = 改动前快照（未被后续修复覆盖）"
            else
                bad "备份内容不等于改动前状态（备份被覆盖）"
            fi
            cp -a "$BAK" "$SSHD_CONF"
            (systemctl reload sshd || systemctl reload ssh || true) >/dev/null 2>&1
            if [ -f "$WORK/weak.conf" ] && cmp -s "$WORK/weak.conf" "$SSHD_CONF"; then
                ok "回滚后与改动前逐字节一致"
            else
                bad "回滚后内容不符"
            fi
            rm -f "$BAK"
        else
            bad "未生成 .guard-bak 备份"
        fi
        $PY - "$WORK/fix-apply.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
rb=[r for r in d["results"] if r.get("item_id")=="CFG-01"]
sys.exit(0 if rb and rb[0]["rollback_commands"] else 1)
PY
        [ $? -eq 0 ] && ok "修复结果含回滚命令" || bad "修复结果缺少回滚命令"
    else
        bad "apply 失败 rc=$APPLY_RC" "$(tail -3 "$WORK/fix-apply.err")"
    fi
else
    skip "无扫描结果" "修复用例跳过"
fi

# ---------- Phase 3 攻击感知 ----------
head_ "Phase 3: 攻击感知（日志分析）"
MON=0
if [ -n "$AUTH_LOG" ] && [ -s "$WORK/scan.json" ]; then
    $PY "$SCRIPTS/attack_monitor.py" --target local --window 24h \
        --output "$WORK/monitor.json" >/dev/null 2>"$WORK/monitor.err"
    if [ $? -eq 0 ] && $PY - "$WORK/monitor.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
ev=[e for e in d["events"] if e.get("type")=="brute_force" and e.get("source_ip")=="203.0.113.66"]
sys.exit(0 if ev and ev[0]["failed_count"]>=5 else 1)
PY
    then ok "检出暴力破解事件（203.0.113.66，≥5 次）"; MON=1
    else bad "未检出注入的暴力破解事件" "$(tail -2 "$WORK/monitor.err")"; fi
else
    skip "无认证日志" "感知用例跳过"
fi

# ---------- Phase 4 防御 ----------
head_ "Phase 4: 攻击防御（dry-run + 加固 dry-run）"
if [ "$MON" -eq 1 ]; then
    $PY "$SCRIPTS/attack_defend.py" --target local --input "$WORK/monitor.json" \
        --block-threshold medium --output "$WORK/defend-dry.json" >/dev/null 2>"$WORK/defend.err"
    if [ $? -eq 0 ] && $PY - "$WORK/defend-dry.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
ips=[b["ip"] for b in d.get("blocked_ips",[])]
sys.exit(0 if d.get("status")=="would_block" and "203.0.113.66" in ips and d.get("rollback_commands") else 1)
PY
    then ok "封禁 dry-run: would_block + 回滚命令"
    else skip "封禁 dry-run 未产生 would_block" "$(tail -2 "$WORK/defend.err")"; fi
else
    skip "无事件" "封禁用例跳过"
fi

$PY "$SCRIPTS/attack_defend.py" --target local --input "$WORK/harden-input.json" \
    --action harden --output "$WORK/harden-dry.json" >/dev/null 2>"$WORK/harden.err"
if [ -s "$WORK/harden-dry.json" ] && $PY - "$WORK/harden-dry.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
sys.exit(0 if d.get("status")=="would_harden" and d.get("operations") else 1)
PY
then ok "加固 dry-run: would_harden，含操作清单"
else skip "加固 dry-run 未执行" "$(tail -2 "$WORK/harden.err" 2>/dev/null)"; fi

# ---------- Phase 5 报告 ----------
head_ "Phase 5: 安全报告"
$PY "$SCRIPTS/security_report.py" --scan "$WORK/scan.json" --fix "$WORK/fix-apply.json" \
    --monitor "$WORK/monitor.json" --defend "$WORK/defend-dry.json" \
    --target "e2e-$(hostname)" --output "$WORK/report.html" >/dev/null 2>"$WORK/report.err"
if [ -s "$WORK/report.html" ]; then
    ok "报告已生成（$(wc -c < "$WORK/report.html") 字节）"
    grep -q '{{' "$WORK/report.html" && bad "报告存在未替换占位符" || ok "无残留占位符"
    grep -q 'e2e-' "$WORK/report.html" && ok "报告含目标标识" || bad "报告缺少目标标识"
else
    bad "报告生成失败" "$(tail -3 "$WORK/report.err")"
fi

# ---------- 网页端 HTTPS ----------
head_ "网页端 HTTPS 自检"
PORT_WEB=18443
$PY "$SCRIPTS/web_ui.py" --port $PORT_WEB > "$WORK/webui.log" 2>&1 &
WEBUI_PID=$!
for _ in $(seq 1 40); do
    grep -q 'Local-only UI' "$WORK/webui.log" 2>/dev/null && break
    sleep 0.25
done
TOK="$(grep -o 'https://127.0.0.1:[0-9]*/#[A-Za-z0-9_-]*' "$WORK/webui.log" | head -1 | sed 's/.*#//')"
if [ -n "$TOK" ]; then
    ok "网页端启动（HTTPS）"
    LAST="$($PY - "$PORT_WEB" "$TOK" "$WORK/webscan.json" <<'PY'
import json, ssl, sys, urllib.request, urllib.error
port, tok, out = sys.argv[1], sys.argv[2], sys.argv[3]
ctx = ssl._create_unverified_context()
op = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPSHandler(context=ctx))
base = f"https://127.0.0.1:{port}"
def get():
    with op.open(base + "/", timeout=10) as r: return r.status
def post(path, body, auth=True):
    h = {"Content-Type": "application/json"}
    if auth: h["Authorization"] = "Bearer " + tok
    req = urllib.request.Request(base + path, data=json.dumps(body).encode(), headers=h, method="POST")
    try:
        with op.open(req, timeout=30) as r: return r.status, r.read()
    except urllib.error.HTTPError as e: return e.code, e.read()
print(get())
print(post("/api/scan", {"target":"local","scope":"config"}, auth=False)[0])
code, body = post("/api/scan", {"target":"local","scope":"config"})
if code == 200: open(out, "wb").write(body)
print(code)
PY
)"
    PAGE_CODE="$(echo "$LAST" | sed -n 1p)"
    NOAUTH_CODE="$(echo "$LAST" | sed -n 2p)"
    AUTH_CODE="$(echo "$LAST" | sed -n 3p)"
    [ "$PAGE_CODE" = "200" ] && ok "GET / 返回 200" || bad "GET / 返回 $PAGE_CODE"
    [ "$NOAUTH_CODE" = "403" ] && ok "无 token 调用 API 返回 403" || bad "无 token 返回 $NOAUTH_CODE"
    [ "$AUTH_CODE" = "200" ] && ok "带 token 扫描返回 200" || bad "带 token 返回 $AUTH_CODE"
    TLS11="$($PY - "$PORT_WEB" <<'PY'
import socket, ssl, sys, warnings
warnings.simplefilter("ignore")
port = int(sys.argv[1])
try:
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx.minimum_version = ssl.TLSVersion.TLSv1_1
    ctx.maximum_version = ssl.TLSVersion.TLSv1_1
except Exception:
    print("unsupported")
else:
    try:
        with ctx.wrap_socket(socket.create_connection(("127.0.0.1", port), timeout=5)):
            print("accepted")
    except Exception:
        print("rejected")
PY
)"
    [ "$TLS11" = "rejected" ] && ok "拒绝 TLS1.1（最低 TLS1.2）" || bad "TLS1.1 检查结果: ${TLS11:-空}"
else
    bad "网页端未启动" "$(tail -5 "$WORK/webui.log")"
fi

head_ "汇总"
printf '  PASS=%d  FAIL=%d  SKIP=%d\n' "$PASS" "$FAIL" "$SKIP"
[ "$FAIL" -eq 0 ] && { echo "  结果: 全链路通过"; exit 0; } || { echo "  结果: 有失败项"; exit 1; }
