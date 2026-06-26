# Video Pipeline 安装指南

## 前置条件

### 系统要求
- Windows 10/11 或 Linux/macOS
- 至少8GB RAM
- 5GB可用磁盘空间
- 网络连接（用于下载依赖和API调用）

### 软件依赖
1. **Node.js** (版本 >= 16.x)
   - 下载地址: https://nodejs.org/
   - 验证安装: `node --version`

2. **Python** (版本 >= 3.8)
   - 下载地址: https://python.org/
   - 验证安装: `python --version`

3. **FFmpeg**
   - 下载地址: https://ffmpeg.org/download.html
   - 验证安装: `ffmpeg -version`

## 安装步骤

### 1. 安装Python依赖
```bash
pip install edge-tts requests dashscope mutagen
```

### 2. 安装Node.js依赖
进入视频项目目录并安装Remotion:
```bash
cd C:\Users\liweiwei\course-video-remotion
npm install remotion @remotion/cli
```

### 3. 验证安装
运行环境检查脚本:
```bash
python "C:\Users\liweiwei\course-video-remotion\scripts\pipeline.py" --help
```

## 环境变量配置

### DashScope API密钥配置
1. 创建API密钥文件:
```bash
mkdir -p ~/.openclaw/workspace/credentials/
```

2. 在 `~/.openclaw/workspace/credentials/dashscope.json` 中添加API密钥:
```json
{
  "api_key": "YOUR_DASHSCOPE_API_KEY_HERE",
  "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
}
```

注意: 请将 `YOUR_DASHSCOPE_API_KEY_HERE` 替换为您的实际API密钥。

## 故障排除

### 常见问题

#### 1. "找不到Python模块"错误
解决方法: 确保已安装所有Python依赖
```bash
pip install -r C:\Users\liweiwei\course-video-remotion\requirements.txt
```

#### 2. "找不到Node.js"错误
解决方法: 确保Node.js已正确安装并添加到PATH环境变量

#### 3. "FFmpeg未找到"错误
解决方法: 
- Windows: 下载FFmpeg并将其bin目录添加到系统PATH
- Linux: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`

#### 4. API调用失败
- 检查网络连接
- 验证API密钥是否正确配置
- 确认API配额是否充足

#### 5. 渲染失败
- 检查是否有足够磁盘空间
- 确保内存充足（建议8GB以上）
- 检查项目路径权限

### 验证安装
运行测试命令验证所有组件是否正常工作:
```bash
python "C:\Users\liweiwei\course-video-remotion\scripts\pipeline.py" "这是一个测试视频，请忽略" --duration 1
```

如果看到环境检测成功的消息，则表示安装成功。