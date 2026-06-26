# 视频下载脚本

## B站下载

```bash
# 先查看可用格式
yt-dlp --list-formats "<bilibili_url>"

# 下载720p视频+音频并合并
yt-dlp -f "30066+30232" -o "<output_path>/bilibili.mp4" --merge-output-format mp4 "<bilibili_url>"

# 如果上面格式不存在，用通用方式
yt-dlp -f "best[height<=720]" -o "<output_path>/bilibili.mp4" "<bilibili_url>"
```

B站URL示例：
- `https://b23.tv/mxxRnay`
- `https://www.bilibili.com/video/BVxxxxx`

## 抖音下载（三步）

### 步骤1: 浏览器打开抖音页面提取视频URL

```
# 使用 chrome-devtools MCP
1. navigate_page -> url: https://v.douyin.com/xxxxx/
2. evaluate_script -> () => { return document.querySelector('video').src; }
3. 记录返回的视频URL
```

### 步骤2: Python带Referer下载

```python
import urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')
url = '<从浏览器获取的视频URL>'
headers = {
    'Referer': 'https://www.douyin.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=60)
data = resp.read()
with open('<output_path>/douyin.mp4', 'wb') as f:
    f.write(data)
print(f'Downloaded: {len(data)/1024/1024:.1f} MB')
```

### 步骤3: 备用方案（如果浏览器方案失败）

如果抖音链接无法通过浏览器提取，可尝试：
1. 让用户在手机上截图发过来
2. 使用 agent-reach 的 douyin MCP（需服务在线）

## 今日头条下载

```bash
# 先查看格式
yt-dlp --list-formats "<toutiao_url>"

# 指定格式下载（头条通常需要指定720p格式）
yt-dlp -f "720p" -o "<output_path>/toutiao.mp4" "<toutiao_url>"

# 或通用方式
yt-dlp -f "best[height<=720]" -o "<output_path>/toutiao.mp4" "<toutiao_url>"
```

头条URL示例：
- `https://m.toutiao.com/is/xxxxx/`
- `https://www.toutiao.com/video/xxxxx/`
