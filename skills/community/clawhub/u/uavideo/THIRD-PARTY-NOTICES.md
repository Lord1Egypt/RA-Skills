# 第三方组件声明

本技能的 Python 脚本依赖以下外部工具，均由使用者在运行环境中自行安装，本技能不以任何形式分发或捆绑其代码或二进制：

| 组件 | 用途 | 许可证 | 许可协议 |
|---|---|---|---|
| curl | 直链素材下载（`scripts/download_media.py`） | curl license（MIT 派生） | https://curl.se/docs/copyright.html |
| ffmpeg / ffprobe | m3u8 合流、抽帧、场景拆条（`scripts/download_media.py`、`scripts/extract_frames.py`） | LGPL-2.1-or-later / GPL（取决于编译选项） | https://www.ffmpeg.org/legal.html |
| yt-dlp | 平台页面链接素材下载（`scripts/download_media.py`，可选依赖） | Unlicense（公有领域） | https://github.com/yt-dlp/yt-dlp/blob/master/LICENSE |
| imageio-ffmpeg | ffprobe/ffmpeg 不在 PATH 时的备选二进制来源（`scripts/extract_frames.py`，可选依赖） | BSD-2-Clause | https://github.com/imageio/imageio-ffmpeg/blob/master/LICENSE |

## 兼容性说明

- 本技能主体代码以 Apache-2.0 发布。Apache-2.0 与上述各组件许可证（MIT 类、Unlicense 公有领域、BSD 类）均兼容，作为「聚合作品」（aggregate/collected work）引用运行时外部程序不产生传染义务，各组件保留其原始许可即可。
- ffmpeg 的默认构建在多数发行版为 LGPL；若使用者自编译并启用 GPL 组件，则 ffmpeg 按 GPL 分发，但仍为独立运行的命令行程序，通过 `subprocess` 参数列表调用（无链接、无源码合并），不影响本技能代码的 Apache-2.0 许可状态。
- imageio-ffmpeg 仅作为可选的本地二进制查找备选，未启用时不需要安装。

## 使用注意事项

- `yt-dlp` 下载平台页面内容时，请遵守对应平台的服务条款与当地法律法规，仅下载您有权获取和使用的素材；因违规使用产生的责任由使用者自行承担。
- 本技能脚本通过参数列表调用外部程序（无 `shell=True`），不拼接不可信字符串到命令行；请勿修改脚本以从网络加载或执行任何载荷。
