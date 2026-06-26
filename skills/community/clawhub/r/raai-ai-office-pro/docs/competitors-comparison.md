# Конкурентный анализ AI-офис PRO vs ClawHub **Составлено:** 2026-04-19 С.19 на основе `openclaw skills install` + чтения SKILL.md каждого конкурента.
**Цель:** чёткое позиционирование AI-офис PRO относительно 3 ближайших конкурентов на ClawHub.
**Обновление:** при каждом bump-версии v3.X → пересмотр этой таблицы. --- ## Топ-3 прямых конкурента (по поиску `openclaw skills search "ceo" / "briefing"`) | Skill | Версия | Язык | Структура | Target | Подход |
|---|---|---|---|---|---|
| **ceo-master** | 1.0.0 | EN | 3 файла: SKILL.md, README.md, ceo_metrics.py | Venture scale (€0→€1B) | Musk/Bezos/Hormozi фреймворки. Файловая система `/workspace/CEO/*.md`. Weekly report в Telegram. Security L2 |
| **ceo-assistant** | 1.0.0 | EN | 1 файл: SKILL.md | Generic executives | Общий Goal → Milestones → Tasks → Next Action. Никакой методологии. |
| **morning-briefing-pro** | 1.0.2 | EN | 1 файл: SKILL.md | Пользователи macOS | Только утренний брифинг. Локальный CLI `briefing`. macOS-only (darwin) |
| **AI-офис PRO (наш)** | **3.5.0** | **RU (+ EN для поиска)** | **16 файлов:** SKILL + README + config × 2 + .env + install + test + 2 examples + 3 docs + 5 proof | **Российский СМБ 5-50 млн руб/мес, команда 5-50** | **9 методологий в одной коробке:** OKR (Doerr), Weekly Review (EOS/Wickman), Decision Log (Bezos с review-циклами), Эйзенхауэр, Утренний брифинг, Квартальное планирование, Делегирование с checkpoints, Investor Update, Стратегические приоритеты | --- ## Что у них есть / чего нет / есть у нас | Фича | ceo-master | ceo-assistant | morning-briefing-pro | **AI-офис PRO** |
|---|---|---|---|---|
| **Язык — русский** | ❌ | ❌ | ❌ | ✅ нативно + EN для ClawHub-поиска |
| **Метод: OKR (Doerr)** | частично | ❌ | ❌ | ✅ 70% threshold, weekly tracking, lag_alert |
| **Метод: Weekly Review (EOS Wickman)** | ❌ | ❌ | ❌ | ✅ пятница 17:00, шаблон, KPI-сверка |
| **Метод: Decision Log (Bezos)** | — упомянут | ❌ | ❌ | ✅ Type 1/2, review 30/60/90 дней, mandatory >50К ₽ |
| **Метод: Эйзенхауэр** | ❌ | ❌ | ❌ | ✅ urgent/important keywords, auto-delegation hints |
| **Утренний брифинг CEO** | ❌ | ❌ | ✅ **единственная фича** | ✅ + 8 других режимов |
| **Квартальное планирование** | ✅ scaling playbook | ❌ | ❌ | ✅ стратсессия + декомпозиция OKR |
| **Делегирование с checkpoints** | ❌ | — упомянуто | ❌ | ✅ gap 2 дня, acceptance_criteria, named_owner |
| **Investor Update** | ❌ | ❌ | ❌ | ✅ quarterly, board-ready формат |
| **config.yaml (настройка под бизнес)** | ❌ | ❌ | JSON для CLI | ✅ 98 строк (5 OBLIGATORY) + 387 строк deep |
| **Кейсы с рублями (proof)** | ❌ | ❌ | ❌ | ✅ 5 кейсов с конкретными ROI |
| **Dogfooding в своей компании** | ❌ | ❌ | ❌ | ✅ RAAI 19-25.04 (в процессе) |
| **install.sh автоустановка** | ❌ | ❌ | npm install | ✅ 15-минутная установка, копирует в target |
| **Smoke-test набор** | ❌ | ❌ | ❌ | ✅ 26 проверок за 3 сек |
| **ROI-калькулятор** | ❌ | ❌ | ❌ | ✅ docs/roi-calculator.md (в работе D.2) |
| **Marketing pack (onepager/comparison)** | ❌ | ❌ | ❌ | ✅ marketing/ (в работе D.4) |
| **Demo-видео через Claude Design** | ❌ | ❌ | ❌ | ✅ demo/video-2min.mp4 (в работе C.4) |
| **Before/After для клиента** | ❌ | ❌ | ❌ | ✅ в SKILL.md + README (в работе D.1) |
| **Integrations config (CRM/Sheets/TG/1C)** | TG weekly | ❌ | Calendar/Reminders macOS | ✅ Bitrix24/amoCRM/HubSpot/1C/МоеДело/Google |
| **Цена явная в пакете** | ❌ | ❌ | MIT (free) | ✅ **30 000 ₽** | **Итого фич уникальных у нас:** 13 из 20 — не встречаются ни у одного из 3 конкурентов. --- ## Кто для кого (разное позиционирование) | Продукт | Идеальный клиент | Цена | Почему выбирает |
|---|---|---|---|
| **ceo-master** | Стартап EN-аудитория, scaling from seed to IPO, команда с technical CTO | MIT free | Venture-frameworks + файловая структура workspace + weekly report автоматизм |
| **ceo-assistant** | Любой EN-говорящий executive | MIT free | Универсальный generic планировщик |
| **morning-briefing-pro** | macOS-пользователь который хочет только утренний брифинг | MIT free (+ npm package) | Узкий инструмент, простая установка |
| **AI-офис PRO (наш)** | **Российский CEO/собственник СМБ 5-50 млн руб/мес, команда 5-50 человек, нет корпоративных фреймворков, работает с Bitrix24/amoCRM/1C, пишет в Telegram** | **30 000 ₽** | **9 готовых методологий на русском с рублёвыми proof-кейсами + deep config под его бизнес + Russian SMB integrations** | **Главная асимметрия:** конкуренты — EN и generic или узкие. Мы — RU-нативный системный пакет с глубокой настройкой под российский СМБ. --- ## Риски позиционирования 1. **ceo-master может казаться серьёзнее** — у него security_level L2, Python-скрипт ceo_metrics.py, venture-brand. Mitigation: наш proof-пакет и dogfooding РЕАЛЬНЫЕ, а у него заявленные фреймворки без доказательств работы. 2. **MIT-free у конкурентов** — кто-то спросит «зачем платить 30К если ceo-master бесплатный». Mitigation: наш продукт — **продукт + сопровождение + русский рынок**, а не голый промпт. Кто умеет сам переводить/адаптировать EN-скиллы под RU-бизнес с 1C — пусть делает, но ROI-калькулятор покажет что стоимость адаптации выше нашей цены. 3. **100 студентов курса Косолапова+Кирилла** подадут Кириллу похожие коробки с теми же курсовыми шаблонами. Mitigation: dogfooding + 5 proof-кейсов с рублями + русская локализация под конкретный бизнес-профиль = не промпт, а готовая система. Никто из 100 не обкатывает на своей компании. --- ## Наш чек-лист дифференциации (для SKILL.md description) При каждой новой версии коробки — проверка: - [ ] **Russian native** мелькает в первых 3 строках description
- [ ] **9 methodologies in one skill** указано в первом абзаце EN-секции
- [ ] **ruble-denominated proof cases** упомянут в середине description
- [ ] **dogfooded at RAAI** явный маркер
- [ ] **Replaces Chief of Staff** ROI-обещание в секции выгод --- ## Bonus-конкуренты (сравнить позже если понадобится) | Skill | Заметки для позиционирования |
|---|---|
| `solo-ceo` | CN, one-person company model. Нам не конкурент (разная аудитория) |
| `ai-daily-briefing` | Калька morning-briefing-pro с memory. Узкая функция |
| `ai-ceo-automation` | «Full automated company operations» — амбициозно но SKILL.md не раскрыт |
| `ceo-xiaomao-agent` | CN, foreign-trade teams. Не пересекаемся | --- **Обновлять эту таблицу при каждом bump версии коробки и каждом появлении нового ClawHub-конкурента в категории CEO/executive/briefing.**
