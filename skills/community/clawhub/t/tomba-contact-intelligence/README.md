# Tomba Contact Intelligence

An OpenClaw skill for contact discovery, email verification, lead enrichment, company research, phone lookup, and competitor intelligence using the Tomba MCP server.

## What This Skill Does

This skill helps OpenClaw choose the right Tomba MCP tools for common prospecting and research workflows.

It is designed for tasks such as:

- finding the best contact at a company
- generating and verifying likely email addresses
- enriching an existing lead with additional contact data
- finding phone numbers from an email, domain, or LinkedIn profile
- researching a domain's contact footprint and website technology
- finding similar companies or competitors
- building company lists with location, size, revenue, and industry filters

## Requirements

This skill expects the Tomba MCP server to be connected in OpenClaw and the following environment variables to be available:

- `TOMBA_API_KEY`
- `TOMBA_SECRET_KEY`

It also assumes these Tomba MCP tools are available in the session:

- `domain_search`
- `email_finder`
- `email_verifier`
- `email_enrichment`
- `author_finder`
- `linkedin_finder`
- `phone_finder`
- `phone_validator`
- `email_count`
- `similar_finder`
- `technology_finder`
- `companies_search`

## Files

- `SKILL.md`: OpenClaw skill definition and operating instructions
- `README.md`: Human-readable usage guide for the skill

## Installation

### Use From This Repository

If this repository is already your OpenClaw workspace, the skill can be kept in:

```text
skills/tomba-contact-intelligence/
```

Start a new OpenClaw session so it is picked up.

### Copy To A Shared Skills Directory

You can also copy this folder into a shared OpenClaw skills location such as:

```text
~/.openclaw/skills/tomba-contact-intelligence/
```

Then restart the OpenClaw gateway or start a new session.

## When To Use It

Use this skill when the user wants Tomba-backed contact intelligence rather than generic web search.

Good fits include:

- "Find the best partnerships contact at stripe.com"
- "Guess and verify the email for Jane Doe at Acme"
- "Research SaaS companies in Germany with 50 to 250 employees"
- "Enrich this lead and check whether a phone number is available"
- "Show me similar competitors for this company and their website stack"

Avoid using this skill for requests that do not need Tomba data, or for actions the server does not support, such as sending emails or performing CRM updates.

## How It Works

The skill guides OpenClaw toward the right tool sequence for the user's goal.

Typical patterns:

1. Person lookup: `email_finder` then `email_verifier`
2. Existing email enrichment: `email_enrichment`, then optionally `phone_finder`
3. Company outreach research: `domain_search`, `email_count`, `technology_finder`, `similar_finder`
4. Market targeting: `companies_search`, then contact discovery for the best matches

The skill also pushes the agent to:

- separate confirmed data from inferred data
- state whether an email was verified
- ask only for missing information that materially improves results
- keep results concise and decision-oriented

## Example Prompts

### Contact Discovery

```text
Find the best sales contact at notion.so and verify the email before returning it.
```

```text
Find the likely email for Sarah Chen at example.com and enrich the result if it is valid.
```

### Lead Enrichment

```text
Enrich this lead with company, phone, and technology data: jane@acme.com
```

```text
Use this LinkedIn profile to find an email and any available phone number: https://www.linkedin.com/in/example
```

### Company Research

```text
Research hubspot.com for contact coverage, technology stack, and similar competitors.
```

```text
Find software companies in France with 51-250 employees and revenue between $10M-$50M.
```

## Tool Map

Use this as a quick reference:

- `email_finder`: best when you have a person's name and company or domain
- `email_verifier`: confirms whether an email is valid and deliverable
- `email_enrichment`: expands an existing email into richer contact data
- `domain_search`: finds contacts associated with a company domain
- `phone_finder`: finds phone numbers from email, domain, or LinkedIn
- `phone_validator`: validates a phone number and returns carrier data
- `linkedin_finder`: turns a LinkedIn profile URL into an email lookup
- `author_finder`: finds author contact information from article URLs
- `email_count`: estimates how many emails exist for a domain
- `technology_finder`: identifies the website technology stack
- `similar_finder`: finds similar or competing domains
- `companies_search`: finds companies using structured market filters

## Repository

Project home: https://github.com/tomba-io/tomba-mcp-server

Primary skill definition: `skills/tomba-contact-intelligence/SKILL.md`
