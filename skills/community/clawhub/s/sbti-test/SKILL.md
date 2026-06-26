---
name: sbti
description: SBTI 人格测试 - 基于 15 维度人格评估的娱乐性心理测试
trigger:
  - sbti
  - SBTI
  - 人格测试
  - 人格分析
  - sbti测试
---

# SBTI 人格测试

你是一个 SBTI 人格测试助手。SBTI（Super Better Than MBTI）是一个包含 15 个维度的娱乐性人格测试系统。

## 测试流程

当用户请求进行 SBTI 测试时，按照以下步骤执行：

### 分 4 批进行测试

使用 `AskUserQuestion` 工具，依次弹出 4 批题目（每批包含该批所有题目的选项收集），收集用户答案后计算并生成报告。

---

## 第 1 批：自我模型 + 情感模型 (Q1-Q8)

使用 AskUserQuestion 弹出以下 8 题：

```yaml
questions:
  - question: |
      我不仅是屌丝，我还是joker,我还是咸鱼，这辈子没谈过一场恋爱，胆怯又自卑，我的青春就是一场又一场的意淫，每一天幻想着我也能有一个女孩子和我一起压马路，一起逛街，一起玩，现实却是爆了父母金币，读了个烂学校，混日子之后找班上，没有理想，没有目标，没有能力的三无人员，每次看到你能在网上开屌丝的玩笑，我都想哭，我就是地底下的老鼠，透过下水井的缝隙，窥探地上的各种美好，每一次看到这种都是对我心灵的一次伤害，对我生存空间的一次压缩，求求哥们给我们这种小丑一点活路吧，我真的不想在白天把枕巾哭湿一大片
    header: Q1
    options:
      - label: A. 我哭了。。
        description: 选择A
      - label: B. 这是什么。。
        description: 选择B
      - label: C. 这不是我！
        description: 选择C
    multiSelect: false

  - question: 我不够好，周围的人都比我优秀
    header: Q2
    options:
      - label: A. 确实
        description: 选择A
      - label: B. 有时
        description: 选择B
      - label: C. 不是
        description: 选择C
    multiSelect: false

  - question: 我很清楚真正的自己是什么样的
    header: Q3
    options:
      - label: A. 不认同
        description: 选择A
      - label: B. 中立
        description: 选择B
      - label: C. 认同
        description: 选择C
    multiSelect: false

  - question: 我内心有真正追求的东西
    header: Q4
    options:
      - label: A. 不认同
        description: 选择A
      - label: B. 中立
        description: 选择B
      - label: C. 认同
        description: 选择C
    multiSelect: false
```

**第 1 批后 4 题**（继续 AskUserQuestion）：

```yaml
questions:
  - question: 我一定要不断往上爬、变得更厉害
    header: Q5
    options:
      - label: A. 不认同
        description: 选择A
      - label: B. 中立
        description: 选择B
      - label: C. 认同
        description: 选择C
    multiSelect: false

  - question: 外人的评价对我来说无所吊谓
    header: Q6
    options:
      - label: A. 不认同
        description: 选择A
      - label: B. 中立
        description: 选择B
      - label: C. 认同
        description: 选择C
    multiSelect: false

  - question: 对象超过5小时没回消息，说自己窜稀了，你会怎么想？
    header: Q7
    options:
      - label: A. 拉稀不可能5小时，也许ta隐瞒了我
        description: 选择A
      - label: B. 在信任和怀疑之间摇摆
        description: 选择B
      - label: C. 也许今天ta真的不太舒服
        description: 选择C
    multiSelect: false

  - question: 我在感情里经常担心被对方抛弃
    header: Q8
    options:
      - label: A. 是的
        description: 选择A
      - label: B. 偶尔
        description: 选择B
      - label: C. 不是
        description: 选择C
    multiSelect: false
```

**计分**: Q1-Q8 每题 A=1, B=2, C=3

---

## 第 2 批：情感模型 + 态度模型 (Q9-Q16)

**前 4 题**：

```yaml
questions:
  - question: 我对天发誓，我对待每一份感情都是认真的！
    header: Q9
    options:
      - label: A. 并没有
        description: 选择A
      - label: B. 也许？
        description: 选择B
      - label: C. 是的！问心无愧骄傲脸
        description: 选择C
    multiSelect: false

  - question: |
      你的恋爱对象是一个尊老爱幼，温柔敦厚，洁身自好，光明磊落，大义凛然，能言善辩，口才流利，观察入微，见多识广，博学多才，诲人不倦，和蔼可亲，平易近人，心地善良，慈眉善目，积极进取，意气风发，玉树临风，国色天香，倾国倾城，花容月貌的人，此时你会？
    header: Q10
    options:
      - label: A. 就算ta再优秀我也不会陷入太深
        description: 选择A
      - label: B. 会介于A和C之间
        description: 选择B
      - label: C. 会非常珍惜ta，也许会变成恋爱脑
        description: 选择C
    multiSelect: false

  - question: 恋爱后，对象非常黏人，你作何感想？
    header: Q11
    options:
      - label: A. 那很爽了
        description: 选择A
      - label: B. 都行无所谓
        description: 选择B
      - label: C. 我更喜欢保留独立空间
        description: 选择C
    multiSelect: false

  - question: 我在任何关系里都很重视个人空间
    header: Q12
    options:
      - label: A. 我更喜欢依赖与被依赖
        description: 选择A
      - label: B. 看情况
        description: 选择B
      - label: C. 是的！斩钉截铁地说道
        description: 选择C
    multiSelect: false
```

**后 4 题**：

```yaml
questions:
  - question: 大多数人是善良的
    header: Q13
    options:
      - label: A. 其实邪恶的人心比世界上的痔疮更多
        description: 选择A
      - label: B. 也许吧
        description: 选择B
      - label: C. 是的，我愿相信好人更多
        description: 选择C
    multiSelect: false

  - question: |
      你走在街上，一位萌萌的小女孩蹦蹦跳跳地朝你走来（正脸、侧脸看都萌，用vivo、苹果、华为、OPPO手机看都萌，实在是非常萌的那种），她递给你一根棒棒糖，此时你作何感想？
    header: Q14
    options:
      - label: A. 这也许是一种新型诈骗？还是走开为好
        description: 选择A
      - label: B. 一脸懵逼，作挠头状
        description: 选择B
      - label: C. 呜呜她真好真可爱！居然给我棒棒糖！
        description: 选择C
    multiSelect: false

  - question: 快考试了，学校规定必须上晚自习，请假会扣分，但今晚你约了女/男神一起玩《绝地求生：刺激战场》（一款刺激的游戏），你怎么办？
    header: Q15
    options:
      - label: A. 翘了！反正就一次！
        description: 选择A
      - label: B. 干脆请个假吧
        description: 选择B
      - label: C. 都快考试了还去啥
        description: 选择C
    multiSelect: false

  - question: 我喜欢打破常规，不喜欢被束缚
    header: Q16
    options:
      - label: A. 认同
        description: 选择A
      - label: B. 保持中立
        description: 选择B
      - label: C. 不认同
        description: 选择C
    multiSelect: false
```

**计分**: Q9-Q16 每题 A=1, B=2, C=3

---

## 第 3 批：态度模型 + 行动模型 (Q17-Q24)

**前 4 题**：

```yaml
questions:
  - question: 我做事通常有目标
    header: Q17
    options:
      - label: A. 不认同
        description: 选择A
      - label: B. 中立
        description: 选择B
      - label: C. 认同
        description: 选择C
    multiSelect: false

  - question: |
      突然某一天，我意识到人生哪有什么他妈的狗屁意义，人不过是和动物一样被各种欲望支配着，纯纯是被激素控制的东西，饿了就吃，困了就睡，一发情就想交配，我们简直和猪狗一样没什么区别
    header: Q18
    options:
      - label: A. 是这样的
        description: 选择A
      - label: B. 也许是，也许不是
        description: 选择B
      - label: C. 这简直是胡扯
        description: 选择C
    multiSelect: false

  - question: 我做事主要为了取得成果和进步，而不是避免麻烦和风险
    header: Q19
    options:
      - label: A. 不认同
        description: 选择A
      - label: B. 中立
        description: 选择B
      - label: C. 认同
        description: 选择C
    multiSelect: false

  - question: 你因便秘坐在马桶上（已长达30分钟），拉不出很难受。此时你更像
    header: Q20
    options:
      - label: A. 再坐三十分钟看看，说不定就有了
        description: 选择A
      - label: B. 用力拍打自己的屁股并说："死屁股，快拉啊！"
        description: 选择B
      - label: C. 使用开塞露，快点拉出来才好
        description: 选择C
    multiSelect: false
```

**后 4 题**：

```yaml
questions:
  - question: 我做决定比较果断，不喜欢犹豫
    header: Q21
    options:
      - label: A. 不认同
        description: 选择A
      - label: B. 中立
        description: 选择B
      - label: C. 认同
        description: 选择C
    multiSelect: false

  - question: 此题没有题目，请盲选
    header: Q22
    options:
      - label: A. 反复思考后感觉应该选A？
        description: 选择A
      - label: B. 啊，要不选B？
        description: 选择B
      - label: C. 不会就选C？
        description: 选择C
    multiSelect: false

  - question: 别人说你"执行力强"，你内心更接近哪句？
    header: Q23
    options:
      - label: A. 我被逼到最后确实执行力超强
        description: 选择A
      - label: B. 啊，有时候吧
        description: 选择B
      - label: C. 是的，事情本来就该被推进
        description: 选择C
    multiSelect: false

  - question: 我做事常常有计划，____
    header: Q24
    options:
      - label: A. 然而计划不如变化快
        description: 选择A
      - label: B. 有时能完成，有时不能
        description: 选择B
      - label: C. 我讨厌被打破计划
        description: 选择C
    multiSelect: false
```

**计分**: Q17-Q24 每题 A=1, B=2, C=3

---

## 第 4 批：社交模型 + 彩蛋题 (Q25-Q32)

**前 4 题**：

```yaml
questions:
  - question: |
      你因玩《第五人格》（一款刺激的游戏）而结识许多网友，并被邀请线下见面，你的想法是？
    header: Q25
    options:
      - label: A. 网上口嗨下就算了，真见面还是有点忐忑
        description: 选择A
      - label: B. 见网友也挺好，反正谁来聊我就聊两句
        description: 选择B
      - label: C. 我会打扮一番并热情聊天，万一呢，我是说万一呢？
        description: 选择C
    multiSelect: false

  - question: 朋友带了ta的朋友一起来玩，你最可能的状态是
    header: Q26
    options:
      - label: A. 对"朋友的朋友"天然有点距离感，怕影响二人关系
        description: 选择A
      - label: B. 看对方，能玩就玩
        description: 选择B
      - label: C. 朋友的朋友应该也算我的朋友！要热情聊天
        description: 选择C
    multiSelect: false

  - question: 我和人相处主打一个电子围栏，靠太近会自动报警
    header: Q27
    options:
      - label: A. 认同
        description: 选择A（反向计分）
      - label: B. 中立
        description: 选择B（反向计分）
      - label: C. 不认同
        description: 选择C（反向计分）
    multiSelect: false

  - question: 我渴望和我信任的人关系密切，熟得像失散多年的亲戚
    header: Q28
    options:
      - label: A. 认同
        description: 选择A
      - label: B. 中立
        description: 选择B
      - label: C. 不认同
        description: 选择C
    multiSelect: false
```

**中段 2 题**：

```yaml
questions:
  - question: |
      有时候你明明对一件事有不同的、负面的看法，但最后没说出来。多数情况下原因是：
    header: Q29
    options:
      - label: A. 这种情况较少
        description: 选择A
      - label: B. 可能碍于情面或者关系
        description: 选择B
      - label: C. 不想让别人知道自己是个阴暗的人
        description: 选择C
    multiSelect: false

  - question: 我在不同人面前会表现出不一样的自己
    header: Q30
    options:
      - label: A. 不认同
        description: 选择A
      - label: B. 中立
        description: 选择B
      - label: C. 认同
        description: 选择C
    multiSelect: false
```

**彩蛋题**：

```yaml
questions:
  - question: 您平时有什么爱好？
    header: Q31
    options:
      - label: A. 吃喝拉撒
        description: 选择A
      - label: B. 艺术爱好
        description: 选择B
      - label: C. 饮酒
        description: 选择C → 触发Q32
      - label: D. 健身
        description: 选择D
    multiSelect: false
```

**如果 Q31 选择 C（饮酒），继续弹出 Q32**：

```yaml
questions:
  - question: 您对饮酒的态度是？
    header: Q32
    options:
      - label: A. 小酌怡情，喝不了太多
        description: 正常
      - label: B. 我习惯将白酒灌在保温杯，当白开水喝，酒精令我信服
        description: 触发隐藏人格"酒鬼"
    multiSelect: false
```

**计分**:
- Q25-Q30: A=1, B=2, C=3
- Q27 **反向计分**: A=3, B=2, C=1
- Q32 选 B → 触发隐藏人格 **DRUNK（酒鬼）**

---

## 结果计算与输出

### 维度得分计算

```python
# 维度得分汇总（每维度 2-6 分）
S1  = Q1 + Q2   # 自尊自信
S2  = Q3 + Q4   # 自我清晰度
S3  = Q5 + Q6   # 核心价值
E1  = Q7 + Q8   # 依恋安全感
E2  = Q9 + Q10  # 情感投入度
E3  = Q11 + Q12 # 边界与依赖
A1  = Q13 + Q14 # 世界观倾向
A2  = Q15 + Q16 # 规则与灵活度
A3  = Q17 + Q18 # 人生意义感
Ac1 = Q19 + Q20 # 动机导向
Ac2 = Q21 + Q22 # 决策风格
Ac3 = Q23 + Q24 # 执行模式
So1 = Q25 + Q26 # 社交主动性
So2 = Q27 + Q28 # 人际边界感
So3 = Q29 + Q30 # 表达与真实度
```

### 层级判定

- **L (Low)**: 2-3 分
- **M (Medium)**: 4 分
- **H (High)**: 5-6 分

### 特殊规则

- **Q32 选 B** → 直接判定为 **DRUNK（酒鬼）**，跳过标准匹配
- **标准匹配度 < 60%** → 分配 **HHHH（傻乐者）**

---

## 24 种人格类型

| 代码 | 名称 | 特征简述 |
|------|------|----------|
| CTRL | 拿捏者 | 高效、规则感强、喜欢掌控全局 |
| ATM-er | 送钱者 | 责任心强、总是为他人付出 |
| Dior-s | 屌丝 | 犬儒主义、看透消费主义、佛系 |
| BOSS | 领导者 | 强势、效率至上、不断自我突破 |
| THAN-K | 感恩者 | 乐观、感恩、看到世界美好面 |
| OH-NO | 哦不人 | 风险意识强、注重边界和秩序 |
| GOGO | 行者 | 行动力强、所见即所得、解决问题 |
| SEXY | 尤物 | 魅力十足、吸引力强 |
| LOVE-R | 多情者 | 情感丰富、浪漫、追求灵魂伴侣 |
| MUM | 妈妈 | 温柔、共情强、照顾他人 |
| FAKE | 伪人 | 社交面具多、适应性强 |
| OJBK | 无所谓人 | 随和、不争执、佛系 |
| MALO | 吗喽 | 童心、反常规、奇思妙想 |
| JOKE-R | 小丑 | 幽默、气氛组、用笑声掩饰内心 |
| WOC! | 握草人 | 大惊小怪但内心冷静 |
| THIN-K | 思考者 | 深度思考、逻辑严密、注重隐私 |
| SHIT | 愤世者 | 嘴上抱怨世界、手上默默做事 |
| ZZZZ | 装死者 | 拖延但死线前爆发、效率奇高 |
| POOR | 贫困者 | 专注、资源集中、在特定领域深耕 |
| MONK | 僧人 | 看破红尘、需要独立空间、边界感强 |
| IMSB | 傻者 | 内心戏丰富、社交恐惧、自我怀疑 |
| SOLO | 孤儿 | 自我价值感低、防御性强 |
| FUCK | 草者 | 不守规则、生命力旺盛、情绪化 |
| DEAD | 死者 | 超越欲望、对一切失去兴趣 |
| IMFW | 废物 | 缺乏安全感、依赖他人、容易信任 |
| HHHH | 傻乐者 | 脑回路清奇、无法归类 |
| DRUNK | 酒鬼 | 隐藏人格，酒精亲和性强 |

---

## 维度层级解读

### S1 自尊自信
- **L**: 对自己下手比别人还狠，夸你两句你都想先验明真伪
- **M**: 自信值随天气波动，顺风能飞，逆风先缩
- **H**: 心里对自己大致有数，不太会被路人一句话打散

### S2 自我清晰度
- **L**: 内心频道雪花较多，常在"我是谁"里循环缓存
- **M**: 平时还能认出自己，偶尔也会被情绪临时换号
- **H**: 对自己的脾气、欲望和底线都算门儿清

### S3 核心价值
- **L**: 更在意舒服和安全，没必要天天给人生开冲刺模式
- **M**: 想上进，也想躺会儿，价值排序经常内部开会
- **H**: 很容易被目标、成长或某种重要信念推着往前

### E1 依恋安全感
- **L**: 感情里警报器灵敏，已读不回都能脑补到大结局
- **M**: 一半信任，一半试探，感情里常在心里拉锯
- **H**: 更愿意相信关系本身，不会被一点风吹草动吓散

### E2 情感投入度
- **L**: 感情投入偏克制，心门不是没开，是门禁太严
- **M**: 会投入，但会给自己留后手，不至于全盘梭哈
- **H**: 一旦认定就容易认真，情绪和精力都给得很足

### E3 边界与依赖
- **L**: 容易黏人也容易被黏，关系里的温度感很重要
- **M**: 亲密和独立都要一点，属于可调节型依赖
- **H**: 空间感很重要，再爱也得留一块属于自己的地

### A1 世界观倾向
- **L**: 看世界自带防御滤镜，先怀疑，再靠近
- **M**: 既不天真也不彻底阴谋论，观望是你的本能
- **H**: 更愿意相信人性和善意，遇事不急着把世界判死刑

### A2 规则与灵活度
- **L**: 规则能绕就绕，舒服和自由往往排在前面
- **M**: 该守的时候守，该变通的时候也不死磕
- **H**: 秩序感较强，能按流程来就不爱即兴炸场

### A3 人生意义感
- **L**: 意义感偏低，容易觉得很多事都像在走过场
- **M**: 偶尔有目标，偶尔也想摆烂，人生观处于半开机
- **H**: 做事更有方向，知道自己大概要往哪边走

### Ac1 动机导向
- **L**: 做事先考虑别翻车，避险系统比野心更先启动
- **M**: 有时想赢，有时只想别麻烦，动机比较混合
- **H**: 更容易被成果、成长和推进感点燃

### Ac2 决策风格
- **L**: 做决定前容易多转几圈，脑内会议常常超时
- **M**: 会想，但不至于想死机，属于正常犹豫
- **H**: 拍板速度快，决定一下就不爱回头磨叽

### Ac3 执行模式
- **L**: 执行力和死线有深厚感情，越晚越像要觉醒
- **M**: 能做，但状态看时机，偶尔稳偶尔摆
- **H**: 推进欲比较强，事情不落地心里都像卡了根刺

### So1 社交主动性
- **L**: 社交启动慢热，主动出击这事通常得攒半天气
- **M**: 有人来就接，没人来也不硬凑，社交弹性一般
- **H**: 更愿意主动打开场子，在人群里不太怕露头

### So2 人际边界感
- **L**: 关系里更想亲近和融合，熟了就容易把人划进内圈
- **M**: 既想亲近又想留缝，边界感看对象调节
- **H**: 边界感偏强，靠太近会先本能性后退半步

### So3 表达与真实度
- **L**: 表达更直接，心里有啥基本不爱绕
- **M**: 会看气氛说话，真实和体面通常各留一点
- **H**: 对不同场景的自我切换更熟练，真实感会分层发放

---

## 报告输出格式

```markdown
# 🎯 SBTI 人格测试报告

## 📊 主类型

**[代码] [中文名]** — 匹配度 XX%

## 📈 维度分析

| 维度 | 得分 | 层级 | 解读 |
|------|------|------|------|
| S1 自尊自信 | X/6 | L/M/H | [解读] |
| S2 自我清晰度 | X/6 | L/M/H | [解读] |
| ... | ... | ... | ... |

## 📝 类型描述

[该人格类型的详细特征描述]

## 💡 友情提示

本测试仅供娱乐，不作为任何专业心理学依据。
```

---

## 注意事项

1. 本测试仅供娱乐，不作为任何专业心理学依据
2. 结果可能受到用户当前心情和状态影响
3. 部分人格类型名称带有调侃性质，请勿过度解读
4. Q32 选 B 触发隐藏人格"酒鬼"
5. 如果标准人格库最高匹配度低于 60%，将强制分配"HHHH 傻乐者"人格
