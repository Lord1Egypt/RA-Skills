---
name: undocs-contributors-sponsors
description: Display contributors and sponsors on landing page in undocs
---

# Contributors & Sponsors

Undocs displays GitHub contributors and sponsors on the landing page.

## Contributors

### Enable

Enable contributors in landing config:

```yaml
# .config/docs.yaml
landing:
  contributors: true
```

Requires `github` to be set. Contributors are fetched from GitHub via ungh.cc API.

### API

Contributors are fetched from:

```
https://ungh.cc/repos/{owner}/{repo}/contributors
```

Returns `{ contributors: [{ username }] }`. Bot contributors are filtered out.

### Data Shape

```typescript
interface Contributor {
  name: string;   // @username
  username: string;
  profile: string;  // https://github.com/username
  avatar: string;   // https://github.com/username.png
}
```

### Display

`PageContributors` renders:

- Avatar grid of contributors (UTooltip with name)
- "Contribute on GitHub" button linking to `https://github.com/{github}`

## Sponsors

### Enable

Provide sponsors API URL:

```yaml
# .config/docs.yaml
sponsors:
  api: https://sponsors.example.com/sponsors.json
```

### API Format

The sponsors API should return:

```typescript
interface Sponsors {
  username: string;  // GitHub username for "Become a Sponsor" link
  sponsors: {
    name: string;
    image: string;
    inactive?: boolean;
    website: string;
  }[][];  // Array of tiers, each tier is array of sponsors
}
```

Tiers:

- `sponsors[0]` — Top tier (large display)
- `sponsors[1]` — Second tier
- `sponsors[2]` — Third tier (avatars)
- `sponsors[3]` — Fourth tier (small avatars)

### Display

`PageSponsors` renders:

- Top 2 tiers with logo/name prominently
- Tier 3: Avatar grid
- Tier 4: Small avatar grid
- "Become a Sponsor" button linking to `https://github.com/sponsors/{username}`

## Composable

### useContributors

```typescript
const contributors = await useContributors();
// Returns Contributor[] or undefined
```

### useSponsors

```typescript
const sponsors = await useSponsors();
// Returns Sponsors or undefined
```

## Key Points

- Contributors require `github` and `landing.contributors: true`
- Sponsors require `sponsors.api` URL
- Contributors use ungh.cc API; sponsors use custom JSON API
- Both are displayed on landing page only

<!--
Source references:
- https://github.com/unjs/undocs/blob/main/app/composables/useContributors.ts
- https://github.com/unjs/undocs/blob/main/app/composables/useSponsors.ts
- https://github.com/unjs/undocs/blob/main/app/components/page/PageContributors.vue
- https://github.com/unjs/undocs/blob/main/app/components/page/PageSponsors.vue
-->
