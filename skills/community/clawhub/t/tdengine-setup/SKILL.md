---
name: tdengine-setup
description: 自动化安装和配置 TDengine 3.3.6.0。包含从官网下载、安装、启动服务以及基础数据库验证的完整流程。
metadata:
  {
    "openclaw": {
      "requires": {
        "bins": ["taos", "systemctl", "wget", "tar"]
      }
    }
  }
---

# TDengine 安装与配置技能

该技能用于在 Linux 环境下自动化部署 TDengine 时序数据库。

## 快速开始

```bash
# 运行安装脚本
sh ./scripts/install.sh
```

## 操作步骤详解

### 1. 下载安装包
从 TDengine 官方地址下载 3.3.6.0 Server 版：
- **地址**: `https://www.taosdata.com/assets-download/TDengine-server-3.3.6.0-Linux-x64.tar.gz`

### 2. 解压与安装
```bash
tar -xzvf TDengine-server-3.3.6.0-Linux-x64.tar.gz
cd TDengine-server-3.3.6.0
./install.sh
```
*注：安装过程中会提示输入安装路径和是否加入集群，通常按回车使用默认值即可。*

### 3. 启动服务
安装完成后，通过 systemd 管理服务：
```bash
systemctl start taosd
systemctl enable taosd
```

### 4. 基础验证
使用 `taos` 命令行工具验证：
```bash
taos -s "show databases"
```

## 必要文件说明
- `install.sh`: 官方安装脚本。
- `taosd`: 核心服务程序。
- `taos`: 命令行客户端。

## 故障排查
- 如果 `systemctl` 启动失败，请检查 `/var/log/taos/` 下的日志文件。
- 确保防火墙已开放 6030-6041 端口（默认端口）。
