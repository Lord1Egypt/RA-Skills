---
name: vibecode
description: Build iPhone apps and web apps with Vibecode, then put them online, on the user's iPhone or in the App Store. Use when the user wants to build, make or create an app (an iPhone or iOS app, a mobile app, a game, a tracker, a website or a web app), change an app they built in Vibecode, check on a build, read an app's logs or code, deploy it, install it on their iPhone, or publish it to the App Store.
homepage: https://www.vibecodeapp.com/mcp
metadata:
  openclaw:
    emoji: "📱"
    homepage: https://www.vibecodeapp.com/mcp
    requires:
      bins: []
      env: []
---

# Vibecode

[Vibecode](https://www.vibecodeapp.com) builds native iPhone apps and web apps from a description. Vibecode's agent writes the app, builds it and tests it in the user's Vibecode account. This skill drives that work through Vibecode's remote MCP server, `https://api.vibecodeapp.com/mcp`. Every tool acts on the Vibecode account the user signed in with.

## Connect (once)

The tools come from Vibecode's MCP server. Sign-in is OAuth with the user's Vibecode account; no API key is stored.

```bash
openclaw mcp add vibecode --url https://api.vibecodeapp.com/mcp --transport streamable-http --auth oauth
openclaw mcp login vibecode
openclaw mcp probe vibecode
```

`login` prints a link: the user opens it, signs in to Vibecode (or creates an account with Google or Apple) and allows access. `probe` should then list the Vibecode tools. In a direct chat, the owner can also ask OpenClaw to connect Vibecode and get the sign-in link there. OpenClaw shows the tools with the server's prefix, such as `vibecode__create_app`.

If no Vibecode tools are available, give the user the three commands above instead of guessing.

## Building and changing
- To make a new app, call `create_app` with a clear brief: what the app is for, its screens, its look and anything the user asked for. Use platform `ios` for an iPhone app (the default; games, tools and trackers included) and `web` for a website or web app. Android-only apps aren't supported. A build usually takes about 10 minutes; a new app with a backend can take about 30.
- Write the brief like a product manager: the app's name, what it does, the 3 to 5 things a user can do, and the feel. Leave frameworks and file names to Vibecode's agent.
- To start from an existing app, `find_templates` searches Vibecode's public templates and `remix_app` copies one into the user's account.
- To change an app, call `edit_app`. If the agent is still working on that app, the change waits its turn and starts by itself.
- After either, call `wait_for_build` again and again until it reports the app is ready or the build stopped, then tell the user. Each call returns after a short wait with the build's stage, so a long build takes many calls; that's normal. `get_build_status` answers at once, without waiting.
- `show_app` and `get_handoff_links` give links to open the app in Vibecode on the web, in the Vibecode iPhone app, or to publish it from Vibecode.

## Following the agent
- `get_activity` shows what the agent did and why a build failed.
- `stop_build` stops the agent's current work and anything waiting behind it. Ask the user first.

## When something isn't working
- `get_logs` reads the app's logs: the workspace's while it runs, or the published backend's (`where: live`).
- `list_files` and `read_file` show the app's code. `.env` files can't be read, and keys in any output are hidden.
- `get_screenshot` shows the app's latest screenshot.

## Running commands
- `run_command` runs a bash command in the app's workspace, a Linux sandbox in the app's folder, and returns the output with the app's keys hidden. Use it to run tests, check versions, install a package or make a small fix. For a feature or a design change, use `edit_app`, so Vibecode's agent makes and tests it.
- On Free, `run_command` counts toward 50 a week and a command stops after 45 seconds. On paid plans a command can run up to 20 minutes: when the answer has status `running`, call `get_command_output` with the `project_id` and `command_id` until it returns an exit code, rather than running it again.
- `run_live_command` runs a command on the deployed app's live server (paid plans), with real users' data. It backs up the live database first. Run only what the user asked for.

## On the user's iPhone and in the App Store
- `connect_apple` returns the link where the user connects their Apple developer account. They type their Apple password only on that page, never in the chat.
- `install_on_iphone` builds the app signed for the user's own iPhone and returns the install link (or the link to register their iPhone first). Call it again to follow the build.
- `publish_to_app_store` submits the app to the App Store: an update for an app already there, or a first release, where Vibecode's agent makes the listing and the build. A first release needs a bundle id and a phone number for Apple's reviewers.
- `get_app_store_status` says whether the Apple account is connected, which iPhones are registered and where the app stands with Apple. Submitted is not approved: Apple reviews every release.

## Deploying
- `deploy_app` puts the app online: a web app's site, or the server behind an iPhone app. It never starts a charge: when deploying would start a trial or a charge, it returns a link instead, so pass that on. Then call `get_deployment` to see when it's live and at what address.
- `set_address` gives a web app its `name.vibecode.run` address or connects the user's own domain (it returns the DNS records to add). `set_web_password` turns password protection on or off; ask the user for the username and password.

## Versions and apps
- `list_versions` lists saved versions; `restore_version` brings an earlier one back as a new version (ask first), then `deploy_app` to put it live.
- `list_projects` finds the user's apps. Refer to apps by name; never show project ids to the user.
- `rename_app` and `duplicate_app` change only the app named. `delete_app` removes the app, and only Vibecode support can bring it back: use it only when the user asks, and confirm the app's name first.

## Account and credits
- `get_profile` names the connected account, its plan and its credits.
- A new account's first app build is free. After that, builds and changes use Vibecode credits. When a tool says the account needs a plan or more credits, pass on its link: plans and credits are managed on vibecodeapp.com, and nothing is sold in the chat.

## Links
- Vibecode MCP: https://www.vibecodeapp.com/mcp
- Setup guides: https://www.vibecodeapp.com/docs/guides/vibecode-mcp
- Source and issues: https://github.com/vibecode/vibecode
- Support: support@vibecodeapp.com
