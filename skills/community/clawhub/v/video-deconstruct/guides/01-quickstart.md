# 5 分钟跑通 video-deconstruct

## 1. 装依赖

```bash
cd video-deconstruct/
pip install -r requirements.txt

# v2.0 起需要 ffmpeg：超过 128MB 时的压缩兜底 + ASR 抽音轨都靠它
brew install ffmpeg     # macOS
# apt install ffmpeg   # Linux
```

## 2. 拿 StepFun API key

去 [https://platform.stepfun.com](https://platform.stepfun.com) 注册 → 控制台 → API Keys → 新建 → 复制

```bash
export STEP_API_KEY=5g0AsLMZzGGQUacQJ2JfMNpDlITeYSMbOr8QXJUIke5nUW3TrT7T7nJ5oYhsbyUFi
```

> 想永久生效就写到 `~/.zshrc` 里。

## 3. 跑你的第一段视频

```bash
# 仅视觉（v1 兼容模式）
python scripts/analyze.py /path/to/your-video.mp4

# 推荐：开启 ASR，把对白文本一起喂给视觉模型
python scripts/analyze.py /path/to/your-video.mp4 --with-asr
```

执行流程会打印：

```
🎤 抽音轨 + 跑 stepaudio-2.5-asr ...
   ✅ ASR 转录 412 字：'帅哥加个微信...好巧啊...你怎么来了...'
📤 上传视频到 StepFun: your-video.mp4 (3.2MB)
   file_id = file-AbCdEfGh12
🤖 调 step-1o-turbo-vision 拆解中 (附 ASR 对白)...
📝 渲染报告...
✅ 报告: ./output/your-video-report.md
📜 ASR 转录: ./output/your-video-transcript.txt
🧹 已清理云端文件: file-AbCdEfGh12
```

## 5. 看报告

打开 `output/your-video-report.md`，10 个章节全部就位（评论区在 v1 里是占位）。
原始 JSON 在同目录的 `your-video-analysis.json`。

## 常见问题

**Q：报错 `STEP_API_KEY 未设置`**
A：见步骤 2。

**Q：报错 `文件 xxxMB 超过 128MB 上限`**
A：先压一下（需要本机装 ffmpeg，skill 本身不依赖）：`ffmpeg -i big.mp4 -vcodec libx264 -crf 28 -preset fast small.mp4`

**Q：报错 `只支持 mp4`**
A：先转一下：`ffmpeg -i in.mov out.mp4`。StepFun 的文件 API 只接受 mp4。

**Q：想保留云端文件不被自动删除**
A：加 `--keep-upload` 参数。适用于想重复分析同一段视频不同 prompt 的情况。

**Q：上传卡住**
A：默认上传超时 10 分钟。128MB 视频在一般网速下 1-3 分钟应该能传完。如果卡更久，检查网络或把文件压小一点。
