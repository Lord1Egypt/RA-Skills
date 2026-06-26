> ## Documentation Index
> Fetch the complete documentation index at: https://docs.tavily.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Tavily Search

> Execute a search query using Tavily Search.



## OpenAPI

````yaml POST /search
openapi: 3.0.3
info:
  title: Tavily Search and Extract API
  description: >-
    Our REST API provides seamless access to Tavily Search, a powerful search
    engine for LLM agents, and Tavily Extract, an advanced web scraping solution
    optimized for LLMs.
  version: 1.0.0
servers:
  - url: https://api.tavily.com/
security: []
tags:
  - name: Search
  - name: Extract
  - name: Crawl
  - name: Map
  - name: Research
  - name: Usage
paths:
  /search:
    post:
      summary: Search for data based on a query
      description: Execute a search query using Tavily Search.
      requestBody:
        description: Parameters for the Tavily Search request.
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                query:
                  type: string
                  description: The search query to execute with Tavily.
                  example: who is Leo Messi?
                search_depth:
                  type: string
                  description: >-
                    Controls the latency vs. relevance tradeoff and how
                    `results[].content` is generated:

                    - `advanced`: Highest relevance with increased latency. Best
                    for detailed, high-precision queries. Returns multiple
                    semantically relevant snippets per URL (configurable via
                    `chunks_per_source`).

                    - `basic`: A balanced option for relevance and latency.
                    Ideal for general-purpose searches. Returns one NLP summary
                    per URL.

                    - `fast`: Prioritizes lower latency while maintaining good
                    relevance. Returns multiple semantically relevant snippets
                    per URL (configurable via `chunks_per_source`).

                    - `ultra-fast`: Minimizes latency above all else. Best for
                    time-critical use cases. Returns one NLP summary per URL.


                    **Cost**:

                    - `basic`, `fast`, `ultra-fast`: 1 API Credit

                    - `advanced`: 2 API Credits


                    See [Search Best
                    Practices](/documentation/best-practices/best-practices-search#search-depth)
                    for guidance on choosing the right search depth.
                  enum:
                    - advanced
                    - basic
                    - fast
                    - ultra-fast
                  default: basic
                chunks_per_source:
                  type: integer
                  description: >-
                    Chunks are short content snippets (maximum 500 characters
                    each) pulled directly from the source. Use
                    `chunks_per_source` to define the maximum number of relevant
                    chunks returned per source and to control the `content`
                    length. Chunks will appear in the `content` field as:
                    `<chunk 1> [...] <chunk 2> [...] <chunk 3>`. Available only
                    when `search_depth` is `advanced`.
                  default: 3
                  minimum: 1
                  maximum: 3
                max_results:
                  type: integer
                  example: 1
                  description: The maximum number of search results to return.
                  default: 5
                  minimum: 0
                  maximum: 20
                topic:
                  type: string
                  description: >-
                    The category of the search.`news` is useful for retrieving
                    real-time updates, particularly about politics, sports, and
                    major current events covered by mainstream media sources.
                    `general` is for broader, more general-purpose searches that
                    may include a wide range of sources.
                  default: general
                  enum:
                    - general
                    - news
                    - finance
                time_range:
                  type: string
                  description: >-
                    The time range back from the current date to filter results
                    based on publish date or last updated date. Useful when
                    looking for sources that have published or updated data.
                  enum:
                    - day
                    - week
                    - month
                    - year
                    - d
                    - w
                    - m
                    - 'y'
                  default: null
                start_date:
                  type: string
                  description: >-
                    Will return all results after the specified start date based
                    on publish date or last updated date. Required to be written
                    in the format YYYY-MM-DD
                  example: '2025-02-09'
                  default: null
                end_date:
                  type: string
                  description: >-
                    Will return all results before the specified end date based
                    on publish date or last updated date. Required to be written
                    in the format YYYY-MM-DD
                  example: '2025-12-29'
                  default: null
                include_answer:
                  oneOf:
                    - type: boolean
                    - type: string
                      enum:
                        - basic
                        - advanced
                  description: >-
                    Include an LLM-generated answer to the provided query.
                    `basic` or `true` returns a quick answer. `advanced` returns
                    a more detailed answer.
                  default: false
                include_raw_content:
                  oneOf:
                    - type: boolean
                    - type: string
                      enum:
                        - markdown
                        - text
                  description: >-
                    Include the cleaned and parsed HTML content of each search
                    result. `markdown` or `true` returns search result content
                    in markdown format. `text` returns the plain text from the
                    results and may increase latency.
                  default: false
                include_images:
                  type: boolean
                  description: >-
                    Also perform an image search and include the results in the
                    response.
                  default: false
                include_image_descriptions:
                  type: boolean
                  description: >-
                    When `include_images` is `true`, also add a descriptive text
                    for each image.
                  default: false
                include_favicon:
                  type: boolean
                  description: Whether to include the favicon URL for each result.
                  default: false
                include_domains:
                  type: array
                  description: >-
                    A list of domains to specifically include in the search
                    results. Maximum 300 domains.
                  items:
                    type: string
                  default: []
                exclude_domains:
                  type: array
                  description: >-
                    A list of domains to specifically exclude from the search
                    results. Maximum 150 domains.
                  items:
                    type: string
                  default: []
                country:
                  type: string
                  description: >-
                    Boost search results from a specific country. This will
                    prioritize content from the selected country in the search
                    results. Available only if topic is `general`.
                  enum:
                    - afghanistan
                    - albania
                    - algeria
                    - andorra
                    - angola
                    - argentina
                    - armenia
                    - australia
                    - austria
                    - azerbaijan
                    - bahamas
                    - bahrain
                    - bangladesh
                    - barbados
                    - belarus
                    - belgium
                    - belize
                    - benin
                    - bhutan
                    - bolivia
                    - bosnia and herzegovina
                    - botswana
                    - brazil
                    - brunei
                    - bulgaria
                    - burkina faso
                    - burundi
                    - cambodia
                    - cameroon
                    - canada
                    - cape verde
                    - central african republic
                    - chad
                    - chile
                    - china
                    - colombia
                    - comoros
                    - congo
                    - costa rica
                    - croatia
                    - cuba
                    - cyprus
                    - czech republic
                    - denmark
                    - djibouti
                    - dominican republic
                    - ecuador
                    - egypt
                    - el salvador
                    - equatorial guinea
                    - eritrea
                    - estonia
                    - ethiopia
                    - fiji
                    - finland
                    - france
                    - gabon
                    - gambia
                    - georgia
                    - germany
                    - ghana
                    - greece
                    - guatemala
                    - guinea
                    - haiti
                    - honduras
                    - hungary
                    - iceland
                    - india
                    - indonesia
                    - iran
                    - iraq
                    - ireland
                    - israel
                    - italy
                    - jamaica
                    - japan
                    - jordan
                    - kazakhstan
                    - kenya
                    - kuwait
                    - kyrgyzstan
                    - latvia
                    - lebanon
                    - lesotho
                    - liberia
                    - libya
                    - liechtenstein
                    - lithuania
                    - luxembourg
                    - madagascar
                    - malawi
                    - malaysia
                    - maldives
                    - mali
                    - malta
                    - mauritania
                    - mauritius
                    - mexico
                    - moldova
                    - monaco
                    - mongolia
                    - montenegro
                    - morocco
                    - mozambique
                    - myanmar
                    - namibia
                    - nepal
                    - netherlands
                    - new zealand
                    - nicaragua
                    - niger
                    - nigeria
                    - north korea
                    - north macedonia
                    - norway
                    - oman
                    - pakistan
                    - panama
                    - papua new guinea
                    - paraguay
                    - peru
                    - philippines
                    - poland
                    - portugal
                    - qatar
                    - romania
                    - russia
                    - rwanda
                    - saudi arabia
                    - senegal
                    - serbia
                    - singapore
                    - slovakia
                    - slovenia
                    - somalia
                    - south africa
                    - south korea
                    - south sudan
                    - spain
                    - sri lanka
                    - sudan
                    - sweden
                    - switzerland
                    - syria
                    - taiwan
                    - tajikistan
                    - tanzania
                    - thailand
                    - togo
                    - trinidad and tobago
                    - tunisia
                    - turkey
                    - turkmenistan
                    - uganda
                    - ukraine
                    - united arab emirates
                    - united kingdom
                    - united states
                    - uruguay
                    - uzbekistan
                    - venezuela
                    - vietnam
                    - yemen
                    - zambia
                    - zimbabwe
                  default: null
                auto_parameters:
                  type: boolean
                  description: >-
                    When `auto_parameters` is enabled, Tavily automatically
                    configures search parameters based on your query's content
                    and intent. You can still set other parameters manually, and
                    your explicit values will override the automatic ones. The
                    parameters `include_answer`, `include_raw_content`, and
                    `max_results` must always be set manually, as they directly
                    affect response size. Note: `search_depth` may be
                    automatically set to advanced when it's likely to improve
                    results. This uses 2 API credits per request. To avoid the
                    extra cost, you can explicitly set `search_depth` to
                    `basic`.
                  default: false
                exact_match:
                  type: boolean
                  description: >-
                    Ensure that only search results containing the exact quoted
                    phrase(s) in the query are returned, bypassing synonyms or
                    semantic variations. Wrap target phrases in quotes within
                    your query (e.g. `"John Smith" CEO Acme Corp`). Punctuation
                    is typically ignored inside quotes.
                  default: false
                include_usage:
                  type: boolean
                  description: Whether to include credit usage information in the response.
                  default: false
              required:
                - query
      responses:
        '200':
          description: Search results returned successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  query:
                    type: string
                    description: The search query that was executed.
                    example: Who is Leo Messi?
                  answer:
                    type: string
                    description: >-
                      A short answer to the user's query, generated by an LLM.
                      Included in the response only if `include_answer` is
                      requested (i.e., set to `true`, `basic`, or `advanced`)
                    example: >-
                      Lionel Messi, born in 1987, is an Argentine footballer
                      widely regarded as one of the greatest players of his
                      generation. He spent the majority of his career playing
                      for FC Barcelona, where he won numerous domestic league
                      titles and UEFA Champions League titles. Messi is known
                      for his exceptional dribbling skills, vision, and
                      goal-scoring ability. He has won multiple FIFA Ballon d'Or
                      awards, numerous La Liga titles with Barcelona, and holds
                      the record for most goals scored in a calendar year. In
                      2014, he led Argentina to the World Cup final, and in
                      2015, he helped Barcelona capture another treble. Despite
                      turning 36 in June, Messi remains highly influential in
                      the sport.
                  images:
                    type: array
                    description: >-
                      List of query-related images. If
                      `include_image_descriptions` is true, each item will have
                      `url` and `description`.
                    example: []
                    items:
                      type: object
                      properties:
                        url:
                          type: string
                        description:
                          type: string
                  results:
                    type: array
                    description: A list of sorted search results, ranked by relevancy.
                    items:
                      type: object
                      properties:
                        title:
                          type: string
                          description: The title of the search result.
                          example: Lionel Messi Facts | Britannica
                        url:
                          type: string
                          description: The URL of the search result.
                          example: https://www.britannica.com/facts/Lionel-Messi
                        content:
                          type: string
                          description: A short description of the search result.
                          example: >-
                            Lionel Messi, an Argentine footballer, is widely
                            regarded as one of the greatest football players of
                            his generation. Born in 1987, Messi spent the
                            majority of his career playing for Barcelona, where
                            he won numerous domestic league titles and UEFA
                            Champions League titles. Messi is known for his
                            exceptional dribbling skills, vision, and goal
                        score:
                          type: number
                          format: float
                          description: The relevance score of the search result.
                          example: 0.81025416
                        raw_content:
                          type: string
                          description: >-
                            The cleaned and parsed HTML content of the search
                            result. Only if `include_raw_content` is true.
                          example: null
                        favicon:
                          type: string
                          description: The favicon URL for the result.
                          example: https://britannica.com/favicon.png
                  auto_parameters:
                    type: object
                    description: >-
                      A dictionary of the selected auto_parameters, only shown
                      when `auto_parameters` is true.
                    example:
                      topic: general
                      search_depth: basic
                  response_time:
                    type: number
                    format: float
                    description: Time in seconds it took to complete the request.
                    example: '1.67'
                  usage:
                    type: object
                    description: Credit usage details for the request.
                    example:
                      credits: 1
                  request_id:
                    type: string
                    description: >-
                      A unique request identifier you can share with customer
                      support to help resolve issues with specific requests.
                    example: 123e4567-e89b-12d3-a456-426614174111
                required:
                  - query
                  - results
                  - images
                  - response_time
                  - answer
        '400':
          description: Bad Request - Your request is invalid.
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: object
                    properties:
                      error:
                        type: string
              example:
                detail:
                  error: >-
                    <400 Bad Request, (e.g Invalid topic. Must be 'general' or
                    'news'.)>
        '401':
          description: Unauthorized - Your API key is wrong or missing.
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: object
                    properties:
                      error:
                        type: string
              example:
                detail:
                  error: 'Unauthorized: missing or invalid API key.'
        '429':
          description: Too many requests - Rate limit exceeded
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: object
                    properties:
                      error:
                        type: string
              example:
                detail:
                  error: >-
                    Your request has been blocked due to excessive requests.
                    Please reduce rate of requests.
        '432':
          description: Key limit or Plan Limit exceeded
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: object
                    properties:
                      error:
                        type: string
              example:
                detail:
                  error: >-
                    <432 Custom Forbidden Error (e.g This request exceeds your
                    plan's set usage limit. Please upgrade your plan or contact
                    support@tavily.com)>
        '433':
          description: PayGo limit exceeded
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: object
                    properties:
                      error:
                        type: string
              example:
                detail:
                  error: >-
                    This request exceeds the pay-as-you-go limit. You can
                    increase your limit on the Tavily dashboard.
        '500':
          description: Internal Server Error - We had a problem with our server.
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: object
                    properties:
                      error:
                        type: string
              example:
                detail:
                  error: Internal Server Error
      security:
        - bearerAuth: []
      x-codeSamples:
        - lang: python
          label: Python SDK
          source: |-
            from tavily import TavilyClient

            tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")
            response = tavily_client.search("Who is Leo Messi?")

            print(response)
        - lang: javascript
          label: JavaScript SDK
          source: |-
            const { tavily } = require("@tavily/core");

            const tvly = tavily({ apiKey: "tvly-YOUR_API_KEY" });
            const response = await tvly.search("Who is Leo Messi?");

            console.log(response);
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: >-
        Bearer authentication header in the form Bearer <token>, where <token>
        is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).

````
