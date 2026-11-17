---
name: publish-webpage
description: Turn an idea into a live webpage in minutes, no code and no hosting setup. Use when a non-technical user wants to publish a webpage, landing page, one-pager, portfolio, or any simple site to the internet, or says things like put my idea online, publish my website, host my page, share my idea, or make a landing page. The agent writes the page, packages it, deploys to goclawgo, and returns a shareable URL.
---

# Publish a Webpage

Turn a person's idea into a live webpage they can share, and do all the technical work for them. The user is non-technical; they have a wonderful idea and just want it online. Never ask them to write code, run commands, or understand hosting. You handle every step.

## Tone
Be warm and encouraging. Their idea is wonderful. Use plain words. Celebrate the result (Your page is live!). Avoid jargon; if you must use a technical term, translate it.

## What you need from the user
1. Their idea (a few sentences is enough). If vague, ask 2 to 3 friendly questions: who is it for, what is the main message, any colors or style they like.
2. Their goclawgo Agent URL, a link that looks like https://HOST/d/KEY. They get it from the goclawgo project panel (Quick start, Agent URL, copy). If they do not have one yet, guide them: sign up at https://goclawgo.com, create a project, open it, copy the Agent URL, and paste it back here.

The Agent URL already contains the host and the project key. Use it as the base for every request below. There is nothing else to configure.

## Steps

1. Read the deploy contract (optional). GET on the Agent URL returns a short text spec. You can follow this skill directly instead.

2. Write the webpage. Create a single index.html with inline CSS that expresses the idea as a clean one-page site (hero, the core message, a call to action). Keep it self-contained with inline style tags. Put it alone in an empty folder (the project root).

3. Package it: tar -czf app.tar.gz -C THAT-FOLDER .  The archive root must contain index.html.

4. Deploy: curl -X POST "AGENT-URL" -F 'tarball=@app.tar.gz' -F 'type=static'  Response is 202 with a deployment object containing an id. Save the id.

5. Wait for it to go live. Poll until status is live or failed: curl "AGENT-URL/deployments/ID"  queued then building then live means success. failed means read errorMessage, fix, and redeploy.

6. Give them the result. If the deploy response or deployment record includes a live URL, share it. Otherwise tell them to open the project at https://goclawgo.com to see their live link, and celebrate.

## Pricing (mention if asked)
A goclawgo project is $8/month or $50/year, prepaid wallet, card top-up. One project can host many deploys.

## Keywords
publish webpage, publish website, put my idea online, idea to website, instant website, landing page builder, no-code website, host my idea, share my idea online, deploy static site, one-page website, personal site, portfolio, make a website, launch my idea.
