# 安装指南

## 系统依赖

### FFmpeg（必需）

FFmpeg用于从视频中提取关键帧，是必需依赖。

#### Windows

```powershell
# 使用 Chocolatey
choco install ffmpeg

# 或使用 Scoop
scoop install ffmpeg

# 或手动下载
# 访问 https://ffmpeg.org/download.html 下载并添加到PATH
```

#### macOS

```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install ffmpeg
```

#### Linux (CentOS/RHEL)

```bash
sudo yum install epel-release
sudo yum install ffmpeg
```

#### 验证安装

```bash
ffmpeg -version
```

## Python依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows

# 安装依赖
pip install requests yt-dlp
```

### 依赖说明

| 包 | 版本 | 用途 |
|---|------|------|
| `requests` | >=2.28.0 | HTTP请求，获取视频元数据 |
| `yt-dlp` | >=2023.0.0 | 视频下载 |

### 开发依赖（可选）

```bash
pip install hypothesis pytest
```

| 包 | 版本 | 用途 |
|---|------|------|
| `hypothesis` | >=6.0.0 | 属性测试 |
| `pytest` | >=7.0.0 | 单元测试 |
