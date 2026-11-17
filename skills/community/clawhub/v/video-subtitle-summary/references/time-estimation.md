---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: '3eafd0b5-b672-4688-81a8-247d806d4d2b'
  PropagateID: '3eafd0b5-b672-4688-81a8-247d806d4d2b'
  ReservedCode1: 'bf3641d8-b15a-4653-9b22-8243713ff74c'
  ReservedCode2: 'bf3641d8-b15a-4653-9b22-8243713ff74c'
---

# Time Estimation

Estimate processing time before handling a video source. The skill is subtitle-only, so the estimate reflects only subtitle extraction and summarization. Treat the estimate as a range, not a promise.

## Required Estimate Message

Use this shape before extraction:

```text
预计处理耗时：{range}。依据：{source_type}，{duration_or_size}，预计字幕获取方式为 {acquisition_method}。主要不确定因素：{risk_factors}。
```

If duration is unknown:

```text
我还不知道视频时长，因此只能先给粗略估计：{range}。如果页面能读取到时长或你提供视频时长，我会更新估计。
```

## Baseline Ranges (subtitle-only)

- Existing local subtitle file (SRT/VTT/TXT/MD/JSON): 1-5 minutes to parse and summarize.
- Public video page with exposed subtitles: 2-8 minutes (page fetch + subtitle parse + summary).
- Browser-visible transcript panel: 2-10 minutes if the transcript is fully visible; longer if the page lazy-loads transcript chunks.
- Subtitle not exposed and user needs to provide a file: cannot estimate until the file arrives; output a "waiting for subtitle file" state instead of a numeric range.

## Source-Based Estimates

| Source / acquisition path | Estimated range |
|---|---|
| Local subtitle file | 1-5 minutes |
| Public page with exposed subtitles | 2-8 minutes |
| Browser-visible transcript panel | 2-10 minutes |
| Bilibili / public platform without exposed subtitles | N/A — ask user for subtitle file or switch source |
| Direct media / HLS link without subtitle tracks | N/A — ask user for subtitle file |
| Local video/audio file | N/A — skill does not transcribe audio; ask user for subtitle file |
| Subtitle file pending from user | waiting state until file received |

## Risk Factors to Mention

- Unknown duration or file size.
- Need for user login.
- No exposed subtitles (skill cannot fall back to audio).
- Slow or throttled network for page/subtitle fetch.
- Large, lazy-loaded, or paginated transcript panels.
- Multi-language subtitles or auto-generated captions with low accuracy.
- Dynamic player requiring interaction to reveal transcript.

## Output When Subtitles Are Unavailable

If the source does not expose subtitles, output a clear judgment instead of a numeric estimate:

```text
【判断结果】字幕可达性：not-accessible。本技能不做音频转写。建议：1) 提供 SRT/VTT 字幕文件；2) 换用有字幕的视频源；3) 在浏览器中打开页面让助手读取可见 transcript 面板。
```

## Optimization Rules

- Prefer already-exposed subtitles over asking the user to log in.
- Ask for existing subtitle files, transcript exports, or course handouts when online extraction is slow.
- For long videos, summarize the transcript in chunks and report progress after each chunk.
- If transcript chunks are lazy-loaded, paginate patiently rather than skipping content.