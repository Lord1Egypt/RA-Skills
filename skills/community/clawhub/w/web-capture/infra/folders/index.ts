import { defineFolder } from "@cargo-ai/cdk";

// Every resource this cookbook deploys is filed under a folder named after the
// cookbook, not under a shared "GTM" one.
//
// The reason is provenance. A workspace accumulates resources from several
// cookbooks plus whatever the team wrote by hand, and six months later the
// only question that matters about an agent nobody recognises is "what put
// this here, and what else came with it". A folder per cookbook answers that
// by looking; a shared folder makes it an archaeology exercise across the
// repo. It is also what makes removing a cookbook a bounded operation rather
// than a hunt.
//
// Folders are per-kind, and this cookbook deploys one agent, so one folder.
export const agentsFolder = defineFolder("web_capture_agents", {
  kind: "agent",
  name: "Web capture",
});
