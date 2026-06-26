# Sugar Finance Bot

## Overview

Sugar Finance Bot is a financial analysis tool designed for import/export food companies. It calculates the landed cost of shipments based on structured cost data.

This is useful for:
- supply chain finance teams
- import/export operations
- cost analysis and margin tracking

---

## What is Landed Cost?

Landed cost represents the total cost of a shipment including:

- product cost (invoice value)
- ocean or air freight
- cargo insurance
- customs duties
- MPF (Merchandise Processing Fee)
- HMF (Harbor Maintenance Fee)
- broker fees
- domestic transportation
- other import-related charges

---

## Tools

### get_shipment_record

Loads shipment data based on a shipment ID.

**Input:**
- shipment_id (string)

**Output:**
- structured shipment object including product and cost data

---

### calculate_landed_cost

Calculates total landed cost and unit economics.

**Input:**
- shipment (object)

**Output:**
- total landed cost
- cost per kg
- cost per unit

---

## Example

### Input

Shipment ID: