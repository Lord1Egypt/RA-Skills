# Studio Booking

Скилл для автоматизации бронирования студии звукозаписи через Telegram-бота.

## Когда использовать

- Пользователь хочет забронировать студию (дата, время, длительность)
- Администратор управляет бронями (создание, отмена, перенос)
- Клиент спрашивает свободные слоты, цены, услуги
- Нужно сгенерировать ссылку на оплату через TelegaPay
- Требуется крос-сейл дополнительных услуг (звукорежиссёр, мастеринг, сессионный музыкант)
- Клиент спрашивает статус своей брони или историю посещений

## Инструкции

### 1. Квалификация лида

Перед началом бронирования определи тип клиента:

**Новый клиент:**
- Уточни: тип проекта (запись трека, сведение, мастеринг, репетиция)
- Бюджет и предпочтительное время
- Запроси контакт для подтверждения (если не указан)
- Предложи экскурсию по студии перед бронированием

**Постоянный клиент:**
- Приветствуй по имени, напомни о прошлом проекте
- Спроси, нужна ли та же конфигурация (микрофоны, оборудование)
- Предложи скидку за лояльность (если >5 броней)

### 2. Проверка слотов

Используй следующий SQL-шаблон для проверки доступности слота:

```sql
SELECT s.id, s.start_time, s.end_time, s.price
FROM slots s
WHERE s.date = :date
  AND s.is_available = 1
  AND s.id NOT IN (
    SELECT b.slot_id FROM bookings b
    WHERE b.status IN ('pending', 'confirmed', 'paid')
      AND b.cancelled_at IS NULL
  )
  AND (
    CAST(strftime('%s', s.start_time) AS INTEGER) >= CAST(strftime('%s', :time_from) AS INTEGER)
  )
ORDER BY s.start_time;
```

Параметры:
- `:date` — дата в формате `YYYY-MM-DD`
- `:time_from` — минимальное время начала (например `10:00`)

Если слотов нет — предложи соседние даты (±3 дня).

### 3. Создание бронирования

SAGA-паттерн из 5 шагов:

```python
STEPS = [
    ("validate_slot", lambda: check_slot_available(db, slot_id)),
    ("create_booking", lambda: create_booking_record(db, user_id, slot_id, service_id)),
    ("hold_payment", lambda: hold_invoice(payment, booking_id, amount)),
    ("send_confirmation", lambda: send_booking_notification(bot, chat_id, booking_id)),
    ("notify_admin", lambda: notify_admin_new_booking(bot, admin_chat_id, booking_id)),
]

COMPENSATIONS = {
    "validate_slot": None,
    "create_booking": lambda: delete_booking_record(db, booking_id),
    "hold_payment": lambda: cancel_invoice(payment, invoice_id),
    "send_confirmation": lambda: True,
    "notify_admin": lambda: True,
}
```

Каждый шаг должен иметь timeout 30 секунд. Компенсации запускаются в обратном порядке при фейле любого шага.

### 4. TelegaPay — генерация ссылки на оплату

```python
import hashlib
import hmac
import json
from urllib.parse import urlencode


def generate_telegapay_link(
    amount: int,
    order_id: str,
    description: str,
    secret_key: str,
    shop_id: str,
    callback_url: str,
    user_phone: str = "",
    expires_in: int = 3600,
) -> str:
    payload = {
        "amount": str(amount),
        "order_id": order_id,
        "description": description,
        "shop_id": shop_id,
        "callback_url": callback_url,
        "expires_in": str(expires_in),
    }
    if user_phone:
        payload["phone"] = user_phone

    sign_str = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    signature = hmac.new(
        secret_key.encode(), sign_str.encode(), hashlib.sha256
    ).hexdigest()
    payload["signature"] = signature
    return f"https://telegapay.com/pay?{urlencode(payload)}"
```

### 5. Крос-сейл матрица

Предлагай дополнительные услуги на основе выбранной основной:

| Основная услуга | Крос-сейл 1 | Крос-сейл 2 | Крос-сейл 3 |
|---|---|---|---|
| Запись вокала | Сведение (+40%) | Мастеринг (+25%) | Бэк-вокалист (+60%) |
| Запись инструмента | Сведение (+40%) | Студийный гитарист (+50%) | Рейк-микрофон (+15%) |
| Сведение | Мастеринг (+25%) | Стем-рендер (+10%) | Контрольный прослушивание (+5%) |
| Мастеринг | Винтаж-пресс (+80%) | Продвинутый лимитер (+30%) | — |
| Репетиция | Звукорежиссёр (+35%) | Запись репетиции (+50%) | — |

Процент — наценка к базовой стоимости.

### 6. Управление бронями

**Отмена брони:**

```python
async def cancel_booking(db, booking_id: int, reason: str = "", refund: bool = False):
    booking = await db.fetch_one(
        "SELECT * FROM bookings WHERE id = ?", (booking_id,)
    )
    if not booking:
        raise ValueError("Booking not found")

    async with db.transaction():
        await db.execute(
            "UPDATE bookings SET status = 'cancelled', cancelled_at = datetime('now'), "
            "cancel_reason = ?, refunded = ? WHERE id = ?",
            (reason, int(refund), booking_id),
        )
        if refund and booking.get("paid_at"):
            await refund_telegapay(booking["invoice_id"], booking["amount"])

        await db.execute(
            "UPDATE slots SET is_available = 1 WHERE id = ?",
            (booking["slot_id"],),
        )
```

**Календарь занятости:**

```python
async def get_occupancy_calendar(db, year: int, month: int) -> dict:
    """Возвращает словарь {день: количество броней} за месяц."""
    rows = await db.fetch_all(
        """SELECT CAST(strftime('%d', s.date) AS INTEGER) as day, COUNT(*) as count
           FROM bookings b
           JOIN slots s ON b.slot_id = s.id
           WHERE strftime('%Y-%m', s.date) = ?
             AND b.status IN ('confirmed', 'paid')
           GROUP BY day""",
        (f"{year:04d}-{month:02d}",),
    )
    return {row["day"]: row["count"] for row in rows}
```

### 7. Клиентский трекинг

**История посещений:**

```sql
SELECT b.id, s.date, s.start_time, s.end_time,
       sv.name as service, b.amount,
       b.status, b.created_at
FROM bookings b
JOIN slots s ON b.slot_id = s.id
JOIN services sv ON b.service_id = sv.id
WHERE b.user_id = :user_id
  AND b.status IN ('paid', 'confirmed')
ORDER BY s.date DESC, s.start_time DESC
LIMIT 20;
```

**Статистика клиента:**

```python
async def client_stats(db, user_id: int) -> dict:
    row = await db.fetch_one(
        """SELECT COUNT(*) as total_bookings,
                  SUM(amount) as total_spent,
                  COUNT(DISTINCT strftime('%Y-%m', s.date)) as months_active,
                  MAX(s.date) as last_visit
           FROM bookings b
           JOIN slots s ON b.slot_id = s.id
           WHERE b.user_id = ? AND b.status = 'paid'""",
        (user_id,),
    )
    return dict(row) if row else {}
```

### 8. Уведомления

- **Клиенту за 2 часа:** напоминание о брони
- **Клиенту через 1 час после брони:** отзыв
- **Админу:** новая бронь, отмена, просрочка оплаты
- **Клиенту через 1 день:** предложение повторить (снарядить крос-сейл)

### 9. Обработка ошибок

| Ситуация | Действие |
|---|---|
| Слот занят в момент оплаты | Предложить альтернативный слот, отменить инвойс |
| TelegaPay timeout | Retry 3 раза с exponential backoff (1s, 3s, 9s) |
| Дупликат брони (user+slot+status) | Вернуть существующую бронь, не создавать новую |
| Дата в прошлом | Отказать с сообщением "Нельзя бронировать прошлое" |
| Минимальное время до слота | <2 часов — отказать, предложить следующий день |

### 10. Стоимость и пакеты

```python
PRICING_RULES = {
    "base_hourly": 2500_00,
    "min_booking": 2,
    "discounts": {
        "3_hours": 0.05,
        "5_hours": 0.10,
        "night_rate": 0.80,
        "weekend": 1.15,
        "loyalty_5plus": 0.10,
    },
    "extras": {
        "engineer": 800_00,
        "mixing": 3500_00,
        "mastering": 2000_00,
        "backup_copy": 500_00,
    },
}
```

### 11. Интеграция с Telegram-ботом

```python
async def booking_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, *params = query.data.split(":")
    booking_flow = BookingCoordinator(db, payment, bot)

    match action:
        case "calendar":
            await booking_flow.show_calendar(query)
        case "select_date":
            await booking_flow.show_time_slots(query, params[0])
        case "select_time":
            await booking_flow.show_services(query, params[0])
        case "select_service":
            await booking_flow.show_extras(query, params[0], params[1])
        case "confirm":
            await booking_flow.run_saga(query, params)
        case "pay":
            await booking_flow.generate_payment(query, params[0])
```

## Референсы

- Документация TelegaPay: `https://telegapay.com/docs`
- python-telegram-bot: `https://docs.python-telegram-bot.org/`
- Формат времени: `HH:MM` в 24-часовом формате
- Даты: `YYYY-MM-DD` (ISO 8601)
- Цены: int, минимальная единица — копейка (1 рубль = 100)
- Часовой пояс: Europe/Moscow (UTC+3, без DST)
