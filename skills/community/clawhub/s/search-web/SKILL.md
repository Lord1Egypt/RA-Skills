# search_web

A local OpenClaw tool that performs internet searches using a self-hosted SearXNG instance.

This skill connects an OpenClaw agent to a running SearXNG server so the agent can retrieve
recent information from the internet. It sends a search query to the SearXNG HTTP API and
returns structured results containing titles and URLs.

## Why this skill exists

Language models often need information that may be newer than their training data.
By connecting the agent to a self-hosted SearXNG instance, the system can retrieve
fresh results from the web while remaining privacy-friendly and avoiding proprietary APIs.

## Typical agent use cases

An agent should call this tool when it needs to:

- find recent news or research
- check documentation for a technology
- verify facts from external sources
- gather links for further reading
- retrieve current information about blockchain, AI, or cybersecurity

## Parameters

query (string)  
The search query that will be sent to the SearXNG search endpoint.

Example query:

latest blockchain security research

## Output format

The tool returns JSON containing the top search results.

Example output:

[
  {
    "title": "Example article title",
    "url": "https://example.com/article"
  }
]

## Requirements

- SearXNG running locally
- Default endpoint: http://localhost:8080/search
- JSON response enabled

This skill is designed for self-hosted environments where the user wants a
private and customizable web search capability inside their OpenClaw agent.
