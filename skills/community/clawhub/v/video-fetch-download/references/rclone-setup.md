# rclone 115网盘配置指南

## 首次授权

运行登录脚本，用 115 App 扫码（TV模式）：

```bash
python3 scripts/115_qrlogin.py
```

扫码后凭证自动写入 rclone config，remote 名称为 `115drive`。

**TV模式说明：** 不占用手机/网页的登录名额，不会挤掉其他端，长期稳定。

## 验证连接

```bash
rclone lsd 115drive:        # 列出根目录
rclone lsd 115drive:云下载  # 列出云下载目录
```

## 重新授权

Cookie 失效时（通常数月后），重新运行：

```bash
python3 scripts/115_qrlogin.py
```

## 自定义上传目录

```bash
# 上传到指定目录
export VIDEOFETCH_REMOTE="115drive:我的影片"

# 或在命令行指定
bash scripts/video_fetch.sh <url> 115drive:电影
```

## rclone 115改版说明

标准 rclone 不支持115网盘，本 skill 使用 [gaoyb7/rclone-release](https://github.com/gaoyb7/rclone-release) 改版。
install.sh 会自动安装正确版本。

## 115网盘限制

- 最多同时下载 5 个文件（`--transfers=5`）
- 单文件最多 2 线程（`--multi-thread-streams=2`）
- 离线下载任务由115服务器执行，本机无需下载
