# 子技能 07 · 确认后生产 production
**来源**：drama-skills short-drama-produce（先批量预览、明确确认后再调用接口；任务 ID 立即落盘；audit / collect 断点续跑；密钥放在项目外），claude-video-studio（音频先行），Toonflow 和 hyperframes 的多模型接入。

## 目标
在花钱可控的前提下拿到所有素材，中途断了也能接着跑。

## 方法
1. **plan**：为每个参考图、首帧、motion、台词、配乐建一个 task，状态为 `planned`。同时算出 estimate（数量和预估费用）。
2. **预览确认**：把任务清单（数量、内容、参考图、参数、费用）展示给用户。用户明确确认后，写 `confirmed:true` 和确认时间。
3. **静帧段**：只排 image 任务（ref 填 cut_id），不排 video 任务；排了会报 STILL_HAS_VIDEO 警告。
4. **执行顺序**：
   - 先出音频：TTS 和配乐。台词的实际时长要回填，如果超过对应 beat 的时长，回到 02 或 05 调整
   - 再出参考图和首帧
   - 最后出视频
4. **断点续跑**：任务一提交，就把 task_id 写进文件。中断后先 audit，找出 submitted 但还没完成的任务，再 collect 取回结果。只有确认平台那边确实失败了，才重新提交。
5. **失败处理**：同一个任务换 seed 最多重试 2 次。还失败就标 `failed`，交给评审阶段，由修复环节回到 06 或 05 去改。
6. **回填**：output 写文件路径，actual_duration_sec 用 ffprobe 实测。
7. **失效**：上游一变（用 stale 检测），相关任务就标 `stale`。

## 常见错误码
SPEND_WITHOUT_CONFIRM、OVER_BUDGET、NO_TASK_ID、TASK_FAILED、CLIP_DURATION、FILE_MISSING
