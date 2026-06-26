# Default design

Current version: **0.1.7**

## Purpose
This skill sits before `residential-property-rolling-suds-estimator`.
Its job is to clean and normalize messy intake so pricing has better inputs.

## Default output goals
1. Clean intake summary
2. Estimator-ready handoff
3. Workiz-ready note
4. Follow-up questions
5. Manual-review flags

## What this skill should NOT do by default
- Do not act like the final estimator
- Do not invent missing data
- Do not ask a giant wall of questions
- Do not hide uncertainty

## Default assumptions
- Business context: Rolling Suds exterior cleaning / pressure washing / window cleaning
- Service area context: St. Louis metro
- Internal workflow context: sales intake feeding Workiz and `residential-property-rolling-suds-estimator`
- Virtual quotes are a primary operating mode for residential work
- Some inbound wording may come from awkward cold-calling or lead-gen phrasing and should be normalized to intended meaning

## Design principle
The skill should reduce chaos, not create more text.

## Good outputs feel like
- something a salesperson can use immediately
- something that can be pasted into the estimator
- something that flags risk without drama

## Common messy inputs
- "Need quote for house and driveway in Florissant"
- "Lady wants windows and maybe fence too"
- "Address attached, wants power washing next week"
- pasted customer text messages
- call summary notes
- short sales rep summaries with half the details missing

## Recommended future improvements
- Add explicit service-area fit checks
- Add more structured address validation behavior
- Add examples of excellent handoffs to `residential-property-rolling-suds-estimator`
- Add deeper Workiz note conventions if the team develops a standard style
- Add more appointment-status normalization rules if the lead source uses consistent weird wording
