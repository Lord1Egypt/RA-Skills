---
name: marketingskills-ai-agent-collection
description: Marketing skills collection for AI agents - CRO, copywriting, SEO, analytics, and growth engineering
triggers:
  - "help me with marketing tasks using AI agent skills"
  - "install marketing skills for my AI agent"
  - "set up CRO and copywriting skills"
  - "add SEO and analytics capabilities to my agent"
  - "use the marketingskills collection"
  - "optimize my site with AI marketing skills"
  - "create a product marketing context document"
  - "run an SEO audit with agent skills"
---

# Marketing Skills for AI Agents

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

A collection of AI agent skills focused on marketing tasks including conversion optimization, copywriting, SEO, analytics, and growth engineering. Works with Claude Code, OpenAI Codex, Cursor, Windsurf, and any agent that supports the [Agent Skills spec](https://agentskills.io).

## What This Project Does

Marketing Skills provides 40+ specialized markdown-based skills that give AI coding agents expertise in marketing tasks. Each skill contains frameworks, workflows, and best practices for specific marketing disciplines:

- **SEO & Content**: seo-audit, ai-seo, site-architecture, programmatic-seo, schema, content-strategy, aso
- **CRO**: cro, signup, onboarding, popups, paywalls
- **Content & Copy**: copywriting, copy-editing, cold-email, emails, social, video, image
- **Paid & Measurement**: ads, ad-creative, ab-testing, analytics
- **Growth & Retention**: referrals, free-tools, churn-prevention, community-marketing, lead-magnets, co-marketing
- **Sales & GTM**: revops, sales-enablement, launch, pricing, competitors, competitor-profiling, directory-submissions
- **Strategy**: marketing-ideas, marketing-psychology, customer-research, product-marketing

Skills reference each other and build on shared context, with `product-marketing` as the foundation that all other skills check first.

## Installation

### Option 1: CLI Install (Recommended)

```bash
# Install all skills
npx skills coreyhaines31/marketingskills

# Install specific skills
npx skills coreyhaines31/marketingskills --skills seo-audit,copywriting,cro

# Install to custom directory
npx skills coreyhaines31/marketingskills --dir .ai/custom-skills
```

### Option 2: Manual Install

```bash
# Clone the repository
git clone https://github.com/coreyhaines31/marketingskills.git

# Copy skills to your project's .ai directory
cp -r marketingskills/skills .ai/
```

### Option 3: Git Submodule

```bash
# Add as submodule
git submodule add https://github.com/coreyhaines31/marketingskills.git .ai/marketingskills

# Update submodule
git submodule update --remote .ai/marketingskills
```

## Project Structure

```
marketingskills/
├── skills/                    # All skill markdown files
│   ├── product-marketing/     # Foundation skill (read by all others)
│   │   └── SKILL.md
│   ├── seo-audit/
│   │   └── SKILL.md
│   ├── copywriting/
│   │   └── SKILL.md
│   ├── cro/
│   │   └── SKILL.md
│   └── [40+ more skills]/
├── examples/                  # Example outputs and workflows
├── scripts/                   # Utility scripts
└── README.md
```

## Core Concepts

### Skills are Markdown Files

Each skill is a `.md` file with YAML frontmatter containing:

```yaml
---
name: skill-name-kebab-case
description: One-line description of what the skill does
triggers:
  - "when user says this"
  - "or mentions this"
---
```

### Skills Reference Each Other

Skills can reference and build upon each other:

```markdown
## Related Skills

- **product-marketing** — Always read first to understand product context
- **customer-research** — Use to gather insights before writing copy
- **ab-testing** — Use to test copy variations
```

### Product Marketing is the Foundation

Every marketing skill checks `product-marketing/SKILL.md` first to understand:

- Product name, description, and positioning
- Target audience and personas
- Value propositions and messaging
- Core features and benefits
- Brand voice and tone

## Usage Examples

### Creating a Product Marketing Context

```javascript
// Agent automatically uses product-marketing skill when you say:
// "Create a product marketing context document for my SaaS"

// The skill will prompt for:
// - Product name and tagline
// - Target audience and personas
// - Core value propositions
// - Key features and benefits
// - Competitors and differentiation
// - Brand voice and tone

// Output saved to: product-context.md or .ai/product-marketing.md
```

### Running an SEO Audit

```javascript
// Agent uses seo-audit skill when you say:
// "Audit my website's SEO"

// The skill will:
// 1. Check product-marketing context first
// 2. Analyze site structure and technical SEO
// 3. Review on-page optimization
// 4. Check content quality and targeting
// 5. Provide prioritized recommendations

// Example output structure:
const seoAuditReport = {
  technical: {
    siteSpeed: "analysis",
    mobileFriendly: "check",
    indexability: "status",
    structuredData: "validation"
  },
  onPage: {
    titleTags: "optimization",
    metaDescriptions: "review",
    headings: "hierarchy",
    internalLinking: "analysis"
  },
  content: {
    keywordTargeting: "gaps",
    contentQuality: "assessment",
    topicalAuthority: "score"
  },
  recommendations: [
    { priority: "high", task: "Fix crawl errors", impact: "Critical" },
    { priority: "medium", task: "Improve title tags", impact: "High" }
  ]
};
```

### Optimizing Conversion Rates

```javascript
// Agent uses cro skill when you say:
// "Help me improve conversions on my landing page"

// The skill applies CRO frameworks:
// 1. Reads product-marketing context
// 2. Analyzes current page structure
// 3. Applies conversion optimization principles
// 4. Suggests A/B test ideas

// Example CRO analysis
const croRecommendations = {
  headline: {
    current: "We help businesses grow",
    suggested: "Double your leads in 30 days",
    reasoning: "Specific outcome + timeframe"
  },
  cta: {
    current: "Sign up",
    suggested: "Start your free trial",
    reasoning: "Lower friction, clear value"
  },
  socialProof: {
    add: ["customer logos", "testimonials", "case study metrics"],
    placement: "above the fold"
  },
  experiments: [
    { test: "Hero headline variations", priority: "high" },
    { test: "CTA button copy", priority: "high" },
    { test: "Pricing display", priority: "medium" }
  ]
};
```

### Writing Marketing Copy

```javascript
// Agent uses copywriting skill when you say:
// "Write homepage copy for my product"

// The skill follows this workflow:
// 1. Read product-marketing context
// 2. Apply copywriting frameworks (AIDA, PAS, etc.)
// 3. Generate copy variations
// 4. Suggest improvements

// Example generated copy structure
const homepageCopy = {
  hero: {
    headline: "Turn Visitors Into Customers",
    subheadline: "AI-powered conversion optimization for modern SaaS",
    cta: "Start optimizing free"
  },
  valueProps: [
    {
      headline: "Know exactly what to test",
      body: "AI analyzes your traffic and suggests high-impact experiments"
    },
    {
      headline: "Ship tests in minutes, not days",
      body: "Visual editor makes A/B testing accessible to any team"
    }
  ],
  socialProof: {
    stat: "10,000+ companies trust us",
    testimonial: "We increased signups 47% in the first month"
  }
};
```

### Setting Up Analytics

```javascript
// Agent uses analytics skill when you say:
// "Set up Google Analytics 4 tracking"

// The skill provides implementation code
// Example: GA4 setup with custom events

// Install gtag
const setupGA4 = () => {
  // Add to <head>
  const gtagScript = `
    <script async src="https://www.googletagmanager.com/gtag/js?id=${process.env.GA4_MEASUREMENT_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', '${process.env.GA4_MEASUREMENT_ID}');
    </script>
  `;
};

// Track custom events
const trackConversion = (eventName, value) => {
  if (typeof gtag !== 'undefined') {
    gtag('event', eventName, {
      'event_category': 'conversion',
      'event_label': eventName,
      'value': value
    });
  }
};

// Example usage
trackConversion('trial_started', 1);
trackConversion('purchase_completed', 99);
```

### Creating Programmatic SEO Pages

```javascript
// Agent uses programmatic-seo skill when you say:
// "Create landing pages for all my competitors"

// Example: Generate competitor comparison pages
const generateCompetitorPages = async (competitors) => {
  // Read product context
  const product = await readProductContext();
  
  // Template for competitor pages
  const template = (competitor) => ({
    url: `/vs/${competitor.slug}`,
    title: `${product.name} vs ${competitor.name} - Comparison`,
    metaDescription: `Compare ${product.name} and ${competitor.name}. See features, pricing, and why teams choose ${product.name}.`,
    schema: {
      "@type": "ComparisonTable",
      items: [product, competitor]
    },
    sections: {
      hero: `${product.name} vs ${competitor.name}`,
      comparison: generateComparisonTable(product, competitor),
      whyChooseUs: generateDifferentiators(product, competitor),
      cta: `Try ${product.name} free`
    }
  });
  
  // Generate pages
  return competitors.map(competitor => ({
    path: `/vs/${competitor.slug}/index.html`,
    content: renderTemplate(template(competitor))
  }));
};
```

### Building an Email Sequence

```javascript
// Agent uses emails skill when you say:
// "Create an onboarding email sequence"

// Example: Trial onboarding sequence
const onboardingSequence = [
  {
    delay: 0,
    subject: "Welcome to {product_name}! Here's what to do first",
    preview: "Get started in 3 simple steps",
    body: `
      Hi {first_name},
      
      Welcome! Here's how to get the most value in your first week:
      
      1. Complete your profile (2 min)
      2. Import your data (5 min)
      3. Run your first campaign (10 min)
      
      [Get Started] → {onboarding_url}
    `
  },
  {
    delay: 2, // days
    subject: "Quick question about your {product_name} trial",
    condition: "not_activated",
    body: `
      Hi {first_name},
      
      I noticed you haven't {activation_milestone} yet.
      
      Is there anything blocking you? Hit reply and I'll personally help.
      
      Common issues we've solved:
      - Integration setup
      - Data import
      - Team training
      
      Want to jump on a quick call? [Book 15 min]
    `
  },
  {
    delay: 5,
    subject: "Your trial ends in 2 days",
    condition: "trial_ending",
    body: `
      Hi {first_name},
      
      Your trial ends in 2 days. Here's what you've achieved:
      
      ✓ {metric_1}
      ✓ {metric_2}
      ✓ {metric_3}
      
      Ready to keep going? [Choose your plan]
      
      Questions? Reply to this email.
    `
  }
];

// Implementation with variables
const sendEmail = (template, user) => {
  const variables = {
    product_name: process.env.PRODUCT_NAME,
    first_name: user.firstName,
    onboarding_url: `${process.env.APP_URL}/onboarding`,
    activation_milestone: "imported your first campaign",
    metric_1: user.metrics.campaigns,
    metric_2: user.metrics.conversions,
    metric_3: user.metrics.revenue
  };
  
  return replaceVariables(template.body, variables);
};
```

### Running A/B Tests

```javascript
// Agent uses ab-testing skill when you say:
// "Set up an A/B test for my pricing page"

// Example: Client-side A/B test implementation
const abTest = {
  name: "pricing_page_layout",
  variants: {
    control: { 
      layout: "traditional",
      weight: 0.5 
    },
    treatment: { 
      layout: "comparison_table",
      weight: 0.5 
    }
  },
  metrics: {
    primary: "trial_signups",
    secondary: ["page_views", "time_on_page", "scroll_depth"]
  }
};

// Assignment function
const assignVariant = (userId, testName) => {
  const hash = simpleHash(`${userId}-${testName}`);
  return hash % 100 < 50 ? 'control' : 'treatment';
};

// Track experiment exposure
const trackExperiment = (testName, variant) => {
  if (typeof gtag !== 'undefined') {
    gtag('event', 'experiment_view', {
      'experiment_name': testName,
      'variant': variant
    });
  }
};

// Track conversion
const trackConversion = (testName, variant, metric) => {
  if (typeof gtag !== 'undefined') {
    gtag('event', metric, {
      'experiment_name': testName,
      'variant': variant
    });
  }
};

// Usage
const variant = assignVariant(user.id, 'pricing_page_layout');
trackExperiment('pricing_page_layout', variant);

// On conversion
document.querySelector('.signup-button').addEventListener('click', () => {
  trackConversion('pricing_page_layout', variant, 'trial_signups');
});
```

## Configuration

### Environment Variables

Skills reference environment variables for configuration:

```bash
# Product context
PRODUCT_NAME="Your Product"
PRODUCT_URL="https://yourproduct.com"

# Analytics
GA4_MEASUREMENT_ID="G-XXXXXXXXXX"
GOOGLE_TAG_MANAGER_ID="GTM-XXXXXX"

# Marketing platforms
MAILCHIMP_API_KEY="your_api_key"
HUBSPOT_API_KEY="your_api_key"

# SEO tools
AHREFS_API_KEY="your_api_key"
SEMRUSH_API_KEY="your_api_key"
```

### Skill Directory Location

Skills can be installed in different locations:

```javascript
// Default: .ai/skills/
// Custom: .ai/custom-skills/
// Or any directory your agent checks

// Specify in your agent config
{
  "skillsDirectory": ".ai/marketingskills/skills"
}
```

## Common Patterns

### Sequential Skill Usage

Many marketing tasks use skills in sequence:

```javascript
// Pattern: Research → Strategy → Execution → Optimization
// 1. customer-research - gather insights
// 2. product-marketing - define positioning
// 3. copywriting - write messaging
// 4. cro - optimize conversion
// 5. ab-testing - validate improvements
```

### Cross-Referencing Skills

Skills often reference each other:

```javascript
// When writing copy, agent might also use:
// - customer-research (for voice of customer)
// - marketing-psychology (for persuasion principles)
// - ab-testing (for testing variations)
// - copy-editing (for refinement)
```

### Data-Driven Workflows

```javascript
// Pattern: Audit → Analyze → Recommend → Implement
// Example: SEO workflow

// 1. seo-audit - identify issues
const auditResults = await runSEOAudit(siteUrl);

// 2. Analyze findings
const prioritized = prioritizeIssues(auditResults);

// 3. ai-seo - optimize for AI search
const aiOptimizations = generateAISearchContent();

// 4. schema - add structured data
const schemaMarkup = generateSchemaMarkup();

// 5. analytics - track improvements
const tracking = setupSEOTracking();
```

## Troubleshooting

### Skills Not Loading

```bash
# Verify skills directory exists
ls -la .ai/skills/

# Check skill file structure
cat .ai/skills/product-marketing/SKILL.md

# Ensure YAML frontmatter is valid
# Skills must start with ---
```

### Agent Not Using Skills

```bash
# Be explicit in your prompts
# Instead of: "help with marketing"
# Try: "use the seo-audit skill to analyze my site"

# Or: "read my product-marketing context and write homepage copy"
```

### Missing Product Context

```bash
# Most skills require product-marketing context first
# Create it with:
# "Create a product marketing context document"

# Or manually create:
# .ai/product-marketing.md
```

### Skill Conflicts

```bash
# If multiple skills trigger, be specific:
# "use the copywriting skill" (not just "write copy")
# "use the cold-email skill" (not just "write email")
```

## Integration Examples

### With Next.js

```javascript
// pages/vs/[competitor].js
import { generateCompetitorPage } from '@/lib/programmatic-seo';
import { getProductContext } from '@/lib/product-marketing';

export async function getStaticPaths() {
  const competitors = await getCompetitors();
  return {
    paths: competitors.map(c => ({ params: { competitor: c.slug } })),
    fallback: false
  };
}

export async function getStaticProps({ params }) {
  const product = await getProductContext();
  const competitor = await getCompetitor(params.competitor);
  const page = await generateCompetitorPage(product, competitor);
  
  return { props: { page } };
}
```

### With React

```javascript
// components/ABTest.jsx
import { useEffect, useState } from 'react';
import { assignVariant, trackExperiment } from '@/lib/ab-testing';

export const ABTest = ({ testName, variants, children }) => {
  const [variant, setVariant] = useState(null);
  
  useEffect(() => {
    const userId = getUserId();
    const assigned = assignVariant(userId, testName);
    setVariant(assigned);
    trackExperiment(testName, assigned);
  }, [testName]);
  
  if (!variant) return null;
  
  return children(variants[variant]);
};

// Usage
<ABTest 
  testName="hero_headline"
  variants={{
    control: { headline: "Welcome" },
    treatment: { headline: "Double Your Growth" }
  }}
>
  {(variant) => <h1>{variant.headline}</h1>}
</ABTest>
```

### With Express

```javascript
// server.js
import express from 'express';
import { trackEvent } from './lib/analytics.js';

const app = express();

app.post('/api/track', async (req, res) => {
  const { event, properties } = req.body;
  
  await trackEvent(event, {
    ...properties,
    timestamp: new Date(),
    userAgent: req.headers['user-agent'],
    ip: req.ip
  });
  
  res.json({ success: true });
});

app.listen(3000);
```

## Related Resources

- [Agent Skills Spec](https://agentskills.io) - Standard for AI agent skills
- [Coding for Marketers](https://codingformarketers.com) - Learn coding for marketing
- [Conversion Factory](https://conversionfactory.co) - CRO agency by the creator
- [Swipe Files](https://swipefiles.com) - Marketing examples and templates

## Contributing

Skills are community-maintained. To contribute:

```bash
# Fork the repository
git clone https://github.com/YOUR_USERNAME/marketingskills.git

# Create a new skill
mkdir skills/your-skill-name
cd skills/your-skill-name

# Create SKILL.md with frontmatter
cat > SKILL.md << 'EOF'
---
name: your-skill-name
description: One-line description
triggers:
  - "trigger phrase 1"
  - "trigger phrase 2"
---

# Your Skill Name

Content here...
EOF

# Submit PR
git add skills/your-skill-name/
git commit -m "Add your-skill-name skill"
git push origin main
```

Each skill should include:
- Clear trigger phrases
- Real examples and code
- Related skills section
- Practical workflows
