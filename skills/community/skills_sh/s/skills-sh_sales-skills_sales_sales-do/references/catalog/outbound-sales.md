# Outbound Sales & Sequences


## /sales-agency-outbound

Multi-client outbound for lead gen agencies — infrastructure architecture, client isolation, domain strategy, warmup at scale, white-labeling, unified reporting, client onboarding playbooks, and cross-client operations. Use when one client's domain reputation is dragging down others, new client onboarding takes too long, mailbox warmup isn't scaling across clients, can't isolate sending infrastructure per client, or need a repeatable playbook for agency-wide reporting. Do NOT use for Smartlead-specific platform config (use /sales-smartlead), single-domain deliverability (use /sales-deliverability), or individual campaign strategy (use /sales-cadence).


## /sales-field-sales

Hyperlocal field-sales strategy — door-to-door / territory / route-based outbound to cash-heavy local SMB owners (restaurants, gas stations, convenience stores, salons, gyms, contractors, HVAC, lawn care) who ignore email cadences and aren't on Apollo or ZoomInfo. Covers corridor and territory target-list building from local sources (Google Maps Places API, Yelp Fusion, Foursquare, Outscraper, Phantombuster local-business scrapers — NOT Apollo), route planning and density optimization, 60-second clerk / in-person pitch frameworks, objection handling for cash-heavy owners, non-email follow-up via SMS / handwritten note / phone, and platform selection across SalesRabbit, Spotio, Map My Customers, Badger Maps, Outfield, Repsly, Skynamo, Geopointe. Use when planning a single-corridor pilot before multi-city expansion, can't find local SMBs in Apollo, an email cadence isn't getting replies from restaurant or gas-station owners, deciding which field-sales platform to pick for a small rep team, or following up on an in-person "maybe" without an email sequence. Do NOT use for database-driven B2B SaaS prospect lists (use /sales-prospect-list), digital email/LinkedIn cadences (use /sales-cadence), or post-call coaching on a recorded in-person visit (use /sales-siro).


## /sales-two-sided-marketplace

Two-sided marketplace GTM strategy — the cold-start chicken-and-egg problem, supply-vs-demand sequencing, flywheel mechanics, supply-side recruiting in tight local labor markets, and a single-corridor pilot framework before multi-city expansion for on-demand and recurring service marketplaces (cleaning, food delivery, courier, lawn care, mobile detailing, home services, pet care). Use when stuck on the chicken-and-egg problem and unsure whether to seed supply first or demand first, can't recruit 1099 gig workers fast enough to fulfill the demand you're closing, every demand-side sales call should double as a supply recruiting call but you don't know how to flip the "I don't mind cleaning the bathrooms" objection into a recruit, evaluating Wonolo / Instawork / Bluecrew / Workstream / Craigslist / Indeed as supply-side channels, planning a single-corridor pilot before multi-corridor or multi-city expansion, or writing a one-page integrated GTM plan tying brand + demand + supply + local visibility together. Do NOT use for the demand-side execution layer — door-to-door / territory / 60-second pitch design — (use /sales-field-sales) or the supply-side payment infrastructure (use /sales-marketplace-payouts).


## /sales-marketplace-payouts

Marketplace payouts strategy — selecting and operating the payment infrastructure that pays 1099 supply workers, sellers, drivers, hosts, and creators on a two-sided marketplace. Covers Stripe Connect (Standard / Express / Custom), PayPal Hyperwallet, Adyen for Platforms, Trolley, Tipalti, Routable, dots.dev, Branch, Nium, Wise Business, and Tremendous — when to pick each, the connected-account vs custodial trade-off, KYC and onboarding burden, daily-vs-weekly-vs-on-demand pay schedules, multi-currency, tax form generation (1099-K, 1099-NEC, W-9, W-8), and the 1099-misclassification risk that worker payment design carries. Use when deciding between Stripe Connect Standard vs Express vs Custom for a 1099 cleaning marketplace, comparing Hyperwallet vs Trolley for multi-country payouts, the supply side is churning because payouts arrive too slowly, can't decide whether to use a per-payout API (Trolley, Routable) or a full marketplace stack (Stripe Connect, Adyen for Platforms), need on-demand pay to compete on supply recruiting (Branch), worker classification risk shows up in how you set the payout schedule, or planning the 1099-K / 1099-NEC tax form workflow. Do NOT use for buyer-side checkout optimization or payment collection (use /sales-checkout) or affiliate commission tracking that ISN'T a marketplace payout (use /sales-affiliate-program).


## /sales-11x

11x.ai platform help — AI digital workers for revenue operations: Alice (AI SDR for multi-channel outbound via email, LinkedIn, SMS, WhatsApp) and Mike/Julian (AI phone agent for inbound calls, 24/7 qualification, meeting booking). Use when Alice's outreach personalization feels generic, campaign reply rates are below expectations, CRM sync with Salesforce or HubSpot not working, wondering if 11x is worth the annual contract cost, phone agent not handling objections well, want to connect 11x to your stack via API, or evaluating 11x vs AiSDR vs Artisan vs Salesforge for AI SDR. Do NOT use for general outbound cadence design (use /sales-cadence) or general email deliverability strategy (use /sales-deliverability).


## /sales-aisdr

AiSDR platform help — AI-powered SDR that automates cold email and LinkedIn outreach with deeply researched personalization. Use when AiSDR campaigns aren't getting replies, emails landing in spam, HubSpot sync not working, prospect imports failing, not sure how message credits work, wondering if AiSDR is the right AI SDR tool, or reply rates are lower than expected. Do NOT use for general outbound cadence design (use /sales-cadence) or general email deliverability strategy (use /sales-deliverability).


## /sales-amplemarket

Amplemarket platform help — AI-native all-in-one sales engagement with Duo AI copilot, 300M+ B2B contacts, multichannel sequences, intent signals, and deliverability suite. Use when setting up Amplemarket sequences, Amplemarket emails going to spam, Amplemarket credits burning fast, Amplemarket data enrichment not finding contacts, Amplemarket intent signals not triggering, or Amplemarket CRM sync issues with Salesforce or HubSpot. Do NOT use for general outbound strategy without a platform (use /sales-cadence), or general deliverability without Amplemarket (use /sales-deliverability).


## /sales-apollo

Apollo.io platform help — config, integrations, CRM sync, API, analytics, dialer, Chrome extension, credit management, admin. Use when Apollo settings aren't configured right, CRM sync is breaking or duplicating records, running out of credits too fast, API calls returning errors, or something in Apollo isn't working as expected. Do NOT use for building prospect lists (use /sales-prospect-list), enriching contacts (use /sales-enrich), interpreting buying signals (use /sales-intent), or designing outbound sequences (use /sales-cadence).


## /sales-apollo-sequences

Manages outbound sequences in Apollo.io — create, configure, optimize deliverability, and analyze performance. Use when Apollo emails are going to spam, sequence open rates are low, A/B tests aren't producing clear winners, mailboxes keep getting throttled, sequence stats don't look right, or emails just aren't sending. Do NOT use for designing cadence strategy and content (use /sales-cadence), general Apollo platform help (use /sales-apollo), or non-Apollo sequence tools (use /email-sequence).


## /sales-cirrus-insight

Cirrus Insight platform help — Salesforce-native sales productivity with email/calendar sync, Meeting AI, Conversation Intelligence, Live Coaching, Smart Scheduler, and Buyer Signals. Use when Cirrus Insight sync keeps breaking or needing reinstall, emails not logging to Salesforce automatically, Cirrus Insight sidebar not loading in Gmail or Outlook, choosing between Cirrus Insight and Yesware or Mixmax or Revenue Grid for Salesforce email integration, setting up Cirrus Insight Meeting AI for prospect research, configuring Buyer Signals tracking, Email Blast campaign erroring out, or understanding Cirrus Insight modular pricing. Do NOT use for picking between note-takers generally (use /sales-note-taker) or building a coaching program (use /sales-coaching).


## /sales-clari-copilot

Clari Copilot (formerly Wingman) platform help — conversation intelligence with real-time battlecards, live coaching during calls, AI call summaries, coaching scorecards, gametapes, deal intelligence, and CRM auto-update within Clari's revenue orchestration platform. Use when setting up Clari Copilot for a sales team, battlecards popping up too often during calls, meeting bot not joining or joining late, Clari Copilot vs Gong pricing or features, Clari API integration for forecast export or data ingestion, CRM field mapping not syncing correctly, coaching scorecards not scoring accurately, or evaluating Clari Copilot for enterprise conversation intelligence. Do NOT use for picking a note-taker across vendors (use /sales-note-taker) or building a coaching program (use /sales-coaching).


## /sales-closum

Closum platform help — omnichannel marketing automation: email, SMS, WhatsApp, Telegram, Web Push from one dashboard, drag-and-drop editors, no-code automations, AI assistant, landing pages, contact management. Use when Closum campaigns not sending or reaching inboxes, automations not triggering, landing pages not converting, CRM connection broken or data not syncing, or Closum deliverability rates dropping. Do NOT use for general email marketing strategy (use /sales-email-marketing), outbound cadence strategy (use /sales-cadence), funnel strategy (use /sales-funnel), or connecting Closum to other tools via Zapier (use /sales-integration).


## /sales-cluely

Cluely platform help — real-time AI meeting assistant with live coaching overlay, pre-call briefs, meeting notes, conversation analytics, and knowledge base RAG. Use when setting up Cluely for live AI prompts during sales calls, configuring the knowledge base with company docs for real-time RAG retrieval, connecting Cluely to HubSpot or Salesforce via Merge.dev, troubleshooting transcription accuracy or speaker attribution errors, comparing Cluely Pro vs Pro + Undetectability plans, or setting up team coaching scorecards and missed opportunity tracking. Do NOT use for choosing between AI note-takers across vendors (use /sales-note-taker) or reviewing a call for coaching (use /sales-call-review).


## /sales-lemlist

Lemlist platform help — multichannel sequences, lead database, enrichment, Lemwarm, unified inbox, AI personalization, LinkedIn automation, calls, WhatsApp, API, integrations. Use when Lemlist sequences not sending, emails landing in spam despite Lemwarm, leads not importing correctly, integrations not syncing, People Database search returning poor matches, or Lemlist API calls failing. Do NOT use for building prospect lists (use /sales-prospect-list), designing cadence strategy (use /sales-cadence), cross-platform deliverability (use /sales-deliverability), or enriching contacts outside Lemlist (use /sales-enrich).


## /sales-mailmo

Mailmo platform help — Email Finder, Email Verifier, catch-all detection, LinkedIn Chrome extension, bulk verification, CSV export. Use when Mailmo email lookups returning no results, verification flagging valid emails as risky, Chrome extension not finding contacts on LinkedIn, or bulk verification stuck or giving unexpected bounce rates. Do NOT use for building prospect lists (use /sales-prospect-list), cross-platform deliverability (use /sales-deliverability), enriching contacts across multiple tools (use /sales-enrich), or sending cold emails (Mailmo is a finder/verifier, not a sending tool — use /sales-cadence for outreach strategy).


## /sales-mailshake

Mailshake platform help — campaigns, Lead Catcher, recipients, senders, webhooks, API, analytics, integrations, deliverability settings. Use when Mailshake campaigns aren't getting replies, Lead Catcher is missing leads, recipients aren't importing correctly, sender accounts keep disconnecting, integrations aren't syncing, or API calls are failing. Do NOT use for building prospect lists (use /sales-prospect-list), enriching contacts (use /sales-enrich), designing cadence strategy (use /sales-cadence), or cross-platform deliverability (use /sales-deliverability).


## /sales-maxiq

MaxIQ platform help — AI-native revenue intelligence with EchoIQ conversation intelligence, InspectIQ pipeline visibility, ForecastIQ AI-driven forecasting, 9 AI agents (NoteTaker, Radar, Summarizer, Coach, Taskmaster, Watchdog, Forecaster, Revenue Planner, Deal Mapper), usage-based pricing (no per-seat), Salesforce/HubSpot CRM sync. Use when EchoIQ not capturing all meeting types, AI Coach scoring criteria not matching your sales process, CRM fields not auto-populating from calls, InspectIQ deal signals seem inaccurate, ForecastIQ predictions not matching reality, comparing MaxIQ vs Gong vs Clari for revenue intelligence, setting up AI Radar keyword tracking, or evaluating usage-based CI pricing vs per-seat alternatives. Do NOT use for designing outbound cadences (use /sales-cadence) or cross-platform coaching programs (use /sales-coaching).


## /sales-mixmax

Mixmax platform help — sequences, email tracking, one-click meetings, rules engine, dialer, AI Compose, Salesforce/HubSpot integration, polls, reporting. Use when Mixmax sequences aren't sending, rules or automations aren't firing, Salesforce or HubSpot sync is broken, scheduling links aren't working, open/click tracking seems inaccurate, or Mixmax emails are landing in spam. Do NOT use for general outbound cadence strategy (use /sales-cadence), cross-platform email deliverability (use /sales-deliverability), meeting scheduling strategy (use /sales-meeting-scheduler), email tracking strategy (use /sales-email-tracking), or connecting Mixmax to other tools via Zapier (use /sales-integration).


## /sales-momentum

Momentum platform help — AI revenue orchestration with automated CRM updates, Slack Deal Rooms, MEDDIC Autopilot, AI coaching, churn signals, and executive briefs. Use when Salesforce fields never get updated after calls, deal rooms in Slack are noisy or disorganized, MEDDIC tracking is inconsistent across reps, post-call action items aren't making it into the CRM, you need churn risk signals from customer conversations, or AI coaching scores don't match what you see on calls. Do NOT use for building outbound sequences (use /sales-cadence) or picking an AI note-taker (use /sales-note-taker).


## /sales-nooks

Nooks platform help — AI-native sales engagement workspace with parallel dialer, multi-channel sequencing, real-time coaching, and waterfall enrichment. Use when SDR team needs to increase connect rates with parallel dialing, reps are getting numbers flagged as spam during cold calling, setting up multi-channel sequences across calls email SMS and social in Nooks, configuring AI coaching scorecards or roleplay scenarios, evaluating Nooks vs Orum vs Koncert for parallel dialing, prospects complain about awkward delay when answering parallel dialer calls, or setting up waterfall enrichment across multiple data providers. Do NOT use for building a general coaching program (use /sales-coaching) or general outbound cadence strategy (use /sales-cadence).


## /sales-orum

Orum platform help — AI-powered parallel dialer for SDR teams with power and parallel dialing (up to 10 lines), AI Coaching Suite (scorecards, roleplay, coaching portals), virtual salesfloor, spam detection and number rotation, call intelligence. Use when setting up Orum parallel or power dialer for an SDR team, connect rates are dropping and numbers are getting flagged as spam, prospects hear awkward silence when answering parallel dialer calls, configuring Orum AI coaching scorecards or roleplay, evaluating Orum vs Nooks vs Koncert for parallel dialing, or setting up Orum integrations with Salesforce HubSpot Outreach Salesloft. Do NOT use for general outbound cadence strategy (use /sales-cadence) or building a coaching program (use /sales-coaching).


## /sales-outreach-io

Outreach platform help — sales engagement sequences, Kaia conversation intelligence, deal management, forecasting, and coaching. Use when sequences not getting replies in Outreach, Kaia not recording or transcribing correctly, deals stuck in pipeline and need Outreach deal insights, reps not following cadence steps, Outreach API integration or webhook setup, Outreach CRM sync issues with Salesforce or HubSpot, forecasting inaccurate in Outreach, or coaching reps using Kaia call recordings. Do NOT use for general cold email writing (use /sales-cadence) or Salesloft-specific questions (use /sales-salesloft).


## /sales-people-ai

People.ai (now Backstory) platform help — automatic activity capture, deal intelligence, pipeline health, revenue forecasting, MCP integration, Salesforce/Dynamics/Oracle CRM sync. Use when reps aren't logging activities and CRM data is stale, deals are slipping without warning and you need early risk signals, forecast accuracy is poor because it's based on gut not data, evaluating People.ai vs Gong vs Clari vs Revenue.io for revenue intelligence, activity data isn't tying back to pipeline or revenue outcomes, or you want to connect People.ai to AI agents via MCP. Do NOT use for conversation intelligence with call recording and transcription (use /sales-gong or /sales-note-taker), building outbound sequences (use /sales-cadence), or general CRM data cleanup strategy (use /sales-data-hygiene).


## /sales-reply

Reply.io platform help — multichannel sequences (email, LinkedIn, calls, SMS, WhatsApp), Jason AI SDR, B2B database, email warmup, deliverability tools, unified inbox, analytics, Salesforce/HubSpot integration, agency features. Use when Reply.io emails are landing in spam, sequences aren't getting replies, Jason AI isn't handling responses correctly, warmup isn't improving sender reputation, or Reply.io data isn't syncing to your CRM. Do NOT use for general outbound cadence strategy (use /sales-cadence), cross-platform email deliverability (use /sales-deliverability), email tracking strategy (use /sales-email-tracking), building prospect lists (use /sales-prospect-list), or connecting Reply.io to other tools via Zapier (use /sales-integration).


## /sales-revenue-io

Revenue.io platform help — Salesforce-native revenue orchestration with RingDNA dialer, Guided Selling cadences, Moments real-time coaching, conversation intelligence, and Revenue Intelligence dashboards. Use when calls not logging to Salesforce from Revenue.io, setting up Guided Selling cadences and task prioritization, configuring Moments real-time coaching notifications, choosing between Activate vs Engage vs Orchestrate tiers, dialer call dispositions not syncing to Salesforce, or Revenue.io vs Gong for conversation intelligence. Do NOT use for general conversation intelligence strategy (use /sales-note-taker) or building a coaching program (use /sales-coaching).


## /sales-salesken

Salesken platform help — AI-powered conversation intelligence with real-time in-call coaching, QA automation on 100% of calls, revenue intelligence with deal health and forecasting, field sales analytics, multilingual transcription, Salesforce/HubSpot/Zoho native CRM sync. Use when reps need live coaching prompts during calls, QA team wants to stop random call sampling and score every call automatically, compliance team needs automatic regulatory breach detection, managers can't see which deals are actually at risk, field sales team conversations aren't being captured, or real-time objection handling cues aren't reaching reps fast enough. Do NOT use for choosing between note-taker platforms (use /sales-note-taker) or building a coaching program (use /sales-coaching).


## /sales-salesloft

Salesloft platform help — config, Rhythm, Conversations, Deals, Forecast, Analytics, Drift, integrations, admin, API. Use when Salesloft settings aren't configured right, Rhythm signals feel noisy or unhelpful, Analytics dashboards don't show what you need, Drift chatbots aren't converting, or Salesloft integrations are broken. Do NOT use for building cadences (use /sales-cadence), reviewing calls (use /sales-call-review), inspecting deals (use /sales-deal-inspect), or forecasting (use /sales-forecast).


## /sales-salesroom

Salesroom platform help — AI-powered video conferencing built for sales with real-time coaching, buyer engagement scoring, battle cards, and CRM auto-update. Use when setting up Salesroom for your sales team, real-time coaching prompts not appearing during calls, buyer engagement scores not matching your read of the meeting, CRM updates not syncing to HubSpot or Salesforce after calls, choosing between Salesroom and Zoom with a separate note-taker, highlight clips not generating or sharing incorrectly, comparing Salesroom to Demodesk or Cluely for live coaching, or understanding Salesroom pricing tiers and free plan limits. Do NOT use for picking between note-takers generally (use /sales-note-taker) or building a coaching program (use /sales-coaching).


## /sales-smartlead

Smartlead platform help — campaigns, SmartSenders, SmartInfra, SmartAgents, SmartDialer, SmartProspect, SmartDelivery, warmup, API, integrations, agency/white-label. Use when Smartlead emails are landing in spam, campaigns have low reply rates, SmartSenders mailboxes keep getting flagged, warmup scores aren't improving, SmartAgents aren't personalizing well, SmartDialer connect rates are low, SmartDelivery tests show poor inbox placement, agency workspaces need restructuring, or the Smartlead API isn't syncing. Do NOT use for building prospect lists (use /sales-prospect-list), designing cadence strategy (use /sales-cadence), cross-platform deliverability (use /sales-deliverability), or multi-client agency architecture (use /sales-agency-outbound).


## /sales-solidroad

Solidroad platform help — AI-powered QA and training for CX teams. Use when reps ramping too slowly and need AI practice simulations, QA only covers 2% of conversations and you want 100% automated scoring, training and QA are disconnected and insights don't turn into coaching, setting up Solidroad scorecards or custom quality rubrics, connecting Solidroad to Salesforce Service Cloud or Zendesk or Intercom, or evaluating Solidroad vs Observe.AI vs Balto vs Cresta for contact center QA. Do NOT use for general coaching strategy without a specific platform (use /sales-coaching).


## /sales-trellus

Trellus platform help — AI-powered parallel dialer with real-time coaching for SDR teams, embedded in existing SEPs/CRMs via Chrome extension. Use when setting up Trellus parallel or power dialer inside Salesloft Outreach HubSpot Apollo, reps not getting real-time coaching cues during cold calls, phone numbers getting flagged as spam while dialing, configuring Trellus voice agents for practice roleplay or inbound call handling, evaluating Trellus vs Nooks vs Orum vs Kixie for parallel dialing, Trellus LinkedIn inbox management with Superhuman, or connecting Trellus to Salesforce HubSpot or other CRMs. Do NOT use for building a general coaching program (use /sales-coaching) or general outbound cadence strategy (use /sales-cadence).


## /sales-veloxy

Veloxy platform help — Salesforce-native field sales enablement with predictive intelligence, geolocation route planning, email tracking, and mobile CRM. Use when configuring Veloxy for a field sales team, Veloxy emails stopped sending or email sync breaking, Veloxy geolocation not showing nearby leads, Veloxy mobile app crashing or lead status not updating, comparing Veloxy to Scratchpad or Weflow or Badger Maps for Salesforce field reps, Veloxy Lite drip campaigns not triggering, or evaluating field sales software for outside reps on Salesforce. Do NOT use for conversation intelligence or meeting recording (use /sales-note-taker) or general CRM selection (use /sales-crm-selection).


## /sales-woodpecker

Woodpecker.co platform help — cold email campaigns, condition-based sequences, email warmup, Bounce Shield, Adaptive Sending, email verification, inbox rotation, centralized inbox, LinkedIn automation, Lead Finder, agency panel, API & webhooks. Use when Woodpecker emails are landing in spam, campaign open rates are dropping, you're not sure how to set up condition-based sequences, warmup isn't improving deliverability, the agency panel isn't isolating client data properly, or Woodpecker sending has stopped unexpectedly. Do NOT use for general outbound cadence strategy (use /sales-cadence), cross-platform email deliverability (use /sales-deliverability), email tracking strategy (use /sales-email-tracking), building prospect lists (use /sales-prospect-list), or connecting Woodpecker to other tools via Zapier (use /sales-integration).


## /sales-yesware

Yesware platform help — email tracking, campaigns, templates, Prospector, Meeting Scheduler, Salesforce integration, reporting. Use when Yesware tracking isn't showing opens, campaigns aren't sending to recipients, templates aren't personalizing correctly, Prospector search returns irrelevant leads, Meeting Scheduler links aren't working, or the Salesforce sync isn't logging activities. Do NOT use for building prospect lists (use /sales-prospect-list), enriching contacts (use /sales-enrich), designing cadence strategy (use /sales-cadence), cross-platform deliverability (use /sales-deliverability), meeting scheduling strategy (use /sales-meeting-scheduler), or email tracking strategy (use /sales-email-tracking).
