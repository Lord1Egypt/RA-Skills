# Space & Earth Science Explorer Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `space-earth-science-explorer`

x402 availability: not enabled for this product.

## `query_space_science_data`

Action slug: `query-space-science-data`

Price: `5` credits

Search across NASA, NOAA, and USGS public data sources using a natural-language query. Returns space imagery, scientific datasets, earthquake events, and earth observation records.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | `integer` | no | Maximum records to return. |
| `query` | `string` | yes | Natural-language query for space or science data. |
| `source` | `string` | no | Preferred source filter. nasa = NASA Image Library and NASA datasets, noaa = NOAA climate/ocean/weather datasets, usgs = USGS earthquakes and DOI datasets, all = query all sources. |
| `time_period` | `string` | no | Optional time period filter. Accepts 'latest', a single year like '2024', or a range like '2015:2024'. |

Sample parameters:

```json
{
  "limit": 20,
  "query": "example search query",
  "source": "all",
  "time_period": "example time period"
}
```

Generated JSON parameter schema:

```json
{
  "limit": {
    "default": 20,
    "description": "Maximum records to return.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "query": {
    "description": "Natural-language query for space or science data.",
    "required": true,
    "type": "string"
  },
  "source": {
    "default": "all",
    "description": "Preferred source filter. nasa = NASA Image Library and NASA datasets, noaa = NOAA climate/ocean/weather datasets, usgs = USGS earthquakes and DOI datasets, all = query all sources.",
    "enum": [
      "nasa",
      "noaa",
      "usgs",
      "all"
    ],
    "required": false,
    "type": "string"
  },
  "time_period": {
    "description": "Optional time period filter. Accepts 'latest', a single year like '2024', or a range like '2015:2024'.",
    "required": false,
    "type": "string"
  }
}
```
