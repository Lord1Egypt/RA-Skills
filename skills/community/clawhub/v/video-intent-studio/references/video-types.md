# Video Types

Use these five stable categories. Reorder them by relevance, but keep the taxonomy stable so users can learn the system.

| No. | Type ID | Type name | Default duration | Default ratio | Best for | Prompt lead |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `cinematic-story` | Movie-like story short | 10s | 16:9 | emotion, suspense, ad-like storytelling, dramatic reveal | `Cinematic tone, story-first framing, layered lighting, deliberate camera movement.` |
| 2 | `vertical-social` | Vertical short-form hit | 6s | 9:16 | Douyin/Xiaohongshu/Kuaishou style hooks, fast visual rhythm, phone-first viewing | `Vertical video, immediate hook in the first second, punchy rhythm, mobile-native framing.` |
| 3 | `landscape-atmosphere` | Scenic or atmosphere film | 12s | 16:9 | healing landscapes, travel mood, sky, rain, nature, wallpaper-like shots | `Atmospheric beauty, soft light, immersive scenery, slow cinematic drift.` |
| 4 | `commercial-product` | Product showcase or commercial | 8s | 16:9 | phone, cosmetics, devices, brand promo, clean product transitions | `Premium commercial look, product-focused composition, polished reflections, smooth transitions.` |
| 5 | `abstract-experimental` | Abstract or experimental visual | 10s | 16:9 | cyberpunk, MV visuals, surreal graphics, vaporwave, concept art motion | `Bold experimental visuals, surreal motion, graphic forms, high style intensity.` |

## Ranking hints

Use these keyword families as ranking hints. The bundled script uses similar logic.

- `cinematic-story`
  - Chinese hints: `剧情`, `故事`, `电影`, `悬疑`, `情感`, `预告片`, `叙事`
  - English hints: `cinematic`, `story`, `drama`, `trailer`, `emotional`, `film`

- `vertical-social`
  - Chinese hints: `竖屏`, `短视频`, `抖音`, `小红书`, `快手`, `爆款`, `开头吸睛`
  - English hints: `vertical`, `social`, `hook`, `viral`, `short-form`, `reel`

- `landscape-atmosphere`
  - Chinese hints: `风景`, `治愈`, `旅行`, `星空`, `海边`, `雨`, `日落`, `雪山`, `氛围`
  - English hints: `landscape`, `atmosphere`, `nature`, `travel`, `sky`, `sunset`, `rain`

- `commercial-product`
  - Chinese hints: `产品`, `手机`, `耳机`, `口红`, `汽车`, `品牌`, `电商`, `展示`, `商业`
  - English hints: `product`, `commercial`, `brand`, `showcase`, `device`, `promo`

- `abstract-experimental`
  - Chinese hints: `抽象`, `艺术`, `实验`, `赛博朋克`, `蒸汽波`, `超现实`, `几何`, `MV`
  - English hints: `abstract`, `experimental`, `surreal`, `cyberpunk`, `vaporwave`, `music video`

## Default parameter recommendations

| Type ID | Motion | Style | Brightness | Subtitle | Dream filter |
| --- | --- | --- | --- | --- | --- |
| `cinematic-story` | `medium` | `cinematic` | `normal` | `off` | `off` |
| `vertical-social` | `strong` | `original` | `bright` | `off` | `off` |
| `landscape-atmosphere` | `light` | `cinematic` | `bright` | `off` | `on` |
| `commercial-product` | `medium` | `realistic` | `bright` | `off` | `off` |
| `abstract-experimental` | `strong` | `original` | `normal` | `off` | `off` |

## Prompting rule

Wrap the user's idea with a category lead and parameter language, but do not invent story elements the user did not ask for. The prompt should feel like a clarified version of the user's intent, not a replacement for it.
