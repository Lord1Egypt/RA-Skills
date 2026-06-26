# Weather Outfit Advisor - 天气穿搭建议 🌤️👔

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文) | [日本語](#日本語) | [Français](#français)

---

## English

**Smart outfit recommendations based on real-time weather data.**

This skill queries weather forecasts for your destination and provides personalized clothing suggestions tailored to your preferences.

### Key Features
- 🌡️ Real-time weather data from free APIs
- 📅 Smart date parsing (tomorrow, next Monday, etc.)
- 🌍 Multi-language city name support
- 👤 Personalized recommendations (怕冷/怕热，casual/business)
- 🖼️ Fashion inspiration images from Pexels

### Quick Start
```bash
python scripts/get_weather.py Paris tomorrow
python scripts/search_images.py "Paris fashion" 5
python scripts/generate_outfit_advice.py Paris 2026-06-01 casual
```

---

## 简体中文

**基于实时天气数据的智能穿搭建议助手。**

根据您的出行目的地和穿衣习惯，提供个性化的穿搭建议。

### 核心功能
- 🌡️ 免费天气 API 实时查询
- 📅 智能日期解析（明天、后天、下周一等）
- 🌍 中英文城市名自动转换
- 👤 个性化推荐（怕冷/怕热、休闲/商务）
- 🖼️ Pexels 时尚图片参考

### 快速开始
```bash
python scripts/get_weather.py Paris tomorrow
python scripts/search_images.py "Paris fashion" 5
python scripts/generate_outfit_advice.py Paris 2026-06-01 casual
```

---

## 繁體中文

**基於實時天氣數據的智能穿搭建議助手。**

根據您的出行目的地和穿衣習慣，提供個性化的穿搭建議。

### 核心功能
- 🌡️ 免費天氣 API 實時查詢
- 📅 智能日期解析（明天、後天、下週一等）
- 🌍 中英文城市名自動轉換
- 👤 個性化推薦（怕冷/怕熱、休閒/商務）
- 🖼️ Pexels 時尚圖片參考

### 快速開始
```bash
python scripts/get_weather.py Paris tomorrow
python scripts/search_images.py "Paris fashion" 5
python scripts/generate_outfit_advice.py Paris 2026-06-01 casual
```

---

## 日本語

**リアルタイムの天気データに基づくスマートな服装提案スキル。**

旅行先の天気予報を照会し、個人の好みに合わせた服装のアドバイスを 제공합니다。

### 主な機能
- 🌡️ 無料の天気 API でリアルタイムデータ取得
- 📅 スマートな日付解析（明日、明後日、来週の月曜など）
- 🌍 中国語・英語の都市名自動変換
- 👤 パーソナライズされた提案（寒がり/暑がり、カジュアル/ビジネス）
- 🖼️ Pexels のファッション画像リファレンス

### クイックスタート
```bash
python scripts/get_weather.py Paris tomorrow
python scripts/search_images.py "Paris fashion" 5
python scripts/generate_outfit_advice.py Paris 2026-06-01 casual
```

---

## Français

**Recommandations vestimentaires intelligentes basées sur les données météorologiques en temps réel.**

Ce skill consulte les prévisions météorologiques de votre destination et fournit des suggestions vestimentaires personnalisées adaptées à vos préférences.

### Fonctionnalités clés
- 🌡️ Données météorologiques en temps réel via des API gratuites
- 📅 Analyse intelligente des dates (demain, après-demain, lundi prochain, etc.)
- 🌍 Support multilingue des noms de villes
- 👤 Recommandations personnalisées (sensible au froid/chaleur, casual/business)
- 🖼️ Images d'inspiration mode depuis Pexels

### Démarrage rapide
```bash
python scripts/get_weather.py Paris tomorrow
python scripts/search_images.py "Paris fashion" 5
python scripts/generate_outfit_advice.py Paris 2026-06-01 casual
```

---

## 📁 Directory Structure / 目录结构

```
weather-outfit-advisor/
├── README.md                     # 多语言介绍文件
├── SKILL.md                      # 详细使用说明
└── scripts/
    ├── get_weather.py           # 天气查询脚本
    ├── search_images.py         # 图片搜索脚本
    └── generate_outfit_advice.py # 完整建议生成脚本
```

---

## 🔧 Requirements / 环境要求

- Python 3.6+
- No external dependencies required (仅标准库)
- Pexels API key (已内置，也可自行配置)

---

## 📝 License / 许可证

MIT License

---

## 🤝 Contributing / 贡献

Welcome issues and pull requests! 欢迎提交 Issue 和 Pull Request！

---

**Made with ❤️ for FlyAI Skills**
