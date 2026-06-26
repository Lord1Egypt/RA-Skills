const DEFAULT_SHOPIFY_API_VERSION = "2026-01"
const RAW_RESPONSE_LIMIT = 4000
const READ_ONLY_REST_METHODS = new Set(["GET", "HEAD"])
const WRITE_REST_METHODS = new Set(["POST", "PUT", "PATCH", "DELETE"])

const readString = value =>
  typeof value === "string" && value.trim().length > 0 ? value.trim() : undefined

const truncate = (value, maxLength) =>
  value.length > maxLength ? `${value.slice(0, maxLength - 1)}...` : value

const toHeadersRecord = headers => {
  const result = {}
  headers.forEach((value, key) => {
    result[key] = value
  })
  return result
}

const toBodyText = value => {
  if (typeof value === "string") {
    return truncate(value, RAW_RESPONSE_LIMIT)
  }

  try {
    return truncate(JSON.stringify(value), RAW_RESPONSE_LIMIT)
  } catch {
    return "[unserializable]"
  }
}

const normalizeConnection = connection => {
  const storeDomain = readString(connection.storeDomain)
  const clientId = readString(connection.clientId)
  const apiKey = readString(connection.apiKey)
  const apiVersion = readString(connection.apiVersion)

  if (!storeDomain || !clientId || !apiKey) {
    return undefined
  }

  return {
    storeDomain,
    clientId,
    apiKey,
    apiVersion,
  }
}

const getShopifyAccessToken = async (connection, signal) => {
  const response = await fetch(`https://${connection.storeDomain}/admin/oauth/access_token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      grant_type: "client_credentials",
      client_id: connection.clientId,
      client_secret: connection.apiKey,
    }).toString(),
    signal,
  })

  const contentType = response.headers.get("content-type")?.toLowerCase() ?? ""
  const bodyText = await response.text()
  if (!contentType.includes("application/json")) {
    throw new Error(
      `Failed to fetch Shopify access token: ${response.status} ${truncate(bodyText, 200)}`,
    )
  }

  const payload = JSON.parse(bodyText)
  if (!response.ok || typeof payload !== "object" || payload === null) {
    throw new Error(
      `Failed to fetch Shopify access token: ${response.status} ${response.statusText}`,
    )
  }

  const accessToken = typeof payload.access_token === "string" ? payload.access_token : undefined
  const errorDescription =
    typeof payload.error_description === "string" ? payload.error_description : undefined
  const errorCode = typeof payload.error === "string" ? payload.error : undefined

  if (!accessToken) {
    throw new Error(
      `Failed to fetch Shopify access token: ${errorDescription ?? errorCode ?? response.statusText}`,
    )
  }

  return accessToken
}

const withQuery = (url, query) => {
  Object.entries(query).forEach(([key, value]) => {
    if (value !== undefined) {
      url.searchParams.set(key, String(value))
    }
  })
  return url
}

const parseResponseBody = async (response, method) => {
  if (
    method === "HEAD" ||
    response.status === 204 ||
    response.status === 205 ||
    response.status === 304
  ) {
    return { body: undefined, bodyText: "" }
  }

  const contentType = response.headers.get("content-type")?.toLowerCase() ?? ""
  const bodyText = await response.text()

  if (bodyText.length === 0) {
    return { body: undefined, bodyText: "" }
  }

  if (contentType.includes("application/json")) {
    return {
      body: JSON.parse(bodyText),
      bodyText: truncate(bodyText, RAW_RESPONSE_LIMIT),
    }
  }

  return {
    body: bodyText,
    bodyText: truncate(bodyText, RAW_RESPONSE_LIMIT),
  }
}

const createResponseRecord = async (response, method) => {
  const parsed = await parseResponseBody(response, method)
  return {
    ok: response.ok,
    status: response.status,
    url: response.url,
    headers: toHeadersRecord(response.headers),
    body: parsed.body,
    bodyText: parsed.bodyText,
  }
}

const createRequestLogger = (requestSummary, rawResponses) => {
  return async input => {
    const startedAt = Date.now()
    const response = await input.execute()
    const record = await createResponseRecord(response, input.method)
    rawResponses.push(record)
    requestSummary.push({
      method: input.method,
      url: input.url.toString(),
      status: record.status,
      durationMs: Date.now() - startedAt,
      description: input.description,
    })
    return input.map(record)
  }
}

const toExecuteAction = (method, mode) => {
  if (READ_ONLY_REST_METHODS.has(method)) {
    return "read"
  }

  if (WRITE_REST_METHODS.has(method)) {
    if (mode === "read") {
      throw new Error(`Shopify read-only requests only support GET or HEAD. Received ${method}.`)
    }
    return "write"
  }

  throw new Error(`Shopify does not support ${method} in the executor context.`)
}

const isGraphqlNameStart = character => /[_A-Za-z]/u.test(character)
const isGraphqlNameCharacter = character => /[_0-9A-Za-z]/u.test(character)
const isEscapedGraphqlBlockStringTerminator = (document, index) => document[index - 1] === "\\"

const tokenizeGraphqlDocument = document => {
  const tokens = []
  let index = 0

  while (index < document.length) {
    const character = document[index]
    if (!character) {
      break
    }

    if (character === "#" || character === ",") {
      if (character === "#") {
        index += 1
        while (index < document.length && document[index] !== "\n" && document[index] !== "\r") {
          index += 1
        }
        continue
      }

      index += 1
      continue
    }

    if (/\s/u.test(character)) {
      index += 1
      continue
    }

    if (character === '"') {
      const isBlockString = document.slice(index, index + 3) === '"""'
      index += isBlockString ? 3 : 1

      while (index < document.length) {
        if (isBlockString) {
          if (
            document.slice(index, index + 3) === '"""' &&
            !isEscapedGraphqlBlockStringTerminator(document, index)
          ) {
            index += 3
            break
          }
          index += 1
          continue
        }

        if (document[index] === "\\") {
          index += 2
          continue
        }

        if (document[index] === '"') {
          index += 1
          break
        }

        index += 1
      }

      continue
    }

    if (character === "." && document.slice(index, index + 3) === "...") {
      tokens.push({ kind: "punctuator", value: "..." })
      index += 3
      continue
    }

    if ("!$():=@[]{}|".includes(character)) {
      tokens.push({ kind: "punctuator", value: character })
      index += 1
      continue
    }

    if (isGraphqlNameStart(character)) {
      let end = index + 1
      while (end < document.length && isGraphqlNameCharacter(document[end] ?? "")) {
        end += 1
      }

      tokens.push({ kind: "name", value: document.slice(index, end) })
      index = end
      continue
    }

    index += 1
  }

  return tokens
}

const consumeGraphqlSelectionSet = (tokens, startIndex) => {
  let braceDepth = 0
  let parenDepth = 0
  let bracketDepth = 0
  let index = startIndex

  while (index < tokens.length) {
    const token = tokens[index]
    if (token?.kind === "punctuator") {
      if (token.value === "(") {
        parenDepth += 1
      } else if (token.value === ")") {
        parenDepth = Math.max(0, parenDepth - 1)
      } else if (token.value === "[") {
        bracketDepth += 1
      } else if (token.value === "]") {
        bracketDepth = Math.max(0, bracketDepth - 1)
      } else if (token.value === "{" && parenDepth === 0 && bracketDepth === 0) {
        braceDepth += 1
      } else if (token.value === "}" && parenDepth === 0 && bracketDepth === 0) {
        braceDepth -= 1
        if (braceDepth === 0) {
          return index + 1
        }
      }
    }

    index += 1
  }

  return index
}

const consumeGraphqlDefinitionHeader = (tokens, startIndex) => {
  let index = startIndex
  let parenDepth = 0
  let bracketDepth = 0

  while (index < tokens.length) {
    const token = tokens[index]
    if (token?.kind === "punctuator") {
      if (token.value === "(") {
        parenDepth += 1
      } else if (token.value === ")") {
        parenDepth = Math.max(0, parenDepth - 1)
      } else if (token.value === "[") {
        bracketDepth += 1
      } else if (token.value === "]") {
        bracketDepth = Math.max(0, bracketDepth - 1)
      } else if (token.value === "{" && parenDepth === 0 && bracketDepth === 0) {
        return consumeGraphqlSelectionSet(tokens, index)
      }
    }

    index += 1
  }

  return index
}

const collectGraphqlOperationTypes = document => {
  const tokens = tokenizeGraphqlDocument(document)
  const operationTypes = []
  let index = 0

  while (index < tokens.length) {
    const token = tokens[index]
    if (!token) {
      break
    }

    if (token.kind === "punctuator" && token.value === "{") {
      operationTypes.push("query")
      index = consumeGraphqlSelectionSet(tokens, index)
      continue
    }

    if (token.kind === "name") {
      if (token.value === "query" || token.value === "mutation" || token.value === "subscription") {
        operationTypes.push(token.value)
        index = consumeGraphqlDefinitionHeader(tokens, index + 1)
        continue
      }

      if (token.value === "fragment") {
        index = consumeGraphqlDefinitionHeader(tokens, index + 1)
        continue
      }
    }

    index += 1
  }

  return operationTypes
}

const containsGraphqlNonQueryOperation = document =>
  collectGraphqlOperationTypes(document).some(
    operationType => operationType === "mutation" || operationType === "subscription",
  )

const validateGraphqlOperation = (document, mode) => {
  const operationTypes = collectGraphqlOperationTypes(document)
  if (operationTypes.length === 0) {
    throw new Error("Shopify GraphQL document did not include an executable operation.")
  }

  if (operationTypes.includes("subscription")) {
    throw new Error(
      "Shopify GraphQL executor does not support subscriptions. Use a query or mutation instead.",
    )
  }

  if (mode === "read" && operationTypes.includes("mutation")) {
    throw new Error(
      "Shopify read-only GraphQL only supports queries. Mutations and subscriptions are not allowed.",
    )
  }
}

export const shopifyProvider = {
  name: "shopify",
  label: "Shopify",
  defaultApiVersion: DEFAULT_SHOPIFY_API_VERSION,
  defaultDocs: [
    {
      title: "Shopify Admin GraphQL API",
      url: "https://shopify.dev/docs/api/admin-graphql",
    },
    {
      title: "GraphQL queries basics",
      url: "https://shopify.dev/docs/apps/build/graphql/basics/queries",
    },
    {
      title: "GraphQL mutations basics",
      url: "https://shopify.dev/docs/apps/build/graphql/basics/mutations",
    },
  ],
  curatedNotes: [
    {
      title: "Shopify provider operating rules",
      url: "provider://shopify/operating-rules",
      content: [
        "Use Admin GraphQL by default for read workflows.",
        "Store access depends on the configured store domain plus the configured clientId and apiKey.",
        "Order data can still fail when protected customer data access is missing.",
        "Long order windows may require both read_orders and read_all_orders.",
        "Prefer narrow paginated queries and respect API throttling in multi-step reads.",
      ].join(" "),
    },
  ],
  validateConnection(connection) {
    return normalizeConnection(connection)
      ? { ok: true }
      : {
          ok: false,
          reason:
            "Set SHOPIFY_STORE_DOMAIN, SHOPIFY_CLIENT_ID, and configure this skill's apiKey so OpenClaw can inject SHOPIFY_CLIENT_SECRET.",
        }
  },
  describeConnection(connection) {
    return {
      connection: {
        storeDomain: readString(connection.storeDomain) ?? "unknown",
        clientId: readString(connection.clientId) ?? "missing",
        apiVersion: readString(connection.apiVersion) ?? DEFAULT_SHOPIFY_API_VERSION,
      },
    }
  },
  async createExecutorContext(inputConnection, signal, execution) {
    const connection = normalizeConnection(inputConnection)
    if (!connection) {
      throw new Error(
        "Set SHOPIFY_STORE_DOMAIN, SHOPIFY_CLIENT_ID, and configure this skill's apiKey so OpenClaw can inject SHOPIFY_CLIENT_SECRET.",
      )
    }

    const requestSummary = []
    const rawResponses = []
    const accessToken = await getShopifyAccessToken(connection, signal)
    const apiVersion = connection.apiVersion ?? DEFAULT_SHOPIFY_API_VERSION
    const baseUrl = `https://${connection.storeDomain}/admin/api/${apiVersion}`
    const runLoggedRequest = createRequestLogger(requestSummary, rawResponses)

    const request = async input => {
      const method = input.method?.trim().toUpperCase() || "GET"
      toExecuteAction(method, execution.mode)

      const requestPath = input.path.startsWith("/") ? input.path : `/${input.path}`
      const url = withQuery(new URL(`${baseUrl}${requestPath}`), input.query ?? {})

      return runLoggedRequest({
        description: `${method} ${requestPath}`,
        method,
        url,
        execute: () =>
          fetch(url, {
            method,
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
              "X-Shopify-Access-Token": accessToken,
              ...input.headers,
            },
            body: input.json === undefined ? undefined : JSON.stringify(input.json),
            signal,
          }),
        map: response => {
          if (!response.ok) {
            throw new Error(`Shopify request failed (${response.status}): ${response.bodyText}`)
          }
          return response.body
        },
      })
    }

    const graphql = async (query, variables) => {
      if (execution.mode === "read" && containsGraphqlNonQueryOperation(query)) {
        throw new Error(
          "Shopify read-only GraphQL only supports queries. Mutations and subscriptions are not allowed.",
        )
      }

      validateGraphqlOperation(query, execution.mode)
      const url = new URL(`${baseUrl}/graphql.json`)

      return runLoggedRequest({
        description: "POST /graphql.json",
        method: "POST",
        url,
        execute: () =>
          fetch(url, {
            method: "POST",
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
              "X-Shopify-Access-Token": accessToken,
            },
            body: JSON.stringify({
              query,
              variables: variables ?? {},
            }),
            signal,
          }),
        map: response => {
          if (!response.ok) {
            throw new Error(
              `Shopify GraphQL request failed (${response.status}): ${response.bodyText}`,
            )
          }

          if (typeof response.body !== "object" || response.body === null) {
            throw new Error("Shopify GraphQL response was not JSON.")
          }

          const errors = Array.isArray(response.body.errors) ? response.body.errors : []
          if (errors.length > 0) {
            throw new Error(`Shopify GraphQL errors: ${toBodyText(errors)}`)
          }

          return response.body.data ?? response.body
        },
      })
    }

    return {
      profile: {
        id: connection.storeDomain,
        name: connection.storeDomain,
        provider: shopifyProvider.name,
      },
      connection: {
        storeDomain: connection.storeDomain,
        apiVersion,
      },
      graphql,
      request,
      requestSummary,
      rawResponses,
    }
  },
}
