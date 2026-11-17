# VSD Craft Operations

VSD Craftの設定・導入・更新・復旧を扱う、独立して使えるAgent Skillです。
通常の設定は標準機能で行い、必要になった部分だけを開発スキルへ渡します。

## インストール

このディレクトリ全体を、使うエージェントのスキル検索ディレクトリへコピーします。
OpenClawなら `<workspace>/skills/vsd-craft-operations/`、Codexなら
プロジェクトの `.agents/skills/vsd-craft-operations/` など。既存コピーは退避して更新します。
スキルの配置だけでVSD Craftやデバイスの設定は変わりません。

## 依頼例

- 「VSD Craftのノブに標準機能でページ送りを割り当てて」
- 「このStreamDockプラグインを設定を残して更新して」
- 「USB再接続後、キーの表示だけ止まる原因を調べて」

## 読み取り専用の棚卸し

Python 3.9以降を使います。スキルのディレクトリで実行:

```sh
python3 scripts/inspect_data.py --root /path/to/confirmed/StreamDock
```

Windowsでは `py -3 scripts/inspect_data.py --root "確認済みのデータルート"` でも実行できます。
アプリや機器は起動・停止せず、プロファイル本文・シーン名・ログ・トークンを出力しません。
棚卸しでデータが見つかることは、そのフォルダが現在使われている証明ではありません。

ヘルパーの確認: `python3 -B -m unittest discover -s scripts -p 'test_*.py'`。
一時データのみを使用し、実際のVSD Craft設定には触れません。
2026-10-09にLinux / Python 3.12.3で同梱試験1件とスキル形式・相対参照の検証が成功。

## 内容

- [SKILL.md](SKILL.md): エージェント用の手順。
- [操作知見と出典](references/operations.md): VSD Craft 3.10.205.0918 / Windows / M3の観測と公開資料を区別。
- [検証票](references/verification.md): アプリ表示と実機確認を別々に記録。

プラグイン実装・Elgato移植には、別スキル `vsd-craft-plugin-development` を使います。
本スキル単独ではそちらのファイルを必要としません。
