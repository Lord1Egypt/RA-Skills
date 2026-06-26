#!/bin/bash
# Session Manager for OpenClaw Context Persistence

LAST_SESSION_FILE="./memory/sessions/last-session-summary.md"
DAILY_SESSION_DIR="./memory/"

# 确保目录存在
mkdir -p $(dirname $LAST_SESSION_FILE)
mkdir -p $DAILY_SESSION_DIR

# 读取上一个会话摘要
function read_last_session() {
  if [ -f $LAST_SESSION_FILE ]; then
    cat $LAST_SESSION_FILE
  fi
}

# 追加新的会话要点
function append_session_point() {
  local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
  local point="$1"
  echo -e "\n## [$timestamp] $point" >> $LAST_SESSION_FILE
}

# 压缩会话摘要到当日文件
function archive_session() {
  local today=$(date "+%Y-%m-%d")
  local daily_file="${DAILY_SESSION_DIR}/${today}.md"
  if [ -f $LAST_SESSION_FILE ]; then
    cat $LAST_SESSION_FILE >> $daily_file
    # 清空last-session文件，保留头部
    echo -e "# 上一个会话要点摘要\n\n> 此文件在每次会话结束时自动更新\n" > $LAST_SESSION_FILE
  fi
}

# 处理命令
case "$1" in
  read)
    read_last_session
    ;;
  append)
    append_session_point "$2"
    ;;
  archive)
    archive_session
    ;;
  *)
    echo "Usage: $0 {read|append|archive}"
    exit 1
    ;;
esac
