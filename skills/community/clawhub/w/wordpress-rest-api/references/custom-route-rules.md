# Custom Route Rules

Primary docs:

- Routes and endpoints handbook: <https://developer.wordpress.org/rest-api/extending-the-rest-api/routes-and-endpoints/>
- Adding custom endpoints: <https://developer.wordpress.org/rest-api/extending-the-rest-api/adding-custom-endpoints/>

Use this file when you are reviewing or implementing custom REST routes.

## Registration Rules

Default pattern:

- choose a unique namespace such as `vendor/v1`
- register routes with `register_rest_route()`
- declare methods explicitly
- provide a `permission_callback`
- validate and sanitize args instead of trusting raw input

## Permission Callback

Do not omit `permission_callback`.

That callback should answer:

- who may call the route
- under which conditions
- which capabilities or authentication state are required

## Response Rules

Prefer:

- `WP_REST_Response`
- plain arrays that core can convert to JSON
- `WP_Error` for structured failures

If you are returning custom objects, convert them to API-safe arrays first.

## Args And Schema

For write routes:

- declare expected args
- set required flags where appropriate
- sanitize input
- validate enum-like values

For public routes:

- trim the response to only what clients need
- avoid exposing raw internal objects or secrets

## Discovery Rules

When reverse engineering a custom route:

1. inspect `/wp-json/`
2. locate the custom namespace
3. send `OPTIONS`
4. inspect the server-side registration if you own the code

Treat plugin routes as live contracts, not as inferred clones of core routes.
