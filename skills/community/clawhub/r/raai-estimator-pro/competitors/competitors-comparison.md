# estimator-pro — Анализ конкурентов (verified + гипотезы, перезаписано 2026-04-20) > Источник: прямой скрейп clawhub.ai через firecrawl 2026-04-20. Конкурент 3 — 🟡 гипотеза (нет прямого скилла на ClawHub). --- ## Конкурент 1: afrexai-construction-estimator by @1kalin **✅ verified** | URL: https://clawhub.ai/1kalin/afrexai-construction-estimator **Загрузок:** 929 | **Звёзды:** 2 | **Версия:** v1.0.0 | **Цена:** бесплатно **Что делает:** Полная методология строительного сметирования — от классификации проекта до подачи тендера. 12 фаз, CSI MasterFormat, RSMeans бенчмарки, EVM, 100-балльная рубрика качества. **Количество триггеров/режимов:** 12 команд / 12 фаз. **Ключевые фичи:**
- Estimate Type Matrix: 5 типов от Order-of-Magnitude до Control
- QTO по CSI MasterFormat 2018 (24 дивизии + waste factors)
- Sub Quote Scoring Matrix (5 факторов)
- Earned Value Management (SPI/CPI/EAC/VAC)
- VE Opportunity Matrix (8 систем, типовые savings %)
- Change Order YAML Template + T&M документация
- 100-Point Estimate Quality Rubric
- RSMeans City Cost Indices (20 US городов) **Таблица различий:** | Фича | afrexai-construction-estimator | НАША |
|---|---|---|
| Российская нормативная база (ГЭСН/ФЕР/ТЕР) | НЕТ (RSMeans/CSI US) | ДА |
| Форматы РФ (КС-2/КС-3/КС-6) | НЕТ | ДА |
| Русский язык | НЕТ | ДА |
| Региональные коэффициенты РФ | НЕТ | ДА |
| Госзаказ / 44-ФЗ | НЕТ | ДА |
| Methodology (12 фаз) | ДА | ДА |
| QTO / Takeoff | ДА | ДА |
| Change Order management | ДА | ДА | --- ## Конкурент 2: open-construction-estimate by @datadrivenconstruction **✅ verified** | URL: https://clawhub.ai/datadrivenconstruction/open-construction-estimate **Загрузок:** 1 700 | **Звёзды:** 2 | **Версия:** v2.0.0 | **Цена:** бесплатно **Статус безопасности:** Benign (medium confidence) — требует network + filesystem **Что делает:** ML-автоматизация сметирования через сопоставление BIM-элементов с открытой базой 55k+ позиций (TF-IDF + sentence-transformers). Региональные коэффициенты включают moscow/spb/regions_ru. **Ключевые фичи:**
- 55,000+ work items (OpenConstructionEstimate база)
- Semantic matching: TF-IDF + all-MiniLM-L6-v2
- BIM Integration (IFC-элементы → позиции сметы)
- Regional factors: moscow(1.20) / spb(1.10) / regions_ru(0.85)
- Excel export
- Требует Python + pandas + sentence-transformers **Таблица различий:** | Фича | open-construction-estimate | НАША |
|---|---|---|
| Официальная база РФ (ГЭСН/ФЕР) | НЕТ (open source база) | ДА |
| Форматы КС-2/КС-3 | НЕТ | ДА |
| Без программирования | НЕТ (требует Python) | ДА |
| Русский язык | НЕТ (EN-only) | ДА |
| Госзаказ / 44-ФЗ | НЕТ | ДА |
| BIM integration | ДА | 🟡 планируется |
| Региональные коэффициенты РФ | ДА (базовые) | ДА (полные ФЕРы) | --- ## Конкурент 3: Сметные ИИ-ассистенты (веб-сервисы) **🟡 гипотеза** — поиск clawhub.ai по запросам "смета / estimate / КС-2 / ГЭСН / ФЕР" вернул 0 релевантных скиллов на ClawHub (2026-04-20). **Потенциальные конкуренты за пределами ClawHub:**
- Сметный ИИ (beta): российские веб-стартапы типа SmartEstimate / EstimAI
- GPT-промпты на Gumroad/PromptBase для работы со сметами
- Excel/Google Sheets шаблоны смет с ChatGPT интеграцией **Оценка угрозы:**
- На ClawHub нет прямых конкурентов в российском сметировании — ниша пустая
- Западные сметные скиллы (CSI/RSMeans) не применимы для работы с ГЭСН/ФЕР без переработки
- Bariera входа: знание норматив РФ + язык = уникальная позиция RAAI --- ## Сводная таблица + наши дифференциаторы | Дифференциатор | afrexai-estimator | open-estimate | рф-конкуренты | НАША |
|---|---|---|---|---|
| ГЭСН/ФЕР/ТЕР (нормативы РФ) | НЕТ | НЕТ | 🟡 частично | **ДА** |
| Форматы КС-2/КС-3/КС-6 | НЕТ | НЕТ | 🟡 частично | **ДА** |
| Русский язык | НЕТ | НЕТ | ДА | **ДА** |
| Госзаказ / 44-ФЗ | НЕТ | НЕТ | НЕТ | **ДА** |
| Без кода/настройки | ДА | НЕТ (Python) | НЕТ | **ДА** |
| Безопасность Benign | ДА | ДА | н/д | **ДА** |
| ClawHub / OpenClaw нативно | ДА | ДА | НЕТ | **ДА** | --- ## 6 verified дифференциаторов estimator-pro 1. **Нормативная база РФ** — ГЭСН, ФЕР, ТЕР, ФССЦ — ни у одного конкурента на ClawHub нет. Это структурная пустая ниша.
2. **Формы КС-2/КС-3** — стандартные формы актов о приёмке и справок о стоимости. Западные конкуренты работают с US bid forms.
3. **Русский язык** — оба verified конкурента EN-only. @datadrivenconstruction добавил RU коэффициенты но сам инструмент на английском.
4. **Госзаказ / 44-ФЗ** — тендерные процедуры, требования к сметной документации для государственных контрактов — ни у кого нет.
5. **Без программирования** — open-construction-estimate требует Python + ML-стек. Наша — instruction-only, устанавливается за 15 мин.
6. **Ценовые базы 2024-2026 РФ** — региональные коэффициенты из ФСНБ, не только moscow/spb generic factor. --- *verified: afrexai-construction-estimator и open-construction-estimate — прямой скрейп clawhub.ai 2026-04-20.* *Конкурент 3 — 🟡 гипотеза: прямых RU-сметных скиллов на ClawHub не найдено.*
