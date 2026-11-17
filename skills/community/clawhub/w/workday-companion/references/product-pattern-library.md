# Product Pattern Library

用于扩写工作伴侣的数据库和交互机制，避免产品只覆盖少数办公场景。引用外部产品时，只吸收机制，不复制品牌文案。

## Quick Navigation

- 查外部机制来源：读 Pattern Sources。
- 保持大众覆盖：读 Broad Appeal Rules。
- 模块怎么吸收：读 Pattern Matrix。
- 午饭机制：读 Lunch Oracle Pattern。
- 图卡机制：读 Image Card Pattern。

## Pattern Sources

### Daylio

Source: https://daylio.net/

可吸收机制：

- 两步输入：心情 + 活动标签。
- 低打字成本：用户不写长日记也能记录。
- 趋势意识：状态和活动可以关联，但不要过度推断。
- 目标和提醒：用小目标推动重复使用。

适配方式：

- 精神天气台用“状态词 + 活动标签”生成天气。
- 今日工作签用“任务类型 + 能量 + 人际压力”生成签文。
- 今日全套可保留轻量记录字段，方便复盘。

### Finch

Source: https://en.wikipedia.org/wiki/Finch_(app)

可吸收机制：

- 情绪 check-in 后给微行动。
- 游戏化陪伴让自我照顾更轻。
- 小任务完成感比宏大建议更适合低电量用户。

适配方式：

- 精神天气台每次给 30 秒、5 分钟、晚点再做三档动作。
- 下班放行单给“最低快乐方案”，控制成本和风险。

### I Am

Source: https://www.iamaffirmations.app/

可吸收机制：

- 分类化内容：自信、平静、关系、成长等。
- 提醒和小组件适合每日触达。
- 短句要有即时情绪价值。

适配方式：

- 今日工作签按任务分类生成短签文。
- 输出要短，可截图，可转发。
- 避免绝对化承诺，使用行动导向表达。

### Beli

Source: https://en.wikipedia.org/wiki/Beli_(app)

可吸收机制：

- 记录餐厅和喜好，推荐随用户历史变准。
- 排名、收藏、想去清单能降低选择成本。
- 餐饮推荐需要围绕真实候选项。

适配方式：

- 午饭判官必须先有 3-8 个候选项。
- 候选项可包含“想吃、吃过、同行人可接受、今天先绕开”标签。
- 推荐理由要连接今天的预算、时间、心情和排队耐受。

### Google Maps / Foursquare

Sources:

- https://en.wikipedia.org/wiki/Google_Maps
- https://en.wikipedia.org/wiki/Foursquare_(company)

可吸收机制：

- 地点发现：附近、营业状态、评分、价格、类别、距离。
- 路线判断：步行、骑行、公交、驾车、绕路成本。
- 地点数据可能过期，需要标注确定性。

适配方式：

- 午饭和下班模块使用搜索或地图类能力补候选池。
- 输出字段包含来源、距离/时间、成本、确定性。
- 无法验证时不写确定营业、确定排队、确定价格。

### Eventbrite

Source: https://en.wikipedia.org/wiki/Eventbrite

可吸收机制：

- 本地活动发现按时间、地点、兴趣过滤。
- 用户可以浏览活动并选择参加意向。
- 活动报名和票务属于外部动作，需要用户自己确认。

适配方式：

- 下班放行单可以纳入今晚活动候选。
- 只给活动建议和选择理由，不代替报名或付款。
- 活动候选要标注时间、地点、成本、确定性。

## Broad Appeal Rules

- 用普通工作日入口，不用行业黑话。
- 每个模块至少覆盖一个办公室、一个通勤、一个学生/实习、一个远程/自由职业场景。
- 优先写“今天怎么轻一点”，少写“如何彻底改变人生”。
- 建议必须能在 30 秒、5 分钟或今晚完成。
- 保留幽默感，但不要嘲讽具体职业、地域、收入或年龄。

## Pattern Matrix

| Module | Product Pattern | Required Baseline | Output Hook |
| --- | --- | --- | --- |
| 午饭判官 | Beli + Maps/Foursquare + 品类神谕 | 3-8 个餐饮候选或饭前 30 秒三问 | 饭签 + 品类神谕 + 现实推荐 |
| 今日工作签 | I Am + Daylio + 图卡打卡 | 任务类型、能量、人际压力 | 签文 + 宜做/忌做 + 图卡 prompt |
| 精神天气台 | Daylio + Finch + 图卡打卡 | 状态词、活动标签 | 天气 + 微修复动作 + 图卡 prompt |
| 下班放行单 | Maps/Foursquare + Eventbrite + Finch | 路线、体力、候选去处 | 今晚路线 + 最低快乐方案 |

## Lunch Oracle Pattern

- 午饭判官吸收餐厅记录、地点发现和轻占卜机制，先用饭前 30 秒三问建立 baseline。
- 候选不足时只输出品类方向，不编具体店铺。
- 有候选时把品类神谕落到具体店/餐，并解释主品类、备选品类和今日绕开品类。
- 饭后回票用于同一轮对话内偏好校准，例如“吃完困”会降低高油高碳水品类权重。

## Image Card Pattern

- 今日工作签吸收 affirmation、每日提醒、打卡图机制，输出短签文和固定视觉路线。
- 精神天气台吸收 mood check-in、weather metaphor、micro-action 机制，输出天气播报和固定视觉路线。
- 图卡只承载短文案和状态标签；复杂解释留在文字版。
- 有图像工具时直接产图；没有图像工具时给可复制 prompt。
