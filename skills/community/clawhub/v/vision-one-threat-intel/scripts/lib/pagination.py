"""Auto-pagination for Vision One API endpoints using nextLink."""

from urllib.parse import urlparse, parse_qs


def _extract_items(resp):
    """Extract items from either STIX bundle or items-based response."""
    # STIX bundle format (feedIndicators, feeds)
    bundle = resp.get("bundle")
    if bundle:
        return bundle.get("objects", [])
    # Standard items format (suspiciousObjects, etc.)
    return resp.get("items", [])


def _parse_next_link(next_link):
    """Parse ALL query params from a nextLink URL.

    Vision One nextLinks include required params (topReport,
    responseObjectFormat, etc.) that must be preserved.
    """
    parsed = urlparse(next_link)
    # parse_qs returns lists; flatten single values
    params = {}
    for key, values in parse_qs(parsed.query).items():
        params[key] = values[0] if len(values) == 1 else values
    path = parsed.path
    return path, params


def paginate(client, path, params=None, max_items=200, use_top=True):
    """Yield items from a paginated Vision One API endpoint.

    Handles both STIX bundle responses (bundle.objects[]) and
    standard responses (items[]). Follows nextLink automatically.

    Set use_top=False for endpoints that don't support the 'top' parameter
    (e.g., /feeds).
    """
    params = dict(params or {})
    collected = 0
    if use_top:
        page_size = min(200, max_items)
        params["top"] = page_size

    while collected < max_items:
        resp = client.get(path, params)

        items = _extract_items(resp)
        if not items:
            break

        for item in items:
            yield item
            collected += 1
            if collected >= max_items:
                return

        # Check for next page
        next_link = resp.get("nextLink", "")
        if not next_link:
            break

        # Use ALL params from nextLink (preserves required server params)
        path, params = _parse_next_link(next_link)
