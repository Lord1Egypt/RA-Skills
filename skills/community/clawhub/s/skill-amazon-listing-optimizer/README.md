# skill-amazon-listing-optimizer

> **OpenClaw Agent Skill** — Automatically detect, fix, and re-upload non-square Amazon product listing images via SP-API. No Seller Central. No manual work. Just run and it's done.

---

## The Problem

Amazon penalizes listings with non-square or low-resolution images — lower ranking, suppressed buy box, reduced conversion. Common issues:
- 16:9 landscape shots (2560×1440)
- 4:3 product photography (2560×1920)
- Portrait images (305×518)
- Sub-1000px anything

Fixing them manually means downloading, editing in Photoshop, re-uploading through Seller Central — for every single slot, every product.

**This skill does it in one command.**

---

## What It Does

| Script | What it does |
|--------|-------------|
| `audit.js` | Scans all your listing image slots, flags non-square and undersized images |
| `pad_to_square.py` | Pads flagged images to 2000×2000 white background (Amazon standard) |
| `push_images.js` | Serves fixed images via HTTP, submits URLs to SP-API, auto-closes after Amazon crawls |

---

## Quick Start

```bash
# 1. Install dependencies
npm install amazon-sp-api
pip3 install Pillow

# 2. Set up SP-API credentials (see skill-amazon-spapi)
export AMAZON_SPAPI_PATH=./amazon-sp-api.json

# 3. Full pipeline — audit, fix, push
node scripts/audit.js --all --out report.json
python3 scripts/pad_to_square.py ./image_fix/
node scripts/push_images.js --dir ./image_fix/ --from-report report.json
```

Amazon processes updates within **15–30 minutes**.

---

## Step by Step

### Step 1 — Audit
```bash
node scripts/audit.js --all
```
```
🔍 Auditing 5 SKUs...

  SKU-001... ✅ all images OK
  SKU-002... ⚠️  2 issue(s)
    [PT03] 2560x1920 (non-square)
    [PT05] 2560x1440 (non-square)
  SKU-003... ⚠️  1 issue(s)
    [PT06] 305x518 (non-square, too small)

📊 Summary: 2/5 SKUs have image issues
```

### Step 2 — Fix
```bash
python3 scripts/pad_to_square.py ./image_fix/
```
```
Processing 3 images...

  ✅ SKU-002_PT03_orig.jpg (2560x1920) → SKU-002_PT03_fixed.jpg (2000x2000)
  ✅ SKU-002_PT05_orig.jpg (2560x1440) → SKU-002_PT05_fixed.jpg (2000x2000)
  ✅ SKU-003_PT06_orig.jpg (305x518)   → SKU-003_PT06_fixed.jpg (2000x2000)
```

### Step 3 — Push
```bash
node scripts/push_images.js --dir ./image_fix/ --from-report report.json
```
```
🚀 Amazon Listing Image Pusher
📡 Serving images at http://YOUR.IP:8899

  SKU-002 [PT03] ... ✅ ACCEPTED
  SKU-002 [PT05] ... ✅ ACCEPTED
  SKU-003 [PT06] ... ✅ ACCEPTED

✅ 3/3 patches accepted
⏳ Keeping server alive 15 mins for Amazon to crawl...
🔒 Server closed. Done.
```

---

## Image Slot Reference

| Slot | Description |
|------|-------------|
| `MAIN` | Hero image — must be white background |
| `PT01`–`PT08` | Secondary images |

---

## Requirements

- Python 3 + Pillow (`pip3 install Pillow`)
- Node.js + `amazon-sp-api` (`npm install amazon-sp-api`)
- SP-API credentials with `listingsItems` write permission
- VPS/server with a publicly accessible IP and open port (default: 8899)

---

## Part of the Zero2AI Skill Library

Built and battle-tested in production. Part of a growing open-source library of AI agent skills for e-commerce automation.

- 🔗 [skill-amazon-spapi](https://github.com/Zero2Ai-hub/skill-amazon-spapi) — Core SP-API auth & orders
- 🔗 [skill-amazon-ads-optimizer](https://github.com/Zero2Ai-hub/skill-amazon-ads-optimizer) — Campaign & bid management

---

**Built by [Zero2AI](https://zeerotoai.com) · Published on [ClawHub](https://clawhub.ai)**
