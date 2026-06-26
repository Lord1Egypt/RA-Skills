# QStrader — AI Trading Assistant

> **quantumstocks.ru** | Версия 1.0.0 | Лицензия: MIT

## Что это

AI-ассистент для автоматизированного хедж-фонда. Анализирует рынки, проверяет риски, управляет позициями через n8n MCP.

## Возможности

- 📊 **Технический анализ** — RSI, MACD, Bollinger Bands, EMA (20/50/100)
- 🤖 **LSTM прогноз** — 10 шагов вперёд + VaR 95% + стоп-лоссы по 3 методам
- 🛡️ **Risk Manager** — автоматическая проверка SL/TP, margin, дневных лимитов
- 📰 **Новости** — CNBC, Bloomberg, Berezin, макро-календарь, FED
- 📊 **Фундаментал** — балансы компаний, финансовые скоры, FRED макроданные
- 💰 **Торговля** — ордера, SL/TP, закрытие сделок через брокера
- 📝 **Trade Journal** — лог сделок в Qdrant (векторная БД)
- 🔍 **Семантическая память** — поиск по истории решений и паттернов

## Требования

- **OpenClaw** — https://github.com/openclaw/openclaw
- **mcporter** — CLI для MCP (входит в OpenClaw)
- **n8n** — с MCP workflow (торговый терминал)
- **Python 3.10+**
- **Qdrant** — векторная БД (опционально, для памяти)
- **LightRAG** — графовая БД (опционально, для знаний)

## Установка

### 1. Распаковать skill

```bash
# Если у тебя .skill файл:
mkdir -p ~/.openclaw/workspace/skills/qstrader
tar -xzf qstrader.skill -C ~/.openclaw/workspace/skills/

# Или скопировать папку qstrader/ в skills/
```

### 2. Настроить ключи

```bash
cp ~/.openclaw/workspace/skills/qstrader/.env.example ~/.openclaw/workspace/skills/qstrader/.env
```

Заполни `.env` своими ключами:

```bash
# n8n MCP Server (торговый терминал)
N8N_MCP_URL=https://your-n8n-instance.amvera.io/mcp/YOUR-WORKFLOW-ID

# Qdrant (векторная БД для памяти)
QDRANT_URL=https://your-qdrant.amvera.io
QDRANT_API_KEY=your-api-key

# LightRAG (графовая БД для знаний)
LIGHTRAG_URL=https://your-lightrag.amvera.io
LIGHTRAG_USERNAME=admin
LIGHTRAG_PASSWORD=your-password

# OpenRouter (LLM + Embeddings)
OPENROUTER_API_KEY=your-api-key
```

### 3. Подключить MCP серверы

```bash
# n8n (торговый терминал)
mcporter config add my-n8n-mcp --url $N8N_MCP_URL --transport streamable-http

# Qdrant (память) — если используешь
mcporter config add qdrant-trading --command "python3 path/to/qdrant_mcp_server.py"
```

Или запусти автоматическую настройку:

```bash
bash ~/.openclaw/workspace/skills/qstrader/scripts/setup.sh
```

### 4. Проверить

```bash
# Проверить подключение к брокеру
mcporter call my-n8n-mcp.Get_account_data

# Анализ рынка
python3 ~/.openclaw/workspace/skills/qstrader/scripts/market_analysis.py ^GSPC

# Risk check
python3 ~/.openclaw/workspace/skills/qstrader/scripts/risk_manager.py US500 buy 1 6600 --sl 6500 --tp 6800
```

## Использование

### Анализ рынка

```bash
# S&P 500
python3 scripts/market_analysis.py ^GSPC

# Bitcoin
python3 scripts/market_analysis.py BTC-USD

# Gold
python3 scripts/market_analysis.py GC=F

# EUR/USD
python3 scripts/market_analysis.py EURUSD=X
```

Выводит: теханализ (RSI, MACD, BB, EMA) + LSTM прогноз (10 шагов, VaR, стоп-лоссы) + данные аккаунта.

### Проверка рисков

```bash
# ✅ Валидный ордер
python3 scripts/risk_manager.py US500 buy 1 6600 --sl 6500 --tp 6800

# ❌ Без SL/TP — будет REJECTED
python3 scripts/risk_manager.py US500 buy 1 6600

# ⚠️ Большой объём — warning о потенцильном убытке
python3 scripts/risk_manager.py US500 buy 10 6600 --sl 6500 --tp 6800
```

**Лимиты:**
- SL/TP — обязательно
- Margin < 50%
- Дневной убыток < 2%
- Потенциальный убыток позиции < $100

### Лог сделки

```bash
python3 scripts/trade_logger.py log --ticker US500 --side buy --price 6600 --volume 1 --strategy trend_follow --tags indices,trend
```

### Через агента (OpenClaw)

После установки skill активируется автоматически. Агент:
1. Анализирует рынок перед каждой сделкой
2. Проверяет risk limits
3. Запрашивает подтверждение на ордер
4. Логирует сделку в память

Просто скажи: "проанализируй S&P 500" или "открой long на золото".

## Форматы тикеров

| Тип | Формат | Примеры |
|---|---|---|
| **Брокерские ордера** | из instrument.json | US500, EURUSD, GC=F, VXX |
| **Теханализ + LSTM** | Yahoo Finance | ^GSPC, ^DJI, GC=F, EURUSD=X, BTC-USD, TSLA |
| **Опции** | Yahoo Finance | AAPL, TSLA |
| **Фундаментал** | Тикер компании | AAPL, TSLA |
| **Макро (FRED)** | Series ID | DGS10 (10Y), GDP, UNRATE |

### LSTM формат дат

```
start_date: YYYY-MM-DD-HH-MM (текущая дата - 11 месяцев)
end_date:   YYYY-MM-DD-HH-MM (текущая дата + 1 день)
interval:   1h
future_steps: 10
time_step:   512
```

## Структура

```
qstrader/
├── SKILL.md                      # Инструкция для агента
├── .env.example                  # Шаблон ключей
├── scripts/
│   ├── setup.sh                  # Автонастройка mcporter
│   ├── market_analysis.py        # TA + LSTM + аккаунт
│   ├── risk_manager.py           # Проверка risk limits
│   └── trade_logger.py           # Лог сделок в Qdrant
└── references/
    ├── mcp-endpoints.md          # Справочник 47 эндпоинтов
    ├── risk-rules.md             # Правила risk management
    └── ticker-formats.md         # Форматы тикеров
```

## MCP эндпоинты (47 шт)

### Брокер (15)
`Get_account_data`, `Deals`, `ORDERS`, `Get_active_orders`, `Get_filled_orders`, `Get_history_orders`, `Get_in_execution_orders`, `Get_canceled_orders`, `Get_rejected_orders`, `Quotes`, `Place_Order`, `Close_an_open_deal`, `Set_Stop_Loss_Take_Profit_order_for_an_open_deal_or_edit_them_`, `Delete_unfulfilled_Limit_or_Stop_order`, `Modify_Order`

### Рынок (12)
`get_time_check`, `Date_Time3`, `get_enhanced_market_snapshot`, `get_technical_analysis`, `get_historical_data`, `Think`, `predict_future_price_lstm`, `get_options_expirations`, `get_options_data`, `get_rss_sources`, `get_rss_feed`, `RSS_Finam`

### Новости (11)
`CNBC_news`, `BEREZIN_sentiment`, `Latest_news_from_berezin`, `BBG_tech`, `BBG_market`, `BBG_politic`, `macroeconomic_calendar_`, `Macroeconomic_archive`, `FED1`, `get_global_market_news`, `get_company_news`

### Фундаментал (9)
`get_company_fundamentals`, `get_advanced_company_fundamentals`, `get_company_financial_scores`, `get_nasdaq_company_data`, `get_fred_series_data`, `get_fred_series_search`, `get_fred_search_sources`, `register_new_user`, `get_access_token`

## Важно

- **⚠️ Concurrency limit:** n8n MCP принимает до 20 одновременных запросов. При превышении — 503. Вызывай последовательно.
- **⚠️ Write-эндпоинты** (ордера) — только с подтверждения человека
- **⚠️ Проверяй числа дваждую** — ошибка 640 вместо 6400 уже стоила $574
- **📋 Тикеры брокера** — из `instrument.json` (16,709 инструментов), искать через Python

## Автор

**quantumstocks.ru** | Антон Быстров
