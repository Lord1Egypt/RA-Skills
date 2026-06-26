# Seedance 2.0 官方案例库

> 来源：EvoLinkAI/awesome-seedance-2-guide
> 持续收录优质案例，供 Anna 学习参考

---

## Case 1：连续动作 — 晒衣服 ✅

**类型：** Image-to-Video
**难度：** ⭐⭐

**用户输入：**
```
女孩在优雅的晒衣服，晒完接着在桶里拿出另一件，用力抖一抖衣服。
```

**参考图：** 1张女孩图片

**成功关键：**
- 连续动作描述清晰（晒→拿→抖）
- 提供了具体动作细节
- 场景简单，易于模型理解

**Prompt 优化版（加入镜头）：**
```
A girl elegantly hangs laundry from @image1, then reaches into the bucket to grab another piece, shaking it vigorously.
Camera slowly pulls back to reveal full yard setting, soft sunlight, gentle breeze.
```

---

## Case 2：创意叙事 — 可乐广告 ✅

**类型：** Reference-to-Video
**难度：** ⭐⭐⭐⭐

**用户输入：**
```
画里面的人物心虚的表情，眼睛左右看了看探出画框，快速的将手伸出画框拿起可乐喝了一口，
然后露出一脸满足的表情，这时传来脚步声，画中的人物赶紧将可乐放回原位，此时一位西部
牛仔拿起杯子里的可乐走了，最后镜头前推画面慢慢变得纯黑背景只有顶光照耀的罐装可乐，
画面最下方出现艺术感字幕和旁白："宜口可乐，不可不尝！"
```

**成功关键：**
- 完整的叙事弧线（偷喝→满足→被撞见→放回→拿走→特写）
- 镜头运动清晰（前推→纯黑背景）
- 有具体音效/字幕描述

**Prompt 优化版：**
```
The character in the painting has a guilty expression, eyes glancing left and right as they peek out of the frame, quickly reaching out to grab a cola and take a sip, then showing a satisfied expression.
Suddenly footsteps are heard, the character quickly puts the cola back in place.
A western cowboy picks up the cup with cola and walks away.
Finally, the camera pushes forward and the scene slowly becomes a pure black background with only top lighting illuminating the canned cola.
At the bottom of the frame, artistic subtitles and voiceover appear: "Yikou Cola, a must-try!"
```

---

## Case 3：复杂场景 — 19世纪伦敦 ✅

**类型：** Reference-to-Video
**难度：** ⭐⭐⭐⭐⭐

**用户输入：**
```
镜头小幅度拉远（露出街头全景）并跟随女主移动，风吹拂着女主的裙摆，女主走在19世纪的伦敦大街上；
女主走着走着右边街道驶来一辆蒸汽机车，快速驶过女主身旁，风将女主的裙摆吹起，
女主一脸震惊的赶忙用双手向下捂住裙摆；背景音效为走路声，人群声，汽车声等等
```

**成功关键：**
- 多主体（女主+蒸汽机车）
- 镜头运动复杂（拉远+跟随）
- 天气效果（风）影响角色（裙摆）
- 丰富的环境音效

**注意：** 此案例复杂度极高，对模型理解能力要求高，建议分段或简化

---

## Case 4：追逐动作 — 黑衣男逃亡 ✅

**类型：** Reference-to-Video
**难度：** ⭐⭐⭐⭐

**用户输入：**
```
镜头跟随黑衣男子快速逃亡，后面一群人在追，镜头转为侧面跟拍，人物惊慌撞倒路边的水果摊爬起来继续逃，人群慌乱的声音。
```

**成功关键：**
- 镜头类型转换（跟拍→侧拍）
- 连续动作（跑→撞→爬→继续跑）
- 环境互动（撞倒水果摊）
- 音效配合（慌乱声音）

**Prompt 优化版：**
```
Camera follows the man in black as he flees rapidly, with a group of people chasing behind.
Camera switches to side tracking shot.
The character panics and knocks over a fruit stand, gets up and continues fleeing.
Chaotic crowd sounds, footsteps, scattered fruit on the ground.
```

---

## Case 5：产品展示（参考用）

**类型：** Image-to-Video / Reference-to-Video
**难度：** ⭐⭐⭐

**适合：** 电商、品牌、产品宣传

**模板 Prompt：**
```
@image1 as the main product, on a clean minimalist background.
Camera slowly orbits around the product, showcasing all angles.
[产品材质/光泽/细节] clearly visible under soft studio lighting.
Subtle reflection on the surface, premium feel.
[Optional: add relevant environment: on a marble surface / in a lifestyle setting]
```

---

## Case 6：转场动画

**类型：** Reference-to-Video
**难度：** ⭐⭐⭐

**适合：** 图文到视频的转换、回忆场景

**模板 Prompt：**
```
The image from @image1 slowly transitions into a live-action scene.
[主体] begins to move, [initial action].
Camera [movement type], revealing [new element].
The transition from illustration to reality is seamless.
Background [setting description], atmospheric lighting.
```

---

## 案例质量评估维度

| 维度 | 说明 |
|------|------|
| **动作清晰度** | 每个动作是否有具体描述（谁/做什么/怎么做） |
| **镜头语言** | 是否包含镜头运动（推/拉/移/跟/环绕） |
| **时间轴** | 长视频是否有分段（0-3s / 3-6s...） |
| **音效配合** | 是否有音效/音乐/配音描述 |
| **复杂度** | 单镜头 vs 多镜头、多主体 vs 单主体 |

---

## Anna 从案例中学到的规律

1. **镜头必须参考视频**：纯文字描述镜头效果不稳定，通过 @video 参考效果更好
2. **动作要具体化**："Sad" → "tears slide down cheeks, mouth trembles"
3. **连续动作是 Seedance 强项**：晒衣服/追逐/广告叙事都是它的擅长场景
4. **场景不要太复杂**：多主体+多镜头+多音效对模型压力大
5. **结尾加 No scene cuts**：确保生成连续镜头而非切镜

---

*此案例库由 Anna 整理 · 持续更新*
