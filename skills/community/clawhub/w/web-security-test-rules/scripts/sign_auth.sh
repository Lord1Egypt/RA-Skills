#!/usr/bin/env bash
# sign_auth.sh —— 对 AUTHORIZATION.json 的授权声明做非对称签名（RSA + SHA256）
#
# 主校验流程用的签名工具：授权方用私钥对"授权声明"签名，生成 signature + signed_payload，
# skill 在测试前用对应公钥验签（见 SKILL.md 授权门禁·主路径）。
#
# 用法：
#   AUTH_PRIVKEY=./private_keys/team-a.pem bash scripts/sign_auth.sh AUTHORIZATION.json
#
# 输入文件需含字段：
#   authorized_by, issued_at, valid_from, valid_until,
#   targets[], allowed_methods[], scope_note, key_id, nonce,
#   scope{ in_scope[], internal_ranges[], include_internal, out_of_scope[], accounts[] }
# 输出：
#   在原文件基础上追加 signed_payload（被签名的规范化字符串）与 signature（base64 签名）
#
# 安全注意：私钥绝不进仓库；用环境变量 AUTH_PRIVKEY 或本地 gitignore 目录引用。

set -euo pipefail

IN="${1:?用法: sign_auth.sh <AUTHORIZATION.json>}"
PRIV="${AUTH_PRIVKEY:?请设置环境变量 AUTH_PRIVKEY 指向私钥 PEM（如 ./private_keys/team-a.pem）}"
[ -f "$PRIV" ] || { echo "私钥不存在: $PRIV" >&2; exit 1; }
[ -f "$IN" ]   || { echo "授权文件不存在: $IN" >&2; exit 1; }

TMP=$(mktemp)
# 1) 抽取并规范化声明字段（排序、紧凑、不含 signature/signed_payload/checksum，无尾随换行）
python3 - "$IN" <<'PY' > "$TMP"
import sys, json
d = json.load(open(sys.argv[1], encoding='utf-8'))
fields = {k: d[k] for k in (
    "authorized_by","issued_at","valid_from","valid_until",
    "targets","allowed_methods","scope_note","key_id","nonce","scope"
) if k in d}
payload = json.dumps(fields, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
sys.stdout.write(payload)
PY

# 2) RSA + SHA256 签名，base64 编码
SIG_B64=$(openssl dgst -sha256 -sign "$PRIV" "$TMP" | base64 -w0)

# 3) 回写 signed_payload 与 signature
python3 - "$IN" "$TMP" <<PY
import sys, json
inp, tmp = sys.argv[1], sys.argv[2]
d = json.load(open(inp, encoding='utf-8'))
d["signed_payload"] = open(tmp, encoding='utf-8').read()
d["signature"] = "$SIG_B64"
json.dump(d, open(inp, "w", encoding='utf-8'), ensure_ascii=False, indent=2)
print("已签名并写回:", inp)
print("key_id =", d.get("key_id"))
PY

rm -f "$TMP"
