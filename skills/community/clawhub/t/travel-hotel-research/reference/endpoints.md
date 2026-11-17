# travel-hotel-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**71 endpoints across 10 platform group(s).**

## Booking (8)

### `booking_attractions_detail`

- **HTTP:** `GET /booking-attractions/detail`
- **What:** Booking.com attraction detail. Returns the details of one Booking.com attraction by `slug`, taken from `products[].slug` in a `booking-attractions-search` result: `name`, `short_description`, `description`, `duration`, `price` with `currency`, `review_score`, `review_count` and `city`. The returned `id` is the `product_id` for `booking-attractions-reviews`.
- **Params:** `slug` (string, **required**) — Attraction slug, from a prior attraction search result

### `booking_attractions_reviews`

- **HTTP:** `GET /booking-attractions/reviews`
- **What:** Booking.com attraction reviews. Returns guest reviews for a Booking.com attraction. `product_id` is required and comes from `products[].id` in a `booking-attractions-search` result. `page` is 1-based (default 1) and `limit` is 1 to 50 (default 10). Each review has `score`, `content`, `reviewer_name`, `reviewer_country`, `language` and `reviewed_date`, and `total` gives the count.
- **Params:** `limit` (integer, optional) — Reviews per page, 1-50, default 10; `page` (integer, optional) — 1-based result page, default 1; `product_id` (string, **required**) — Attraction product id, from a prior attraction search result

### `booking_attractions_search`

- **HTTP:** `GET /booking-attractions/search`
- **What:** Search Booking.com attractions. Returns Booking.com attractions/things-to-do search results for a destination and date range, with an optional category/subcategory filter and a discoverable category taxonomy.
- **Params:** `category` (string, optional) — Optional top-level category tagname filter, from a prior response's categories; `end_date` (string, optional) — Availability end date, YYYY-MM-DD, defaults to start_date; `limit` (integer, optional) — Results per page, 1-30, default 15; `page` (integer, optional) — 1-based result page, default 1; `query` (string, **required**) — Destination name or city; `start_date` (string, **required**) — Availability start date, YYYY-MM-DD; `subcategory` (string, optional) — Optional subcategory tagname filter, from a prior response's categories

### `booking_flights_autocomplete`

- **HTTP:** `GET /booking-flights/autocomplete`
- **What:** Booking.com flight autocomplete. Returns Booking.com flight-search location suggestions (airports and cities) for `query`, which is required. `type` is `to` (default) or `from`; `origin` and `origin_type` bias results by proximity. Each result has `name`, `code`, `type`, `country`, `country_name` and `region_name`. Combine `code` and `type` as `{code}.{TYPE}` for `booking-flights-search`.
- **Params:** `origin` (string, optional) — Optional origin location code, biases results by proximity; `origin_type` (string, optional) — Origin location type; `query` (string, **required**) — City or airport name/code to search; `type` (string, optional) — Location role, default to

### `booking_flights_search`

- **HTTP:** `GET /booking-flights/search`
- **What:** Search Booking.com flights. Returns Booking.com flight offers between two locations given as `from` and `to` (such as `SGN.AIRPORT`), for a `depart` date. `type` is `ROUNDTRIP` (default, needs `return`) or `ONEWAY`. Also takes `adults` (1 to 9), `children`, `cabin_class` and `sort`. Offers carry `price`, `currency` and segments with legs; the response adds `total_count` and `min_price`.
- **Params:** `adults` (integer, optional) — Number of adults, 1-9, default 1; `cabin_class` (string, optional) — Cabin class, default ECONOMY; `children` (integer, optional) — Number of children, 0-9; `depart` (string, **required**) — Departure date, YYYY-MM-DD; `from` (string, **required**) — Origin location id, e.g. SGN.AIRPORT, from a prior autocomplete result; `from_country` (string, optional) — Origin country code; `return` (string, optional) — Return date, YYYY-MM-DD, required when type is ROUNDTRIP; `sort` (string, optional) — Result sort order, default BEST; `to` (string, **required**) — Destination location id, same composite format as from; `to_country` (string, optional) — Destination country code; `type` (string, optional) — Trip type, default ROUNDTRIP

### `booking_hotel_detail`

- **HTTP:** `GET /booking/hotel-detail`
- **What:** Booking.com hotel detail. Returns a Booking.com hotel's core detail page: rating, facilities, highlights, house rules, cover photos, and rooms with their own photos.
- **Params:** `hotel_id` (integer, **required**) — Booking.com hotel id, from a prior search's property id

### `booking_reviews`

- **HTTP:** `GET /booking/reviews`
- **What:** Booking.com hotel reviews. Returns guest reviews for a Booking.com hotel. `hotel_id` and `hotel_country_code` are required, both from a `booking-search` result. `search_text` filters review content, `page` is 1-based and `limit` is 1 to 25 (default 10). Reviews have `score`, `title`, `positive_text`, `negative_text`, `room_type` and stay dates; `rating_scores` and `reviews_count` summarise the hotel.
- **Params:** `destination_id` (integer, optional) — Destination id (ufi), from a prior search response; `hotel_country_code` (string, **required**) — Hotel's country code, from a prior search response; `hotel_id` (integer, **required**) — Booking.com hotel id, from a prior search's property id; `hotel_score` (number, optional) — Hotel's overall review score; `limit` (integer, optional) — Reviews per page, 1-25, default 10; `page` (integer, optional) — 1-based result page, default 1; `search_text` (string, optional) — Optional free-text search over review content

### `booking_search`

- **HTTP:** `GET /booking/search`
- **What:** Search Booking.com hotels. Searches Booking.com hotels for a destination `query` between `checkin` and `checkout` (`YYYY-MM-DD`, both required). `adults` is 1 to 9 (default 2), `rooms` 1 to 8 (default 1), `children` 0 to 9, and `page` is 1-based. Each property has `name`, `price`, `currency`, `review_score`, `star_rating` and `distance`; `results_count` gives the total.
- **Params:** `adults` (integer, optional) — Number of adults, 1-9, default 2; `checkin` (string, **required**) — Check-in date, YYYY-MM-DD; `checkout` (string, **required**) — Check-out date, YYYY-MM-DD; `children` (integer, optional) — Number of children, 0-9; `page` (integer, optional) — 1-based result page, default 1; `query` (string, **required**) — Destination name or city; `rooms` (integer, optional) — Number of rooms, 1-8, default 1

## Expedia (7)

### `expedia_activities_search`

- **HTTP:** `POST /expedia/activities/search`
- **What:** Search Expedia activities. Searches Expedia things to do (activities and tours) for a free-text `destination` between `start_date` and `end_date` (`YYYY-MM-DD`), all required in the JSON body. Optional `page`, `page_size` (1-50, default 20), `currency` (default `USD`) and `locale` (default `en_US`). Each activity has its id, name, duration, price, review score and label, review count, free-cancellation flag and thumbnail.
- **Params:** `option` (object, **required**) — Activity search payload
- **REST body:** Send the value of the MCP argument `option` directly as the JSON body; do not wrap it in a `option` property.

### `expedia_flights_search`

- **HTTP:** `POST /expedia/flights/search`
- **What:** Search Expedia flights. Searches Expedia flights between two IATA airport codes, `origin` and `destination`, on `departure_date` (`YYYY-MM-DD`). `return_date` is required for the default `round_trip`; `one_way` is the alternative `trip_type`. Optional `adults` (1-9, default 1), `cabin_class` (default `COACH`), `currency` and `locale`. Returns departing-leg offers only, with airline, times, duration, stops, route and price.
- **Params:** `option` (object, **required**) — Flights search payload
- **REST body:** Send the value of the MCP argument `option` directly as the JSON body; do not wrap it in a `option` property.

### `expedia_locations_search`

- **HTTP:** `POST /expedia/locations/search`
- **What:** Search Expedia destinations. Returns Expedia destination and property suggestions for a free-text `term` (required, 100 characters or fewer), with optional `currency` and `locale`. Each item has its type, geo type, primary and secondary text, full location name, coordinates, and `region_id`, `property_id` or `airport_code` where they exist.
- **Params:** `option` (object, **required**) — Location search payload
- **REST body:** Send the value of the MCP argument `option` directly as the JSON body; do not wrap it in a `option` property.

### `expedia_properties_detail`

- **HTTP:** `POST /expedia/properties/detail`
- **What:** Expedia Stays property detail. Returns a summary for one Expedia hotel by `property_id`, for the stay given by `check_in` and `check_out` (`YYYY-MM-DD`), all required in the JSON body. Optional `adults` (1-9, default 2), `currency` and `locale`. The response has the name, star rating, address, city, province, country code, coordinates, top amenities and VIP message.
- **Params:** `option` (object, **required**) — Property detail payload
- **REST body:** Send the value of the MCP argument `option` directly as the JSON body; do not wrap it in a `option` property.

### `expedia_properties_filters`

- **HTTP:** `POST /expedia/properties/filters`
- **What:** Expedia search filters. Returns the sort and filter facets (amenities, star rating, neighborhood, nightly price range, sort options) available for a Stays search.
- **Params:** `option` (object, **required**) — Property filters payload
- **REST body:** Send the value of the MCP argument `option` directly as the JSON body; do not wrap it in a `option` property.

### `expedia_properties_reviews`

- **HTTP:** `POST /expedia/properties/reviews`
- **What:** Expedia Stays property guest reviews. Returns the overall rating and a short set of guest reviews, typically around six, for one Expedia hotel. `property_id`, `check_in` and `check_out` (`YYYY-MM-DD`) are required in the JSON body; `adults` (1-9, default 2), `currency` and `locale` are optional. Each review has the reviewer name, date, rating label, message and verified flag. It is not the full review archive.
- **Params:** `option` (object, **required**) — Property reviews payload
- **REST body:** Send the value of the MCP argument `option` directly as the JSON body; do not wrap it in a `option` property.

### `expedia_properties_search`

- **HTTP:** `POST /expedia/properties/search`
- **What:** Search Expedia Stays properties. Returns Expedia Stays (hotel) search results for a free-text destination and date range. Promotional banners and sponsored ad slots are dropped, so every returned property has an id and name.
- **Params:** `option` (object, **required**) — Property search payload
- **REST body:** Send the value of the MCP argument `option` directly as the JSON body; do not wrap it in a `option` property.

## Agoda (8)

### `agoda_activities_search`

- **HTTP:** `GET /agoda/activities/search`
- **What:** Search Agoda activities. Returns Agoda activities (tours, attractions, experiences) matching a free-text keyword and/or a city. When keyword is omitted, the resolved city's name is used instead to return a general listing of activities in that city. Callers may supply a known Agoda city id or a free-text city name for the city filter; when both are supplied city_id takes precedence.
- **Params:** `city` (string, optional) — Free-text city name, used directly as the search text when keyword is omitted, and to resolve a city id filter.; `city_id` (integer, optional) — Numeric Agoda city id to filter results to. Optional if keyword is supplied; city_id takes precedence over city when both are supplied.; `keyword` (string, optional) — Free-text activity search keyword. When omitted, the resolved city's name is used instead.

### `agoda_activity_detail`

- **HTTP:** `GET /agoda/activities/{activity_id}`
- **What:** Get Agoda activity detail. Returns full activity detail from Agoda: title, description, stated duration, categories, and content images.
- **Params:** `activity_id` (string, **required**) — Numeric Agoda activity id, from a prior activities search call's activity_id field

### `agoda_flights_itinerary_amenities`

- **HTTP:** `POST /agoda/flights/itinerary-amenities`
- **What:** Get Agoda flight segment amenities. Returns real-content amenities (aircraft type, seat layout, meals, entertainment, wifi) for one or more flight segments. Copy the segments straight from a flight search response's own segment fields.
- **Params:** `body` (object, **required**) — One or more flight segments to fetch amenities for
- **REST body:** Send the value of the MCP argument `body` directly as the JSON body; do not wrap it in a `body` property.

### `agoda_flights_search`

- **HTTP:** `GET /agoda/flights/search`
- **What:** Search Agoda one-way flights. Returns bookable one-way flight itineraries between two IATA airport codes for a departure date, including per-segment flight number, airline, times, layovers, aircraft type, and price. Resolve free-text city/airport names to codes first via the flight destination search endpoint.
- **Params:** `adults` (integer, optional) — Adult passengers (age 12+), defaults to 1; `cabin_class` (string, optional) — Cabin class, defaults to Economy; `children` (integer, optional) — Child passengers (age 2-11), defaults to 0; `departure_date` (string, **required**) — Departure date, YYYY-MM-DD; `destination` (string, **required**) — Destination IATA airport code; `infants` (integer, optional) — Infant passengers (under age 2), defaults to 0; `origin` (string, **required**) — Origin IATA airport code; `page` (integer, optional) — 1-indexed result page, defaults to 1

### `agoda_flights_search_locations`

- **HTTP:** `GET /agoda/flights/search-locations`
- **What:** Search Agoda flight destinations/airports. Resolves a free-text city or airport name into IATA airport codes for flight search, with each city's direct and nearby airports.
- **Params:** `keyword` (string, **required**) — Free-text city or airport name

### `agoda_homes_search`

- **HTTP:** `GET /agoda/homes/search`
- **What:** Search Agoda Homes & Apartments by city. Returns Homes & Apartments results for an Agoda city: full listing detail for every matching property whose accommodation type is Apartment. Callers may supply a known Agoda city id or a free-text city name; when both are supplied city_id takes precedence.
- **Params:** `city` (string, optional) — Free-text city name, resolved to a numeric city id via Agoda's own destination search. Ignored when city_id is also supplied.; `city_id` (integer, optional) — Numeric Agoda city id, e.g. 9395 for Bangkok. Either city_id or city is required; city_id takes precedence when both are supplied.; `limit` (integer, optional) — Candidate listings fetched per page before filtering to homes/apartments, defaults to 10, maximum 50; `page` (integer, optional) — 1-indexed result page over the underlying city search, defaults to 1

### `agoda_hotel_detail`

- **HTTP:** `GET /agoda/hotels/{property_id}`
- **What:** Get Agoda hotel detail. Returns full hotel detail from Agoda: identity (name, any former name), an accommodation type code, address (street address, postal code, city, country), guest rating, a main photo, room count, hotel chain id, a long and short description, and short-form policy statements (minimum age, adult/child definitions, extra-bed and additional-room booking policy).
- **Params:** `property_id` (string, **required**) — Numeric Agoda property id, from a prior search call's property_id field or the id embedded in an Agoda hotel URL

### `agoda_hotels_search`

- **HTTP:** `GET /agoda/hotels/search`
- **What:** Search Agoda hotels by city. Returns hotel search results for an Agoda city: the matching property ids for that city plus a direct link to each property's listing page. Callers may supply a known Agoda city id or a free-text city name; when both are supplied city_id takes precedence.
- **Params:** `city` (string, optional) — Free-text city name, resolved to a numeric city id via Agoda's own destination search. Ignored when city_id is also supplied.; `city_id` (integer, optional) — Numeric Agoda city id, e.g. 9395 for Bangkok. Either city_id or city is required; city_id takes precedence when both are supplied.; `limit` (integer, optional) — Results per page, defaults to 10, maximum 50; `page` (integer, optional) — 1-indexed result page, defaults to 1

## TripAdvisor (6)

### `tripadvisor_autocomplete`

- **HTTP:** `GET /tripadvisor/autocomplete`
- **What:** Autocomplete TripAdvisor locations and places. Returns TripAdvisor typeahead suggestions for the required query `q`, optionally narrowed by `limit`, `locale`, `scope_geo_id` and a `type` hint. Each result has its id, title, type, URL, image, parent location and coordinates, and may carry nested search shortcuts. Results can be locations, hotels, restaurants or attractions.
- **Params:** `limit` (integer, optional) — Maximum results; `locale` (string, optional) — TripAdvisor locale; `q` (string, **required**) — Autocomplete query; `route_uid` (string, optional) — Optional captured route uid; `scope_geo_id` (integer, optional) — Optional scoped geo id; `search_session_id` (string, optional) — Optional captured search session id; `type` (string, optional) — Optional result type hint; `typeahead_id` (string, optional) — Optional captured typeahead id

### `tripadvisor_enums`

- **HTTP:** `GET /tripadvisor/enums`
- **What:** Get TripAdvisor enum metadata. Returns the values TripAdvisor place and listing filters accept: `locales`, `currencies`, `languages`, `listing_types`, `sorts`, `pricing_modes`, `hotel_classes`, `hotel_amenities`, `restaurant_types`, `restaurant_options`, attraction categories with their ids, and `filter_ids`. It also lists `unsupported_entity_types`. Takes no parameters.
- **Params:** _none_

### `tripadvisor_hotels`

- **HTTP:** `GET /tripadvisor/hotels`
- **What:** Search TripAdvisor hotels. Searches TripAdvisor hotels in the area given by the required `geo_id`. Filter with `class`, `amenities`, `price_min`, `price_max`, `pricing_mode`, `travelers_choice` and `currency`; page with `offset` and `limit`; order with `sort`. Each hotel has its title, URL, image, rating, review count, star rating, rank, price, provider, location and a review snippet when TripAdvisor supplies them.
- **Params:** `amenities` (array, optional) — Amenity filter ids; `class` (integer, optional) — Hotel class filter; `currency` (string, optional) — Currency code; `filter_id` (string, optional) — Optional filter id such as class or ufe; `geo_id` (integer, **required**) — TripAdvisor geo id; `limit` (integer, optional) — Maximum results; `offset` (integer, optional) — Zero-based result offset; `price_max` (integer, optional) — Maximum price filter; `price_min` (integer, optional) — Minimum price filter; `pricing_mode` (string, optional) — Pricing mode; `sort` (string, optional) — Sort value; `travelers_choice` (boolean, optional) — Filter Travelers' Choice properties; `travelers_choice_botb` (boolean, optional) — Filter Best of the Best properties

### `tripadvisor_place`

- **HTTP:** `GET /tripadvisor/place`
- **What:** Get TripAdvisor place. Returns a rich TripAdvisor place profile.
- **Params:** `id` (string, optional) — TripAdvisor location id fallback; `url` (string, optional) — TripAdvisor place URL

### `tripadvisor_reviews`

- **HTTP:** `GET /tripadvisor/reviews`
- **What:** Get TripAdvisor reviews. Returns reviews for a TripAdvisor place identified by `id` (location id) or `url`. `limit` defaults to 20 (max 50); `page` is 1-based; `language`, `ratings` (1 to 5) and `sort_by` refine the list. Each review has author, title, text, dates, rating, language, helpful votes, photos and URL. A page beyond `total` returns an empty `reviews` array.
- **Params:** `do_machine_translation` (boolean, optional) — Enable upstream machine translation; `id` (string, optional) — TripAdvisor location id; `language` (string, optional) — Review language; `limit` (integer, optional) — Maximum reviews; `page` (integer, optional) — 1-based review page; `photos_per_review_limit` (integer, optional) — Maximum photos per review; `ratings` (array, optional) — Rating filters; `sort_by` (string, optional) — Legacy sort field; DATE selects newest first, FAVORABLE_RATING uses upstream order; `sort_type` (string, optional) — Legacy sort type; DEFAULT selects newest first, ML_SORTED uses upstream order unless sort_by is DATE; `url` (string, optional) — TripAdvisor place URL

### `tripadvisor_search`

- **HTTP:** `GET /tripadvisor/search`
- **What:** Search TripAdvisor places. Searches TripAdvisor places in the area given by the required `geo_id`, for the required `type`: `hotel`, `restaurant`, `attraction`, `all`, or an attraction category type from `/tripadvisor/enums`. Hotel and restaurant filters, `offset`, `limit`, `locale`, `currency` and `sort` are optional. Each result has title, URL, rating, review count, rank, price and location. Unsupported entity-only types return a validation error.
- **Params:** `amenities` (array, optional) — Hotel amenity filter ids; `class` (integer, optional) — Hotel class filter; `currency` (string, optional) — Currency code; `establishment_types` (array, optional) — Restaurant establishment type ids; `filter_id` (string, optional) — Optional hotel filter id; `geo_id` (integer, **required**) — TripAdvisor geo id; `limit` (integer, optional) — Maximum results; `locale` (string, optional) — TripAdvisor locale; `offset` (integer, optional) — Zero-based result offset; `online_options` (array, optional) — Restaurant online option ids; `price_max` (integer, optional) — Maximum hotel price filter; `price_min` (integer, optional) — Minimum hotel price filter; `pricing_mode` (string, optional) — Hotel pricing mode; `restaurant_date` (string, optional) — Restaurant availability date; `restaurant_guests` (integer, optional) — Restaurant guest count; `restaurant_time` (string, optional) — Restaurant availability time; `sort` (string, optional) — Sort value; `travelers_choice` (boolean, optional) — Filter Travelers' Choice hotels; `travelers_choice_botb` (boolean, optional) — Filter Best of the Best hotels; `type` (string, **required**) — Listing type

## Trip.com (2)

### `tripcom_hotel_detail`

- **HTTP:** `GET /tripcom/hotels/{id}`
- **What:** Get Trip.com hotel detail. Returns a Trip.com hotel-detail page: identity (name, local name, star rating, city/province/country), location (address, zone, latitude/longitude, nearby-transport description), guest rating (overall score plus cleanliness/amenities/location/service breakdown), images, description, check-in/check-out and child policy summaries, and popular facilities. Pricing is not included: Trip.com's detail page only returns per-night rates alongside check-in/check-out dates, which this endpoint does not take as input -- use the search endpoint for a city's current display prices.
- **Params:** `id` (string, **required**) — Trip.com hotel id, from a prior search call's hotel_id field; `slug` (string, optional) — Optional slug segment for a nicer canonical source URL (e.g. the district/city slug from a search result's url). Not required and not validated by Trip.com.

### `tripcom_hotels_search`

- **HTTP:** `GET /tripcom/hotels/search`
- **What:** Search Trip.com hotels by city. Returns Trip.com's own top-hotels page for a city: hotel summaries (name, location, star rating, guest rating, review count, image, display price) for the hotels Trip.com features on that city's hotel-list page. Trip.com does not expose a free-text city search, so callers supply the exact city_slug and city_id pair from a known Trip.com hotel-list URL of the form https://www.trip.com/hotels/{city_slug}-hotels-list-{city_id}/.
- **Params:** `city_id` (string, **required**) — Trip.com numeric city id, the trailing number of a /hotels/{city_slug}-hotels-list-{city_id}/ URL; `city_slug` (string, **required**) — Trip.com city slug, the text segment of a /hotels/{city_slug}-hotels-list-{city_id}/ URL

## Airbnb (7)

### `airbnb_host`

- **HTTP:** `GET /airbnb/host/{id}`
- **What:** Get Airbnb host profile. Returns an Airbnb public host profile — display name, Superhost and identity-verification status, location, bio, hosting tenure, total guest-review count, and total listing count.
- **Params:** `id` (string, **required**) — Host id (numeric)

### `airbnb_host_listings`

- **HTTP:** `GET /airbnb/host/{id}/listings`
- **What:** Get Airbnb host listings. Returns the listings an Airbnb host manages, paginated. Page 1 comes from the host profile; deeper pages page through the host's full portfolio.
- **Params:** `id` (string, **required**) — Host id (numeric); `page` (integer, optional) — 1-based page

### `airbnb_host_reviews`

- **HTTP:** `GET /airbnb/host/{id}/reviews`
- **What:** Get Airbnb host reviews. Returns the reviews guests left for an Airbnb host, identified by the numeric host `id`. `page` is 1-based (default 1). Each review has its `id`, `rating`, `comments`, `created_at`, `reviewer` name and `reviewer_location`, and `has_more` says whether another page follows.
- **Params:** `id` (string, **required**) — Host id (numeric); `page` (integer, optional) — 1-based page

### `airbnb_room`

- **HTTP:** `GET /airbnb/room/{id}`
- **What:** Get Airbnb room. Returns the public details of one Airbnb listing by room id: title, description, property type, location and coordinates, guest capacity, amenities, price and price per night, rating, review count, host, and the Superhost and Guest Favorite flags. Some fields are present only when Airbnb exposes them for the listing.
- **Params:** `id` (string, **required**) — Room id

### `airbnb_room_calendar`

- **HTTP:** `GET /airbnb/room/{id}/calendar`
- **What:** Get Airbnb room calendar. Returns the public availability calendar for one Airbnb room, grouped by month. Each day carries its date, whether it is available and bookable, whether it can be a check-in or check-out day, and the minimum and maximum nights. Months are returned only when Airbnb exposes them for the listing.
- **Params:** `id` (string, **required**) — Room id

### `airbnb_room_reviews`

- **HTTP:** `GET /airbnb/room/{id}/reviews`
- **What:** Get Airbnb room reviews. Returns public guest reviews for one Airbnb room by room id, one page at a time (`page` is 1-based). Each review has the author, date, rating and text. Reviews are returned only when Airbnb exposes them for the listing.
- **Params:** `id` (string, **required**) — Room id; `page` (integer, optional) — 1-based page

### `airbnb_search`

- **HTTP:** `GET /airbnb/search`
- **What:** Search Airbnb stays. Searches public Airbnb stays for a location, with optional check-in and check-out dates, adult count, currency and page. Pass `ne_lat`, `ne_lng`, `sw_lat` and `sw_lng` to bound the search to a map area. Each result has the listing id, title, URL, location and coordinates, price and price per night, rating, review count, host, and the Superhost and Guest Favorite flags.
- **Params:** `adults` (integer, optional) — Adult guests; `check_in` (string, optional) — Check-in date; `check_out` (string, optional) — Check-out date; `currency` (string, optional) — Currency for bounded map search; `location` (string, **required**) — Location; `ne_lat` (number, optional) — Northeast latitude for bounded map search; `ne_lng` (number, optional) — Northeast longitude for bounded map search; `page` (integer, optional) — 1-based page; `sw_lat` (number, optional) — Southwest latitude for bounded map search; `sw_lng` (number, optional) — Southwest longitude for bounded map search; `zoom` (integer, optional) — Map zoom for bounded map search

## Ticketmaster (15)

### `ticketmaster_attraction`

- **HTTP:** `GET /ticketmaster/attraction`
- **What:** Get a Ticketmaster attraction. Returns one Ticketmaster attraction (artist, team or other event entity) by numeric `id`: name, synopsis, image, URL, classification (segment, genre, sub-genre) and `has_artist_video`. Past performance `setlists` and `setlist_source_url` appear only when available. An unknown attraction returns 404.
- **Params:** `id` (string, **required**) — Numeric Ticketmaster attraction id

### `ticketmaster_attraction_events`

- **HTTP:** `GET /ticketmaster/attraction-events`
- **What:** List an attraction's Ticketmaster events. Lists upcoming Ticketmaster events for the attraction with numeric `id`. `page` is zero-based, 0 to 49, default 0; `sort` is `relevance` or `date` (default). Each event has title, start time, time zone, venue, attractions, presales, seat map and status flags such as `sold_out` and `cancelled`. The response gives `total`.
- **Params:** `id` (string, **required**) — Numeric Ticketmaster attraction id; `page` (integer, optional) — Zero-based page (0-49); `sort` (string, optional) — Result order

### `ticketmaster_attraction_related`

- **HTTP:** `GET /ticketmaster/attraction-related`
- **What:** List a Ticketmaster attraction's related attractions. Returns the "Fans Also Viewed" attractions shown on one attraction's own page. An attraction with no recommendation data returns a valid empty list.
- **Params:** `id` (string, **required**) — Numeric Ticketmaster attraction id

### `ticketmaster_attraction_reviews`

- **HTTP:** `GET /ticketmaster/attraction-reviews`
- **What:** List a Ticketmaster attraction's fan reviews. Lists fan reviews for the Ticketmaster attraction with numeric `id`, with its `average_rating`, `best_rating`, `total` and Ticketmaster's own `ai_review_summary`. Each review has a rating, title, text, nickname, city, venue and date. `offset` runs 0 to 9995 (default 0); `limit` runs 10 to 50 (default 10).
- **Params:** `id` (string, **required**) — Numeric Ticketmaster attraction id; `limit` (integer, optional) — Reviews per page (10-50); `offset` (integer, optional) — Result offset (0-9995)

### `ticketmaster_discover_categories`

- **HTTP:** `GET /ticketmaster/discover-categories`
- **What:** List Ticketmaster discover categories. Lists every current Concerts, Sports, Arts & Theater, and Family category with pagination. Section accepts `all`, `concerts`, `sports`, `arts-theater`, and `family`.
- **Params:** `page` (integer, optional) — One-based page; `per_page` (integer, optional) — Categories per page; `section` (string, optional) — Discover section

### `ticketmaster_discover_category_events`

- **HTTP:** `GET /ticketmaster/discover-category-events`
- **What:** List events in a Ticketmaster discover category. Lists events in a Ticketmaster discover category, identified by `category_id` from `ticketmaster-discover-categories`. `page` is zero-based, 0 to 49. Each event has title, start time, time zone, venue, attractions, presales, seat map and status flags such as `sold_out` and `cancelled`. The response gives `total` and `count`.
- **Params:** `category_id` (string, **required**) — Ticketmaster discover category id; `page` (integer, optional) — Zero-based page

### `ticketmaster_discover_cities`

- **HTTP:** `GET /ticketmaster/discover-cities`
- **What:** List Ticketmaster discover cities. Lists Ticketmaster's discover city destinations for a `country` (two-letter code, default `US`). Each city has a `slug`, name, canonical URL, locale and image. `page` starts at 1 and `per_page` runs 1 to 100. The response gives `total`. Pass a city `slug` to `ticketmaster-discover-city-events`.
- **Params:** `country` (string, optional) — Two-letter country code; `page` (integer, optional) — One-based page; `per_page` (integer, optional) — Cities per page

### `ticketmaster_discover_city_events`

- **HTTP:** `GET /ticketmaster/discover-city-events`
- **What:** List events in a Ticketmaster discover city. Lists events for a Ticketmaster discover city, identified by `city` (a slug from `ticketmaster-discover-cities`) and `country` (two-letter code matching the city, default `US`). It covers all municipalities grouped under that destination. `page` is zero-based, 0 to 49. Each event has title, start time, venue, attractions and status flags.
- **Params:** `city` (string, **required**) — Ticketmaster discover city slug; `country` (string, optional) — Two-letter country code matching the selected city; `page` (integer, optional) — Zero-based page

### `ticketmaster_event`

- **HTTP:** `GET /ticketmaster/event`
- **What:** Get a Ticketmaster event. Returns one Ticketmaster event by `id`: title, description, start time, time zone, currency, venue, attractions, classification, presales, on-sale time, seat map URL, and flags for sold out, cancelled, postponed, rescheduled and virtual. An unknown event returns 404; a concluded or removed event returns 410.
- **Params:** `id` (string, **required**) — Ticketmaster event id

### `ticketmaster_search_events`

- **HTTP:** `GET /ticketmaster/search-events`
- **What:** Search Ticketmaster events. Searches Ticketmaster events by artist, event, team, or venue. A zero total with an empty events list is a valid no-results response. The sort enum accepts `relevance` and `date`.
- **Params:** `page` (integer, optional) — Zero-based page (0-49); `q` (string, **required**) — Artist, event, team, or venue query; `sort` (string, optional) — Result order

### `ticketmaster_suggest`

- **HTTP:** `GET /ticketmaster/suggest`
- **What:** Suggest Ticketmaster artists, events, and venues. Returns autocomplete suggestions for a partial artist, event, team or venue name in `q`. Each suggestion has a title, `type`, category, URL, image and, when available, an `event_count`. The response also gives the echoed `query` and the `count` of suggestions.
- **Params:** `q` (string, **required**) — Partial artist, event, team, or venue query

### `ticketmaster_trending_attractions`

- **HTTP:** `GET /ticketmaster/trending-attractions`
- **What:** List trending Ticketmaster attractions. Returns a ranked list of currently-trending attractions across every segment (music, sports, arts and theater, family), not scoped to one category or city.
- **Params:** _none_

### `ticketmaster_venue`

- **HTTP:** `GET /ticketmaster/venue`
- **What:** Get a Ticketmaster venue. Returns one Ticketmaster venue by numeric `id`: name, address, city, state, country, postal code, coordinates, time zone, image, URL and visitor information as name and text entries. `seat_maps` and `city_categories` are omitted when none exist. An unknown venue returns 404.
- **Params:** `id` (string, **required**) — Numeric Ticketmaster venue id

### `ticketmaster_venue_enhanced_details`

- **HTTP:** `GET /ticketmaster/venue-enhanced-details`
- **What:** Get a Ticketmaster venue's enhanced branding details. Returns header branding imagery and external links (the venue's own site, resident teams) for major venues. Smaller venues without enhanced content return 404.
- **Params:** `id` (string, **required**) — Numeric Ticketmaster venue id

### `ticketmaster_venue_events`

- **HTTP:** `GET /ticketmaster/venue-events`
- **What:** List a venue's Ticketmaster events. Lists upcoming Ticketmaster events at the venue with numeric `id`. `page` is zero-based, 0 to 49, default 0; `sort` is `relevance` or `date` (default). Each event has title, start time, time zone, attractions, presales, seat map and status flags such as `sold_out` and `cancelled`. The response gives `total`.
- **Params:** `id` (string, **required**) — Numeric Ticketmaster venue id; `page` (integer, optional) — Zero-based page (0-49); `sort` (string, optional) — Result order

## TicketWeb (3)

### `ticketweb_event`

- **HTTP:** `GET /ticketweb/event`
- **What:** Get a TicketWeb event. Returns details for one TicketWeb event: venue, dates, age restriction, delivery methods, and per-tier ticket pricing (base price, fee breakdown, and total) when tickets are on sale. `has_tickets` is false and `sections` is empty for a free/RSVP event with no paid tickets, a sold-out event, or an access-code-gated event -- TicketWeb's own data does not reliably distinguish these three cases at this level, so the response reports the shared observable state (no purchasable sections) rather than guessing which applies.
- **Params:** `id` (string, **required**) — Numeric TicketWeb event id

### `ticketweb_search`

- **HTTP:** `GET /ticketweb/search`
- **What:** Search TicketWeb events. Searches TicketWeb events by artist, event, or venue. A zero count with an empty events list is a valid no-results response. availability is one of `in_stock`, `sold_out`, `unknown` per event.
- **Params:** `page` (integer, optional) — One-based result page, 1-50; `q` (string, **required**) — Artist, event, or venue query

### `ticketweb_venue`

- **HTTP:** `GET /ticketweb/venue`
- **What:** Get a TicketWeb venue. Returns one TicketWeb venue's detail (name, address) plus one page of its upcoming events. A zero count with an empty events list on page 1 is a valid "no upcoming events" response.
- **Params:** `id` (string, **required**) — Numeric TicketWeb venue id; `page` (integer, optional) — One-based page of upcoming events, 1-50

## Accor (8)

### `accor_amenities`

- **HTTP:** `GET /accor/amenities`
- **What:** Accor amenity reference catalog. Returns the anonymous public Accor amenity catalog with stable amenity codes, labels, categories, and display ordering. It is reference data for interpreting hotel search facets; booking, rates, rooms, reviews, and account data are excluded.
- **Params:** _none_

### `accor_brands`

- **HTTP:** `GET /accor/brands`
- **What:** Accor brand directory. Returns the Accor brand directory published on the public brands page, with each brand's name, slug, and source URL. Booking, rates, rooms, reviews, contacts, and location are excluded.
- **Params:** _none_

### `accor_catalog_hotels`

- **HTTP:** `GET /accor/catalog/hotels`
- **What:** Search the Accor hotel catalog. Searches Accor's anonymous public hotel catalog by text, hotel code, or latitude/longitude radius. Results contain static property identity and broad location metadata plus catalog relevance/distance; contact details, precise hotel coordinates, payment, loyalty, media, rates, rooms, reviews, and booking data are excluded.
- **Params:** `hotel_id` (string, optional) — Four-character Accor hotel code; `latitude` (number, optional) — Search-center latitude (-90 to 90); `limit` (integer, optional) — Results per request (1 to 50); `longitude` (number, optional) — Search-center longitude (-180 to 180); `offset` (integer, optional) — Zero-based result offset (0 to 300); `query` (string, optional) — Destination or hotel text (at least two characters); `radius_km` (number, optional) — Search radius in kilometers (0.1 to 100; defaults to 10 for coordinate searches)

### `accor_destination_hotels`

- **HTTP:** `GET /accor/destination/hotels`
- **What:** Accor hotels in a destination. Returns the static list of hotels published on one Accor destination directory page (world, continent, country, region, department, city, district, or place), optionally narrowed by a theme facet. Each hotel carries its code, name, source URL, and broad city/country. Booking, rates, rooms, reviews, contacts, and precise location are excluded.
- **Params:** `destination_type` (string, **required**) — Destination level: world, continent, country, region, department, city, district, or place; `slug` (string, optional) — Destination page slug, e.g. hotels-dusseldorf-v1158. Required for every type except world.; `theme` (string, optional) — Optional theme facet: 4-stars, 5-stars, apart-hotel, breakfast, budget-friendly, business, eco-certified, family-friendly, fitness, luxury, meetings-and-events, parking, pet-friendly, pool, resorts, or spa

### `accor_property`

- **HTTP:** `GET /accor/property`
- **What:** Accor hotel metadata. Returns static public metadata for one Accor hotel code, including name, brand, city/country, explicitly listed amenities, and published check-in/check-out times. Booking, rates, rooms, reviews, contacts, and precise location are excluded.
- **Params:** `hotel_code` (string, **required**) — Four-character Accor hotel code

### `accor_search`

- **HTTP:** `GET /accor/search`
- **What:** Search Accor hotels. Searches the public Accor hotel index by destination or hotel name, with optional country, city, brand, star, page, and page-size filters. Results contain static hotel identity, location labels, ratings, and source URLs; booking, rates, rooms, reviews, loyalty, and payment flows are excluded.
- **Params:** `brand` (string, optional) — Accor brand code facet; `city` (string, optional) — City facet; `country` (string, optional) — Country facet; `language` (string, optional) — Index locale; `limit` (integer, optional) — Results per page, 1-100; `page` (integer, optional) — Zero-based result page; `query` (string, **required**) — Destination or hotel query (at least two characters); `stars` (integer, optional) — Exact star facet

### `accor_search_details`

- **HTTP:** `GET /accor/search/details`
- **What:** Accor place coordinates and viewport. Resolves an anonymous Accor search suggestion identifier to its description, coordinates, viewport, radius, and address components. It uses the same public place-details source as the Accor search box; booking, rates, rooms, reviews, and account data are excluded.
- **Params:** `id` (string, **required**) — Identifier returned by Accor search suggestions; `language` (string, optional) — Optional locale; `source` (string, **required**) — Suggestion source

### `accor_search_suggest`

- **HTTP:** `GET /accor/search/suggest`
- **What:** Accor destination and hotel search suggestions. Returns anonymous Accor typeahead suggestions for a partial destination or hotel query, including destination/place and hotel identifiers, types, labels, and match metadata. It uses the public search-box suggestion source only; booking, rates, rooms, reviews, and result-list requests are excluded.
- **Params:** `language` (string, optional) — Optional locale used by the suggestion source; `query` (string, **required**) — Partial destination or hotel query (at least two characters)

## Hotels.com (7)

### `hotels_autocomplete`

- **HTTP:** `GET /hotels/autocomplete`
- **What:** Get Hotels.com destination suggestions. Returns Hotels.com search-box suggestions for a partial destination or property name in `q` (up to 120 characters). Each suggestion has its type, primary and secondary text, full location name, coordinates, and region or property id. A query with no match returns an empty `suggestions` list.
- **Params:** `q` (string, **required**) — Partial destination or property name

### `hotels_offers`

- **HTTP:** `POST /hotels/offers`
- **What:** Get Hotels.com room offers. Returns the public room/unit offer summaries shown for one Hotels.com property and date range, including room labels and non-transactional offer messages. Booking, checkout, payment, and reservation tokens are never returned. property_id is the numeric global property id from a Search response.
- **Params:** `request` (object, **required**) — Room offers request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `hotels_property`

- **HTTP:** `POST /hotels/property`
- **What:** Get Hotels.com property details. Returns public static metadata from one canonical Hotels.com property page, including name, address, rating, images, and amenities. Date-bound availability, prices, booking, and review content are excluded.
- **Params:** `request` (object, **required**) — Canonical Hotels.com property URL
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `hotels_rates`

- **HTTP:** `POST /hotels/rates`
- **What:** Get Hotels.com rates for one property. Returns one Hotels.com property's date-bound rates and availability: the same property card Search returns, with the live per-night and per-stay prices Hotels.com shows for the requested dates. property_id is the numeric global property id from a Search response's properties[].id; it is distinct from the legacy /ho<id>/ URL id.
- **Params:** `request` (object, **required**) — Rates request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `hotels_reviews`

- **HTTP:** `POST /hotels/reviews`
- **What:** Get Hotels.com guest reviews. Returns one Hotels.com property's review overview: the overall rating (0-10) with its descriptive label, the per-category sub-ratings (cleanliness, service, amenities, and so on), and a bounded set of highlighted guest reviews with reviewer, date, rating label, text, and verified-stay flag. property_id is the numeric global property id from a Search response's properties[].id. This mirrors the property page's Guest reviews section; the full paginated review archive is not exposed.
- **Params:** `request` (object, **required**) — Reviews request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `hotels_reviews_archive`

- **HTTP:** `POST /hotels/reviews/archive`
- **What:** List Hotels.com guest reviews. Returns one page of public guest reviews for a Hotels.com property, including reviewer, date, traveler type, rating label, title, and message. Use page and page_size to walk the archive; the response reports whether another page is available. property_id is the numeric global property id from a Search response's properties[].id. Booking, account, and private review data are not included.
- **Params:** `request` (object, **required**) — Review archive request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `hotels_search`

- **HTTP:** `POST /hotels/search`
- **What:** Search Hotels.com hotels. Returns a page of date-bound Hotels.com hotel search results for either a free-text destination or a numeric Hotels.com region_id: property cards with per-night and per-stay prices, review score and count, location, thumbnail, amenities, and promotional badges. Provide exactly one of query or region_id; region_id skips destination typeahead resolution. Prices are the live rates Hotels.com shows for the requested check-in and check-out dates.
- **Params:** `request` (object, **required**) — Search request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.
