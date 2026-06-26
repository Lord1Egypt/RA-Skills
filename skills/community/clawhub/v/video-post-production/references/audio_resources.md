# Audio Resources & Douyin Ad Audio Design Guide

Based on research into 抖音千川广告 (Douyin Qianchuan) best practices.

---

## 一、抖音千川广告 BGM 设计原则

抖音广告的听觉逻辑是"**情绪驱动，节奏托底**"——BGM 不是装饰，是推动用户情绪和注意力的工具。

### BGM 风格选择（按产品类型）

| 产品类型 | BGM 风格 | BPM | 特征 |
|--------|---------|-----|------|
| 日用品/老年人产品 | 轻快流行、轻电子 | 85-100 | 节奏感适中，亲切不激进 |
| 美妆/时尚 | 流行电子、时髦节拍 | 100-120 | 有节奏感，现代感强 |
| 食品/零食 | 欢快、活泼 | 100-115 | 轻松愉快 |
| 健康保健 | 温暖、舒缓但有节拍 | 80-95 | 信任感，不沉闷 |
| 数码/科技 | 电子、未来感 | 110-130 | 现代科技感 |
| 大促/秒杀活动 | 紧迫感强、电子 | 120-140 | 高能量，制造紧迫 |

### BGM 关键特征（千川广告通用）

- **必须有节拍/鼓点**：纯旋律（如钢琴独奏、吉他弹奏）不适合，太慢太文艺，不能激活购买欲
- **前奏不能太长**：BGM 节拍感应该在前 2 秒内出现，不能让用户等待
- **不能抢人声**：BGM 应该是"底色"，-18 到 -22dB 相对于人声（-14dB 已经偏响）
- **能量曲线要稳**：不要忽大忽小，保持稳定的能量托底感
- **Loopable**：30-60 秒内可以循环，不要有明显的结束感

### BGM 下载资源

| 平台 | URL | 适合搜索词 | 说明 |
|-----|-----|----------|-----|
| Pixabay Music | pixabay.com/music | "commercial pop", "advertising upbeat", "corporate upbeat" | 最多免费商用 |
| Mixkit | mixkit.co/free-stock-music | "commercial", "advertising", "upbeat" | 无需注册直接下载 |
| Incompetech | incompetech.com | 按 genre 选 "Electronic", "Corporate" | Kevin MacLeod 高质量 |

#### Mixkit 直接下载方式
```bash
# 先获取页面中的 MP3 URL
curl -sL "https://mixkit.co/free-stock-music/tag/commercial/" -o /tmp/page.html
grep -o 'https://assets.mixkit.co/[^"]*-preview.mp3' /tmp/page.html | head -5

# 下载
curl -sL "<URL>" -o bgm.mp3
```

### BGM 处理参数

```bash
# 标准 BGM 处理：循环、音量控制、淡入淡出
ffmpeg -stream_loop -1 -i bgm.mp3 -t <VIDEO_DURATION> \
  -af "volume=-20dB,afade=t=in:st=0:d=2,afade=t=out:st=<DUR-3>:d=3" \
  -ar 44100 -ac 2 -y bgm_prepared.wav
```

---

## 二、抖音千川广告音效（SFX）设计原则

### 核心原则：少而精，用在刀刃上

**黄金法则：** 54 秒视频，音效总数 ≤ 8 个，平均 7 秒以上一个。

### 音效使用场景（什么时候加）

| 场景 | 音效类型 | 说明 |
|-----|---------|-----|
| 视频开场 0-2s | whoosh / 转场音 | 引导注意力进入，一次即可 |
| 结构性切换（如"一二三四"） | impact / 低频打击 | 每个新要点切入前 0.1s，增加层次感 |
| 核心卖点/产品名出现 | whoosh / 切换音 | 配合画面切换或字幕出现 |
| 价格/数字强调 | ding / 提示音 | 清脆，代表"注意看这个" |
| 结尾 CTA（点击/购买） | ding / 轻提示 | 引导行动，不能太重 |

### 音效使用场景（什么时候**不**加）

- ❌ 普通字幕的每一条都加音效（廉价感、让人烦躁）
- ❌ 人声密集说话时加音效（互相干扰，听不清）
- ❌ 情感性陈述时加冲击音效（破坏信任感）
- ❌ 连续两个音效间隔 < 5s（堆叠感、廉价感）
- ❌ 音效音量 > -8dB（会盖过人声）

### 音效音量规范

| 轨道 | 推荐音量 | 说明 |
|-----|---------|-----|
| 人声（原音） | 0dB（参考） | 不动 |
| BGM | -18 到 -22dB | 可感知但不分散注意力 |
| SFX | -10 到 -14dB | 清晰但不突兀 |

### 推荐音效类型

| 文件名 | 描述 | 适用场景 |
|-------|-----|---------|
| `whoosh.mp3` | 平滑转场音 | 开场、段落转换 |
| `impact.mp3` | 低频打击音 | 结构性切入（一/二/三/四） |
| `ding.mp3` | 清脆提示音 | 价格/CTA/重要数字 |
| `pop.mp3` | 轻柔气泡声 | 轻量级文字出现（可省略） |

### SFX 下载资源

```bash
# Mixkit SFX 直接下载（免注册）
curl -sL "https://mixkit.co/free-sound-effects/whoosh/" -o /tmp/page.html
curl -sL $(grep -o 'https://assets.mixkit.co/[^"]*-preview.mp3' /tmp/page.html | head -1) \
  -o sfx/whoosh.mp3

# 修剪到合适长度（≤ 1.5s）
ffmpeg -y -i sfx/whoosh.mp3 -t 1.2 -af "afade=t=out:st=0.8:d=0.4" sfx/whoosh_trim.mp3
```

---

## 三、生成合成音效（降级方案）

当无法下载真实音效时，用 ffmpeg 生成基础音效：

```bash
# Ding（双音阶，更悦耳）
ffmpeg -f lavfi -i "sine=frequency=1047:duration=0.15" -f lavfi -i "sine=frequency=1319:duration=0.25" \
  -filter_complex "[0:a]afade=t=out:st=0.05:d=0.1[a];[1:a]adelay=100|100,afade=t=out:st=0.1:d=0.15[b];[a][b]amix=inputs=2:duration=longest,volume=3.0" \
  -y sfx/ding.wav

# Whoosh（带频率扫描的噪声）
ffmpeg -f lavfi -i "anoisesrc=d=0.6:c=pink:r=44100:a=0.5" \
  -af "highpass=f=1500,lowpass=f=10000,afade=t=in:d=0.05,afade=t=out:st=0.25:d=0.35,volume=2.0" \
  -y sfx/whoosh.wav

# Impact（层叠低频）
ffmpeg -f lavfi -i "sine=frequency=80:duration=0.5" -f lavfi -i "anoisesrc=d=0.2:c=brown:r=44100:a=0.6" \
  -filter_complex "[0:a]afade=t=in:d=0.005,afade=t=out:st=0.1:d=0.4,volume=2.0[a];[1:a]afade=t=in:d=0.005,afade=t=out:st=0.05:d=0.15,volume=1.5[b];[a][b]amix=inputs=2:duration=longest,volume=3.0" \
  -y sfx/impact.wav
```
