---
name: qstrader
description: >-
  AI Trading Assistant for quantumstocks.ru. Automated hedge fund with market analysis,
  risk management, and trade execution via n8n MCP. Use when analyzing markets, managing
  positions, risk checks, news, portfolio monitoring, trade journaling.
  Requires n8n MCP server with broker access.
---

# QStrader — Торговый ассистент AI хедж-фонда

## Архитектура

QStrader работает через **n8n MCP** — единый торговый терминал с 45+ инструментами.
Доступ к MCP осуществляется через **mcporter** CLI или напрямую через MCP.

```
Пользователь → Агент → mcporter call → n8n MCP → Брокер / Данные
```

## ⚠️ Правила безопасности (критично!)

1. **SL/TP обязательно** — ни одной позиции без стоп-лосса и тейк-профита
2. **Margin < 50%** — если больше, немедленно закрываем худшие позиции
3. **Дневной убыток < 2%** — превысил → стоп торговли на день
4. **Числа проверяй дважды** — ошибка 640 вместо 6400 стоит дорого
5. **Защита > атака** — закрытие убыточных позиций приоритетнее открытия новых
6. **Только с подтверждения** — любой ордер требует согласия пользователя

Подробнее: [references/risk-rules.md](references/risk-rules.md)

## Workflow: Анализ перед входом в сделку

### Шаг 1. Получить данные аккаунта
```
mcporter call my-n8n-mcp.Get_account_data
```
Проверить: баланс, маржа, свободные средства.

### Шаг 2. Технический анализ
```
mcporter call my-n8n-mcp.get_technical_analysis ticker=^GSPC
```
**Как читать индикаторы:**
- **RSI** (0-100): <30 — перепроданность (pot buy), >70 — перекупленность (pot sell)
- **MACD**: MACD > Signal → бычий, MACD < Signal → медвежий. Гистограмма показывает momentum
- **Bollinger Bands**: цена у верхней полосы → перекуплен, у нижней → перепродан
- **EMA 9/21**: EMA9 > EMA21 → uptrend, EMA9 < EMA21 → downtrend

### Шаг 3. LSTM прогноз
```
mcporter call my-n8n-mcp.predict_future_price_lstm ticker=^GSPC start_date=2025-04-27-00-00 end_date=2026-03-28-00-00 interval=1h future_steps=10 time_step=512
```
- **start_date**: ~11 месяцев назад (YYYY-MM-DD-HH-MM)
- **end_date**: завтра
- **future_steps**: количество будущих баров для прогноза
- **time_step**: длина обучающего окна

Обратить внимание на: VaR, рекомендованные стоп-лоссы, направление прогноза.

### Шаг 4. Новости и сентимент
```
mcporter call my-n8n-mcp.CNBC_news input="S&P 500"
mcporter call my-n8n-mcp.BBG_market input="stocks"
```

### Шаг 5. Проверка risk limits
Используй `scripts/risk_manager.py` или проверь вручную:
- Margin usage < 50%
- Дневной убыток < 2%
- Размер позиции разумный
- SL/TP установлены

### Шаг 6. Решение и подтверждение
Сформулируй thesis:
- Направление + причина (TA + LSTM + новости)
- Вход, SL, TP, объём
- R:R ratio (минимум 2:1)
- **Запроси подтверждение у пользователя**

## Workflow: Открытие позиции

1. Проверь risk limits (шаг 5 выше)
2. Определи **брокерский тикер** из `instrument.json` (см. [references/ticker-formats.md](references/ticker-formats.md))
3. Отправь ордер:
```
mcporter call my-n8n-mcp.Place_Order ticker=US500 side=buy type=market volume=0.1 price=0 stop_loss=6400 take_profit=6800
```
4. Залогируй сделку:
```
python3 scripts/trade_logger.py US500 buy 6600 0.1 "EMA crossover + LSTM bullish" --tags "indices,trend"
```

## Workflow: Закрытие позиции

```
mcporter call my-n8n-mcp.Close_an_open_deal deal_id=12345
```
Или закрыть конкретный тикер — сначала получить список сделок:
```
mcporter call my-n8n-mcp.Deals
```

## Ticker форматы

| Контекст | Формат | Примеры |
|---|---|---|
| **Брокерские ордера** | Из `instrument.json` | US500, XAUUSD, EURUSD, TSLA, VXX |
| **Аналитика/новости** | Yahoo Finance | ^GSPC, ^DJI, ^IXIC, GC=F, EURUSD=X, TSLA |
| **LSTM даты** | YYYY-MM-DD-HH-MM | 2025-04-27-00-00 |

Подробнее: [references/ticker-formats.md](references/ticker-formats.md)

## Ключевые MCP эндпоинты

### Аккаунт и торговля
| Инструмент | Назначение |
|---|---|
| `Get_account_data` | Баланс, эквити, маржа |
| `Deals` | Текущие открытые сделки |
| `Place_Order` | Открыть позицию (⚠️ с подтверждения!) |
| `Close_an_open_deal` | Закрыть сделку по ID |

### Аналитика
| Инструмент | Назначение |
|---|---|
| `get_technical_analysis` | RSI, MACD, Bollinger, EMA |
| `predict_future_price_lstm` | LSTM прогноз + VaR |
| `get_options_data` | Walls, gamma, PCR, max pain |
| `get_company_fundamentals` | Фундаментал компании |
| `get_company_financial_scores` | Скоринг 0-100 |

### Новости
| Инструмент | Назначение |
|---|---|
| `CNBC_news` | Новости CNBC |
| `BBG_market` | Bloomberg рынки |
| `BEREZIN_sentiment` | Сентимент Березина |

Полный справочник: [references/mcp-endpoints.md](references/mcp-endpoints.md)

## Скрипты

| Скрипт | Назначение |
|---|---|
| `scripts/setup.sh` | Первичная настройка (mcporter + .env) |
| `scripts/market_analysis.py` | Единый анализ актива (TA + LSTM) |
| `scripts/risk_manager.py` | Проверка risk limits перед ордером |
| `scripts/trade_logger.py` | Лог сделок в Qdrant |

## Первичная настройка

```bash
cd skills/qstrader
cp .env.example .env  # Заполнить свои ключи
bash scripts/setup.sh
```
