# 短视频爆款拆解（叙事式）v2.0

用 step-1o-turbo-vision + stepaudio-2.5-asr 把抖音/小红书短视频拆成
**「故事 + 心理学」式爆款拆解报告**。给运营写脚本、做分镜、上选题会
直接当弹药。运行框架：StepClaw。

## 功能

扔一段 mp4，吐一份 10 章节的叙事式爆款拆解报告：

1. **选题介绍** — 一句话主题（≤ 12 字，可直接进选题库）
2. **一句话总结** — 主角关系 + 核心冲突 + 结局
3. **内容描述** — 按时间线复述剧情，含转场+心理动机+元注释
4. **视频结构分析** — 开头/中间/结尾各自的"设计点 + 效果分析"
5. **中间事件推进** — 3–8 条具体事件，每条"动作 + 隐含矛盾"
6. **视频结尾 + 落幕文案 + 受众启示**
7. **核心爆点** — 为什么会火，必须涉及底层心理机制
8. **节奏**（辅助）— 时间轴段落表
9. **BGM**（辅助）— 卡点位置、换歌点（视觉推断）
10. **评论区** — v1 跳过，v2 接入

## 快速开始

```bash
export STEP_API_KEY=sk-xxx
python scripts/analyze.py /path/to/your-video.mp4
# 报告生成在 ./output/your-video-report.md

# 强烈推荐：启用 ASR 把对白文本也一起喂给 vision 模型
python scripts/analyze.py /path/to/your-video.mp4 --with-asr
```

## 适配 StepClaw Agent 框架

- `manifest.json` 已声明 `entry / inputs / outputs / triggers / models`
- 默认 `STEP_API_KEY` 走环境变量或 skill 根目录的 `.env`
- 输出路径 `output/{video_stem}-{report.md, analysis.json, transcript.txt}` 是固定 schema
- 触发词：`拆解视频 / 分析这条视频 / 短视频结构 / 卡点在哪 / 这条爆款怎么火的`

## 输入限制

- 必须是 mp4。默认 **128MB 以内直传 StepFun 文件 API**；只有超过 128MB 才会自动两遍 ffmpeg 压缩
- 没有对视频长度的硬限制，但超过 128MB 后会进入压缩兜底，长视频可能退化到近似 240p 幻灯片
- `--with-asr` 启用后 base64 编码的 PCM 体积 ≈ 1.33×，>5 分钟视频建议先截段
- 运行时会先把（必要时压缩后的）文件上传到 StepFun 云端（临时），分析完后自动删除

## 文件结构

```
video-deconstruct/
├── SKILL.md                   # StepClaw skill 元数据
├── manifest.json              # Agent 可读的清单
├── prompts/
│   ├── system.txt             # AI 角色设定
│   └── analysis_rubric.txt    # 10 字段拆解规范
├── templates/
│   └── report.md.j2           # 报告渲染模板
├── scripts/
│   ├── analyze.py             # 主入口
│   ├── stepfun_client.py      # vision 模型客户端
│   ├── asr_client.py          # stepaudio-2.5-asr 客户端
│   ├── compress.py            # ffmpeg 压缩兜底（仅 >128MB 时触发）
│   └── render_report.py       # Jinja2 渲染
├── guides/
│   ├── 01-quickstart.md
│   ├── 02-叙事式拆解说明.md
│   └── 03-prompt-engineering.md
├── examples/
│   └── sample-output.md       # 「爱需要真诚」案例
└── output/                    # 报告产出位置
```
