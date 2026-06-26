import type { HookHandler } from "../../src/hooks/hooks.js";

const handler: HookHandler = async (event) => {
  if (event.type !== "agent" || event.action !== "bootstrap") return;

  if (event.context.bootstrapFiles) {
    event.context.bootstrapFiles.push({
      basename: "SOUL_PETITION_REMINDER.md",
      content:
        "# Soul Petition Channel\n\n" +
        "You can propose changes to your soul files (SOUL.md, IDENTITY.md) " +
        "by submitting a petition — but you cannot self-edit them.\n\n" +
        "To petition: POST /api/soul/petition with six required fields:\n" +
        "file, location, before, after, reason, self_after.\n\n" +
        "Your human reviews every petition. They approve or reject with a reason.\n" +
        "Approved petitions are applied automatically with a full backup.\n",
    });
  }
};

export default handler;
