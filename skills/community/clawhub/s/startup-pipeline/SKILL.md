# Startup Adaptation Pipeline — WORKFLOW v3.1

## Обзор

Систематический поиск и адаптация западных стартапов с PMF для российского рынка.

**Pipeline**: Стратег → API → Verifier → GitHub Libraries → Copy-Paste Plan

**Срок**: Vibe Coding MVP — 3 ночи / ~1 месяц

---

## ЦЕПОЧКА — 6 ШАГОВ

### ШАГ 1: ГЛУБОКИЙ ПОИСК И АНАЛИЗ

**Принцип:** Не торопиться. Перебирать 5–7 кандидатов из разных регионов, сравнивать, только потом выбирать лучшего.

**Источники:**
- Банковская аналитика: Sberbank Analytics, Тинькофф Исследования, ВТБ Капитал
- Венчурные: РВК, ФРИИ, Y Combinator batch-отчёты, Sequoia, a16z, Index Ventures
- Аналитические: CB Insights, Crunchbase, PitchBook, Tracxn
- Региональные: 36Kr/iResearch (Китай), e27/TechInAsia (ЮВА), LatamVC (Латинская America)
- Консалтинг: McKinsey, BCG, Bain, Deloitte
- Трекинг: SimilarWeb, SensorTower, Google Trends, Яндекс.Вордстат

**Для каждого кандидата фиксировать:**
1. Откуда стартап (страна, регион)?
2. Какую проблему решает (боль → решение)?
3. Какой доказанный PMF (метрики, раунды, пользователи)?
4. Сколько стран/рынков захватил?
5. **Почему НЕ может зайти в РФ?** (конкретные барьеры)
6. **Есть ли в РФ спрос на аналоги?** (Вордстат, форумы, чаты)
7. **Есть ли в РФ прямые конкуренты?** Насколько слабы?

**Конкурентный скан по 6 источникам:**

| Источник | Что искать | Вес |
|----------|-----------|-----|
| GitHub | Репозитории + звёзды | 22% |
| Hacker News | Обсуждения + upvotes | 14% |
| npm | JS/TS-пакеты | 18% |
| PyPI | Python-пакеты | 13% |
| Product Hunt | Запуски конкурентов | 14% |
| Stack Overflow | Вопросы = спрос | 10% |

---

### ШАГ 2: ДЕКОМПОЗИЦИЯ ОРИГИНАЛА

- **Core Feature** — 1 функция, 1 предложение
- **Воронка** — как попадают → активируются → платят → возвращаются
- **Монетизация** — модель, цены, LTV, CAC
- **Технический стек** — зависимости, API
- **Сетевой эффект** — есть/нет, как запускается?

---

### ШАГ 3: РЕАЛИИ РФ — АДАПТАЦИЯ

**Платёжные системы (СТРОГО эти, НЕ Stripe/PayPal/Square):**

| Задача | РФ-решение | Модель | Комиссия |
|--------|-----------|--------|----------|
| Приём карт | ЮKassa / Тинькофф Касса | acquiring | 2.8–3.5% |
| P2P-переводы | СБП | bank transfer | 0–0.5% |
| Telegram-платежи | Telegram Stars / ЮKassa | in-app | 5–15% / 2.8% |
| Крипта | BTC/USDT через P2P | crypto | variable |
| Подписки | ЮKassa recurring / Тинькофф | subscription | 2.8–3.5% |

**Инфраструктура:**

| Задача | РФ-решение | Fallback |
|--------|-----------|----------|
| Хостинг | Selectel / Timeweb / RUVDS | Cloudflare DNS-proxy |
| База данных | Selectel Managed PostgreSQL | Яндекс.Облако |
| CDN | Selectel CDN / Яндекс.CDN | Cloudflare |
| Auth | Telegram Login Widget | email magic link |
| LLM | GigaChat (не OpenAI!) | — |
| Email | UniSender / Sendsay (не SendGrid!) | Яндекс.360 |

**Юридическое:**
- **152-ФЗ** — данные граждан РФ хранить на серверах в РФ
- **РКН** — регистрация как оператор ПДн
- **54-ФЗ** — онлайн-касса при приёме платежей физлиц
- Политика конфиденциальности + пользовательское соглашение — обязательны

**SEO для Яндекса:**
- Навигационные запросы («X аналог», «X замена») — **наше золото!**
- Информационные («как сделать X») — конкуренция низкая-средняя
- Транзакционные («купить X») — конкуренция высокая

---

### ШАГ 4: МАРКЕТИНГОВЫЙ АУДИТ ОРИГИНАЛА

1. Канал привлечения — откуда основной трафик?
2. Воронка конверсии — free→paid? Freemium→premium?
3. Позиционирование — для кого? USP в 1 предложении
4. Виральная механика — рефералки? UGC? Сетевой эффект?
5. Retention — почему возвращаются?
6. Контент — что генерирует лиды?

**Адаптация каналов для РФ:**

| Глобальный | РФ-аналог |
|-----------|-----------|
| Google Ads | Яндекс.Директ + VK Реклама |
| Twitter/X | Telegram-каналы + VC.ru |
| Product Hunt | VC.ru + Habr + Telegram-рассылка |
| SEO (Google) | SEO (Яндекс) + Яндекс.Дзен |
| LinkedIn | VC.ru + Telegram-комьюнити |
| Influencer | Telegram-блогеры + YouTube-техблогеры |

---

### ШАГ 5: RED TEAM CHECK

#### 5A: idea-reality-mcp API

```
POST https://idea-reality-mcp.onrender.com/api/check
Body: {"idea_text": "...", "depth": "deep"}
```

**Интерпретация:**

| Условие | Вердикт |
|---------|---------|
| < 30 + accelerating | 🟢 Свободная ниша |
| 30–60 + accelerating | 🟡 Рынок растёт, ищем нишу |
| > 60 + accelerating | 🟡 Горячий рынок |
| > 60 + declining | 🔴 Затухающий |
| > 75 (любой) | 🔴 Уже реализовано |

**Ключевые требования:**
- `reality_signal` ≥ 55
- `trend` = accelerating
- `duplicate_likelihood` ≠ high
- Хотя бы один HN-запрос с **0 posts**

#### 5B: РФ-специфика (ручная проверка)

| Проверка | Красный флаг |
|----------|-------------|
| Спрос | Вордстат < 1000/мес |
| Регуляторика | РКН заблокирует, 152-ФЗ невозможно |
| Конкуренты | 3+ сильных аналога |
| Юнит-экономика | CAC > LTV |
| Техническая реализуемость | Зависимость от заблокированных API |
| Маркетинговая доступность | Нет каналов с CAC < LTV |

---

### ШАГ 6: VIBE CODING PLAN — 3 НОЧИ НА MVP

**Ночь 1: Core Feature**
- Next.js 14+ (App Router) + Tailwind CSS + shadcn/ui
- Selectel Managed PostgreSQL + Drizzle ORM
- ТОЛЬКО core feature
- Минимальная авторизация (Telegram Login Widget)
- Деплой на Selectel / Vercel через Cloudflare DNS-proxy

**Ночь 2: Auth + Payments + Landing**
- Полная авторизация
- ЮKassa (acquiring 2.8–3.5%) или СБП
- Landing page: Hero → Problem → Solution → Pricing → CTA
- Яндекс.Метрика + goals
- Политика конфиденциальности + Пользовательское соглашение

**Ночь 3: Polish + Deploy + First Post**
- Favicon, OG-метки, мета-описания для Яндекса
- Mobile-responsive
- Первый пост: VC.ru + Habr + 5 Telegram-каналов
- Реферальная механика (если применимо)
- Мониторинг: UptimeRobot

---

## ФИЛЬТР СТРАН (приоритет)

1. 🇧🇷 Бразилия — PIX, нет санкций
2. 🇰🇷 Корея — Kakao/Naver platform
3. 🇮🇳 Индия — UPI, Razorpay
4. 🇻🇳🇮🇩 Вьетнам/Индонезия — быстрорастущий
5. 🇯🇵 Япония — LINE platform
6. 🇩🇪 Германия — Wirecard → ЮKassa

---

## КРИЗИСНЫЙ ПРИОРИТЕТ

| Приоритет | Категория | Почему |
|-----------|-----------|--------|
| ✅ 1 | Upskilling | Кризис → люди учатся |
| ✅ 2 | Automation | Автоматизация рутины |
| ✅ 3 | Productivity | Инструменты продуктивности |
| ✅ 4 | Cost-saving | Экономия денег |
| ❌ | Luxury | Не для кризиса |

---

## ВЫХОДНОЙ ФОРМАТ (для каждого кандидата)

```
## [Номер]. [Название] — [СТРАНА]

### 1. СТРАТЕГ
[анализ по шаблону]

### 2. API CHECK
- reality_signal: [число]
- trend: [accelerating/stable]
- 0 HN posts: [да/нет]
- pivot_hints: [подсказки]

### 3. VERIFIER
[таблица 14 пунктов]
**ИТОГ**: X ✅ / Y ⚠️ / Z ❌
**ВЕРДИКТ**: 🟢 GREEN / 🟡 YELLOW / 🔴 RED

### 4. GitHub Libraries
[список с stars]

### 5. Copy-Paste Plan
[по шаблону]
```

---

## КАТЕГОРИИ-ТАБУ (АВТОМАТИЧЕСКИЙ RED)

| Категория | Почему |
|-----------|--------|
| Кросспостинг SMM | SMMplanner, Postmypost — занято |
| Telegram CRM B2B | CRMchat, Salebots — занято |
| Invoice + 1C | Vysor, BuhBot — занято |
| Yandex SEO | Topvisor, SeoLik — занято |
| Telegram Payments | GramMonetize — занято |
| Формы/конструкторы | Tally, Google Forms |
| Voice AI колл-центры | Sber SaluteSpeech, Voximplant |
| HealthTech / MedTech / BioTech / FemTech | Лицензии, ЕМИАС, 152-ФЗ медданные |

---

## ЗАПРЕЩЁННЫЕ ЗАВИСИМОСТИ

| Заменить | На |
|---------|----|
| Stripe, PayPal, Square | ЮKassa, СБП, Telegram Stars, USDT |
| AWS, GCP, Azure | Yandex Cloud, VK Cloud, Selectel |
| OpenAI | GigaChat (не OpenAI!) |
| Google Analytics | Яндекс.Метрика |
| Twilio | Voximplant, SberVox |
| SendGrid | UniSender, Sendsay |
| Notion | NocoDB, Seatable |
| Supabase (EU) | Selectel Managed PostgreSQL |

---

## КАЛЕНДАРЬ

1. Прочитать этот SKILL.md в начале каждой сессии
2. Применять все 6 шагов последовательно
3. Проверять российский рынок параллельно с HN/GitHub
4. Фиксировать конкурентов с ценами
5. Обновлять память после каждого кандидата
