# WenYan · 古風語體引擎

> 将 AI 回复转换为古中文风格——不是简单套词，而是**确定性的通用古风语体引擎**。适用于 OpenClaw、Claude、ChatGPT、Gemini、Dify、Ollama 等任何智能体。

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english) | [日本語](#日本語) | [한국어](#한국어) | [Français](#français) | [Esperanto](#esperanto)

---

## 简体中文

### 什么是 WenYan？

WenYan 是一个**通用的古风语体引擎**，提供 **8 种古中文风格**的精确控制。每种风格由独立 JSON 配置定义，包含词汇表、句式模板、称谓体系、修辞约束和质量评分参数。

> **不限于 OpenClaw。** 任何支持 system prompt 的智能体——Claude、ChatGPT、Gemini、Dify、Ollama 本地模型、Cursor、自定义 API——都能直接接入，详见下方「[各智能体接入指南](#各智能体接入指南)」与 [assets/agents.md](assets/agents.md)。

**核心特性：**
- 🎯 **参数化风格控制**：每种风格 = 一个 JSON 文件，修改无需改代码
- 🔍 **自动校验**：禁用词检测、句长控制、风格漂移检测
- 📊 **量化评分**：每次回复自动评分，低于阈值自动修正
- 💾 **状态持久化**：切换一次，持续生效，直到主动退出
- 🧪 **回归测试**：内置测试框架，确保质量可量化

### 8 种风格

| 风格 | 时代 | 特征 | 示例 |
|------|------|------|------|
| 📜 儒雅 | 唐宋 | 温润如玉，引经据典 | 「承蒙垂问，不胜感激。」 |
| ⚔️ 武侠 | 明清 | 快意恩仇，豪爽直率 | 「某家见过兄台。」 |
| 🗡️ 三国 | 汉末 | 运筹帷幄，兵法韬略 | 「主公，臣有一计。」 |
| 🏹 战国 | 先秦 | 纵横捭阖，气势磅礴 | 「大王，此事久拖不决！」 |
| 📖 史记 | 西汉 | 沉郁顿挫，太史公笔法 | 「太史公曰：悲夫！」 |
| 🎭 白话 | 明清 | 生动活泼，说书口吻 | 「话说回来——」 |
| 🌿 诗经 | 上古 | 古朴浑厚，四言为主 | 「蒹葭苍苍，白露为霜。」 |
| 🪷 禅意 | 唐宋 | 空灵淡远，机锋禅语 | 「施主，放下执念。」 |

### 安装

```bash
openclaw skills install wenyan
```

### 使用方式

```
切换三国风3        → 激活三国风格，强度 90%
切换武侠风         → 激活武侠风格，强度 60%（默认）
用文言说话         → 激活儒雅风格（默认）
退出古风           → 恢复正常模式
```

**语义退出**（不限关键词）：「够了」「算了」「太文了」「我听不懂」「换回来」

### 各智能体接入指南

wenyan 的核心是**纯 JSON 配置 + Python 引擎**，与任何模型框架解耦。

**通用三步法（适用一切智能体）：**

```bash
# ① 生成系统提示词（可直接粘贴进任何智能体的 system prompt / 系统指令）
python scripts/style_engine.py prompt sanguo

# ② 把生成的提示词设为该智能体的 system prompt（见下方各平台说明）
# ③ 用引擎校验/评分模型回复，确保风格达标（可选）
echo "你的回复文本" | python scripts/style_engine.py validate sanguo
echo "你的回复文本" | python scripts/style_engine.py score sanguo
```

**主要智能体配置方式：**

| 智能体 | 接入方法 |
|--------|----------|
| **OpenClaw** | `openclaw skills install wenyan`，对 AI 说「切换三国风3」即可 |
| **Claude（claude.ai / API）** | 生成 prompt → 粘贴进 **Settings → System prompt**，或作为 API 的 `system` 字段 |
| **ChatGPT（GPT-4 / GPT-5）** | 生成 prompt → 粘贴进 **Settings → Personalities / Custom instructions**，或用 Projects 的 Instructions |
| **Gemini / Grok / 其他 Web AI** | 生成 prompt → 粘贴进 **Settings → System instructions** |
| **Dify / Coze / FastGPT** | 生成 prompt → 填入应用的「系统提示词 / System Prompt」配置项 |
| **Ollama 本地模型** | 生成 prompt → 写入 Modelfile 的 `SYSTEM` 字段，或每次请求的 `system` 参数 |
| **Cursor / Cline / Continue 等代码助手** | 生成 prompt → 写入 `.cursorrules` / `clinerules` / `.continuerules` |
| **自定义 API 服务** | 生成 prompt → 作为 `system` 字段发给模型，回复后再用 `validate`/`score` 校验 |

**强度设计**

| 强度 | 代号 | 古文浓度 | 适用场景 |
|------|------|----------|----------|
| 🌿 浅度 | 1 | ~20% | 日常对话，夹带古文词汇 |
| 🎋 中度 | 2 | ~60% | 半文半白，保留现代逻辑 |
| 🏯 深度 | 3 | 90%+ | 全文古文，句式工整 |

### 技术架构

```
Layer 1: 风格参数化配置（JSON）→ Layer 2: 风格引擎（Python）→ Layer 3: 回归测试
```

### 许可证

MIT License。**但必须保留 Pondsi 的署名。** 详见 [LICENSE](LICENSE)。

---

## 繁體中文

### 什麼是 WenYan？

WenYan 是一個**通用的古風語體引擎**，提供 **8 種古中文風格**的精確控制。每種風格由獨立 JSON 配置定義，包含詞彙表、句式模板、稱謂體系、修辭約束和品質評分參數。

> **不限於 OpenClaw。** 任何支援 system prompt 的智慧體——Claude、ChatGPT、Gemini、Dify、Ollama 本機模型、Cursor、自訂 API——都能直接接入，詳見下方「[各智慧體接入指南](#各智慧體接入指南)」與 [assets/agents.md](assets/agents.md)。

**核心特性：**
- 🎯 **參數化風格控制**：每種風格 = 一個 JSON 檔案，修改無需改程式碼
- 🔍 **自動校驗**：禁用詞偵測、句長控制、風格漂移偵測
- 📊 **量化評分**：每次回覆自動評分，低於閾值自動修正
- 💾 **狀態永續化**：切換一次，持續生效，直到主動退出
- 🧪 **回歸測試**：內建測試框架，確保品質可量化

### 8 種風格

| 風格 | 時代 | 特徵 | 範例 |
|------|------|------|------|
| 📜 儒雅 | 唐宋 | 溫潤如玉，引經據典 | 「承蒙垂問，不勝感激。」 |
| ⚔️ 武俠 | 明清 | 快意恩仇，豪爽直率 | 「某家見過兄台。」 |
| 🗡️ 三國 | 漢末 | 運籌帷幄，兵法韜略 | 「主公，臣有一計。」 |
| 🏹 戰國 | 先秦 | 縱橫捭闔，氣勢磅礴 | 「大王，此事久拖不決！」 |
| 📖 史記 | 西漢 | 沉鬱頓挫，太史公筆法 | 「太史公曰：悲夫！」 |
| 🎭 白話 | 明清 | 生動活潑，說書口吻 | 「話說回來——」 |
| 🌿 詩經 | 上古 | 古樸渾厚，四言為主 | 「蒹葭蒼蒼，白露為霜。」 |
| 🪷 禪意 | 唐宋 | 空靈淡遠，機鋒禪語 | 「施主，放下執念。」 |

### 安裝

```bash
openclaw skills install wenyan
```

### 使用方式

```
切換三國風3        → 啟動三國風格，強度 90%
切換武俠風         → 啟動武俠風格，強度 60%（預設）
用文言說話         → 啟動儒雅風格（預設）
退出古風           → 恢復正常模式
```

**語義退出**（不限關鍵詞）：「夠了」「算了」「太文了」「我聽不懂」「換回來」

### 各智慧體接入指南

wenyan 的核心是**純 JSON 設定 + Python 引擎**，與任何模型框架解耦。

**通用三步法（適用一切智慧體）：**

```bash
# ① 產生系統提示詞（可直接貼進任何智慧體的 system prompt）
python scripts/style_engine.py prompt sanguo

# ② 把產生的提示詞設為該智慧體的 system prompt
# ③ 用引擎校驗/評分模型回覆（可選）
echo "你的回覆文字" | python scripts/style_engine.py validate sanguo
echo "你的回覆文字" | python scripts/style_engine.py score sanguo
```

**主要智慧體設定：**

| 智慧體 | 接入方法 |
|--------|----------|
| **OpenClaw** | `openclaw skills install wenyan`，對 AI 說「切換三國風3」 |
| **Claude（claude.ai / API）** | 產生 prompt → **Settings → System prompt**，或 API 的 `system` 欄位 |
| **ChatGPT（GPT-4 / GPT-5）** | 產生 prompt → **Settings → Personalities / Custom instructions** |
| **Gemini / Grok / 其他 Web AI** | 產生 prompt → **Settings → System instructions** |
| **Dify / Coze / FastGPT** | 產生 prompt → 填入「系統提示詞」設定項 |
| **Ollama 本機模型** | 產生 prompt → 寫入 Modelfile 的 `SYSTEM` 欄位，或請求的 `system` 參數 |
| **Cursor / Cline / Continue** | 產生 prompt → 寫入 `.cursorrules` / `clinerules` / `.continuerules` |
| **自訂 API 服務** | 產生 prompt → 作為 `system` 欄位發給模型，回覆後用 `validate`/`score` 校驗 |

### 強度設計

| 強度 | 代號 | 古文濃度 | 適用場景 |
|------|------|----------|----------|
| 🌿 淺度 | 1 | ~20% | 日常對話，夾帶古文詞彙 |
| 🎋 中度 | 2 | ~60% | 半文半白，保留現代邏輯 |
| 🏯 深度 | 3 | 90%+ | 全文古文，句式工整 |

### 許可證

MIT License。**但必須保留 Pondsi 的署名。** 詳見 [LICENSE](LICENSE)。

---

## English

### What is WenYan?

WenYan is a **universal classical Chinese style engine** providing **8 classical Chinese writing styles** with precise control. Each style is defined by an independent JSON configuration containing vocabulary, sentence templates, address systems, rhetoric constraints, and quality scoring parameters.

> **Not limited to OpenClaw.** Any agent with a system prompt — Claude, ChatGPT, Gemini, Dify, Ollama local models, Cursor, custom APIs — can plug in directly. See the [Per-Agent Integration Guide](#per-agent-integration-guide) below and [assets/agents.md](assets/agents.md).

**Key Features:**
- 🎯 **Parameterized style control**: Each style = one JSON file, no code changes needed
- 🔍 **Auto-validation**: Forbidden word detection, sentence length control, style drift detection
- 📊 **Quantified scoring**: Auto-scored per reply, auto-corrected below threshold
- 💾 **Persistent state**: Switch once, stays active until manually exited
- 🧪 **Regression testing**: Built-in test framework for measurable quality

### 8 Styles

| Style | Era | Character | Example |
|-------|-----|-----------|---------|
| 📜 Ruya | Tang/Song | Elegant scholar | "承蒙垂問，不勝感激。" |
| ⚔️ Wuxia | Ming/Qing | Martial hero | "某家見過兄台。" |
| 🗡️ Sanguo | Late Han | Strategic advisor | "主公，臣有一計。" |
| 🏹 Zhanguo | Pre-Qin | Diplomatic strategist | "大王，此事久拖不決！" |
| 📖 Shiji | Western Han | Grand Historian | "太史公曰：悲夫！" |
| 🎭 Baihua | Ming/Qing | Storyteller | "話說回來——" |
| 🌿 Shijing | Ancient | Four-character odes | "蒹葭蒼蒼，白露為霜。" |
| 🪷 Chan | Tang/Song | Zen master | "施主，放下執念。" |

### Installation

```bash
openclaw skills install wenyan
```

### Usage

```
Switch to Sanguo 3    → Activate Three Kingdoms style, intensity 90%
Switch to Wuxia       → Activate Martial style, intensity 60% (default)
Switch to Ruya        → Activate Scholar style (default)
Exit classical style  → Return to normal mode
```

**Semantic exit** (not limited to keywords): "enough", "stop", "too classical", "I don't understand"

### Per-Agent Integration Guide

WenYan's core is **pure JSON config + a Python engine** — fully decoupled from any model framework.

**Universal 3-step method (works with any agent):**

```bash
# ① Generate a system prompt (paste it into any agent's system prompt / system instructions)
python scripts/style_engine.py prompt sanguo

# ② Set that prompt as the agent's system prompt (see per-platform notes below)
# ③ Optionally validate/score the model's reply to ensure style compliance
echo "your reply text" | python scripts/style_engine.py validate sanguo
echo "your reply text" | python scripts/style_engine.py score sanguo
```

**Major agent setups:**

| Agent | Integration |
|-------|-------------|
| **OpenClaw** | `openclaw skills install wenyan`, then tell the AI "Switch to Sanguo 3" |
| **Claude (claude.ai / API)** | Generate prompt → paste into **Settings → System prompt**, or use as the API `system` field |
| **ChatGPT (GPT-4 / GPT-5)** | Generate prompt → paste into **Settings → Personalities / Custom instructions**, or use Projects Instructions |
| **Gemini / Grok / other Web AI** | Generate prompt → paste into **Settings → System instructions** |
| **Dify / Coze / FastGPT** | Generate prompt → fill into the app's "System Prompt" setting |
| **Ollama local models** | Generate prompt → write into the Modelfile `SYSTEM` field, or send as the `system` parameter per request |
| **Cursor / Cline / Continue** | Generate prompt → write into `.cursorrules` / `clinerules` / `.continuerules` |
| **Custom API services** | Generate prompt → send as the `system` field to the model, then `validate`/`score` the reply |

**Intensity Levels**

| Level | Code | Classical Ratio | Use Case |
|-------|------|-----------------|----------|
| 🌿 Light | 1 | ~20% | Daily chat with classical flavor |
| 🎋 Medium | 2 | ~60% | Semi-classical, modern logic preserved |
| 🏯 Deep | 3 | 90%+ | Full classical, structured sentences |

| Level | Code | Classical Ratio | Use Case |
|-------|------|-----------------|----------|
| 🌿 Light | 1 | ~20% | Daily chat with classical flavor |
| 🎋 Medium | 2 | ~60% | Semi-classical, modern logic preserved |
| 🏯 Deep | 3 | 90%+ | Full classical, structured sentences |

### License

MIT License. **Attribution to Pondsi is required.** See [LICENSE](LICENSE).

---

## 日本語

### WenYan とは？

WenYan は**汎用の古典中国語スタイルエンジン**で、**8種の古典中国語スタイル**を精密に制御します。各スタイルは独立した JSON 設定で定義されており、語彙、句テンプレート、敬称体系、修辞制約、品質評価パラメータを含みます。

**主な機能：**
- 🎯 **パラメータ化スタイル制御**：各スタイル = 1つの JSON ファイル
- 🔍 **自動検証**：禁止語検出、文長制御、スタイルドリフト検出
- 📊 **数値化スコアリング**：返答ごとに自動スコアリング
- 💾 **状態永続化**：一度切り替えたら、手動で終了するまで維持
- 🧪 **リグレッションテスト**：品質の数値化を保証

### 8つのスタイル

| スタイル | 時代 | 特徴 | 例 |
|----------|------|------|-----|
| 📜 儒雅 | 唐宋 | 温雅な学者風 | 「承蒙垂問，不勝感激。」 |
| ⚔️ 武侠 | 明清 | 江湖の侠客風 | 「某家見過兄台。」 |
| 🗡️ 三国 | 漢末 | 軍師の戦略風 | 「主公，臣有一計。」 |
| 🏹 战国 | 先秦 | 縦横家の雄弁風 | 「大王，此事久拖不決！」 |
| 📖 史記 | 西漢 | 太史公の筆法 | 「太史公曰：悲夫！」 |
| 🎭 白話 | 明清 | 説明口調 | 「話說回來——」 |
| 🌿 詩経 | 上古 | 四言の古朴風 | 「蒹葭蒼蒼，白露為霜。」 |
| 🪷 禅意 | 唐宋 | 禅の空霊風 | 「施主，放下執念。」 |

### インストール

```bash
openclaw skills install wenyan
```

### 使い方

```
三國風3に切替      → 三国スタイル激活、強度90%
武侠風に切替        → 武侠スタイル激活、強度60%（デフォルト）
文言で说话          → 儒雅スタイル激活（デフォルト）
古風を退出          → 通常モードに戻る
```

**意味による退出**（キーワードに限定されない）：「夠了」「算了」「太文了」「我聽不懂」

### エージェント別統合ガイド

wenyan の中核は**純 JSON 設定 + Python エンジン**で、いかなるモデルフレームワークとも解耦されています。

**汎用3ステップ（あらゆるエージェントに適用）：**

```bash
# ① システムプロンプト生成（あらゆるエージェントの system prompt に貼り付け可）
python scripts/style_engine.py prompt sanguo

# ② そのプロンプトをエージェントの system prompt として設定
# ③ 必要に応じてモデルの返答を検証/採点
echo "あなたの返信テキスト" | python scripts/style_engine.py validate sanguo
echo "あなたの返信テキスト" | python scripts/style_engine.py score sanguo
```

**主要エージェント設定：**

| エージェント | 統合方法 |
|--------------|----------|
| **OpenClaw** | `openclaw skills install wenyan`、AIに「三國風3に切替」と言う |
| **Claude（claude.ai / API）** | prompt 生成 → **Settings → System prompt** に貼り付け、または API の `system` フィールドに使用 |
| **ChatGPT（GPT-4 / GPT-5）** | prompt 生成 → **Settings → Personalities / Custom instructions** に貼り付け |
| **Gemini / Grok / その他 Web AI** | prompt 生成 → **Settings → System instructions** に貼り付け |
| **Dify / Coze / FastGPT** | prompt 生成 → アプリの「システムプロンプト」設定に記入 |
| **Ollama 地元モデル** | prompt 生成 → Modelfile の `SYSTEM` フィールドに記入、またはリクエスト毎の `system` パラメータ |
| **Cursor / Cline / Continue** | prompt 生成 → `.cursorrules` / `clinerules` / `.continuerules` に記入 |
| **カスタム API サービス** | prompt 生成 → `system` フィールドとしてモデルに送信、返答後は `validate`/`score` で検証 |

### ライセンス

MIT ライセンス。**Pondsi の帰属表示が必要です。** 詳細は [LICENSE](LICENSE)。

---

## 한국어

### WenYan이란?

WenYan은**범용 고전 중국어 스타일 엔진**으로, **8가지 고전 중국어 스타일**을 정밀하게 제어합니다. 각 스타일은 독립적인 JSON 설정으로 정의되며, 어휘, 문장 템플릿, 호칭 체계, 수사적 제약, 품질 점수 매개변수를 포함합니다.

**주요 기능:**
- 🎯 **매개변수화 스타일 제어**: 각 스타일 = 하나의 JSON 파일
- 🔍 **자동 검증**: 금지어 감지, 문장 길이 제어, 스타일 이탈 감지
- 📊 **정량화된 점수**: 응답마다 자동 점수 매기기
- 💾 **상태 영속화**: 한 번 전환하면 수동으로 종료할 때까지 유지
- 🧪 **회귀 테스트**: 내장 테스트 프레임워크

### 8가지 스타일

| 스타일 | 시대 | 특징 | 예시 |
|--------|------|------|------|
| 📜 유아 | 당/송 | 온화한 학자풍 | "承蒙垂問，不勝感激。" |
| ⚔️ 무협 | 명/청 | 강호의 협객풍 | "某家見過兄台。" |
| 🗡️ 삼국 | 한말 | 군사의 전략풍 | "主公，臣有一計。" |
| 🏹 전국 | 선진 | 종횡가의 웅변풍 | "大王，此事久拖不決！" |
| 📖 사기 | 서한 | 태사공의 필법 | "太史公曰：悲夫！" |
| 🎭 백화 | 명/청 | 설명 구調 | "話說回來——" |
| 🌿 시경 | 상고 | 사언의 고박풍 | "蒹葭蒼蒼，白露為霜。" |
| 🪷 선의 | 당/송 | 선의 공령풍 | "施主，放下執念。" |

### 설치

```bash
openclaw skills install wenyan
```

### 사용법

```
삼국풍3으로 전환    → 삼국 스타일 활성화, 강도 90%
무협풍으로 전환      → 무협 스타일 활성화, 강도 60% (기본)
문언으로 말하기      → 유아 스타일 활성화 (기본)
고풍 모드 종료       → 정상 모드로 복귀
```

**의미적 종료** (키워드에 국한되지 않음): "够了", "算了", "太文了", "我聽不懂"

### 에이전트별 통합 가이드

wenyan 의 코어는**순수 JSON 설정 + Python 엔진**이며, 모든 모델 프레임워크와 분리되어 있습니다.

**범용 3단계 (모든 에이전트에 적용):**

```bash
# ① 시스템 프롬프트 생성 (모든 에이전트의 system prompt 에 붙여넣기 가능)
python scripts/style_engine.py prompt sanguo

# ② 해당 프롬프트를 에이전트의 system prompt 로 설정
# ③ 필요 시 모델의 응답을 검증/점수 매기기
echo "귀하의 응답 텍스트" | python scripts/style_engine.py validate sanguo
echo "귀하의 응답 텍스트" | python scripts/style_engine.py score sanguo
```

**주요 에이전트 설정:**

| 에이전트 | 통합 방법 |
|----------|----------|
| **OpenClaw** | `openclaw skills install wenyan`, AI 에게 "삼국풍3으로 전환" |
| **Claude (claude.ai / API)** | prompt 생성 → **Settings → System prompt** 에 붙여넣기, 또는 API 의 `system` 필드 사용 |
| **ChatGPT (GPT-4 / GPT-5)** | prompt 생성 → **Settings → Personalities / Custom instructions** 에 붙여넣기 |
| **Gemini / Grok / 기타 Web AI** | prompt 생성 → **Settings → System instructions** 에 붙여넣기 |
| **Dify / Coze / FastGPT** | prompt 생성 → 앱의 "시스템 프롬프트" 설정에 입력 |
| **Ollama 로컬 모델** | prompt 생성 → Modelfile 의 `SYSTEM` 필드에 입력, 또는 요청별 `system` 파라미터 |
| **Cursor / Cline / Continue** | prompt 생성 → `.cursorrules` / `clinerules` / `.continuerules` 에 입력 |
| **사용자 정의 API 서비스** | prompt 생성 → `system` 필드로 모델에 전송, 응답 후 `validate`/`score` 로 검증 |

### 라이선스

MIT 라이선스. **Pondsi의 저작자 표시가 필요합니다.** 자세한 내용은 [LICENSE](LICENSE) 참조.

---

## Français

### Qu'est-ce que WenYan ?

WenYan est un **moteur de style chinois classique universel** offrant **8 styles d'écriture chinois classiques** avec un contrôle précis. Chaque style est défini par une configuration JSON indépendante contenant le vocabulaire, les modèles de phrases, le système d'adresses, les contraintes rhétoriques et les paramètres de notation qualité.

**Fonctionnalités clés :**
- 🎯 **Contrôle de style paramétré** : Chaque style = un fichier JSON
- 🔍 **Validation automatique** : Détection de mots interdits, contrôle de longueur
- 📊 **Notation quantifiée** : Note automatique par réponse
- 💾 **État persistant** : Activez une fois, maintenu jusqu'à désactivation
- 🧪 **Tests de régression** : Framework de test intégré

### 8 Styles

| Style | Époque | Caractère | Exemple |
|-------|--------|-----------|---------|
| 📜 Ruya | Tang/Song | Lettré élégant | "承蒙垂問，不勝感激。" |
| ⚔️ Wuxia | Ming/Qing | Héros martial | "某家見過兄台。" |
| 🗡️ Sanguo | Fin Han | Conseiller stratégique | "主公，臣有一計。" |
| 🏹 Zhanguo | Avant Qin | Stratégue diplomatique | "大王，此事久拖不決！" |
| 📖 Shiji | Han occidental | Grand Historien | "太史公曰：悲夫！" |
| 🎭 Baihua | Ming/Qing | Conteur | "話說回來——" |
| 🌿 Shijing | Ancien | Odes à quatre caractères | "蒹葭蒼蒼，白露為霜。" |
| 🪷 Chan | Tang/Song | Maître Zen | "施主，放下執念。" |

### Installation

```bash
openclaw skills install wenyan
```

### Utilisation

```
Passer en Sanguo 3   → Activer le style Trois Royaumes, intensité 90%
Passer en Wuxia      → Activer le style Martial, intensité 60% (défaut)
Passer en Ruya       → Activer le style Lettré (défaut)
Quitter le style     → Retour au mode normal
```

**Sortie sémantique** (pas limitée aux mots-clés) : "assez", "arrête", "trop classique"

### Guide d'intégration par agent

Le cœur de wenyan est une **config JSON pure + un moteur Python** — totalement découplé de tout framework de modèle.

**Méthode universelle en 3 étapes (tous agents) :**

```bash
# ① Générer le prompt système (à coller dans le system prompt de tout agent)
python scripts/style_engine.py prompt sanguo

# ② Définir ce prompt comme system prompt de l'agent
# ③ Valider/noter la réponse du modèle si nécessaire
echo "votre texte de réponse" | python scripts/style_engine.py validate sanguo
echo "votre texte de réponse" | python scripts/style_engine.py score sanguo
```

**Configurations principales :**

| Agent | Intégration |
|-------|-------------|
| **OpenClaw** | `openclaw skills install wenyan`, dire à l'AI "Passer en Sanguo 3" |
| **Claude (claude.ai / API)** | Générer le prompt → coller dans **Settings → System prompt**, ou champ `system` de l'API |
| **ChatGPT (GPT-4 / GPT-5)** | Générer le prompt → coller dans **Settings → Personalities / Custom instructions** |
| **Gemini / Grok / autre Web AI** | Générer le prompt → coller dans **Settings → System instructions** |
| **Dify / Coze / FastGPT** | Générer le prompt → remplir le champ "System Prompt" de l'app |
| **Ollama (modèles locaux)** | Générer le prompt → écrire dans le champ `SYSTEM` du Modelfile, ou paramètre `system` par requête |
| **Cursor / Cline / Continue** | Générer le prompt → écrire dans `.cursorrules` / `clinerules` / `.continuerules` |
| **Services API personnalisés** | Générer le prompt → envoyer comme champ `system` au modèle, puis `validate`/`score` la réponse |

### Licence

MIT License. **L'attribution à Pondsi est requise.** Voir [LICENSE](LICENSE).

---

## Esperanto

### Kio estas WenYan?

WenYan estas **universala klasika ĉina skribskra-stil-motoro** ofertanta **8 stilojn de klasika ĉina skribado** kun preciza regado. Ĉiu stilo estas difinita per sendependa JSON-agordado enhavanta vortaron, frazajn ŝablonojn, adres-sistemon, retorikajn limojn kaj kvalitajn parametrojn.

**Ĉefaj ecoj:**
- 🎯 **Parametra stila regado**: Ĉiu stilo = unu JSON-dosiero
- 🔍 **Aŭtomata validado**: Detekto de malpermesitaj vortoj
- 📊 **Kvantigita poentado**: Aŭtomata poentado por ĉiu respondo
- 💾 **Daŭrigebla stato**: Ŝanĝu unufoje, daŭrigas ĝis mana ĉeso
- 🧪 **Regrupa testo**: Enkonstruita testo- kadro

### 8 Stiloj

| Stilo | Epoko | Karaktero | Ekzemplo |
|-------|-------|-----------|----------|
| 📜 Ruya | Tang/Song | Elekta scholaro | "承蒙垂問，不勝感激。" |
| ⚔️ Wuxia | Ming/Qing | Martia heroo | "某家見過兄台。" |
| 🗡️ Sanguo | Fino de Han | Konsilisto strategia | "主公，臣有一計。" |
| 🏹 Zhanguo | Antaŭ Qin | Diplomata strategiisto | "大王，此事久拖不決！" |
| 📖 Shiji | Okcidenta Han | Granda Historiisto | "太史公曰：悲夫！" |
| 🎭 Baihua | Ming/Qing | Rakontisto | "話說回來——" |
| 🌿 Shijing | Antikva | Kvar-silabaj odoj | "蒹葭蒼蒼，白露為霜。" |
| 🪷 Chan | Tang/Song | Zen-majstro | "施主，放下執念。" |

### Instalado

```bash
openclaw skills install wenyan
```

### Uzo

```
Ŝanĝi al Sanguo 3   → Aktivigi tri-reĝaĵojn stilon, intenseco 90%
Ŝanĝi al Wuxia      → Aktivigi martian stilon, intenseco 60% (apriora)
Ŝanĝi al Ruya       → Aktivigi scholaran stilon (apriora)
Eliri klasikaĵon    → Reiri al normala reĝimo
```

**Signifa eliro** (ne limigita al ŝlosilvortoj): "sufiĉas", "ĉesu", "tro klasika"

### Agenta integrado-gvidilo

La kerno de wenyan estas **pura JSON-agordo + Python-motoro** — tute malkupligita de iu ajn modela frameworko.

**Universala 3-ŝtapa metodo (ĉiuj agintoj) :**

```bash
# ① Generi sisteman prompton (gluiti en la system prompt de iu ajn aginto)
python scripts/style_engine.py prompt sanguo

# ② Fari tiun prompton la system prompt de la aginto
# ③ Validi/skori la respondon de la modelo se necese
echo "via responda teksto" | python scripts/style_engine.py validate sanguo
echo "via responda teksto" | python scripts/style_engine.py score sanguo
```

**Ĉefaj agentoj :**

| Aginto | Integraĵo |
|--------|-----------|
| **OpenClaw** | `openclaw skills install wenyan`, diri al la AI "Ŝanĝi al Sanguo 3" |
| **Claude (claude.ai / API)** | Generi prompton → glui en **Settings → System prompt**, aŭ kiel la `system`-kampo de la API |
| **ChatGPT (GPT-4 / GPT-5)** | Generi prompton → glui en **Settings → Personalities / Custom instructions** |
| **Gemini / Grok / aliaj Web-AI** | Generi prompton → glui en **Settings → System instructions** |
| **Dify / Coze / FastGPT** | Generi prompton → enigi en la "System Prompt"-agordo de la aplikativo |
| **Ollama (lokaj modeloj)** | Generi prompton → skribi en la `SYSTEM`-kampo de Modelfile, aŭ kiel `system`-parametro per peto |
| **Cursor / Cline / Continue** | Generi prompton → skribi en `.cursorrules` / `clinerules` / `.continuerules` |
| **Propraj API-servoj** | Generi prompton → sendi kiel `system`-kampojn al la modelo, poste `validate`/`score` la respondo |

### Licenco

MIT Licenco. **Atribuo al Pondsi estas bezonata.** Vidu [LICENSE](LICENSE).

---

**Made with ❤️ by [Pondsi](https://github.com/Pondsi)**
