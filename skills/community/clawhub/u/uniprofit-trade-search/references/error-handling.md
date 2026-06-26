# Error Handling

## 401 Invalid credential

Meaning:

- key missing
- key revoked
- wrong key value

Action:

- tell the user the UniProfit trade search key is invalid or missing
- suggest checking `UNIPROFIT_TRADE_SEARCH_KEY`

## 403 Wrong skill or no quota

Meaning:

- using a non-`trade_search` key
- no purchased search quota

Action:

- tell the user the current key cannot use trade search, or the account has no remaining quota

## 400 Unsupported filters or blocked broad query

Meaning:

- unsupported filter was sent for the chosen source
- no effective filter was provided, so the backend blocked a broad query
- page depth exceeded the current runtime limit

Action:

- surface the backend error directly
- tell the user which filters are supported for that source
- suggest switching source or narrowing the request
- do not keep paging deeper when the backend asks for narrower filters
- if the rejected request was low-confidence anyway, prefer one clarifying question before retrying

## 404 Order or resource not found

Usually not part of runtime search unless backend data is inconsistent.

Action:

- surface the backend message
- do not fabricate a result

## Empty data

Action:

- state the search returned no data
- recommend a broader retry or a different source
- if the original source choice was weak, suggest a different source rather than blindly repeating the same query
