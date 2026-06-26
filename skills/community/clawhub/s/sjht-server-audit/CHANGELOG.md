# Changelog — server-audit

所有格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [0.1.0] — 2026-03-19

### 新增
- 初始版本发布
- **服务器巡检脚本** `scripts/server-audit.sh`
  - 系统信息采集：OS、内核、CPU、内存、磁盘、Swap
  - 运行服务检测：systemd running services
  - 开放端口扫描：ss -tlnp 全部 TCP 监听
  - 防火墙状态检查：firewalld 规则、SELinux 模式
  - Web 服务检测：Nginx/PHP-FPM/MariaDB/Node/Docker 版本与状态
  - Nginx 虚拟主机配置提取（server_name/root/listen）
  - 网站目录扫描：WordPress 检测、HTML 站点检测
  - 安全配置审计：SSH 配置（密码认证/Root 登录/端口）
  - 可疑项检查：失败登录记录、用户/系统定时任务、高内存进程
  - 快速安全判定：自动识别 🔴严重/⚠️警告 级别问题

### 安全判定规则
- 🔴 严重：数据库端口全网暴露、管理面板全网暴露、SSH 允许 Root 密码登录
- ⚠️ 警告：防火墙未启用、SELinux 禁用、SSH 密码认证未禁用、无 Swap、暴力破解痕迹

### 首次验证
- 对 xxxxx（OpenCloudOS 9.4）完成完整巡检
- 检出 3 个严重安全问题
- 检出 4 个警告
- 生成详细巡检报告