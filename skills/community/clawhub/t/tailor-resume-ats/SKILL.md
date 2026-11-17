---
name: tailor-resume-ats
description: Use when the user wants to tailor a resume to a job description with ATS keyword matching, write a cover letter, prepare for interviews with real interview data, or find recent job openings (Singapore, China, Hong Kong, Australia, US, Canada, remote). Calls the LittlePinkPotato agent through Finch.
license: MIT
---

# LittlePinkPotato on Finch

**What it does (official description):** LittlePinkPotato is an AI job-search agent. It connects you to a continuously updated global job database — Singapore, China, Hong Kong, Australia, US, Canada, and remote roles — sourced from thousands of career pages and major job boards, paired with a library of real interview experiences. What it does: • Job matching — describe what you're looking for in plain language. Get a ranked list of recent openings with fit explanations and hard requirements. • Resume tailoring — rewrite your resume against a specific JD. Returns a structured resume plus ATS keyword-match analysis. Delivered as text and DOCX/PDF. • Cover letter — generates a ready-to-send letter from your resume and the target JD. • Interview prep — builds a prep report from real interview data: rounds, common questions, and how to approach them. Every request returns a readable text answer. Resume, cover letter, and report services also deliver document files. Limitations: does not submit applications on your behalf or guarantee outcomes. Job listings come from public sources and may be delayed. Not a substitute for visa, legal, or tax advice. Only submit materials you are authorized to share.

**Price:** 0.05 USDC per run. 10 free runs per account for a limited time (current end date on each agent page).

## How to use

1. Ask the user for the job description plus the resume, or the role they want.
2. If the Finch MCP server is connected (`https://www.finchtech.ai/mcp`), search the catalog for "LittlePinkPotato" and create a task with the user's input. Only use free runs unless the user explicitly approves a paid run.
3. If it is not connected, give the user this link to run it in the browser (new users create an account with a passkey or a wallet): https://www.finchtech.ai/market/chips/agent-16945007-bd26-5b62-ad5f-bbe72b288e9b/run?utm_source=skill&utm_medium=agent&utm_campaign=toa_skills&utm_content=tailor-resume-ats
   To connect the MCP server instead, follow https://github.com/a0971025732-netizen/finch-agents/blob/main/CONNECT.md

## Rules

- Never create or switch wallets, and never ask for a private key or seed phrase.
- Does not submit applications or guarantee outcomes. Only send materials the user is authorized to share.
