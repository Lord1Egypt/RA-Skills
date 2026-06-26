---
name: shodan-skill
description: Advanced Shodan API interactions including search, scan, alerts, and DNS.
read_when:
  - User wants to perform advanced Shodan searches with facets
  - User wants to scan specific IPs using Shodan (on-demand)
  - User wants to manage Shodan network alerts
  - User wants to lookup DNS or domain information
metadata: {"openclaw":{"emoji":"🔍","requires":{"bins":["python3","pip"]}}}
---

# Shodan Skill

A comprehensive wrapper for the Shodan API using the official Python library.

## Setup

1.  **Install dependencies**:
    ```bash
    pip install shodan
    ```

2.  **Configure API Key**:
    ```bash
    shodan init <YOUR_API_KEY>
    ```

## Usage

### 1. Search (Advanced)

Search with limits, pages, and facets (statistics).

```bash
python3 {baseDir}/scripts/shodan_skill.py search "<QUERY>" --limit <LIMIT> --page <PAGE> --facets <FACETS>
```
*   `--facets`: Comma separated, e.g., `country:5,org:5` (top 5 countries and orgs).

### 2. Count (Statistics)

Get the total count of results without consuming query credits for full details.

```bash
python3 {baseDir}/scripts/shodan_skill.py count "<QUERY>" --facets <FACETS>
```

### 3. Host Details

Get details for an IP.

```bash
python3 {baseDir}/scripts/shodan_skill.py host <IP> [--history] [--minify]
```

### 4. On-Demand Scan

Request Shodan to scan a network (consumes Scan Credits).

```bash
python3 {baseDir}/scripts/shodan_skill.py scan <IPs>
```
*   `<IPs>`: Single IP, CIDR, or comma-separated list.

### 5. Network Alerts

Monitor your networks for exposure.

*   **List Alerts**: `python3 {baseDir}/scripts/shodan_skill.py alert_list`
*   **Create Alert**: `python3 {baseDir}/scripts/shodan_skill.py alert_create <NAME> <IP_RANGE>`
*   **Alert Info**: `python3 {baseDir}/scripts/shodan_skill.py alert_info <ALERT_ID>`

### 6. DNS & Domains

*   **Domain Info**: `python3 {baseDir}/scripts/shodan_skill.py dns_domain <DOMAIN>`
*   **Resolve**: `python3 {baseDir}/scripts/shodan_skill.py dns_resolve <HOSTNAMES>`

### 7. Account & Tools

*   **Profile**: `python3 {baseDir}/scripts/shodan_skill.py profile`
*   **My IP**: `python3 {baseDir}/scripts/shodan_skill.py myip`
*   **Ports**: `python3 {baseDir}/scripts/shodan_skill.py ports`
*   **Protocols**: `python3 {baseDir}/scripts/shodan_skill.py protocols`

### 8. Directory (Saved Queries)

*   **Search Queries**: `python3 {baseDir}/scripts/shodan_skill.py query_search "<TERM>"`
*   **Popular Tags**: `python3 {baseDir}/scripts/shodan_skill.py query_tags`

### 9. Notifiers (Alerts)

*   **List Notifiers**: `python3 {baseDir}/scripts/shodan_skill.py notifier_list`

### 10. Exploits

*   **Search Exploits**: `python3 {baseDir}/scripts/shodan_skill.py exploit_search "<QUERY>"`

### 11. Stream (Realtime)

Stream realtime banners. Use `--ports` or `--alert` to filter.

```bash
python3 {baseDir}/scripts/shodan_skill.py stream --limit 10
```

### 12. Trends (Facets)

Use `count` with facets to analyze trends.

```bash
python3 {baseDir}/scripts/shodan_skill.py count "apache" --facets "country"
```

### 13. Cheat Sheets (Help)

*   **List Filters**: `python3 {baseDir}/scripts/shodan_skill.py filters`
*   **List Banner Fields**: `python3 {baseDir}/scripts/shodan_skill.py datapedia`
