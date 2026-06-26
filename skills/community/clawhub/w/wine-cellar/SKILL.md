---
name: wine-cellar
description: Comprehensive wine cellar management skill for tracking inventory, providing meal-based recommendations, acting as a virtual sommelier, tracking consumption/purchases, and supporting barcode lookup to retrieve bottle details. Use when you need to manage a personal wine collection, get wine pairing suggestions for meals, scan barcodes for wine information, or maintain detailed records of your wine inventory.
---

# Wine Cellar

## Overview

This skill enables comprehensive management of a personal wine cellar, including inventory tracking, barcode-based bottle lookup, meal-based wine recommendations, sommelier-style advice, and consumption/purchase tracking. It provides both data management capabilities and intelligent wine expertise.

## Core Capabilities

### 1. Inventory Management
Track your wine collection with detailed records including:
- Bottle details (producer, varietal, vintage, region)
- Storage location within your cellar
- Acquisition date and price
- Current quantity and drinking window
- Tasting notes and ratings

### 2. Barcode Lookup
Input barcode numbers to automatically retrieve:
- Wine producer and name
- Vintage and varietal information
- Region and appellation details
- Typical price range and availability
- Wine critic scores when available

### 3. Meal-Based Recommendations
Get intelligent wine pairing suggestions based on:
- Specific dishes or cuisines
- Flavor profiles and ingredients
- Cooking methods and preparation styles
- Course progression (appetizer, main, dessert)

### 4. Virtual Sommelier
Receive expert advice on:
- Wine characteristics and tasting notes
- Optimal drinking windows and aging potential
- Decanting and serving temperature recommendations
- Glassware suggestions
- Similar wine alternatives

### 5. Consumption & Purchase Tracking
Maintain detailed logs of:
- Consumption events (when, with whom, occasion)
- Purchase history and pricing trends
- Inventory valuation and cellar management
- Drinking patterns and preferences

## Getting Started

To begin using this skill, you can:
1. Add wines to your inventory manually or via barcode scan
2. Organize your collection by storage location or categories
3. Request meal-based wine pairings for specific dishes
4. Look up detailed information about any wine in your collection
5. Track consumption events and purchase history

## Data Structure

The wine cellar skill uses the following data models:

### Wine Bottle
- **id**: Unique identifier
- **producer**: Wine producer/winery name
- **name**: Wine label name
- **varietal**: Grape variety or blend
- **vintage**: Year of production
- **region**: Geographic origin
- **appellation**: Specific designated area
- **quantity**: Number of bottles in inventory
- **location**: Storage location (bin, shelf, etc.)
- **acquired_date**: When purchased/acquired
- **price_paid**: Purchase price per bottle
- **current_value**: Estimated current market value
- **drinking_window**: Optimal years for consumption
- **tasting_notes**: Personal tasting impressions
- **rating**: Personal score (typically 0-100)
- **barcode**: UPC/EAN code for scanning

### Consumption Event
- **id**: Unique identifier
- **wine_id**: Reference to consumed bottle
- **date**: Consumption date
- **occasion**: Event or meal context
- **with_whom**: People present
- **rating**: Experience score
- **notes**: Additional comments

### Purchase Record
- **id**: Unique identifier
- **wine_id**: Reference to purchased bottle
- **date**: Purchase date
- **quantity**: Number of bottles purchased
- **price_per_unit**: Cost per bottle
- **total_cost**: Total purchase amount
- **source**: Retailer, winery, or private seller
- **notes**: Purchase details

## Usage Examples

### Adding Wine to Inventory
"I just bought a 2018 Chateau Margaux and want to add it to my cellar. It's barcode 123456789012."

### Barcode Lookup
"Scan this barcode: 085000014315 to get wine details."

### Meal-Based Recommendation
"What wine would pair well with mushroom risotto?"

### Sommelier Advice
"How long should I decant a young Bordeaux before serving?"

### Tracking Consumption
"I opened a bottle of 2016 Domaine de la Romanée-Conti last night with dinner and want to log it."

## Storage & Persistence

This skill maintains data in JSON format within the skill directory:
- `data/wine_inventory.json` - Main wine collection
- `data/consumption_log.json` - Drinking history
- `data/purchase_history.json` - Acquisition records
- `data/barcode_cache.json` - Lookup results for performance

## Extending Functionality

To add custom fields or adapt to specific needs:
1. Modify the data models in the scripts/
2. Update validation and storage logic
3. Extend the recommendation engine with personal preferences
4. Add integration with external wine databases or APIs

## Best Practices

- Regularly backup your wine cellar data
- Update drinking windows based on expert advice and personal experience
- Use consistent naming conventions for producers and regions
- Take tasting notes immediately after opening for accuracy
- Review your collection periodically for optimal drinking windows

## Resources

### scripts/
Executable tools for wine cellar operations:
- `add_wine.py` - Add new bottles to inventory
- `lookup_barcode.py` - Retrieve wine details from barcode
- `recommend_pairing.py` - Get meal-based wine suggestions
- `log_consumption.py` - Record drinking events
- `generate_report.py` - Create inventory and valuation reports
- `utils.py` - Shared helper functions

### references/
Reference materials for wine knowledge:
- `wine_regions.md` - Major wine growing regions and characteristics
- `varietal_guide.md` - Grape varietal profiles and traits
- `pairing_principles.md` - Food and wine matching guidelines
- `vintage_chart.md` - Historical vintage quality references
- `serving_guide.md` - Temperature, decanting, and glassware advice

### assets/
Templates and reference materials:
- `wine_label_template.pdf` - Printable label format for bin tags
- `cellar_map_template.svg` - Diagram for mapping physical storage
- `tasting_sheet.pdf` - Structured tasting note template

--- 
