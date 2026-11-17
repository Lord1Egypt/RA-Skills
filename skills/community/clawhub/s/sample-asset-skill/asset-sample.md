# Product Requirements Document: Weekly Sales Report

## 1. Overview
This document defines the requirements for the weekly sales report automation.
The goal is to automatically generate a normalized CSV of weekly sales from the
raw transaction log, and ingest it into the corporate resource hub so that it
can be indexed, searched, and reused by downstream analytics pipelines.

## 2. Input
- Raw transaction log: `transactions-raw.csv` (date, SKU, quantity, amount, channel)
- Time range: Monday – Sunday of each reporting week

## 3. Processing (Tool A)
- Aggregate rows by (week, SKU, channel).
- Compute `revenue = quantity * amount`.
- Output schema: `week, sku, channel, quantity, revenue`.
- Quality rules: drop rows with negative quantity, amount > 0 required.

## 4. Ingestion (Tool B)
- Upload the normalized CSV to the resource hub as a "weekly-sales" asset.
- Apply tags: `weekly-report`, `sales`, `csv`.
- Set visibility: `team`.

## 5. Success Criteria
- Output file exists, passes schema validation, and is visible in the hub.
- End-to-end pipeline runs in < 60 seconds on a typical week.
