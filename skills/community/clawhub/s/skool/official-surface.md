# Official Surface - Skool

Use this file when the task depends on what Skool officially supports right now.

## Core Product Areas

- **Community**: members, posts, comments, DMs, moderation, and approvals live at the group level.
- **Classroom**: courses, folders, lessons, resources, and access rules live alongside the community.
- **Calendar**: events can be native Skool calls or external meeting links and should be treated as retention infrastructure.

## Native Controls That Change Operations

- Membership questions shape who applies and what data is captured before approval.
- Membership question answers can be reviewed before approval and exported later from the Members tab.
- Instant approval changes how much manual review the group needs.
- AutoDM can handle welcome or follow-up workflows without inventing unsupported bots.
- Level gating and course permissions control what members unlock and when.
- Group invites can be issued by share link, direct email, or bulk CSV import.
- Calendar supports native Skool Calls for all admins and Pro webinars for one-to-many sessions.

## Official Automation Surfaces

- **Zapier plugin**: official help content documents four core flows on Pro: paid-member info to CRM, membership-question answers to CRM, invite-a-member, and unlock-a-course.
- **Webhook plugin**: official help content describes off-platform invite automation and labels the feature developer-only.
- **Tracking plugins**: official help content documents Google Ads, Meta pixel, and Hyros integrations for attribution and retargeting.
- **Native product settings**: approval, invites, pricing, trials, affiliates, classroom access, and events often solve the need without extra tooling.

## Current Hard Boundaries

- Do not assume there is an official CLI unless live docs show one.
- Do not assume direct write endpoints are stable unless current docs or a verified integration contract show them.
- Do not normalize posting bots, comment bots, or DM bots outside supported Skool features.
- Do not suggest sharing Skool account credentials with third parties; official help explicitly warns creators not to share credentials.

## Plan and Feature Checks

- Verify whether the group is on Hobby or Pro before recommending plan-gated workflows.
- Re-check live docs before relying on webinars, advanced plugins, or newer automation surfaces.
- Confirm whether the workflow is for one group or several because URLs, approvals, and classroom access are group-specific.

## What To Verify Before Building

- exact group URL and admin permissions
- live plan and any beta or developer-only features
- whether the task is advisory or a real write
- whether Zapier or a webhook host is already approved
- whether the user wants official-only implementation boundaries
- whether the workflow is better served by invites, exports, tracking plugins, or native calendar instead of custom automation
