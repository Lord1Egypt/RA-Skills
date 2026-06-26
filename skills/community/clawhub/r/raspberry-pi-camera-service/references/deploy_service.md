# 摄像头录制服务部署指南

## 安装系统依赖

```bash
sudo apt-get update
sudo apt-get install python3-venv python3-picamera2 ffmpeg -y
```

## 部署

### 配置变量
可修改 `scripts/deploy/install.sh` 脚本中的配置变量:

- SERVICE_NAME="camera-service"
- SERVICE_USER=$(id -un)
- SERVICE_GROUP=$(id -gn)
- WORKING_DIR="/opt/camera-service"
- PYTHON_CMD="python3"
- PORT=27793

### 执行部署脚本
```bash
sudo scripts/deploy/install.sh
```

## 卸载服务

```bash
sudo scripts/deploy/uninstall.sh
```

## 故障排查

### 服务无法启动

```bash
# 查看详细错误信息
sudo journalctl -u <SERVICE_NAME> -n 50 --no-pager

# 检查端口占用
sudo lsof -i :<PORT>

# 手动测试服务
```bash
/opt/<WORKING_DIR>/venv/bin/python -c "from service import app; print('OK')"
```

### 摄像头无法识别

```bash
# 检查 CSI 摄像头
libcamera-hello --list-cameras

# 检查 USB 摄像头
ls -la /dev/video*
v4l2-ctl --list-devices
```

### 权限问题

```bash
# 检查视频设备权限
ls -la /dev/video0

# 将用户加入 video 组
sudo usermod -a -G video pi

# 重新登录使权限生效
```

## 配置文件

环境配置文件位于 `$WORKING_DIR/.env`（部署时从模板生成），可修改以下参数：

```bash
HOST=0.0.0.0          # 服务监听地址
PORT=27793            # 服务端口
LOG_LEVEL=INFO        # 日志级别 (DEBUG/INFO/WARNING/ERROR)
OUTPUT_DIR=/opt/camera-service/output  # 视频输出目录
```

修改后需要重启服务生效：

```bash
sudo systemctl restart <SERVICE_NAME>
```

**注意**：也可使用 `systemctl edit <SERVICE_NAME>` 创建 override 配置。