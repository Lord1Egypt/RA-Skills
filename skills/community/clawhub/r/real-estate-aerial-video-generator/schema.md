# Real Estate Aerial Video Generator Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `real-estate-aerial-video-generator`

x402 availability: not enabled for this product.

## `fetch_existing_aerial_video`

Action slug: `fetch-existing-aerial-video`

Price: `0` credits

Retrieve a completed aerial video or check the status of a previous request. Provide either the original address or a prior video_id.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | `string` | no | Street address used for the video request. Provide this or video_id. |
| `video_id` | `string` | no | Video identifier from a previous aerial video request. Provide this or address. |

Sample parameters:

```json
{
  "address": "example address",
  "video_id": "example video id"
}
```

Generated JSON parameter schema:

```json
{
  "address": {
    "description": "Street address used for the video request. Provide this or video_id.",
    "required": false,
    "type": "string"
  },
  "video_id": {
    "description": "Video identifier from a previous aerial video request. Provide this or address.",
    "required": false,
    "type": "string"
  }
}
```

## `generate_aerial_video`

Action slug: `generate-aerial-video`

Price: `25` credits

Request an aerial video for a street address. If a video already exists for that address, return it immediately. Otherwise queue the request and return the current status.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | `string` | yes | Full street address for the property or location. |

Sample parameters:

```json
{
  "address": "example address"
}
```

Generated JSON parameter schema:

```json
{
  "address": {
    "description": "Full street address for the property or location.",
    "required": true,
    "type": "string"
  }
}
```
