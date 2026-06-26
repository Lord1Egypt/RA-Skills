/**
 * Guillotine query + TypeScript types template.
 *
 * Replace placeholders:
 *   __APP_KEY__      → e.g. "com.enonic.app.myapp"
 *   __CONTENT_TYPE__ → e.g. "BlogPost"
 *   __FIELDS__       → e.g. "title\n  summary\n  publishDate"
 */

// ---------------------------------------------------------------------------
// TypeScript interfaces
// ---------------------------------------------------------------------------

export interface __CONTENT_TYPE__Data {
  // TODO: Add typed fields matching the content type schema
  // __FIELDS__
}

export interface __CONTENT_TYPE__Content {
  _id: string;
  _name: string;
  _path: string;
  displayName: string;
  type: string;
  createdTime: string;
  modifiedTime: string;
  data: __CONTENT_TYPE__Data;
}

export interface ContentEdge<T = __CONTENT_TYPE__Content> {
  cursor: string;
  node: T;
}

export interface PageInfo {
  startCursor: string;
  endCursor: string;
  hasNext: boolean;
}

export interface ContentConnection<T = __CONTENT_TYPE__Content> {
  totalCount: number;
  edges: ContentEdge<T>[];
  pageInfo: PageInfo;
  aggregationsAsJson?: Record<string, unknown>;
  highlightAsJson?: Record<string, unknown>;
}

export interface GuillotineResponse<T> {
  data: {
    guillotine: T;
  };
}

// ---------------------------------------------------------------------------
// Query string
// ---------------------------------------------------------------------------

export const LIST_QUERY = `
query List__CONTENT_TYPE__($after: String, $first: Int) {
  guillotine {
    queryDslConnection(
      query: {
        term: {
          field: "type"
          value: { string: "__APP_KEY__:__CONTENT_TYPE__" }
        }
      }
      after: $after
      first: $first
      sort: { field: "createdTime", direction: DESC }
    ) {
      totalCount
      pageInfo {
        startCursor
        endCursor
        hasNext
      }
      edges {
        cursor
        node {
          _id
          displayName
          ... on __GRAPHQL_TYPE__ {
            data {
              __FIELDS__
            }
          }
        }
      }
    }
  }
}
`;

export const GET_QUERY = `
query Get__CONTENT_TYPE__($key: ID) {
  guillotine {
    get(key: $key) {
      _id
      _name
      _path
      displayName
      type
      createdTime
      modifiedTime
      ... on __GRAPHQL_TYPE__ {
        data {
          __FIELDS__
        }
      }
    }
  }
}
`;

// ---------------------------------------------------------------------------
// Fetch helper
// ---------------------------------------------------------------------------

const GUILLOTINE_ENDPOINT = "/site/<project>/<branch>";

export async function guillotineQuery<T>(
  query: string,
  variables: Record<string, unknown> = {},
  siteKey?: string
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (siteKey) {
    headers["X-Guillotine-SiteKey"] = siteKey;
  }

  const res = await fetch(GUILLOTINE_ENDPOINT, {
    method: "POST",
    headers,
    body: JSON.stringify({ query, variables }),
  });

  if (!res.ok) {
    throw new Error(`Guillotine request failed: ${res.status} ${res.statusText}`);
  }

  const json: GuillotineResponse<T> = await res.json();
  return json.data.guillotine;
}
