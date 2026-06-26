---
name: yys-wallpaper
description: 阴阳师原画壁纸下载工具。自动从 https://yys.163.com/media/picture.html 抓取壁纸，按分辨率下载到 ~/图片/{分辨率}/ 目录，跳过已存在的文件。触发条件：用户想要下载阴阳师壁纸、整理壁纸、批量下载图片。
---

# 阴阳师原画壁纸下载

## 使用方式

```bash
python3 skills/yys-wallpaper/scripts/download.py [分辨率] [选项]
```

### 参数说明

- `分辨率`：可选，默认 `1920x1080`
- `--batch-size`：每批下载数量，默认 50
- `--no-skip`：不跳过已存在的文件
- `--min-delay`：最小延迟(秒)，默认 0.3
- `--max-delay`：最大延迟(秒)，默认 1.0
- `-h, --help`：显示帮助信息

### 支持的分辨率

- `1366x768`
- `1440x900`
- `1920x1080`（默认）
- `2048x1536`
- `2208x1242`
- `2732x2048`
- `1080x2340`（手机壁纸）
- `2160x1620`

## 示例

```bash
# 下载1920x1080壁纸（默认）
python3 skills/yys-wallpaper/scripts/download.py

# 下载手机壁纸
python3 skills/yys-wallpaper/scripts/download.py 1080x2340

# 自定义批次大小和延迟
python3 skills/yys-wallpaper/scripts/download.py 1920x1080 --batch-size 20 --min-delay 0.5 --max-delay 2.0

# 强制重新下载所有图片
python3 skills/yys-wallpaper/scripts/download.py 1920x1080 --no-skip

# 下载所有分辨率
for res in 1366x768 1440x900 1920x1080 2048x1536 2208x1242 2732x2048 1080x2340 2160x1620; do
  python3 skills/yys-wallpaper/scripts/download.py $res
done
```

## 文件命名规则

URL 示例：`picture/20260311/1/1920x1080.jpg`
→ 文件名：`20260311_1_1920x1080.jpg`

## 保存路径

`~/Pictures/{分辨率}/`

例如：`~/Pictures/1920x1080/20260311_1_1920x1080.jpg`

## 跳过逻辑

本地已存在同名文件时跳过，不重复下载。

## 新功能特性

1. **智能跳过**：自动检测已下载文件，避免重复下载
2. **分批下载**：每批显示进度，便于监控
3. **进度显示**：实时显示下载进度和统计信息
4. **错误重试**：网络错误自动重试3次
5. **延迟控制**：可配置下载延迟，避免请求过快

## 注意事项

- 1920x1080 分辨率共约 1125 张图片（2.1GB）
- 1080x2340 分辨率共约 138 张图片（手机壁纸）
- 全部下载需要一定时间，建议分批下载
- 脚本使用 Python 标准库，无需额外依赖
- 下载大量图片时建议使用 `--min-delay 0.5 --max-delay 2.0` 避免被封IP

## 文件统计（参考）

| 分辨率 | 图片数量 | 估计大小 |
|--------|----------|----------|
| 1920x1080 | 1125张 | 2.1GB |
| 1080x2340 | 138张 | 约150MB |
| 其他分辨率 | 数量不等 | 按需下载 |
