#!/usr/bin/env python3
"""
Willhaben Real Estate Search via internal webapi.
Searches apartments and houses, fetches detail pages for heating/energy/condition.

Usage:
  python3 willhaben-search.py --district schaerding --type apartment --max-price 300000
  python3 willhaben-search.py --district schaerding --type house --max-price 350000
  python3 willhaben-search.py --detail 1148259428
  python3 willhaben-search.py --district schaerding --type apartment --format json

Districts use URL slug: schaerding, ried-im-innkreis, grieskirchen, wels, wels-land,
  linz, linz-land, urfahr-umgebung, eferding, braunau-am-inn, voecklabruck
State: oberoesterreich (default), niederoesterreich, salzburg, etc.
Types: apartment (Eigentumswohnung), house (Haus kaufen)
"""
import argparse
import json
import sys
import time
import requests


API_BASE = 'https://www.willhaben.at/webapi/iad'
SEARCH_BASE = f'{API_BASE}/search/atz/seo/immobilien'
WH_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'de-AT,de;q=0.9',
    'x-wh-client': 'api@willhaben.at;responsive_web;server;1.0.0',
}

TYPE_MAP = {
    'apartment': 'eigentumswohnung',
    'house': 'haus-kaufen',
}

# Fields to extract from detail API
DETAIL_FIELDS = [
    'HEATING', 'BUILDING_CONDITION', 'YEAR_OF_BUILDING',
    'ENERGY_HWB', 'ENERGY_HWB_CLASS', 'ENERGY_FGEE', 'ENERGY_FGEE_CLASS',
    'ESTATE_PRICE/HEATINGCOSTSNET', 'PARKING_TYPE', 'GARAGE',
    'NUMBER_OF_ROOMS', 'ESTATE_SIZE/LIVING_AREA', 'ESTATE_SIZE/USEABLE_AREA',
    'FLOOR', 'PROPERTY_TYPE_FLAT', 'PROPERTY_TYPE_HOUSE',
    'FREE_AREA/FREE_AREA_AREA_TOTAL', 'FREE_AREA_TYPE_NAME',
    'BODY_DYN',
]


def create_session():
    s = requests.Session()
    s.headers.update(WH_HEADERS)
    return s


def search_listings(session, state, district, property_type, max_price=None,
                    min_rooms=None, max_pages=5, rows_per_page=25):
    slug = TYPE_MAP.get(property_type, property_type)
    all_items = []
    total = 0

    for page in range(1, max_pages + 1):
        if district:
            url = f'{SEARCH_BASE}/{state}/{district}'
        else:
            url = f'{SEARCH_BASE}/{state}'

        params = {
            'page': page,
            'rows': rows_per_page,
        }
        if slug == 'eigentumswohnung':
            params['sfId'] = '9a285292-0c04-4a38-b1d2-68b55ec7bcde'
        if max_price:
            params['PRICE_TO'] = max_price
        if min_rooms:
            params['NO_OF_ROOMS_BUCKET'] = f'{min_rooms}X'

        # Prepend property type to URL
        url = f'{SEARCH_BASE}/{slug}/{state}'
        if district:
            url = f'{url}/{district}'

        resp = session.get(url, params=params, timeout=30)
        if resp.status_code != 200:
            print(f"  [API error page {page}: {resp.status_code}]", file=sys.stderr)
            break

        data = resp.json()
        total = data.get('rowsFound', 0)
        ads = data.get('advertSummaryList', {}).get('advertSummary', [])

        for a in ads:
            attrs = {}
            for at in a.get('attributes', {}).get('attribute', []):
                name = at.get('name', '')
                vals = at.get('values', [])
                attrs[name] = vals[0] if vals else ''

            seo_url = attrs.get('SEO_URL', '')
            full_url = f'https://www.willhaben.at/iad/{seo_url}' if seo_url else ''

            all_items.append({
                'id': str(a.get('id', '')),
                'title': a.get('description', '').replace('\n', ' ').strip(),
                'url': full_url,
                'price': attrs.get('PRICE', ''),
                'rooms': attrs.get('NUMBER_OF_ROOMS', attrs.get('ROOMS', '')),
                'area': attrs.get('ESTATE_SIZE/LIVING_AREA', attrs.get('ESTATE_SIZE', '')),
                'location': attrs.get('LOCATION', ''),
                'district': attrs.get('DISTRICT', ''),
                'postcode': attrs.get('POSTCODE', ''),
                'published': attrs.get('PUBLISHED_String', ''),
                'is_private': attrs.get('ISPRIVATE', ''),
                'property_type': attrs.get('PROPERTY_TYPE', ''),
            })

        if page * rows_per_page >= total:
            break

    return total, all_items


def get_detail(session, ad_id):
    resp = session.get(f'{API_BASE}/atverz/{ad_id}', timeout=15)
    if resp.status_code != 200:
        return {'error': f'{resp.status_code}'}

    data = resp.json()
    attrs = {}
    for at in data.get('attributes', {}).get('attribute', []):
        name = at.get('name', '')
        vals = at.get('values', [])
        attrs[name] = vals[0] if vals else ''

    result = {
        'id': ad_id,
        'heating': attrs.get('HEATING', ''),
        'condition': attrs.get('BUILDING_CONDITION', ''),
        'year': attrs.get('YEAR_OF_BUILDING', ''),
        'hwb': attrs.get('ENERGY_HWB', ''),
        'hwb_class': attrs.get('ENERGY_HWB_CLASS', ''),
        'fgee': attrs.get('ENERGY_FGEE', ''),
        'fgee_class': attrs.get('ENERGY_FGEE_CLASS', ''),
        'heating_costs': attrs.get('ESTATE_PRICE/HEATINGCOSTSNET', ''),
    }

    # Look for parking-related fields
    parking_parts = []
    for k, v in attrs.items():
        kl = k.lower()
        if v and any(w in kl for w in ['parking', 'garage', 'stellplatz', 'carport']):
            parking_parts.append(v)
    result['parking'] = ', '.join(parking_parts) if parking_parts else ''

    # Extract body text for keyword scanning
    body = attrs.get('BODY_DYN', '')
    if body and not result['heating']:
        body_l = body.lower()
        for h in ['wärmepumpe', 'fernwärme', 'pellet', 'gas', 'öl', 'elektro', 'biomasse']:
            if h in body_l:
                result['heating'] = f'(from description: {h})'
                break
    if body and not result['parking']:
        body_l = body.lower()
        for p in ['garage', 'stellplatz', 'carport', 'tiefgarage', 'parkplatz']:
            if p in body_l:
                result['parking'] = f'(from description: {p})'
                break

    return result


def main():
    parser = argparse.ArgumentParser(description='Willhaben Real Estate Search')
    parser.add_argument('--state', default='oberoesterreich',
                        help='Austrian state slug (default: oberoesterreich)')
    parser.add_argument('--district', help='District slug (e.g., schaerding, ried-im-innkreis)')
    parser.add_argument('--type', default='apartment', choices=['apartment', 'house'],
                        help='Property type')
    parser.add_argument('--max-price', type=int, help='Maximum price in EUR')
    parser.add_argument('--min-rooms', type=int, help='Minimum rooms (uses bucket: 2X, 3X, etc.)')
    parser.add_argument('--max-pages', type=int, default=5, help='Max pages (default: 5)')
    parser.add_argument('--detail', help='Get detail for a specific ad ID')
    parser.add_argument('--with-details', action='store_true',
                        help='Fetch detail page for each listing (slower but includes heating/energy)')
    parser.add_argument('--format', choices=['json', 'text'], default='text')
    args = parser.parse_args()

    session = create_session()

    if args.detail:
        result = get_detail(session, args.detail)
        if args.format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            for k, v in result.items():
                print(f'{k}: {v}')
        return

    if not args.district and not args.state:
        parser.error('--district or --state is required for search')

    total, listings = search_listings(
        session, args.state, args.district, args.type,
        args.max_price, args.min_rooms, args.max_pages
    )

    if args.with_details:
        for listing in listings:
            detail = get_detail(session, listing['id'])
            listing.update(detail)
            time.sleep(0.3)  # Be nice to the API

    if args.format == 'json':
        print(json.dumps({'total': total, 'listings': listings}, indent=2, ensure_ascii=False))
    else:
        type_label = 'Apartments' if args.type == 'apartment' else 'Houses'
        district_label = args.district or args.state
        print(f"=== {type_label} {district_label} (max {args.max_price or 'any'} EUR) ===")
        print(f"Total: {total}, fetched: {len(listings)}\n")

        for i, l in enumerate(listings, 1):
            print(f"[{i}] {l['title']}")
            print(f"    Price: {l['price']} EUR | Area: {l['area']} m² | Rooms: {l['rooms']}")
            print(f"    Location: {l['location']}, {l['district']} ({l['postcode']})")
            print(f"    Published: {l['published']}")
            if l.get('heating') or l.get('condition') or l.get('hwb'):
                print(f"    Heating: {l.get('heating', '?')} | Condition: {l.get('condition', '?')}")
                print(f"    HWB: {l.get('hwb', '?')} ({l.get('hwb_class', '?')}) | Year: {l.get('year', '?')}")
                print(f"    Parking: {l.get('parking', '?')}")
            print(f"    URL: {l['url']}")
            print()


if __name__ == '__main__':
    main()
