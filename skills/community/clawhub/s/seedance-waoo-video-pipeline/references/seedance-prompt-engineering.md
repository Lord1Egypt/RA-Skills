# Seedance Prompt Engineering Overlay

> 来源抽取：`dandysuper/seedance-2-prompt-engineering-skill` 的可复用方法层。
> 本文件只保留“可并入执行流水线”的提示词工程规则，不改动当前 submit/poll/download 工程链路。

## 1) 模式先行（Mode First）

每次生成前先声明模式，再写 Prompt：

- Text-only
- First-Frame
- First+Last
- All-Reference

最小模板：

```text
Mode: <Text-only|First-Frame|First+Last|All-Reference>
Assets Mapping:
- @image1: <identity/first frame/character anchor>
- @video1: <camera language/rhythm>
- @audio1: <music pace/beat reference>
```

## 2) Assets Mapping（强约束）

所有引用素材必须明确“控制权”：

- 谁控制人物身份（identity anchor）
- 谁控制镜头语言（camera language）
- 谁控制节奏（rhythm）
- 谁仅作风格参考（style reference）

禁止模糊写法：
- ❌ “参考这几张图做一个酷视频”
- ✅ “@image1 锁人物，@video1 锁运镜节奏，@audio1 仅锁 BPM 氛围”

## 3) 时间轴分段（Timecoded Beats）

建议按段写，且每段只放一个主动作：

```text
0-3s: 动作A + 镜头A
3-7s: 动作B + 转场B
7-10s: 动作C + 结尾定格
```

长视频（>15s）规则：
- 分段生成 + 连续续写
- 每段结尾写“交接帧描述（handoff frame）”
- 下一段显式写：`Extend @video1 by Xs`

## 4) 负向约束（Negative Constraints）

需要干净画面时必须显式加：

- no watermark
- no logo
- no subtitles
- no on-screen text
- no deformed hands/faces（按需）

## 5) 严格剧本模式建议

当用户要求“按剧本锁定/严格按剧本”：

- 先锁连续性：人物一致 + 场景一致 + 运镜方向一致
- 再调风格细节（避免先堆特效导致角色飘）
- 对应工程参数口径：
  - `content`: `text + image_url(first_frame)`
  - 明确 `duration / resolution / generate_audio / camera_fixed / draft / seed / return_last_frame`

## 6) 审核/IP 风险规避（可选）

当提示词可能触发版权/审核问题时：

- 不使用已知 IP 名称、角色名、品牌名
- 改写为原创描述（外观/能力/材质）
- 增加显式排除词（negative list）

## 7) 场景化速用模板

### A. 商品广告
- 锁产品图为 @image1
- 强调 360°、材质高光、干净背景

### B. 短剧情节
- 视觉动作与对白分层写
- 每 3-5 秒一条短对白

### C. 音乐节拍型
- 用 @audio1 锁节奏
- beats 分段对齐镜头切换

### D. 一镜到底
- 多图作为路径路标（waypoints）
- 显式写：no cuts / one-take

## 8) 输出骨架（可直接复用）

```text
Mode: <...>
Assets Mapping:
- @image1: ...
- @video1: ...
- @audio1: ...

Final Prompt:
<ratio>, <duration>, <style>.
0-3s: ...
3-7s: ...
7-10s: ...
Preserve identity and scene continuity. Use coherent lighting and physically plausible motion.

Negative Constraints:
...

Generation Settings:
Duration: ...
Aspect Ratio: ...
```

## 9) 与现有流水线的集成点

- 进入 Phase 0.5（Prompt Engineering Overlay）后，先生成结构化 Prompt 草案。
- 再把草案映射回 panel context：
  - `videoPrompt`
  - `subtitleText`
  - mode-specific asset map
- 最后再走既有工程链：submit -> poll -> download。

---

该文件是“提示词工程层”，不是执行层。
执行可靠性仍以现有 workflow driver 与脚本链路为准。
