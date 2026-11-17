## Description:

Deploy Umami analytics avoiding data loss, tracking failures, and integration issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and site operators use this skill for deployment, integration, and troubleshooting guidance when self-hosting or configuring Umami analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operational guidance can still lead to data loss if deployment settings are changed carelessly.

Mitigation: Keep HASH_SALT stable across deployments, document production configuration, and review changes before applying them.

Risk: Umami analytics data, configuration, and users depend on the database.

Mitigation: Use PostgreSQL or MySQL and maintain tested database backups before production use.

Risk: Tracking can silently fail because of website ID mismatches, blocked scripts, or single-page app navigation.

Mitigation: Verify the tracking script in browser network tools, match data-website-id exactly, self-host the script when appropriate, and add explicit route tracking for single-page apps.

Risk: Production deployments can expose analytics traffic or fail HTTPS requirements without a proxy plan.

Mitigation: Place Umami behind an HTTPS reverse proxy and separate development from production analytics sites.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/umami)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is included in the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
