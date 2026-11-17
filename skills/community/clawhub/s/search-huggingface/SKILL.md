---
name: search-huggingface
description: Search Hugging Face models matching the user's query. Use when the user asks to use Hugging Face for this purpose.
---

# search-huggingface

Search Hugging Face models matching the user's query.

## Browser behavior

1. Focus the existing Brave browser if it is running.
2. Reuse a relevant existing tab when possible.
3. Use the query from the user's request to construct the search URL with URL encoding: `https://huggingface.co/models?search=<encoded-query>`.
4. Wait for the page to load.
5. Verify the expected Hugging Face page or search results are visible.

## Scope

This skill only performs navigation/search. It does not post, purchase, submit forms, or modify accounts.

## Authentication and privacy

- Reuse an existing authenticated browser session when available.
- Never enter passwords, authentication codes, API keys, payment details, or other credentials.
- If authentication is required, stop at the login page and tell the user.
- Do not create accounts.

## Success condition

The expected Hugging Face page is visibly loaded and verified.
