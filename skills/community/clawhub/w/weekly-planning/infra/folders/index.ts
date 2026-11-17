import { defineFolder } from "@cargo-ai/cdk";

// Every resource this cookbook deploys is filed under a folder named after the
// cookbook, not under a shared "GTM" one.
//
// The reason is provenance. A workspace accumulates resources from several
// cookbooks plus whatever the team wrote by hand, and six months later the only
// question that matters about an agent nobody recognises is "what put this
// here, and what else came with it". A folder per cookbook answers that by
// looking; a shared folder makes it an archaeology exercise across the repo.
// It is also what makes removing a cookbook a bounded operation rather than a
// hunt.
export const agentsFolder = defineFolder("weekly_planning_agents", {
  kind: "agent",
  name: "Weekly planning",
});
