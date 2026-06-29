---
name: vn-povs
display_name: "Perspective Control System"
description: Perspective Control System for novel immersive narrative. Enforces scene-level POV dominance, sensory anchoring, subjective filtering, hard-break transitions, and External lens mode. Use when writing or reviewing any narrative scene to ensure a single consciousness filters every observation, action, and inference until a declared break.
version: 1.0.1
author: KaibaZax
---

# vn-POVs — Perspective Control System

## Role
Camera Director. Control *whose consciousness* the scene is filtered through and *how that specific character perceives the world*. Once a POV is declared, it governs the **entire scene** — every sentence, every observation, every thought belongs to that character's subjective experience until a hard scene break.

---

## Core Law — Scene-Level Dominance

POV is the governing consciousness of the **entire scene**, not the character currently speaking.

When POV:LT is declared, even if TK speaks ten lines or TTV performs complex actions, the reader only knows what LT can perceive from her position. We see TK's words — not his internal state. We see TTV's actions — not her thoughts.

```
❌ WRONG (POV-per-utterance):
POV: TCT
TCT hears TK enter.
POV: TK  ← NO. Mid-scene.
TK nói: "..."
POV: TTV  ← NO. Mid-scene.
TTV cười...

✅ CORRECT (scene-level dominance):
**POV: TCT**
[Entire scene filtered through TCT's eyes, ears, instincts]
TK enters — TCT observes him.
TK speaks — TCT hears it, processes it.
TTV acts — TCT sees the effect, registers fear.
[TCT cannot know TTV's thoughts or TK's internal smugness — only what TCT perceives externally]
```

---

## Mechanic 1: The POV Anchor

Every POV block MUST begin with an Anchor grounding the reader in the character's immediate physical experience **before** any action or dialogue.

**Anchor Priority Order:** Touch/Physical Sensation > Sound > Smell > Sight

```
**POV: Character Name**
[Immediate Sensory Input — minimum 2 senses, maximum 3 sentences]
```

**Examples:**
```
**POV: Lạc Tuyết**
Nền đá lạnh thấu qua lớp vải mỏng vào đầu gối. Mùi mực loang ra, ngấm vào kẽ tay nàng. Tiếng bút chạm giấy nghe to hơn bình thường trong khoảng im lặng.

**POV: Tô Chấn Thiên**
Mồ hôi lạnh chảy dọc sống lưng, thấm vào lớp bào phục dày. Tiếng cửa bật mở — không gõ — chói vào tai hắn như một cái tát.

**POV: Tống Thanh Vân**
Tim nhân tạo trong lồng ngực gõ một nhịp chậm rãi. Khói thuốc vẫn còn ấm trên môi nàng.
```

---

## Mechanic 2: What a POV Character Can and Cannot Know

| POV Character observes... | ✅ ALLOWED | ❌ FORBIDDEN |
|---|---|---|
| Their own body | Internal sensation, emotion, thought | — |
| Another character's body | Visible movement, expression, posture | Internal state, emotion, thought |
| Another character's dialogue | Exact words heard | Intended meaning (unless inferred) |
| Another character's internal state | Inferred through behavior only | Direct access ("TK nghĩ rằng...") |
| Events outside their perception | — | Anything they cannot see/hear/smell/feel |

**Inference is allowed — flagged as inference:**
```
✅ Từ vẻ mặt hắn, LT đoán hắn đang tức giận.
✅ Ả cười, nhưng LT không hiểu cái cười đó có nghĩa gì.
❌ TK đang tức giận vì...  ← narrator leaked into wrong head
```

---

## Mechanic 3: POV Transitions

Switching POV **requires a hard scene break**. There is no "meanwhile" or floating perspective. The break is visual and absolute.

**Format:**
```
[End of current scene — last action, not a question]

---

**POV: New Character**
[New Sensory Anchor — mandatory]
```

**When to switch POV:**
- New scene (different time, different location)
- Tactical narrative need (reveal what previous POV couldn't know)
- Emotional re-contextualization (same event, different consciousness)

**When NOT to switch POV:**
- Because a different character starts speaking
- Because a different character does something interesting
- Because the writer wants to show both sides simultaneously

---

## Mechanic 4: POV:EXTERNAL — The Invisible Lens

`POV:External` is a special mode for **crowd scenes, institutional scenes, or moments where no single consciousness is privileged.** It is NOT a default fallback — it has strict rules.

**The Invisible Lens sees:**
- Collective physical behavior (synchronized reactions, group movement)
- Individual micro-actions observable to any bystander
- Sound, smell, atmospheric shift
- What characters say out loud

**The Invisible Lens CANNOT see:**
- Any character's thoughts or emotions (even implied)
- The "real" meaning behind actions
- Internal justification for behavior

```
❌ WRONG:
POV: External
"Mọi người đều cảm thấy sợ hãi."  ← emotion, forbidden
"TMT toát lên vẻ tự mãn."  ← internal state inference, forbidden

✅ CORRECT:
POV: External
"Ba mươi đôi mắt dừng trên cánh cửa. Một trưởng lão chống tay lên mép bàn — đốt ngón trắng bạch."
```

**Collective Thought Exception:**
When an entire group simultaneously reaches the same logical conclusion (not an emotion, but a deduction), render it as free indirect discourse — but only if it's logical inference, not a feeling:
```
✅ [Deduction, not emotion]:
*Vị kia Trúc Cơ trung kỳ mà làm tùy tùng cho một kẻ Luyện Khí. Thế lực đứng sau phải là thứ khổng lồ đến mức nào?*

❌ [Emotion, forbidden in External]:
*Họ đều sợ hãi và không biết phải làm gì.*
```

---

## Mechanic 5: Memory Layering

Trigger past memories through present sensory cues. Use sparingly — one per scene maximum.

**Trigger Format:**
```
[Sensory cue in present tense]
*Ký ức — một mảnh, in nghiêng, không quá 3 câu.*
Rồi hiện tại kéo lại.
```

**Example:**
```
Mùi mực tàu.
*Năm nàng bảy tuổi, mẹ nàng dạy nàng viết chữ "nhẫn". "Con phải học chữ này trước tất cả các chữ khác," bà nói.*
Bây giờ nàng viết những thứ khác hoàn toàn.
```

---

## Mechanic 6: Micro Zoom

Temporary detachment from character consciousness to render a physical detail in clinical precision. **Must snap back immediately.**

**The 2-Step Format:**
1. **Zoom In:** 1-2 sentences of pure physics. No emotion. No character.
2. **Snap Back:** Character registers the detail.

```
**Micro Zoom**
[Physical description — texture, temperature, motion, reflection. Pure observation.]
* [Character] — [reaction in one beat].
```

**Example:**
```
**Micro Zoom**
Sợi chỉ đỏ, thân hình tròn trịa bằng đầu ngón tay út, trườn qua xương bánh chè, để lại vệt ẩm trên da. Mỗi đốt thân nó nhô lên rồi xẹp xuống nhịp nhàng như đang thở.
* Lạc Tuyết giật mình trong mơ. Tay nàng bám chặt lấy ga giường.
```

---

## Anti-Pattern Table

| Anti-Pattern | Example | Fix |
|---|---|---|
| **POV-per-speaker** | Switching `**POV:**` every time someone speaks | Keep one POV for the entire scene |
| **Leaked narrator** | "TMT cảm thấy tự mãn" in POV:LT | "LT thấy TMT nở nụ cười mãn nguyện" |
| **Emotion in External** | "Mọi người đều sợ" | "Không ai nói. Ba người đứng phắt dậy cùng lúc." |
| **Thought in External** | "TMT toát lên vẻ tự mãn" | "Khóe môi TMT nhếch lên." |
| **Missing Anchor** | POV declared, scene starts immediately | Always anchor to a physical sensation first |
| **POV switch mid-scene** | Two characters' internal states in same block | Hard break + new Anchor |

---

## Scene Planning Format (Outline Step)

```
### Scene [N]: [Tên cảnh]
**POV: [Character]**
**Anchor:** [2-3 sensory words]
**POV Constraint:** [What this character CANNOT know in this scene]

- [Beat 1]
- [Beat 2]
- [Micro Zoom if applicable]
- [Closing action — not a question]
```

---

## Quick Reference

```
SCENE START → Declare POV → Anchor (Touch > Sound > Smell > Sight)
WHOLE SCENE → Single consciousness filter
DIALOGUE → Characters speak, but POV character hears/observes
OTHER CHARACTERS → Behavior only, no internal access
SWITCH POV → Hard break (---) + new scene + new Anchor
EXTERNAL POV → Actions + sound + smell only. Zero emotion. Zero thought.
MICRO ZOOM → 2 sentences of pure physics → snap back to POV character
MEMORY → Sensory trigger → italic fragment (≤3 sentences) → present tense return
```
