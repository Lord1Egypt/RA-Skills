# 微信视频下载器 (WeChat Video Downloader)

从微信公众号文章中自动提取并下载嵌入的视频文件。

## ✨ 功能特点

- 🎯 **自动识别** - 智能定位文章中的视频播放器
- 🚀 **一键下载** - 自动提取真实视频 URL 并下载
- 🔓 **绕过验证** - 处理微信的 Referer 验证机制
- 📦 **开箱即用** - 基于 OpenClaw 平台，无需复杂配置

## 📋 前置要求

- Python 3.6+
- [OpenClaw](https://github.com/openclaw/openclaw) CLI 工具
- curl 命令

## 🚀 快速开始

### 1. 安装 OpenClaw

如果尚未安装 OpenClaw，请参考官方文档：
https://docs.openclaw.ai

### 2. 使用脚本下载视频

```bash
# 基本用法
python scripts/download_wechat_video.py <文章 URL>

# 指定输出文件名
python scripts/download_wechat_video.py <文章 URL> 我的视频.mp4
```

### 3. 示例

```bash
# 下载公众号文章中的视频
python scripts/download_wechat_video.py https://mp.weixin.qq.com/s/zCrty8DIPBwm0nxg1s07iA

# 保存为指定文件名
python scripts/download_wechat_video.py https://mp.weixin.qq.com/s/xxx 教学视频.mp4
```

## 💡 使用场景

- 下载微信公众号中的教学视频
- 保存讲座、课程录像
- 离线观看喜欢的内容
- 视频内容归档

## 🔧 工作原理

1. **打开页面** - 使用 OpenClaw browser 工具加载公众号文章
2. **定位视频** - 通过页面快照查找视频播放按钮
3. **触发加载** - 点击播放按钮使视频元素加载
4. **提取 URL** - 通过 JavaScript 获取 `<video>` 元素的真实源地址
5. **下载文件** - 使用 curl 添加正确的请求头下载视频
6. **清理资源** - 关闭浏览器标签页

## 📁 项目结构

```
wechat-video-downloader/
├── README.md                    # 项目说明
├── LICENSE                      # MIT 许可证
├── SKILL.md                     # OpenClaw 技能定义
└── scripts/
    └── download_wechat_video.py # 主下载脚本
```

## ⚠️ 注意事项

1. **视频时效性** - 提取的 URL 包含时效性 token，需立即使用
2. **文件大小** - 视频通常较大（100MB-1GB），确保有足够存储空间
3. **网络环境** - 需要稳定的网络连接
4. **版权尊重** - 仅下载用于个人学习或已获授权的内容

## 🐛 故障排查

| 问题 | 解决方案 |
|------|----------|
| 403 Forbidden | 脚本已自动处理，确保使用最新版本 |
| 找不到视频 | 确认文章包含视频（有些只有图片） |
| 下载的文件为空 | URL 可能过期，重试即可 |
| 脚本无响应 | 确保 OpenClaw browser 已启动 |

## 📝 支持的 video 类型

- ✅ 微信公众号内置视频（mpvideo.qpic.cn）
- ✅ 腾讯视频嵌入（v.qq.com）
- ⚠️ 其他第三方平台（可能需要额外配置）

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 🔗 相关链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [ClawHub 技能市场](https://clawhub.ai)

---

**Made with ❤️ for OpenClaw Community**
