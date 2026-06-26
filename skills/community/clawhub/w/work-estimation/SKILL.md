---
name: work-estimation-en
description: |
  Software Development Work Estimation Skill. Triggered when user mentions "work estimation", "project estimation", "effort estimation", "timeline assessment", "task breakdown", "man-hour calculation", "development cycle", or similar terms.
  Accepts user requirements text or documents, automatically breaks down work items and estimates effort, outputting Excel evaluation reports.
version: 1.0.0
---

# 📊 Software Development Work Estimation

Automatically analyze user requirements, break them into specific work items, and estimate effort across multiple dimensions, outputting structured Excel reports.

## Workflow

### Step 1: Collect Requirements

User provides:
- Requirements description (plain text)
- Or requirements document path (supports .md, .docx, .txt formats)

### Step 2: AI Requirements Breakdown

AI automatically:
1. Analyzes requirement content
2. Breaks down into specific work modules
3. Categorizes by dimension (Analysis, Design, Frontend, Backend, Algorithm, Testing)

### Step 3: Effort Estimation

For each work item, evaluate:
- Workload (man-days)
- Complexity (Low/Medium/High)
- Risk Level (Low/Medium/High)
- Parallel Feasibility
- Prerequisites

### Step 4: Generate Excel

Multi-sheet Excel report:
- Overview
- Dimension Details
- Gantt Chart (Project Progress)
- Key Risk Items
- Coordination Relations
- Cost Estimation

## Output Description

### Sheet 1: Overview

| Work Module | Analysis | Design | Frontend | Backend | Algorithm | Testing | Total |
|------------|----------|--------|----------|---------|-----------|--------|-------|
| Module A   | 1 day   | 2 days | 3 days  | 5 days | 1 day    | 2 days | 14 days |

### Sheet 2-7: Dimension Details

Work content, estimation basis, and estimated hours by dimension.

### Sheet 8: Gantt Chart

Visual display of parallel work, critical path, and milestones. **Automatically skips weekends and holidays**.

### Sheet 9: Key Risk Assessment

Items with high risk or uncertainty are listed separately with explanations and recommendations.

### Sheet 10: Coordination Relations

Dependencies between work items, prerequisites, and coordination matters.

### Sheet 11: Cost Estimation

Three parts:
- **Labor Cost**: Role × man-days × daily rate
- **Hardware/Software Cost**: Servers, domains, SSL, third-party services
- **Total Budget**: Includes 15% contingency buffer

## Estimation Reference

| Complexity | Frontend | Backend | Algorithm | Testing |
|------------|----------|---------|-----------|---------|
| Low        | 1-2 days | 1-3 days | 1-3 days | 0.5-1 day |
| Medium     | 3-5 days | 3-7 days | 3-7 days | 1-3 days  |
| High       | 5-10 days| 7-14 days| 7-14 days| 3-5 days  |

## Notes

- Estimation based on standard team config (1 frontend, 1 backend, 1 tester)
- Parallel work reduces calendar time, not man-hours
- Reserve 10-20% buffer for changes
- Adjust based on actual team situation

## Example

**User:** Help me estimate this project: Develop an e-commerce mini-app with user login, product display, shopping cart, and order payment

**AI:**
```
Got it! I'll help you with the work estimation.

Based on your requirements, I've broken them down into:

📦 **Work Modules**
1. User System (login, register, profile)
2. Product Module (list, detail, search)
3. Shopping Cart Module
4. Order Module
5. Payment Module
6. Infrastructure (routing, state management, API)

Generating detailed estimation report...
```
