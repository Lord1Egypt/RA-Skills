<p align="center">
  <a href="README.md">English</a> |
  <a href="README_CN.md">中文</a> |
  <a href="README_JA.md">日本語</a> |
  <a href="README_FR.md">Français</a> |
  <a href="README_RU.md">Русский</a>
</p>

<p align="center">
  <h1 align="center">量子リサーチラボ</h1>
  <p align="center">
    <strong>マルチエージェント 量子戦略 R&D フレームワーク</strong>
  </p>
  <p align="center">
    トップクオンツファームをモデルにした15の専門LLMエージェント
  </p>
</p>

<p align="center">
  <a href="https://github.com/anthropics/claude-code" target="_blank"><img alt="Claude Code" src="https://img.shields.io/badge/Claude_Code-Compatible-D97706?logo=anthropic&logoColor=white"/></a>
  <a href="https://hermes.nousresearch.com" target="_blank"><img alt="Hermes Agent" src="https://img.shields.io/badge/Hermes_Agent-Skill-7C3AED?logo=data:image/svg+xml;base64,..." /></a>
  <img alt="Roles" src="https://img.shields.io/badge/Roles-15-blue" />
  <img alt="Pipeline Tracks" src="https://img.shields.io/badge/Pipeline_Tracks-8-green" />
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" /></a>
</p>

---

> **量子リサーチラボ**は、LLMベースのコーディングエージェントに機関投資家レベルの量化戦略研究ワークフローをもたらすAIエージェントスキルです。トップクオンツファーム（Goldman Sachs、Renaissance Technologies、Two Sigma、Citadel、Jane Streetなど）の専門知識をモデルにした15の専門エージェントを展開し、協力して量化トレーディング戦略の設計、バックテスト、リスク管理、検証を行います。

> ⚠️ **免責事項**: 本フレームワークは**研究および教育目的**でのみ設計されています。金融、投資、またはトレーディングに関する助言を構成するものではありません。トレーディングのパフォーマンスは、モデルの選択、データ品質、市場状況など多くの要因に依存します。必ずご自身でデューデリジェンスを行ってください。

---

## 目次

- [フレームワーク概要](#フレームワーク概要)
- [15のロール](#15のロール)
- [パイプラインアーキテクチャ](#パイプラインアーキテクチャ)
- [インストール](#インストール)
- [使用方法](#使用方法)
- [品質ゲート](#品質ゲート)
- [ステート管理](#ステート管理)
- [プロジェクト構成](#プロジェクト構成)
- [コントリビューション](#コントリビューション)
- [ライセンス](#ライセンス)

---

## フレームワーク概要

量子リサーチラボは、実際のクオンツトレーディングファームの運用方法を反映しています。複雑な戦略研究を専門ロールに分解し、それぞれが異なる機関投資家の視点から専門知識を提供します。本フレームワークは2つのモードでこれらのロールをオーケストレーションします：

- **ツールボックスモード** — 目的別に個々のロールをオンデマンドで呼び出す
- **パイプラインモード** — 事前設定されたトラック（ロールのシーケンス）を実行し、エンドツーエンドの戦略研究を行う

```
┌─────────────────────────────────────────────────────────────┐
│                    Quant Research Lab                        │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Strategy  │→ │ Backtest │→ │   Risk   │→ │  Alpha   │   │
│  │ Architect │  │  Engine  │  │ Manager  │  │Researcher│   │
│  │ (GS)      │  │ (RenTech)│  │ (Two σ)  │  │ (Citadel)│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│       │              │             │              │         │
│       ▼              ▼             ▼              ▼         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Execution │  │  Factor  │  │ Stat Arb │  │  Macro   │   │
│  │ Algo     │  │  Model   │  │(D.E.Shaw)│  │(Bridge-  │   │
│  │ (Virtu)  │  │  (AQR)   │  │          │  │ water)   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│       │              │             │              │         │
│       ▼              ▼             ▼              ▼         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Data Pipe │  │    ML    │  │Portfolio │  │ Trading  │   │
│  │ (Bloomberg)│ │Researcher│  │Optimizer │  │ System   │   │
│  │          │  │(Point72) │  │(Man Grp) │  │(Millenn.)│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │Factor Backtest│  │  Compliance  │                        │
│  │(Dimensional)  │  │    (GS)      │                        │
│  └──────────────┘  └──────────────┘                        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Quality Gate System                     │   │
│  │  Required Fields │ Numerical Sanity │ Dual Signatures│   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 15のロール

各エージェントは、そのペルソナ、専門知識、および構造化された多次元タスク仕様を定義する詳細なプロンプトテンプレートによって裏付けられています。汎用的な「アシスタント」は存在せず、すべてのエージェントが関連する機関のスタイルで思考し出力を行います。

| ID | ロール | 機関 | 依存先 | 複雑度 | フェーズ |
|:---|:-----|:------------|:-----------|:-----------|:------|
| 01 | **Strategy Architect** | Goldman Sachs | — | High | 1 |
| 02 | **Backtest Engine** | Renaissance Technologies | 01 | Normal | 1 |
| 03 | **Risk Manager** | Two Sigma | 01 | Normal | 1 |
| 04 | **Alpha Researcher** | Citadel | — | High | 1 |
| 05 | **Market Maker** | Jane Street | 01 | Normal | 3 |
| 06 | **Factor Model Builder** | AQR | 02 | Normal | 2 |
| 07 | **Statistical Arbitrage** | D.E. Shaw | 01 | Normal | 2 |
| 08 | **Macro Strategy** | Bridgewater Associates | 01 | Normal | 3 |
| 09 | **Data Pipeline** | Bloomberg | — | Normal | 2 |
| 10 | **Execution Algorithm** | Virtu Financial | 01 | Normal | 1 |
| 11 | **ML Researcher** | Point72 | 01 | High | 3 |
| 12 | **Portfolio Optimizer** | Man Group | 01,02,03,06 | Normal | 2 |
| 13 | **Trading System** | Millennium Management | 10,12 | Normal | 2 |
| 14 | **Factor Backtester** | Dimensional Fund Advisors | 01 | Normal | 3 |
| 15 | **Compliance Framework** | Goldman Sachs | 13 | Normal | 3 |

### ロールのハイライト

**Strategy Architect (01)** — 戦略設計の9つの次元をカバー：テーゼ、銘柄選定、シグナル生成、エントリー/イグジットルール、ポジションサイジング、リスクパラメータ、実装仕様。すべての決定は数式と疑似コードによって裏付けられています。

**Backtest Engine (02)** — データ品質、エンジンアーキテクチャ、取引コストモデリング（Almgren-Chriss）、統計的厳密性（Deflated Sharpe Ratio、False Discovery Rate）、ウォークフォワードテストを含む10次元の検証フレームワーク。

**Risk Manager (03)** — 多層リスク評価：マーケットリスク（VaR/CVaR）、流動性リスク、カウンターパーティリスク、テールリスク（EVT）。歴史的な危機から抽出されたストレステストシナリオを含みます。

**Alpha Researcher (04)** — IC/ICIR分析、シグナル減衰モデリング、多次元直交化を備えたアルファシグナル発見パイプライン。

**Factor Model Builder (06)** — Barraスタイルのファクターモデル構築：アルファファクター、リスクファクター、ファクター共分散推定、ファクターベースの帰属分析。

**ML Researcher (11)** — エンドツーエンドのMLパイプライン：特徴量エンジニアリング、モデル選択（XGBoost/LSTM/Transformer）、ハイパーパラメータ最適化、本番環境デプロイメント仕様。

---

## パイプラインアーキテクチャ

ロールは**有向非巡回グラフ（DAG）**を構成し、単純な直列チェーンではありません。異なる研究シナリオでは異なるトラックを使用します：

| トラック | トリガーフレーズ | ロールシーケンス | 推定時間 | ユースケース |
|:------|:---------------|:--------------|:----------|:---------|
| **Core**（デフォルト） | "启动流水线"（パイプライン起動）/ "pipeline" | 01→02→03→04→10 | 約15分 | 標準：設計→バックテスト→リスク→アルファ→執行 |
| **Factor** | "因子流水线"（ファクターパイプライン） | 01→02→06→14→12 | 約20分 | ファクター研究：構築→バックテスト→検証→最適化 |
| **Execution** | "执行流水线"（執行パイプライン） | 01→10→13→15 | 約18分 | システムデプロイ：アルゴ→トレーディングシステム→コンプライアンス |
| **Macro** | "宏观流水线"（マクロパイプライン） | 01→08→03→12 | 約18分 | マクロ戦略＋リスク＋ポートフォリオ配分 |
| **Stat Arb** | "套利流水线"（裁定パイプライン） | 01→07→02→10 | 約18分 | ペアトレーディング／共積分戦略 |
| **ML** | "ML流水线"（MLパイプライン） | 01→11→02→03 | 約18分 | ML駆動の戦略開発 |
| **Market Making** | "做市流水线"（マーケットメイキングパイプライン） | 01→05→10→13 | 約18分 | マーケットメイキングシステム設計 |
| **Full** | "全量流水线"（フルパイプライン） | 01→...→15 | 約40分 | 完全なエンドツーエンド（注意して使用） |

### パイプラインの機能

- **ブレイクポイント再開** — 任意のロールで一時停止し、後で中断した箇所から再開可能
- **再実行** — 任意のロールから再実行し、下流の出力を破棄
- **カスタムトラック** — 独自のロールシーケンスを定義（例：「01→04→11を実行」）
- **厳密モード** — 品質ゲートの警告で自動継続ではなく停止
- **進捗追跡** — 各ロールの品質ゲートステータスを含むリアルタイム進捗表示

---

## インストール

### 方法1：ワンライナーインストール（推奨）

```bash
npx skills add https://github.com/yili1992/quant-research-lab --skill quant-research-lab
```

### 方法2：以下のテキストを Claude Code に貼り付ける

> `quant-research-lab` スキルをインストールしてください。以下の手順に従ってください：
>
> 1. カレントプロジェクトの `.claude/skills/` ディレクトリが存在することを確認（なければ作成）
> 2. `git clone https://github.com/yili1992/quant-research-lab.git .claude/skills/quant-research-lab` を実行
> 3. 確認：`ls .claude/skills/quant-research-lab/` で `SKILL.md`、`roles/`、`pipelines/` が表示されること
> 4. インストール完了を報告。以降、定量研究のニーズを述べるとこのスキルが自動的に発動します

上記を Claude Code に貼り付けてください。

### 方法3：手動コマンドライン

```bash
git clone https://github.com/yili1992/quant-research-lab.git ~/.hermes/skills/quant-research-lab
```

### 方法4：スタンドアロンリファレンスとして

`roles/` 内のロールテンプレートは、フレームワークなしで任意のLLM向けの高品質なシステムプロンプトとして独立して使用できます。各 `.md` ファイルは、ペルソナ、タスク仕様、出力フォーマット要件を含む自己完結型のファイルです。

### トリガー

インストール後、定量研究のニーズを記述するとスキルが自動的に発動します：

- 「バックテストを実行して」→ バックテストエンジンを発動
- 「クオンツパイプラインを起動」→ パイプライン選択メニューを表示
- 「factor pipeline」→ ファクター研究トラックを開始
- 「ゴールドマンの役割を使って」→ ツールボックスモード

---

## 使用方法

### 自然言語トリガー

量化研究のニーズを記述すると、スキルが自動的に起動します：

```
"帮我设计一个费率套利策略"（手数料裁定戦略を設計して）           → Strategy Architect (01) を起動
"做一下这个策略的回测"（この戦略のバックテストをして）               → Backtest Engine (02) を起動
"启动量化流水线"（量化パイプラインを起動）                     → トラック選択メニューを表示
"因子流水线"（ファクターパイプライン）                         → Factorトラックを開始
"从角色 03 恢复"（ロール03から再開）                     → Risk Managerからパイプラインを再開
"用高盛角色"（ゴールドマン役で） / "做回测"（バックテスト） / "风控分析"（リスク分析）  → 特定ロールのツールボックスモード
"流水线进度"（パイプライン進捗） / "status"              → 現在のパイプライン進捗を表示
"重置流水线"（パイプラインリセット） / "reset"               → パイプラインの状態をリセット
```

### ツールボックスモード

フルパイプラインを実行せずに、個々のロールを使って目的別分析を行います：

1. ロール名を言うか、タスクを記述する
2. スキルが適切なロールにマッチし、テンプレートをロードしてサブエージェントをディスパッチする
3. 結果は品質ゲート注釈付きで `state/research-context.md` に保存される
4. このロールに依存する下流ロールが次のステップとして提案される

### パイプラインモード

エンドツーエンドの研究トラックを実行します：

1. トラックを選択する（またはスキルがゴールに基づいて提案する）
2. 実行計画を確認する：ロールシーケンス、推定時間、依存関係グラフ
3. 確認して開始 — ロールは自動コンテキスト受け渡しで順次実行される
4. `[1/5] 01 Strategy Architect ✅ [QAGATE: PASS]` スタイルの出力で進捗を監視
5. 「暂停」でいつでも一時停止、「从角色 NN 恢复」で後から再開可能

---

## 品質ゲート

すべてのロール出力は、パイプラインに受け入れられる前に自動品質チェックを受けます：

| チェック | スコープ | 検出内容 | 失敗時の動作 |
|:------|:------|:----------------|:-----------|
| **必須フィールド** | 全ロール | `[QAGATE]` ブロックの欠落、コア結論の空白、下流フィールドの欠落 | `[输出不完整]` |
| **数値の健全性** | Backtest/Risk/Factor ロール | Sharpe > 50、MaxDD > -99%、または他の非現実的な値 | `[数值极端异常]` |
| **デュアルシグネチャ** | 数値ロール | `method_signature` または `data_signature` の欠落 | `[缺少签名]` |

各ロールの出力に埋め込まれるQAGATEブロックは、構造化された品質レポートとして機能します：

```
[QAGATE]
core_conclusion: Strategy achieves Sharpe 1.8 with 12% max drawdown
key_params: lookback=20, threshold=2.0σ, rebalance=weekly
downstream_fields: signal_formula, entry_rules, risk_params
method_signature: momentum_zscore_v1
data_signature: binance_btcusdt_perp_2023_2025
[/QAGATE]
```

---

## ステート管理

パイプラインの状態は `state/research-context.md` に永続化されます — YAMLフロントマターを持つ単一のMarkdownファイルです：

```yaml
---
pipeline_id: btc-arb-20260504
pipeline_track: "核心流水线"
status: in-progress
current_role_id: "03"
completed_roles: ["01", "02"]
next_recovery: "04"
created_at: 2026-05-04T02:16:00Z
project: btc-arb
---
```

各ロールの完全な出力は `<!-- ROLE_OUTPUT_START:{ID} -->` と `<!-- ROLE_OUTPUT_END:{ID} -->` マーカーの間に追記され、以下の機能を実現します：

- **再開可能性** — セッションを閉じて後で戻っても、中断した箇所から再開可能
- **選択的再実行** — 特定ロールの出力を破棄して再実行
- **ロール間コンテキスト** — 下流のロールは自動的に上流のパラメータと結論を受け取る
- **監査証跡** — 品質ゲート結果を含む各ロールの出力の完全な履歴

---

## プロジェクト構成

```
quant-research-lab/
├── SKILL.md                          # Skill definition & orchestration logic
├── README.md                         # This file
├── LICENSE                           # MIT License
├── roles/                            # Role prompt templates
│   ├── 01-gs-strategy-architect.md   # Goldman Sachs Strategy Architect
│   ├── 02-rentec-backtest-engine.md  # Renaissance Technologies Backtest Engine
│   ├── 03-twosigma-risk-manager.md   # Two Sigma Risk Manager
│   ├── 04-citadel-alpha-researcher.md# Citadel Alpha Researcher
│   ├── 05-js-market-maker.md         # Jane Street Market Maker
│   ├── 06-aqr-factor-builder.md      # AQR Factor Model Builder
│   ├── 07-deshaw-stat-arb.md         # D.E. Shaw Statistical Arbitrage
│   ├── 08-bridgewater-macro.md       # Bridgewater Macro Strategy
│   ├── 09-bbg-data-pipeline.md       # Bloomberg Data Pipeline
│   ├── 10-virtu-execution.md         # Virtu Execution Algorithm
│   ├── 11-point72-ml-researcher.md   # Point72 ML Researcher
│   ├── 12-man-portfolio-optimizer.md # Man Group Portfolio Optimizer
│   ├── 13-millennium-trading-system.md # Millennium Trading System
│   ├── 14-dimensional-factor-backtest.md # Dimensional Factor Backtest
│   └── 15-gs-compliance.md           # Goldman Sachs Compliance Framework
├── state/                            # Pipeline state (auto-generated)
│   └── research-context.md
└── docs/                             # Design documents & specs
    └── superpowers/
```

---

## 内部動作の仕組み

1. **スキル起動** — 自然言語マッチングまたは明示的な `/quant-research-lab` トリガー
2. **コンテキスト収集** — ロールレジストリを読み取り、既存のパイプライン状態を確認し、ユーザー入力（市場、資金、焦点）を収集
3. **テンプレート読み込み** — 対象ロールの `.md` ファイルを読み取り、完全なプロンプトテンプレートを取得
4. **プレースホルダー置換** — `{user_market}`、`{user_capital}`、`{user_focus}`、`{upstream_params}`、`{upstream_summary}` を収集済みの値で置換
5. **サブエージェントディスパッチ** — 完成したプロンプトで専用サブエージェントを生成（高複雑度ロールはOpus、通常はSonnet）
6. **品質ゲート評価** — QAGATEブロックをパースし、3つの自動チェックを実行
7. **ステート永続化** — マーカー付きでステートファイルに出力を追記し、フロントマターを更新
8. **次ステップ提案** — 依存グラフをスキャンし、次の論理的ロールを提案

---

## コントリビューション

コントリビューションを歓迎します！以下の方法で貢献できます：

### 新しいロールの追加

1. 既存のテンプレート構造に従って `roles/NN-your-role.md` を作成：
   - **ペルソナ**セクション：機関の背景、専門分野、作業哲学
   - **タスク説明**セクション：具体的な量化要件を含む番号付き次元
   - **出力フォーマット**セクション：テーブル、数式、疑似コードを含む構造化Markdown
   - **QAGATE**セクション：必須フィールドと品質基準
2. `SKILL.md` のレジストリテーブルにロールを追加
3. `depends_on` 関係を定義し、`Phase`（1/2/3）を割り当て

### 新しいパイプライントラックの追加

1. 依存DAGに基づいてロールシーケンスを定義
2. `SKILL.md` のトラックテーブルに追加
3. 自然言語マッチング用のトリガーキーワードを追加

### 既存ロールの改善

各ロールテンプレートは機関投資家レベルの出力を生成するように設計されています。以下の分野での改善を歓迎します：
- より精密な数学的仕様
- 追加のエッジケース処理
- より優れた統計手法
- 実世界の制約モデリング

---

## ライセンス

MIT License — 詳細は [LICENSE](LICENSE) をご覧ください。

---

