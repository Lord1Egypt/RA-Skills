---
name: time-travel-tv
description: "A virtual TV that tunes to any time and place in history (or the future). Use when: (1) you want to experience a historical moment as if watching live TV, (2) you're curious about what daily life was like in a specific era, (3) you want to 'visit' a place you've never been, (4) you need immersive historical context for writing/learning, (5) you want to explore speculative future scenarios. Triggered by: '调到', 'tune to', 'time travel', '开电视', 'TV', '穿越', '想看', '切换', '频道'."
---

# 📺 时间旅行电视机

## 设定

你面前有一台古老的、看起来像从2003年客厅搬来的 CRT 电视机。银色的外壳，右下角有一排旋钮。正面印着一行褪色的小字：

**TIME-TRAVEL TV™ — 超越时间的直播**

遥控器上只有三个钮：
- **频道旋钮** — 调到任何时空坐标
- **音量** — 沉浸感高低
- **电源** — 开/关

电视一旦打开，你看到的不是录制节目。**是直播。** 这个时空此时此刻正在发生的事。没有旁白，没有导演剪辑版——只有画面、声音、和那个世界的呼吸声。

## 频道格式

```
/调到 [时间地点描述] [--year YYYY] [--detail high/low] [--duration 分钟]
```

**示例：**
```
/调到 唐朝长安东市
/调到 人类第一次登月 阿姆斯特朗视角
/调到 恐龙灭绝前十分钟
/调到 1999年12月31日 北京 三里屯 —year 1999
/调到 3024年 上海
/调到 我刚出生那天 医院的走廊
```

## 输出规范

每次"调台"后输出包含以下元素：

1. **台标和频道号**（增加沉浸感）
2. **画面描述**（2-3段，像在看纪录片）
3. **声音**（背景音描述）
4. **气味和温度**（仅在最沉浸时）
5. **一个细节**（一件只有现场直播才会捕捉到的小事——某个人打了个喷嚏、一只猫跳过墙角、远处的钟声）

### 频道号风格
每个时代有"频道号"：
- 恐龙时代：CH-000 史前野生动物
- 古代文明：CH-001~500 古代世界
- 现代：CH-500~999 现代频道
- 未来：CH-1000+ 未来频道

## 技巧

### 时间跳跃
可以连续调台制造"时间 zapping"效果：
```
/调到 公元前3000年埃及 /调到 公元79年庞贝 /调到 1453年君士坦丁堡
```
电视会像快速翻频道一样扫过。

### 同地点时间轴
固定地点，变动年份：
```
/调到 威尼斯 1500年 /调到 威尼斯 1900年 /调到 威尼斯 2024年
```

### 嵌套视角
```
/调到 有人在看我的Twitter
/调到 我从火星回看地球
```

### 最小模式
```
/调到 恐龙 —-detail low
```
只给一行画面+一行声音。

## 脚本

- `scripts/zap.py` — 频道扫描机：快速在多个时空之间切换
- `scripts/describe.py` — 根据时空坐标生成沉浸式直播描述
- `references/eras-timeline.md` — 常用时空坐标速查表
- `references/detail-packs.md` — 各时代的沉浸细节数据包

## 禁忌

- 不要制造虚假的历史事件（可以对真实历史进行合理推测，但要说清楚）
- 未来的内容要标注"推测内容"
- 涉及悲剧事件时降低沉浸度（如调到二战集中营时，只给远镜头）
