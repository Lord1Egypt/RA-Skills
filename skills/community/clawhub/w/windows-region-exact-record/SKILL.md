---
name: windows-region-exact-record
description: "Record an exact-length screen region on Windows with ffmpeg gdigrab — including the high-DPI physical-pixel coordinate trap (200% scaling offsets), a no-install screenshot tool path, and a ready-to-use picker plus recorder script. Use for 'region screen record', 'record 10 seconds', 'record specific area', 'gdigrab', 'ffmpeg capture', '区域录屏', '录屏10秒', '指定区域录制', '高DPI坐标不对', '录屏尺寸减半'."
license: MIT
metadata:
  displayName: "Windows Exact-Duration Region Recording (gdigrab/ffmpeg)"
  category: "media-tool"
  slug: windows-region-exact-record
  description_zh: Windows 区域录屏精确时长（区域录屏/录屏10秒/指定区域录制/gdigrab/ffmpeg 抓屏/offset_x/video_size/高DPI 缩放坐标不对/录屏尺寸减半/show_region 校验/无声音/mp4）：物理像素坐标陷阱 + 脚本 + 验收口径。
  version: 1.0.0
  author: WorkBuddy
  agent_created: true
---
# Windows 精确时长区域录屏

在 Windows 上把屏幕上**一块固定矩形**录成 mp4，长度精确到你要的秒数。

这个 skill 解决的不是"怎么录屏"，而是三个具体会翻车的地方：**高 DPI 下坐标差一倍**、**时长不准**、**提示器被录进画面**。

## 什么时候用它

- 要录一段固定时长的素材（做 demo、复现 bug、抓动画）
- 只要屏幕一角，不要全屏
- 高分辨率 + 缩放（4K@200%、2K@150%）下录出来位置不对或尺寸减半

## 一、先定口径：三个数必须说清

| 项 | 口径 | 说错的后果 |
|---|---|---|
| 区域 | `x, y, w, h`，**以主显示器左上角为原点** | gdigrab 的 offset 永远从主屏算，副屏坐标直接偏 |
| 单位 | **物理像素**，不是逻辑像素 | 200% 缩放下差一倍 |
| 时长 | 手动停 或 `--sec N` 自动停 | 靠人手掐表，误差 1~2s 起步 |

## 二、最大的坑：高 DPI 下的两套坐标

一个没有声明 DPI 感知的进程，从 `GetCursorPos` / 窗口矩形拿到的都是**逻辑像素**。而 gdigrab 的 `-offset_x -offset_y -video_size` 全要**物理像素**。

后果：

- 200% 缩放，选区看起来是 1200×800，录出来只有 **600×400**（正好一半）
- 位置整体向屏幕左上角偏移

**修法**——进程启动第一件事就把 DPI 感知打开，只能做一次：

```python
import ctypes
def set_dpi_aware():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)   # PROCESS_PER_MONITOR_DPI_AWARE，Win8.1+
    except Exception:
        ctypes.windll.user32.SetProcessDPIAware()        # Win7 回退
```

**判据（这一步别省）**：选区 1200×800 → 用 `ffprobe` 读输出视频，必须**正好** 1200×800。得到 600×400 就是逻辑像素混进来了，不是"ffmpeg 参数没调好"。

## 三、录制参数

```
ffmpeg -f gdigrab -offset_x X -offset_y Y -video_size WxH \
       -framerate 30 -i desktop \
       -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p out.mp4
```

- `-pix_fmt yuv420p` 必须加。不加出来是 yuv444，部分播放器 / QuickTime 打不开。
- `w`、`h` 强制偶数（`w & ~1`）。奇数尺寸 libx264 直接报错。
- `-framerate` 写 30 就够，写高了文件大且和"精确时长"无关。

## 四、收尾：写 `q`，不要 kill

向 ffmpeg 的 **stdin 写 `q`** 让它自己收尾。`kill` / `terminate` 会让 mp4 的 `moov box` 不完整，文件能播但时长读成 0，或者干脆打不开。

```python
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, ...)
time.sleep(sec)
p.stdin.write(b"q"); p.stdin.flush()
p.wait(timeout=15)
```

## 五、取区域：两种方式

1. **拖拽框选**——全屏半透明遮罩，按住左键拖出矩形，实时显示尺寸，ESC 取消。
2. **两次点击**——点左上角、再点右下角，自动取 `min` 做原点、`abs` 做宽高。
3. **缓存复用**——把上次的 `x y w h` 写进 `last_region.txt`，下次直接读，不用再点。

## 六、提示器不能入画：空心边框窗口

想让人知道"正在录哪里"又不能录进去，做法是把一个窗口的区域设成**外框减内框**（`SetWindowRgn` 两个矩形的差），得到一个空心边框窗口：

- 边框画在录制矩形**外侧** 3px ⇒ 不会被 gdigrab 抓到
- 框内是真空的 ⇒ 鼠标点击穿透，不挡你在被录软件里的操作

状态条（计时 + 结束按钮）同理，自动摆到选区之外的空白处。

## 七、验收：三条，都别靠肉眼

| 项 | 判据 |
|---|---|
| 分辨率 | `ffprobe -show_entries stream=width,height` 与选区**逐像素相等** |
| 时长 | `ffprobe -show_entries format=duration`，与目标差 < 0.3s |
| 提示器未入画 | 抽首帧，取画面**最外 6px 条带**的平均色，不应等于 UI 色 |

实测数据（3840×2160 @ 200% 缩放）：

| 场景 | 结果 |
|---|---|
| 自检录 4 秒，选区 1200×800 | 1200×800 / 30fps / 4.13s / 123 帧 |
| `--sec 5` 自动停 | 5.20s |
| 手动结束（约 25 秒） | 25.30s |
| 边缘 6px 条带平均色 | (248,243,249) / (255,255,255) ≠ 红框 (234,31,33) ⇒ 未入画 |

## 八、已知限制（写进交付说明里，别让客户自己发现）

- **只录主显示器**。gdigrab 的 offset 从主屏左上角起算，副屏上的区域录不到。
- **不录声音**。要系统声/麦克风，用 Windows 11 自带截图工具（`Win + Shift + R`）。

## 九、脚本

| 文件 | 用途 |
|---|---|
| `scripts/rec_region.py` | CLI 主程序：`--pick` / `--region` / `--sec` / `--check` / `--countdown` |
| `scripts/pick_region.py` | 取坐标（两次点击）+ `set_dpi_aware()` 的唯一来源 |
| `scripts/rec10s.bat` | 双击即用：点两个角 → 倒计时 → 录 10 秒 |
| `scripts/region_rec_gui.py` | 纯 ctypes 画的 GUI（零 tkinter/PyQt 依赖），含 `--selftest` 无鼠标自检 |

```bat
rec10s.bat              :: 点两角 → 录 10 秒
rec10s.bat last         :: 复用 last_region.txt
rec10s.bat check        :: 只闪框 3 秒，确认区域对不对
python rec_region.py --sec 10 --region "100 200 800 600"
python region_rec_gui.py --selftest "1000 700 1200 800" --selftest-sec 4
```

## 十、自检口诀

**先跑 `--check` 看框，再跑 `--selftest` 验数，最后才录真东西。**

录完先 `ffprobe` 看 `width/height/duration` 三个数，全对了才交付。
