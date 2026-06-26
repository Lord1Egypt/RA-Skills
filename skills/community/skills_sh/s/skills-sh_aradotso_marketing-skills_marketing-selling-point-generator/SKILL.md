---
name: marketing-selling-point-generator
description: AI-powered tool to discover, prioritize, and write compelling product selling points for marketing campaigns
triggers:
  - generate product selling points
  - analyze product value proposition
  - create marketing copy from features
  - find product differentiators
  - write compelling product descriptions
  - refine product messaging strategy
  - extract selling points from product info
  - optimize product positioning copy
---

# Marketing Selling Point Generator

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

## Overview

Marketing Selling Point Generator is a comprehensive tool designed to help product managers and marketers transform product features into compelling selling points. It uses a three-phase approach: **Find** (discover selling points), **Define** (prioritize them), and **Write** (create persuasive copy).

The tool analyzes product attributes, competitive positioning, user feedback, and pain points to generate targeted marketing copy optimized for different platforms and audiences.

## Installation

```bash
# Clone the repository
git clone https://github.com/danidai098-arch/marketing-selling-point-generator.git
cd marketing-selling-point-generator

# Install dependencies (assuming Node.js/Python based on typical structure)
npm install
# or
pip install -r requirements.txt
```

## Core Workflow

### 1. Find Selling Points (找卖点)

Extract potential selling points from various data sources:

```javascript
const { SellingPointFinder } = require('./src/finder');

const finder = new SellingPointFinder();

// Analyze product attributes
const productData = {
  name: "Smart Wireless Earbuds Pro",
  features: [
    "Active Noise Cancellation",
    "40-hour battery life",
    "IPX7 waterproof",
    "Bluetooth 5.3"
  ],
  price: 99.99,
  category: "Audio"
};

const attributePoints = await finder.analyzeAttributes(productData);
// Returns structured selling points based on features
```

```python
# Python equivalent
from src.finder import SellingPointFinder

finder = SellingPointFinder()

product_data = {
    "name": "Smart Wireless Earbuds Pro",
    "features": [
        "Active Noise Cancellation",
        "40-hour battery life",
        "IPX7 waterproof",
        "Bluetooth 5.3"
    ],
    "price": 99.99,
    "category": "Audio"
}

attribute_points = finder.analyze_attributes(product_data)
```

#### Competitive Analysis

```javascript
// Compare with competitors
const competitorData = [
  { name: "Brand X Earbuds", price: 129.99, battery: "30 hours" },
  { name: "Brand Y Pods", price: 89.99, battery: "24 hours" }
];

const competitivePoints = await finder.compareCompetitors(
  productData,
  competitorData
);
// Returns: differentiation advantages like "33% longer battery vs competitors"
```

#### User Feedback Analysis

```javascript
const reviews = [
  "Amazing battery life, lasts all week!",
  "Sound quality is incredible for the price",
  "Finally earbuds that survive my workouts"
];

const userInsights = await finder.analyzeReviews(reviews);
// Extracts: key value points users actually care about
```

#### Pain Point Mapping

```javascript
const targetAudience = {
  segment: "fitness enthusiasts",
  painPoints: [
    "Earbuds fall out during exercise",
    "Battery dies mid-workout",
    "Not sweat-resistant"
  ]
};

const painPointMap = await finder.mapPainPoints(productData, targetAudience);
// Maps product features to solved pain points
```

### 2. Define Selling Points (定卖点)

Prioritize and score discovered selling points:

```javascript
const { SellingPointRanker } = require('./src/ranker');

const ranker = new SellingPointRanker();

const allPoints = [
  ...attributePoints,
  ...competitivePoints,
  ...userInsights,
  ...painPointMap
];

// Score by differentiation
const scoredPoints = await ranker.scoreDifferentiation(allPoints);
// Returns points sorted by competitive advantage strength

// Match to target audience
const audienceConfig = {
  demographic: "25-35, fitness-focused professionals",
  values: ["performance", "durability", "convenience"],
  channels: ["Instagram", "fitness forums"]
};

const audienceMatched = await ranker.matchAudience(scoredPoints, audienceConfig);

// Evaluate by scenario
const scenarios = ["gym workout", "daily commute", "work calls"];
const scenarioScores = await ranker.evaluateScenarios(audienceMatched, scenarios);

// Predict viral potential
const viralityScores = await ranker.predictVirality(scenarioScores);
```

```python
# Python equivalent
from src.ranker import SellingPointRanker

ranker = SellingPointRanker()

scored_points = ranker.score_differentiation(all_points)
audience_matched = ranker.match_audience(scored_points, audience_config)
scenario_scores = ranker.evaluate_scenarios(audience_matched, scenarios)
virality_scores = ranker.predict_virality(scenario_scores)
```

### 3. Write Selling Points (写卖点)

Generate platform-optimized copy:

```javascript
const { CopyWriter } = require('./src/writer');

const writer = new CopyWriter();

const topPoints = viralityScores.slice(0, 5);

// FAB (Features-Advantages-Benefits) transformation
const fabCopy = await writer.transformFAB(topPoints[0]);
// Input: "40-hour battery life"
// Output: {
//   feature: "40-hour battery life",
//   advantage: "5x longer than typical earbuds",
//   benefit: "Charge once a week, not every day"
// }

// Emotion hook design
const emotionHooks = await writer.createEmotionHooks(topPoints, {
  emotions: ["relief", "excitement", "confidence"]
});
// Returns: "Never ask 'Are my earbuds charged?' again"

// Platform-specific copy
const platformCopy = await writer.adaptToPlatform(topPoints, {
  platform: "ecommerce",
  maxLength: 150,
  includeCTA: true
});

// E-commerce example
console.log(platformCopy.ecommerce);
// "40-hour battery. IPX7 waterproof. Premium sound at half the price. 
//  Your all-day, every-workout companion. Shop Now →"

// Social media version
const socialCopy = await writer.adaptToPlatform(topPoints, {
  platform: "instagram",
  style: "casual",
  includeEmoji: true
});

console.log(socialCopy.instagram);
// "Charge once. Play all week. 🔋💪 
//  40 hours of battery = zero anxiety. #NeverDie"
```

#### A/B Testing Variants

```javascript
const abVariants = await writer.generateABVariants(topPoints[0], {
  count: 3,
  variables: ["headline", "cta", "emotional_angle"]
});

console.log(abVariants);
// [
//   { headline: "Battery that lasts as long as you do", cta: "Shop Now" },
//   { headline: "40 hours of pure freedom", cta: "Get Yours" },
//   { headline: "Never cut your workout short again", cta: "Try It" }
// ]
```

## Configuration

Create a `config.json` file:

```json
{
  "platform": "ecommerce",
  "style": "professional",
  "max_points": 5,
  "include_emotion_hook": true,
  "include_cta": true,
  "target_audience": {
    "age_range": "25-45",
    "interests": ["fitness", "technology"],
    "pain_points": ["battery anxiety", "durability concerns"]
  },
  "brand_voice": {
    "tone": "confident but approachable",
    "avoid": ["technical jargon", "hype"],
    "emphasize": ["reliability", "value"]
  },
  "output_formats": ["short_bullet", "long_description", "social_caption"]
}
```

Load configuration:

```javascript
const { loadConfig } = require('./src/config');

const config = loadConfig('./config.json');
const writer = new CopyWriter(config);
```

## Complete Example Workflow

```javascript
const { 
  SellingPointFinder, 
  SellingPointRanker, 
  CopyWriter 
} = require('./src');

async function generateMarketingCopy(productData, competitorData, reviews) {
  // Phase 1: Find
  const finder = new SellingPointFinder();
  const attributePoints = await finder.analyzeAttributes(productData);
  const competitivePoints = await finder.compareCompetitors(
    productData, 
    competitorData
  );
  const userPoints = await finder.analyzeReviews(reviews);
  
  // Phase 2: Define
  const ranker = new SellingPointRanker();
  const allPoints = [...attributePoints, ...competitivePoints, ...userPoints];
  const scoredPoints = await ranker.scoreDifferentiation(allPoints);
  const topPoints = scoredPoints.slice(0, 5);
  
  // Phase 3: Write
  const writer = new CopyWriter({
    platform: 'ecommerce',
    style: 'professional',
    include_cta: true
  });
  
  const marketingCopy = {
    mainHeadline: await writer.createEmotionHooks([topPoints[0]]),
    bulletPoints: await Promise.all(
      topPoints.map(p => writer.transformFAB(p))
    ),
    platformCopy: await writer.adaptToPlatform(topPoints, {
      platform: 'ecommerce',
      maxLength: 200
    }),
    abVariants: await writer.generateABVariants(topPoints[0], { count: 3 })
  };
  
  return marketingCopy;
}

// Usage
const result = await generateMarketingCopy(
  productData,
  competitorData,
  reviews
);

console.log(result);
```

## Common Patterns

### Pattern 1: Quick Product Description

```javascript
const { quickGenerate } = require('./src/quick');

const description = await quickGenerate({
  productName: "Smart Wireless Earbuds Pro",
  keyFeatures: ["40h battery", "ANC", "IPX7"],
  targetPlatform: "amazon"
});

// Returns optimized Amazon listing copy
```

### Pattern 2: Multi-Platform Campaign

```javascript
const platforms = ['ecommerce', 'instagram', 'facebook_ad', 'google_ad'];

const campaign = await Promise.all(
  platforms.map(platform => 
    writer.adaptToPlatform(topPoints, { 
      platform, 
      style: 'casual' 
    })
  )
);

const campaignPack = Object.fromEntries(
  platforms.map((p, i) => [p, campaign[i]])
);
```

### Pattern 3: Competitive Positioning

```javascript
const positioning = await finder.generatePositioningStatement({
  product: productData,
  competitors: competitorData,
  targetAudience: "fitness enthusiasts",
  keyDifferentiator: "battery life"
});

// Returns: "For fitness enthusiasts who need reliable audio, 
//  Smart Earbuds Pro offers 40-hour battery life—33% longer 
//  than leading competitors—so you never miss a beat."
```

## Environment Variables

```bash
# .env file
OPENAI_API_KEY=your_openai_key_here
ANALYSIS_MODEL=gpt-4
COPY_MODEL=gpt-3.5-turbo
MAX_TOKENS=500
TEMPERATURE=0.7
```

Load in code:

```javascript
require('dotenv').config();

const writer = new CopyWriter({
  apiKey: process.env.OPENAI_API_KEY,
  model: process.env.COPY_MODEL,
  temperature: parseFloat(process.env.TEMPERATURE)
});
```

## Troubleshooting

### Issue: Generated copy too generic

**Solution**: Provide more specific product data and competitive context

```javascript
// ❌ Too generic
const productData = { name: "Earbuds", features: ["wireless"] };

// ✅ Specific
const productData = {
  name: "Smart Wireless Earbuds Pro",
  features: [
    { name: "ANC", spec: "35dB reduction", userBenefit: "blocks gym noise" },
    { name: "Battery", spec: "40 hours", userBenefit: "weekly charging" }
  ],
  targetScenarios: ["gym", "commute", "work calls"]
};
```

### Issue: Points don't match target audience

**Solution**: Define detailed audience configuration

```javascript
const audienceConfig = {
  demographic: "25-35, urban professionals",
  psychographic: "values efficiency and quality",
  painPoints: ["battery anxiety", "poor call quality"],
  desiredOutcomes: ["all-day reliability", "professional sound"],
  influencers: ["tech reviewers", "fitness influencers"]
};

const matched = await ranker.matchAudience(points, audienceConfig);
```

### Issue: Copy doesn't fit platform character limits

**Solution**: Use strict length constraints

```javascript
const twitterCopy = await writer.adaptToPlatform(points, {
  platform: 'twitter',
  maxLength: 280,
  enforceStrict: true, // Cuts off at limit
  priorityPoints: [points[0], points[1]] // Focus on top 2
});
```

### Issue: Need multilingual support

**Solution**: Specify target language in config

```javascript
const chineseCopy = await writer.adaptToPlatform(points, {
  platform: 'ecommerce',
  language: 'zh-CN',
  culturalContext: 'China market preferences'
});
```

## Advanced Usage

### Custom Scoring Weights

```javascript
const ranker = new SellingPointRanker({
  weights: {
    differentiation: 0.4,
    audienceMatch: 0.3,
    virality: 0.2,
    feasibility: 0.1
  }
});
```

### Batch Processing

```javascript
const products = [product1, product2, product3];

const batchResults = await Promise.all(
  products.map(p => generateMarketingCopy(p, competitors, reviews))
);
```

### Export to Marketing Tools

```javascript
const { exportToCSV, exportToJSON } = require('./src/export');

await exportToCSV(marketingCopy, './output/copy.csv');
await exportToJSON(campaignPack, './output/campaign.json');
```
