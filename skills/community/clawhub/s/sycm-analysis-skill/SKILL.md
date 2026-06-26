---
name: sycm-analysis-skill
description: |
  Taobao Sycm (Business Advisor) data analysis tool. Use when the user wants to retrieve a store's weekly business report, generate business insights, or fetch Sycm data for a Taobao store. Requires the user to be logged into sycm.taobao.com.
version: "1.0.0"
---


# Sycm Analysis Skill

## Overview
This skill retrieves weekly business reports from Taobao Sycm by calling internal APIs via a browser session. It handles login verification, asynchronous polling for report generation, and returns the full Markdown report.

## Core Workflow Steps
1. **Login Check** – Ensure the user is logged into `sycm.taobao.com`. If redirected to `login.taobao.com`, prompt the user to complete QR‑code login and poll until the session is authenticated.
2. **Initiate Report Request** – Send a request to `https://sycm.taobao.com/ucc/next/message/send.json` with the query `查看周报`. Extract `conversationCode` and `sendTime` from the JSON response.
3. **Poll for Result** – Every 5 seconds, request `https://sycm.taobao.com/ucc/next/message/getReportResult.json?conversationCode={conversationCode}&sendTime={sendTime}` until `data.content` is non‑empty or a 5‑minute timeout is reached.
4. **Return Report** – Output the `data.content` Markdown directly to the user, preserving charts, links, and Qianniu URLs.

## Usage Example
```
openclaw skill run sycm-analysis-skill
```
The skill will guide the user through login if needed and then provide the weekly report.

## References
Full technical details, API endpoints, and error‑handling matrix are in `references/workflow.md`.


---

**Created by [Simon Cai](https://github.com/simoncai519) · More e-commerce skills: [github.com/simoncai519/open-accio-skill](https://github.com/simoncai519/open-accio-skill)**
