PRODUCT_LIST = """
query($first: Int!, $query: String) {
  products(first: $first, query: $query) {
    nodes {
      id
      title
      status
      vendor
      productType
      tags
      variants(first: 1) {
        nodes {
          price
        }
      }
    }
  }
}
"""

PRODUCT_GET = """
query($id: ID!) {
  product(id: $id) {
    id
    title
    descriptionHtml
    status
    vendor
    productType
    tags
    variants(first: 10) {
      nodes {
        id
        title
        price
        sku
      }
    }
    metafields(first: 20) {
      nodes {
        namespace
        key
        value
        type
      }
    }
  }
}
"""

PRODUCT_CREATE = """
mutation($input: ProductCreateInput!, $media: [CreateMediaInput!]) {
  productCreate(product: $input, media: $media) {
    product {
      id
      title
      status
    }
    userErrors {
      field
      message
    }
  }
}
"""

PRODUCT_UPDATE = """
mutation($input: ProductUpdateInput!, $media: [CreateMediaInput!]) {
  productUpdate(product: $input, media: $media) {
    product {
      id
      title
      status
    }
    userErrors {
      field
      message
    }
  }
}
"""

PRODUCT_DELETE = """
mutation($input: ProductDeleteInput!) {
  productDelete(input: $input) {
    deletedProductId
    userErrors {
      field
      message
    }
  }
}
"""

METAFIELD_DEFINITION_LIST = """
query($ownerType: MetafieldOwnerType!, $first: Int!) {
  metafieldDefinitions(ownerType: $ownerType, first: $first) {
    nodes {
      namespace
      key
      name
      type {
        name
      }
      ownerType
      pinnedPosition
    }
  }
}
"""

METAFIELD_DEFINITION_CREATE = """
mutation($definition: MetafieldDefinitionInput!) {
  metafieldDefinitionCreate(definition: $definition) {
    createdDefinition {
      id
      namespace
      key
      name
    }
    userErrors {
      field
      message
    }
  }
}
"""

METAFIELDS_SET = """
mutation($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields {
      id
      namespace
      key
      value
      type
    }
    userErrors {
      field
      message
    }
  }
}
"""

METAOBJECT_DEFINITION_CREATE = """
mutation($definition: MetaobjectDefinitionCreateInput!) {
  metaobjectDefinitionCreate(definition: $definition) {
    metaobjectDefinition {
      id
      type
      name
    }
    userErrors {
      field
      message
    }
  }
}
"""

METAOBJECT_UPSERT = """
mutation($handle: MetaobjectHandleInput!, $metaobject: MetaobjectUpsertInput!) {
  metaobjectUpsert(handle: $handle, metaobject: $metaobject) {
    metaobject {
      id
      handle
      type
      displayName
    }
    userErrors {
      field
      message
    }
  }
}
"""

METAOBJECT_LIST = """
query($type: String!, $first: Int!) {
  metaobjects(type: $type, first: $first) {
    nodes {
      id
      handle
      type
      displayName
    }
  }
}
"""

METAOBJECT_UPDATE = """
mutation($id: ID!, $metaobject: MetaobjectUpdateInput!) {
  metaobjectUpdate(id: $id, metaobject: $metaobject) {
    metaobject {
      id
      handle
      displayName
    }
    userErrors {
      field
      message
    }
  }
}
"""

METAOBJECT_DELETE = """
mutation($id: ID!) {
  metaobjectDelete(id: $id) {
    deletedId
    userErrors {
      field
      message
    }
  }
}
"""

BLOG_LIST = """
query($first: Int!) {
  blogs(first: $first) {
    nodes {
      id
      title
      handle
    }
  }
}
"""

BLOG_CREATE = """
mutation($blog: BlogCreateInput!) {
  blogCreate(blog: $blog) {
    blog {
      id
      title
      handle
    }
    userErrors {
      field
      message
    }
  }
}
"""

ARTICLE_LIST = """
query($first: Int!, $query: String) {
  articles(first: $first, query: $query) {
    nodes {
      id
      title
      blog {
        title
      }
      author {
        name
      }
      publishedAt
    }
  }
}
"""

ARTICLE_CREATE = """
mutation($article: ArticleCreateInput!) {
  articleCreate(article: $article) {
    article {
      id
      title
    }
    userErrors {
      field
      message
    }
  }
}
"""

ARTICLE_UPDATE = """
mutation($id: ID!, $article: ArticleUpdateInput!) {
  articleUpdate(id: $id, article: $article) {
    article {
      id
      title
      publishedAt
    }
    userErrors {
      field
      message
    }
  }
}
"""

ARTICLE_DELETE = """
mutation($id: ID!) {
  articleDelete(id: $id) {
    deletedArticleId
    userErrors {
      field
      message
    }
  }
}
"""

STAGED_UPLOADS_CREATE = """
mutation($input: [StagedUploadInput!]!) {
  stagedUploadsCreate(input: $input) {
    stagedTargets {
      url
      resourceUrl
      parameters {
        name
        value
      }
    }
    userErrors {
      field
      message
    }
  }
}
"""

FILE_CREATE = """
mutation($files: [FileCreateInput!]!) {
  fileCreate(files: $files) {
    files {
      id
      fileStatus
      alt
      createdAt
      ... on MediaImage {
        image {
          width
          height
        }
      }
      ... on GenericFile {
        url
      }
    }
    userErrors {
      field
      message
    }
  }
}
"""
