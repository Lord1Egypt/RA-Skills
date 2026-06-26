# Hosting Decision Guide

Use this file when deciding where the website should live.

## Default: Netlify

Choose Netlify by default when the user wants:
- a non-developer-friendly setup
- manual or API deploys without requiring Git
- the option to add GitHub later
- UI-managed environment variables
- easy serverless helpers for Notion-backed content or publish workflows

This is the best default for a Notion-managed website that may start simple and grow into:
- live blog/article endpoints
- webhook-triggered publish flows
- preview deploys
- helper APIs

Default operating pattern:
1. prepare site output locally
2. run the validator
3. deploy with `scripts/netlify_zip_deploy.py`
4. fall back to Netlify Drop only when a manual release is simpler

Netlify rule:
- if `NETLIFY_SITE_ID` is missing, create the site programmatically with the token and persist the returned site id and URLs
- persist non-secret deploy metadata to `.website-manager/deploy.json` by default

## When Cloudflare Pages fits better

Choose Cloudflare Pages when:
- the site is truly static
- the user already manages hosting and DNS in Cloudflare
- the team is comfortable with Wrangler and Cloudflare-specific workflows

## When to add GitHub

Add GitHub only if the user wants:
- change history
- collaborative reviews
- preview workflows
- a formal code backup

Do not force GitHub on solo non-technical operators.
