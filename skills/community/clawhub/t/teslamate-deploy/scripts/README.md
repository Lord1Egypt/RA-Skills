# TeslaMate 部署系统

## 概述

TeslaMate 是一个开源的 Tesla 车辆数据记录和可视化工具。本项目提供模块化的部署解决方案，支持本地和远程部署。

## 新的脚本架构

### 分离的脚本设计
- **`install-teslamate.sh`** - 本地安装脚本
- **`deploy-setup.sh`** - 远程部署脚本

### 设计理念
- **职责分离**: 安装和部署逻辑完全分离
- **代码复用**: 远程部署重用本地安装脚本
- **简化维护**: 每个脚本专注于单一职责

## 快速开始

### 简化使用（推荐）

使用 `deploy-setup.sh` 脚本，根据参数自动选择部署方式：

```bash
cd /Users/martinzhang/git/teslamate/mytesla/deploy

# 本地安装（无参数）
./deploy-setup.sh

# 远程部署（指定服务器IP）
./deploy-setup.sh <服务器IP>

# 示例：
./deploy-setup.sh                    # 本地安装
./deploy-setup.sh 192.0.2.1     # 远程部署
```

### 高级使用

如需更多控制选项，可以直接使用安装脚本：

```bash
# 智能安装（自动检测并安装Docker）
./install-teslamate.sh

# 强制重新安装Docker环境（仅限Ubuntu/Debian）
./install-teslamate.sh --install-docker
```

**本地安装执行流程：**
1. 检查/安装 Docker 环境
2. 在当前目录创建必要文件和环境
3. 拉取 Docker 镜像
4. 启动 TeslaMate 服务
5. 显示安装结果

**远程部署执行流程：**
1. 传输配置文件到远程服务器
2. 传输安装脚本到远程服务器
3. 在远程服务器上执行安装脚本
4. 显示部署结果

## 部署架构

### 服务组件
- **TeslaMate**: 主应用服务（端口 4000）
- **PostgreSQL 16**: 数据库服务
- **Grafana**: 数据可视化（端口 3000）
- **Mosquitto**: MQTT 消息代理（端口 1883）

### 镜像来源
所有镜像直接从镜像源拉取：
- `teslamate/teslamate:latest` - TeslaMate 主应用
- `postgres:16` - PostgreSQL 数据库
- `teslamate/grafana:latest` - 定制版 Grafana
- `eclipse-mosquitto:2` - MQTT 消息代理

## 访问地址

部署完成后可通过以下地址访问：

### 本地部署
- **TeslaMate**: http://localhost:4000
- **Grafana**: http://localhost:3000

### 远程部署
- **TeslaMate**: http://<服务器IP>:4000
- **Grafana**: http://<服务器IP>:3000

**Grafana 默认账号**: admin/admin

## 故障排除

### 常见问题
1. **权限错误**: 确保使用 `sudo` 执行 Docker 相关操作
2. **网络问题**: 检查服务器能否访问 Docker Hub
3. **端口冲突**: 确保 3000、4000、1883 端口未被占用

### 网络超时处理
如果遇到镜像拉取超时：
```bash
# 重启 Docker 服务刷新网络连接
sudo systemctl restart docker

# 单独拉取镜像测试
sudo docker pull postgres:16
```

### 日志查看
```bash
# 查看服务状态
docker compose ps

# 查看服务日志
docker compose logs

# 查看特定服务日志
docker compose logs teslamate

# 实时查看日志
docker compose logs -f
```

## 文件说明

- `deploy-setup.sh` - 远程一键部署脚本（主要使用）
- `deploy-local.py` - 简化部署脚本（适合已有 Docker 环境的服务器）
- `docker-compose.yml` - Docker Compose 配置文件

## 注意事项

- 部署脚本需要 sudo 权限执行 Docker 相关操作
- 目录创建和文件传输使用普通用户权限
- 腾讯云镜像加速器已配置，会自动使用国内镜像源
