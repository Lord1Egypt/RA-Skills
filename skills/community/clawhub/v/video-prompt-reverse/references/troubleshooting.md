# 常见问题排查指南

## PowerShell 中文编码崩溃

**症状：** 执行含中文的 Python 命令时报 `UnicodeEncodeError: 'gbk' codec can't encode character`

**原因：** PowerShell 默认使用 GBK 编码，Python 的 UTF-8 输出无法显示

**解决：** 在命令前加 `PYTHONIOENCODING=utf-8`
```powershell
$env:PYTHONIOENCODING="utf-8"; python script.py
```
**永久解决方案：** PowerShell 配置文件 `~\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1` 中添加：
```powershell
$env:PYTHONIOENCODING="utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

## yt-dlp 下载失败

**症状：** 下载报错或返回空文件

**排查顺序：**
1. 视频链接是否有效（抖音/快手需要 cookie 才能下非公开/会员内容）
2. 加 `--no-check-certificates` 跳过 SSL 验证
3. 用 `--cookies-from-browser chrome` 从浏览器导入 cookie
4. 查看详细错误：`yt-dlp -v "URL"` 输出 debug 信息

## FFmpeg 提取帧失败

**症状：** `frames/f_%03d.jpg` 文件夹为空

**排查：**
```powershell
# 检查视频是否正常
ffprobe video.mp4

# 检查视频编码
ffmpeg -i video.mp4 2>&1 | Select-String "Video:"

# 常见问题：视频流不在第一个轨道，用 -map 指定
ffmpeg -i video.mp4 -map 0:v:0 -vf "select='not(mod(n\,40))'" -vsync vfr "frames/f_%03d.jpg"
```

## CDP 连接失败

**症状：** `WebSocket connection refused` 或 `CDP connection error`

**排查：**
1. 确认 Edge DevTools 是否开启（端口 9222）
2. 确认端口是否被占用：`netstat -ano | Select-String "9222"`
3. 获取正确 WebSocket URL：
```python
import subprocess, json
r = subprocess.run(['powershell', '-Command',
    'curl -s http://localhost:9222/json'], capture_output=True)
tabs = json.loads(r.stdout.decode())
for t in tabs: print(t['webSocketDebuggerUrl'])
```

## CDP click_by_ref 失效

**症状：** 按钮点击无反应，或报 ref 不存在

**原因：** accessibility tree 快照有延迟，ref 在执行时已过期

**解决：** 用 JS 直接查找和点击：
```python
script = """
const btns = Array.from(document.querySelectorAll('button'));
const btn = btns.find(b => b.innerText.includes('解释图片'));
if (btn) btn.click();
else console.error('NOT_FOUND: ' + btns.map(b=>b.innerText).join('|'));
"""
cdp.execute(script)
```

## 帧文件编号错误

**症状：** 帧文件 `f_060.jpg` / `f_180.jpg` 不存在

**原因：** ffmpeg 每40帧提取，第60帧不在序列中

**正确帧号：** 必须是 40 的倍数：`f_000 / f_040 / f_080 / f_120 / f_160 / f_200 / f_240 / f_280 / f_320 / f_360`

## 豆包分析结果为空

**症状：** 上传图片后豆包无回复或回复无意义

**解决：**
1. 确认图片已全部上传完成（检查豆包界面是否有"上传完成"提示）
2. 等待几秒再点击"解释图片"（上传需要时间）
3. 检查豆包是否登录、是否有网络问题
4. 每次分析后清理输入框（避免上下文混乱）

## 提示词提取质量低

**症状：** 豆包回复太泛、缺细节

**解决：**
1. 上传更多帧（至少5张，覆盖全片不同时间点）
2. 帧间隔不要太大（15s 视频用 40 帧间隔，约 5-7 张）
3. 在分析提示词里明确要求：`请识别景别、机位、运镜、服装细节、色调、构图`
