## Chapter 18: AI Tool Sites Going Global

> Compiled from 32 AI tool articles (2023-2026)

### 18.1 AI Tool Site Technical Architecture

#### 18.1.1 Tech Stack Selection

**Recommended Stack:**
- **Frontend:** Next.js + TailwindCSS + Shadcn/UI
- **Backend:** Next.js API Routes / Hono
- **Database:** Supabase / Neon (PostgreSQL)
- **Deployment:** Vercel / Cloudflare Pages
- **Payments:** Stripe / LemonSqueezy
- **AI Models:** OpenRouter / Replicate / FAL

**Minimal Solution (Zero Server Cost):**
- Pure HTML + CSS + JavaScript single file
- Deploy to Cloudflare Pages
- No framework, no npm needed

**Database-Free Approach:**
- Store data in JSON files
- Update online via GitHub API
- Vercel auto-detects code changes and deploys
- Suitable for directories, blogs, content sites

#### 18.1.2 AI App Development SOP

**Standard Process:**
1. Login/Auth: next-auth / clerk
2. Data Storage: supabase / neon
3. Multi-language: i18n / next-intl
4. Payments: stripe / lemonsqueezy / creem
5. File Storage: s3 / r2
6. Deployment: cloudflare / vercel
7. Domain Management: godaddy / namecheap

#### 18.1.3 Page Generation Techniques

**Using ChatGPT to Generate Pages:**
- Describe requirements to GPT-4, generate HTML+CSS code
- Include SEO requirements in key prompts
- Use "categorical listing" approach to organize content

**Multi-language Support:**
- Not translation, but regeneration in different languages
- Use GPT to translate title, description, button text
- Language directory structure: /hi/, /tl/, etc.

### 18.2 AI Model API Selection & Costs

> **⚠️ Pricing data updated 2026-03-17**, sources: Official docs + pricepertoken.com

#### 18.2.1 Major Model Pricing (per million tokens)

**OpenAI Series:**
| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| GPT-4.1 | $2.00 | $8.00 | Main model |
| GPT-4o | $2.50 | $10.00 | Multimodal |
| GPT-4o mini | $0.15 | $0.60 | Lightweight, very cheap |
| GPT-5 | $1.25 | $10.00 | Latest flagship |
| o4-mini | $1.10 | $4.40 | Reasoning model |

**Claude Series:**
| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| Claude Opus 4.6 | $5.00 | $25.00 | Strongest, for complex tasks |
| Claude Sonnet 4.6 | $3.00 | $15.00 | Best value |
| Claude Haiku 4.5 | $1.00 | $5.00 | Fast, good for batch |

**Google Gemini Series:**
| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| Gemini 2.5 Pro | $1.25 | $10.00 | Flagship |
| Gemini 2.5 Flash | $0.30 | $2.50 | Balanced choice |
| Gemini 2.0 Flash | $0.10 | $0.40 | Very cheap, has free tier |

**Money-Saving Tips:**
- **Batch API:** 50% discount (non-realtime tasks)
- **Context Caching:** Up to 90% savings
- **Free Tier:** Gemini series has generous free quota, good for starting out

**Model Selection Advice:**
- Daily coding: Claude Sonnet 4.6 (best value)
- Deep thinking: Claude Sonnet 4.6 extended thinking
- Complex tasks: Claude Opus 4.6
- Image editing: Gemini 2.5 Flash (Nano Banana)
- Batch processing: GPT-4o mini or Claude Haiku 4.5

#### 18.2.2 API Aggregation Solutions

**OpenRouter:**
- One API to call multiple models
- Middleman model, pay-per-use
- Good for testing different models

**Replicate:**
- Image generation model aggregation
- One model, one site, batch launch
- Common approach for wrapper products

### 18.3 AI Tool Site SEO Strategy

#### 18.3.1 New Keyword Strategy

**New Keyword Sources:**
- Big tech product launches (e.g., Sora, GPTs)
- AI model updates (e.g., Claude 4, GPT-5)
- Hot open source projects (e.g., MCP)

**Execution Points:**
- Prepare website framework before OpenAI/Google releases
- Go live immediately on release day
- Use Fake API to test flow, replace with real API when available

**Success Case:**
- GPTs directory went viral first week
- Got 4,700 backlinks in 4 days
- Key: Solve scarce need + fast launch + open source code

#### 18.3.2 Can You Still Build AI Directories?

**Why Yes:**
- New AI products appear daily
- Each product = new keyword
- New keywords have low competition, everyone has a chance
- First to index + good SEO = traffic

**AI Directory Alliance Strategy:**
- Bundle multiple directories into an alliance
- Split revenue by traffic volume

#### 18.3.3 Finding Real AI Needs

**Need Sources:**
- theresanaiforthat.com/requests (AI tool request collection page)
- Analyze real user requests
- Find buildable needs, make tool sites

### 18.4 AI Wrapper Strategy

#### 18.4.1 Wrapper Product SOP

**Standard Process:**
1. **Discover Trends:** HF Space + Google Trends + GitHub Trending
2. **Register Domain:** Namecheap / GoDaddy
3. **Launch Site:** Vibe Coding + code templates + AI capability (Replicate/FAL/OpenRouter)
4. **Get Traffic:** SEO + social media promotion
5. **Monetize:** Paid subscription + Google Ads

#### 18.4.2 Wrapper Considerations

- No technical barrier, but quickly builds cash flow
- Need to eat before chasing dreams
- Good quick monetization for indie developers

### 18.5 AI Video Generation Tool Comparison

#### 18.5.1 Sora Pricing

| Tier | Price | Credits |
|------|-------|---------|
| Plus | $20/month | 1000 credits, max 50 fast processing |
| Pro | $200/month | 10000 credits, unlimited slow processing, no watermark |

**Sora Video Specs:**
- 480p/720p/1080p resolutions
- 5-20 second duration
- Max 4 generated at once

#### 18.5.2 Midjourney V1 Video

**Pricing Advantage:**
- $60/month unlimited images + unlimited video generation
- Annual $48/month (best value)

**Technical Features:**
- Image-to-video (no text-to-video)
- Strong generalization, supports multiple styles
- Currently 480p resolution, expecting upgrade

#### 18.5.3 Google Veo 3

- Can generate video with sound and subtitles
- All animation, sound effects, voiceover, lip sync in one click

### 18.6 AI Image Editing Tools

#### 18.6.1 Nano Banana (Gemini 2.5 Flash)

**How to Use:**
- Google AI Studio: https://aistudio.google.com/
- Select Gemini 2.5 Flash Image Preview
- Free and unfiltered

**Core Capabilities:**
1. **Photo Editing:** Remove acne, slim body/face, skin repair
2. **Photo Enhancement:** Turn boring photos into stunning shots
3. **Outfit Display:** Flat lay clothing / try new outfits
4. **Doodle Control:** Box and mark for precise generation
5. **Sticker Generation:** Turn photos into cute stickers
6. **E-commerce Editing:** Change model wearing jewelry, preserve details
7. **Storyboard Generation:** Generate movie storyboards from character images

**Core Prompts:**
```
# Enhance boring photo
This photo is very boring and plain. Enhance it! Increase the contrast, boost the colors, and improve the lighting to make it richer. You can crop and delete details that affect the composition.

# Slim face/body
Make the character's face in the image slimmer, while increasing the muscle mass of the arms.

# Flat lay outfit
A flat lay photograph showing all the clothing items involved in the photo.

# Change outfit
The character in Figure 2 is wearing the clothing and accessories from Figure 1.

# Make sticker
Help me turn the character into a white outline sticker similar to Figure 2. The character needs to be transformed into a web illustration style, and add a playful white outline short phrase describing Figure 1.
```

#### 18.6.2 GPT-4o Image Generation

**Core Advantages:**
- Excellent text rendering (menus, invitations, etc.)
- Good multi-round generation consistency
- Strong instruction following
- Diverse styles
- Integrated real-world knowledge

**Limitations:**
- Long image cropping issues
- Hallucination causes fabrication
- Poor with 20+ concepts
- Chinese text rendering not accurate enough

### 18.7 AI Coding Tools

#### 18.7.1 Claude Code Tips (Creator's Recommendations)

**Core Tips (Boris Cherny original):**

1. **Run 5 Claude instances in parallel:** Open 5 terminal windows, use system notifications to know which needs input

2. **Local + Web dual-track:** 5 local + 5-10 claude.ai/code

3. **Always use Opus 4.5 + thinking mode:** Slower but needs less guidance, ultimately faster

4. **Team shares CLAUDE.md:** Claude makes mistake → document → Claude learns → makes fewer mistakes

5. **Most sessions start in Plan mode:** Press shift+tab twice, discuss plan before executing

6. **Use slash commands for frequent workflows:** Put in `.claude/commands/` directory

7. **Use sub-agents to automate common processes:** Do "process automation" not "expert division"

8. **Most important: Give Claude ways to verify work:** Like using Chrome extension to test UI, quality improves 2-3x

#### 18.7.2 Cursor Usage Advice

**Model Selection:**
- Claude Sonnet 4: Daily coding first choice
- Claude Sonnet 4 thinking: Debugging or project planning
- Claude Opus 4: Large complex projects or refactoring

**Best Practices:**
- Product managers have no excuse not to code
- Just describe requirements, Cursor writes code
- Click apply to auto-modify, click accept to approve
- Next.js + TailwindCSS + Shadcn/UI is the best stack

#### 18.7.3 Vibe Coding Practice

**Case: WorkAny Desktop Agent Development:**
- One week, full autopilot
- 100% code completed by cc
- Daily routine: open three windows, let three cc work simultaneously

**Core Insights:**
- AI era democratizes tech, everyone is an architect
- Technical breadth and global vision are biggest advantages
- Used to think hand-washing is cleaner than machine, now can trust AI
- Great programmers won't be replaced by AI

### 18.8 AI Agent Direction

#### 18.8.1 Agent Categories

**General Agents:**
- Manus, Genspark, Minimax Agent, Kouzi Space
- Need large resources, suitable for big companies

**Vertical Agents:**
- Lovart (design), iMean (travel planning), ClipClap (marketing video)
- Suitable for indie developers and small teams
- Enter from small scenarios, use Agent to transform SaaS

#### 18.8.2 Agent Infra Opportunities

**Selling Picks and Shovels:**
- Tools (MCP.so)
- Planning/scheduling
- Memory storage
- Boilerplate templates (ShipAny)
- VM/Container
- Auth
- Payment

### 18.9 MCP Ecosystem Opportunities

#### 18.9.1 What is MCP

- Open standard for AI era
- Like API 2.0
- Supports chatbots, agents, and other consumer endpoints

#### 18.9.2 Buildable Directions

1. **MCP Servers:** Expose SaaS products as MCP
2. **MCP App Store:** Manage and distribute MCP servers (like app stores for AI)
3. **MCP Service Router:** Like OpenRouter, middleman profits
4. **MCP Consumer Endpoints:** Chatbots, agents

### 18.10 Mini Game Site Monetization

#### 18.10.1 Revenue Data Reference

**Actual Data:**
- 13 websites earning $10,000+/month
- Most are mini game sites
- Average $5 per 1K visits

**Revenue Calculation:**
```
$10,000/month = 2M PV ÷ 3 ≈ 660K UV ÷ 30 days ≈ 22K UV/day
```

#### 18.10.2 Mini Game Site Traffic Sources

- 68.7% from organic search
- 26.43% from direct visits
- Good SEO is the core

### 18.11 AI Tool Site Web Design

#### 18.11.1 Three-Step Design Method

1. **Foundation:** Choose component library (Shadcn UI), define theme colors
2. **Accent:** GPT-4o generates icons, progress bars, backgrounds
3. **Elevation:** Style consistency (follow design principles: natural, deterministic)

#### 18.11.2 Quick Beautification

- Buy good-looking commercial templates (e.g., Aceternity Pro)
- Tell Claude Code to apply the template
- Done in 5 minutes

### 18.12 New Software Delivery Method

**Pure Static HTML Single-File Delivery:**
- User receives HTML file, opens in browser to run
- Sell API Key (limited credits, buy more when depleted)
- Or sell HTML file directly (one-time purchase, lifetime use)
- Get customers via software demo videos on social media

### 18.13 AI Search Aggregation

**SeekAll Case:**
- Browser plugin integrating multiple AI search entrances
- Open multiple windows to compare search results
- Solve AI hallucination: cross-validate multiple AI answers

### 18.14 Product Differentiation Methods

#### 18.14.1 Feature Differentiation

- **Vector Search:** GPTs Works was first to support vector retrieval
- **Browser Plugin:** GPTs Works was first to support browser plugin
- **Open Source:** Get stars and backlinks, expand influence

#### 18.14.2 Speed Differentiation

- First to index new AI products
- Fast launch more important than feature completeness
- Take off first, refuel later

#### 18.14.3 Scenario Differentiation

- 400+ segmented scenarios (HIX.AI case)
- Dedicated prompt optimization for each scenario

### 18.15 Core Lessons Summary

1. **Speed wins:** Launch in a week, a day, even an hour
2. **Quality over speed long-term:** After finding PMF, persist
3. **Dream big, start small:** Enter from vertical scenarios
4. **Self-sustaining:** Don't rely on capital, continuous monetization
5. **Traffic is king:** Actively manage social accounts, build influence
6. **Building products should be fun:** Continuous creation is the source of joy

---

*Notes:*
- This chapter based on 32 articles from AI tools category
- Time span: October 2023 - March 2026
- Focus: Technical architecture, API costs, SEO strategy, product differentiation
- Removed community ads and promotional content
- Preserved specific tool names, API prices, cost data
- Last updated: 2026-03-17
