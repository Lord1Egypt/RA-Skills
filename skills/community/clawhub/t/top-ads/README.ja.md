# Denote Top Ads

ゲームやツール系アプリの人気広告・急上昇広告・新着広告を探し、次のユーザー獲得施策で試す広告素材を選べます。

[EN](README.md) · [ZH](README.zh.md) · JA · [KO](README.ko.md) · [ES](README.es.md) · [NL](README.nl.md) · [DE](README.de.md) · [FR](README.fr.md)

Denote はゲームとツール系アプリの広告データを毎日収集・更新します。1回の収集で6,000万件を超える広告レコードを対象とし、週に1回ランキングにまとめます。 無料アカウントで、直近の終了週におけるゲームまたはアプリの広告を、3つのランキングで各10件まで確認できます。 [Denote の広告ランキングを見る](https://denote.net/top-ads)。

| 無料ランキング | わかること |
| --- | --- |
| 人気広告 | 先週、特に注目を集めた広告を確認できます。 |
| 急上昇広告 | 前週と比べて人気の伸び幅が大きかった広告を見つけられます。 |
| 新着広告 | 新たに観測された広告を、初期の人気順に確認できます。 |

## 最初の週間ランキングを取得する

OpenClaw のワークスペースで次のコマンドを実行します。Python 3 が必要です。

```sh
git clone https://github.com/denote-developer/denote-top-ads.git skills/denote-top-ads
```

1. 新しいセッションを開き、「Denote でどんな広告を探せますか？」と聞いてください。
2. [無料の Denote アカウントを作成する](https://denote.net/user/register)。登録済みの場合はログインしてください。`top_ads:read` 権限を持つ Denote API キーを作成するか、既存のキーにこの権限を追加します。
3. エージェントのシークレット設定にキーを `DENOTE_API_KEY` として保存し、「先週のアプリ広告ランキングを見せて」と伝えてください。3つのランキングが表示されます。カテゴリを省略するとゲームが選ばれます。

チャットでは各ランキングの上位3件を1行ずつ、素材リンクと配信期間付きで表示します。人気・新着は週間スコア合計、急上昇は週間増加量と増加率を示します。返信末尾のローカルレポートで全件を確認できます。カードを開くと動画再生、概要、推移、関連広告、オーディエンスを確認でき、詳細が取得できない場合もワークスペースの該当ランキングに移動できます。

## 広告を詳しく見る

「急上昇広告の2位を詳しく見せて」と聞いてみてください。Top Ads Pro または Business では、広告の実績やオーディエンスなど、取得可能な詳細を確認できます。3つの週間ランキングは無料です。

## 画面例

[![左側のナビゲーションから3つの週間ランキングを開けます。](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/top-ads-navigation.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/top-ads-navigation.jpg)

*左側のナビゲーションから3つの週間ランキングを開けます。*

[![人気広告：2026年11月9日から15日のゲーム広告を週間人気順に表示します。](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/trending-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/trending-ads.jpg)

*人気広告：2026年11月9日から15日のゲーム広告を週間人気順に表示します。*

[![急上昇広告：前週と比べて人気の伸び幅が大きいゲーム広告です。](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/rising-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/rising-ads.jpg)

*急上昇広告：前週と比べて人気の伸び幅が大きいゲーム広告です。*

[![新着広告：新たに観測されたゲーム広告を初期の人気順に表示します。](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/new-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/new-ads.jpg)

*新着広告：新たに観測されたゲーム広告を初期の人気順に表示します。*

[![概要：Vita Mahjong の広告形式や推定表示回数を確認できます。](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/overview.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/overview.jpg)

*概要：Vita Mahjong の広告形式や推定表示回数を確認できます。*

[![推移：Vita Mahjong の日別スコアを基準線と比較できます。](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/data-trend.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/data-trend.jpg)

*推移：Vita Mahjong の日別スコアを基準線と比較できます。*

[![関連広告：同じ素材を使用する広告主や配信期間を比較できます。](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/related-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/related-ads.jpg)

*関連広告：同じ素材を使用する広告主や配信期間を比較できます。*

[![オーディエンス：国・地域、年齢、性別ごとのリーチを確認できます。](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/audience.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/audience.jpg)

*オーディエンス：国・地域、年齢、性別ごとのリーチを確認できます。*
