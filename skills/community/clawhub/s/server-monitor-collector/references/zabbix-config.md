# Zabbix 配置

## 环境变量

```bash
ZABBIX_URL=http://zabbix.example.com/api_jsonrpc.php
ZABBIX_USER=Admin
ZABBIX_PASSWORD=your_password
# 可选：API Token（优先级高于用户名密码）
ZABBIX_TOKEN=optional_api_token
# TOPN: 所有主机按内存+CPU综合降序取前N台，0=关闭（默认50）
TOPN=50
```

## Zabbix API 认证方式

### 方式一：用户名 + 密码（默认）
```python
auth = api_call("user.login", {
    "user": ZABBIX_USER,
    "password": ZABBIX_PASSWORD,
})
```

### 方式二：API Token（更安全）
在 Zabbix Web UI 生成后填入 `.env`，脚本自动优先使用：
```python
auth = os.environ.get("ZABBIX_TOKEN")  # 有值则跳过 login
```

## 核心采集指标

| 指标 Key | 说明 |
|----------|------|
| `vm.memory.size[available]` | 内存可用字节 |
| `vm.memory.size[total]` | 内存总量字节 |
| `vm.memory.size[pavailable]` | 内存可用百分比 |
| `system.cpu.util` | CPU 利用率（所有核心平均） |
| `vfs.fs.size[/,pused]` | 根分区磁盘使用率 |

## 主机组排除规则

以下名称的主机组默认排除（可在脚本中修改 `EXCLUDE_GROUPS`）：

- `Templates*`（所有以 Templates 开头的主机组）
- `Discovered hosts`（Zabbix 自动发现的主机）

## 字段说明

- **内存占用率(%)**：`(mem_total - mem_avail) / mem_total * 100`
- **输出路径**：`~/.hermes/cron/output/zabbix_monitor.csv` 和 `.xlsx`
- **编码**：CSV 为 UTF-8-BOM，Windows Excel 打开不乱码

## 无 Agent 时

内存指标依赖 Zabbix Agent。若主机无 Agent：
- `mem_total` 和 `mem_avail` 均返回空
- 内存占用率显示 `N/A`
