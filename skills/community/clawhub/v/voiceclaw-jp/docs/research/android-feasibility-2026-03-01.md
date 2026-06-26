# Androidでのwakeword常時稼働の実現性メモ（暫定）

- 日付: 2026-03-01
- 目的: voiceclaw 要件に関連する wakeword OSS が Android 上で動くか（どう動かすか）を整理する。

## 結論（現時点の感触）

- **openWakeWord** 自体は Python ベースで、理屈上は Android でも（例: Termux）動かせる可能性があるが、
  **実用上は依存（onnxruntime/tflite-runtime、音声入力、常駐）をAndroidで安定させる作業**が必要。
- **Wyoming系**は「サテライト（マイク側）を分離」するアーキテクチャで、Androidを“端末/UI/マイク”に寄せやすい。ただし
  - `wyoming-satellite` は上流README上 **deprecated**（後継へ移行）と明記されている。
  - それでも「やりたいことの構造」は非常に近い（wakewordサービス分離、常時入力、検出後に処理へ流す）。
- **Mycroft Precise** は基本 Linux 向けの色が強く、Androidでの実運用はハードル高め（移植/ビルド/常駐の整備が必要）。

## 個別メモ

### openWakeWord

- Repo: https://github.com/dscripka/openWakeWord
- 形態: Pythonライブラリ（wakeword/フレーズ検出）
- Android適性:
  - 直接「Android対応」とうたっているわけではない。
  - **Termux + Python** で動かす方向が現実的。
  - 推論バックエンドが onnxruntime / tflite-runtime なので、Android(arm64)での依存解決が要検証。

### Wyoming openWakeWord / Wyoming Satellite

- wyoming-openwakeword: https://github.com/rhasspy/wyoming-openwakeword
- wyoming-satellite: https://github.com/rhasspy/wyoming-satellite
- Android適性:
  - “サテライト”が基本 Linux だが、Termux 等で動かす事例がコミュニティに存在（別途リンク収集予定）。
  - ただし `wyoming-satellite` は README に **deprecated** とあるため、採用するなら後継（OHF-Voice/linux-voice-assistant 等）も要確認。

### Mycroft Precise

- Repo: https://github.com/MycroftAI/mycroft-precise
- Android適性:
  - 既製のAndroid向け配布/サポートは薄い印象。
  - 研究用途・学習用途としては参考になるが、voiceclaw のAndroid常駐にそのまま使うのは厳しそう。

## 次のアクション（TODO）

1. Termux での常駐（バックグラウンド運用・マイク権限・省電力制限回避）の実例を収集
2. OHF-Voice/linux-voice-assistant（後継）と、ESPHomeプロトコル周辺の調査
3. 「AndroidはUIのみ」案（wakeword常時稼働は別デバイス/RPi/PC）との比較表を作る
