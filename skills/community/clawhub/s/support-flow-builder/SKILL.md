---
name: support-flow-builder
description: Turn ecommerce support policies, ticket patterns, and channel context into reusable support flows, agent playbooks, macros, bot handoff logic, and governance notes for CX leaders, support managers, and operations teams. Use when designing refund, return, delivery-delay, payment-failure, VIP escalation, or bot-to-human workflows without live helpdesk integrations.
---

# Support Flow Builder

## Overview

Use this skill to convert support-policy context and recurring ticket themes into a structured service workflow. It is designed for CX and ecommerce operations teams that need repeatable flows, safer answers, and faster onboarding.

This MVP is documentation-first. It does **not** connect to live helpdesks, edit production bots, or inspect real ticket systems. It applies a policy-grounded flow template and produces channel-ready outputs for review.

## Trigger

Use this skill when the user wants to:
- create or clean up a support flow for a common ticket type
- turn policies and rough ticket patterns into decision trees and agent playbooks
- generate macros or canned responses for email, chat, or marketplace messaging
- design bot handoff requirements and escalation logic
- identify policy gaps or governance risks in current support operations

### Example prompts
- "Build a refund flow for our ecommerce support team"
- "Create macros and escalation logic for delivery-delay tickets"
- "Turn our return policy into a live-chat playbook"
- "Design a bot-to-human handoff for payment failure cases"

## Workflow

1. Capture the support scenario, channels, and policy constraints.
2. Translate the request into decision points, required checks, and exception handling.
3. Build the core flow and define escalation boundaries.
4. Generate agent-facing macros and bot handoff fields.
5. Return a markdown pack that a CX manager can review and adapt.

## Inputs

The user can provide any mix of:
- ticket summaries or transcript snippets
- support policies, SLA notes, and approval rules
- target channels such as email, chat, marketplace IM, or call notes
- scenario goals, such as refund, return, delivery delay, payment failure, or VIP escalation
- team constraints, such as refund authority, warehouse dependencies, or multilingual support

## Outputs

Return a markdown pack with:
- intent summary
- support flow map
- agent playbook
- macros or canned responses
- bot handoff fields
- governance and QA notes
- knowledge gaps to document next

## Safety

- Do not invent policy authority the team has not provided.
- Mark sensitive, legal, fraud, or compensation-heavy cases for human review.
- Keep production automation changes out of scope.
- State clearly when policy gaps prevent a clean decision tree.

## Examples

### Example 1
Input: return policy notes and recent delivery-delay tickets.

Output: produce a flow map, escalation points, and copy-ready chat or email macros.

### Example 2
Input: payment-failure scenario for bot handoff design.

Output: define intake questions, required fields, escalation triggers, and agent response blocks.

## Acceptance Criteria

- Return markdown text.
- Include the flow, macro, and governance sections.
- Keep the output usable by managers and frontline agents.
- Flag policy gaps or sensitive-review points explicitly.
