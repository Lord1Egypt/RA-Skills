# open-construction-estimate — ClawHub SKILL.md (скачано с clawhub.ai) **Источник:** https://clawhub.ai/datadrivenconstruction/open-construction-estimate **Автор:** @datadrivenconstruction (Data Driven Construction) **Версия:** v2.0.0 **Загрузок:** 1 700 | **Звёзды:** 2 **Статус безопасности:** Benign (medium confidence) — требует network/filesystem доступ для ML-моделей **Цена:** бесплатно **Сайт:** https://datadrivenconstruction.io --- ## Описание Access and utilize open construction pricing databases for automated cost estimation. Match BIM elements to standardized work items using ML (TF-IDF + sentence-transformers), calculate costs using public unit price databases with 55,000+ work items. ## Архитектура **Core Components:** 1. **WorkItemMatcher** — семантический поиск по базе 55k+ позиций - TF-IDF (fast initial filtering) + Sentence Transformers (semantic matching) - Model: `all-MiniLM-L6-v2` (загружается с HuggingFace при первом запуске) - BIM element → work item mapping (IfcWall/IfcSlab/IfcColumn/IfcBeam/IfcDoor...) 2. **OpenConstructionEstimator** — расчёт стоимости с региональными коэффициентами - Regional factors: northeast_us(1.15) / west_us(1.08) / moscow(1.20) / spb(1.10) / regions_ru(0.85) - Export в Excel через pandas/openpyxl 3. **OpenDatabaseManager** — управление базой расценок - CSV-хранилище с CSI MasterFormat структурой - Inflation adjustment + version tracking ## Ключевые фичи **База данных (55,000+ work items):**
- OpenConstructionEstimate (open source)
- RSMeans Online (subscription required)
- Government pricing databases
- Regional cost indexes **Database Schema:**
code / description / unit / unit_price / labor_cost / material_cost / equipment_cost / labor_hours / crew_size / productivity / category_l1-l3 / region / year / source **BIM Integration:**
- Прямое сопоставление IFC-элементов с позициями
- Автоматический расчёт по количествам из BIM **Regional Factors:**
Включены коэффициенты для moscow(1.20), spb(1.10), regions_ru(0.85) — единственный конкурент с поддержкой российских регионов ## Зависимости (runtime) ```
pandas, sklearn (TF-IDF/cosine_similarity)
sentence-transformers (all-MiniLM-L6-v2 — загрузка с HuggingFace ~80MB)
openpyxl (Excel export)
``` **Флаги безопасности:**
- Network access: для загрузки ML-модели с HuggingFace
- Filesystem access: чтение CSV баз, запись Excel
- RSMeans требует платную подписку для полного использования
- Hardcoded paths ожидаются в production (не generic) ## Триггерные команды Нет фиксированных триггеров — работает через Python API/CLI. Требует настройки dev-окружения. ## Ограничения - **Требует Python + ML** — не instruction-only, нужна техническая настройка
- База открытая — не официальная ГЭСН/ФЕР (только коэффициент для РФ регионов)
- RSMeans = платный сервис для актуальных цен
- Первый запуск скачивает ~80MB sentence-transformer модели
- Нет готовых шаблонов смет в формате РФ (КС-2, КС-3)
- Нет методологии работы с субподрядчиками и согласования цен
