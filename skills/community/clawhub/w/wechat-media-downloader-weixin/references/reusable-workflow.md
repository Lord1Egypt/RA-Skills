# WeChat 公众号媒体下载复用流程

## 最稳成功路径

1. 用户提供 mp.weixin.qq.com 文章链接。
2. 先尝试普通抓取；若页面返回“环境异常 / 去验证”，不要继续硬爬。
3. 安装最小工具：
   - `python3 -m pip install --user playwright yt-dlp`
4. 让用户打开可见 Chrome：
   ```bash
   google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/openclaw-wechat-debug
   ```
5. 让用户在 Chrome 内：
   - 打开文章
   - 完成验证/登录
   - 确认文章能正常显示媒体
6. 运行抓取脚本：
   ```bash
   python3 scripts/capture_wechat_media.py '<URL>' --out /tmp/wechat_media
   ```
7. 如果只抓到视频、没抓到音频：
   - 让用户把每个音频都点一次播放
   - 再跑一次抓取脚本
8. 从 `manual_page.html` 中提取：
   - `voice_encode_fileid`
   - `<mp-common-mpaudio ... name="...">`
9. 下载：
   - 视频：使用抓到的 `mpvideo.qpic.cn` 直链
   - 音频：`https://res.wx.qq.com/voice/getvoice?mediaid=<voice_encode_fileid>`
10. 按文章顺序重命名、移动到最终目录。

## 关键判断

- **反爬判断**：若 HTML 标题/正文出现“环境异常”“去验证”，说明要走人工验证路线。
- **CDP 连接判断**：如果直接连 `http://127.0.0.1:9222` 报 400，先请求 `/json/version`，取 `webSocketDebuggerUrl` 再连接。
- **音频未出现判断**：音频常常只有点击播放后才会发真实请求。

## 清理原则

- 可以清理：临时 HTML、JSON、脚本输出、`.part` 文件、乱码副本。
- 不要默认删除：最终交付文件夹。
- 涉及删除时，最好先说明会删什么。
