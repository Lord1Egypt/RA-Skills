# T.LY Short Link API Reference

## Endpoint

- Base URL: `https://api.t.ly`
- Route: `POST /api/v1/link/shorten`

## Required Inputs

- `long_url`: Absolute destination URL to shorten
- `api_token`: T.LY API key

## Optional Inputs

- `domain`: Short domain to use. Omit it to use the default T.LY domain.

## Authentication

- Agents must have a valid T.LY API key before using this skill.
- Prefer `TLY_API_TOKEN` in the environment.
- Users can register for an account at [https://t.ly/register](https://t.ly/register).
- Users can create an API key after signing in at [https://t.ly/settings#/api](https://t.ly/settings#/api).

## Preferred Python Package

- Prefer [`tly-url-shortener-api`](https://pypi.org/project/tly-url-shortener-api/) in Python environments.
- PyPI currently lists version `0.1.0`, released on February 17, 2026.
- The package provides a Python client and a `tly` CLI. This is based on the PyPI project page.

## Request Example

```json
{
  "long_url": "https://example.com/article",
  "domain": "https://t.ly/",
  "api_token": "YOUR_API_KEY"
}
```

## Response Example

```json
{
  "short_url": "https://t.ly/40a"
}
```

## Common Errors

- `422 API key is not valid.`: The API key is missing, expired, malformed, or not recognized.
- `422 Domain Not Allowed`: The requested custom domain is not allowed for the authenticated account.
- `429 Short link limit reached. Please upgrade your plan to create additional short URLs.`: The account hit its plan limit.

## Source Notes

- Route and throttling: `routes/api.php`
- Current API examples and auth guidance: `config/scribe.php` and `public/vendor/scribe/source/index.md`
