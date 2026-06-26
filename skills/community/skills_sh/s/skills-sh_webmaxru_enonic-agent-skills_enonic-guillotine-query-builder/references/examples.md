# Guillotine Query Examples

Complete query examples with variables for common Guillotine patterns.

## 1. Fetch a Single Content by Path

```graphql
{
  guillotine {
    get(key: "/blog/first-post") {
      _id
      displayName
      type
      createdTime
      ... on com_enonic_app_myapp_BlogPost {
        data {
          title
          summary
          body {
            processedHtml
          }
        }
      }
    }
  }
}
```

## 2. Query Content by Type Using Term DSL

```graphql
{
  guillotine {
    queryDsl(
      query: {
        term: {
          field: "type"
          value: { string: "com.enonic.app.myapp:BlogPost" }
        }
      }
      sort: { field: "data.publishDate", direction: DESC }
      first: 10
    ) {
      displayName
      ... on com_enonic_app_myapp_BlogPost {
        data {
          title
          publishDate
          author {
            displayName
          }
        }
      }
    }
  }
}
```

## 3. Paginated Connection with Variables

```graphql
query GetPosts($after: String, $first: Int) {
  guillotine {
    queryDslConnection(
      query: {
        term: {
          field: "type"
          value: { string: "com.enonic.app.myapp:BlogPost" }
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
          ... on com_enonic_app_myapp_BlogPost {
            data {
              title
              summary
            }
          }
        }
      }
    }
  }
}
```

Variables:
```json
{
  "after": null,
  "first": 10
}
```

For the next page, set `"after"` to `pageInfo.endCursor` from the previous response.

## 4. Boolean Compound Query

Fetch published articles that must contain "javascript" in the title and must not be of category "archived":

```graphql
{
  guillotine {
    queryDsl(
      query: {
        boolean: {
          must: [
            { term: { field: "type", value: { string: "com.enonic.app.myapp:Article" } } }
            { fulltext: { fields: ["data.title"], query: "javascript", operator: AND } }
          ]
          mustNot: [
            { term: { field: "data.category", value: { string: "archived" } } }
          ]
        }
      }
      first: 20
    ) {
      displayName
      ... on com_enonic_app_myapp_Article {
        data {
          title
          category
        }
      }
    }
  }
}
```

## 5. Date Range Filtering

Fetch blog posts published in a date range:

```graphql
{
  guillotine {
    queryDsl(
      query: {
        boolean: {
          must: [
            { term: { field: "type", value: { string: "com.enonic.app.myapp:BlogPost" } } }
            {
              range: {
                field: "data.publishDate"
                gte: { localDateTime: "2024-01-01T00:00:00" }
                lt: { localDateTime: "2025-01-01T00:00:00" }
              }
            }
          ]
        }
      }
      sort: { field: "data.publishDate", direction: DESC }
    ) {
      ... on com_enonic_app_myapp_BlogPost {
        displayName
        data {
          publishDate
          title
        }
      }
    }
  }
}
```

## 6. Following Content References

Query an article and follow its author reference to get author details:

```graphql
{
  guillotine {
    get(key: "/articles/my-article") {
      ... on com_enonic_app_myapp_Article {
        displayName
        data {
          title
          author {
            ... on com_enonic_app_myapp_Person {
              displayName
              data {
                firstName
                lastName
                email
              }
            }
          }
        }
      }
    }
  }
}
```

## 7. Aggregations

Get a count of blog posts per category:

```graphql
{
  guillotine {
    queryDslConnection(
      query: {
        term: {
          field: "type"
          value: { string: "com.enonic.app.myapp:BlogPost" }
        }
      }
      first: 0
      aggregations: [
        {
          name: "byCategory"
          terms: { field: "data.category", size: 20 }
        }
      ]
    ) {
      totalCount
      aggregationsAsJson
    }
  }
}
```

## 8. Full-Text Search with Highlighting

```graphql
{
  guillotine {
    queryDslConnection(
      query: {
        fulltext: {
          fields: ["data.title", "data.body"]
          query: "machine learning"
          operator: OR
        }
      }
      first: 10
      highlight: {
        properties: [
          { propertyName: "data.title" }
          { propertyName: "data.body", fragmentSize: 200, numberOfFragments: 3 }
        ]
      }
    ) {
      totalCount
      highlightAsJson
      edges {
        node {
          _id
          displayName
        }
      }
    }
  }
}
```

## 9. Children and Nested Hierarchies

```graphql
{
  guillotine {
    getChildren(key: "/products", first: 50, sort: "displayName ASC") {
      _id
      _name
      displayName
      hasChildren
      children(first: 5) {
        displayName
      }
    }
  }
}
```

## 10. Rich Text with Processed HTML

```graphql
{
  guillotine {
    get(key: "/blog/first-post") {
      ... on com_enonic_app_myapp_BlogPost {
        data {
          body(processHtml: { type: absolute, imageWidths: [600, 1200] }) {
            processedHtml
            links {
              ref
              uri
              content { _id }
            }
            images {
              ref
              image { _id }
              style { name, aspectRatio }
            }
          }
        }
      }
    }
  }
}
```

## 11. Site Context Query with ${site} Placeholder

```graphql
{
  guillotine(siteKey: "/my-site") {
    getChildren(key: "${site}/blog") {
      displayName
      _path(type: siteRelative)
      ... on com_enonic_app_myapp_BlogPost {
        data {
          title
        }
      }
    }
  }
}
```

## 12. eXtra Data (xData)

```graphql
{
  guillotine {
    get(key: "/persons/jane-doe") {
      displayName
      x {
        com_example_myproject {
          SoMe {
            twitter
            linkedin
          }
        }
      }
    }
  }
}
```

## 13. Ngram Partial-Match Search

```graphql
{
  guillotine {
    queryDsl(
      query: {
        ngram: {
          fields: ["displayName", "data.title"]
          query: "jav"
        }
      }
      first: 10
    ) {
      _id
      displayName
    }
  }
}
```

## 14. Scaled Image URL from Media Content

Query image content and generate a scaled image URL:

```graphql
{
  guillotine {
    queryDsl(
      query: {
        term: {
          field: "type"
          value: { string: "media:image" }
        }
      }
      first: 10
    ) {
      displayName
      ... on media_Image {
        imageUrl(scale: "block(800,200)", type: absolute)
        data {
          caption
          artist
        }
      }
    }
  }
}
```

## 15. In DSL with Typed Value Arrays

Fetch content matching any of several category values using `in` with `stringValues`:

```graphql
{
  guillotine {
    queryDsl(
      query: {
        boolean: {
          must: [
            { term: { field: "type", value: { string: "com.enonic.app.myapp:Article" } } }
            { in: { field: "data.category", stringValues: ["news", "opinion", "review"] } }
          ]
        }
      }
      sort: { field: "createdTime", direction: DESC }
      first: 20
    ) {
      displayName
      ... on com_enonic_app_myapp_Article {
        data {
          title
          category
        }
      }
    }
  }
}
```

## 15. Scaled Image URL for Media Content

Query image content and generate a scaled, absolute URL:

```graphql
{
  guillotine {
    queryDsl(query: {
      term: {
        field: "type"
        value: { string: "media:image" }
      }
    }, first: 10) {
      displayName
      ... on media_Image {
        imageUrl(scale: "block(800,200)", type: absolute)
      }
    }
  }
}
```
