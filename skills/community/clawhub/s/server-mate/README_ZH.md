[English](README.md) | 中文版

---

# Server-Mate | 轻量级服务器监控与 AI 运维

> 面向运行 Nginx 或 Apache 的 Linux 主机的双平面监控系统，并通过宝塔（BT-Panel）API 提供**轻量级集中式远程监控**——一台 Agent，纳管多台服务器，目标主机零安装。

[![Version](https://img.shields.io/badge/version-1.5.1-blue.svg)]()
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-success.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-CentOS%2FUbuntu%2FDebian-lightgrey.svg)](https://linux.org)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Web Server](https://img.shields.io/badge/Web%20Server-Nginx%2FApache-orange.svg)](https://nginx.org)

---

## 项目概览

**Server-Mate** 是一套面向 Linux Web 主机的轻量级服务器监控与 AI 运维工作流，适合运行 Nginx 或 Apache 的场景。

自 v1.5.x 起，Server-Mate 新增了**深度 Linux 系统指标采集**能力，覆盖四个层次：CPU 明细、内存/Swap、磁盘 IOPS、网络速率、进程统计、Inode 使用率、TCP 连接状态，以及 systemd 服务健康探测——全部通过 `psutil` 与标准库实现，**零新依赖**。同时完整保留 v1.4.x 的**中心化远程监控架构**：一台 Agent 通过宝塔 API 拉取多台服务器日志，目标主机零安装。

它将职责拆分为两个平面：
- **Server Agent**：运行在主机侧的 Python 采集器，负责本地日志增量读取（或通过宝塔 API 拉取远程日志）、主机指标采样与 SQLite 聚合落库
- **AI Analyzer**：运行在 OpenClaw 侧的聚合与解释层，负责报表生成、Webhook 推送、AI 诊断与受控自动化

### 核心特性

- **集中式远程采集**：通过宝塔 API 远程拉取多主机的 Nginx / Apache 日志，目标机器零安装、零依赖
- **实时指标采集**：通过 `psutil` 采集 CPU、内存、磁盘、负载、网络 I/O
- **扩展 Linux 指标 — Layer 1**：CPU user/system/iowait；可用内存；Swap 使用率；单周期磁盘 IOPS 增量；网络 Mbps；NIC 错误包/丢包计数
- **扩展 Linux 指标 — Layer 2**：进程总数、僵尸进程检测、Top-5 CPU/内存进程排行
- **扩展 Linux 指标 — Layer 3**：根目录 Inode 使用率；可配置额外分区监控（如 `/data`、`/home`）
- **扩展 Linux 指标 — Layer 4**：TCP 连接状态分布（ESTABLISHED / TIME_WAIT / CLOSE_WAIT）；systemd 服务健康探测
- **日志解析**：标准化 Nginx / Apache 的访问日志与错误日志
- **流量分析**：统计 PV、UV、IP 数、QPS、带宽、状态码分布
- **蜘蛛识别**：识别常见爬虫家族并与普通访客流量分离
- **智能告警**：支持钉钉、企业微信、飞书、Telegram 等 Webhook 通道
- **10 种新告警类型**：`iowait_high`、`swap_high`、`memory_critical`、`net_errors`、`high_iops`、`zombie_process`、`inode_low`、`disk_multi_low`、`tcp_timewait_high`、`service_down`
- **SSH 防暴破护盾**：增量解析认证日志，识别 SSH 爆破并可联动 auto-ban
- **AI 诊断**：将异常转换成自然语言解释与排查建议
- **自动报表**：生成日报、周报、月报 PDF，并附带 AI 点评
- **SSL 到期巡检**：在 PDF 概览和 Webhook 摘要中展示证书剩余天数
- **Guarded Automation**：提供带冷却期、白名单和审计日志的 auto-ban / auto-heal

### 使用场景

- 不替换现有栈的前提下，为 Linux 主机补上监控和日报能力
- 不再直接面对原始日志，而是通过 AI 获得清晰的异常解释
- 自动化生成日报、周报和月报，掌握流量、性能和安全趋势
- 识别可疑 IP、404 扫描、5xx 峰值和 SSH 暴破行为
- 以白名单、TTL 和审计留痕为前提，安全启用自动化干预

---

## v1.5.1 新增内容

### 告警触发后自动深度自查（Post-Alert Automatic Deep Diagnostics）

当硬件或系统服务触发告警时，Agent 会在本地（使用 subprocess）或远程（使用宝塔 API `exec_shell`）自动执行一套针对性诊断命令，直接将排查结果追加到 Webhook 推送的 Markdown 消息底部：
- **CPU / 内存 / Swap 告警**：自动列出 CPU 占用最高的前 8 个进程、系统负载（uptime）、内存使用分布（free -h），以及近期内核 OOM 事件日志（dmesg）。
- **磁盘 / Inode 告警**：自动列出磁盘分区占用（df -hT/df -i）、自动扫描大文件夹目录用量（du -sh），快速定位空间爆满元凶。
- **网络 / TCP 告警**：自动输出网卡统计（ip -s link）与 TCP 状态连接数汇总（ss -s）。
- **系统服务故障（service_down）**：自动抓取指定服务的状态（systemctl status）与最近 20 行运行日志（journalctl -u）。

### 告警自动恢复通知（Alert Recovery Notifications）

支持持久化追踪活动告警的状态，当监控指标恢复正常时自动向 Webhook 推送 ✅ 恢复通知：
- **持续时长统计**：精确计算并展示故障持续的分钟和秒数（例如 `持续时长: 约 2 分 34 秒`）。
- **峰值展示**：记录并报告告警发生期间指标达到的最高值（例如 CPU 达到的最高百分比）。
- **去抖动设计**：通过 `recovery_min_duration_seconds` 配置参数限制（默认 30 秒内自动恢复的瞬时波动不发恢复通知），避免服务器指标短暂瞬间越线带来无谓的推送打扰。

---

## v1.5.0 新增内容

### 深度 Linux 系统指标扩充 — 四层采集体系

所有新指标均通过 `psutil` 与 Python 标准库实现，**零新依赖**。

**Layer 1 — CPU 明细 / 内存与 Swap / 磁盘 IOPS / 网络速率**
- `cpu_user_pct`、`cpu_system_pct`、`cpu_iowait_pct`（来自 `cpu_times_percent()`）
- `memory_used_bytes`、`memory_available_bytes`、`swap_used_pct`、`swap_used_bytes`
- 单周期 IOPS 增量：`disk_read_iops`、`disk_write_iops`（ops/s）、`disk_read_bytes_delta`、`disk_write_bytes_delta`
- `net_rx_mbps`、`net_tx_mbps`、`net_rx_errs`、`net_tx_errs`、`net_rx_drop`、`net_tx_drop`

**Layer 2 — 进程统计**
- `process_count`、`process_running`、`process_sleeping`、`process_zombie`
- `top_cpu_procs` 和 `top_mem_procs`：按 CPU / 内存占用排列的前 5 进程

**Layer 3 — Inode 与额外分区**
- `disk_inode_used_pct`：通过 `os.statvfs()` 采集根挂载点 Inode 饱和度
- 可配置 `extra_disk_partitions` 列表：每个挂载点采集 `used_pct`、`free_bytes`、`inode_used_pct`

**Layer 4 — TCP 连接状态 / systemd 服务健康**
- `tcp_established`、`tcp_time_wait`、`tcp_close_wait`（来自 `psutil.net_connections(kind="tcp")`）
- 可配置 `service_probes` 列表：通过 `systemctl is-active` 探测每个服务，返回 `service_failed_units`

### 10 种新告警类型

| 告警类型 | 触发条件 |
|---|---|
| `iowait_high` | CPU iowait > `iowait_pct`（默认 30%） |
| `swap_high` | Swap 使用率 > `swap_pct`（默认 60%） |
| `memory_critical` | 可用内存 < `memory_min_available_mb`（默认 200 MB） |
| `net_errors` | NIC 错误包 + 丢包 > `net_error_count`（默认 100） |
| `high_iops` | 写 IOPS > `disk_write_iops`（默认 5 000/s） |
| `zombie_process` | 存在任意僵尸进程 |
| `inode_low` | Inode 使用率 > `inode_used_pct`（默认 90%） |
| `disk_multi_low` | 额外分区剩余比例 < `disk_free_ratio` |
| `tcp_timewait_high` | TIME_WAIT 连接数 > `tcp_timewait_count`（默认 5 000） |
| `service_down` | 任意 `service_probes` 服务状态为非 active |

### 零停机数据库迁移

- `migrate_schema()` 在 `init_database()` 启动时自动调用，通过 `PRAGMA table_info` 检查后，幂等地为 `metric_rollups` 表新增 11 列——**无需手动迁移，不丢失任何数据**。

### 向后兼容配置

- 4 个新 `system_metrics` 配置项（`collect_processes`、`collect_tcp_states`、`service_probes`、`extra_disk_partitions`）均具备默认安全值，**已有 `config.yaml` 无需改动**即可升级。
- 7 个新告警阈值（`iowait_pct`、`swap_pct`、`memory_min_available_mb`、`net_error_count`、`disk_write_iops`、`inode_used_pct`、`tcp_timewait_count`）均已内置合理默认值。

---

## v1.4.1 新增内容

### 宝塔 API 深度集成（Deep BT-Panel API Integration）

- **完整签名算法合规**：客户端现已完整实现宝塔标准签名算法——一种 HMAC 风格的 MD5 签名（HMAC-like MD5 Signature），即 `request_token = md5(str(request_time) + md5(api_key))`。**每次请求（包括重试）都会重新计算签名**，确保每次调用都携带新的 `request_time`，**绝不**复用过期 token
- **强制 POST + 表单参数合并**：严格遵循宝塔官方文档"统一使用 POST 方式请求"的要求，将鉴权字典与业务参数合并写入同一份 `application/x-www-form-urlencoded` 表单 body
- **Session 复用以应对高频采集**：每个面板实例化独立的 `requests.Session()`，自动复用 TCP/TLS 连接池并保持宝塔会话 Cookie。在「单面板多站点 + cron 高频拉取」场景下，握手开销被彻底消除
- **无感多站点扇出**：远程站点统一进入既有的 `sites[]` 矩阵，流量聚合、爬虫识别、AI 诊断、Webhook 路由、PDF 报表对远程主机零侵入复用。`panel_id` 留空则保持与 1.3.x 完全字节级兼容的本地 tail 行为

### 字节级流量与内存保护（Memory Safety: Byte-Level Throughput & Memory Protection）

- **字节偏移截断（Byte-offset chunking）**：远程读取通过宝塔 `ExecShell` 接口下发 `tail -c +<offset> | head -c <chunk>` 命令实现，**整文件 body 绝不传输**
- **5 MB 单次拉取上限**：每个 cron 周期单次拉取上限为 `chunk_bytes`（默认 5 242 880 字节）。即便远程 `error_log` 因上游异常瞬间暴涨数百 MB，Agent 内存占用始终**保持恒定**，HTTP 超时与 OOM 被分类阻断，剩余字节自动顺延到后续 cron 周期继续追读
- **纵深防御边界**：5 MB 上限**同时**在 Python 调用层做 clamp、并烤进远端 shell 管道本身（`head -c 5242880`），即便面板侧响应异常，内核也会在 5 MB 字节处主动断开管道
- **积压可见化**：远程游标持久化 `backlog_bytes` 字段（`status="backlog"`），并在站点落后于实时进度时主动输出 WARNING 日志，杜绝「静默漏采」

### 安全加固（Security Hardening）

- **命令注入防御（Command Injection Prevention）**：所有来自配置文件的远端 Shell 路径在拼入 `ExecShell` 命令前，必须经过 `shlex.quote` 严格转义 + 控制字符（NUL / CR / LF）拒绝双层校验。即使配置中混入恶意 payload（例如 `"/path; rm -rf /"`），最终也只能以单引号字面量形式存在于 shell 中，**绝不会被解析为独立命令**
- **NTP 漂移自动识别（NTP Drift Auto-Detection）**：宝塔签名失败往往以 HTTP 200 + `{"status": false, "msg": "request_token error"}` 的形式返回，而非 401/403，极易误导排查方向。客户端现已识别中英文双语的鉴权失败关键字，并在异常 message 与 WARNING 日志中**同时**附加精准的修复指引——*"Authentication failed. Please check if the time on the Agent server and the Remote BT panel are synchronized (NTP Time Drift)."*
- **站点级故障隔离**：任意单个远程面板的失败均会被捕获、记录、并写入游标的 `status` 字段，**绝不**会让一台远程不稳定导致 cron 周期崩溃，也不会饿死其他配置站点

---

## v1.3.2 新增内容

### SSH 防暴破护盾

- **认证日志解析**：增量解析 `logs.auth_log`，若为空则自动探测 `/var/log/auth.log` 或 `/var/log/secure`，识别 `Failed password` 指纹
- **联动自动封禁**：连续 SSH 失败可触发 `ssh_brute_force` 告警，并进入现有的白名单感知 auto-ban 流程

### SSL 证书到期巡检

- **证书检查**：在报表生成阶段，使用 Python `ssl` 与 `socket` 巡检每个已配置站点的证书有效期
- **全链路透出**：剩余天数会显示在 PDF 概览区与 Webhook Markdown 摘要中，小于 15 天时附带警示标记

### PDF 长文本防溢出

- **URL / Referer 截断**：在表格渲染前先移除查询参数，再对超长文本做硬截断
- **版式稳定**：极长 Token 或恶意扫描路径不再撑爆高密度 PDF 页面

### Telegram 推送

- **新增通道**：Webhook 中心已支持 Telegram Bot 推送
- **环境变量回退**：当配置中留空时，会回退读取 `TELEGRAM_BOT_TOKEN` 与 `TELEGRAM_CHAT_ID`

### GeoIP 开箱即用

- **自动补全依赖**：若缺少 GeoLite2 `.mmdb` 数据库，报表生成器会自动从公共镜像下载，实现零配置地理位置解析
- **优先使用 MaxMind**：若存在 `./data/GeoIP.conf` 且系统已安装 `geoipupdate`，则会优先用你的 MaxMind 账号刷新数据库，失败后再回退公共镜像

### AI 告警实时诊断

- **发送前 AI 复核**：`warning` / `critical` 告警在推送前可先调用共享 AI 接口做解释
- **两句话输出**：告警卡片可追加紧凑的 `AI 智能诊断` 模块，用大白话说明原因和下一步建议

### systemd 模板

- **`--generate-service`**：Agent 可直接输出一份与当前本地路径匹配的 systemd unit 模板，便于宿主机守护部署

### 多站点监控

- **矩阵配置**：通过 `sites[]` 同时监控同机多个域名
- **全局系统指标**：新增 `system_metrics`，专门采集 CPU、内存、磁盘、网络等宿主机级指标
- **作用域隔离**：使用 `__host__` 将主机级资源指标与站点级业务流量拆开

### 加固日志读取

- **兼容 logrotate**：能处理 inode 变化、文件截断、文件短暂缺失等情况
- **稳健状态跟踪**：Agent 重启后仍可延续增量读取状态

### 受控自动化

- **Dry-Run 模式**：默认先试运行，先观察通知和审计再决定是否执行真实动作
- **白名单感知 auto-ban**：保护受信 IP 和已知搜索引擎蜘蛛
- **TTL 自动解封**：封禁到期后自动释放，避免规则无限堆积
- **冷却保护**：每条自动化策略都带冷却期，防止动作风暴
- **强制通知**：所有自动化动作都会记录并推送通知

### SQLite 审计跟踪

- **`automation_actions` 表**：记录自动化事件的完整审计轨迹
- **`banned_ips` 表**：记录当前有效封禁、TTL 和元数据

### 配置模板

- **`config.example.yaml`**：推荐从该文件开始，内置多站点、Telegram、SSH 认证日志、SSL 巡检、AI 诊断和 Guarded Automation 的示例配置

---

## 快速开始

### 1. 安装

```bash
# 克隆仓库
git clone https://github.com/tankeito/server-mate.git
cd server-mate

# 安装基础依赖
python3 -m pip install psutil pyyaml matplotlib requests

# 可选：启用 GeoIP 能力
python3 -m pip install geoip2 maxminddb aiohttp

# 可选：安装官方 MaxMind 更新器
# CentOS / Rocky / AlmaLinux: sudo yum install geoipupdate
# Ubuntu / Debian: sudo apt-get install geoipupdate
```

### 2. 配置

建议先从 [`config.example.yaml`](config.example.yaml) 复制生成 `config.yaml`。

在 OpenClaw 环境中，请将 `config.yaml`、`metrics.db`、`logs/` 和 `reports/` 都保留在当前工作区，也就是 `./` 下面，不要写入系统全局目录。

如果启用 AI 功能，OpenClaw 会自动注入 `OPENAI_API_KEY`，因此不需要再手动执行 `export OPENAI_API_KEY=...`。

```yaml
agent:
  host_id: web-01
  timezone: Asia/Shanghai
  mode: once

system_metrics:
  enabled: true

logs:
  auth_log: ""

sites:
  - domain: site-a.example.com
    site_host: site-a.example.com
    enabled: true
    access_log: ./logs/site-a.access.log
    error_log: ./logs/site-a.error.log
  - domain: site-b.example.com
    site_host: site-b.example.com
    enabled: true
    access_log: ./logs/site-b.access.log
    error_log: ./logs/site-b.error.log

storage:
  database_file: ./metrics.db
  rollup_minutes: [10, 60]

notifications:
  webhooks:
    dingtalk:
      enabled: true
      url: https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN
    telegram:
      enabled: false
      bot_token: ""
      chat_id: ""
  reports:
    report_language: zh
    report_export_dir: ""
    public_base_url: ""
    geoip_city_db: ./data/GeoLite2-City.mmdb
    geoip_update_config: ./data/GeoIP.conf
    ai_analysis:
      enabled: true
      simulate: false
      api_key_env: OPENAI_API_KEY
    daily:
      enabled: true
      push_time: "08:30"
      channels: [dingtalk]
      output_dir: ./reports

automation:
  dry_run: true
  auto_ban:
    enabled: false
  auto_heal:
    enabled: false
```

### 2.1 GeoIP 说明

- 将你的 MaxMind 配置文件放在 `./data/GeoIP.conf`
- 请手动创建 `./data/GeoIP.conf`，真实文件不要提交到 Git
- 若希望报表中展示真实地区，请安装 `geoip2` 及其依赖，例如 `maxminddb`、`aiohttp`
- 免费 GeoLite2 账号注册地址：[MaxMind GeoLite 注册](https://www.maxmind.com/en/geolite2/signup)
- License Key 生成说明：[Generate a License Key](https://support.maxmind.com/hc/en-us/articles/4407111582235-Generate-a-License-Key)
- `geoip_update_config` 是可选项，但推荐本地统一使用 `./data/GeoIP.conf`
- 若你暂时不使用 MaxMind，Server-Mate 仍会回退到公共 `.mmdb` 镜像
- 如果 License Key 曾明文泄露，请在正式环境前先旋转密钥

### 3. 手动运行 Agent

```bash
# 单次采集
python3 scripts/server_agent.py --config config.yaml --once

# 查看已聚合的数据
python3 scripts/report_generator.py --config config.yaml daily --date 2026-03-26 --json
```

### 4. 使用 Cron 定时调度

```bash
crontab -e
```

加入以下任务：

```cron
# 每 10 分钟采集一次
*/10 * * * * /usr/bin/env bash -lc 'python3 ./scripts/server_agent.py --config ./config.yaml --once >> ./logs/server-mate-agent.log 2>&1'

# 每天 01:00 生成日报 PDF 并推送
0 1 * * * /usr/bin/env bash -lc 'python3 ./scripts/report_generator.py --config ./config.yaml pdf --range daily --send >> ./logs/server-mate-report.log 2>&1'

# 每周一 01:10 生成周报 PDF 并推送
10 1 * * 1 /usr/bin/env bash -lc 'python3 ./scripts/report_generator.py --config ./config.yaml pdf --range weekly --send >> ./logs/server-mate-report.log 2>&1'

# 每月 1 日 01:20 生成月报 PDF 并推送
20 1 1 * * /usr/bin/env bash -lc 'python3 ./scripts/report_generator.py --config ./config.yaml pdf --range monthly --send >> ./logs/server-mate-report.log 2>&1'
```

---

## 架构设计

### 双平面设计

```text
+--------------------------------------------------------------+
| Server Agent (Linux Host)                                    |
| - psutil 指标采样（CPU / 内存 / 磁盘 / 网络）                |
| - 日志增量读取（Nginx / Apache access + error）              |
| - JSON 事件输出                                              |
| - SQLite 聚合落库                                            |
+--------------------------------------------------------------+
                            |
                            | SQLite / JSON events
                            v
+--------------------------------------------------------------+
| AI Analyzer (OpenClaw)                                       |
| - 聚合与存储                                                 |
| - 自然语言问答                                               |
| - AI 异常诊断                                                |
| - Webhook 推送（钉钉 / 企微 / 飞书 / Telegram）             |
| - Guarded auto-ban / auto-heal                               |
| - PDF 报表生成（日 / 周 / 月）                               |
+--------------------------------------------------------------+
```

### 组件流转

1. **Agent 采集**：产生 `system_snapshot`、`access_event`、`error_event`
2. **SQLite 聚合**：写入 10 分钟和 60 分钟粒度的 rollup 桶
3. **报表生成器**：读取聚合数据并生成 PDF / Markdown
4. **Webhook 中心**：推送告警和报表摘要
5. **AI 分析**：可选调用大模型，生成异常解释与优化建议

---

## 数据契约

### 核心事件类型

| 事件类型 | 用途 | 关键字段 |
|----------|------|----------|
| `system_snapshot` | 主机健康指标 | `cpu_pct`, `memory_pct`, `disk_free_bytes`, `load_1m` |
| `access_event` | 访问日志解析结果 | `client_ip`, `uri`, `status`, `response_ms`, `user_agent` |
| `error_event` | 错误日志解析结果 | `severity`, `component`, `category`, `fingerprint`, `message` |
| `action_event` | 自动化审计记录 | `action`, `target`, `reason`, `dry_run`, `result`, `ttl_seconds` |

### 指标定义

| 指标 | 说明 |
|------|------|
| **PV** | 统计窗口内的总请求数 |
| **UV** | 唯一访客键，优先使用 IP + UA 组合 |
| **IP 数** | 独立客户端 IP 数量 |
| **QPS** | `request_count / window_seconds` |
| **慢请求** | `response_ms > threshold`，默认阈值为 2000ms |
| **出站带宽** | 响应字节数总和 |

---

## 配置参考

### `agent` 部分

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `host_id` | string | - | 告警与报表使用的逻辑主机名 |
| `timezone` | string | `UTC` | 本地时区，用于时间桶划分 |
| `mode` | string | `once` | `once` 或 `daemon` |
| `poll_interval_seconds` | int | `60` | 守护模式下的轮询间隔 |
| `state_file` | string | `./server_agent_state.json` | 增量读取游标状态文件 |

### `system_metrics` 部分

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enabled` | boolean | `true` | 是否采集宿主机全局指标 |
| `disk_root` | string | `/` | 磁盘容量检查的挂载点 |
| `collect_network_io` | boolean | `true` | 是否采集网络 I/O |

### `logs` 部分

| 字段 | 类型 | 说明 |
|------|------|------|
| `auth_log` | string | SSH 认证日志路径；留空时自动探测系统默认位置 |

### `sites` 部分

| 字段 | 类型 | 说明 |
|------|------|------|
| `domain` | string | 站点域名，用于报表命名与 SSL 巡检 |
| `site_host` | string | 站点展示名称，可与域名一致 |
| `enabled` | boolean | 是否启用该站点监控 |
| `access_log` | string | 访问日志路径。未设置 `panel_id` 时为本地路径；设置 `panel_id` 后必须填写**远端主机上的绝对路径** |
| `error_log` | string | 错误日志路径，语义同 `access_log` |
| `panel_id` | string | *可选。* 将该站点绑定到 `remote_panels` 中定义的远程宝塔面板。**留空（或省略）则走原有 `LocalLogReader` 读取本地日志**；设置后改由 `BTRemoteLogReader` 通过该面板远程拉取 |

### `remote_panels` 部分 *（v1.4.x 新增）*

顶层映射表，键为 `panel_id`，值为一份宝塔面板连接配置。`sites[]` 通过 `panel_id` 字段引用对应面板，从而启用零侵入远程日志采集。

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `<panel_id>` | string（键名） | - | 逻辑标识，被 `sites[].panel_id` 引用 |
| `url` | string | - | 宝塔面板基础 URL，需带端口，例如 `https://panel-hk.example.com:8888` |
| `api_key` | string | `""` | 宝塔**接口密钥**。明文写法仅作兜底，强烈建议改用 `api_key_env` |
| `api_key_env` | string | `""` | 运行时从该环境变量读取 api_key，**优先级高于** `api_key` 明文 |
| `timeout_seconds` | int | `15` | 单次 HTTP 请求超时 |
| `retries` | int | `2` | 仅对传输层临时错误生效；鉴权失败永不重试 |
| `chunk_bytes` | int | `5242880` | 单次 ExecShell 拉取与单个 cron 周期的字节上限，默认 5 MB |
| `verify_tls` | boolean | `true` | TLS 证书校验开关，仅自签证书场景下可设为 `false` |

示例：

```yaml
remote_panels:
  bt-prod-hk:
    url: https://panel-hk.example.com:8888
    api_key_env: BT_PANEL_HK_API_KEY     # 推荐写法
    timeout_seconds: 15
    retries: 2

sites:
  - domain: site-local.example.com
    enabled: true
    access_log: ./logs/site-local.access.log     # 本地站点，无需 panel_id
    error_log: ./logs/site-local.error.log
  - domain: site-remote.example.com
    enabled: true
    panel_id: bt-prod-hk                         # 远程站点，绑定面板
    access_log: /www/wwwlogs/site-remote.example.com.log
    error_log: /www/wwwlogs/site-remote.example.com.error.log
```

> ⚠️ **安全警告** — 宝塔面板的 `api_key` 拥有该面板纳管所有主机的最高权限，等同于 root。**请务必不要将含有 `api_key` 明文的 `config.yaml` 提交到任何版本控制系统（包括私有仓库）。** 推荐工作流：
>
> 1. 将 `config.yaml` 加入 `.gitignore`（项目默认已配置）。
> 2. 通过 `api_key_env` 注入密钥，并在 `/etc/server-mate/env`、systemd 的 `EnvironmentFile=`、或企业密钥管理系统中维护实际值。
> 3. 一旦发现密钥曾被误提交（即使是私有仓库或已强制推送删除），立即在宝塔面板侧轮换 / 撤销该密钥，**不要依赖 `git rm` 或重写历史**。

### `storage` 部分

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `database_file` | string | `./metrics.db` | SQLite 数据库路径 |
| `rollup_minutes` | array | `[10, 60]` | 聚合桶粒度 |

### `notifications.webhooks` 部分

| 通道 | 字段 |
|------|------|
| `dingtalk` | `enabled`, `url`, `timeout_seconds`, `at_all` |
| `wecom` | `enabled`, `url`, `timeout_seconds` |
| `feishu` | `enabled`, `url`, `timeout_seconds` |
| `telegram` | `enabled`, `bot_token`, `chat_id`, `timeout_seconds` |

### `notifications.reports` 部分

| 字段 | 类型 | 说明 |
|------|------|------|
| `report_language` | string | `zh` 或 `en` |
| `report_export_dir` | string | 对外暴露的 PDF 导出目录 |
| `public_base_url` | string | 下载链接的 URL 前缀 |
| `geoip_city_db` | string | GeoLite2 城市库路径 |
| `geoip_update_config` | string | MaxMind 更新配置路径 |
| `daily.enabled` | boolean | 是否启用日报 |
| `daily.push_time` | string | `"08:30"` 格式 |
| `weekly.push_weekday` | int | `1-7`，其中 `1` 表示周一 |
| `monthly.push_day` | int | `1-28` |

### `automation` 部分

| 字段 | 类型 | 说明 |
|------|------|------|
| `dry_run` | boolean | 试运行开关；`true` 时只通知不执行 |
| `auto_ban.enabled` | boolean | 是否启用自动封禁 |
| `auto_ban.whitelist_ips` | array | IP 白名单 |
| `auto_ban.ban_ttl_seconds` | int | 自动解封 TTL |
| `auto_heal.enabled` | boolean | 是否启用自动自愈 |
| `auto_heal.cooldown_seconds` | int | 自动重启冷却时间 |

---

## 报表类型

### 日报

**生成时机**：每天在配置的 `push_time` 生成

**内容包含**：
- 前 24 小时的 PV、UV、IP 汇总
- 带浏览量(PV) / 访问数(UV) 的热门页面、带地区的热门 IP、热门来源
- 蜘蛛流量分布
- 状态码分布（2xx / 3xx / 4xx / 5xx）
- Top 错误和慢响应端点
- AI 健康点评（若已启用）

### 周报

**生成时机**：每周一在配置时间生成

**内容包含**：
- 7 天流量趋势
- 被拦截 IP 趋势
- 爬虫抓取模式
- 可疑路由聚类
- 重复错误指纹
- AI 周度摘要

### 月报

**生成时机**：每月 1 日生成

**内容包含**：
- 30 天流量与性能趋势
- 磁盘增长分析
- 带宽峰值检测
- 容量预警
- 处置总结
- AI 月度回顾

---

## 告警阈值

| 告警类型 | 默认阈值 | 窗口 |
|----------|----------|------|
| CPU 过高 | `> 85%` | 连续 5 分钟 |
| 内存过高 | `> 85%` | 连续 5 分钟 |
| 磁盘剩余过低 | `< 10%` 可用空间 | 即时 |
| 5xx 突增 | `> 20` 次错误 | 1 分钟 |
| 可疑 IP | `> 200` RPM | 1 分钟 |
| 404 扫描突增 | 短时间显著突增 | 短窗口 |
| 慢路由 | 平均 `> 2000ms` | 告警窗口 |

---

## 安全与自动化

### Auto-Ban 策略（可选启用）

**要求**：
- 必须配置受信 IP 白名单
- 必须有明确的滥用证据，而不是正常流量暴涨
- 必须有冷却时间和每小时动作上限
- 必须有 TTL，例如 24 小时后自动解封
- 必须记录精确执行命令与结果

**适合的触发对象**：
- 单个 IP 持续超速请求
- 扫描器式 UA 与 404 喷洒行为
- 对后台管理路径的暴力尝试

### Auto-Heal 策略（保守启用）

**要求**：
- 必须有重复 `502` 或上游故障证据
- 最好伴随健康检查失败或其他二次信号
- 每个冷却窗口内只允许一次重启尝试
- 必须执行动作后的回查验证
- 重启失败时必须升级为人工介入

**推荐流程**：
1. 先告警
2. 输出 dry-run 建议
3. 对明确异常的服务执行一次受控重启
4. 回查错误率与健康状态
5. 若仍异常，则升级处理而不是死循环重启

---

## 项目结构

```text
server-mate/
├── SKILL.md                    # Skill 定义与触发规则
├── README.md                   # 英文说明
├── README_ZH.md                # 中文说明
├── user-guide.md               # 详细部署指南
├── config.example.yaml         # 完整配置模板
├── agents/
│   └── openai.yaml             # OpenAI agent 接口配置
├── references/
│   ├── architecture.md         # 架构设计与边界说明
│   ├── data-contracts.md       # 事件模型与指标定义
│   ├── ops-playbook.md         # 阈值、告警与自动化策略
│   └── sqlite-schema.md        # 数据库结构与查询模式
├── scripts/
│   ├── server_agent.py         # 主采集器
│   ├── report_generator.py     # PDF / Markdown 报表生成器
│   └── webhook_center.py       # Webhook 推送服务
└── config.yaml                 # 运行时配置文件（按需生成）
```

---

## 故障排查

### PDF 中中文显示为方块

**解决方法**：

```bash
# CentOS / Rocky / AlmaLinux
sudo yum install google-noto-sans-cjk-ttc-fonts

# Ubuntu / Debian
sudo apt-get update
sudo apt-get install fonts-noto-cjk

# 刷新字体缓存
fc-cache -fv
```

### Webhook 消息只显示本地路径

**解决方法**：
1. 在配置中设置 `report_export_dir`
2. 在配置中设置 `public_base_url`
3. 通过 Nginx 或 Apache 暴露导出目录

### 报表没有数据

**解决方法**：
1. 检查 `database_file` 是否正确
2. 确认 Agent 是否已经写入 rollup 数据
3. 确认配置中的站点标识与数据库中的数据作用域一致

### 慢响应路由或异常 IP 板块为空

**解决方法**：
- 确认当前 Agent 版本已经创建 `slow_request_rollups` 和 `suspicious_ip_rollups` 表

---

## 技术支持

- **GitHub Issues**: https://github.com/tankeito/server-mate/issues
- **Repository**: https://github.com/tankeito/server-mate
- **Email**: tqd354@gmail.com

---

**Server-Mate** | 轻量级服务器监控与 AI 运维

**Developed by tankeito** | MIT License | 2026
