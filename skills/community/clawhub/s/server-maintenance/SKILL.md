# Server Maintenance Skill

## 描述
自动化服务器维护工具。检查磁盘使用率、清理缓存、优化系统资源。支持多服务器批量操作。

## 触发词
- 服务器维护
- 清理磁盘
- 检查磁盘
- server maintenance
- disk cleanup

## 功能

### 1. 磁盘检查
- 检查磁盘使用率
- 识别大文件和目录
- 分析缓存占用

### 2. 自动清理
- npm 缓存清理
- Playwright 旧版本清理
- 临时文件清理

### 3. 系统优化
- Swap 使用检查
- 内存占用分析
- 进程资源监控

### 4. 多服务器支持
- 支持本地和远程服务器
- SSH 批量操作
- 统一报告输出

## 使用方法

### 单服务器检查
```bash
bash ~/.openclaw/skills/server-maintenance/check.sh
```

### 多服务器批量维护
```bash
bash ~/.openclaw/skills/server-maintenance/maintain-all.sh
```

### 定时任务
在 OpenClaw 中设置 cron：
```json
{
  "schedule": "0 2 * * 0",
  "task": "server-maintenance"
}
```

## 配置

服务器列表在 `servers.json`：
```json
{
  "servers": [
    {
      "name": "硅谷",
      "host": "localhost",
      "type": "local"
    },
    {
      "name": "中央",
      "host": "43.163.225.27",
      "type": "ssh"
    },
    {
      "name": "东京",
      "host": "43.167.192.145",
      "type": "ssh"
    }
  ]
}
```

## 输出示例

```
=== 服务器维护报告 ===
时间：2026-03-03 10:08

| 服务器 | 清理前 | 清理后 | 释放空间 |
|--------|--------|--------|----------|
| 硅谷   | 79%    | 69%    | 4.7GB    |
| 中央   | 88%    | 78%    | 5.0GB    |
| 东京   | 71%    | 63%    | 4.0GB    |

总计释放：13.7GB
```

## 安全措施
- 只清理已知安全的缓存目录
- 不删除用户数据
- 操作前自动备份关键配置
- 支持 dry-run 模式

## 依赖
- bash
- ssh（远程服务器）
- du, df（磁盘工具）
- npm（缓存清理）

## 版本
v1.0.0 - 2026-03-03
