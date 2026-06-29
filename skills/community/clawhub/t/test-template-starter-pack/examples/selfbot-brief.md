# SelfBot — Russian Self-Employed Tax Assistant (Example Brief)

Vertical: Tax automation for самозанятые (self-employed) in Russia
Market: ~12M самозанятые in Russia, Telegram-dominant country
Pricing: ₽0 (free) → ₽499/mo (Pro) → ₽990/mo (Business)

## Seed Data

```python
SEED_DATA = {
    "entities": [
        {"id": "1", "name": "Иван Петров", "phone": "+79030000000", "tier": "free", "inn": "000000000000"},
        {"id": "2", "name": "Мария Сидорова", "phone": "+79037654321", "tier": "pro", "inn": "987654321098"},
    ],
    "slots": [
        {"id": "q1", "quarter": "Q2 2026", "deadline": "2026-07-25"},
        {"id": "q2", "quarter": "Q3 2026", "deadline": "2026-10-25"},
    ],
    "templates": [
        {"intent": "tax_reminder", "template": "До {deadline} осталось {days_left} дней. Сумма к уплате: ₽{tax_amount}."},
        {"intent": "invoice", "template": "Чек №{invoice_id} на сумму ₽{amount} для {client_name} готов."},
        {"intent": "expense_track", "template": "Расход ₽{amount} ({category}) сохранён. Баланс за месяц: ₽{monthly_balance}."},
    ],
}
```

## Intent Patterns

```python
INTENT_PATTERNS = {
    "invoice": ["чек", "выставить счёт", "invoice", "платёж"],
    "expense_track": ["расход", "потратил", "затраты", "expense"],
    "tax_calc": ["налог", "сколько платить", "рассчитай", "tax"],
    "receipt_scan": ["фото чека", "скан", "receipt", "приход"],
    "bank_parse": ["выписка", "банк", "парсинг", "bank statement"],
    "reminder": ["напомни", "срок", "дедлайн", "reminder"],
    "faq": ["как", "что", "помоги", "help", "справка"],
}
```

## Routing Rules

```python
ROUTING_RULES = {
    "free": {"max_invoices_per_month": 5, "max_expenses_per_month": 20, "tax_calc": "basic", "reminders": False},
    "pro": {"max_invoices_per_month": 100, "max_expenses_per_month": 500, "tax_calc": "advanced", "reminders": True, "bank_parse": True},
    "business": {"max_invoices_per_month": 1000, "max_expenses_per_month": 5000, "tax_calc": "advanced", "reminders": True, "bank_parse": True, "receipt_scan": True, "multi_client": True},
}
```

## Pricing Tiers

```python
PRICING_TIERS = {
    "free": {"price": 0, "currency": "RUB", "features": "5 invoices/mo, 20 expenses tracking, basic tax calc"},
    "pro": {"price": 499, "currency": "RUB", "features": "100 invoices/mo, bank statement parsing, tax reminders, advanced analytics"},
    "business": {"price": 990, "currency": "RUB", "features": "unlimited everything, receipt scanning OCR, multi-client, priority import"},
}
```

## Follow-Up Sequences

```python
FOLLOW_UP_SEQUENCES = {
    "tax_deadline": [
        {"delay_days": 14, "message": "До подачи налоговой декларации 14 дней. Сумма: ₽{estimated_tax}"},
        {"delay_days": 7, "message": "7 дней до дедлайна! Не забудьте оплатить налог."},
        {"delay_days": 1, "message": "ЗАВТРА дедлайн! Оплатите сегодня чтобы избежать штрафа."},
    ],
    "inactive_user": [
        {"delay_days": 14, "message": "Вы не выставляли чеки 2 недели. Всё в порядке?"},
        {"delay_days": 30, "message": "Месяц без активности. Попробуйте Pro — автоматический импорт из банка."},
    ],
}
```

## Result

- 12/12 tests pass
- FNS mock integration
- Bank statement parser (CSV/XLSX)
- Invoice generator
- Deploy time: 2 minutes (swap bot token)
