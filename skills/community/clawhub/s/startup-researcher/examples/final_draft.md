<h1 style="text-align: center; font-size: 28pt; margin-top: 100px;">Custom Silicon AI Market Intelligence Report</h1>

<p style="text-align: center; font-size: 14pt; margin-top: 40px;">SambaNova · Groq · Cerebras

<p style="text-align: center; font-size: 11pt; color: #708090; margin-top: 20px;">March 22, 2026

<div style="page-break-after: always;"></div>

## Table of Contents

- [Custom Silicon — Market Overview](#custom-silicon--market-overview)
  - [Macro Trends](#macro-trends)
  - [Capital Concentration](#capital-concentration)
  - [Key Risks](#key-risks)
  - [Customer Adoption](#customer-adoption)
  - [Hiring Trends](#hiring-trends)
  - [Outlook](#outlook)
- [Competitive Pros/Cons Matrix](#competitive-proscons-matrix)
- [SambaNova Systems](#sambanova-systems)
- [Groq](#groq)
- [Cerebras Systems](#cerebras-systems)

<div style="page-break-after: always;"></div>

## Custom Silicon — Market Overview

### Macro Trends

The custom silicon AI market is undergoing a fundamental recalibration in early 2026. The industry narrative has decisively shifted from training-dominant workloads toward inference, which is projected to constitute two-thirds of all AI computation by year-end 2026 — up from 50% in 2025. This shift is creating massive demand for specialized inference hardware that can deliver orders-of-magnitude improvements in latency, throughput, and energy efficiency over general-purpose GPUs. Three architectural paradigms are competing: SambaNova's Reconfigurable Dataflow Units (RDUs), Groq's deterministic Language Processing Units (LPUs), and Cerebras's wafer-scale computing. Notably, Nvidia — the incumbent GPU monopolist — has begun validating alternate architectures by licensing Groq's LPU technology and integrating it into its own platforms, signaling that single-architecture solutions may not be sufficient for the next generation of AI workloads, particularly agentic AI systems that demand deterministic, low-latency responses.

### Capital Concentration

Capital flows in hot AI chips have been enormous but increasingly bifurcated. Cerebras leads the pack with $2.55B raised and a $23B valuation, driven by its OpenAI contract and imminent IPO. Groq has raised $1.75B at a $6.9B valuation, supercharged by its $17–20B Nvidia licensing deal. SambaNova, the earliest-founded of the three, has raised $1.48B but has seen its valuation compress from $5.1B (2021) to an implied range of $0.8–2.2B. This divergence reflects investor preference for companies with clear revenue anchors (Cerebras–OpenAI, Groq–Nvidia) versus those still building enterprise pipeline. Strategic investors are increasingly prominent — Intel invested $100–150M in SambaNova, Samsung participates in Groq, and AMD backs Cerebras — indicating that chip incumbents view these startups as both threats and potential technology sources.

### Key Risks

The primary risk across the category is **customer concentration**. Cerebras derived over 80% of its revenue from a single UAE-based customer (G42) in 2023–H1 2024, triggering a CFIUS review that delayed its IPO. Groq revised its 2025 revenue forecast from $2B+ to $500M+ due to data center scaling delays. SambaNova's valuation compression suggests the market questions whether its enterprise-focused GTM strategy can scale fast enough. Additionally, all three companies face ecosystem risk: Nvidia's CUDA moat means every customer adopting alternative silicon must also adopt a new software stack, creating significant switching costs. Geopolitical risk — particularly U.S. export controls and CFIUS reviews — adds regulatory uncertainty, as seen in Cerebras's G42 situation.

### Customer Adoption

Customer adoption is accelerating among the largest AI consumers. Cerebras's deal with OpenAI (750MW of wafer-scale inference, $10B+) and its AWS Bedrock integration mark the entry of wafer-scale AI into mainstream cloud infrastructure. Groq's technology is being validated at the highest level through Nvidia's integration of the Groq 3 LPU into the Vera Rubin platform, which will expose LPU-accelerated inference to the entire Nvidia ecosystem. SambaNova is targeting enterprise markets via the AWS Marketplace and has secured SoftBank as its first SN50 customer. Across the board, the trend is clear: hyperscalers and cloud providers are no longer relying on GPUs alone and are actively diversifying their compute portfolios.

### Hiring Trends

All three companies are in aggressive hiring mode, with emphasis on ASIC/chip design engineers, ML compiler specialists, and cloud infrastructure engineers. Cerebras is also hiring finance and accounting talent ahead of its IPO. SambaNova recently onboarded Clyde Hosein as President & COO, signaling operational maturity. Groq's Nvidia deal saw many of its senior engineers join Nvidia, which could create short-term talent gaps but also validates the caliber of its engineering team. The broader market is competing fiercely for AI compiler engineers — professionals who can bridge custom silicon hardware with AI framework software — as this skill set is the critical bottleneck for custom silicon adoption.

### Outlook

The next six months will be defining for the custom silicon category. **Cerebras** is on track for what could be the largest pure-play AI chip IPO, potentially listing as early as April 2026. A successful offering would validate the entire custom silicon thesis and provide a public benchmark for peer valuations. **Groq** will see its technology reach the broadest possible audience through Nvidia's Vera Rubin platform (Q3 2026 launch), though questions about its independent business model remain. **SambaNova** must deliver the SN50 chip (shipping H2 2026) and prove its performance claims against Nvidia Blackwell to reverse its valuation decline. The inference market opportunity is enormous — estimated at tens of billions in annual spend — and all three companies are positioned to capture meaningful share if their technology delivers. The wild card is Nvidia's response: will it embrace heterogeneous compute (as the Groq deal suggests), or aggressively defend GPU dominance?

<div style="page-break-after: always;"></div>

## Competitive Pros/Cons Matrix

| Company | Key Advantage (Pro) | Primary Weakness / Risk (Con) | Target Niche |
|---|---|---|---|
| **SambaNova** | Full-stack platform (chip + software + cloud); SN50 chip claims 5x faster than Blackwell at 3x lower TCO; strong enterprise focus with on-prem capability | Valuation compression (~$5.1B → ~$0.8–2.2B) signals market skepticism; requires customers to adopt non-GPU SW stack; no marquee hyperscaler contract yet | Enterprises deploying on-premise AI; regulated industries; SoftBank next-gen data centers |
| **Groq** | Industry-leading inference speed; Nvidia partnership validates technology; deterministic execution model ideal for agentic AI; $6.9B valuation with strong momentum | Revenue forecast miss ($2B → $500M+); Nvidia deal may commoditize LPU technology; senior engineer migration to Nvidia; long-term independence uncertain | Ultra-low-latency inference for LLMs; decode-phase acceleration; agentic AI applications |
| **Cerebras** | Wafer-scale architecture is a defensible physics advantage (56x larger than largest GPU); $23B valuation; $10B+ OpenAI deal; AWS Bedrock integration; IPO imminent | Historical customer concentration (G42 >80% of revenue); CFIUS/geopolitical risk; enormous capital requirements for wafer-scale manufacturing; IPO execution risk | Hyperscale AI inference and training; world's largest AI deployments (OpenAI); cloud provider integration |

<div style="page-break-after: always;"></div>

## SambaNova Systems

### 1. Fundamental Facts

| | |
|---|---|
| **Company Name** | SambaNova Systems |
| **Company Website URL** | [https://sambanova.ai](https://sambanova.ai) |
| **Public or Private** | Private |
| **Founding Year & HQ** | 2017, Palo Alto, California |
| **Founders and Key Leadership** | Rodrigo Liang (Co-founder & CEO), Kunle Olukotun (Co-founder & Chief Technologist), Christopher Ré (Co-founder), Lip-Bu Tan (Chairman), Clyde Hosein (President & COO) |
| **Key Investors** | Vista Equity Partners, Cambium Capital, Intel / Intel Capital, Battery Ventures, T. Rowe Price Associates, SoftBank, Google Ventures, BlackRock |
| **Total Raised, Latest Round & Current Valuation** | Total raised: ~$1.48B. Latest: Series E ($350M) in February 2026 led by Vista Equity Partners & Cambium Capital. Valuation: Undisclosed for Series E; prior Series D valuation was $5.1B (April 2021); implied secondary-market valuations range from ~$807M to ~$2.2B as of early 2026 |
| **Main Products / Technology** | Custom AI chips (Reconfigurable Dataflow Units — RDUs), full-stack enterprise AI platform for training and inference |
| **Market Focus / Target Audience** | Enterprises deploying on-premise or cloud-based AI, hyperscaler data centers, government & defense |

### 2. Narrative Overview

**Recent Developments (Last 6–12 Months):**

SambaNova closed its Series E round of over $350 million in February 2026, led by Vista Equity Partners and Cambium Capital with significant participation from Intel ($100–150M). This came on the heels of failed acquisition talks with Intel in late 2025, signaling the company's decision to remain independent and continue scaling.

The headline announcement was the <strong>SN50 AI chip</strong>, unveiled on February 24, 2026. SambaNova claims the SN50 is five times faster than Nvidia's Blackwell GPUs and delivers three-times lower total cost of ownership for agentic AI workloads. The SN50 is built on SambaNova's Reconfigurable Data Unit (RDU) architecture and is designed for models exceeding 10 trillion parameters with very large context lengths. SoftBank has been announced as the first customer, deploying the SN50 in their next-generation AI data center. In May 2025, SambaNova's AI platform became available on the AWS Marketplace, broadening enterprise access.

**Competitive Positioning:**

SambaNova differentiates through its <strong>dataflow architecture</strong> — a fundamental departure from the GPU-centric model. Rather than general-purpose GPUs, SambaNova's RDUs are purpose-built for AI workloads and claim to deliver superior performance-per-watt for large model inference. The company's full-stack approach (chip + software + cloud) appeals to enterprises that need on-premise control over sensitive data. However, the company faces an uphill battle against Nvidia's dominant ecosystem and must convince customers to adopt a non-GPU software stack. The significant gap between its Series D valuation ($5.1B) and recent implied secondary valuations ($0.8–2.2B) reflects market skepticism.

### 3. Product Details

| Product Name | Product Website URL | Description & Value Proposition | Target Users / Customers | Pricing Model | Key Features & Underlying Technology |
|---|---|---|---|---|---|
| SN50 AI Chip | [sambanova.ai](https://sambanova.ai) | Next-gen RDU chip — 5x faster than Nvidia Blackwell, 3x lower TCO for agentic AI | Hyperscale data centers, enterprise AI deployments | Enterprise / OEM licensing | Reconfigurable Dataflow Architecture; 10T+ parameter models; massive context windows; ships H2 2026 |
| SambaNova DataScale | [sambanova.ai](https://sambanova.ai) | Integrated HW/SW system for deep learning, foundation models, and AI-for-Science | Enterprise R&D, government labs | Appliance purchase / subscription | Dataflow architecture, pre-integrated SW stack, on-premise deployment |
| SambaNova Cloud | [cloud.sambanova.ai](https://cloud.sambanova.ai) | Cloud inference platform — "world's fastest AI inference" powered by SN40L | Developers, enterprises needing API-based inference | API usage tiers (free / paid) | Llama 3.1 405B support, multiple model hosting, powered by SN40L RDU |
| SambaNova Suite | [sambanova.ai](https://sambanova.ai) | Full-stack AI solution (on-prem or cloud) for enterprise AI deployment | Enterprises, regulated industries | Enterprise subscription | End-to-end platform: training + inference, data pipeline integration |
| Samba-1 | [sambanova.ai](https://sambanova.ai) | Trillion-parameter generative AI model composition from 50+ open-source models | Enterprises needing diverse AI capabilities | Platform-bundled | Composition of experts from 50+ models, enterprise-grade safety |

### 4. Hiring

SambaNova is actively hiring across engineering, product, and go-to-market roles. Key open positions include ASIC / Chip Design Engineers, Software Engineers (AI Platform / Cloud), ML / AI Research Scientists, and Sales & Solutions Engineers.

Careers page: [https://sambanova.ai/careers](https://sambanova.ai/careers)

### 5. Highlights

- 🚩 **Funding >$100M:** Series E raised $350M+ in February 2026
- 🚀 **Major Product Launch:** SN50 AI chip unveiled February 24, 2026 — claims 5x faster than Nvidia Blackwell
- 🤝 **Major Partnership:** SoftBank to be first SN50 customer for next-gen AI data center
- 📉 **Valuation Concern:** Implied secondary-market valuation has dropped significantly from $5.1B (2021) to ~$0.8–2.2B range
- 🏪 **Distribution:** SambaNova platform available on AWS Marketplace (May 2025)

### 6. References

- https://sambanova.ai
- https://sacra.com (SambaNova profile)
- https://tracxn.com (SambaNova funding data)
- https://siliconrepublic.com (Series E coverage)
- https://economictimes.com (Intel investment / acquisition talks)
- https://hpcwire.com (SN50 announcement)
- https://aibusiness.com (SN50 product details)
- https://businesswire.com (AWS Marketplace, SN50 PR)
- https://pminsights.com (Valuation data)
- https://craft.co (Leadership team)

<div style="page-break-after: always;"></div>

## Groq

### 1. Fundamental Facts

| | |
|---|---|
| **Company Name** | Groq |
| **Company Website URL** | [https://groq.com](https://groq.com) |
| **Public or Private** | Private |
| **Founding Year & HQ** | 2016, Mountain View, California (offices in San Jose, CA; Liberty Lake, WA; Toronto, Canada; London, UK) |
| **Founders and Key Leadership** | Jonathan Ross (CEO & Co-founder), Douglas Wightman (Co-founder), Sunny Madra (COO & President), Dinesh Maheshwari (CTO), Claire Hart (CLO), Ian Andrews (CRO) |
| **Key Investors** | Disruptive (lead, Sept 2025), BlackRock, Neuberger Berman, DTCP, Samsung, Cisco, Chamath Palihapitiya, Tiger Global |
| **Total Raised, Latest Round & Current Valuation** | Total raised: ~$1.75B across 6 rounds. Latest: $750M round in September 2025. Post-money valuation: $6.9B (up from $2.8B in August 2024) |
| **Main Products / Technology** | Language Processing Unit (LPU) — custom inference-specific AI chip; GroqCloud API platform |
| **Market Focus / Target Audience** | AI developers, enterprises needing ultra-fast low-latency inference, hyperscalers, agentic AI applications |

### 2. Narrative Overview

**Recent Developments (Last 6–12 Months):**

Groq's trajectory over the past year has been defined by two landmark events: a <strong>$750M funding round</strong> in September 2025 (valuing the company at $6.9B) and a <strong>transformative deal with Nvidia</strong> in December 2025.

The Nvidia deal — reportedly worth $17–20 billion — saw Nvidia acquire a non-exclusive license to Groq's LPU technology and physical assets, along with the integration of many of Groq's senior engineers into Nvidia. At <strong>GTC 2026</strong> in March 2026, Nvidia unveiled the <strong>Groq 3 LPU</strong>, announcing its integration into Nvidia's new <strong>Vera Rubin AI platform</strong>. The Groq 3 LPU, manufactured by Samsung on a 4nm process, is designed as a dedicated decode-phase co-processor, complementing Nvidia's GPUs for extreme inference speed. Nvidia plans to release the Groq 3 LPU in Q3 2026.

Groq adjusted its 2025 revenue forecasts downward — from over $2 billion to more than $500 million — citing delays in scaling data center capacity. The company opened its first European data center in Helsinki and continues to build out global AI infrastructure.

**Competitive Positioning:**

Groq occupies a unique niche as the <strong>speed leader in AI inference</strong>. Its LPU architecture prioritizes deterministic execution with large amounts of on-chip SRAM, avoiding GPU-style memory-bandwidth bottlenecks. Groq claims up to 10x higher energy efficiency for certain inference tasks. The Nvidia partnership validates Groq's core technology while raising questions about its long-term independence — Nvidia is now both a customer/partner and a competitor. The company's GroqCloud platform allows developers and enterprises to access LPU-powered inference via API, positioning it as both a chip company and an inference-as-a-service provider.

### 3. Product Details

| Product Name | Product Website URL | Description & Value Proposition | Target Users / Customers | Pricing Model | Key Features & Underlying Technology |
|---|---|---|---|---|---|
| Groq LPU (Language Processing Unit) | [groq.com](https://groq.com) | Custom inference chip delivering industry-leading speed and energy efficiency for LLM workloads | Hyperscalers, enterprises, AI infrastructure providers | OEM / enterprise licensing | Deterministic execution, large on-chip SRAM, eliminates memory-bandwidth bottleneck, 10x energy efficiency claim |
| Groq 3 LPU | [groq.com](https://groq.com) | Next-gen LPU integrated into Nvidia Vera Rubin platform as decode-phase co-processor | Nvidia ecosystem customers, data centers | Via Nvidia platform | Samsung 4nm process, dedicated decode-phase acceleration, complements Nvidia GPUs |
| GroqCloud | [groq.com/groqcloud](https://groq.com/groqcloud) | Cloud API platform offering LPU-powered inference for major open-source models | Developers, enterprises, AI app builders | API usage-based pricing (free tier available) | Llama, Mixtral model support; ultra-low latency; simple REST API |

### 4. Hiring

Groq is actively hiring across hardware, software, cloud, and business functions. Key areas include ASIC / Hardware Design Engineers, Cloud Infrastructure Engineers, ML Compiler Engineers, and Sales & Business Development.

Careers page: [https://groq.com/careers](https://groq.com/careers)

### 5. Highlights

- 🚩 **Funding >$100M:** $750M raised in September 2025 at $6.9B valuation
- 🚀 **Major Product Launch:** Groq 3 LPU unveiled at GTC 2026 (March 2026), integrated into Nvidia Vera Rubin
- 💰 **Landmark Deal:** Nvidia acquired non-exclusive LPU license for ~$17–20B (December 2025)
- 🌍 **Infrastructure Expansion:** First European data center opened in Helsinki
- ⚠️ **Revenue Miss:** 2025 revenue forecast reduced from $2B+ to $500M+ due to data center scaling delays
- 🏢 **Valuation Milestone >$1B:** $6.9B valuation (September 2025)

### 6. References

- https://groq.com (Official site, press releases)
- https://siliconangle.com (Sept 2025 funding coverage)
- https://tracxn.com (Groq funding data)
- https://techzine.eu (Revenue forecast, Helsinki data center)
- https://scmp.com (Revenue forecast details)
- https://servethehome.com (Nvidia-Groq deal at GTC 2026)
- https://tomshardware.com (Groq 3 LPU details)
- https://jonpeddie.com (Nvidia-Groq strategy analysis)
- https://alphamatch.ai (Groq 3 LPU technical details)
- https://wikipedia.org (Groq overview, founders)
- https://craft.co (Leadership team)

<div style="page-break-after: always;"></div>

## Cerebras Systems

### 1. Fundamental Facts

| | |
|---|---|
| **Company Name** | Cerebras Systems |
| **Company Website URL** | [https://cerebras.ai](https://cerebras.ai) |
| **Public or Private** | Private (IPO expected Q2 2026) |
| **Founding Year & HQ** | 2015, Sunnyvale, California (offices in San Diego, Toronto, Bangalore) |
| **Founders and Key Leadership** | Andrew Feldman (Co-founder & CEO), Gary Lauterbach (Co-founder & CTO Emeritus), Sean Lie (Co-founder & CTO), Jean-Philippe Fricker (Co-founder & Chief System Architect), Michael James (Co-founder & Chief Architect, Advanced Technologies), Dhiraj Mallick (COO), Andy Hock (CSO & SVP Product) |
| **Key Investors** | Fidelity Management & Research Company, Atreides Management, Tiger Global, Valor Equity Partners, 1789 Capital, Altimeter, Alpha Wave Global, Benchmark, AMD |
| **Total Raised, Latest Round & Current Valuation** | Total raised: ~$2.55B across 8 rounds. Latest: Series H ($1B) in February 2026 at $23B post-money valuation. Prior: Series G ($1.1B) in September 2025 at $8.1B |
| **Main Products / Technology** | Wafer Scale Engine (WSE) — world's largest AI chip; CS-3 AI compute system; Cerebras Cloud & inference services |
| **Market Focus / Target Audience** | Hyperscalers (OpenAI, Meta), cloud providers (AWS), enterprise AI, government & defense, AI research labs |

### 2. Narrative Overview

**Recent Developments (Last 6–12 Months):**

Cerebras has had a breakout year, cementing its position as the most highly valued custom silicon AI startup. The company raised <strong>$1.1B in Series G</strong> (September 2025, $8.1B valuation) followed by a <strong>$1B Series H</strong> (February 2026, $23B valuation) — nearly tripling its valuation in five months. Total funding now exceeds $2.55 billion.

The company's <strong>IPO journey</strong> has been closely watched. After initially filing in September 2024, Cerebras withdrew its S-1 in October 2025, citing that the prospectus was "out of date." A key obstacle was a CFIUS (Committee on Foreign Investment) security review related to ties with UAE-based G42, which had accounted for over 80% of revenue in 2023 and H1 2024. Cerebras has since restructured its investor base to satisfy regulators and is preparing to refile for an IPO in Q2 2026, targeting a ~$2B listing with Morgan Stanley, potentially as early as April 2026.

On the business side, <strong>Cerebras signed a multi-year deal with OpenAI</strong> in January 2026 to deploy 750 megawatts of wafer-scale systems, a contract valued at over $10 billion — creating what is expected to be the world's largest high-speed AI inference deployment. In March 2026, Cerebras and <strong>AWS announced a collaboration</strong> to introduce a disaggregated inference solution on Amazon Bedrock, combining AWS's Trainium chips with Cerebras CS-3 systems.

**Competitive Positioning:**

Cerebras's moat is its radical <strong>wafer-scale architecture</strong> — the WSE-3 chip contains 4 trillion transistors and 900,000 AI-optimized cores on a single wafer, making it 56x larger than the biggest GPUs. This delivers a physics-based advantage: the entire model fits on-chip, eliminating inter-chip communication overhead. Cerebras claims 20x faster inference and training than GPU-based alternatives with dramatically lower power consumption per compute unit. The company projects that inference workloads will constitute two-thirds of all AI computation in 2026, positioning its technology at the center of the industry's most important trend. However, customer concentration (OpenAI, G42) and regulatory risk remain concerns.

### 3. Product Details

| Product Name | Product Website URL | Description & Value Proposition | Target Users / Customers | Pricing Model | Key Features & Underlying Technology |
|---|---|---|---|---|---|
| Wafer Scale Engine 3 (WSE-3) | [cerebras.ai](https://cerebras.ai) | World's largest AI chip — 4 trillion transistors, 900K cores on a single wafer | Hyperscalers, AI labs, government | OEM / system integration | 56x larger than largest GPUs, on-chip model execution, 20x faster than GPU alternatives |
| CS-3 System | [cerebras.ai](https://cerebras.ai) | Complete AI compute system powered by WSE-3 | Data centers, enterprises, cloud providers | System purchase / managed service | Full system integration, cooling, networking; pairs with MemoryX & SwarmX |
| Cerebras Cloud (Inference) | [cerebras.ai/cloud](https://cerebras.ai/cloud) | Cloud-hosted AI inference service | Developers, enterprises, AI app builders | API usage-based pricing | Ultra-fast inference, Llama model support, low-latency API |
| Cerebras + AWS Bedrock Integration | [cerebras.ai](https://cerebras.ai) / [aws.amazon.com](https://aws.amazon.com) | Disaggregated inference solution combining Trainium + CS-3 on Amazon Bedrock | AWS enterprise customers | Via AWS Bedrock pricing | AWS Trainium + Cerebras CS-3 hybrid, accelerates GenAI and LLM workloads |

### 4. Hiring

Cerebras is aggressively hiring across all functions as it prepares for its IPO. Key areas include ASIC & Hardware Engineers, Software / ML Infrastructure Engineers, Cloud Platform Engineers, Finance / Accounting (IPO-readiness), and Sales & Customer Success.

Careers page: [https://cerebras.ai/careers](https://cerebras.ai/careers)

### 5. Highlights

- 🚩 **Funding >$100M:** Series G ($1.1B, September 2025) and Series H ($1B, February 2026)
- 💰 **Valuation Milestone >$10B:** Valued at $23B post-money (February 2026)
- 🚀 **Major Partnership:** Multi-year, $10B+ deal with OpenAI for 750MW of wafer-scale inference (January 2026)
- 🤝 **Cloud Partnership:** AWS Bedrock integration announced (March 2026)
- 📈 **IPO Imminent:** Preparing to refile IPO in Q2 2026; potential ~$2B listing led by Morgan Stanley
- ⚠️ **Regulatory Risk:** CFIUS review over G42 ties delayed original IPO filing; investor base restructured

### 6. References

- https://cerebras.ai (Official site, press releases, team page)
- https://crunchbase.com (Cerebras funding/IPO data)
- https://nextplatform.com (Series G coverage)
- https://marketscreener.com (Series H details)
- https://pminsights.com (Valuation data)
- https://tracxn.com (Funding rounds summary)
- https://wikipedia.org (Cerebras overview)
- https://marketwise.com (WSE-3 specs, inference projections)
- https://financialcontent.com (IPO details, OpenAI deal)
- https://techinasia.com (AWS partnership, OpenAI deal)
- https://digitimes.com (AWS Bedrock integration)
- https://forgeglobal.com (IPO timeline)

---

<span style="font-size: 8px;">Generated with <a href="https://github.com/hxy9243/skills/tree/main/startup-researcher">startup researcher</a>, March 22, 2026</span>
