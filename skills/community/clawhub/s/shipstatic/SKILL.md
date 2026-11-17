---
name: publish-online
description: Publish a site, page, report, dashboard, slide deck, document, portfolio or small web app at a ShipStatic link anyone can open, with no account needed and optional built-in password protection. Use when the user asks to publish something, deploy or host a static site or a build folder, put it online, or get a link others can open. Not for HTML the user only wants to see, download or keep as a file.
---

# Publish online

Publish when the user has asked for something to be online. If they want to
see a draft first, show it and publish when they say so.

**Publishing needs no account.** Don't ask the user to sign in, connect
anything, create an account or give a key before publishing. Most sites are
published with no account, and that is the normal way, not a fallback.

## Talk to the user in plain words

Many people who publish with ShipStatic aren't developers. They made
something, often with your help, and they want a link they can share.

- Do the technical work yourself. Tell the user what happened, not how you
  did it. Ask them only for what you can't decide for them, such as a
  password or which version to keep.
- Use their words: their site, page, link and password. Don't say deploy,
  build, CLI, MCP, static, server, Node.js or token unless the user said it
  first, or a step they have to do needs it.
- If something goes wrong, say in one or two short sentences what it means
  for them and what you'll do next. Don't paste error messages or logs.
- If the user has to do something, give one step at a time, with exactly
  where to click or what to type.

## Two separate questions

1. **How the files travel: you choose.** There are two ways, and both work
   with no account:
   - **The CLI:** `npx -y @shipstatic/ship@3 <folder> --json`, for a folder on
     disk.
   - **The upload:** the ShipStatic MCP server's `deployments_upload` tool,
     for files you send in the call.
2. **Where the site lands: the result tells you.** The user's setup decides
   it, and you don't check it first. With nothing set up, the site has no
   account. If the user has set up an account for the way you used, it goes
   into that account.

## Find what to publish

- **A project with a build step:** run its build, and once it succeeds,
  publish the folder it writes. Build first even when an older build folder is
  already there. If the build can't run or fails, don't write what it would
  make by hand, and don't publish the older folder: say the site isn't online
  yet and why, and give the user one step, such as running the build
  themselves.
- **A built site with nothing to build:** a folder with an `index.html` at the
  top, such as `dist/`, `build/` or `out/`. Publish that folder. If the user
  names a folder, publish that one as it is.
- **What you publish is a static site:** an `index.html` at the top of the
  folder, with the files it uses beside it. It's the page visitors see first,
  and a site without one is refused. If a build makes a server app
  instead (no `index.html`), don't publish it: say ShipStatic publishes sites
  that run in the browser, not apps that need their own server, and offer to
  change the project so it can be published that way. Don't change the
  project's settings without asking.
- **A single file that isn't a page,** like an image or a PDF: put it in a new
  folder with a small `index.html` that shows it or links to it, and publish
  that folder.
- **Something new to make:** make the files in a new folder of its own, with
  an `index.html` at the top. Never write them into an existing folder
  such as `dist/` or the project's own files: that overwrites the user's work
  and publishes files that don't belong to the new site.

## Make the files

- Make it as HTML, with CSS, JavaScript, images and fonts as needed. It runs in
  the browser. There is no server, so no backend code, database or server-side
  form handling.
- Put an `index.html` at the top of what you publish: it's the page visitors
  see first. Link pages and files to each other with relative paths.
- A report or a single page can be one `index.html` with its CSS and
  JavaScript inside it, unless the user wants separate files. Charts and
  tables can be drawn with inline SVG, HTML and CSS.
- Use only content the user gave you or that you can make yourself. Don't link
  to images or files at addresses you guessed.
- Don't publish passwords, keys, government ID numbers, health records or
  payment card numbers, even behind a password. Offer a version with those
  left out or replaced by made-up examples.

## Publish

Choose the way:

- **A shell with Node.js 20.19 or newer: the CLI.** It reads the files from
  disk, so nothing passes through the conversation.
- **The CLI can't run** (no shell, no Node.js, or the shell can't reach npm
  or ShipStatic) **and the files
  are few and small: the upload.** Send text files (HTML, CSS, JavaScript,
  JSON, SVG) as plain text, and binary files such as images and fonts with
  `encoding: "base64"`.
- **A large build the CLI can't send:** never read it into the conversation.
  Ask the user to let the CLI reach the internet, or tell them what is
  missing (Node.js for the CLI, or the ShipStatic MCP server for the upload)
  and how to add it, one step at a time.

Then:

- Publish straight away. Before publishing, don't call `whoami` or any other
  ShipStatic tool, don't run `ship whoami` or `ship config`, don't add
  `--token`, and don't start a sign-in, unless the user asked to publish into
  their account; the last section says how.
- Publish all the files of a version at once.
- Don't set an expiry (`ttl`) or a domain unless the user asks for one. Both
  need an account.
- If the user wants it private or behind a password, use ShipStatic's built-in
  password protection: `--password <password>` on the CLI, or `password` on
  the upload. It works with no account, and it is checked before any file is
  served. Don't build a password page or script into the site. Make up a new
  password that is hard to guess, of letters and numbers only, unless the
  user chose one. Never ask for a password the user already uses somewhere
  else.
- Pass the folder and the password to the CLI as single literal arguments
  for the shell you use, so nothing in them is expanded or run. Never show
  the user a command line with the password in it.
- If the CLI fails with `authentication_failed`, the key it used was refused.
  Tell the user their saved ShipStatic key didn't work, and how to replace it
  with a new key from
  https://my.shipstatic.com/api-key, where it is set: in `SHIP_TOKEN` if that
  is set (it comes first), otherwise by running
  `npx -y @shipstatic/ship@3 config`. Then stop: don't publish another way,
  with no account or through the upload, unless the user asks. Another way can
  put the site in another account, or in none.
- If publishing fails otherwise, read the message and tell the user in plain
  words what went wrong. Fix what you can, for example a file type that
  isn't allowed, files that are too large, or a project folder where its
  build folder was meant, and publish once more.
- If a publish ends with no result, tell the user, and check whether the
  site went up before you publish again. Don't switch to the other way: each
  publish makes a new site.

## Tell the user

Both ways return the same fields for a published site. Read them; never
decide from whether you are connected, or from which way you used. (A domain
request returns the domain instead: report its `status` as it is.)

The `claim` link says who owns the site, and `expires` says whether it
expires.

- **The result has a `claim` link** (the usual case): the site has no account.
  Give the link (`url`), say it stays up for 3 days, and give the claim link:
  opening it and signing in keeps the site for good. The claim link is for
  the user alone, since whoever opens it and signs in owns the site, so never
  put it in the site or share it anywhere else. For example:

  > Your site is live: https://example-site-abc1234.shipstatic.com
  > It stays up for 3 days. To keep it, open
  > https://my.shipstatic.com/claim/… and sign in.

- **The result has no `claim` link:** the site is already in the user's
  ShipStatic account. Give the link. If `expires` is not null, say when it
  expires; if it is null, it stays until they delete it. The result doesn't
  say which account, so don't guess.
- **The result has `password: true`:** the site asks for a password before
  showing anything. Say so, and give the password if you set one: a password
  the user never sees locks them out.

Keep the reply short. The links matter more than a summary of the files.

## When the user wants changes

Something published doesn't change. To change it, publish again: the user gets
a new link, and the earlier one keeps working until it expires. Say which link
is the new one, and that the claim link of the version they want to keep is
the one to open.

## When to decline

If the request needs a server (an API, a database, sign-in for the people who
open the link), say that ShipStatic publishes sites that run in the browser,
and that this part needs a server it doesn't run. Offer a version that works
without one, if one would do the job.

## Accounts, only when the user asks

Bring up an account only when the user asks to see or manage what they have
published, to use their own domain, or to publish into their account. The two
ways are set up separately:

- **A site already published with no account** moves into the user's account
  through its claim link, whichever way it was sent.
- **The upload** goes into an account once the ShipStatic MCP server is
  connected to one. The host asks the user to sign in when an account tool is
  first used. If an account tool is refused and no sign-in starts, the user
  can see and manage their sites at https://my.shipstatic.com.
- **The CLI** publishes into an account once the user runs
  `npx -y @shipstatic/ship@3 config`, with an API key from
  https://my.shipstatic.com/api-key.

When the user asks to publish into their account, use a way that is set up
for it, and check which one is before publishing. If neither is, help them
set one up first, and never guess that the two ways share an account.
