# 场景处理指南

当用户需求匹配以下场景时，参考对应的处理策略。

## 视频延长
用户说"把视频延长/续接 X 秒"：
- 写 `Extend @video1 by Xs`
- Duration 填新增段的时长，不是总时长
- 连续性指令：preserve identity, outfit, camera direction, lighting

## 角色替换
用户说"把视频里的人换成这个角色"：
- @video1 = 原始动作和镜头
- @image1 = 替换角色外观
- 保留编舞、时间节奏、转场

## 节拍同步
用户说"按音乐节拍剪辑"：
- @video/@audio 作为节奏参考
- 按时间段锁定节拍切换点

## 多段拼接（视频 > 15 秒）
单段上限 15 秒，超过时拆分：

1. 顶部声明总时长和分段数
2. 第 1 段正常生成（≤15s），结尾留干净交接帧
3. 第 2 段起：上传前段尾帧截图作为首帧
4. 每段末尾写交接帧描述
5. 连续性指令：preserve identity, outfit, lighting, camera style

人物一致性操作建议：
- 尾帧截图选角色面部清晰的帧，不要选背影或远景帧
- 如果某段角色偏差大，重新生成几次挑最接近的
- 可使用即梦"首尾帧"模式同时上传首帧和尾帧，一致性更好
- 段越短一致性越好，建议 10 秒一段优于 15 秒一段

## 对话短剧
- 画面、对话、音效分三层写
- 对话：`Dialogue (Name, emotion): "line"` — 每 3-5 秒一句
- 音效：`Sound: [描述]`
- 情绪标签：cold / desperate / cheerful / whispering / firm / sarcastic

## 旁白叙事
- 画面、旁白、音效分三层写
- 旁白：`Narration (emotion): "line"` — 每 3-5 秒一句
- 音效：`Sound: [描述]`
- 情绪标签：calm / tired / curious / determined / tense / urgent / reflective
- 旁白和画面的关键动作要标注同步点
- 旁白语言跟随用户指定（默认中文）

## 产品展示 / 电商广告
- @image1 = 产品照片（身份锚点）
- 常用技巧：360° 旋转、3D 爆炸视图、重组动画、英雄光
- 背景干净：纯色渐变 / 中性台面 / 场景化
- 指定材质：glass reflections, metallic sheen, matte finish, translucent glow

## 一镜到底
- @image1 = 首帧（主角/开场构图）
- 后续 @image = 场景路标
- prompt 写成连续镜头路径，按顺序经过路标
- 明确写 `no cuts, single continuous shot, one-take`
- 15 秒配 3-5 个路标效果最佳
