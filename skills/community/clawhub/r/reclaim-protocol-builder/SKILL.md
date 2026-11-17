---
name: reclaim-protocol-builder
description: Integrate Reclaim Protocol verification of data from online accounts, author verification providers, and investigate verification sessions with the Reclaim Builder MCP.
version: 0.1.0
license: MIT-0
metadata:
  openclaw:
    homepage: https://build.reclaimprotocol.org
    requires:
      bins:
        - node
        - npx
---

# Reclaim Protocol Builder

Use this skill when a developer wants an app or workflow to verify a claim using a person's online account: enrollment, employment, account ownership, purchases, or another data point supported by a Reclaim provider. A provider describes how a source site supplies evidence; a verification session is the account holder's individual verification attempt. Confirm that a suitable provider exists before promising a particular claim can be verified.

## Connect the tools

The tools come from the published `@reclaimprotocol/agent` npm package. They run locally over MCP stdio and require Node.js 22.12 or newer. This skill supplies instructions; installing it alone does not connect the MCP server.

If Reclaim tools are unavailable, have the operator add the server through OpenClaw Settings → MCP with command `npx` and arguments `-y`, `--package=@reclaimprotocol/agent`, `reclaim-mcp-server`. Alternatively, with their permission, use:

```bash
openclaw mcp add reclaim --command npx --arg=-y --arg=--package=@reclaimprotocol/agent --arg=reclaim-mcp-server
openclaw mcp doctor reclaim --probe
```

Check the tool catalog after connection. Respect the operator's installation and tool permissions. If setup is denied, explain the remaining setup step and stop that action.

## Work on the request

For a new product integration, invoke `start_integration` with the intended claim and application context, using the tool's current schema. Apply the resulting guidance to the application and implement the verification result handling it describes.

For provider authoring or repair, open `how_it_works` to discover the available documentation topics, then request the relevant topics and follow their instructions. Use the server's provider search and inspection tools to establish whether the source and claim are supported.

For an existing session, inspect it with `get_verification_session`. Use `list_verification_events` to investigate progress and `list_verification_deliveries` to inspect callback delivery. State the observed status and the next corrective step. A pending or failed session is not evidence that the claim was verified.

Account holders complete their own sign-in and consent. Use the server's documented credential setup for organization operations; never request passwords, private keys, or organization keys in chat, and never display stored credentials. Verify the callback or proof on the server as directed by the integration tools before granting access or benefits.

## Account and support

Private organization operations require a Reclaim account and the appropriate permissions. Reclaim account plan limits and service charges are separate from this free skill; check the Builder account before starting paid operations.

Product: https://build.reclaimprotocol.org

Public distribution and other clients: https://github.com/reclaimprotocol/developer-tools

OpenClaw MCP setup: https://docs.openclaw.ai/tools/mcp

Support: support@reclaimprotocol.org

This newly authored skill is licensed under MIT-0. The linked npm software and other repository content retain their respective licenses.
