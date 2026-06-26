# 模式与交互说明（即梦 Seedance 2.0）

## 模式选择

### 1) 首帧/尾帧模式
用户只提供首帧图（或首帧+尾帧）加文字提示词时使用。

推荐写法：
- `Use @image1 as first frame.`
- `End near @image2 composition.`

### 2) 纯文本模式
无参考素材时使用。提示词必须包含所有视觉指导。

推荐写法：
- 开头声明画幅、时长、帧率和风格。
- 用完全原创的名字和独特特征描述角色/生物。
- 所有动作使用时间码节拍。
- 特别适合 IP 安全的原创概念（无参考图时）。

### 3) 全素材引用模式
使用图片/视频/音频/文本进行多模态控制时使用。

推荐写法：
- `@image1 for character design consistency`
- `@video1 for camera language and transition rhythm`
- `@audio1 for pacing and atmosphere`

## @Asset 调用模式

始终在提示词正文前映射素材，减少错误：

```text
Assets Mapping:
- @image1 = first frame
- @image2 = environment style
- @video1 = motion + camera reference
- @audio1 = music rhythm
```

## 可利用的控制优势

Seedance 2.0 擅长：
- 从参考视频复制运动/镜头语言
- 通过图片参考保持角色和风格一致性
- 平滑延长/续接已有片段
- 对已有视频进行定向编辑（替换/添加/移除元素）
- 音乐节拍同步和情绪节奏
- 360° 产品旋转和 3D 爆炸视图动画
- 使用多图路标的一镜到底连续跟拍
- 超过 15 秒的多段拼接

## 对话与音效设计

当提示词包含角色台词或音效时，与画面指导**分层**写：

```text
0-5s: [画面动作和镜头]
Dialogue (角色名, 情绪): "台词"
Sound: [环境/音效描述]
```

最佳实践：
- 每 3-5 秒最多一句对话。
- 明确标注情绪：`cold`、`desperate`、`cheerful`、`whispering`。
- 音效单独描述：footsteps、ambient hum、score swell、silence。
- 结尾用音频收束：`score fades`、`ambient wind`、`silence`。

## 多段工作流（>15 秒）

超过 15 秒的视频：

1. 顶部声明**总时长**和**分段数**。
2. 每段是独立的提示词（每段最长 15 秒）。
3. 第 1 段：正常生成。结尾留**干净交接帧**。
4. 第 2 段起：上传前段输出为 `@video1`，使用 `Extend @video1 by Xs`。
5. 每段末尾包含**交接帧描述**。
6. 延续：identity、outfit、lighting、camera style、scene continuity。

## 一镜到底 / 连续镜头技巧

无剪辑的跟拍镜头：
- `@image1` 作为首帧（主角/开场构图）。
- 额外 `@image` 作为**场景路标** — 镜头经过的地点、角色或道具。
- 提示词写成连续镜头路径，按顺序经过每个路标。
- 明确写：`no cuts, single continuous shot, one-take`。
- 15 秒配 3-5 个路标效果最佳。

## 产品展示技巧

- 产品照片绑定到 `@image1` 作为身份锚点。
- 技巧：**360° 旋转**、**3D 爆炸视图**、**重组卡扣**、**英雄光**。
- 指定材质渲染：`glass reflections`、`metallic sheen`、`matte finish`、`translucent glow`。
- 背景保持干净：纯色渐变、中性台面或场景化。
- 灯光词汇参考 `camera-and-styles.md`。

## 常见陷阱

- 上传过多文件但未明确各自角色
- 缺少 identity/wardrobe/props 的连续性指令
- 混淆最终总时长与延长段时长
- 使用可能被审核拦截的真实人脸参考
- 使用品牌名、角色名或品牌相关词汇（触发审核拒绝）
- 描述标志性特征过于接近原始 IP（如 "yellow lightning mouse"、"red-gold armor with chest reactor"）
- 保留参考图中的品牌 logo 或商标未明确去除
- 未在负面约束中列出可推断的品牌引用

## 快速验证清单

- [ ] 文件数量和大小在限制内
- [ ] 混合文件总数 ≤ 12
- [ ] 时长在 4-15 秒之间
- [ ] 每个参考素材有明确的 `@asset` 角色
- [ ] 提示词有清晰的时间轴节拍
- [ ] 需要时包含负面约束
- [ ] 无品牌名、角色名或品牌词
- [ ] 负面约束明确列出所有可推断的 IP 引用
- [ ] 角色/生物使用完全原创的名字和独特视觉特征
- [ ] 对话和音效与画面动作分层写
- [ ] 多段视频有明确的交接帧描述
- [ ] 镜头术语匹配 `camera-and-styles.md` 词汇表
