# Real Estate Sales Leasing and Valuations Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `real-estate-sales-leasing-and-valuations`

x402 availability: not enabled for this product.

## `market_statistics`

Action slug: `market-statistics`

Price: `25` credits

Get aggregated market data for a zip code

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `data_type` | `string` | no | Data type: All, Sale, or Rental |
| `history_range` | `integer` | no | Historical range in months (default 12) |
| `zip_code` | `string` | yes | 5-digit US zip code |

Sample parameters:

```json
{
  "data_type": "All",
  "history_range": 1,
  "zip_code": "example zip code"
}
```

Generated JSON parameter schema:

```json
{
  "data_type": {
    "description": "Data type: All, Sale, or Rental",
    "enum": [
      "All",
      "Sale",
      "Rental"
    ],
    "required": false,
    "type": "string"
  },
  "history_range": {
    "description": "Historical range in months (default 12)",
    "required": false,
    "type": "integer"
  },
  "zip_code": {
    "description": "5-digit US zip code",
    "required": true,
    "type": "string"
  }
}
```

## `property_details`

Action slug: `property-details`

Price: `25` credits

Get a single property record by ID

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `record_id` | `string` | yes | Property ID (e.g. '5500-Grand-Lake-Dr,-San-Antonio,-TX-78244') |

Sample parameters:

```json
{
  "record_id": "example record id"
}
```

Generated JSON parameter schema:

```json
{
  "record_id": {
    "description": "Property ID (e.g. '5500-Grand-Lake-Dr,-San-Antonio,-TX-78244')",
    "required": true,
    "type": "string"
  }
}
```

## `property_search`

Action slug: `property-search`

Price: `25` credits

Search property records by location and criteria

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | `string` | no | Full address or address with radius for area search |
| `bathrooms` | `string` | no | Bathrooms filter (supports ranges) |
| `bedrooms` | `string` | no | Bedrooms filter (supports ranges) |
| `city` | `string` | no | City name (case-sensitive) |
| `latitude` | `number` | no | Latitude for area search |
| `limit` | `integer` | no | Max results 1-500 (default 50) |
| `longitude` | `number` | no | Longitude for area search |
| `lot_size` | `string` | no | Lot size in sqft (supports ranges) |
| `offset` | `integer` | no | Pagination offset |
| `property_type` | `string` | no | Property type filter |
| `radius` | `number` | no | Search radius in miles (max 100) |
| `sale_date_range` | `string` | no | Days since last sold (min 1) |
| `square_footage` | `string` | no | Sqft filter (supports ranges) |
| `state` | `string` | no | 2-char state abbreviation |
| `year_built` | `string` | no | Year built (supports ranges) |
| `zip_code` | `string` | no | 5-digit zip code |

Sample parameters:

```json
{
  "address": "example address",
  "bathrooms": "example bathrooms",
  "bedrooms": "example bedrooms",
  "city": "example city",
  "latitude": 1,
  "limit": 1,
  "longitude": 1,
  "lot_size": "example lot size"
}
```

Generated JSON parameter schema:

```json
{
  "address": {
    "description": "Full address or address with radius for area search",
    "required": false,
    "type": "string"
  },
  "bathrooms": {
    "description": "Bathrooms filter (supports ranges)",
    "required": false,
    "type": "string"
  },
  "bedrooms": {
    "description": "Bedrooms filter (supports ranges)",
    "required": false,
    "type": "string"
  },
  "city": {
    "description": "City name (case-sensitive)",
    "required": false,
    "type": "string"
  },
  "latitude": {
    "description": "Latitude for area search",
    "required": false,
    "type": "number"
  },
  "limit": {
    "description": "Max results 1-500 (default 50)",
    "required": false,
    "type": "integer"
  },
  "longitude": {
    "description": "Longitude for area search",
    "required": false,
    "type": "number"
  },
  "lot_size": {
    "description": "Lot size in sqft (supports ranges)",
    "required": false,
    "type": "string"
  },
  "offset": {
    "description": "Pagination offset",
    "required": false,
    "type": "integer"
  },
  "property_type": {
    "description": "Property type filter",
    "enum": [
      "Single Family",
      "Condo",
      "Townhouse",
      "Manufactured",
      "Multi-Family",
      "Apartment",
      "Land"
    ],
    "required": false,
    "type": "string"
  },
  "radius": {
    "description": "Search radius in miles (max 100)",
    "required": false,
    "type": "number"
  },
  "sale_date_range": {
    "description": "Days since last sold (min 1)",
    "required": false,
    "type": "string"
  },
  "square_footage": {
    "description": "Sqft filter (supports ranges)",
    "required": false,
    "type": "string"
  },
  "state": {
    "description": "2-char state abbreviation",
    "required": false,
    "type": "string"
  },
  "year_built": {
    "description": "Year built (supports ranges)",
    "required": false,
    "type": "string"
  },
  "zip_code": {
    "description": "5-digit zip code",
    "required": false,
    "type": "string"
  }
}
```

## `rent_estimate`

Action slug: `rent-estimate`

Price: `25` credits

Get a rent estimate with comparable rentals

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | `string` | no | Full address: Street, City, State, Zip |
| `bathrooms` | `string` | no | Number of bathrooms |
| `bedrooms` | `string` | no | Number of bedrooms (0 for studio) |
| `comp_count` | `integer` | no | Number of comps (5-25, default 15) |
| `days_old` | `string` | no | Max days since comps were on market |
| `latitude` | `number` | no | Latitude (alternative to address) |
| `longitude` | `number` | no | Longitude (alternative to address) |
| `max_radius` | `number` | no | Max distance for comps in miles |
| `property_type` | `string` | no | Property type |
| `square_footage` | `string` | no | Living area in sqft |

Sample parameters:

```json
{
  "address": "example address",
  "bathrooms": "example bathrooms",
  "bedrooms": "example bedrooms",
  "comp_count": 1,
  "days_old": "example days old",
  "latitude": 1,
  "longitude": 1,
  "max_radius": 1
}
```

Generated JSON parameter schema:

```json
{
  "address": {
    "description": "Full address: Street, City, State, Zip",
    "required": false,
    "type": "string"
  },
  "bathrooms": {
    "description": "Number of bathrooms",
    "required": false,
    "type": "string"
  },
  "bedrooms": {
    "description": "Number of bedrooms (0 for studio)",
    "required": false,
    "type": "string"
  },
  "comp_count": {
    "description": "Number of comps (5-25, default 15)",
    "required": false,
    "type": "integer"
  },
  "days_old": {
    "description": "Max days since comps were on market",
    "required": false,
    "type": "string"
  },
  "latitude": {
    "description": "Latitude (alternative to address)",
    "required": false,
    "type": "number"
  },
  "longitude": {
    "description": "Longitude (alternative to address)",
    "required": false,
    "type": "number"
  },
  "max_radius": {
    "description": "Max distance for comps in miles",
    "required": false,
    "type": "number"
  },
  "property_type": {
    "description": "Property type",
    "enum": [
      "Single Family",
      "Condo",
      "Townhouse",
      "Manufactured",
      "Multi-Family",
      "Apartment"
    ],
    "required": false,
    "type": "string"
  },
  "square_footage": {
    "description": "Living area in sqft",
    "required": false,
    "type": "string"
  }
}
```

## `rental_listing_details`

Action slug: `rental-listing-details`

Price: `25` credits

Get a single rental listing by ID

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `record_id` | `string` | yes | Listing ID |

Sample parameters:

```json
{
  "record_id": "example record id"
}
```

Generated JSON parameter schema:

```json
{
  "record_id": {
    "description": "Listing ID",
    "required": true,
    "type": "string"
  }
}
```

## `rental_listings`

Action slug: `rental-listings`

Price: `25` credits

Search rental listings in an area

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | `string` | no | Full address or address with radius |
| `bathrooms` | `string` | no | Bathrooms filter |
| `bedrooms` | `string` | no | Bedrooms filter |
| `city` | `string` | no | City name (case-sensitive) |
| `days_old` | `string` | no | Days since listed |
| `latitude` | `number` | no | Latitude for area search |
| `limit` | `integer` | no | Max results 1-500 (default 50) |
| `longitude` | `number` | no | Longitude for area search |
| `lot_size` | `string` | no | Lot size filter |
| `offset` | `integer` | no | Pagination offset |
| `price` | `string` | no | Price filter (supports ranges) |
| `property_type` | `string` | no | Property type filter |
| `radius` | `number` | no | Search radius in miles (max 100) |
| `square_footage` | `string` | no | Sqft filter |
| `state` | `string` | no | 2-char state abbreviation |
| `status` | `string` | no | Listing status |
| `year_built` | `string` | no | Year built filter |
| `zip_code` | `string` | no | 5-digit zip code |

Sample parameters:

```json
{
  "address": "example address",
  "bathrooms": "example bathrooms",
  "bedrooms": "example bedrooms",
  "city": "example city",
  "days_old": "example days old",
  "latitude": 1,
  "limit": 1,
  "longitude": 1
}
```

Generated JSON parameter schema:

```json
{
  "address": {
    "description": "Full address or address with radius",
    "required": false,
    "type": "string"
  },
  "bathrooms": {
    "description": "Bathrooms filter",
    "required": false,
    "type": "string"
  },
  "bedrooms": {
    "description": "Bedrooms filter",
    "required": false,
    "type": "string"
  },
  "city": {
    "description": "City name (case-sensitive)",
    "required": false,
    "type": "string"
  },
  "days_old": {
    "description": "Days since listed",
    "required": false,
    "type": "string"
  },
  "latitude": {
    "description": "Latitude for area search",
    "required": false,
    "type": "number"
  },
  "limit": {
    "description": "Max results 1-500 (default 50)",
    "required": false,
    "type": "integer"
  },
  "longitude": {
    "description": "Longitude for area search",
    "required": false,
    "type": "number"
  },
  "lot_size": {
    "description": "Lot size filter",
    "required": false,
    "type": "string"
  },
  "offset": {
    "description": "Pagination offset",
    "required": false,
    "type": "integer"
  },
  "price": {
    "description": "Price filter (supports ranges)",
    "required": false,
    "type": "string"
  },
  "property_type": {
    "description": "Property type filter",
    "enum": [
      "Single Family",
      "Condo",
      "Townhouse",
      "Manufactured",
      "Multi-Family",
      "Apartment"
    ],
    "required": false,
    "type": "string"
  },
  "radius": {
    "description": "Search radius in miles (max 100)",
    "required": false,
    "type": "number"
  },
  "square_footage": {
    "description": "Sqft filter",
    "required": false,
    "type": "string"
  },
  "state": {
    "description": "2-char state abbreviation",
    "required": false,
    "type": "string"
  },
  "status": {
    "description": "Listing status",
    "enum": [
      "Active",
      "Inactive"
    ],
    "required": false,
    "type": "string"
  },
  "year_built": {
    "description": "Year built filter",
    "required": false,
    "type": "string"
  },
  "zip_code": {
    "description": "5-digit zip code",
    "required": false,
    "type": "string"
  }
}
```

## `sale_listing_details`

Action slug: `sale-listing-details`

Price: `25` credits

Get a single sale listing by ID

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `record_id` | `string` | yes | Listing ID |

Sample parameters:

```json
{
  "record_id": "example record id"
}
```

Generated JSON parameter schema:

```json
{
  "record_id": {
    "description": "Listing ID",
    "required": true,
    "type": "string"
  }
}
```

## `sale_listings`

Action slug: `sale-listings`

Price: `25` credits

Search sale listings in an area

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | `string` | no | Full address or address with radius |
| `bathrooms` | `string` | no | Bathrooms filter |
| `bedrooms` | `string` | no | Bedrooms filter |
| `city` | `string` | no | City name (case-sensitive) |
| `days_old` | `string` | no | Days since listed |
| `latitude` | `number` | no | Latitude for area search |
| `limit` | `integer` | no | Max results 1-500 (default 50) |
| `longitude` | `number` | no | Longitude for area search |
| `lot_size` | `string` | no | Lot size filter |
| `offset` | `integer` | no | Pagination offset |
| `price` | `string` | no | Price filter (supports ranges) |
| `property_type` | `string` | no | Property type filter |
| `radius` | `number` | no | Search radius in miles (max 100) |
| `square_footage` | `string` | no | Sqft filter |
| `state` | `string` | no | 2-char state abbreviation |
| `status` | `string` | no | Listing status |
| `year_built` | `string` | no | Year built filter |
| `zip_code` | `string` | no | 5-digit zip code |

Sample parameters:

```json
{
  "address": "example address",
  "bathrooms": "example bathrooms",
  "bedrooms": "example bedrooms",
  "city": "example city",
  "days_old": "example days old",
  "latitude": 1,
  "limit": 1,
  "longitude": 1
}
```

Generated JSON parameter schema:

```json
{
  "address": {
    "description": "Full address or address with radius",
    "required": false,
    "type": "string"
  },
  "bathrooms": {
    "description": "Bathrooms filter",
    "required": false,
    "type": "string"
  },
  "bedrooms": {
    "description": "Bedrooms filter",
    "required": false,
    "type": "string"
  },
  "city": {
    "description": "City name (case-sensitive)",
    "required": false,
    "type": "string"
  },
  "days_old": {
    "description": "Days since listed",
    "required": false,
    "type": "string"
  },
  "latitude": {
    "description": "Latitude for area search",
    "required": false,
    "type": "number"
  },
  "limit": {
    "description": "Max results 1-500 (default 50)",
    "required": false,
    "type": "integer"
  },
  "longitude": {
    "description": "Longitude for area search",
    "required": false,
    "type": "number"
  },
  "lot_size": {
    "description": "Lot size filter",
    "required": false,
    "type": "string"
  },
  "offset": {
    "description": "Pagination offset",
    "required": false,
    "type": "integer"
  },
  "price": {
    "description": "Price filter (supports ranges)",
    "required": false,
    "type": "string"
  },
  "property_type": {
    "description": "Property type filter",
    "enum": [
      "Single Family",
      "Condo",
      "Townhouse",
      "Manufactured",
      "Multi-Family",
      "Apartment",
      "Land"
    ],
    "required": false,
    "type": "string"
  },
  "radius": {
    "description": "Search radius in miles (max 100)",
    "required": false,
    "type": "number"
  },
  "square_footage": {
    "description": "Sqft filter",
    "required": false,
    "type": "string"
  },
  "state": {
    "description": "2-char state abbreviation",
    "required": false,
    "type": "string"
  },
  "status": {
    "description": "Listing status",
    "enum": [
      "Active",
      "Inactive"
    ],
    "required": false,
    "type": "string"
  },
  "year_built": {
    "description": "Year built filter",
    "required": false,
    "type": "string"
  },
  "zip_code": {
    "description": "5-digit zip code",
    "required": false,
    "type": "string"
  }
}
```

## `value_estimate`

Action slug: `value-estimate`

Price: `25` credits

Get a property value estimate with comparable sales

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | `string` | no | Full address: Street, City, State, Zip |
| `bathrooms` | `string` | no | Number of bathrooms |
| `bedrooms` | `string` | no | Number of bedrooms (0 for studio) |
| `comp_count` | `integer` | no | Number of comps (5-25, default 15) |
| `days_old` | `string` | no | Max days since comps were on market |
| `latitude` | `number` | no | Latitude (alternative to address) |
| `longitude` | `number` | no | Longitude (alternative to address) |
| `max_radius` | `number` | no | Max distance for comps in miles |
| `property_type` | `string` | no | Property type |
| `square_footage` | `string` | no | Living area in sqft |

Sample parameters:

```json
{
  "address": "example address",
  "bathrooms": "example bathrooms",
  "bedrooms": "example bedrooms",
  "comp_count": 1,
  "days_old": "example days old",
  "latitude": 1,
  "longitude": 1,
  "max_radius": 1
}
```

Generated JSON parameter schema:

```json
{
  "address": {
    "description": "Full address: Street, City, State, Zip",
    "required": false,
    "type": "string"
  },
  "bathrooms": {
    "description": "Number of bathrooms",
    "required": false,
    "type": "string"
  },
  "bedrooms": {
    "description": "Number of bedrooms (0 for studio)",
    "required": false,
    "type": "string"
  },
  "comp_count": {
    "description": "Number of comps (5-25, default 15)",
    "required": false,
    "type": "integer"
  },
  "days_old": {
    "description": "Max days since comps were on market",
    "required": false,
    "type": "string"
  },
  "latitude": {
    "description": "Latitude (alternative to address)",
    "required": false,
    "type": "number"
  },
  "longitude": {
    "description": "Longitude (alternative to address)",
    "required": false,
    "type": "number"
  },
  "max_radius": {
    "description": "Max distance for comps in miles",
    "required": false,
    "type": "number"
  },
  "property_type": {
    "description": "Property type",
    "enum": [
      "Single Family",
      "Condo",
      "Townhouse",
      "Manufactured",
      "Multi-Family",
      "Apartment",
      "Land"
    ],
    "required": false,
    "type": "string"
  },
  "square_footage": {
    "description": "Living area in sqft",
    "required": false,
    "type": "string"
  }
}
```
