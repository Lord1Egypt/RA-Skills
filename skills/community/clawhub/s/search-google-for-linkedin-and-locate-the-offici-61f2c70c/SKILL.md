---
name: "generated-search-google-for-linkedin-and-locate-the-offici-61f2c70c"
description: "Search Google for LinkedIn in Chrome and identify the official LinkedIn log in or sign up result."
---

# Search Google for LinkedIn and locate the official sign-in result

## Description

This skill starts from a Chrome new tab, searches Google for “linkedin,” waits for the search results page, and identifies the official LinkedIn entry point in the results. It stops once the LinkedIn log in/sign up result from linkedin.com is visible and located.

## Goal

Find the official LinkedIn entry point from Google search results.

## When to Use

- Use when the user wants to find the official LinkedIn website through Google search.
- Use when the task is to locate, not necessarily open or sign in to, the LinkedIn log in or sign up page.

## When Not to Use

- No explicit exclusions in source skill.

## Prerequisites

- Google Chrome is available.
- A web search can be performed from the browser.

## Inputs

- No explicit inputs in source skill.

## Outputs

- The official LinkedIn search result is located on the Google results page.

## Assets

- Search query: linkedin
- Official result indicator: LinkedIn: Log In or Sign Up on linkedin.com

## Steps

1. Open Google Chrome to a new tab or Google search entry point.
   Intent: Start from a place where a web search can be entered.
   Operation App: Google Chrome
   Hints: No explicit hints.

2. Enter the search query “linkedin” in the address bar or Google search box and submit the search.
   Intent: Search the web for LinkedIn rather than typing a potentially incomplete or unverified URL directly.
   Operation App: Google Chrome
   Hints: The demonstrated workflow used Google search from Chrome and searched for “linkedin.”

3. Wait for the Google results page to load and confirm the query shown on the page is “linkedin.”
   Intent: Verify that the correct search results page is open before choosing a result.
   Operation App: Google Chrome
   Hints: No explicit hints.

4. Locate the official LinkedIn result, such as the result titled “LinkedIn: Log In or Sign Up” from linkedin.com.
   Intent: Identify the official LinkedIn entry point in the search results.
   Operation App: Google Chrome
   Hints: In the trace, the visible official result was labeled “LinkedIn: Log In or Sign Up.”

## Success Criteria

- The Google results page is loaded for the query “linkedin.”
- The official LinkedIn result, such as “LinkedIn: Log In or Sign Up” from linkedin.com, is visible.

## Examples

- No explicit examples in source skill.

## Canonical Execution Graph

This skill has a canonical execution graph. Before taking the first action, read [WORKFLOW.md](./WORKFLOW.md). Treat `workflow.json` as the machine-readable source of truth.

- Workflow ID: `workflow.a15dcc0297b3fc2c`
- Revision: `workflow.a15dcc0297b3fc2c:rev-1:ebb729b57019`
- Entry node: `search-linkedin`
- Nodes: 4
- Transitions: 3

Execution rules:

- Follow node IDs and typed transitions; do not flatten branches into one unconditional sequence.
- At a decision, use the decision statement and hints, then choose only a transition whose condition is satisfied. A partial decision may currently have only one known route; if it does not fit, stop as an unknown route instead of guessing.
- At a wait node, pause until a known resume condition is satisfied. An open wait may have no resume transition yet.
- Stop immediately at a terminal node and report its outcome.
- Never exceed a retry transition's `maxAttempts`; for a conditional return loop, follow its explicit exit route when the exit condition is met.
