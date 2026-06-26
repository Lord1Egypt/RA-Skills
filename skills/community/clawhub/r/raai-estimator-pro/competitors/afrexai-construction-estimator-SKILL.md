# afrexai-construction-estimator — ClawHub SKILL.md (скачано с clawhub.ai) **Источник:** https://clawhub.ai/1kalin/afrexai-construction-estimator **Автор:** @1kalin (AfrexAI) **Версия:** v1.0.0 **Загрузок:** 929 | **Звёзды:** 2 **Статус безопасности:** Benign high confidence **Цена:** бесплатно --- ## Описание Complete construction estimating and cost management system — from quantity takeoff to bid submission. Zero dependencies. Instruction-only methodology. ## Архитектура (12 фаз) 1. Project Classification & Estimate Type — Estimate Type Matrix (5 типов) + Project Brief YAML + Project Type Quick Reference ($80-900/SF бенчмарки)
2. Quantity Takeoff (QTO) — CSI MasterFormat 2018 (24 дивизии) + Waste Factors по материалам + QTO Line Item Template + Cross-checks
3. Pricing & Cost Assembly — Unit Cost Hierarchy (Sub quotes → Historical → RSMeans → Vendor → Published) + Labor Rate Build-Up + Sub Quote Scoring Matrix + Crew Rate Assembly
4. Indirect Costs & Markups — Division 01 Checklist (18 позиций) + Markup Stack YAML + Contingency Guide
5. Bid Preparation & Strategy — Bid/No-Bid Scorecard (9 факторов) + Bid Day Checklist + Competitive Bid Strategy
6. Value Engineering (VE) — VE Opportunity Matrix (8 систем) + VE Proposal Template + VE Decision Rules
7. Change Order Management — CO Pricing Rules (Owner/Sub markup tiers) + T&M documentation + CO YAML Template + Negotiation Tips
8. Cost Control During Construction — Earned Value Management (BAC/PV/EV/AC/SPI/CPI) + Monthly Cost Report + Red Flags
9. Specialty Estimates — Renovation/Remodel factors + Sitework YAML checklist + MEP Quick Checks
10. Escalation & Location Adjustments — Escalation Formula + RSMeans City Cost Indices (20 городов)
11. Estimate Quality Review — 100-Point Quality Rubric (8 измерений) + Peer Review Checklist
12. Common Mistakes & Edge Cases — 10 типовых ошибок + Edge cases (occupied/remote/fast-track/public/D-B) ## Ключевые фичи **Estimate Type Matrix:**
- Order of Magnitude (-30/+50%) → Conceptual (-15/+30%) → Detailed (-10/+15%) → Definitive (-5/+10%) → Control **Project Brief YAML:** полная структура с project/scope/schedule/estimate/assumptions/exclusions **CSI MasterFormat Division Structure:** 24 дивизии с типичными % от общего объёма **Sub Quote Scoring Matrix (5 факторов):**
Price(30%) / Scope(25%) / Qualifications(20%) / Past Performance(15%) / Bond/Insurance(10%) **Earned Value Management:** SPI = EV/PV, CPI = EV/AC, EAC = BAC/CPI, VAC = BAC-EAC **100-Point Estimate Quality Rubric:**
Scope(20) + Quantities(20) + Pricing basis(15) + Indirect(10) + Markup(10) + Documentation(10) + Adjustments(10) + Presentation(5) **RSMeans Location Factors:** 20 US городов (NY: 130-145, SF: 125-140, Rural: 70-85) ## Триггерные команды (12 штук) "Estimate this project" / "Price [division/trade]" / "Check my quantities" / "Value engineer [system]" / "Write change order for [scope]" / "Compare sub quotes for [trade]" / "Monthly cost report" / "Bid/no-bid analysis for [project]" / "Location adjust to [city]" / "Escalate costs to [date]" / "Review my estimate" / "Generate bid summary" ## Ограничения - Только методология и шаблоны — нет code/автоматизации
- Все бенчмарки в US долларах и RSMeans City Indices (Россия не покрыта)
- Нормативная база CSI/MASTERFORMAT — не ГЭСН/ФЕР/ТЕР РФ
- Нет поддержки российского порядка ценообразования (ПК-сметы, ЭСС, ФЕРы)
- RSMeans — платный сервис, потребуются отдельные данные
