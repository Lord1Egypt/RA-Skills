# VSD Craft Plugin Development

Elgato互換の調査結果を読んで、そのまま小さく動かせる独立したAgent Skillです。
個人のHerdr環境、シーンID、ログ、秘密情報は含みません。

## インストール

このディレクトリ全体を、エージェントのスキル検索ディレクトリへコピーします。
例: `<workspace>/skills/vsd-craft-plugin-development/` またはプロジェクトの
`.agents/skills/vsd-craft-plugin-development/`。既存コピーは退避して更新します。

依頼例: 「VSD Craft用のプラグインを作って」「このElgatoプラグインをM3へ移植して」。

## クイックスタート

必要なもの: Python 3.9以降、Node.js 20以降、npm。雛形のホスト指定はNode 20です。
以下はスキルのディレクトリで実行する例です。出力先は未使用の場所を指定します。

```sh
python3 scripts/scaffold.py --id com.example.counter --name "Counter" \
  --output /tmp/vsd-demo/com.example.counter.sdPlugin
cd /tmp/vsd-demo/com.example.counter.sdPlugin
npm install --ignore-scripts --omit=optional --no-audit --no-fund
npm test
```

Windowsでは `/tmp/...` を任意の作業先へ置き換え、Pythonは `py -3` でも実行できます。
生成されたフォルダは**まだインストールされません**。

- キーの押下→解放で数値を加算。
- ノブの回転量で加減算、押下→解放で0へ戻す。
- 設定画面で加算幅を変更。
- 表示context単位で値を分け、USB切断中の入力を破棄して再接続時に再描画。
- 外部アプリ操作、キー送信、通知、シーン変更は行わない。

この雛形の数値はメモリ上のデモ状態です。加算幅のみホスト設定へ保存します。
アプリ再起動と`willDisappear` (配置の削除・ページ切替などで非表示になるとき) で数値を破棄します。
同じホスト接続内のUSB切断だけでは数値・配置contextを保持します。

## 配布用ZIP

スキルのディレクトリへ戻って:

```sh
python3 scripts/package_plugin.py /tmp/vsd-demo/com.example.counter.sdPlugin \
  --output /tmp/vsd-demo/counter.zip
```

ZIPを展開して配置する方式です。VSD Craft専用インストーラーやElgatoパッケージではありません。
梱包ヘルパーはこの雛形のファイル構成専用で、`ws`の本体とLICENSEも含めます。

## 最初に読むもの

- [API互換表](references/elgato-compatibility.md)
- [既存環境で確認した挙動](references/field-observations.md)
- [実装・配布・実機検証](references/development.md)
- [公式出典](references/sources.md)

`npm test`の成功は模擬ホストでの成功です。この新規雛形の実アプリ起動・物理M3試験は別途必要です。

## 検証済みの範囲 (2026-10-09)

- Linux上のNode 20.20.2 / 24.18.0で、同梱の6試験すべて成功。
- Python 3.12.3で、生成・既存ファイル保護・パス検証・配布内容を確認する3試験が成功。
- 生成→lockfileから依存導入→ZIP化→別フォルダへ展開後、Node 20で再び6試験成功。
  展開先には試験コードだけを追加し、runtime依存はZIP内のものだけを使用。
- スキル形式、相対参照、個人パスや実行ログが同梱されていないことを確認。

実アプリや物理機器への導入は行っていません。既存プラグインの実機知見と、
この新規雛形の模擬試験結果は区別してください。
