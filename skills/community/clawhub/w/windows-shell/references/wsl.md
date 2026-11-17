# WSL：值不值得上，以及必知陷阱

考虑把项目搬进 WSL、或已在 WSL 中遇到问题时读本文。

## 什么时候才值得上 WSL

WSL 的优势只有一个来源：**ext4 原生文件系统**。而它成立的前提是**项目文件真的放在 ext4 里**。

| 操作 | ext4（WSL 原生） | NTFS（Windows 原生） | `/mnt/*`（WSL 访问 Windows 盘） |
|------|------|------|------|
| tsc 类型检查 | 1.00x | 1.52x | **4.93x** |
| vitest | 1.00x | 2.36x | **9.69x** |
| 3000 个小文件增删查 | 1.00x | 8.96x | **54.2x** |

**判定规则：**

- 项目在 `C:\` / `D:\` 上 → **不要用 WSL 操作它**。`/mnt/*` 走 9p 协议逐文件跨界，比纯 Windows 还慢 4–6 倍，而且惩罚随项目规模线性放大（文件数 ×3.5，惩罚 ×2）。小 demo 上试不出来，真项目上卡死。
- 项目能整个搬进 WSL 的 `~/` 且构建密集 → 值得，编译测试全项最快。
- 只是想跑 `make`、`gcc`、`rsync` → 值得，但记得项目也要在 ext4。
- 其它情况 → 留在 Git Bash。

**用 WSL 时必须知道的两件事：**

```bash
# 1) 不要用 wsl.exe -- bash -c '<脚本>' 传复杂脚本
#    wsl.exe 会用 WSL 登录环境预展开变量，脚本内定义的变量被吞成空，且退出码仍为 0
wsl.exe -d Ubuntu -- bash -c 'i=3; echo "$((i+1))"'   # → 1（错误数字，无报错）

# 正确：走 stdin
wsl.exe -d Ubuntu -- bash -s <<'EOF'
i=3; echo "$((i+1))"                                   # → 4
EOF

# 2) 命令先落盘再取退出码，别指望行内 echo
#    进度条的回车符经 wsl.exe 回传时会互相覆盖，echo $? 整行可能消失
wsl.exe -d Ubuntu -- bash -s <<'EOF'
npx vitest run > /tmp/t.log 2>&1; echo "EXIT=$?"; tail -6 /tmp/t.log
EOF
```

另外：**git worktree 在 WSL 里完全不可用**——`.git` 文件里存的是 `D:/...` 盘符路径，Linux 的 git 解析不了，直接 fatal。
