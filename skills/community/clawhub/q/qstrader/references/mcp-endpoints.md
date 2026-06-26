# n8n MCP — Полный справочник торгового терминала

> **Основной инструмент торговли и данных.** 47 эндпоинтов через `mcporter call my-n8n-mcp.ИМЯ`.
> **ВАЖНО:** Вызывать строго последовательно, по одному! Concurrency limit = 20, при превышении — 503.
> URL: `https://nnn8-antonbustrov.amvera.io/mcp/acc6ad15-3e20-4d20-9094-85bbb12e0780`
> Auth: нет

---

## 🏦 БРОКЕР — Торговля и аккаунт

### Read (безопасно, вызывать)

| Эндпоинт | Параметры | Что возвращает |
|---|---|---|
| `Get_account_data` | — | balance, equity, margin, free_margin, unrealized_pl |
| `Deals` | — | Текущие открытые сделки |
| `ORDERS` | — | Все ордера |
| `Get_active_orders` | — | Активные ордера |
| `Get_filled_orders` | — | Исполненные ордера |
| `Get_history_orders` | — | История ордеров |
| `Get_in_execution_orders` | — | В процессе исполнения |
| `Get_canceled_orders` | — | Отменённые |
| `Get_rejected_orders` | — | Отклонённые |
| `Quotes` | URL | Котировки (требует URL параметр) |

### Write (⚠️ ТОЛЬКО с подтверждения Антона!)

| Эндпоинт | Параметры | Описание |
|---|---|---|
| `Place_Order` | ticker, side, type, volume, price, stop_loss | Открыть ордер |
| `Close_an_open_deal` | URL | Закрыть сделку |
| `Set_Stop_Loss_Take_Profit_order_for_an_open_deal_or_edit_them_` | URL, parameters0_Value (SL), parameters1_Value (TP) | Установить/изменить SL/TP |
| `Delete_unfulfilled_Limit_or_Stop_order` | URL | Удалить лимитный/стоп ордер |
| `Modify_Order` | URL, parameters0-4 | Изменить ордер |

**Брокерские тикеры:** из `/home/server/instrument.json` (16,709 инструментов).
Поля: ticker, description, contract_size, min_volume, max_volume, volume_step, min_tick, leverage, trade_mode.
```python
import json
with open('/home/server/instrument.json') as f:
    instruments = json.load(f)['data']
# Поиск: [i for i in instruments if 'US500' in i['ticker']]
```

### Примеры ответов брокера

**Get_account_data:**
```json
{"code": "ok", "data": {"margin": {
  "balance": 23418.81,
  "unrealized_pl": -68.92,
  "equity": 23349.89,
  "margin": 228.81,
  "free_margin": 23121.08
}}}
```

---

## 📈 РЫНОК — Данные и аналитика

### Тикеры: Yahoo Finance формат
`^GSPC` (S&P 500), `^DJI` (Dow), `^IXIC` (NASDAQ), `GC=F` (Gold), `EURUSD=X`, `TSLA`, `AAPL`

### Эндпоинты

| Эндпоинт | Параметры | Что возвращает |
|---|---|---|
| `get_time_check` | — | Текущее время сервера |
| `Date_Time3` | Include_Current_Time=true | Дата/время |
| `get_enhanced_market_snapshot` | limit=N | Снимок рынка (топ тикеров) |
| `get_technical_analysis` | ticker="^GSPC" | RSI, MACD, Bollinger Bands, EMA 20/50/100, ATP |
| `get_historical_data` | ticker, start_date, end_date | Исторические свечи |
| `Think` | — | AI-аналитика рынка |
| `predict_future_price_lstm` | ticker, start_date, end_date, interval, future_steps, time_step | LSTM прогноз |
| `get_options_expirations` | ticker="AAPL" | Даты экспирации опционов |
| `get_options_data` | ticker, expiration_date | Call/Put walls, gamma, PCR, max pain |
| `get_rss_sources` | — | Доступные RSS источники |
| `get_rss_feed` | source, limit | RSS лента |
| `RSS_Finam` | input | Новости Финам |

### LSTM — правильный вызов
```bash
mcporter call my-n8n-mcp.predict_future_price_lstm \
  ticker="^GSPC" \
  start_date="2025-04-27-00-00" \
  end_date="2026-03-28-00-00" \
  interval="1h" \
  future_steps=10 \
  time_step=512
```
**Формат дат:** `YYYY-MM-DD-HH-MM`
**start:** текущая дата - 11 месяцев
**end:** текущая дата + 1 день

**Ответ LSTM содержит:**
- `predictions[]` — массив прогнозов (10 значений)
- `last_price` — последняя цена
- `volatility` — волатильность
- `mae`, `mse`, `rmse`, `mape` — метрики качества
- `good_forecast` — оценка качества прогноза (0-100%)
- `var_95_all`, `var_95_last` — Value at Risk 95%
- `stop_loss_var`, `stop_loss_atr`, `stop_loss_volatility` — стоп-лоссы по 3 методам
- `atr_last` — Average True Range

### Теханализ — структура ответа
```json
{
  "rsi": 29.46,          // < 30 = перепроданность, > 70 = перекупленность
  "macd": -26.09,        // < 0 = медвежий
  "macdsignal": -15.37,
  "macdhist": -10.72,    // гистограмма
  "bb_upper": 6646.05,   // верхняя полоса Боллинджера
  "bb_middle": 6561.08,  // средняя
  "bb_lower": 6476.10,   // нижняя
  "ema_20": 6547.98,     // краткосрочный тренд
  "ema_50": 6586.52,     // среднесрочный
  "ema_100": 6629.47     // долгосрочный
}
```

### Опции — структура ответа
```json
{
  "quote_data": { "regularMarketPrice": 252.89, ... },
  "metrics": {
    "call_wall": 280.0,        // уровень максимального call OI
    "put_wall": 260.0,         // уровень максимального put OI
    "zero_gamma": 270.0,       // уровень нулевой гаммы
    "pcr": 0.61,               // Put/Call Ratio
    "max_pain": 255.0,         // max pain
    "vol_skew": -0.02,         // скошенность волатильности
    "total_gamma_exposure": 4549.97
  },
  "summary": {
    "total_call_volume": 60019,
    "total_put_volume": 19378,
    "max_call_oi_strike": 280.0,
    "max_put_oi_strike": 260.0
  }
}
```

---

## 📰 НОВОСТИ — Поисковые запросы (input = строка поиска)

| Эндпоинт | Параметры | Описание |
|---|---|---|
| `CNBC_news` | input="stock market" | Новости CNBC |
| `BEREZIN_sentiment` | input="S&P 500" | Сентимент Березина |
| `Latest_news_from_berezin` | input="" | Последние новости Березина |
| `BBG_tech` | input="AI technology" | Bloomberg Tech |
| `BBG_market` | input="stock market" | Bloomberg Market |
| `BBG_politic` | input="Federal Reserve" | Bloomberg Politics |
| `macroeconomic_calendar_` | input="" | Макро-календарь на неделю |
| `Macroeconomic_archive` | input="interest rate" | Архив макро-событий |
| `FED1` | input="interest rate" | Данные ФРС |
| `get_global_market_news` | — | Глобальные новости |
| `get_company_news` | ticker="AAPL" | Новости компании |

---

## 📊 ФУНДАМЕНТАЛ

| Эндпоинт | Параметры | Что возвращает |
|---|---|---|
| `get_company_fundamentals` | ticker_symbol="AAPL" | Профиль, выручка, прибыль, баланс, FCF, EPS |
| `get_advanced_company_fundamentals` | ticker_symbol, detail_level | Расширенный фундаментал |
| `get_company_financial_scores` | ticker_symbols="AAPL" | Скор 0-100: profitability, health, growth, valuation |
| `get_nasdaq_company_data` | compnumber (числовой ID) | Данные NASDAQ |
| `get_fred_series_data` | series_id="DGS10" | Данные FRED (10Y Treasury и др.) |
| `get_fred_series_search` | search_text="GDP" | Поиск серий FRED |
| `get_fred_search_sources` | — | Источники FRED |

### Фундаментал — скоринг
```json
{
  "score": 20.46,
  "components": {
    "profitability": {"weight": 30, "score": 0.46},
    "financial_health": {"weight": 25, "score": 8},
    "growth": {"weight": 25, "score": 12},
    "valuation": {"weight": 20, "score": 0}
  }
}
```
Шкала: 80+ = Сильная, 60-79 = Хорошая, 40-59 = Средняя, <40 = Слабая

---

## ⚙️ АВТОРИЗАЦИЯ (не используется)

| Эндпоинт | Параметры | Описание |
|---|---|---|
| `register_new_user` | secret_phrase, username, password | Регистрация |
| `get_access_token` | username, password | Получение токена |

---

## 🚨 ПРАВИЛА БЕЗОПАСНОСТИ

1. **Только последовательно!** Один mcporter call за раз, пауза между запросами
2. **Write-эндпоинты (ордера)** — ТОЛЬКО с подтверждения Антона
3. **Проверять числа дважды** перед ордером (ошибка 640 vs 6400 = -$574)
4. **SL/TP обязательно** для каждого ордера
5. **Margin < 50%**, дневной убыток < 2%
