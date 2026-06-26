# Telegram Marketing Audit Command Handler Skill

## Purpose
Handles the Telegram `/marketing_audit` command by triggering the Marketing Orchestrator skill with given input and replying with the final report.

## Telegram Command
- Command: `/marketing_audit`
- Args: `instagramHandle` (optional), `websiteDomain` (optional)

## Implementation
```javascript
module.exports = async function marketingAuditHandler(context) {
  const { instagramHandle, websiteDomain } = context.args;

  if (!instagramHandle && !websiteDomain) {
    await context.reply("Please provide an Instagram handle or website domain (or both).");
    return;
  }

  await context.reply("Starting marketing audit. This may take a few minutes...");

  try {
    const result = await context.callSkill("marketing-orchestrator", {
      instagramHandle,
      websiteDomain,
    });

    if (result && result.reportMarkdown) {
      await context.reply(result.reportMarkdown);
    } else {
      await context.reply("Audit completed but no report was generated.");
    }
  } catch (err) {
    await context.reply("Error during marketing audit: " + err.message);
  }
};
```

## Notes
- Add this skill folder to OpenClaw skills directory.
- Register a Telegram slash command `/marketing_audit` that uses this skill as the handler via OpenClaw config or ClawHub.
- Ensure environment variables for collectors (API keys) are set.
