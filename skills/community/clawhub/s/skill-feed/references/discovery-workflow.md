# ClawHub Search + Ranking Workflow

## Discovery URLs

- Search entry: `https://clawhub.ai/skills?focus=search`
- Stars ranking: `https://clawhub.ai/skills?sort=stars&dir=desc`
- Recently updated: `https://clawhub.ai/skills?sort=updatedAt&dir=desc`

## Practical Search Flow

1. Run Q1 broad query to collect capability families.
2. Run Q2 scenario query to narrow to user workflow.
3. Run Q3 failure query with exact error markers.
4. Merge candidates and deduplicate by slug.
5. Rank with weighted scoring.

## Weighted Scoring (100)

- Goal fit: 40
- Failure-type fit: 25
- Setup friction: 15
- Maintenance/activity: 10
- Safety/risk posture: 10

## Scoring Example

Scenario: user wants to auto-post tweets but gets a 401 invalid token error.

| Candidate | Goal fit (40) | Failure fit (25) | Setup (15) | Maintenance (10) | Safety (10) | Total |
|-----------|--------------|-----------------|------------|------------------|-------------|-------|
| skill-twitter-poster | 38 | 22 | 12 | 8 | 9 | 89 |
| skill-social-suite | 35 | 20 | 8 | 7 | 8 | 78 |
| skill-api-gateway | 20 | 15 | 10 | 9 | 9 | 63 |

- **Goal fit**: how directly the skill solves the stated goal (tweet posting → twitter-poster scores highest).
- **Failure fit**: how well the skill addresses the specific error (401 auth → skills with token refresh score higher).
- **Setup friction**: lower friction = higher score (simple install beats complex config).
- **Maintenance**: recent updates and active repo = higher score.
- **Safety**: narrow scopes and no broad permissions = higher score.

## Recommendation Guardrails

- Prefer lower-friction options when scores are close.
- Flag skills requiring broad scopes or paid APIs.
- Include one conservative fallback for reliability.
- Avoid recommending >3 primary options.
