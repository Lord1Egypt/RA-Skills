# Zone & Domain Discovery

Nearly all EdgeOne API operations require a **ZoneId** (zone ID, in the format `zone-xxx123abc456`).
Below is the standard process for discovering ZoneIds and reverse-looking up domains.

## APIs Involved

| Action | Description | API Docs |
|---|---|---|
| DescribeZones | Query the list of zones | `curl -s https://cloudcache.tencentcs.com/capi/refs/service/teo/action/DescribeZones.md` |
| DescribeAccelerationDomains | Query the list of acceleration domains | `curl -s https://cloudcache.tencentcs.com/capi/refs/service/teo/action/DescribeAccelerationDomains.md` |

Check the API docs above before calling, to get the exact usage of Filters, pagination, and other parameters.

## 1. List All Zones

Call **DescribeZones** — the `Zones` array in the response contains each zone's `ZoneId`, `ZoneName` (zone domain), `Status`, and other info.

> **Important**:
> 
> 1. **Pagination Mechanism**: DescribeZones returns a maximum of 20 records per request by default. **Must use pagination mechanism** to retrieve all zones:
> 
> 2. **Status Filtering**: After retrieving the zone list, **must filter out** zones with `Status` as `initializing`:
>    - These zones are initializing and have not completed creation
>    - Should not be displayed to users or used for subsequent operations
>    - Only display and use available zones with `Status` as `active`
> 
> **Pagination Parameters**:
> - `Limit`: Maximum number of records returned per request, recommend setting to `100` (maximum value)
> - `Offset`: Offset, starting from `0`, increment by `Limit` value each iteration
>
> **Pagination Logic**:
> ```
> 1. Initial call: Offset=0, Limit=100
> 2. Check TotalCount (total number of zones) in response
> 3. If TotalCount > number of zones retrieved:
>    - Offset += 100
>    - Continue calling until all zones are retrieved
> 4. Merge all paginated results
> ```
>
> **Example (Pseudo Code)**:
> ```python
> all_zones = []
> offset = 0
> limit = 100
> 
> # Paginate to retrieve all zones
> while True:
>     response = DescribeZones(Offset=offset, Limit=limit)
>     all_zones.extend(response.Zones)
>     
>     if offset + limit >= response.TotalCount:
>         break
>     offset += limit
> 
> # Filter out zones that are initializing
> available_zones = [zone for zone in all_zones if zone.Status != 'initializing']
> ```

## 2. Query by Zone Name

When the user already knows the zone domain, call **DescribeZones** with `Filters` (`zone-name`) for an exact match.

> **Note**: The query results also need to check the `Status` field and filter out zones with `initializing` status.

## 3. Reverse-Lookup ZoneId from a Subdomain

When the user only provides a subdomain (e.g., `www.example.com`) and doesn't know the ZoneId:

1. First call **DescribeZones** to list all zones, and find the ZoneId corresponding to the root domain matching the subdomain
   > **Must use pagination**: Refer to the pagination mechanism in "1. List All Zones" to ensure traversing **all** zones for matching
2. Then call **DescribeAccelerationDomains** with `Filters` (`domain-name`) to confirm the domain exists under the zone

## 4. List All Domains Under a Zone

Call **DescribeAccelerationDomains** with the `ZoneId`. Be sure to use pagination parameters to handle multi-page results.

## 5. ZoneId Caching Recommendation

Within the same session, previously discovered ZoneIds should be remembered and reused to avoid repeated calls to `DescribeZones`.
