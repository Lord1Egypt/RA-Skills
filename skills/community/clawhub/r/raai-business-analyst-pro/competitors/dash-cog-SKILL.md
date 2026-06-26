# dash-cog — ClawHub SKILL.md (скачано с clawhub.ai) **Источник:** https://clawhub.ai/nitishgargiitd/dash-cog **Автор:** @nitishgargiitd (CellCog) **Версия:** v1.0.11 (12 версий, активно обновляется) **Загрузок:** 3 300 | **Звёзды:** 5 **Статус безопасности:** Benign (требует внешнюю зависимость CellCog SDK) **Цена:** бесплатно (но требует CellCog API ключ) **Зависимость:** `pip install -U cellcog`, `CELLCOG_API_KEY` --- ## Описание AI dashboard and web app generation powered by CellCog. Interactive dashboards, KPI trackers, data visualization, charts, analytics apps, data explorers, calculators, games. ## Что может генерировать **Analytics Dashboards:** Sales / Marketing / Financial / HR **KPI Trackers:** Business KPIs (MRR/CAC/LTV) / Project KPIs / SaaS Metrics **Data Visualizations:** Time Series / Comparisons / Geographic / Hierarchical / Network **Data Explorers:** Dataset Explorer / Survey Results / Log Analyzer **Interactive Apps:** Calculators / Configurators / Quizzes / Timelines **Games:** Puzzle / Memory / Trivia / Arcade ## Dashboard Features (все интерактивные) - Charts: Line / Bar / Pie / Scatter / Area / Heatmaps / Treemaps
- Filters: Date ranges / Dropdowns / Search / Multi-select
- KPI Cards с трендами
- Data Tables: сортировка / поиск / пагинация
- Drill-Down по клику
- Responsive (desktop + tablet + mobile)
- Dark/Light Themes ## Data Sources 1. Inline data в промпте (маленькие датасеты)
2. File upload (CSV / JSON / Excel через SHOW_FILE)
3. Sample/mock data (генерирует сам) ## Chat Modes - `"agent"` — стандартные дашборды, KPI, визуализации (по умолчанию)
- `"agent team"` — сложные приложения, игры, новаторские инструменты ## Ограничения - Требует CellCog SDK и API ключ (платно)
- Данные уходят на бэкенд CellCog
- Не подключается к внешним БД напрямую (только upload)
- Нет встроенного FP&A / unit economics расчётов
