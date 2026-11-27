# VirusTotal access policy

An access policy limits which endpoints VirusTotal connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/virustotal#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for VirusTotal: its 158 read-only endpoints, plus deny rules for the 2 write endpoints a read rule would otherwise match. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create virustotal --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/v3/analyses/{id}"},
    {"method": "GET", "path": "api/v3/analyses/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/analyses/{id}/{id}"},
    {"method": "GET", "path": "api/v3/operations/{id}"},
    {"method": "GET", "path": "api/v3/submission/{id}"},
    {"method": "GET", "path": "api/v3/attack_tactics/{id}"},
    {"method": "GET", "path": "api/v3/attack_tactics/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/attack_tactics/{id}/{id}"},
    {"method": "GET", "path": "api/v3/attack_techniques/{id}"},
    {"method": "GET", "path": "api/v3/attack_techniques/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/attack_techniques/{id}/{id}"},
    {"method": "GET", "path": "api/v3/groups/{id}/activity_log_entries"},
    {"method": "GET", "path": "api/v3/collections"},
    {"method": "GET", "path": "api/v3/collections/{id}"},
    {"method": "GET", "path": "api/v3/collections/{id}/aggregations/download/{id}"},
    {"method": "GET", "path": "api/v3/collections/{id}/comments"},
    {"method": "GET", "path": "api/v3/collections/{id}/download/{id}"},
    {"method": "GET", "path": "api/v3/collections/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/collections/{id}/search"},
    {"method": "GET", "path": "api/v3/collections/{id}/{id}"},
    {"method": "GET", "path": "api/v3/collections/{id}/{id}/download/{id}"},
    {"method": "GET", "path": "api/v3/comments"},
    {"method": "GET", "path": "api/v3/comments/{id}"},
    {"method": "GET", "path": "api/v3/comments/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/comments/{id}/{id}"},
    {"method": "GET", "path": "api/v3/feeds/domains/hourly/{id}"},
    {"method": "GET", "path": "api/v3/feeds/domains/{id}"},
    {"method": "GET", "path": "api/v3/domains/{id}"},
    {"method": "GET", "path": "api/v3/domains/{id}/comments"},
    {"method": "GET", "path": "api/v3/domains/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/domains/{id}/votes"},
    {"method": "GET", "path": "api/v3/domains/{id}/{id}"},
    {"method": "GET", "path": "api/v3/resolutions/{id}"},
    {"method": "GET", "path": "api/v3/file_behaviours/{id}"},
    {"method": "GET", "path": "api/v3/file_behaviours/{id}/evtx"},
    {"method": "GET", "path": "api/v3/file_behaviours/{id}/html"},
    {"method": "GET", "path": "api/v3/file_behaviours/{id}/memdump"},
    {"method": "GET", "path": "api/v3/file_behaviours/{id}/pcap"},
    {"method": "GET", "path": "api/v3/file_behaviours/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/file_behaviours/{id}/{id}"},
    {"method": "GET", "path": "api/v3/files/{id}/behaviour_mitre_trees"},
    {"method": "GET", "path": "api/v3/files/{id}/behaviour_summary"},
    {"method": "GET", "path": "api/v3/files/{id}/behaviours"},
    {"method": "GET", "path": "api/v3/feeds/files/hourly/{id}"},
    {"method": "GET", "path": "api/v3/feeds/files/{id}"},
    {"method": "GET", "path": "api/v3/feeds/files/{id}/download"},
    {"method": "GET", "path": "api/v3/files/{id}"},
    {"method": "GET", "path": "api/v3/files/{id}/comments"},
    {"method": "GET", "path": "api/v3/files/{id}/download"},
    {"method": "GET", "path": "api/v3/files/{id}/download_url"},
    {"method": "GET", "path": "api/v3/files/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/files/{id}/votes"},
    {"method": "GET", "path": "api/v3/files/{id}/{id}"},
    {"method": "GET", "path": "api/v3/sigma_rules/{id}"},
    {"method": "GET", "path": "api/v3/yara_rulesets/{id}"},
    {"method": "GET", "path": "api/v3/groups/{id}"},
    {"method": "GET", "path": "api/v3/groups/{id}/relationships/administrators"},
    {"method": "GET", "path": "api/v3/groups/{id}/relationships/administrators/{id}"},
    {"method": "GET", "path": "api/v3/groups/{id}/relationships/users"},
    {"method": "GET", "path": "api/v3/groups/{id}/relationships/users/{id}"},
    {"method": "GET", "path": "api/v3/groups/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/groups/{id}/{id}"},
    {"method": "GET", "path": "api/v3/ioc_stream"},
    {"method": "GET", "path": "api/v3/ioc_stream_notifications/{id}"},
    {"method": "GET", "path": "api/v3/ip_addresses/{id}"},
    {"method": "GET", "path": "api/v3/ip_addresses/{id}/comments"},
    {"method": "GET", "path": "api/v3/ip_addresses/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/ip_addresses/{id}/scanning_technologies"},
    {"method": "GET", "path": "api/v3/ip_addresses/{id}/votes"},
    {"method": "GET", "path": "api/v3/ip_addresses/{id}/{id}"},
    {"method": "GET", "path": "api/v3/feeds/ip_addresses/hourly/{id}"},
    {"method": "GET", "path": "api/v3/feeds/ip_addresses/{id}"},
    {"method": "GET", "path": "api/v3/intelligence/hunting_notification_files"},
    {"method": "GET", "path": "api/v3/intelligence/hunting_notifications"},
    {"method": "GET", "path": "api/v3/intelligence/hunting_notifications/{id}"},
    {"method": "GET", "path": "api/v3/intelligence/hunting_rulesets"},
    {"method": "GET", "path": "api/v3/intelligence/hunting_rulesets/{id}"},
    {"method": "GET", "path": "api/v3/intelligence/hunting_rulesets/{id}/relationships/editors/{id}"},
    {"method": "GET", "path": "api/v3/intelligence/hunting_rulesets/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/intelligence/hunting_rulesets/{id}/{id}"},
    {"method": "GET", "path": "api/v3/popular_threat_categories"},
    {"method": "GET", "path": "api/v3/port_analyses/{id}"},
    {"method": "GET", "path": "api/v3/port_analyses/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/port_analyses/{id}/{id}"},
    {"method": "GET", "path": "api/v3/port_infos/{id}"},
    {"method": "GET", "path": "api/v3/port_infos/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/port_infos/{id}/{id}"},
    {"method": "GET", "path": "api/v3/private/analyses"},
    {"method": "GET", "path": "api/v3/private/analyses/{id}"},
    {"method": "GET", "path": "api/v3/private/analyses/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/private/analyses/{id}/{id}"},
    {"method": "GET", "path": "api/v3/private/file/{id}/behaviours"},
    {"method": "GET", "path": "api/v3/private/file_behaviours/{id}"},
    {"method": "GET", "path": "api/v3/private/file_behaviours/{id}/evtx"},
    {"method": "GET", "path": "api/v3/private/file_behaviours/{id}/html"},
    {"method": "GET", "path": "api/v3/private/file_behaviours/{id}/memdump"},
    {"method": "GET", "path": "api/v3/private/file_behaviours/{id}/pcap"},
    {"method": "GET", "path": "api/v3/private/file_behaviours/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/private/file_behaviours/{id}/{id}"},
    {"method": "GET", "path": "api/v3/private/files/{id}/behaviour_mitre_trees"},
    {"method": "GET", "path": "api/v3/private/files/{id}/behaviour_summary"},
    {"method": "GET", "path": "api/v3/private/files"},
    {"method": "GET", "path": "api/v3/private/files/{id}"},
    {"method": "GET", "path": "api/v3/private/files/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/private/files/{id}/{id}"},
    {"method": "GET", "path": "api/v3/private/urls/{id}"},
    {"method": "GET", "path": "api/v3/private/urls/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/private/urls/{id}/{id}"},
    {"method": "GET", "path": "api/v3/groups/{id}/api_usage"},
    {"method": "GET", "path": "api/v3/groups/{id}/users_consuming_quota/{id}"},
    {"method": "GET", "path": "api/v3/users/{id}/api_usage"},
    {"method": "GET", "path": "api/v3/intelligence/retrohunt_jobs"},
    {"method": "GET", "path": "api/v3/intelligence/retrohunt_jobs/{id}"},
    {"method": "GET", "path": "api/v3/intelligence/retrohunt_jobs/{id}/matching_files"},
    {"method": "GET", "path": "api/v3/feeds/file_behaviours/hourly/{id}"},
    {"method": "GET", "path": "api/v3/feeds/file_behaviours/{id}"},
    {"method": "GET", "path": "api/v3/feeds/file_behaviours/{id}/evtx"},
    {"method": "GET", "path": "api/v3/feeds/file_behaviours/{id}/html"},
    {"method": "GET", "path": "api/v3/feeds/file_behaviours/{id}/memdump"},
    {"method": "GET", "path": "api/v3/feeds/file_behaviours/{id}/pcap"},
    {"method": "GET", "path": "api/v3/saved_searches"},
    {"method": "GET", "path": "api/v3/saved_searches/{id}"},
    {"method": "GET", "path": "api/v3/saved_searches/{id}/relationship/{id}"},
    {"method": "GET", "path": "api/v3/saved_searches/{id}/{id}"},
    {"method": "GET", "path": "api/v3/intelligence/search"},
    {"method": "GET", "path": "api/v3/intelligence/search/snippets/{id}"},
    {"method": "GET", "path": "api/v3/metadata"},
    {"method": "GET", "path": "api/v3/search"},
    {"method": "GET", "path": "api/v3/groups/{id}/relationships/service_accounts"},
    {"method": "GET", "path": "api/v3/service_accounts/{id}"},
    {"method": "GET", "path": "api/v3/feeds/urls/hourly/{id}"},
    {"method": "GET", "path": "api/v3/feeds/urls/{id}"},
    {"method": "GET", "path": "api/v3/urls/{id}"},
    {"method": "GET", "path": "api/v3/urls/{id}/comments"},
    {"method": "GET", "path": "api/v3/urls/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/urls/{id}/votes"},
    {"method": "GET", "path": "api/v3/urls/{id}/{id}"},
    {"method": "GET", "path": "api/v3/users/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/users/{id}/{id}"},
    {"method": "GET", "path": "api/v3/graphs"},
    {"method": "GET", "path": "api/v3/graphs/{id}"},
    {"method": "GET", "path": "api/v3/graphs/{id}/comments"},
    {"method": "GET", "path": "api/v3/graphs/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/graphs/{id}/{id}"},
    {"method": "GET", "path": "api/v3/graphs/{id}/relationships/editors"},
    {"method": "GET", "path": "api/v3/graphs/{id}/relationships/editors/{id}"},
    {"method": "GET", "path": "api/v3/graphs/{id}/relationships/viewers"},
    {"method": "GET", "path": "api/v3/graphs/{id}/relationships/viewers/{id}"},
    {"method": "GET", "path": "api/v3/yara_rules"},
    {"method": "GET", "path": "api/v3/yara_rules/{id}"},
    {"method": "GET", "path": "api/v3/yara_rules/{id}/relationships/{id}"},
    {"method": "GET", "path": "api/v3/yara_rules/{id}/{id}"},
    {"method": "GET", "path": "api/v3/intelligence/zip_files/{id}"},
    {"method": "GET", "path": "api/v3/intelligence/zip_files/{id}/download"},
    {"method": "GET", "path": "api/v3/intelligence/zip_files/{id}/download_url"},
    {"method": "GET", "path": "api/v3/private/zip_files/{id}"},
    {"method": "GET", "path": "api/v3/private/zip_files/{id}/download"},
    {"method": "GET", "path": "api/v3/private/zip_files/{id}/download_url"}
  ],
  "deny": [
    {"method": "GET", "path": "api/v3/files/upload_url"},
    {"method": "GET", "path": "api/v3/private/files/upload_url"}
  ]
}
```

## Endpoints

The VirusTotal endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/v3/analyses/{id} | read | analyses | Get a URL / file analysis. |
| GET | api/v3/analyses/{id}/relationships/{id} | read | analyses | Get object descriptors related to an analysis. |
| GET | api/v3/analyses/{id}/{id} | read | analyses | Get objects related to an analysis. |
| GET | api/v3/operations/{id} | read | analyses | Get an operation object. |
| GET | api/v3/submission/{id} | read | analyses | Get a submission object. |
| GET | api/v3/attack_tactics/{id} | read | attack tactics | Get an attack tactic object. |
| GET | api/v3/attack_tactics/{id}/relationships/{id} | read | attack tactics | Get object descriptors related to an attack tactic. |
| GET | api/v3/attack_tactics/{id}/{id} | read | attack tactics | Get objects related to an attack tactic. |
| GET | api/v3/attack_techniques/{id} | read | attack techniques | Get an attack technique object. |
| GET | api/v3/attack_techniques/{id}/relationships/{id} | read | attack techniques | Get object descriptors related to an attack technique. |
| GET | api/v3/attack_techniques/{id}/{id} | read | attack techniques | Get objects related to an attack technique. |
| GET | api/v3/groups/{id}/activity_log_entries | read | audit log | Get Activity Logs. |
| POST | api/v3/codeinsights/analyse-binary | write | code insights | Analyse code blocks with Code Insights. |
| GET | api/v3/collections | read | collections | List collections. |
| POST | api/v3/collections | write | collections | Create a new collection. |
| GET | api/v3/collections/{id} | read | collections | Get a collection. |
| PATCH | api/v3/collections/{id} | write | collections | Update a collection. |
| DELETE | api/v3/collections/{id} | write | collections | Delete a collection. |
| GET | api/v3/collections/{id}/aggregations/download/{id} | read | collections | Export aggregations from a collection. |
| GET | api/v3/collections/{id}/comments | read | collections | Get comments on a collection. |
| POST | api/v3/collections/{id}/comments | write | collections | Add a comment to a collection. |
| GET | api/v3/collections/{id}/download/{id} | read | collections | Export IOCs from a collection. |
| GET | api/v3/collections/{id}/relationships/{id} | read | collections | Get object descriptors related to a collection. |
| GET | api/v3/collections/{id}/search | read | collections | Search IoCs inside a collection. |
| GET | api/v3/collections/{id}/{id} | read | collections | Get objects related to a collection. |
| POST | api/v3/collections/{id}/{id} | write | collections | Add new items to a collection. |
| DELETE | api/v3/collections/{id}/{id} | write | collections | Delete items from a collection. |
| GET | api/v3/collections/{id}/{id}/download/{id} | read | collections | Export IOCs from a given collection's relationship. |
| GET | api/v3/comments | read | comments | Get latest comments. |
| GET | api/v3/comments/{id} | read | comments | Get a comment object. |
| DELETE | api/v3/comments/{id} | write | comments | Delete a comment. |
| GET | api/v3/comments/{id}/relationships/{id} | read | comments | Get object descriptors related to a comment. |
| POST | api/v3/comments/{id}/vote | write | comments | Add a vote to a comment. |
| GET | api/v3/comments/{id}/{id} | read | comments | Get objects related to a comment. |
| GET | api/v3/feeds/domains/hourly/{id} | read | domain intelligence feed | Get an hourly domain feed batch. |
| GET | api/v3/feeds/domains/{id} | read | domain intelligence feed | Get a minutely domain feed batch. |
| GET | api/v3/domains/{id} | read | domains & resolutions | Get a domain report. |
| POST | api/v3/domains/{id}/analyse | write | domains & resolutions | Request an domain (re)scan. |
| GET | api/v3/domains/{id}/comments | read | domains & resolutions | Get comments on a domain. |
| POST | api/v3/domains/{id}/comments | write | domains & resolutions | Add a comment to a domain. |
| GET | api/v3/domains/{id}/relationships/{id} | read | domains & resolutions | Get object descriptors related to a domain. |
| GET | api/v3/domains/{id}/votes | read | domains & resolutions | Get votes on a domain. |
| POST | api/v3/domains/{id}/votes | write | domains & resolutions | Add a vote to a domain. |
| GET | api/v3/domains/{id}/{id} | read | domains & resolutions | Get objects related to a domain. |
| GET | api/v3/resolutions/{id} | read | domains & resolutions | Get a DNS resolution object. |
| GET | api/v3/file_behaviours/{id} | read | file behaviours | Get a file behavior report from a sandbox. |
| GET | api/v3/file_behaviours/{id}/evtx | read | file behaviours | Get the EVTX file generated during a file’s behavior analysis. |
| GET | api/v3/file_behaviours/{id}/html | read | file behaviours | Get a detailed HTML behaviour report. |
| GET | api/v3/file_behaviours/{id}/memdump | read | file behaviours | Get the memdump file generated during a file’s behavior analysis. |
| GET | api/v3/file_behaviours/{id}/pcap | read | file behaviours | Get the PCAP file generated during a file’s behavior analysis. |
| GET | api/v3/file_behaviours/{id}/relationships/{id} | read | file behaviours | Get object descriptors related to a behaviour report. |
| GET | api/v3/file_behaviours/{id}/{id} | read | file behaviours | Get objects related to a behaviour report. |
| GET | api/v3/files/{id}/behaviour_mitre_trees | read | file behaviours | Get a summary of all MITRE ATT&CK techniques observed in a file. |
| GET | api/v3/files/{id}/behaviour_summary | read | file behaviours | Get a summary of all behavior reports for a file. |
| GET | api/v3/files/{id}/behaviours | read | file behaviours | Get all behavior reports for a file. |
| GET | api/v3/feeds/files/hourly/{id} | read | file intelligence feed | Get a hourly file feed batch. |
| GET | api/v3/feeds/files/{id} | read | file intelligence feed | Get a per-minute file feed batch. |
| GET | api/v3/feeds/files/{id}/download | read | file intelligence feed | Download a file published in the file feed. |
| POST | api/v3/files | write | files | Upload a file for analysis. Shares the file with the VirusTotal community. |
| GET | api/v3/files/upload_url | write | files | Get a URL for uploading large files. Kept out of read: prepares a file upload. |
| GET | api/v3/files/{id} | read | files | Get a file report. |
| POST | api/v3/files/{id}/analyse | write | files | Request a file rescan (re-analyze). |
| GET | api/v3/files/{id}/comments | read | files | Get comments on a file. |
| POST | api/v3/files/{id}/comments | write | files | Add a comment to a file. |
| GET | api/v3/files/{id}/download | read | files | Download a file. |
| GET | api/v3/files/{id}/download_url | read | files | Get a file’s download URL. |
| GET | api/v3/files/{id}/relationships/{id} | read | files | Get object descriptors related to a file. |
| GET | api/v3/files/{id}/votes | read | files | Get votes on a file. |
| POST | api/v3/files/{id}/votes | write | files | Add a vote on a file. |
| GET | api/v3/files/{id}/{id} | read | files | Get objects related to a file. |
| GET | api/v3/sigma_rules/{id} | read | files | Get a crowdsourced Sigma rule object. |
| GET | api/v3/yara_rulesets/{id} | read | files | Get a crowdsourced YARA ruleset. |
| GET | api/v3/groups/{id} | read | group management | Get a group object. |
| PATCH | api/v3/groups/{id} | write | group management | Update a group object. |
| GET | api/v3/groups/{id}/relationships/administrators | read | group management | Get administrators for a group. |
| GET | api/v3/groups/{id}/relationships/administrators/{id} | read | group management | Check if a user is a group admin. |
| GET | api/v3/groups/{id}/relationships/users | read | group management | Get group users. |
| POST | api/v3/groups/{id}/relationships/users | write | group management | Add users to a group. |
| PATCH | api/v3/groups/{id}/relationships/users | write | group management | Manage the roles of users in a group. |
| GET | api/v3/groups/{id}/relationships/users/{id} | read | group management | Check if a user is a group member. |
| DELETE | api/v3/groups/{id}/relationships/users/{id} | write | group management | Remove a user from a group. |
| GET | api/v3/groups/{id}/relationships/{id} | read | group management | Get object descriptors related to a group. |
| GET | api/v3/groups/{id}/{id} | read | group management | Get objects related to a group. |
| GET | api/v3/ioc_stream | read | ioc stream | Get objects from the IoC Stream. |
| DELETE | api/v3/ioc_stream | write | ioc stream | Delete notifications from the IoC Stream. |
| GET | api/v3/ioc_stream_notifications/{id} | read | ioc stream | Get an IoC Stream notification. |
| DELETE | api/v3/ioc_stream_notifications/{id} | write | ioc stream | Delete an IoC Stream notification. |
| GET | api/v3/ip_addresses/{id} | read | ip addresses | Get an IP address report. |
| POST | api/v3/ip_addresses/{id}/analyse | write | ip addresses | Request an IP address (re)scan. |
| GET | api/v3/ip_addresses/{id}/comments | read | ip addresses | Get comments on an IP address. |
| POST | api/v3/ip_addresses/{id}/comments | write | ip addresses | Add a comment to an IP address. |
| GET | api/v3/ip_addresses/{id}/relationships/{id} | read | ip addresses | Get object descriptors related to an IP address. |
| GET | api/v3/ip_addresses/{id}/scanning_technologies | read | ip addresses | Get the technologies detected on an IP address. |
| GET | api/v3/ip_addresses/{id}/votes | read | ip addresses | Get votes on an IP address. |
| POST | api/v3/ip_addresses/{id}/votes | write | ip addresses | Add a vote to an IP address. |
| GET | api/v3/ip_addresses/{id}/{id} | read | ip addresses | Get objects related to an IP address. |
| GET | api/v3/feeds/ip_addresses/hourly/{id} | read | ip intelligence feed | Get an hourly IP address feed batch. |
| GET | api/v3/feeds/ip_addresses/{id} | read | ip intelligence feed | Get a minutely IP address feed batch. |
| GET | api/v3/intelligence/hunting_notification_files | read | livehunt | Retrieve file objects for Livehunt notifications. |
| GET | api/v3/intelligence/hunting_notifications | read | livehunt | Get Livehunt notifications. |
| DELETE | api/v3/intelligence/hunting_notifications | write | livehunt | Delete Livehunt notifications. |
| GET | api/v3/intelligence/hunting_notifications/{id} | read | livehunt | Get a Livehunt notification object. |
| DELETE | api/v3/intelligence/hunting_notifications/{id} | write | livehunt | Delete a Livehunt notification. |
| GET | api/v3/intelligence/hunting_rulesets | read | livehunt | Get Livehunt rulesets. |
| POST | api/v3/intelligence/hunting_rulesets | write | livehunt | Create a new Livehunt ruleset. |
| DELETE | api/v3/intelligence/hunting_rulesets | write | livehunt | Remove all Livehunt rulesets. |
| GET | api/v3/intelligence/hunting_rulesets/{id} | read | livehunt | Get a Livehunt ruleset. |
| PATCH | api/v3/intelligence/hunting_rulesets/{id} | write | livehunt | Update a Livehunt ruleset. |
| DELETE | api/v3/intelligence/hunting_rulesets/{id} | write | livehunt | Delete a Livehunt ruleset. |
| POST | api/v3/intelligence/hunting_rulesets/{id}/relationships/editors | write | livehunt | Grant Livehunt ruleset edit permissions for a user or group. |
| GET | api/v3/intelligence/hunting_rulesets/{id}/relationships/editors/{id} | read | livehunt | Check if a user or group is a Livehunt ruleset editor. |
| DELETE | api/v3/intelligence/hunting_rulesets/{id}/relationships/editors/{id} | write | livehunt | Revoke Livehunt ruleset edit permission from a user or group. |
| POST | api/v3/intelligence/hunting_rulesets/{id}/relationships/owner | write | livehunt | Transfer Livehunt ruleset to another user. |
| GET | api/v3/intelligence/hunting_rulesets/{id}/relationships/{id} | read | livehunt | Get object descriptors related to a Livehunt ruleset. |
| GET | api/v3/intelligence/hunting_rulesets/{id}/{id} | read | livehunt | Get objects related to a Livehunt ruleset. |
| GET | api/v3/popular_threat_categories | read | popular threat categories | Get a list of popular threat categories. |
| GET | api/v3/port_analyses/{id} | read | ports & services | Get a Port Analysis object. |
| GET | api/v3/port_analyses/{id}/relationships/{id} | read | ports & services | Get object descriptors related to a Port Analysis. |
| GET | api/v3/port_analyses/{id}/{id} | read | ports & services | Get objects related to a Port Analysis. |
| GET | api/v3/port_infos/{id} | read | ports & services | Get a Port Info object. |
| GET | api/v3/port_infos/{id}/relationships/{id} | read | ports & services | Get object descriptors related to a Port Info. |
| GET | api/v3/port_infos/{id}/{id} | read | ports & services | Get objects related to a Port Info. |
| GET | api/v3/private/analyses | read | private analyses | List private analyses. |
| GET | api/v3/private/analyses/{id} | read | private analyses | Get a private analysis. |
| GET | api/v3/private/analyses/{id}/relationships/{id} | read | private analyses | Get object descriptors related to a private analysis. |
| GET | api/v3/private/analyses/{id}/{id} | read | private analyses | Get objects related to a private analysis. |
| GET | api/v3/private/file/{id}/behaviours | read | private file behaviours | Get the behaviour reports from a private file. |
| GET | api/v3/private/file_behaviours/{id} | read | private file behaviours | Get a behaviour report from a private file. |
| GET | api/v3/private/file_behaviours/{id}/evtx | read | private file behaviours | Get the EVTX file generated during a private file’s behavior analysis. |
| GET | api/v3/private/file_behaviours/{id}/html | read | private file behaviours | Get a detailed HTML behaviour report. |
| GET | api/v3/private/file_behaviours/{id}/memdump | read | private file behaviours | Get the memdump file generated during a private file’s behavior analysis. |
| GET | api/v3/private/file_behaviours/{id}/pcap | read | private file behaviours | Get the PCAP file generated during a private file’s behavior analysis. |
| GET | api/v3/private/file_behaviours/{id}/relationships/{id} | read | private file behaviours | Get object descriptors related to a private file's behaviour report. |
| GET | api/v3/private/file_behaviours/{id}/{id} | read | private file behaviours | Get objects related to a private file's behaviour report. |
| GET | api/v3/private/files/{id}/behaviour_mitre_trees | read | private file behaviours | Get a summary of all MITRE ATT&CK techniques observed in a file. |
| GET | api/v3/private/files/{id}/behaviour_summary | read | private file behaviours | Get a summary of all behavior reports for a file. |
| GET | api/v3/private/files | read | private files | List private files. |
| POST | api/v3/private/files | write | private files | Upload a file. |
| GET | api/v3/private/files/upload_url | write | private files | Get a URL for uploading large files. Kept out of read: prepares a file upload. |
| GET | api/v3/private/files/{id} | read | private files | Get a private file report. |
| DELETE | api/v3/private/files/{id} | write | private files | Delete a private file report. |
| POST | api/v3/private/files/{id}/analyse | write | private files | Rescan a private file. |
| GET | api/v3/private/files/{id}/relationships/{id} | read | private files | Get object descriptors related to a file. |
| GET | api/v3/private/files/{id}/{id} | read | private files | Get objects related to a private file. |
| POST | api/v3/private/urls | write | private urls | Private Scan URL. |
| GET | api/v3/private/urls/{id} | read | private urls | Get a URL analysis report. |
| GET | api/v3/private/urls/{id}/relationships/{id} | read | private urls | Get object descriptors related to a private URL. |
| GET | api/v3/private/urls/{id}/{id} | read | private urls | Get objects related to a private URL. |
| GET | api/v3/groups/{id}/api_usage | read | quota management | Get a group’s API usage. |
| GET | api/v3/groups/{id}/users_consuming_quota/{id} | read | quota management | Get a group's usage per feature. |
| GET | api/v3/users/{id}/api_usage | read | quota management | Get a user’s API usage. |
| GET | api/v3/intelligence/retrohunt_jobs | read | retrohunt | Get a list of Retrohunt jobs. |
| POST | api/v3/intelligence/retrohunt_jobs | write | retrohunt | Create a new Retrohunt job. |
| GET | api/v3/intelligence/retrohunt_jobs/{id} | read | retrohunt | Get a Retrohunt job object. |
| DELETE | api/v3/intelligence/retrohunt_jobs/{id} | write | retrohunt | Delete a Retrohunt job. |
| POST | api/v3/intelligence/retrohunt_jobs/{id}/abort | write | retrohunt | Abort a Retrohunt job. |
| GET | api/v3/intelligence/retrohunt_jobs/{id}/matching_files | read | retrohunt | Retrieve matches for a Retrohunt job. |
| GET | api/v3/feeds/file_behaviours/hourly/{id} | read | sandbox analyses feed | Get an hourly file behaviour feed batch. |
| GET | api/v3/feeds/file_behaviours/{id} | read | sandbox analyses feed | Get a per-minute file behaviour feed batch. |
| GET | api/v3/feeds/file_behaviours/{id}/evtx | read | sandbox analyses feed | Get the EVTX file generated during a file’s behavior analysis. |
| GET | api/v3/feeds/file_behaviours/{id}/html | read | sandbox analyses feed | Get a file behaviour's detailed HTML report. |
| GET | api/v3/feeds/file_behaviours/{id}/memdump | read | sandbox analyses feed | Get the memdump file generated during a file’s behavior analysis. |
| GET | api/v3/feeds/file_behaviours/{id}/pcap | read | sandbox analyses feed | Get the PCAP file generated during a file’s behavior analysis. |
| GET | api/v3/saved_searches | read | saved searches | List Saved Searches. |
| POST | api/v3/saved_searches | write | saved searches | Create a Saved Search. |
| GET | api/v3/saved_searches/{id} | read | saved searches | Get a Saved Search. |
| PATCH | api/v3/saved_searches/{id} | write | saved searches | Update a Saved Search. |
| DELETE | api/v3/saved_searches/{id} | write | saved searches | Delete a Saved Search. |
| GET | api/v3/saved_searches/{id}/relationship/{id} | read | saved searches | Get object descriptors related to a Saved Search. |
| POST | api/v3/saved_searches/{id}/relationship/{id} | write | saved searches | Share a Saved Search. |
| DELETE | api/v3/saved_searches/{id}/relationship/{id} | write | saved searches | Revoke access to a Saved Search. |
| GET | api/v3/saved_searches/{id}/{id} | read | saved searches | Get objects related to a Saved Search. |
| GET | api/v3/intelligence/search | read | search & metadata | Advanced corpus search. |
| GET | api/v3/intelligence/search/snippets/{id} | read | search & metadata | Get file content search snippets. |
| GET | api/v3/metadata | read | search & metadata | Get VirusTotal metadata. |
| GET | api/v3/search | read | search & metadata | Search for files, URLs, domains, IPs and comments. |
| GET | api/v3/groups/{id}/relationships/service_accounts | read | service account management | Get Service Accounts of a group. |
| POST | api/v3/groups/{id}/relationships/service_accounts | write | service account management | Create a new Service Account. |
| PATCH | api/v3/groups/{id}/relationships/service_accounts | write | service account management | Update a service account object. |
| GET | api/v3/service_accounts/{id} | read | service account management | Get a Service Account object. |
| GET | api/v3/feeds/urls/hourly/{id} | read | url intelligence feed | Get an hourly URL feed batch. |
| GET | api/v3/feeds/urls/{id} | read | url intelligence feed | Get a minutely URL feed batch. |
| POST | api/v3/urls | write | urls | Scan a URL. Shares the URL with the VirusTotal community. |
| GET | api/v3/urls/{id} | read | urls | Get a URL report. |
| POST | api/v3/urls/{id}/analyse | write | urls | Request a URL rescan (re-analyze). |
| GET | api/v3/urls/{id}/comments | read | urls | Get comments on a URL. |
| POST | api/v3/urls/{id}/comments | write | urls | Add a comment on a URL. |
| GET | api/v3/urls/{id}/relationships/{id} | read | urls | Get object descriptors related to a URL. |
| GET | api/v3/urls/{id}/votes | read | urls | Get votes on a URL. |
| POST | api/v3/urls/{id}/votes | write | urls | Add a vote on a URL. |
| GET | api/v3/urls/{id}/{id} | read | urls | Get objects related to a URL. |
| GET | api/v3/users/{id} | write | user management | Get a user object. Kept out of read: returns the account's API key for your own user. |
| PATCH | api/v3/users/{id} | write | user management | Update a user object. |
| DELETE | api/v3/users/{id} | write | user management | Delete a user. |
| GET | api/v3/users/{id}/relationships/{id} | read | user management | Get object descriptors related to a user. |
| GET | api/v3/users/{id}/{id} | read | user management | Get objects related to a user. |
| GET | api/v3/graphs | read | vt graphs | Search graphs. |
| POST | api/v3/graphs | write | vt graphs | Create a graph. |
| GET | api/v3/graphs/{id} | read | vt graphs | Get a graph object. |
| PATCH | api/v3/graphs/{id} | write | vt graphs | Update a graph object. |
| DELETE | api/v3/graphs/{id} | write | vt graphs | Delete a graph. |
| GET | api/v3/graphs/{id}/comments | read | vt graphs | Get comments on a graph. |
| POST | api/v3/graphs/{id}/comments | write | vt graphs | Add a comment to a graph. |
| GET | api/v3/graphs/{id}/relationships/{id} | read | vt graphs | Get object descriptors related to a graph. |
| GET | api/v3/graphs/{id}/{id} | read | vt graphs | Get objects related to a graph. |
| GET | api/v3/graphs/{id}/relationships/editors | read | vt graphs permissions & acl | Get users and groups that can edit a graph. |
| POST | api/v3/graphs/{id}/relationships/editors | write | vt graphs permissions & acl | Grant users and groups permission to edit a graph. |
| GET | api/v3/graphs/{id}/relationships/editors/{id} | read | vt graphs permissions & acl | Check if a user or group can edit a graph. |
| DELETE | api/v3/graphs/{id}/relationships/editors/{id} | write | vt graphs permissions & acl | Revoke edit graph permissions from a user or group. |
| GET | api/v3/graphs/{id}/relationships/viewers | read | vt graphs permissions & acl | Get users and groups that can view a graph. |
| POST | api/v3/graphs/{id}/relationships/viewers | write | vt graphs permissions & acl | Grant users and groups permission to see a graph. |
| GET | api/v3/graphs/{id}/relationships/viewers/{id} | read | vt graphs permissions & acl | Check if a user or group can view a graph. |
| DELETE | api/v3/graphs/{id}/relationships/viewers/{id} | write | vt graphs permissions & acl | Revoke view permission from a user or group. |
| GET | api/v3/yara_rules | read | yara rules | List Crowdsourced YARA Rules. |
| GET | api/v3/yara_rules/{id} | read | yara rules | Get a Crowdsourced YARA rule. |
| GET | api/v3/yara_rules/{id}/relationships/{id} | read | yara rules | Get objects descriptors related to a Crowdsourced YARA rule. |
| GET | api/v3/yara_rules/{id}/{id} | read | yara rules | Get objects related to a Crowdsourced YARA rule. |
| POST | api/v3/intelligence/zip_files | write | zipping files | Create a password-protected ZIP with VirusTotal files. |
| GET | api/v3/intelligence/zip_files/{id} | read | zipping files | Check a ZIP file’s status. |
| GET | api/v3/intelligence/zip_files/{id}/download | read | zipping files | Download a ZIP file. |
| GET | api/v3/intelligence/zip_files/{id}/download_url | read | zipping files | Get a ZIP file’s download URL. |
| POST | api/v3/private/zip_files | write | zipping private files | Create a password-protected ZIP with VirusTotal private files. |
| GET | api/v3/private/zip_files/{id} | read | zipping private files | Check a ZIP file’s status. |
| GET | api/v3/private/zip_files/{id}/download | read | zipping private files | Download a ZIP file. |
| GET | api/v3/private/zip_files/{id}/download_url | read | zipping private files | Get a ZIP file’s download URL. |
