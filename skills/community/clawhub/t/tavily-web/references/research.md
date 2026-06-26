> ## Documentation Index
> Fetch the complete documentation index at: https://docs.tavily.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Create Research Task

> Tavily Research performs comprehensive research on a given topic by conducting multiple searches, analyzing sources, and generating a detailed research report.



## OpenAPI

````yaml POST /research
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
  /research:
    post:
      summary: Initiate a research task
      description: >-
        Tavily Research performs comprehensive research on a given topic by
        conducting multiple searches, analyzing sources, and generating a
        detailed research report.
      requestBody:
        description: Parameters for the Tavily Research request.
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                input:
                  type: string
                  description: The research task or question to investigate.
                  example: What are the latest developments in AI?
                model:
                  type: string
                  description: >-
                    The model used by the research agent. "mini" is optimized
                    for targeted, efficient research and works best for narrow
                    or well-scoped questions. "pro" provides comprehensive,
                    multi-angle research and is suited for complex topics that
                    span multiple subtopics or domains
                  enum:
                    - mini
                    - pro
                    - auto
                  default: auto
                stream:
                  type: boolean
                  description: >-
                    Whether to stream the research results as they are
                    generated. When 'true', returns a Server-Sent Events (SSE)
                    stream. See [Streaming
                    documentation](/documentation/api-reference/endpoint/research-streaming)
                    for details.
                  default: false
                output_schema:
                  type: object
                  description: >-
                    A JSON Schema object that defines the structure of the
                    research output. When provided, the research response will
                    be structured to match this schema, ensuring a predictable
                    and validated output shape. Must include a 'properties'
                    field, and may optionally include 'required' field.
                  default: null
                  properties:
                    properties:
                      type: object
                      description: >-
                        An object containing property definitions. Each key is a
                        property name, and each value is a property schema.
                      additionalProperties:
                        type: object
                        properties:
                          type:
                            type: string
                            enum:
                              - object
                              - string
                              - integer
                              - number
                              - array
                            description: >-
                              The type of the property. Must be one of: object,
                              string, integer, number, or array.
                          description:
                            type: string
                            description: A description of the property.
                          properties:
                            type: object
                            description: >-
                              Required when type is 'object'. Recursive
                              definition of object properties.
                          items:
                            type: object
                            description: >-
                              Required when type is 'array'. Defines the schema
                              for array items.
                        required:
                          - type
                          - description
                    required:
                      type: array
                      description: >-
                        An array of property names that are required. At least
                        one key from the properties object must be included.
                      items:
                        type: string
                  example:
                    properties:
                      company:
                        type: string
                        description: The name of the company
                      key_metrics:
                        type: array
                        description: List of key performance metrics
                        items:
                          type: string
                      financial_details:
                        type: object
                        description: Detailed financial breakdown
                        properties:
                          operating_income:
                            type: number
                            description: Operating income for the period
                    required:
                      - company
                citation_format:
                  type: string
                  description: The format for citations in the research report.
                  enum:
                    - numbered
                    - mla
                    - apa
                    - chicago
                  default: numbered
              required:
                - input
      responses:
        '201':
          description: Research task queued successfully (when not streaming)
          content:
            application/json:
              schema:
                type: object
                properties:
                  request_id:
                    type: string
                    description: A unique identifier for the research task.
                    example: 123e4567-e89b-12d3-a456-426614174111
                  created_at:
                    type: string
                    description: Timestamp when the research task was created.
                    example: '2025-01-15T10:30:00Z'
                  status:
                    type: string
                    description: The current status of the research task.
                    example: pending
                  input:
                    type: string
                    description: The research task or question investigated.
                    example: What are the latest developments in AI?
                  model:
                    type: string
                    description: The model used by the research agent.
                    example: mini
                  response_time:
                    type: integer
                    description: Time in seconds it took to complete the request.
                    example: 1.23
                required:
                  - request_id
                  - created_at
                  - status
                  - input
                  - model
                  - response_time
              example:
                request_id: 123e4567-e89b-12d3-a456-426614174111
                created_at: '2025-01-15T10:30:00Z'
                status: pending
                input: What are the latest developments in AI?
                model: mini
                response_time: 1.23
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
                  error: 'Invalid model. Must be one of: mini, pro, auto'
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
                    This request exceeds your plan's set usage limit. Please
                    upgrade your plan or contact support@tavily.com
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
                  error: Error when executing research task
      security:
        - bearerAuth: []
      x-codeSamples:
        - lang: python
          label: Python SDK
          source: >-
            from tavily import TavilyClient


            tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")

            response = tavily_client.research("What are the latest developments
            in AI?")


            print(response)
        - lang: javascript
          label: JavaScript SDK
          source: >-
            const { tavily } = require("@tavily/core");


            const tvly = tavily({ apiKey: "tvly-YOUR_API_KEY" });

            const response = await tvly.research("What are the latest
            developments in AI?");


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