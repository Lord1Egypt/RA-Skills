#!/bin/zsh
set -u
tool_dir="${0:A:h}"
print '恢复当前账号的本地项目、会话关联和空间归属'
print '请先用 ⌘Q 完全退出 ChatGPT/Codex。'
print ''
python3 "$tool_dir/restore_local_projects.py" --apply
result=$?
print ''
read -r '?按回车关闭窗口。'
exit "$result"
