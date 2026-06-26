# 安装指南

**适用场景**: 首次使用you-get，需要安装和配置环境

---

## 一、安装前准备

### 目标
确保系统具备运行you-get的基础环境

### 前置条件
- Python 3.7.4 或更高版本
- pip包管理器
- （推荐）FFmpeg视频处理工具

### 检查环境

**AI执行说明**: AI将自动检查你的系统环境

```bash
# 检查Python版本
python --version

# 检查pip
pip --version

# 检查FFmpeg（可选）
ffmpeg -version
```

**期望结果**:
- Python 3.7.4+ ✅
- pip已安装 ✅
- FFmpeg已安装 ✅（可选）

---

## 二、安装you-get

### 方法1: 使用pip安装（推荐）

**AI执行说明**: AI可以直接执行安装命令

```bash
# 安装you-get
pip install you-get

# 验证安装
you-get --version
```

**期望结果**:
```
you-get: version 0.4.1555, a tiny downloader that scrapes the web.
```

### 方法2: 使用Homebrew（macOS）

```bash
brew install you-get
```

### 方法3: 从源码安装

```bash
# 克隆仓库
git clone https://github.com/soimort/you-get.git

# 安装
cd you-get
python -m pip install .
```

---

## 三、安装FFmpeg（重要）

**为什么需要FFmpeg?**
- 合并分段视频（DASH格式）
- 下载高清视频（1080p+）
- 转换视频格式

### macOS安装

```bash
brew install ffmpeg
```

### Linux安装

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

### Windows安装

1. 下载: https://ffmpeg.org/download.html
2. 解压到任意目录
3. 添加到系统PATH

---

## 四、验证安装

**AI执行说明**: AI将验证所有依赖是否正确安装

```bash
# 验证you-get
you-get --version

# 验证FFmpeg
ffmpeg -version

# 测试下载
you-get -i 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
```

**成功标志**:
- ✅ you-get版本信息显示
- ✅ FFmpeg版本信息显示
- ✅ 测试视频信息获取成功

---

## 五、升级you-get

```bash
# 使用pip升级
pip install --upgrade you-get

# 或使用you-get自升级
you-get https://github.com/soimort/you-get/archive/master.zip
```

---

## 六、常见安装问题

### 问题1: pip not found

**解决方案**:
```bash
# 安装pip
python -m ensurepip --upgrade
```

### 问题2: 权限错误

**解决方案**:
```bash
# 使用用户安装
pip install --user you-get
```

### 问题3: 网络超时

**解决方案**:
```bash
# 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple you-get
```

---

## 完成确认

### 检查清单
- [ ] Python 3.7.4+ 已安装
- [ ] you-get 已安装并可运行
- [ ] FFmpeg 已安装（推荐）
- [ ] 测试下载成功

### 下一步
继续阅读 [快速开始](02-quickstart.md) 学习如何下载视频