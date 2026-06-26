# Workflow Notes

Use this sheet to keep longer-form explanations out of SKILL.md.

## Workflow Skeleton
1. 接单 → 判断需求（导航 / 交互 / 取证 / 下载）。
2. 连接 Desktop 节点（`tools.exec.node="Desktop"`）。
3. 运行相应脚本：
   - 启动/聚焦 Edge → `launch_edge.ps1` + `focus_edge.ps1`
   - 导航 or JS 注入 → `edge_nav.ps1`（暂先通过 URL 导航）
   - 取证 → `capture_screenshot.ps1`
   - 打包下载 → `download_and_zip.ps1`
4. 回传证据（文件、日志、stdout）。

## Command Snippets
```powershell
# 切换到 Desktop 节点后执行脚本
tools.exec node=Desktop command="powershell -File scripts/windows-browser-ops/launch_edge.ps1 -Url 'https://example.com'"
```

## References
- 详尽脚本说明/疑难杂症：`references/edge_playbook.md`
