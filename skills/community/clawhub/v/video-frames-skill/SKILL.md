# Video Frame Extractor - Skill 文档

基于 PyAV 的命令行视频帧提取工具，支持单帧、批量、采样提取及视频信息查看。

## 📋 功能特性

- ✅ 单帧提取（按帧号或时间点）
- ✅ 批量提取多帧
- ✅ 按时间间隔采样提取
- ✅ 批量目录首帧提取
- ✅ 视频信息查看
- ✅ 视频压缩（H.264 重新编码）
- ✅ 图片压缩转换为 WebP 格式
- ✅ 多线程加速
- ✅ 递归目录处理
- ✅ 跨平台支持（Windows/macOS/Linux）

## 🚀 安装

### 自动安装（推荐）

```bash
# 使用安装脚本一键安装
curl -sSL https://raw.githubusercontent.com/indulgeback/video-frame-extractor/main/install.sh | bash
```

脚本会自动：
- 下载仓库到 `~/.video-frame-extractor`
- 创建 Python 虚拟环境
- 安装所有依赖（PyAV、tqdm、Pillow）
- 创建可执行命令 `frame-extractor`

### 手动安装

```bash
# 克隆仓库
git clone https://github.com/indulgeback/video-frame-extractor.git ~/.video-frame-extractor

# 进入目录
cd ~/.video-frame-extractor

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 创建可执行链接
ln -sf ~/.video-frame-extractor/frame-extractor.py ~/.local/bin/frame-extractor
```

### 配置 PATH

确保 `~/.local/bin` 在你的 PATH 中：

```bash
# 添加到 ~/.zshrc（macOS/Linux）
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 验证安装

```bash
frame-extractor -v
```

如果显示版本信息，说明安装成功！

## 🔧 诊断和错误排除

### 常见问题

#### 1. 命令找不到

**症状：**
```bash
frame-extractor: command not found
```

**解决方案：**
```bash
# 检查 PATH
echo $PATH | grep -o '[^:]*\.local/bin[^:]*'

# 如果没有输出，添加到 PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### 2. 权限错误

**症状：**
```bash
Permission denied: '/Users/xxx/.local/bin/frame-extractor'
```

**解决方案：**
```bash
chmod +x ~/.local/bin/frame-extractor
```

#### 3. Python 模块导入错误

**症状：**
```bash
ModuleNotFoundError: No module named 'av'
```

**解决方案：**
```bash
# 重新安装依赖
cd ~/.video-frame-extractor
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. FFmpeg 相关错误

**症状：**
```bash
RuntimeError: Could not find libavformat
```

**解决方案：**

PyAV 内置了 FFmpeg，但如果有问题：

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# 验证 FFmpeg
ffmpeg -version
```

#### 5. 虚拟环境问题

**症状：**
```bash
/bin/sh: venv/bin/python: No such file or directory
```

**解决方案：**
```bash
cd ~/.video-frame-extractor
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 运行诊断脚本

```bash
bash ~/.openclaw/skills/video-frames/scripts/diagnose.sh
```

诊断脚本会检查：
- Python 版本
- frame-extractor 命令是否存在
- PATH 配置
- 依赖安装情况
- FFmpeg 可用性

## 📖 使用指南

### 1. 查看版本信息

```bash
frame-extractor -v
```

### 2. 提取单帧

#### 按帧号提取

```bash
# 提取第 100 帧
frame-extractor single -i video.mp4 -f 100 -o frame100.jpg

# 指定 JPEG 质量
frame-extractor single -i video.mp4 -f 100 -o frame100.jpg --quality 90
```

#### 按时间点提取

```bash
# 提取第 3.5 秒的帧
frame-extractor single -i video.mp4 -t 3.5 -o frame_at_3_5s.jpg

# 提取第 10 秒的帧
frame-extractor single -i video.mp4 -t 10 -o frame_10s.jpg
```

### 3. 批量提取多帧

```bash
# 提取第 10 到 50 帧，每隔 5 帧提取一次
frame-extractor batch -i video.mp4 -o frames -s 10 -e 50 -d 5

# 使用多线程加速
frame-extractor batch -i video.mp4 -o frames -s 0 -e 100 -d 1 -w 8
```

### 4. 按时间间隔采样

```bash
# 每 2 秒提取一帧
frame-extractor sample -i video.mp4 -o samples -t 2

# 每 0.5 秒提取一帧
frame-extractor sample -i video.mp4 -o samples -t 0.5
```

### 5. 显示视频信息

```bash
frame-extractor info -i video.mp4
```

输出示例：
```
Video Information:
  Path: video.mp4
  Duration: 120.5 seconds
  Frame Rate: 30.0 fps
  Total Frames: 3615
  Resolution: 1920x1080
  Codec: h264
```

### 6. 批量提取目录首帧

#### 提取当前目录

```bash
# 提取目录下所有视频的首帧
frame-extractor dirfirst -i videos_dir -o output_dir
```

#### 递归提取（保持目录结构）

```bash
# 递归提取所有子目录下的视频首帧
frame-extractor dirfirst -i videos_dir -o output_dir -r
```

#### 提取并压缩为 WebP

```bash
# 提取首帧并压缩转换为 WebP
frame-extractor dirfirst -i videos_dir -o output_dir -c

# 指定 WebP 质量
frame-extractor dirfirst -i videos_dir -o output_dir -c --webp-quality 90

# 控制文件大小（50-100KB）
frame-extractor dirfirst -i videos_dir -o output_dir -r -c --min-size 50 --max-size 100
```

### 7. 图片压缩转换为 WebP

#### 压缩当前目录

```bash
# 压缩图片为 WebP
frame-extractor compress -i images_dir -o webp_dir
```

#### 递归压缩

```bash
# 递归压缩所有子目录（保持目录结构）
frame-extractor compress -i images_dir -o webp_dir -r
```

#### 指定质量和大小

```bash
# 指定 WebP 质量
frame-extractor compress -i images_dir -o webp_dir -q 95

# 限制文件大小（不超过 100KB）
frame-extractor compress -i images_dir -o webp_dir --max-size 100

# 限制文件大小范围（50-200KB）
frame-extractor compress -i images_dir -o webp_dir --min-size 50 --max-size 200
```

### 8. 视频压缩

#### 压缩单个视频

```bash
# 中等质量压缩（推荐）
frame-extractor vcompress -i input.mp4 -o output.mp4 -q 50

# 高质量压缩
frame-extractor vcompress -i input.mp4 -o output.mp4 -q 80

# 高压缩率
frame-extractor vcompress -i input.mp4 -o output.mp4 -q 20
```

#### 使用不同的编码预设

```bash
# 高质量，慢速编码（最终发布）
frame-extractor vcompress -i input.mp4 -o output.mp4 -q 50 -p slower

# 快速编码（临时处理）
frame-extractor vcompress -i input.mp4 -o output.mp4 -q 50 -p veryfast
```

#### 批量压缩目录

```bash
# 压缩目录下的所有视频
frame-extractor vcompress -i videos_dir -o output_dir -q 50

# 递归压缩，使用多线程
frame-extractor vcompress -i videos_dir -o output_dir -r -q 50 -p slow -w 4
```

## 📊 压缩参数说明

### Quality 参数（-q, --quality）

| Quality | CRF 值 | 说明 |
|---------|--------|------|
| 100     | 0      | 几乎无损，文件最大 |
| 80      | 10     | 高质量 |
| 60      | 20     | 较好质量 |
| 50      | 25     | 中等质量（推荐） |
| 40      | 30     | 较低质量 |
| 20      | 40     | 高压缩率 |
| 0       | 51     | 最高压缩率，质量最低 |

### Preset 参数（-p, --preset）

| Preset    | 编码速度 | 压缩效率 | 适用场景 |
|-----------|----------|----------|----------|
| ultrafast | 最快     | 最低     | 实时转码、快速预览 |
| veryfast  | 很快     | 较低     | 快速处理 |
| fast      | 快       | 中等     | 日常使用 |
| medium    | 中等     | 中等     | 默认推荐 |
| slow      | 慢       | 较高     | 存档备份 |
| slower    | 更慢     | 很高     | 最终发布版本 |
| veryslow  | 最慢     | 最高     | 追求最小文件体积 |

**提示：** 预设越慢，同等画质下文件越小，但编码时间越长。

## 📋 完整参数一览

### 全局参数

| 参数 | 说明 |
|------|------|
| -v, --version | 显示版本和依赖信息 |

### single（提取单帧）

| 参数 | 说明 | 必需 | 备注 |
|------|------|------|------|
| -i, --input | 输入视频路径 | ✅ |  |
| -o, --output | 输出图像路径 |  | 默认自动生成 |
| -f, --frame | 要提取的帧号 | 二选一 | 和 -t 互斥 |
| -t, --time | 要提取的时间点（秒） | 二选一 | 和 -f 互斥 |
| --quality | JPEG 质量（0-100） |  | 默认 95 |

### batch（批量提取）

| 参数 | 说明 | 必需 | 备注 |
|------|------|------|------|
| -i, --input | 输入视频路径 | ✅ |  |
| -o, --output | 输出目录 | ✅ |  |
| -s, --start | 起始帧号 | ✅ |  |
| -e, --end | 结束帧号 | ✅ |  |
| -d, --delta | 帧间隔 |  | 默认 1 |
| -w, --workers | 工作线程数 |  | 默认 4 |

### sample（采样提取）

| 参数 | 说明 | 必需 | 备注 |
|------|------|------|------|
| -i, --input | 输入视频路径 | ✅ |  |
| -o, --output | 输出目录 | ✅ |  |
| -t, --interval | 采样间隔（秒） |  | 默认 1.0 |
| -w, --workers | 工作线程数 |  | 默认 4 |

### info（视频信息）

| 参数 | 说明 | 必需 |
|------|------|------|
| -i, --input | 输入视频路径 | ✅ |

### dirfirst（批量目录首帧提取）

| 参数 | 说明 | 必需 | 备注 |
|------|------|------|------|
| -i, --input_dir | 输入视频目录 | ✅ |  |
| -o, --output_dir | 输出图片目录 | ✅ |  |
| -r, --recursive | 递归遍历子目录 |  | 保持对等目录结构 |
| -c, --compress | 压缩转换为 WebP |  | 自动清理原始图片 |
| --webp-quality | WebP 压缩质量（0-100） |  | 默认 85 |
| --max-size | 最大文件大小（KB） |  | 默认 100 |
| --min-size | 最小文件大小（KB） |  | 默认 50 |

### compress（图片压缩转换）

| 参数 | 说明 | 必需 | 备注 |
|------|------|------|------|
| -i, --input_dir | 输入图片目录 | ✅ |  |
| -o, --output_dir | 输出 WebP 图片目录 | ✅ |  |
| -r, --recursive | 递归遍历子目录 |  | 保持对等目录结构 |
| -q, --quality | WebP 压缩质量（0-100） |  | 默认 85 |
| --max-size | 最大文件大小（KB） |  | 默认 100 |
| --min-size | 最小文件大小（KB） |  | 默认 50 |

### vcompress（视频压缩）

| 参数 | 说明 | 必需 | 备注 |
|------|------|------|------|
| -i, --input | 输入视频路径或目录 | ✅ | 文件或目录 |
| -o, --output | 输出视频路径或目录 | ✅ | 文件或目录 |
| -r, --recursive | 递归遍历子目录 |  | 保持对等目录结构 |
| -q, --quality | 压缩质量（0-100） |  | 默认 50 |
| -p, --preset | 编码速度预设 |  | 默认 medium |
| -w, --workers | 工作线程数 |  | 默认 2 |

## 🎯 典型使用场景

### 场景 1：为视频库生成缩略图

```bash
# 递归提取所有视频的首帧并压缩为 WebP
frame-extractor dirfirst -i ~/Videos -o ~/Thumbnails -r -c --min-size 30 --max-size 80
```

### 场景 2：提取关键帧用于分析

```bash
# 每 5 秒提取一帧
frame-extractor sample -i video.mp4 -o keyframes -t 5
```

### 场景 3：视频质量优化

```bash
# 压缩视频以减小文件大小
frame-extractor vcompress -i large_video.mp4 -o compressed_video.mp4 -q 50 -p slow
```

### 场景 4：批量转换图片为 WebP

```bash
# 递归转换所有图片为 WebP，质量 90
frame-extractor compress -i ~/Pictures -o ~/Pictures_WebP -r -q 90
```

## 🦠 卸载

```bash
# 删除安装目录
rm -rf ~/.video-frame-extractor

# 删除可执行命令
rm ~/.local/bin/frame-extractor
```

## 🤝 参与贡献

欢迎提交 PR 或 issue！

仓库地址：https://github.com/indulgeback/video-frame-extractor

## 📚 相关文档

- 主仓库：https://github.com/indulgeback/video-frame-extractor
- 问题反馈：https://github.com/indulgeback/video-frame-extractor/issues

---

**作者：** indulgeback
**版本：** 1.0.0
**许可证：** MIT
