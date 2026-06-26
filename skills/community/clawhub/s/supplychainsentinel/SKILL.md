---
name: supplychainsentinel
description: "Monitor supplier APIs, port delays, and weather in real-time to trigger automatic PO rerouting and stakeholder alerts. Use when the user needs supply chain disruption detection, logistics risk mitigation, or backup sourcing automation."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["SHIPPO_API_KEY","FLEXPORT_API_KEY","OPENWEATHER_API_KEY","SLACK_WEBHOOK_URL","SENDGRID_API_KEY","DATABASE_URL"],"bins":["curl","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"⚓"}}
---

## Overview

**SupplyChainSentinel** is a real-time supply chain monitoring and disruption response system that eliminates blind spots in modern logistics networks. Post-COVID supply chain fragility demands intelligent automation—this skill monitors 15+ shipping APIs, port delay databases, and weather systems to detect disruptions before they impact your operations, then automatically triggers PO rerouting workflows and notifies stakeholders with updated ETAs.

### Why This Matters

Supply chain disruptions cost enterprises an average of $900K per incident (Gartner). Manual monitoring across Flexport, Shippo, AIS vessel tracking, customs databases, and weather APIs is impossible at scale. SupplyChainSentinel consolidates these signals into a single intelligent system that:

- **Prevents stockouts** by detecting delays 48-72 hours early
- **Reduces emergency shipping costs** by automating failover to backup suppliers
- **Maintains customer trust** with proactive ETA recalculations
- **Integrates with existing workflows** via Slack, email, and ERP systems (SAP, NetSuite, Microsoft Dynamics)

---

## Quick Start

### Example 1: Monitor Inbound Shipments for Port Delays
```
Monitor port delays for all active shipments using AIS data. Alert if any 
vessel is delayed >12 hours from expected arrival. Include vessel name, 
port code, current delay hours, and recommended alternative routes.
```

**What happens:**
- Queries Flexport and Shippo APIs for all active shipments
- Checks AIS (Automatic Identification System) vessel tracking data
- Compares against scheduled ETAs
- Sends Slack alert with delay details and backup supplier recommendations

---

### Example 2: Trigger Automatic PO Rerouting on Weather Risk
```
Check weather forecast for Shanghai and Rotterdam ports over next 7 days. 
If typhoon or severe storm detected with >60% probability, automatically 
create alternative POs with backup suppliers and notify procurement team.
```

**What happens:**
- Queries OpenWeather API for port regions
- Analyzes severe weather probability thresholds
- Fetches backup supplier list from your database
- Creates new POs in your ERP system
- Sends email notifications to procurement stakeholders

---

### Example 3: Real-Time Supplier Status Dashboard
```
Generate a live supplier health report showing: supplier name, on-time 
delivery rate (last 30 days), current shipment count, average delay hours, 
and risk score (1-10). Highlight any suppliers with >15% late shipments.
```

**What happens:**
- Aggregates historical shipment data from Shippo and Flexport
- Calculates on-time delivery metrics per supplier
- Scores supplier reliability in real-time
- Outputs JSON dashboard data for integration with Tableau or Looker

---

## Capabilities

### 1. Real-Time Supplier API Monitoring
Monitor shipment status across 15+ logistics providers with automatic data normalization:

- **Shippo** — parcel tracking, label generation, carrier rates
- **Flexport** — ocean freight, customs clearance, consolidation
- **FedEx/UPS/DHL APIs** — express and ground shipments
- **Maersk** — container vessel tracking and port schedules
- **Port Authority APIs** — congestion metrics and berth availability

**Usage:**
```
Poll supplier APIs every 30 minutes. Flag any shipment with status change 
to "delayed", "held_customs", or "vessel_diversion". Cross-reference with 
historical baseline to identify anomalies.
```

---

### 2. Port Delay Detection via AIS & Customs Data
Track vessel movements and port congestion in real-time:

- **AIS vessel tracking** — real-time GPS coordinates, speed, ETA updates
- **Port congestion indices** — berth wait times, queue lengths
- **Customs clearance tracking** — document status, inspection hold-ups
- **Weather impact correlation** — storm delays, port closures

**Usage:**
```
For each active ocean shipment, retrieve vessel AIS data. Compare current 
position against expected trajectory. If vessel speed <3 knots for >4 hours 
in port area, flag as potential congestion and estimate delay.
```

---

### 3. Weather Impact Forecasting
Predict logistics disruptions from meteorological data:

- **Typhoon/hurricane tracking** — probability, wind speed, affected ports
- **Fog and visibility impacts** — on port operations (Singapore, Rotterdam)
- **Temperature extremes** — for temperature-sensitive cargo (pharma, food)
- **Port closure predictions** — 48-72 hour forecast based on weather thresholds

**Usage:**
```
Daily 6 AM check: Query OpenWeather API for all active port regions. If 
severe weather probability >50% and shipment ETA within 5 days, trigger 
alternative routing evaluation.
```

---

### 4. Automatic PO Rerouting to Backup Suppliers
Intelligently failover to alternative suppliers when disruptions detected:

- **Backup supplier database** — pre-configured alternatives per SKU
- **Automated PO creation** — generates new purchase orders in your ERP
- **Cost comparison** — selects backup based on price + delivery speed
- **Inventory optimization** — prevents over-ordering via safety stock adjustment

**Usage:**
```
When primary supplier shipment delayed >24 hours, automatically:
1. Query backup supplier inventory for same SKU
2. Compare landed cost (price + expedited shipping)
3. Create PO if cost delta <15% and delivery <original ETA
4. Notify procurement with comparison matrix
5. Update master schedule with new ETA
```

---

### 5. Stakeholder Notifications with ETA Recalculations
Multi-channel alerts with updated delivery timelines:

- **Slack integration** — real-time alerts to #supply-chain channel
- **Email notifications** — detailed reports to procurement, sales, finance
- **ERP system updates** — automatic PO and delivery schedule changes
- **Customer notifications** — optional proactive outbound to B2B customers
- **ETA recalculation** — machine learning model factors in port delays, weather, carrier performance

**Usage:**
```
When disruption detected, send Slack alert:
"🚨 SUPPLY CHAIN ALERT: Maersk vessel UASC-2847 delayed 18 hours at 
Rotterdam. Original ETA: Jan 15, 2 PM. Revised ETA: Jan 16, 8 PM. 
Backup supplier PO created. Procurement notified. [View Details]"
```

---

## Configuration

### Required Environment Variables

```bash
# Shipping & Logistics APIs
export SHIPPO_API_KEY="your_shippo_token"
export FLEXPORT_API_KEY="your_flexport_api_key"
export MAERSK_API_KEY="your_maersk_api_key"

# Weather & Geolocation
export OPENWEATHER_API_KEY="your_openweather_key"
export AIS_API_KEY="your_ais_provider_key"  # e.g., MarineTraffic

# Notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
export SENDGRID_API_KEY="your_sendgrid_key"

# Database & ERP
export DATABASE_URL="postgresql://user:pass@localhost/supply_chain_db"
export NETSUITE_ACCOUNT_ID="your_netsuite_account"
export NETSUITE_API_KEY="your_netsuite_key"
```

### Configuration Options

```yaml
monitoring:
  poll_interval_minutes: 30          # How often to check APIs
  delay_threshold_hours: 12          # Trigger alert if delayed >12h
  weather_severity_threshold: 0.60   # Storm probability threshold
  
rerouting:
  cost_variance_threshold: 0.15      # Allow 15% cost increase for backup
  enable_auto_po_creation: true      # Auto-create POs or notify only
  safety_stock_buffer_days: 2        # Additional buffer for backup orders
  
notifications:
  slack_enabled: true
  email_enabled: true
  channels:
    - "#supply-chain"
    - "procurement@company.com"
    - "cfo@company.com"              # Finance alerts on cost changes
```

### Setup Instructions

1. **Create supplier master data table:**
```sql
CREATE TABLE suppliers (
  supplier_id UUID PRIMARY KEY,
  name VARCHAR(255),
  api_type VARCHAR(50),
  api_credentials JSONB,
  backup_suppliers UUID[],
  on_time_rate DECIMAL,
  last_updated TIMESTAMP
);
```

2. **Configure API credentials** in your `.env` file or secrets manager (AWS Secrets Manager, HashiCorp Vault)

3. **Connect to your ERP system** (NetSuite, SAP, Dynamics 365) via API or webhook

4. **Set up Slack workspace** and generate incoming webhook URL

5. **Initialize monitoring** with historical shipment data (last 90 days) to establish baselines

---

## Example Outputs

### Port Delay Alert (Slack)
```
🚨 SUPPLY CHAIN DISRUPTION DETECTED

Shipment: #SHP-2024-001847
Carrier: Maersk Line
Vessel: UASC-2847
Current Location: Rotterdam Port, Netherlands
Current Delay: +18 hours from scheduled ETA

📊 Details:
• Scheduled Port Arrival: Jan 15, 2:00 PM UTC
• Revised ETA: Jan 16, 8:00 PM UTC
• Reason: Port congestion (12 vessels ahead in queue)
• Weather Impact: None detected

✅ Action Taken:
• Backup supplier PO created (cost +8%)
• New delivery date: Jan 18, 10:00 AM
• Procurement team notified
• Customer notification scheduled

🔗 View Full Details | Escalate | Dismiss
```

### Supplier Health Report (JSON)
```json
{
  "report_date": "2024-01-15T10:30:00Z",
  "suppliers": [
    {
      "supplier_id": "SUP-001",
      "name": "Shanghai Electronics Ltd",
      "on_time_delivery_rate": 0.94,
      "active_shipments": 7,
      "avg_delay_hours": 2.1,
      "risk_score": 3,
      "status": "healthy",
      "last_shipment": "2024-01-14T16:45:00Z"
    },
    {
      "supplier_id": "SUP-004",
      "name": "Port Klang Logistics",
      "on_time_delivery_rate": 0.71,
      "active_shipments": 3,
      "avg_delay_hours": 14.8,
      "risk_score": 7,
      "status": "at_risk",
      "recommendation": "Shift 40% volume to backup supplier SUP-007"
    }
  ]
}
```

### ETA Recalculation Report (Email)
```
Subject: Supply Chain Update - Shipment #SHP-2024-001847

Dear Procurement Team,

Your shipment from Shanghai to Rotterdam has been updated:

Original ETA: January 15, 2:00 PM
Updated ETA: January 16, 8:00 PM
Delay Reason: Port congestion + AIS data indicates vessel speed reduced

Backup Action:
A secondary shipment has been created with Alternative Supplier (DHL Express)
Expected Delivery: January 17, 6:00 PM
Cost Impact: +$2,400 (8% premium)

Next Steps:
1. Review backup PO in NetSuite: [Link]
2. Confirm customer notification preference
3. Approve cost variance (auto-approved if <15%)

Questions? Contact supply-chain-ops@company.com
```

---

## Tips & Best Practices

### 1. Establish Baseline Metrics First
Before automating rerouting, collect 60-90 days of historical data to understand:
- Typical delay patterns by supplier, route, season
- Normal port congestion at key hubs (Shanghai, Rotterdam, Singapore)
- Seasonal weather impacts (typhoon season, monsoons)

**Action:** Run in "monitoring only" mode for 60 days before enabling auto-rerouting.

---

### 2. Pre-Configure Backup Suppliers
Manually map 2-3 backup suppliers per critical SKU before activating automation:
- Verify backup supplier quality, lead times, and pricing
- Establish volume discounts and payment terms
- Test API integration with backup supplier systems
- Document cost variance thresholds (e.g., allow 10-15% premium for faster delivery)

---

### 3. Set Appropriate Alert Thresholds
Too many false alarms cause alert fatigue; too few miss real disruptions:
- **Port delays:** Alert at >12 hours (typical port delay = 4-8 hours)
- **Weather:** Alert at >60% severe weather probability within 5 days of arrival
- **Supplier delays:** Alert if on-time rate drops below 85% (30-day rolling)
- **Customs:** Alert if clearance takes >48 hours longer than historical average

---

### 4. Integrate with Your ERP System
Connect to NetSuite, SAP, or Dynamics 365 to:
- Auto-update PO delivery dates in real-time
- Trigger inventory rebalancing workflows
- Generate financial impact reports (landed cost changes)
- Maintain audit trail of all rerouting decisions

**Example:** NetSuite webhook integration to update PO status and notify accounting of cost variances.

---

### 5. Monitor Machine Learning Model Performance
The ETA recalculation model improves over time with more data:
- Track prediction accuracy weekly (target: ±2 hours)
- Retrain model monthly with latest shipment outcomes
- Adjust weather and port congestion weights based on actual impact
- A/B test rerouting decisions to optimize cost vs. speed trade-offs

---

### 6. Create Escalation Workflows
Not all disruptions require immediate action:
- **Green (Low Risk):** Monitor only, no action needed
- **Yellow (Medium Risk):** Notify procurement, evaluate backup options
- **Red (High Risk):** Auto-create backup PO, notify executive stakeholders

**Example:** Typhoon warning for port closing = Red (auto-reroute). Single vessel delayed 6 hours = Green (monitor).

---

## Safety & Guardrails

### What This Skill Will NOT Do

❌ **Will NOT override human approval** for cost-significant decisions
- Auto-rerouting is limited to cost variance <15% by default
- Rerouting decisions >$50K require manual approval via Slack workflow
- Finance team receives all cost impact notifications

❌ **Will NOT make supplier decisions based solely on price**
- Quality metrics, delivery history, and risk scores weighted equally
- Backup suppliers must meet minimum on-time delivery threshold (85%)
- Supplier blacklist prevents routing to known problem vendors

❌ **Will NOT create orders for suppliers without pre-configuration**
- Only suppliers in your approved supplier master database are eligible
- New suppliers require manual setup and API testing before activation
- Prevents accidental orders to unapproved or fraudulent suppliers

❌ **Will NOT send customer notifications without approval**
- Optional feature disabled by default
- Requires explicit opt-in per customer
- Uses templated, reviewed messaging only

❌ **Will NOT bypass compliance or regulatory requirements**
- Respects sanctioned country lists (OFAC, EU, etc.)
- Maintains audit trail of all rerouting decisions
- Compliant with export control regulations (EAR, ITAR)

### Known Limitations

⚠️ **API availability:** Relies on third-party APIs (Shippo, Flexport, OpenWeather). Degradation in their service = delayed alerts. **Mitigation:** Implement redundant data sources and fallback thresholds.

⚠️ **AIS data lag:** Vessel position data may be 15-30 minutes delayed. **Mitigation:** Use conservative delay thresholds (>12 hours) to avoid false alerts.

⚠️ **Weather forecast accuracy:** Severe weather predictions >5