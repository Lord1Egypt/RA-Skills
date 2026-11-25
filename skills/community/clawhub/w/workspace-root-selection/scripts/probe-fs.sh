#!/usr/bin/env bash
# 文件系统适配探针：判断某目录能否当 OpenClaw 工作区
# 用法：bash probe-fs.sh <目标目录> [对照目录]
set -u
TARGET="${1:-}"
BASE="${2:-$HOME}"
N=300

if [ -z "$TARGET" ]; then
  echo "用法: bash probe-fs.sh <目标目录> [对照目录]" >&2
  exit 2
fi

probe() {
  local dir="$1" label="$2"
  if [ ! -d "$dir" ]; then
    printf '%-14s 目录不存在\n' "$label"
    return
  fi
  local fstype tmp t0 t1 write_ms case_note perm chmod_note i
  fstype=$(stat -f -c '%T' "$dir" 2>/dev/null)
  tmp="$dir/.oc-fs-probe-$$"
  rm -rf "$tmp" 2>/dev/null
  if ! mkdir -p "$tmp" 2>/dev/null; then
    printf '%-14s 不可写\n' "$label"
    return
  fi
  t0=$(date +%s%N)
  for i in $(seq 1 $N); do printf 'x' > "$tmp/f$i.txt"; done
  t1=$(date +%s%N)
  write_ms=$(( (t1 - t0) / 1000000 ))
  printf 'x' > "$tmp/MixedCase.txt"
  if [ -f "$tmp/mixedcase.txt" ]; then case_note="不敏感(会互吞)"; else case_note="敏感"; fi
  chmod 600 "$tmp/MixedCase.txt" 2>/dev/null
  perm=$(stat -c '%a' "$tmp/MixedCase.txt" 2>/dev/null)
  if [ "$perm" = "600" ]; then chmod_note="生效"; else chmod_note="无效(mode=$perm)"; fi
  printf '%-14s fs=%-7s 写%d文件=%6sms  大小写=%-12s chmod=%s\n' "$label" "$fstype" "$N" "$write_ms" "$case_note" "$chmod_note"
  rm -rf "$tmp" 2>/dev/null
}

echo "== 文件系统适配探针 (N=$N) =="
probe "$TARGET" "目标"
probe "$BASE" "对照"

if command -v python3 >/dev/null 2>&1; then
  python3 - "$TARGET" <<'PY'
import os, sqlite3, sys, tempfile, shutil
base = sys.argv[1]
try:
    d = tempfile.mkdtemp(dir=base)
    db = os.path.join(d, "t.db")
    c = sqlite3.connect(db)
    c.execute("create table t(a int)")
    c.execute("insert into t values(1)")
    c.commit()
    n = c.execute("select count(*) from t").fetchone()[0]
    c.close()
    print("SQLite          基础读写=%s" % ("正常" if n == 1 else "异常"))
    shutil.rmtree(d, ignore_errors=True)
except Exception as e:
    print("SQLite          失败: %s: %s" % (type(e).__name__, e))
PY
fi
