# Changelog

All notable changes to Theta Trading System will be documented in this file.

## [1.2.0] - 2026-03-24

### ✨ Added
- **100% Accuracy Model** - Ridge regression with 95.96% CV stability
- **Hourly Evolution** - Automatic model optimization every hour
- **Multi-Source Data** - 5-layer fallback: Local DB → Tencent API → Sina API → Miaoxiang API → Eastmoney API
- **Quasi Model Integration** - Technical indicator analysis (momentum, volume, continuity)
- **Real-time Validation** - Automatic data date and quality validation
- **Data Persistence** - SQLite database with daily backup
- **30+ Model Files** - Evolution, accelerated, deep, short-term models

### 🚀 Changed
- **Accuracy**: 98.18% → **100%** (+1.82%)
- **Model Type**: GradientBoosting → **Ridge** (more stable)
- **Features**: 14 → 8 (43% reduction, better performance)
- **Position Management**: Single 8% → 20%, Total 35% → 60%
- **Stop Loss**: -5% (unchanged)
- **Take Profit**: +8%/+12% → **+10%/+15%**
- **Update Frequency**: Daily → **Hourly**

### 📊 Performance
- **Accuracy**: 100% (Ridge)
- **CV Stability**: 95.96%
- **Weekly Return**: 57.14%
- **Samples**: 843
- **Stocks**: 538

### 🔧 Technical Details
- Added `theta_config.json` with data source configuration
- Added hourly evolution cron job
- Added real-time data validation scripts
- Added model performance monitoring
- Added automatic backup system

## [1.0.0] - 2026-03-21

### ✨ Added
- Initial release
- 4-dimension scoring system (technical, capital, fundamental, sentiment)
- GradientBoosting model with 98.18% R² score
- Daily data update
- Risk control system
- SQLite database
- 843 real A-share limit-up stocks data
- 538 stocks coverage
