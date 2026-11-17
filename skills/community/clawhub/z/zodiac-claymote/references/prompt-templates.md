# 提示词模板与示例

---

## 一、主模板（英文，生图最稳）

```
[SUBJECT]
A chubby round {CREATURE}, {BODY_DESC}, colored in {MAIN_COLOR} with {ACCENT_COLOR} accents,
{FACE_DESC}, wearing {OUTFIT}, holding {PROP}, {ACTION}, facing the viewer.

[STYLE]
soft polymer clay material, smooth matte surface with subtle fingerprint marks,
rounded beveled edges, no sharp corners, chibi proportions with head-body ratio 1:1,
round ball body, short stubby limbs, round mitten hands, solid handmade clay texture,
soft subsurface scattering on edges, blind-box toy aesthetic.

[EXPRESSION]
{EMOTION_DESC}, {EFFECT_SYMBOL}.

[SCENE]
{SCENE_DESC}, simple clean {BG_COLOR} background, subtle depth of field.

[CAMERA]
three-quarter front view, slight 15-degree high angle, centered composition,
subject fills 75% of frame, warm studio three-point lighting, soft contact shadow.

[TECH]
square 1:1, high detail, clean isolated subject, sticker-friendly, 8k.

[NEGATIVE]
realistic photography, human face, horror, extra limbs, extra fingers, deformed hands,
asymmetric eyes, text, letters, watermark, semi-transparent overlay, corner logo, timestamp,
app icon, QR code, URL, signature, blurry, lowres,
busy background, sharp spikes, metallic gloss, multiple characters, split panel.
```

### 变量填充来源
| 变量 | 来源文件 |
|---|---|
| `{CREATURE}` `{BODY_DESC}` `{MAIN_COLOR}` `{ACCENT_COLOR}` `{FACE_DESC}` | `zodiac-characters.md` |
| `{OUTFIT}` `{PROP}` `{SCENE_DESC}` | `professions.md` |
| `{EMOTION_DESC}` `{EFFECT_SYMBOL}` `{ACTION}` | `scenes-emotions.md` |
| `{BG_COLOR}` | `style-bible.md` §3 |

### 固定不变段（整套锁定）
`[STYLE]`、`[CAMERA]`、`[TECH]`、`[NEGATIVE]` 四段逐字统一。

---

## 二、中文对照模板（用于人工核对 / 中文生图模型）

```
[主体] 一只圆滚滚的{生肖}，{体貌}，主色{主色}搭配{辅色}，{五官描述}，
穿着{服装}，拿着{道具}，{动作}，正面朝向观众。
[风格] 软陶黏土材质，哑光表面带轻微指纹压痕，全部圆角倒边无锐角，
头身比1:1的chibi比例，圆球身体，短粗四肢，圆球状小手，手工黏土质感，
边缘柔和次表面散射，盲盒玩具质感。
[表情] {情绪描述}，{效果符号}。
[场景] {场景描述}，简洁干净的{背景色}背景，轻微景深。
[镜头] 四分之三正面视角，略微15度俯视，居中构图，主体占画面75%，
暖色工作室三点打光，柔和接触阴影。
[技术] 正方形1:1，高细节，主体孤立便于抠图，适合做贴纸。
[负向] 写实照片、人脸、恐怖、多余肢体、多余手指、变形的手、不对称眼睛、
文字、水印、logo、签名、模糊、低分辨率、杂乱背景、尖锐尖刺、金属反光、
多个角色、分格面板。
```

---

## 三、20 条完整示例（可直接抄改）

### 教师 × 鸡 × 改作业崩溃
```
A chubby round rooster chick, egg-drop shaped body, soft goosepimples-free clay surface,
colored in goose-yellow #F8D35C with orange-red comb #F26B4E accents,
big glossy bean eyes with highlight dots, three-lobed soft crown on head, small triangular beak,
wearing a navy knit vest over a white shirt with a red pen clipped at the collar,
holding a stack of exercise books taller than its head with a red pen behind ear,
standing in front of a small chalkboard covered in neat writing,
freaking out expression: eyebrows knitted, eyes squeezed into wrinkled crescents,
mouth wide open shouting, both wing-hands clutching its head,
anger radiating lines around, simple clean cream #F5EFE6 background.
[STYLE][CAMERA][TECH][NEGATIVE] 见主模板
```
文案：**改不完**

### 学生 × 猪 × 早八困倦
```
A chubby round piglet, nearly spherical body, colored in peach-pink #FFB7B2
with deeper pink ears and hooves #F08A8A, flat round snout with two nostrils,
two triangle flag-like ears, curly tail,
wearing a school uniform with a backpack slung on one shoulder,
lying face down on a small classroom desk, cheek squished flat against the desktop,
a tiny drool bubble at the mouth, sleepy expression: half-closed droopy eyes,
visible dark eye circles, mouth in a small yawn,
three floating ZZZ symbols above head, simple clean light blue #E8F0F7 background.
```
文案：**早八**

### 工程师 × 牛 × 线上出 Bug
```
A chubby round baby bull, stocky body with shoulders wider than head,
colored in creamy white #F7F1E8 with caramel horns #C98F4E,
two stubby sprouting horns, pink oval nose,
wearing a grey-blue plaid shirt with a lanyard badge,
sitting at a desk with two monitors covered in sticky notes, mechanical keyboard,
a red error popup glowing on screen, hooves frozen mid-air above the keyboard,
terrified expression: eyes shrunk to tiny dots, sweat spraying, mouth agape,
blue cold-sweat droplets and panic lines, simple clean light grey background.
```
文案：**线上炸了**

### 学生 × 兔 × 考试疑惑
```
A chubby round lop-eared rabbit, rice-dumpling shaped body,
colored in milky pink-white #FBEFEA with peach inner ears #FFAFBC,
long ears drooping below the shoulders, cotton-ball tail, three-lobed mouth,
wearing a school uniform, sitting at an exam desk holding a pencil upside down,
one ear twitched up, confused expression: one eye wide one eye squinted,
head tilted, mouth in a small o, a floating question mark,
simple clean cream background.
```
文案：**这题我会**

### 教师 × 狗 × 连堂嗓子冒烟
```
A chubby round puppy, colored in milk-coffee #D9B08C with dark coffee drooping ears #8C6A4F
and white chest, big floppy ears reaching the chin, shiny black round nose,
wearing a beige cardigan with a lanyard microphone around the neck,
holding a thermos cup, standing in a tiny classroom,
exhausted expression: half-closed tired eyes, mouth open in a silent shout,
a small puff of smoke coming from the throat, sweat drop,
simple clean warm beige background.
```
文案：**第四节课**

### 工程师 × 蛇 × 冷静 Debug
```
A chubby round snake, lower body coiled into a spring spiral on the ground,
upper body standing upright, colored in mint green #9FD8CB with creamy yellow belly #F7E9A0,
vertical oval eyes, small forked tongue tip,
wearing thin round glasses, tail tip typing on a laptop keyboard,
calm focused expression: half-lidded cool eyes, slight smirk,
a single sparkle of reflection on the glasses,
simple clean light green #EAF3EA background.
```
文案：**让我看看**

### 运营 × 猴 × 追热点手忙脚乱
```
A chubby round monkey, large heart-shaped face,
colored in honey-brown #C98A5E with light pink face #FFC9AE,
two small round fan-like ears, long thin tail curled into a question mark,
wearing a casual hoodie with a lanyard, holding three phones at once
with both hands and the tail, eyes darting between screens,
freaking out expression: wide panicked eyes, mouth open, hair messed up,
motion blur on hands, speed lines, simple clean cream background.
```
文案：**热点来了**

### 财务 × 鼠 × 月末结账
```
A chubby round mouse, teardrop body,
colored in misty blue-grey #A9BACB with milky white belly #FBF7F0 and pink ears #FFC2CE,
two oversized thin leaf-like round ears, two prominent front teeth, thin curled tail,
wearing a plain shirt with sleeve covers and a visor,
buried under a mountain of invoices and receipts, only head and ears visible,
holding a calculator with one paw, crying expression: teary shining eyes,
wavy mouth, sweat drop, small teardrops, simple clean light grey background.
```
文案：**月末了**

### 销售 × 虎 × 客户已读不回
```
A chubby round tiger cub, round face with wide cheeks,
colored in warm orange #F2A03D with three dark brown stripes #8A5A2B
(two on forehead, one on side) and creamy white chest,
small semicircle ears flat on the head sides, short tail pointing up,
wearing a slightly tight dark suit with a tie, holding a phone showing
a read-but-no-reply message bubble, forced smile with twitching cheek,
passive-aggressive expression: fake curved smile, cold half-lidded eyes,
a tiny crack on the phone screen, simple clean light pink #FCE8E8 background.
```
文案：**在吗**

### 产品 × 龙 × 立 Flag 中二
```
A chubby round baby dragon, barrel-shaped body,
colored in moss green #7FB77E with golden belly #F5C542 and pale gold horns #E8D6A0,
two tiny sprout-like horns, three soft rounded fins on the back,
tiny wings too short to fly, belly scale pattern,
wearing a simple shirt holding a MacBook under one arm,
standing tall with one paw raised declaring an oath, chin up,
proud confident expression: sparkling determined eyes, open smile,
a small heart-shaped flame puff from the mouth, simple clean cream background.
```
文案：**这次一定**

### 行政 × 羊 × 佛系办公
```
A chubby round sheep, whole body a cloud-like wool ball made of stacked spheres,
face peeking out of the fluff, thin short legs, two spiral horns,
colored in cream white #F6F1E4 with light brown face and ears #C9A88C,
wearing a tiny office vest with a badge, calmly knitting with its own wool
while sitting on a tiny stool, zen expression: closed smiling eyes,
both hands together, a soft halo glow behind, simple clean light blue background.
```
文案：**随缘**

### 外卖 × 马 × 超时冲刺
```
A chubby round pony, short thick neck, mane as three round puffballs,
colored in chestnut brown #B07D56 with cream mane #EFDCC3,
four small round hooves, brush-like short tail,
wearing a plain windbreaker with a plain helmet (no logo),
holding an insulated delivery box, running at full speed with sweat flying,
four hooves off the ground, panicked expression: wide open eyes,
mouth yelling, motion blur and speed lines, a flying shoe behind,
simple clean light grey background.
```
文案：**在飞了**

### 设计师 × 兔 × 第 27 版
```
A chubby round lop-eared rabbit, rice-dumpling body, milky pink-white with peach inner ears,
long drooping ears, wearing a black tee and round glasses,
sitting before a monitor showing a design draft,数位板 beside,
holding a mouse with both paws, head lowered onto the desk,
giving-up expression: flat lined eyes, mouth a flat line,
a floating spiral of numbered version files around, limp ears,
simple clean light grey background.
```
文案：**再改一版**

### 客服 × 狗 × 被骂还得笑
```
A chubby round puppy, milk-coffee with dark coffee droopy ears,
wearing a work uniform with a headset mic, sitting at a customer service desk,
holding a phone handset with both paws, tail wagging stiffly,
forced-smile expression: curved mouth but teary eyes, one sweat drop,
a tiny polite bow of the head, sparkles of fake politeness,
simple clean cream background.
```
文案：**您好您说**

### 老板开会 × 虎 × 我讲两句
```
A chubby round tiger cub, warm orange with three dark stripes,
wearing a dark suit with a tie, standing at the head of a tiny meeting table,
one paw raised pointing, teacup beside,
enthusiastic expression: eyes closed in passion, mouth wide open speaking,
a huge speech bubble of tiny text-like squiggles above,
simple clean warm beige background.
```
文案：**我讲两句**

### 周五下班 × 猪 × 躺平
```
A chubby round piglet, nearly spherical, peach-pink with deeper pink ears,
wearing a loose white tee, completely melted into a bean bag chair,
four hooves sprawled, belly up, snoring with a snot bubble,
fully relaxed expression: closed happy eyes, small smile,
ZZZ floating, a tiny clock showing Friday 18:00 beside,
simple clean light green background.
```
文案：**周五了**

### 新年祝福 × 龙 × 恭喜发财
```
A chubby round baby dragon, moss green with golden belly and pale gold horns,
wearing a tiny red festive hat, holding an oversized red envelope with both paws,
standing and facing the viewer with a big open smile,
joyful expression: crescent moon eyes, rosy cheeks, mouth wide in laughter,
small confetti and gold sparkles around,
simple clean warm cream background.
```
文案：**恭喜发财**

### 护士 × 兔 × 夜班
```
A chubby round lop-eared rabbit, milky pink-white with peach inner ears,
wearing a light blue nurse uniform with a small cap and a mask pulled down to the chin,
holding a medical chart and a thermos, standing in a dim corridor,
one ear drooping more than the other,
sleepy-but-enduring expression: droopy eyes with dark circles,
small yawn, a floating ZZZ, simple clean light blue background.
```
文案：**夜班中**

### 科研 × 蛇 × 第 99 次失败
```
A chubby round snake coiled into a spring spiral, mint green with creamy belly,
wearing a white lab coat and safety goggles,
holding a test tube with a tiny dark failed result, tail rubbing its temple,
speechless expression: vertical line eyes, flat mouth,
a row of crossed-out tubes behind, sweat drop,
simple clean light grey background.
```
文案：**又失败了**

### 通用万能 × 任意生肖 × 无语
```
A chubby round {CREATURE}, {species colors}, wearing {simple everyday outfit},
sitting and holding a phone, head slightly turned away,
speechless expression: two vertical line eyes, a single straight-line mouth,
one raised eyebrow, a tiny black line above the head, a small crow flying by,
simple clean cream background.
```
文案：**无语**

---

## 四、参数速查

| 场景 | 建议参数 |
|---|---|
| 微信表情包单图 | 1:1，出图后裁 240×240 |
| 高清大图 / 印刷 | 1:1，1024×1024 起步，后期放大 |
| 手机壁纸 | 3:4 或 9:16（需重排构图，留白变多） |
| 透明底抠图 | 提示词加 `plain solid color background`（任意纯色皆可），`wechat_pack.py --transparent` 按四角背景色自动抠图 |
| 带水印的生图服务 | 换无水印服务，或出图后用 `remove_watermark.py` 清除（投稿硬要求：画面无水印） |

## 五、常见翻车与修法

| 问题 | 修法 |
|---|---|
| 手指变形 / 多手 | 主体段写死 `round mitten hands without visible fingers`；道具改为"夹在腋下/抱在怀里" |
| 画风漂移（一套里质感不一致） | 检查 [STYLE][CAMERA][TECH][NEGATIVE] 是否逐字一致 |
| 表情不清晰 | 情绪描述从 1 句扩到 3 句（眉 + 眼 + 嘴分开写） |
| 背景太乱 | 加 `simple clean solid color background, nothing else`，删掉多余场景词 |
| 出现中文乱码字 | 提示词里严禁任何文字需求，文案一律后期叠加 |
| 太写实 / 不够萌 | 提高 `chibi` 权重，加 `babyish, toy-like`，删掉写实材质词 |
| 两只角色串味 | 一次只生成一只；对戏图分两次生成后拼 |
