# Weights and half-lives

Two numbers per signal type, in `infra/settings.ts`:

- **weight**: what the signal is worth on the day it lands, in the same unit as the thresholds.
- **half-life**: how many days until it is worth half that. After two half-lives it is worth a
  quarter, after three an eighth.

The score is the sum over the account's events:

```
weight × 0.5 ^ (age in days / half-life in days)
```

## How to choose them

- **Weight is intent.** Ask what the signal says about buying from you, not how rare it is. A demo
  request is someone asking; a round is money that will be spent on something; a job posting is a
  team being built.
- **Half-life is how long the signal stays true.** A demo request goes cold in weeks; a funded
  company spends its round over two or three quarters; a job posting is filled or dropped in a
  month. Profile views and post reactions are true for days.
- **Set the ready line in signals, not in points.** Decide "a fresh round alone is ready" or "two
  job postings and a demo request is ready", then set `readyThreshold` to that sum. The pilot
  distribution checks it.
- **Start with few types.** Three well-weighed types beat ten guessed ones. A type whose weight
  nobody can defend is deleted from `signals`, not set low: unknown types already weigh 0.

## Starting points

Defaults to propose, then correct with the operator. The key is the `signal_type` Cargo Signals
writes, or the model slug for a first-party event (read both from the inventory query in
[`run.md`](run.md#inventory)). Confirm each Cargo Signals key there before weighing it: most are
the feed's name in snake case, but not all (the competitor-relationships feed writes
`competitor_relationship_monitoring`), and a misspelled key weighs 0 without an error.

| Key                    | Source                               | Weight | Half-life (days) | Why                                                      |
| ---------------------- | ------------------------------------ | ------ | ---------------- | -------------------------------------------------------- |
| a demo-request model   | first party                          | 20     | 30               | Someone asked. The strongest signal there is             |
| a product-signup model | first party                          | 8      | 14               | Hands on the product, decays fast if nothing follows     |
| `fundraising`          | `listenFundraising`                  | 10     | 120              | Budget for months; the spend comes in the first quarters |
| `mergers_acquisitions` | `listenMergersAcquisitions`          | 6      | 90               | Systems get consolidated; a slower, larger project       |
| `job_offers`           | `listenJobOffers` (title-filtered)   | 4      | 21               | A team being built; the posting is filled or dropped     |
| `recruitment_campaign` | `listenRecruitmentCampaign`          | 5      | 30               | Hiring at volume: growth with money behind it            |
| `department_growth`    | `listenDepartmentGrowth`             | 4      | 45               | The team you sell to is growing                          |
| `tech_adoption`        | `listenTechAdoption`                 | 5      | 60               | They bought something that pairs with you                |
| `tech_displacement`    | `listenTechDisplacement`             | 7      | 45               | They are leaving something you replace                   |
| a web-sessions model   | first party (visitor-identification) | 1      | 7                | Noisy alone; adds up only when it repeats                |

Example from a sales team that scored this way before: profile views counted for days, a round for
about six months, a demo request strongly and for weeks. That shape (fast, slow, strong) is what
the table above encodes.

## Checking them

After the first sync, read the top accounts (`run.md`, pilot). Two symptoms and their fix:

- **The top is all one type.** That weight is too high against the others, or its feed is noisy.
  Lower it or filter the feed (job titles for job offers), not the threshold.
- **An account the team knows is hot scores low.** Its signal is not in Account Events (no feed, or
  the model does not unify as an account event), or its type has no weight. Check the inventory
  query for that account's domain.
