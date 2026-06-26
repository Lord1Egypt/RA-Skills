/**
 * GraphQL query strings for Startup School API.
 * Captured from live Apollo Client inspection (2026-03-03).
 *
 * Endpoint: POST https://www.startupschool.org/graphql
 * Content-Type: application/json
 */

export const UPDATES_INDEX = `
query UPDATES_INDEX($companyId: ID) {
  currentUser {
    slug
    track
    __typename
  }
  updates(companyId: $companyId) {
    companyName
    updates {
      biggestBlocker
      biggestChange
      canEdit
      completableGoals {
        key
        goal
        completed
        __typename
      }
      createdAt
      formattedDate
      goals
      id
      learnedFromUsers
      metricDisplayName
      metricValue
      morale
      path
      talkedTo
      __typename
    }
    thisWeekSubmitted
    __typename
  }
}
`;

export const UPDATE_CHARTS = `
query UPDATE_CHARTS($companyId: ID) {
  updates(companyId: $companyId) {
    updates {
      createdAt
      metricDisplayName
      metricValue
      morale
      talkedTo
      __typename
    }
    __typename
  }
}
`;

/**
 * Dashboard query — reconstructed from Apollo cache inspection.
 * Fields confirmed: currentStreak, curriculum (completed, required, nextItem),
 * updatesByWeek (url, weekLabel), cofounderMatching, completedActions.
 */
export const DASHBOARD_DATA = `
query DASHBOARD_DATA {
  currentUser {
    slug
    firstName
    track
    returningUser
    __typename
  }
  completedActions
  dashboard {
    currentStreak
    curriculum {
      completed
      required
      nextItem {
        id
        title
        previewLink
        contentType
        url
        __typename
      }
      __typename
    }
    updatesByWeek {
      url
      weekLabel
      __typename
    }
    __typename
  }
  cofounderMatching {
    __typename
  }
  updates {
    __typename
  }
}
`;

/**
 * Current user query — lightweight identity check.
 */
export const CURRENT_USER = `
query CURRENT_USER {
  currentUser {
    slug
    firstName
    track
    returningUser
    __typename
  }
}
`;
