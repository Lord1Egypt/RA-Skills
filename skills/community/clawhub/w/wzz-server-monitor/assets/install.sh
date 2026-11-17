#!/usr/bin/env bash
# wzz-server-monitor 一键安装
#   1. 检查/安装依赖 (psutil / pyyaml / jinja2)
#   2. 初始化 XDG 目录并生成配置模板
#   3. 校验配置 + 发送测试邮件（配置就绪时）
#   4. 幂等写入 crontab（每 5 分钟检查一次）
#   5. 提示 WSL2/容器 cron 服务注意事项
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PYTHON:-$(command -v python3 || echo /usr/bin/python3)}"
MONITOR="$SKILL_DIR/scripts/monitor.py"
CONFIG_DIR="$HOME/.config/resource-monitor"
STATE_DIR="$HOME/.local/state/resource-monitor"
CONFIG="$CONFIG_DIR/config.yaml"
CRON_TAG="wzz-server-monitor"
MIRROR="${PIP_MIRROR:--i https://pypi.tuna.tsinghua.edu.cn/simple}"

echo "==> 1/5 检查依赖"
if ! "$PY" -c "import psutil, yaml, jinja2" 2>/dev/null; then
  echo "缺少依赖，尝试安装 psutil pyyaml jinja2 ..."
  "$PY" -m pip install "$MIRROR" psutil pyyaml jinja2
else
  echo "依赖已就绪 (psutil / pyyaml / jinja2)"
fi

echo "==> 2/5 初始化目录与配置"
mkdir -p "$CONFIG_DIR" "$STATE_DIR"
if [ ! -f "$CONFIG" ]; then
  cp "$SKILL_DIR/assets/config.example.yaml" "$CONFIG"
  echo "已生成配置模板: $CONFIG"
  echo "  请先编辑该文件，填入 SMTP 与阈值，再重新运行本脚本。"
else
  echo "配置已存在: $CONFIG"
fi

echo "==> 3/5 校验配置"
if ! "$PY" "$MONITOR" validate-config --config "$CONFIG"; then
  echo "  ✗ 配置校验未通过，未安装定时任务。请编辑 $CONFIG 后重跑本脚本。"
  exit 1
fi
echo "  配置校验通过"

echo "==> 4/5 发送测试邮件"
if [ "${SKIP_TEST_MAIL:-0}" != "1" ]; then
  if "$PY" "$MONITOR" send-test --config "$CONFIG"; then
    echo "  测试邮件已发送 ✓"
  else
    echo "  ⚠️  测试邮件发送失败（SMTP 问题），但仍可继续安装定时任务。"
    echo "     排查：QQ/163 邮箱需用「授权码」而非登录密码；检查 security/port。"
  fi
else
  echo "  （SKIP_TEST_MAIL=1，跳过测试邮件）"
fi

echo "==> 5/5 安装 crontab（每 5 分钟检查一次）"
CRON_LINE="*/5 * * * * $PY $MONITOR check --config $CONFIG >> $STATE_DIR/monitor.log 2>&1"
( crontab -l 2>/dev/null | grep -v "$CRON_TAG" ; echo "# $CRON_TAG" ; echo "$CRON_LINE" ) | crontab -
echo "已写入 crontab:"
crontab -l | grep -A1 "$CRON_TAG" || true

# WSL2 / 容器中 cron 服务默认不启动
if ! pgrep -x cron >/dev/null 2>&1 && ! pgrep -x crond >/dev/null 2>&1; then
  echo "⚠️  未检测到 cron 服务进程。若在 WSL2 / Docker 容器中，请先启动:"
  echo "    sudo service cron start"
  echo "  如需开机自启，参见 SKILL.md 中「WSL2 cron 自启」一节。"
fi

echo ""
echo "完成。查看状态: $PY $MONITOR status --config $CONFIG"
