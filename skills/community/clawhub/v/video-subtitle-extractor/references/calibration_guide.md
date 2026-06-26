# Text Calibration Guide for Chinese ASR Output

Common transcription errors and their corrections. Apply these patterns when calibrating whisper output for Chinese financial/technical content.

## 1. Homophone Replacements (同音字混淆)

| Raw (Wrong) | Correct | Example |
|-------------|---------|---------|
| 硬钢 | 硬扛 | 硬钢→硬扛 |
| 抛押 | 抛压 | 消化抛押→消化抛压 |
| 模两个月 | 磨两个月 | 横盘调整模两个月→磨两个月 |
| 膜光短线 | 磨光短线 | 膜光短线→磨光短线 |
| 流通骨 | 流通股 | 流通骨的换手→流通股的换手 |
| 金接盘 | 新接盘 | 金接盘的成本→新接盘的成本 |
| 拉伸 | 拉升 | 拉伸成本→拉升成本 |
| 跟锋 | 跟风 | 跟锋买入→跟风买入 |
| 微转 | 微赚 | 微转就抛售→微赚就抛售 |
| 落带为安 | 落袋为安 | 落带为安→落袋为安 |
| 互盘 | 护盘 | 主力互盘明显→主力护盘明显 |
| 逼散互买 | 逼散户卖 | 洗盘本质是逼散互买→逼散户卖 |
| 仅 | 有 | 仅有资金拖住→有资金托住 |
| 军线 | 均线 | 关键军线→关键均线 |
| 快有动作 | 快有动作 | Already correct, but watch for 快会→快会 |

## 2. Financial Term Corrections

| Raw | Correct | Context |
|-----|---------|---------|
| 交筹 | 交筹 | 慢慢就焦愁→慢慢就交筹 |
| 再计 | 在即 | 拉升再计→拉升在即 |
| 没装 | 没仓 | 根本没装→根本没仓 |
| 利空 | 利空 | Already correct, verify |
| K线收14星 | K线收十字星 | 14→十 |
| 14星 | 十字星 | K线收十字星 |
| 洗崩 | 洗崩 | Already correct (跌太多) |
| 割肉 | 割肉 | Already correct |

## 3. Domain Term Patterns

Whisper often confuses financial jargon:
- 洗盘 (xǐ pán) vs 洗盘 (same pronunciation but context-dependent)
- 筹码 (chóu mǎ) - usually correct
- 建仓 (jiàn cāng) - usually correct
- 杠杆 (gàng gǎn) - usually correct
- 信托 (xìn tuō) - usually correct

## 4. Structural Cleanup

- Add proper punctuation (periods, commas) where ASR output lacks them
- Split long run-on sentences at natural topic breaks
- Format as flowing paragraphs, not timestamp-ordered fragments
- Add section headings for topic shifts: "洗盘核心目的", "三个核心指标", "三个信号", etc.
- Keep timestamps if user wants time-coded output (from .srt/.vtt)

## 5. Quality Indicators

After calibration, flag low-confidence sections:
- Unclear audio sections (background noise, overlapping speech)
- Rapid technical jargon sequences
- Sections where multiple interpretations are plausible

## 6. Multi-language Content

For bilingual content (Chinese + English):
- Preserve English terms: PE ratio, MA, MACD, KDJ, Bollinger Bands
- Mixed language phrases: "比如 PE 20倍", "MACD 金叉" are correct
- Don't translate technical terms to Chinese

## 7. Calibration Output Format

After applying corrections, present as:
- Clean prose with proper Chinese punctuation
- Optional: show what was changed vs raw output
- Optional: timestamp references from original SRT/VTT

## 8. AI / Tech Domain Corrections (AI 及科技领域)

For videos about AI, semiconductors, and tech investment topics, watch for:

### Chinese Company Names (whisper frequent errors)
| Raw (Wrong) | Correct | Context |
|-------------|---------|---------|
| 中繼續創 | 中际旭创 | A股光模块龙头 |
| 新益勝 | 新易盛 | A股光模块 |
| 天賦通信 | 天孚通信 | A股通信 |
| 元傑科技 | 源杰科技 | A股芯片 |
| 阿力 | 阿里 | 阿里巴巴 |
| Alley | 阿里 | Context: 腾讯、阿里、字节 |

### AI Product & Term Names
| Raw (Wrong) | Correct |
|-------------|---------|
| Deepseat | DeepSeek |
| ChadGPT | ChatGPT |
| Cloud | Claude (if Anthropic context) |
| Moe價構 / 莫架构 | MoE架构 (Mixture of Experts) |
| HPM | HBM (High Bandwidth Memory) |
| 光膜块 | 光模块 (Optical Module) |
| 夜冷 | 液冷 (Liquid Cooling) |
| 巨深智能 | 具身智能 (Embodied AI) |
| 端側推理 | 端侧推理 (On-device Inference) |
| 推測解碼 | 推测解码 (Speculative Decoding) |
| 主能板块 | 储能板块 (Energy Storage) |

### Traditional → Simplified Chinese
Whisper medium/large models commonly output traditional Chinese (繁體) for simplified content. Always convert:
- 發→发, 來→来, 時→时, 會→会, 體→体, 報→报, 機→机
- 線→线, 構→构, 購→购, 業→业, 電→电, 纜→缆, 銅→铜
- 壹→一, 貳→二, 等等