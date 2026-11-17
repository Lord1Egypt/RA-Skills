#!/usr/bin/env bash
# yt2podcast 首次配置(一条命令):装自带 adapter + 环境自检。
#
#   bash scripts/setup.sh
#
# 为什么需要:opencli 的 adapter 不会随 skill 安装自动注册(任何 skill 都做不到
# 在安装时执行代码),所以首次使用必须显式跑一次。装好后 `doctor.sh` 退出码为 0
# 才算就绪;之后 `new-job.sh` 会自己拦住未配置的环境,不会再跑到一半才失败。
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "== 1/2 安装自带 adapter(notebooklm download-audio / xiaoyuzhou upload, upload-status)"
bash "$DIR/install-adapters.sh" --install || {
  echo "adapter 安装失败,先修上面的报错。" >&2
  exit 1
}

echo
echo "== 2/2 环境自检"
bash "$DIR/doctor.sh"
rc=$?

if [ "$rc" -eq 0 ]; then
  echo
  echo "就绪。现在可以把 YouTube 链接发给 agent 了。"
else
  echo
  echo "还有阻塞项没解决(见上面 ❌ 与修复命令)。修好后重跑: bash $DIR/setup.sh"
fi
exit "$rc"
