---
name: Restaurant-Food Service AI
slug: restaurant-food-service
description: All-in-one restaurant operations skill. Menu engineering with profitability analysis, food cost optimization, allergen/nutrition labeling, inventory management with spoilage prediction, recipe scaling, health code compliance, and customer sentiment analytics.
version: 1.0.0
author: ai-gaoqian
tags:
  - restaurant
  - food-service
  - menu-engineering
  - food-cost
  - hospitality
  - recipe-management
  - compliance
metadata:
  openclaw:
    requires: openclaw>=1.0.0
---

# Restaurant-Food Service AI

## Overview
Comprehensive AI skill for restaurant owners, chefs, and food service operators. Covers menu engineering using Kasavana-Smith matrix analysis, ingredient-level food cost optimization, automated allergen and nutrition labeling, intelligent inventory management with spoilage date prediction, recipe scaling across batch sizes, health code compliance checklists, and customer review sentiment aggregation from major platforms.

## Use Cases
- Classify menu items as Stars/Plowhorses/Puzzles/Dogs using contribution margin analysis
- Calculate plate cost from ingredient prices and suggest substitutions to hit target margins
- Generate FDA-compliant nutrition facts panels from recipe data
- Flag allergen cross-contamination risks in shared kitchen environments
- Predict spoilage dates for fresh ingredients based on storage conditions
- Scale recipes from 4 portions to 400 with automatic unit conversions
- Generate health department inspection prep checklists per local jurisdiction
- Aggregate and analyze Google Maps/Yelp/TripAdvisor/Dianping reviews

## Execution Flow
1. Accept input: recipe list with ingredients / menu with prices and sales data / inventory list / inspection jurisdiction
2. Route to appropriate module: menu analysis, cost optimization, compliance labeling, or review analytics
3. Perform calculations using food science databases and industry-standard formulas
4. Output actionable recommendations ranked by impact on profitability and safety

## Output Format
- Menu matrix (Stars/Plowhorses/Puzzles/Dogs quadrant with action recommendations)
- Cost card per dish (ingredient breakdown, plate cost, margin %, suggested price)
- Nutrition label (per FDA/CFIA/EFSA format with allergens highlighted)
- Inventory dashboard (stock levels, spoilage alerts, reorder suggestions)
- Health inspection checklist (by jurisdiction, with critical violation flags)
- Review sentiment report (rating trend, top praised dishes, top complaint themes)

## Food Safety Standards
- FDA Food Code (US)
- HACCP principles
- EU Regulation 1169/2011 (FIC)
- CFIA Safe Food for Canadians Regulations
- China GB 28050 nutrition labeling
- Allergen labeling: Big 9 (US) / Big 14 (EU)

## Menu Engineering Methodology
Based on Kasavana & Smith (1982) matrix:
- **Stars**: High popularity + high margin → Promote aggressively
- **Plowhorses**: High popularity + low margin → Reprice or reformulate
- **Puzzles**: Low popularity + high margin → Reposition or nudge
- **Dogs**: Low popularity + low margin → Replace or remove

## Review Platform Coverage
Google Maps, Yelp, TripAdvisor, Zomato, Dianping (大众点评), Meituan, OpenTable, TheFork

## Notes
- Ingredient price database covers 5000+ items updated weekly
- Nutrition data from USDA SR28, CIQUAL, China Food Composition tables
- Health code templates for 30+ major city health departments
- Spoilage models account for temperature, humidity, and packaging type
- Recipe conversion handles metric/US/British imperial units
