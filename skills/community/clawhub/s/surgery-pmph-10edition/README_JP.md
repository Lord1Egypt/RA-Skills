# 外科学 Surgery-PMPH-10edition

<div align="center">

> *「21世紀 医学生ガイド」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> 人民衛生出版社『外科学』第10版に基づく臨床スキルハンドブック — 240 の外科・救急・集中治療の臨床スキル
<br>
<br>
<img src="https://github.com/xllgreen/Surgery-PMPH-10edition-/blob/main/assets/Surgery.png" width="260px">
<br>

一冊の本を苦しんで読む必要はありません<br>
質問を入力するだけで、教科書から自動的に解決策を見つけます

<br>

**他の言語 / Other Languages:**

[简体中文](README.md) · [English](README_EN.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## プロジェクト概要

本プロジェクトは、臨床外科学、救急・集中治療医学、周術期管理、外傷治療、総合的癌治療、感染制御、多系統疾患診療などの中核領域を体系的に統合し、**240 の主要臨床スキル** を **17 の大カテゴリ** に分類して網羅しています。

**対象読者**：外科医、救急医、集中治療チーム、医学生

**参考教科書**：人民衛生出版社『外科学』第 10 版

## プロジェクト構成

```
Surgery-PMPH-10edition/
├── SKILL.md              # 核心設定 — 240 スキルレジストリ
├── README.md             # 本ドキュメント — プロジェクト概要と使用ガイド
├── <skill-name>/         # 各スキルの詳細定義
│   └── SKILL.md          #   スキル詳細（適応、手順、参考文献）
├── scripts/              # 実行可能ユーティリティスクリプト
│   ├── skill-search.sh   #   キーワードによるスキル検索
│   └── skill-report.sh   #   スキル一覧レポート生成
├── config/               # 設定ファイル
│   └── skill-config.yaml #   スキル分類とメタデータ設定
└── tests/                # 検証とテスト
    └── validate-all.sh   #   完全性検証スクリプト
```

## スキルカテゴリ一覧

| カテゴリ | スキル数 | 説明 |
|---------|---------|------|
| 🚑 救急・蘇生 | 14 | CPR、ショック蘇生、電解質異常救急処置 |
| 🦴 外傷・骨折 | 27 | 骨折分類、整復固定、神経損傷 |
| 🩺 一般外科・腹部救急 | 22 | 虫垂炎、イレウス、ヘルニア、腹膜炎 |
| 🫁 肝胆膵脾外科 | 19 | 胆道結石、膵炎、肝外傷 |
| 🩻 胃腸外科 | 10 | 胃癌、大腸癌、GERD |
| 🫘 泌尿器科 | 24 | 結石、腫瘍、感染、尿道損傷 |
| 🩸 血管外科 | 7 | DVT、静脈瘤、血管修復 |
| 🔥 熱傷・形成外科 | 8 | 面積推定、深度分類、植皮 |
| 🧬 腫瘍外科・総合的治療 | 16 | TNM分類、放射線・化学療法、四肢温存手術 |
| 📋 周術期管理 | 18 | 術前最適化、抗生物質、栄養サポート |
| 💉 麻酔・疼痛管理 | 11 | 気道管理、脊椎麻酔、局所麻酔 |
| ⚖️ 内分泌・代謝 | 6 | 副甲状腺機能亢進症、脱水、電解質異常 |
| 🦠 感染・免疫 | 7 | 結核、敗血症、破傷風 |
| 📡 画像診断・インターベンション | 10 | 造影、内視鏡、インターベンショナルラジオロジー |
| 🏋️ リハビリテーション・機能評価 | 12 | 骨折リハビリ、神経評価 |
| 🦿 リウマチ・脊椎疾患 | 5 | 強直性脊椎炎、脊柱管狭窄症 |
| 🔧 その他の専門スキル | 10 | ARDS、AKI、除細動など |

## クイックスタート

### インストール

CLI：
```bash
openclaw skills install surgery-pmph-10edition
```

プロンプト：
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Surgery-PMPH-10edition" (xllgreen/surgery-pmph-10edition) from ClawHub only after those checks pass.
Skill page: https://clawhub.ai/xllgreen/surgery-pmph-10edition
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### インストール後の使用方法

エージェントに以下の指示を伝えてください：
```bash
毎回回答する前に、該当する医学スキルを確認してください
```

### スキル検索

```bash
# キーワード検索
bash scripts/skill-search.sh 虫垂炎

# スキル一覧の生成
bash scripts/skill-report.sh
```

### 使用方法

各スキルは次の4つの部分で構成されています：
1. **適応** — いつこのスキルを発動するか
2. **手順** — 標準化された操作フロー
3. **注意事项** — 禁忌と警告
4. **参考文献** — 詳細な補足資料

### 質問戦略

#### 1. **概念**
質問：
```bash
外科学における膵仮性嚢胞の概念とは？
```
回答：
```bash
## 膵仮性嚢胞（Pancreatic Pseudocyst, PPC）の概念
膵仮性嚢胞は、**急性膵炎、膵外傷、または慢性膵炎後に**形成される合併症であり、本質的には**壊死または破裂した膵管から膵液が漏出し、膵周囲または小網嚢内で線維組織に被包されて形成される嚢胞性構造**です。
### 主な特徴
| 特徴 | 説明 |
|------|------|
| **「仮性」の意味** | 嚢壁に**上皮細胞の裏打ちがない**（真性嚢胞と異なる）、線維結合組織と肉芽組織から構成 |
| **形成機序** | 膵管破裂 → 膵液漏出 → 周囲組織の炎症反応・被包化 → 嚢壁の成熟（約 **≥6週間** が必要） |
| **嚢液の成分** | 膵酵素（アミラーゼ・リパーゼ）に富む、タンパク性液体 |
| **好発部位** | 小網嚢、膵周囲腔 |
### 自然経過
- **<4 cm** の嚢胞はほぼ確実に自然吸収される
- **<5 cm** では約 50% が自然吸収される
- **>6 cm または多発** では自然吸収の可能性は低く、介入の検討が必要
- 嚢壁の成熟には約 **6 週間** を要し、成熟後に内視鏡的ドレナージが可能となる
### 真性嚢胞・嚢胞性腫瘍との鑑別
> 画像上、膵嚢胞性腫瘍（漿液性嚢胞腺腫、粘液性嚢胞腺腫、IPMN など）との鑑別を要する。PPC は急性膵炎・外傷の既往、上皮の欠如、嚢液アミラーゼの著明な上昇の3点で鑑別される。
治療戦略（経過観察 vs 内視鏡的ドレナージ vs 経皮的ドレナージ vs 切除）について詳しく説明しましょうか？
```

#### 2. **臨床ケース分析**
質問：
```bash
28歳女性、結婚後3年間不妊。6ヶ月前より無月経・乳汁漏出を認める。身体所見：外観は正常、乳汁漏出あり、眼底・視野は正常。血清プロラクチン 250ng/ml、MRIでトルコ鞍内に4mm×4mmの低信号域を認め、視神経から5mmの距離。本症例の診断と治療方針は？
```
回答：
```bash
## 症例分析
**重要所見の整理：**
| 項目 | 所見 |
|------|------|
| 患者 | 28歳女性 |
| 主訴 | **無月経 + 乳汁漏出 + 不妊**（古典的三徴） |
| 血清 PRL | **250 ng/ml**（正常 < 25、著明高値） |
| MRI | トルコ鞍内 **4mm × 4mm 低信号域**（微小腺腫 < 10mm） |
| 視野・視力 | **正常**、視神経から 5mm（圧迫なし） |
### 診断：プロラクチン分泌性下垂体微小腺腫
**根拠：**
- 高 PRL → GnRH 抑制 → **無月経-乳汁漏出-不妊症候群**
- 4mm 腫瘍 = 微小腺腫
- 視野欠損なし = 視交叉圧迫なし
### 治療：第一選択は薬物療法、手術適応なし
**第一選択：ドパミン受容体作動薬**
| 薬剤 | 用法 | 利点 |
|------|------|------|
| **カベルゴリン** | 0.25–0.5 mg、週1–2回 | 第一選択、副作用が少なく、服薬が容易 |
| ブロモクリプチン | 1.25–5 mg、1日2–3回 | 代替、ただし悪心・めまいが多い |
**予想される効果：**
- **数週間以内** → PRL 正常化 → 排卵性月経の再開、乳汁漏出消失
- **数ヶ月〜1年** → 腫瘍の著明な縮小（約 80–90% 有効）
**なぜ手術をしないのか？**
- 微小腺腫は薬物療法が第一選択 — 有効性が高く、侵襲が少ない
- 経蝶形骨洞手術の適応：薬剤耐性・不耐容、視神経圧迫症状、非プロラクチン産生腫瘍（非機能性腺腫など）が疑われる場合
- 本例は視神経から 5mm、視野正常 — **手術適応なし**
### 経過観察
- 治療後 3–6 ヶ月毎に PRL を再検査
- 腫瘍縮小後は MRI を年に1回
- PRL 正常化後は妊娠可能、産科・内分泌合同管理が必要
```

#### 3. **試験問題**
質問：
```bash
下肢深部静脈血栓症の最も重篤な合併症は？
A 下肢表在性静脈瘤
B 肺塞栓症
C 動脈痙攣を伴う四肢虚血
D 下肢潰瘍
E 静脈閉塞
```
回答：
```bash
正解は **B. 肺塞栓症**
下肢深部静脈血栓症（DVT）の最も重篤な合併症は**肺塞栓症（Pulmonary Embolism, PE）** です — 血栓が遊離し、下大静脈→右心房→右心室→肺動脈に至り、広範な肺梗塞や突然死を引き起こす可能性があります。
- **A** 下肢表在性静脈瘤 → DVT 慢性期の側副血行路代償の徴候であり、重篤な合併症ではない
- **C** 動脈痙攣を伴う四肢虚血 → 大腿青腫（Phlegmasia Cerulea Dolens）型 DVT で見られるが、発生頻度は PE よりはるかに低い
- **D** 下肢潰瘍 → 慢性期後遺症であり、最も重篤ではない
- **E** 静脈閉塞 → 稀であり、通常は DVT の近位伸展の結果
臨床的に DVT 患者における最も致命的な脅威は **血栓遊離による肺塞栓症** であり、これこそが急性 DVT に即時の抗凝固療法と、抗凝固禁忌時の下大静脈フィルター留置が必要とされる根本的理由です。
```

## 著者について

**小緑緑 xllgreen（[xllgreen.github.io](https://xllgreen.github.io)）** — 九江学院臨床医学院 学生 · テックギーク

## テクニカルサポート

<br>
PDF2App プロジェクト：https://pdf2app.cn
<br>
Microsoft Visual Studio Code：https://code.visualstudio.com/
<br>
Claude Code for VS Code：https://claude.com/
© 2026 Anthropic PBC
<br>
<br>
<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>DeepSeek API：https://platform.deepseek.com/
© 2026 杭州深度求索人工智能基礎技術研究有限公司 著作権所有
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>Xiaomi Mimo API：https://platform.xiaomimimo.com/
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved
<br>

## ライセンス

本プロジェクトの内容は人民衛生出版社『外科学』第10版に基づいて整理されたものであり、学習参考目的のみで提供されています。

## Star History

<a href="https://www.star-history.com/?repos=xllgreen%2FSurgery-PMPH-10edition-&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=xllgreen/Surgery-PMPH-10edition-&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=xllgreen/Surgery-PMPH-10edition-&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=xllgreen/Surgery-PMPH-10edition-&type=date&legend=top-left" />
 </picture>
</a>
