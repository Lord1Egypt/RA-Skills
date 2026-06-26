# eBay Listing Template Generator

## Sports Card Listing Template

```markdown
🔥 **INVESTMENT GRADE** {YEAR} {BRAND} {PLAYER} {CARD_TYPE} {GRADE}

## Key Details
• **Condition**: {GRADE} ({POPULATION_INFO})
• **Player**: {PLAYER} - {TEAM} {ACHIEVEMENTS}
• **Card**: {YEAR} {BRAND} {SET} #{CARD_NUMBER}
• **Authenticity**: {GRADING_SERVICE} Certified & Encapsulated

## Investment Highlights
✅ **{INVESTMENT_REASON}**: {INVESTMENT_DETAILS}
✅ **{RARITY_FACTOR}**: {RARITY_DETAILS}
✅ **{CONDITION_HIGHLIGHT}**: {CONDITION_DETAILS}
✅ **{MARKET_TIMING}**: {TIMING_DETAILS}

## Technical Specifications
- **Year**: {YEAR}
- **Brand**: {BRAND}
- **Set**: {SET}
- **Card Number**: #{CARD_NUMBER}
- **Parallel**: {PARALLEL_TYPE}
- **Grading Service**: {GRADING_SERVICE}
- **Grade**: {GRADE}
- **Cert Number**: {CERT_NUMBER}

## Why This Card Matters
{PLAYER_NARRATIVE}

## Shipping & Handling
🚚 **Same-Day Shipping** (orders by 2 PM EST)
📦 **Premium Packaging**: Team bags, toploaders, bubble mailers
🔒 **Insurance Included** on all orders $100+
📍 **Tracking Provided** for all shipments

## Seller Credentials
⭐ **99.8% Positive Feedback** ({FEEDBACK_COUNT}+ transactions)
🏆 **Top Rated Seller** with eBay Premium Service
🎯 **Card Specialist** - {YEARS_EXPERIENCE}+ years in the industry
🔍 **Authentication Guarantee** - 30-day return policy

{PAYMENT_TERMS}
{RETURN_POLICY}
{INTERNATIONAL_SHIPPING}
```

## Pokemon Card Listing Template

```markdown
✨ **MINT CONDITION** {YEAR} Pokemon {SET} {POKEMON_NAME} #{CARD_NUMBER} {GRADE}

## Card Overview
• **Pokemon**: {POKEMON_NAME} ({POKEMON_TYPE})
• **Set**: {YEAR} {SET}
• **Card Number**: #{CARD_NUMBER}/{TOTAL_IN_SET}
• **Rarity**: {RARITY_SYMBOL} {RARITY_NAME}
• **Condition**: {GRADE} - {GRADING_SERVICE}

## Special Features
🌟 **{SPECIAL_FEATURE_1}**: {FEATURE_DESCRIPTION_1}
🌟 **{SPECIAL_FEATURE_2}**: {FEATURE_DESCRIPTION_2}
🌟 **{SPECIAL_FEATURE_3}**: {FEATURE_DESCRIPTION_3}

## Card Details
- **HP**: {HP_VALUE}
- **Attacks**: {ATTACK_NAMES}
- **Weakness**: {WEAKNESS}
- **Resistance**: {RESISTANCE}
- **Retreat Cost**: {RETREAT_COST}

## Collector Information
📊 **Population**: {POPULATION_COUNT} graded at this level
💎 **Market Trend**: {PRICE_TREND} over last 90 days
🎯 **Estimated Value**: ${LOW_ESTIMATE} - ${HIGH_ESTIMATE}

{STANDARD_SHIPPING_TERMS}
```

## Vintage Card Listing Template

```markdown
🏛️ **VINTAGE TREASURE** {YEAR} {BRAND} {PLAYER} #{CARD_NUMBER} {CONDITION}

## Historical Significance
This {YEAR} {BRAND} {PLAYER} represents {HISTORICAL_CONTEXT}

## Condition Assessment
📋 **Overall Grade**: {CONDITION_ASSESSMENT}
🔍 **Corners**: {CORNER_CONDITION}
🔍 **Edges**: {EDGE_CONDITION}  
🔍 **Surface**: {SURFACE_CONDITION}
🔍 **Centering**: {CENTERING_ASSESSMENT}

## Vintage Card Details
- **Era**: {ERA_CLASSIFICATION}
- **Manufacturer**: {MANUFACTURER}
- **Set**: {SET_NAME}
- **Card Number**: #{CARD_NUMBER}
- **Print Run**: {PRINT_RUN_INFO}
- **Variations**: {KNOWN_VARIATIONS}

## Market Context
📈 **Recent Sales**: ${RECENT_SALE_RANGE}
📊 **Available Supply**: {SUPPLY_ASSESSMENT}
🎯 **Collector Demand**: {DEMAND_LEVEL}

## Authenticity Guarantee
✅ Examined by vintage card specialist
✅ Period-appropriate printing and materials verified
✅ 30-day authenticity guarantee
✅ Detailed condition photos provided

{VINTAGE_SHIPPING_TERMS}
```

## Template Variables Reference

### Player Information
- `{PLAYER}` - Full player name
- `{TEAM}` - Current or primary team
- `{ACHIEVEMENTS}` - Notable achievements (All-Star, MVP, etc.)
- `{PLAYER_NARRATIVE}` - Story about player's significance

### Card Specifications  
- `{YEAR}` - Card year
- `{BRAND}` - Card manufacturer
- `{SET}` - Set name
- `{CARD_NUMBER}` - Card number
- `{PARALLEL_TYPE}` - Parallel designation if applicable
- `{CARD_TYPE}` - Base, rookie, insert, etc.

### Condition & Grading
- `{GRADE}` - PSA/BGS grade
- `{GRADING_SERVICE}` - PSA, BGS, SGC
- `{CERT_NUMBER}` - Certification number
- `{CONDITION}` - Raw condition if ungraded
- `{POPULATION_INFO}` - Population count details

### Market Data
- `{POPULATION_COUNT}` - Cards graded at this level
- `{PRICE_TREND}` - Recent price movement
- `{LOW_ESTIMATE}` - Conservative value estimate
- `{HIGH_ESTIMATE}` - Optimistic value estimate
- `{RECENT_SALE_RANGE}` - Recent comparable sales

### Investment Context
- `{INVESTMENT_REASON}` - Why it's a good investment
- `{INVESTMENT_DETAILS}` - Supporting details
- `{RARITY_FACTOR}` - What makes it rare
- `{RARITY_DETAILS}` - Specific rarity information
- `{MARKET_TIMING}` - Current market conditions

### Seller Information
- `{FEEDBACK_COUNT}` - Number of positive feedbacks
- `{YEARS_EXPERIENCE}` - Years selling cards
- `{SPECIALIZATION}` - Areas of expertise

### Standard Terms
- `{PAYMENT_TERMS}` - Accepted payment methods
- `{RETURN_POLICY}` - Return and refund policy
- `{INTERNATIONAL_SHIPPING}` - International shipping options
- `{STANDARD_SHIPPING_TERMS}` - Shipping and handling details

## Usage Examples

### Generate Sports Card Listing
```python
template_vars = {
    'YEAR': 2023,
    'BRAND': 'Topps Chrome',
    'PLAYER': 'Ja Morant',
    'TEAM': 'Memphis Grizzlies',
    'CARD_NUMBER': '15',
    'GRADE': 'PSA 9',
    'GRADING_SERVICE': 'PSA',
    'POPULATION_INFO': 'Population: 1,247',
    'ACHIEVEMENTS': '2x All-Star, MIP Winner',
    'INVESTMENT_REASON': 'Rising Star',
    'INVESTMENT_DETAILS': '2x All-Star, MIP Winner, Playoff Performer'
}

listing = generate_listing_from_template('sports', template_vars)
```

### Generate Pokemon Card Listing
```python
template_vars = {
    'YEAR': 1998,
    'SET': 'Base Set',
    'POKEMON_NAME': 'Charizard',
    'CARD_NUMBER': '4',
    'TOTAL_IN_SET': '102',
    'GRADE': 'PSA 10',
    'GRADING_SERVICE': 'PSA',
    'HP_VALUE': '120',
    'RARITY_SYMBOL': '★',
    'RARITY_NAME': 'Rare Holo'
}

listing = generate_listing_from_template('pokemon', template_vars)
```