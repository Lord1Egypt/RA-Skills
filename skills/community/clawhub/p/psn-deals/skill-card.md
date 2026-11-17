## Description:

PSN Assistant helps agents answer PlayStation Store deal, PS Plus, cross-region pricing, game rating, trophy guide, release calendar, and PSN status questions using public web sources across 10+ regions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jundonggit](https://clawhub.ai/user/jundonggit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find current PlayStation deals, PS Plus offerings, regional price comparisons, ratings, trophy guidance, release timing, and service status. It is useful for purchase decisions and deal reminders where users understand prices and availability may change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill checks public third-party gaming sites, so returned prices, ratings, availability, and service status can be stale or differ from official checkout pages.

Mitigation: Show source links and remind users to verify final prices, regional availability, and claim windows on PlayStation or the cited source before acting.

Risk: Generic trigger words such as "trophy" or "new release" may activate the skill unexpectedly.

Mitigation: Confirm the user's PlayStation intent before running broader deal, release, trophy, or status workflows when the request is ambiguous.

Risk: User-requested deal reminders can save watched deal details in memory/psn-watchlist.json.

Mitigation: Save watchlist entries only after an explicit reminder request and tell users they can review or delete the watchlist when they no longer want saved reminders.

Risk: Cross-region purchase advice can omit account, language, payment, tax, or policy constraints for a user's situation.

Mitigation: Include regional account caveats and treat converted prices as approximate, with final terms checked against the relevant regional store.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jundonggit/skills/psn-deals)
- [PlayStation Blog](https://blog.playstation.com/)
- [Push Square PS Plus games](https://www.pushsquare.com/guides/all-ps-plus-games)
- [PSDeals monthly games](https://psdeals.net/us-store/collection/monthly-games)
- [PSDeals US store](https://psdeals.net/us-store)
- [PSDeals Hong Kong store](https://psdeals.net/hk-store)
- [PSDeals Japan store](https://psdeals.net/jp-store)
- [PSDeals China store](https://psdeals.net/cn-store)
- [PlatPrices](https://platprices.com/)
- [PSNDeals](https://psndeals.com/)
- [Metacritic games](https://www.metacritic.com/game/)
- [OpenCritic games](https://opencritic.com/game/)
- [PlayStation Plus US](https://www.playstation.com/en-us/ps-plus/)
- [Push Square PS Plus Extra games](https://www.pushsquare.com/guides/all-ps-plus-extra-games)
- [Push Square PS Plus Premium games](https://www.pushsquare.com/guides/all-ps-plus-premium-games)
- [Push Square PS5 release dates](https://www.pushsquare.com/games/ps5/release-dates)
- [PSNProfiles guides](https://psnprofiles.com/guide/)
- [PlayStationTrophies guides](https://www.playstationtrophies.org/)
- [PlayStation Network status](https://status.playstation.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown responses with lists, tables, source links, and concise recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include time-sensitive prices, availability windows, regional caveats, and user-requested watchlist reminder details.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
