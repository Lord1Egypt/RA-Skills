# 完整工作流详解

## 工具链概览

| 工具 | 用途 | 安装 |
|------|------|------|
| yt-dlp | 下载短视频 | `pip install -U yt-dlp` |
| ffmpeg | 提取关键帧 | 系统环境变量 |
| Edge + 豆包PC版 | 视觉分析（CDP） | 需开启 DevTools |
| Python + CDP Client | 自动化浏览器操作 | 需 websocket 库 |

## Step 1 · 视频下载

### 平台支持
- 抖音（需 cookie 或非VIP）
- 快手（需 cookie 或非VIP）
- 本地视频文件（直接进入 Step 2）

### 命令模板
```powershell
$env:PYTHONIOENCODING="utf-8"
yt-dlp --max-duration 180 -f "bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]" -o "video.%(ext)s" "VIDEO_URL"
```

**参数说明：**
- `--max-duration 180`：最长3分钟（避免过大文件）
- `-f "bestvideo[ext=mp4][height<=720]+bestaudio"`：优先720p MP4，视频音频分开下载后合并
- 无 cookie 时可能下载失败（需登录态）

### 分析视频参数
```powershell
ffprobe -v quiet -print_format json -show_streams video.mp4
```
输出包含 `duration`（时长秒）、`r_frame_rate`（帧率，如"30000/1001"≈29.97fps）

## Step 2 · 提取关键帧

### 建立帧目录
```powershell
mkdir .\frames
```

### 提取帧
```powershell
ffmpeg -i video.mp4 -vf "select='not(mod(n\,40))',scale=1280:-1" -vsync vfr "frames/f_%03d.jpg" -hide_banner
```

**参数说明：**
- `select='not(mod(n\,40))'`：每40帧取一帧（40帧 @ 29fps ≈ 每1.33秒取一帧）
- `scale=1280:-1`：宽度统一1280px，高度按比例缩放
- `-vsync vfr`：可变帧率，避免重复帧

### 根据视频时长选帧策略
| 时长 | 帧间隔 | 提取数量（13.8s） |
|------|--------|-----------------|
| ~15s 短片 | 40帧 | ~10张 |
| ~30s 短片 | 80帧 | ~10张 |
| ~60s 短片 | 160帧 | ~10张 |

**选帧原则：** 选片头(0%)、中前(25%)、中段(50%)、中后(75%)、片尾(100%)覆盖完整时间线。

## Step 3 · 豆包PC版 CDP 分析

### 启动豆包并开启 DevTools
1. 关闭所有 Edge 窗口
2. 以 DevTools 模式启动豆包：
```powershell
& "C:\Users\Administrator\AppData\Local\MicroMessenger\WeChatWin.dll"  # 错误示例
```
正确方式：在 Edge 地址栏输入 `edge://version/` 查看 Edge 路径，然后：
```powershell
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222
```
然后手动打开豆包网页版 `https://doubao.com`

### 获取 Tab ID
在 Chrome/Edge DevTools (F12) → Console 执行：
```js
chrome.webview.requestHeaderCustomValuesEnabled(true)
// 或直接在 Network 面板找 ws://.../devtools/page/xxx
```
或用 Python 脚本枚举所有 DevTools Tab：
```python
import json, subprocess
result = subprocess.run(['powershell', '-Command', '...'], ...)
# 解析 JSON 获取 tab ID
```

**已知 Tab ID：** `E7C2FA5DB0FB60DDD01D97EFAB45BCD8`（豆包PC版）

### 使用 doubao_cdp.py 批量分析

**核心流程：**
1. 连接 CDP
2. 批量上传多张帧图（一次上传 4-5 张，覆盖完整时间线）
3. 点击"解释图片"按钮
4. 读取分析结果文本

**上传帧选择策略（13.8秒视频）：**
```
f_000 → 0:00  (片头)
f_080 → 2.7s  (片头→中段过渡)
f_160 → 5.5s  (中段)
f_200 → 6.9s  (中段后半)
f_280 → 9.7s  (后段)
f_360 → 12.4s (片尾)
```

**关键代码片段（点击"解释图片"按钮）：**
```python
# 用 JS 直接查找按钮，避免 ref 失效问题
script = """
const buttons = Array.from(document.querySelectorAll('button'));
const target = buttons.find(b => b.innerText.includes('解释图片'));
if (target) { target.click(); console.log('Clicked: ' + target.innerText); }
else { console.log('Buttons found: ' + buttons.map(b=>b.innerText).join('|')); }
"""
cdp.execute(script)
```

**读取分析结果：**
```python
# 等待结果出现，然后 snapshot
snapshot = browser_snapshot(targetId=tab_id, ...)
# 提取回复文本
```

## Step 4 · 提取结构化提示词

### 提示词格式
```
[景别] [主体] in [场景/地点], [服装细节], [色调], [光线描述], [构图方式], shot on [拍摄设备], [运镜方式]
```

### 常用景别词汇
| 英文 | 中文 |
|------|------|
| Extreme Close-up | 极特写 |
| Close-up / CU | 特写 |
| Medium Close-up / MCU | 中特写 |
| Medium Shot / MS | 中景 |
| Medium Wide Shot / MWS | 中全景 |
| Wide Shot / WS | 全景 |
| Extreme Wide Shot / EWS | 超远景 |
| Full Shot | 全身 |
| Over-the-shoulder | 过肩 |
| POV | 主观视角 |

### 常用光线词汇
| 英文 | 中文 |
|------|------|
| Soft natural light | 柔和自然光 |
| Golden hour lighting | 黄金时段光 |
| Backlit silhouette | 逆光剪影 |
| High-key lighting | 高调光 |
| Low-key lighting | 低调光 |
| Rim lighting / edge light | 轮廓光 |
| Studio lighting | 影棚光 |
| Cinematic lighting | 电影感光 |
| Cold/blue tones | 冷调蓝 |
| Warm/orange tones | 暖调橙 |

### 示例输出
```
Medium Close-up portrait of a young man on a dirt road, wearing a worn gray cotton jacket, dusty blue tones, golden afternoon light from the side, 2:1 cinema aspect ratio, shot on Sony A7III with 85mm f/1.4, slow dolly-in movement, cinematic mood

Wide establishing shot of a rural village path at sunset, dust particles floating in warm orange light, faded blue sky, dusty road surface, shot on RED Komodo with 24mm lens, slow tracking shot, documentary realism
```
