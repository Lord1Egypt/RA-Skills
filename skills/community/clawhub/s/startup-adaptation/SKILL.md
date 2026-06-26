# Стратег адаптации стартапов для РФ

## Контекст

Этот скилл используется для поиска и оценки западных стартапов с доказанным PMF, которые могут быть адаптированы для российского рынка с учётом санкций, регуляторных барьеров и отсутствия локальных аналогов.

Работа ведётся по принципу **Vibe Coding MVP** — 3 ночи / ~1 месяц до рабочего прототипа.

---

## ЭТАПЫ ПАЙПЛАЙНА

Каждый кандидат проходит 5 этапов. Только GREEN-кандидаты доходят доGitHub libraries и copy-paste плана.

### Этап 1 — СТРАТЕГ (анализ кандидата)

**Формат**: структурированный анализ по 6 блокам.

**Шаблон**:
```
## Кандидат: [Название]
### Суть
Идея в одном предложении.

### Целевая аудитория
Кто в РФ будет платить.

### Боли
3 ключевых проблемы, которые решает продукт.

### Почему это НЕ работает на Западе (для РФ)
Барьеры входа, санкции, регуляторика.

### Кризисный профиль
✅ Высокий / ⚠️ Средний / ❌ Низкий — фрилансеры/малый бизнес сокращают расходы во время кризиса.

### Оценка сложности адаптации
- Что нужно перестроить/заменить
- Какие российские аналоги существуют
- Оценка времени: 1-4 недели / 1-2 месяца / 3+ месяца
```

---

### Этап 2 — idea-reality-mcp API

**URL**: `POST https://idea-reality-mcp.onrender.com/api/check`

**Тело запроса**:
```json
{
  "idea_text": "описание идеи для российской аудитории",
  "depth": "deep"
}
```

**Что смотреть в ответе**:
- `reality_signal` — 0-100, чем выше тем лучше
- `trend` — accelerating/stable/decelerating
- `duplicate_likelihood` — low/medium/high
- `market_momentum` — 0-100
- `pivot_hints` — подсказки по пивоту в нишу где нет конкурентов
- **0 HN posts** в любом запросе = белый рынок

**Пороговые значения для продолжения**:
- `reality_signal` ≥ 55
- `trend` = accelerating
- `duplicate_likelihood` ≠ high
- хотя бы один запрос с 0 HN posts

---

### Этап 3 — ВЕРИФИКАТОР (14 пунктов)

Каждый пункт оценивается: ✅ / ⚠️ / ❌

| # | Критерий | Суть |
|---|----------|------|
| 1 | **PMF за рубежом** | Продукт имеет доказанный PMF (MRR, ARR, valuation, users) |
| 2 | **Барьер для входа в РФ** | Санкции, regulatory, blocked APIs, нет интереса — объективный барьер |
| 3 | **Структурный барьер** | Western SaaS не работает в РФ без адаптации |
| 4 | **Нет сильного российского аналога** | Не найдено конкурентов при проверке |
| 5 | **Для РФ нужен ребилд** | Western dependencies требуют замены на российские аналоги |
| 6 | **Пригодность для vibe coding** | 1-2 разработчика, 1-4 недели на MVP |
| 7 | **Кризисный профиль** | Решает проблему экономии времени/денег |
| 8 | **CRDT-viability** | ЮKassa, СБП, USDT, Telegram Stars — доступные способы приёма платежей |
| 9 | **Команда/единомышленники** | Есть сообщество, библиотеки, документация |
| 10 | **Legal/Compliance** | Не требует лицензий, special permits |
| 11 | **Монетизация** | Ясная модель, понятная цена |
| 12 | **Масштабируемость** | Горизонтально масштабируется |
| 13 | **Выход на рынок** |渠道 — Product Hunt, Telegram-каналы, Indie Hackers |
| 14 | **Время до MVP** | ≤ 4 недель |

**Итог**: ✅ 10-14 = GREEN, ⚠️ 7-9 = YELLOW, ❌ ≤6 = RED

---

### Этап 4 — GitHub Libraries

Найти библиотеки по категориям:

**Python (предпочтительно)**:
```
- aiogram / pyrogram / telethon (Telegram bots)
- fastapi / flask (web framework)
- reportlab / weasyprint (PDF generation)
- asyncpg / aiomysql (database)
- aiohttp / httpx (API calls)
- vosk / speech_recognition (voice)
- yandexcloud / boto3 (cloud)
```

**Node.js**:
```
- grammY / telegraf (Telegram)
- express / fastify (web)
- pdfkit (Node.js) (PDF)
- prisma / drizzle (database)
```

**Hosting (РФ)**:
```
- Yandex Cloud
- VK Cloud
- Selectel
- SberCloud
```

---

### Этап 5 — Copy-Paste Plan

```
## MVP Roadmap ([Кандидат])

### Week 1-2: Core MVP
- День 1-2: [шаг]
- День 3-4: [шаг]
- ...

### Week 3-4: Polish + Payments
- ...

### Tech Stack
- Backend:
- Database:
- Payments:
- Hosting:

### MRR Goals
- Month 1: [цель]
- Month 3: [цель]
- Month 6: [цель]
```

---

## КРИТИЧЕСКИЕ ПРАВИЛА

### 🔴 КАТЕГОРИИ-ТАБУ (автоматический RED)

Не проверять категории где уже найдены российские конкуренты:

1. **Кросспостинг SMM** — SMMplanner, Postmypost, Socposter, SMMBox (от 562 руб/мес)
2. **Telegram CRM для B2B** — CRMchat, Salebots, Botsap
3. **Invoice + 1C интеграция** — Vysor (@vysorbot), BuhBot, officeRebot, 1С-Коннект
4. **SEO-мониторинг Yandex** — @YandexPositions_bot, @LiftwebPositionsBot, Topvisor, SeoLik
5. **Telegram подписки/payments** — GramMonetize ($4.2M+ оборот), Telegram Subscription Manager, Smartbot Pro
6. **Формы/конструкторы** — Tally, Google Forms (устарел)
7. **Голосовые роботы для колл-центров** — Sber SaluteSpeech, VoiceBox, Voximplant, Neuro.net

### ⚠️ ВСЕГДА ПРОВЕРЯТЬ РОССИЙСКИЙ РЫНОК

**НЕ ДОСТАТОЧНО**: HN posts, GitHub stars, npm packages.

**ОБЯЗАТЕЛЬНО проверять**:
- Поиск в Google: `[название категории] Россия` / `российские [название]`
- Домены: .ru, vc.ru, habr.com, tenchat.ru, otzovik.com
- Telegram-боты: search in Telegram, t.me/bot
- GitHub-репозитории на русском
- Открытые Telegram-каналы про эту нишу

**Алгоритм проверки конкурентов**:
1. Поиск в Google: `site:vc.ru [ниша]` + `site:habr.com [ниша]`
2. Поиск в Telegram: название категории + "бот"
3. Проверка GitHub: запросы на русском языке
4. Проверка Otzovik/Flatstack: есть ли обзоры/рейтинги

**Критерий RED**: найдено 3+ российских конкурента с аналогичным функционалом по цене < 2000 руб/мес

### ✅ КРИТЕРИИ WHITE SPACE

Ниша считается свободной если:
- 0 HN posts за последний год
- ≤ 2 российских конкурента с устаревшим/неполным функционалом
- Или конкуренты существуют но дорогие/сложные для SMB

---

## ФИЛЬТР СТРАН

Приоритет порядок — страна за страной, категория за категорией:

### Tier 1 — Беспрепятственный вход
- 🇧🇷 **Бразилия** — PIX работает, нет санкций, Nubank/VKontakte Parallel
- 🇮🇳 **Индия** — UPI, Razorpay работают
- 🇻🇳 **Вьетнам / 🇮🇩 Индонезия** — быстрорастущий рынок

### Tier 2 — Требуют замены платформы
- 🇰🇷 **Южная Корея** — Kakao/Naver вместо Google/Facebook
- 🇯🇵 **Япония** — LINE вместо WhatsApp
- 🇩🇪 **Германия** — Wirecard/N26 заменяемы

### Tier 3 — Сложная адаптация
- 🇺🇸 **США** —，大部分 SaaS требует перестройки
- 🇨🇳 **Китай** — Great Firewall, Alipay/WeChat Pay
- 🇬🇧 **Великобритания** — Stripe/PayPal → ЮKassa/SBП

---

## КРИЗИСНЫЙ ПРИОРИТЕТ

Во время экономического спада/кризиса приоритет отдаётся:

1. ✅ **Upskilling** — повышение квалификации (EdTech, языки, программирование)
2. ✅ **Automation** — автоматизация рутины (боты, интеграции)
3. ✅ **Productivity** — инструменты продуктивности (time tracking, task management)
4. ✅ **Cost-saving** — экономия денег (сравнение цен, оптимизация расходов)
5. ❌ **Luxury spending** — развлечения, luxury-продукты

---

## ЗАПРЕЩЁННЫЕ ТЕХНОЛОГИИ

**Замены для России**:

| Запрещено | Заменить на |
|-----------|-------------|
| Stripe | ЮKassa, СБП, Telegram Stars, ЮMoney |
| PayPal | ЮKassa, ЮMoney |
| AWS/GCP/Azure | Yandex Cloud, VK Cloud, Selectel |
| Google Analytics | Яндекс.Метрика |
| OpenAI API | Yandex GPT (SaluteGPT), GigaMind |
| Twilio | Voximplant, SberVox, МТС Линк |
| Notion | NocoDB, Seatable |
| Airtable | NocoDB, Smart Tables |

---

## ВЫХОДНОЙ ФОРМАТ

После каждого кандидата выводить:

```
## [Номер]. [Название продукта] — [ORIGIN COUNTRY]

### 1. СТРАТЕГ
[анализ по шаблону]

### 2. API
- reality_signal: [число]
- trend: [accelerating/stable/decelerating]
- duplicate_likelihood: [low/medium/high]
- ключевые HN данные: [0 постов = хорошо]
- pivot_hints: [подсказки]

### 3. ВЕРИФИКАТОР
[таблица 14 пунктов]
ИТОГ: 🟢 GREEN / 🟡 YELLOW / 🔴 RED

### 4. GitHub Libraries
[список с stars count]

### 5. Copy-Paste Plan
[по шаблону]
```

---

## КАЛЕНДАРЬ РАБОТЫ

1. Читать `SKILL.md` в начале каждой сессии
2. Сверяться с категориями-табу перед новой проверкой
3. Проверять российский рынок параллельно с HN/GitHub/npm
4. Фиксировать все найденные конкуренты с ценами
5. Обновлять память после каждого кандидата