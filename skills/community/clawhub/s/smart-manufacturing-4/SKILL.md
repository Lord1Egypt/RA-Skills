---
name: Smart Manufacturing 4.0
slug: smart-manufacturing-4
description: "AI agent for Industry 4.0 smart manufacturing. Covers predictive maintenance, quality control, OEE optimization, digital twin simulation, production scheduling, and IoT sensor data analysis for factories."
version: "1.0.0"
author: ai-gaoqian
tags: ['manufacturing', 'industry-4.0', 'IoT', 'predictive-maintenance', 'quality-control']
category: Business
metadata:
  openclaw:
    requires: []
    interfaces: ["text-input", "file-input", "web-search", "data-analysis"]
    pricing:
      model: pay-per-use
      price: 0.50
      currency: USD
---
# Smart Manufacturing 4.0

## Overview
An intelligent agent skill for factory managers, process engineers, and industrial IoT teams implementing Industry 4.0 transformations.

## Capabilities

### 1. Predictive Maintenance
- Equipment failure prediction using vibration, temperature, and acoustic data
- Remaining Useful Life (RUL) estimation for critical assets
- Maintenance scheduling optimization (minimize downtime, maximize throughput)
- Spare parts inventory optimization
- Root cause analysis with fault tree and FMEA

### 2. Quality Control
- Statistical Process Control (SPC) with control chart generation
- Defect pattern recognition from production line data
- Six Sigma DMAIC project guidance
- First-pass yield and scrap rate analysis
- Measurement System Analysis (Gage R&R)

### 3. Production Optimization
- Overall Equipment Effectiveness (OEE) calculation and improvement
- Production scheduling with constraint-based optimization
- Line balancing and bottleneck analysis
- Changeover time reduction (SMED methodology)
- Capacity planning with what-if scenarios

### 4. Digital Twin
- Factory layout simulation and optimization
- Process digital twin creation from IoT data streams
- Energy consumption modeling and peak shaving
- Material flow simulation for logistics within plant

### 5. Compliance & Safety
- OSHA / ISO 45001 safety compliance checklist
- Machine safety risk assessment (ISO 13849)
- Environmental compliance monitoring (emissions, waste)
- Lockout/Tagout procedure generation

## Usage Examples
- "Predict failure probability for 50 CNC machines based on vibration data"
- "Calculate OEE for Assembly Line 3 and identify top 3 loss factors"
- "Optimize production schedule for 200 work orders across 15 machines"
- "Analyze defect patterns from last month's quality inspection data"
- "Generate FMEA for a new injection molding process"

## Data Sources
OPC-UA, MQTT, MTConnect, SAP MES, Siemens MindSphere, and standard CSV/JSON from PLCs.
