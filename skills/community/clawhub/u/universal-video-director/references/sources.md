# 借鉴来源与吸收点

| 上游 | 许可 | 吸收到 |
|---|---|---|
| zenstory-ai/drama-skills（short-drama、-storyboard、-video-prompts、-produce、-edit） | MIT | 总控和阶段拆分；连戏锁与锁定词；软门禁校验（只有确定性问题才算 ERROR）；先预览确认再花钱；任务 ID 落盘、audit/collect 续跑；GROUP 多镜合生；逐镜挂图计划；字幕逐字取自剧本 → 00/03/05/06/07/08 |
| eternityspring/shuohao-skills（novel-script、novel-storyboard 等） | Apache-2.0 | 按语速确定性估算时长；冷开场钩子门禁；逐角色台词本；segment ≤15s → cut 2–5s → 关键帧三级结构；正面全身锚点图；空镜白板图；参考图过期追踪；开场站位句原样复制 → 02/03/04/05 |
| HBAI-Ltd/Toonflow-app | MIT | 3D 白模预演思路（站位 xy 和机位站点）、按镜头 @ 引用资产 → 04/05 |
| browser-use/video-use | MIT | 以文本为主、按需取帧；剪辑点 30ms 淡化；EDL → 渲染 → 自评最多 3 次；会话记忆落盘 → 08/10 |
| kajisho5/ffmpeg-skill | MIT | 先 probe 再编辑再验证；类型化参数；不覆盖源文件；实测时长和响度 → 07/08 |
| heygen-com/hyperframes | Apache-2.0 | 用 HTML/GSAP 时间线做确定性渲染，作为 compose 后端可选项 → 08 |
| remotion-dev/skills | 无 LICENSE，待确认 | 只借鉴思路：程序化字幕和动效、按 composition 组织 → 08。未复制代码 |
| sanxsnr/ai-short-drama-from-zero | 见原仓库 | 阶段诊断；不可行时退回上游；统一导演机位方案；CUT 几何；180° 轴线；连续镜头机位重复检测 → 05/09/10 |
| rishabhsxn/claude-video-studio | MIT | 审美关卡；音频先行；frame-critic 的 8 项评分和硬性上限；先约定打磨上限 → 00/07/09/10 |

说明：以上都是对设计思路的重新实现，没有复制任何上游代码或提示词原文。
