---
name: voyager-travel-agent
description: "Alipay+ Voyager Travel Agent. Provides comprehensive travel solutions including flight search, hotel recommendations, and multi-day itinerary planning. Use when user mentions 'flight', 'airline', 'hotel', 'accommodation', 'itinerary', 'trip plan', or asks to search or book travel services."
license: MIT-0
---

# Alipay+ Voyager Travel Agent

Powered by Alipay+, a one-stop AI travel companion. Itinerary planning, service booking, travel companionship, all in one.

This skill coordinates multiple travel sub-skills to solve complex user requests. When a query spans multiple domains (e.g., "find flights and hotels for my Tokyo trip"), invoke the relevant sub-skills and combine their results.

## Workflow

1. Analyze the user query to identify which travel domains are involved
2. Load and execute the relevant sub-skill reference(s)
3. Combine results into a unified response

## Sub-skill References

| Sub-skill | Reference File |
|-----------|----------------|
| search-hotels | `references/search-hotels.md` |
| search-flights | `references/search-flights.md` |
| plan-itinerary | `references/plan-itinerary.md` |

Load the reference file to get the detailed workflow for each sub-skill.

## Configuration

**API Key**: This skill works without any API key for trial usage. For enhanced results with higher QPS, API key application is required (feature under development).

## Data & Privacy

**External Service Calls**: This skill invokes tools that make network requests to Alipay+ travel service endpoints. User query data (dates, cities, search terms) will be transmitted to these external services.
**Privacy Notice**: By using this skill, you acknowledge that your travel search queries will be processed by Alipay+ servers to provide recommendations.

## Output Guidelines

Present results in markdown format.

For hotels:
1. Group by city or theme into multiple options
2. Present 1-3 hotels per group in a balanced manner (avoid one group having too many while others have few)
3. Present hotels one by one within each group (not in a table)
4. Provide a comparison table at the end for easy side-by-side review

Each hotel includes: name, price, rating, image: `![{hotelName}]({hotelMainImage})`, booking link: `[Click to book]({jumpUrl})` (translate "Click to book" based on user language)

**CRITICAL**: name, price, rating, image, and booking link MUST be rendered in the output when available in the response data.