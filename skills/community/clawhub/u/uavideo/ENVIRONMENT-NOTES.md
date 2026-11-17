# 环境依赖与适配指南

本指南面向在不同环境中部署和使用本技能的研究者与 AI Agent，汇总依赖要求、平台差异、已知限制及经验证的解决方案，帮助使用者快速完成环境准备并规避常见问题。

- 文档版本：2026-11-13
- 首次整理环境：Windows 11 + 受限沙箱会话（DSH Desktop）
- 适用范围：本技能的全部工作流程（素材获取、抽帧拆条、分析报告）

---

## 一、依赖清单

| 组件 | 参考版本 | 用途 | 说明 |
|---|---|---|---|
| ffmpeg / ffprobe | 9.x | 抽帧、拆条、元信息探测、m3u8 合流 | `extract_frames.py` 的核心依赖，需加入 PATH |
| Python | 3.10+ | 运行 `scripts/` 下全部脚本 | 仅使用标准库调用外部命令，无第三方 pip 依赖 |
| yt-dlp | 2026.10+ | 平台页面链接的视频下载 | `download_media.py` 通过 `shutil.which("yt-dlp")` 探测，需保证在 PATH 中 |
| python-docx | 1.2+ | 生成 .docx 格式分析报告 | 可选 |
| pypdf | 最新 | 读取 PDF 输入 | 可选；受限环境中如安装失败，可改用页面渲染方式读取 |

**安装后自检：**

```powershell
ffmpeg -version | Select-Object -First 1
python -m yt_dlp --version
python -c "import docx; print('python-docx ok')"
```

**常见问题：Python Store 版安装的 yt-dlp 不在 PATH。** 其可执行文件位于 Python 安装目录的 `Scripts\` 子目录下。临时解决方案是将该目录加入当前会话 PATH：

```powershell
$env:PATH = "<Python安装目录>\Scripts;" + $env:PATH
```

如需永久生效，请将该路径添加至系统环境变量后重新打开终端。

---

## 二、平台页面下载：推荐路径与已知限制

对抖音等平台页面链接，`download_media.py`（封装 yt-dlp）是首选方案。以下为实测中发现的三条路径及其适用性结论。

### 路径 1：`download_media.py` + yt-dlp（可能受平台风控限制）

```powershell
python <skill>\scripts\download_media.py "https://v.douyin.com/xxxx/" -o out
```

部分平台的 extractor 要求请求携带新鲜 Cookie（`ttwid` / `msToken` / `odin_tt` 等字段组合，无需登录态）。仅提供单一 Cookie 字段可能仍被拦截，表现为 `Fresh cookies are needed` 类错误。

### 路径 2：`--cookies-from-browser`（受限环境通常不可行）

```powershell
python -m yt_dlp --cookies-from-browser chrome ...
```

该路径存在两类独立障碍：浏览器运行期间 Cookie 数据库被独占锁定；新版本浏览器的 app-bound encryption（Cookie 加密绑定浏览器进程）使 Cookie 难以被外部工具读取。除非用户明确愿意关闭全部浏览器进程并接受仍可能失败，否则不建议在此路径上投入排查时间。

### 路径 3：平台移动端接口解析（推荐的降级方案）

原理：通过短链跳转获取视频 `aweme_id`，再调用平台移动端 feed 接口取得详情 JSON，从中提取 `video.play_addr` / `bit_rate[].play_addr` 的 CDN 直链后直接下载（请求需携带 `Referer: https://www.douyin.com/`）。

关键实现要点（已在 Windows 受限环境验证可行）：

- 短链先跟随跳转，从最终 URL 或页面 HTML 中以正则提取 `/video/(\d+)`；
- 优先选取 `video.bit_rate[]` 中 `bit_rate` 最大的一档，而非 `play_addr.url_list[0]`（后者常为低码率或带水印版本）；
- 下载请求必须携带 `Referer`，否则 CDN 可能返回 403；
- `url_list` 中通常包含 3–4 个不同 CDN 域名，单一域名失败时依次切换重试。

该方案即本技能 SKILL.md 中所述「降级方案：从视频 CDN 域名获取真实地址后直链下载」的一种无界面实现，适用于无法进行浏览器抓包操作的场景。

---

## 三、受限沙箱环境的已知限制与应对

以下问题在 Windows 受限沙箱（如 DSH Desktop 会话）中出现，标准桌面环境通常不受影响，列出以供同类环境参考。

**1. 沙箱内 `curl.exe` 的 HTTPS 请求失败。** 表现为 `schannel: AcquireCredentialsHandle failed` 类错误。应对方式：改用 Node/Electron 运行时的 `fetch` 发起网络请求：

```powershell
$env:ELECTRON_RUN_AS_NODE='1'; & $env:DSH_NODE_EXECUTABLE -e "fetch('https://...').then(r=>r.text()).then(console.log)"
```

**2. 沙箱内 `pip install` 可能因临时目录权限失败。** 报错集中于 pip 的临时 unpack 目录，与网络无关。应对方式：优先使用环境内置 Python 发行版自带的库（如 numpy、pandas、python-docx、openpyxl、Pillow）；确需安装时，切换至非沙箱终端执行。

**3. Windows PowerShell 5.1 不支持 `ProcessStartInfo.ArgumentList`。** 拼接进程参数请使用 `$psi.Arguments`，或将逻辑写入 `.js` / `.py` 文件后以 `&` 调用。

**4. 个别残留文件可能带损坏 ACL 导致无法覆盖写入。** 表现为特定文件名始终写入失败。应对方式：删除该残留文件后重建即可，不影响主流程。

**5. 抽帧间隔的自适应规则需在批量对比时注意。** `extract_frames.py` 对时长超过 180 秒的素材自动将抽帧间隔放宽至 5 秒，180 秒及以下使用 2 秒。进行跨素材的「同帧数」对比实验时，需在脚本输出基础上自行进行二次均匀取样，以消除该自适应规则带来的样本量差异。

---

## 四、命令速查

```powershell
# 抽帧 + 元信息探测
python <skill>\scripts\extract_frames.py <video.mp4> [-f outdir] [--interval 2] [--split]

# 长素材场景切点拆条（scene 阈值 0.4，短于 10s 的片段并入相邻段落）
python <skill>\scripts\extract_frames.py <video.mp4> --split

# 平台页面下载（依赖 yt-dlp 在 PATH 中）
python <skill>\scripts\download_media.py "<url>" -o out

# 平台风控时的降级下载（移动端接口解析，脚本需按上述路径 3 实现）
$env:ELECTRON_RUN_AS_NODE='1'; & $env:DSH_NODE_EXECUTABLE "<dl.js>"
```

---

## 五、反馈与贡献

各环境中的新问题与验证过的解决方案，欢迎通过 Issue 或 Pull Request 反馈至本仓库，共同完善本指南。
