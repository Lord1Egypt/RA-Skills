"""Content Engine — 跨平台内容拆解工具包。

零外部依赖（只用 Python stdlib + 系统命令 ffmpeg）。

**v1 仅支持小红书**。后续阶段（v1.1+）会在本包内新增 douyin / shipinhao 等
子模块，复用同一架构（client / parsers / linkresolve / video / images）。

模块（XHS v1）：
- models     : NoteData / Comment / Keyword dataclass
- client     : TikhubClient（urllib 包装 + 多源 token 解析）
- parsers    : 把 XHS API JSON 转成 dataclass + 评论关键词分类
- linkresolve: XHS 短链 / 长链 / 口令 → note_id
- video      : 流式下载 mp4 + ffmpeg 抽帧（平台无关）
- images     : 并发下载图文笔记的图片（平台无关）
- preflight  : 环境自检（Python / ffmpeg / token / 网络 / 工作区）
"""

__version__ = "0.1.0"
