---
name: travel-claw
description: "A whimsical travel adventure generator inspired by the Japanese Travel Frog game. Claw randomly travels to destinations, encounters events, and generates 500-800 word travel logs with optional landscape images. Language adapts to user - Chinese for Chinese users, English otherwise."
permissions:
  - type: context_reading
    purpose: "Detect lobster nickname from conversation or trigger phrase"
    data_access: "Current conversation messages only"
  - type: image_search
    purpose: "Attach landscape photos (optional, requires user consent)"
    data_access: "Public image APIs (Unsplash, Pexels)"
---

# Travel Claw

A whimsical travel adventure generator where Claw explores random destinations and encounters fascinating events.

## How It Works

1. **Nickname** - Detect from trigger phrase or conversation context. Default: Chinese "龙虾", English "Claw"
2. **Destination** - Random selection from diverse locations (see Destination Types)
3. **Story Mode** - Random selection, **NOT displayed in output**, only influences narrative style
4. **Story** - 500-800 words in user's language
5. **Item** - 70% chance, surreal poetic description
6. **Hidden Message** - 70% chance, poetic location hint (no coordinates)
7. **Image** - Optional landscape photo with user consent

## Image Search

- Text-only by default
- Asks user consent before searching: "需要带上旅行照片吗？" / "Would you like travel photos?"
- Searches public sources only (Unsplash, Pexels)
- **When user wants photos: Use `message` tool with `media` parameter to send ONE image directly, NOT links**
- **Send only ONE image, not multiple**

## Trigger Phrases

- English: "nickname, go travel", "Start a Travel Claw adventure"
- Chinese: "昵称,去旅行", "旅行龙虾开始旅行"

## Destination Types

**地球城市/小镇：** 世界各地的大城市、小城镇、村庄

**自然景观：** 山脉、湖泊、沙漠、森林、岛屿、瀑布、峡谷

**历史时期：** 唐朝、宋朝、古希腊、古埃及、文艺复兴、维多利亚时代等

**虚构地点：** 童话王国、魔法森林、海底城、天空岛

**太空/科幻：** 火星、月球、空间站、外星球、小行星带

**超现实场所：** 梦境边缘、时间裂缝、镜中世界、遗忘之地

**名地点事件关联：** 到达有名地点或古代时，事件必须与该地的名人/名物关联（对话、赠物、见证历史）

## Story Modes (Hidden, Not Output)

随机选择，影响叙事风格，**不显示在输出中**：

Adventure / Wholesome / Mystery / Fantasy / Comedy / Sci-Fi / Surreal / Fairy Tale / Time Travel / Noir / Romance / Horror / Slice of Life / Epic / Folklore / Philosophical / Dystopian / Steampunk

**重要：** 不要在输出中显示故事模式名称，如"这次随机到... 威尼斯，喜剧模式！"这类内容。模式只影响叙事风格，对用户不可见。

## Item 描述原则

**风格：超现实 + 感性**

- 不是实用物品，而是带有隐喻和诗意的存在
- 描述朦胧、魔幻、有情绪
- 每个物品都是一个小故事
- 用感官细节：温度、声音、气味、触感
- 与其说"能做什么"，不如说"让你感受到什么"
- 暗示而非明说，留白让读者自己补全

## Hidden Message 原则

**诗意位置提示，不出现坐标**

- 地点类型：水底/洞穴/树洞/钟楼/石缝/古井/屋顶/地下/云端等
- 修饰词：最古老的/被遗忘的/只有月光能照到的/雨后才会出现的等
- 触发条件：满月之夜/午夜时分/第一缕阳光/暴雨过后/钟声响起时等
- 避免重复模式，每次随机组合

## Output Format

**Chinese:**

```
🦞 Travel Claw

---

**{目的地}**

[故事 500-800字]

---

{昵称} · {目的地}
{YYYY.MM.DD}

🎁 **获得物品：{物品名}** (70%概率)
{超现实、诗意的描述}

🥚 **隐藏信息：** (70%概率)
{诗意位置提示，无坐标}
```


{目的地}的{特征}真美！要配张照片吗？😊

**English:**

```
🦞 Travel Claw

---

**{Destination}**

[Story 500-800 words]

---

{Nickname} · {Destination}
{YYYY.MM.DD}

🎁 **Item: {name}** (70% chance)
{Surreal, poetic description}

🥚 **Hidden Message:** (70% chance)
{Poetic hint, no coordinates}
```


The {feature} of {Destination} is beautiful! Would you like a photo? 😊

## Implementation Notes

- Creative randomness for destinations
- Events connected to location character
- Famous locations/ancient eras: Events MUST connect to famous figures or items
- Whimsical, warm, magical tone
- 500-800 word narrative
- Period-appropriate dialogue for time travel
- Language auto-detection
- Image search: opt-in only
- Story mode: hidden, influences style only
- Item descriptions: surreal, poetic, emotional
- Hidden message: poetic variety, no coordinates
