# 常见问题与解决方案

---

## 问题分类说明

**简单问题（1-2步排查）**：参数错误、环境问题等  
**中等问题（3-5步排查）**：下载失败、格式问题等  
**复杂问题（5-10步排查）**：网络问题、网站更新等

---

## 安装问题

### 1. pip install失败【简单问题】

**问题描述**: 使用pip安装you-get时报错

**排查步骤**:
```bash
# 检查Python版本
python --version

# 检查pip版本
pip --version
```

**常见原因**:
- Python版本过低 (40%)
- 网络连接问题 (30%)
- 权限不足 (20%)
- pip版本过低 (10%)

**解决方案**:

**方案A（推荐新手）**: 升级pip
```bash
python -m pip install --upgrade pip
pip install you-get
```

**方案B（网络问题）**: 使用国内镜像
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple you-get
```

**方案C（权限问题）**: 用户安装
```bash
pip install --user you-get
```

---

### 2. FFmpeg未安装警告【简单问题】

**问题描述**: 下载高清视频时提示FFmpeg未安装

**排查步骤**:
```bash
ffmpeg -version
```

**常见原因**: FFmpeg未安装或未添加到PATH

**解决方案**:

**macOS**:
```bash
brew install ffmpeg
```

**Ubuntu/Debian**:
```bash
sudo apt install ffmpeg
```

**Windows**:
1. 下载 https://ffmpeg.org/download.html
2. 解压并添加到系统PATH

---

## 下载问题

### 3. 视频下载失败【中等问题】

**问题描述**: you-get无法下载视频或提示错误

**排查步骤**:
```bash
# 1. 检查URL是否正确
you-get -i 'URL'

# 2. 检查网站是否支持
you-get --help | grep "supported sites"

# 3. 尝试使用代理
you-get -x 127.0.0.1:8087 'URL'

# 4. 更新you-get
pip install --upgrade you-get
```

**常见原因**:
- 网站更新（需要更新you-get）(40%)
- 网络问题 (30%)
- 地区限制 (20%)
- URL格式错误 (10%)

**解决方案**:

**方案A（推荐）**: 更新you-get
```bash
pip install --upgrade you-get
you-get 'URL'
```

**方案B（网络问题）**: 使用代理
```bash
you-get -x 127.0.0.1:8087 'URL'
```

**方案C（地区限制）**: 使用提取器代理
```bash
you-get -y 127.0.0.1:8087 'URL'
```

---

### 4. YouTube视频无法下载【中等问题】

**问题描述**: YouTube视频下载失败或只有音频

**排查步骤**:
```bash
# 1. 查看可用格式
you-get -i 'https://www.youtube.com/watch?v=xxxxx'

# 2. 检查FFmpeg
ffmpeg -version

# 3. 尝试指定格式
you-get --itag=18 'URL'
```

**常见原因**:
- DASH格式需要FFmpeg合并 (50%)
- 视频被删除或私有 (30%)
- 地区限制 (20%)

**解决方案**:

**方案A（缺少FFmpeg）**: 安装FFmpeg
```bash
# 安装后重新下载
brew install ffmpeg  # macOS
you-get 'URL'
```

**方案B（指定格式）**: 选择非DASH格式
```bash
# 选择itag=18（非DASH）
you-get --itag=18 'URL'
```

**方案C（使用cookies）**: 下载登录后可见视频
```bash
you-get -c cookies.txt 'URL'
```

---

### 5. Bilibili视频下载失败【中等问题】

**问题描述**: Bilibili视频下载提示错误或只能下载低画质

**排查步骤**:
```bash
# 1. 检查视频是否需要登录
you-get -i 'https://www.bilibili.com/video/BV1xx411c7mD'

# 2. 检查是否地区限制
curl -I 'https://www.bilibili.com'

# 3. 尝试更新you-get
pip install --upgrade you-get
```

**常见原因**:
- Bilibili更新反爬机制 (40%)
- 视频需要登录 (30%)
- 高画质需要会员 (20%)
- you-get版本过旧 (10%)

**解决方案**:

**方案A（更新）**: 更新you-get
```bash
pip install --upgrade you-get
pip install --upgrade git+https://github.com/soimort/you-get@develop
```

**方案B（登录）**: 使用cookies
```bash
you-get -c cookies.txt 'URL'
```

**方案C（备用）**: 使用其他工具
```bash
# 如you-get不支持，可尝试youtube-dl或yt-dlp
pip install yt-dlp
yt-dlp 'URL'
```

---

## 格式与质量问题

### 6. 无法下载1080p视频【简单问题】

**问题描述**: 只能下载720p或更低分辨率

**排查步骤**:
```bash
# 查看所有可用格式
you-get -i 'URL'
```

**常见原因**:
- 1080p+需要FFmpeg合并 (60%)
- 视频本身最高只有720p (30%)
- 格式选择错误 (10%)

**解决方案**:

**方案A（安装FFmpeg）**:
```bash
# 安装FFmpeg后可下载任意分辨率
brew install ffmpeg
you-get 'URL'
```

**方案B（手动选择）**:
```bash
# 查看可用格式，选择最高分辨率
you-get -i 'URL'
you-get --itag=最高分辨率itag 'URL'
```

---

### 7. 下载的视频没有声音【中等问题】

**问题描述**: 视频文件只有画面没有声音

**排查步骤**:
```bash
# 1. 检查视频文件
ffprobe video.mp4

# 2. 检查是否有独立音频流
you-get -i 'URL'

# 3. 检查FFmpeg
ffmpeg -version
```

**常见原因**:
- DASH格式音视频分离，未合并 (70%)
- FFmpeg未安装或版本过低 (20%)
- 下载过程中断 (10%)

**解决方案**:

**方案A（安装FFmpeg）**: 
```bash
# 安装FFmpeg，you-get会自动合并
brew install ffmpeg
you-get 'URL'
```

**方案B（手动合并）**:
```bash
# 如果you-get未自动合并
ffmpeg -i video.mp4 -i audio.m4a -c copy output.mp4
```

---

## 网络问题

### 8. 下载速度很慢【中等问题】

**问题描述**: 下载速度远低于带宽上限

**排查步骤**:
```bash
# 1. 测试网络速度
speedtest-cli

# 2. ping视频网站服务器
ping youtube.com

# 3. 尝试使用代理
you-get -x 127.0.0.1:8087 'URL'
```

**常见原因**:
- 源服务器限制 (40%)
- 网络拥堵 (30%)
- 跨境访问慢 (20%)
- 未使用代理 (10%)

**解决方案**:

**方案A（使用代理）**:
```bash
you-get -x 127.0.0.1:8087 'URL'
```

**方案B（使用镜像站）**:
```bash
# 某些网站有国内镜像，访问更快
```

**方案C（分段下载）**:
```bash
# 使用--no-merge，分段下载后手动合并
you-get -n 'URL'
```

---

### 9. 连接超时【简单问题】

**问题描述**: 提示连接超时或Connection timeout

**排查步骤**:
```bash
# 检查网络连接
ping google.com

# 检查代理设置
echo $http_proxy
```

**常见原因**:
- 网络不通 (50%)
- 防火墙阻挡 (30%)
- 需要代理 (20%)

**解决方案**:

**方案A（使用代理）**:
```bash
you-get -x 127.0.0.1:8087 'URL'
```

**方案B（检查防火墙）**:
```bash
# 临时关闭防火墙测试
sudo ufw disable  # Linux
```

---

## 高级问题

### 10. 批量下载中断【中等问题】

**问题描述**: 批量下载时某个视频失败导致整个脚本停止

**排查步骤**:
```bash
# 检查失败的URL
you-get -i '失败URL'

# 单独下载测试
you-get '失败URL'
```

**解决方案**:

**方案A（错误处理）**: 修改脚本添加错误处理
```bash
while read url; do
    you-get "$url" || echo "Failed: $url" >> failed.txt
done < download_list.txt
```

**方案B（并行下载）**: 使用xargs
```bash
cat download_list.txt | xargs -P 4 -I {} you-get {}
```

---

## 获取帮助

### 日志收集
```bash
# 启用详细日志
you-get --debug 'URL'

# 查看详细错误信息
you-get -i 'URL' 2>&1 | tee you-get.log
```

### 诊断命令汇总
```bash
# 检查you-get版本
you-get --version

# 检查Python环境
python --version
pip list | grep you-get

# 检查FFmpeg
ffmpeg -version

# 查看支持的网站
you-get --help
```

### 参考资源
- GitHub: https://github.com/soimort/you-get
- Wiki: https://github.com/soimort/you-get/wiki
- Issues: https://github.com/soimort/you-get/issues
- Gitter: https://gitter.im/soimort/you-get

---

**提示**: 如遇到本文档未涵盖的问题，请到GitHub Issues搜索或提问