# Zoom Admin access policy

An access policy limits which endpoints Zoom Admin connections may call through Maton. Zoom Admin doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/zoom-admin#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Zoom Admin: its 309 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create zoom-admin --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v2/accounts"},
    {"method": "GET", "path": "v2/accounts/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/archive_files"},
    {"method": "GET", "path": "v2/accounts/{id}/groups"},
    {"method": "GET", "path": "v2/accounts/{id}/groups/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/groups/{id}/admins"},
    {"method": "GET", "path": "v2/accounts/{id}/groups/{id}/channels"},
    {"method": "GET", "path": "v2/accounts/{id}/groups/{id}/lock_settings"},
    {"method": "GET", "path": "v2/accounts/{id}/groups/{id}/members"},
    {"method": "GET", "path": "v2/accounts/{id}/groups/{id}/settings"},
    {"method": "GET", "path": "v2/accounts/{id}/groups/{id}/settings/registration"},
    {"method": "GET", "path": "v2/accounts/{id}/h323/devices"},
    {"method": "GET", "path": "v2/accounts/{id}/information_barriers/policies"},
    {"method": "GET", "path": "v2/accounts/{id}/information_barriers/policies/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/lock_settings"},
    {"method": "GET", "path": "v2/accounts/{id}/managed_domains"},
    {"method": "GET", "path": "v2/accounts/{id}/meetings/meeting_summaries"},
    {"method": "GET", "path": "v2/accounts/{id}/meetings/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/meetings/{id}/invitation"},
    {"method": "GET", "path": "v2/accounts/{id}/meetings/{id}/livestream"},
    {"method": "GET", "path": "v2/accounts/{id}/meetings/{id}/meeting_summary"},
    {"method": "GET", "path": "v2/accounts/{id}/meetings/{id}/polls"},
    {"method": "GET", "path": "v2/accounts/{id}/meetings/{id}/polls/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/meetings/{id}/registrants"},
    {"method": "GET", "path": "v2/accounts/{id}/meetings/{id}/registrants/questions"},
    {"method": "GET", "path": "v2/accounts/{id}/meetings/{id}/registrants/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/meetings/{id}/survey"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/ai/adoption"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/ai/kpis"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/ai/usage/details"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/ai/usage/trend"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/aic/roi/kpis"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/aic/roi/meeting_summary_usage"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/chat"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/client/feedback"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/client/feedback/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/client/satisfaction"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/client_versions"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/crc"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/issues/zoomrooms"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/issues/zoomrooms/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/meetings"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/meetings/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/meetings/{id}/participants"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/meetings/{id}/participants/qos"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/meetings/{id}/participants/satisfaction"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/meetings/{id}/participants/sharing"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/meetings/{id}/participants/{id}/qos"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/quality"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/webinars"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/webinars/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/webinars/{id}/participants"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/webinars/{id}/participants/qos"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/webinars/{id}/participants/satisfaction"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/webinars/{id}/participants/sharing"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/webinars/{id}/participants/{id}/qos"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/zoomrooms"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/zoomrooms/issues"},
    {"method": "GET", "path": "v2/accounts/{id}/metrics/zoomrooms/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/past_meetings/{id}/instances"},
    {"method": "GET", "path": "v2/accounts/{id}/past_webinars/{id}/absentees"},
    {"method": "GET", "path": "v2/accounts/{id}/past_webinars/{id}/instances"},
    {"method": "GET", "path": "v2/accounts/{id}/report/activities"},
    {"method": "GET", "path": "v2/accounts/{id}/report/billing"},
    {"method": "GET", "path": "v2/accounts/{id}/report/billing/invoices"},
    {"method": "GET", "path": "v2/accounts/{id}/report/cloud_recording"},
    {"method": "GET", "path": "v2/accounts/{id}/report/daily"},
    {"method": "GET", "path": "v2/accounts/{id}/report/disclaimer"},
    {"method": "GET", "path": "v2/accounts/{id}/report/history_meetings"},
    {"method": "GET", "path": "v2/accounts/{id}/report/meeting_activities"},
    {"method": "GET", "path": "v2/accounts/{id}/report/meetings/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/report/meetings/{id}/participants"},
    {"method": "GET", "path": "v2/accounts/{id}/report/meetings/{id}/polls"},
    {"method": "GET", "path": "v2/accounts/{id}/report/meetings/{id}/qa"},
    {"method": "GET", "path": "v2/accounts/{id}/report/meetings/{id}/survey"},
    {"method": "GET", "path": "v2/accounts/{id}/report/operationlogs"},
    {"method": "GET", "path": "v2/accounts/{id}/report/remote_support"},
    {"method": "GET", "path": "v2/accounts/{id}/report/telephone"},
    {"method": "GET", "path": "v2/accounts/{id}/report/upcoming_events"},
    {"method": "GET", "path": "v2/accounts/{id}/report/users"},
    {"method": "GET", "path": "v2/accounts/{id}/report/users/{id}/meetings"},
    {"method": "GET", "path": "v2/accounts/{id}/report/webinars/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/report/webinars/{id}/participants"},
    {"method": "GET", "path": "v2/accounts/{id}/report/webinars/{id}/polls"},
    {"method": "GET", "path": "v2/accounts/{id}/report/webinars/{id}/qa"},
    {"method": "GET", "path": "v2/accounts/{id}/report/webinars/{id}/survey"},
    {"method": "GET", "path": "v2/accounts/{id}/roles"},
    {"method": "GET", "path": "v2/accounts/{id}/roles/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/roles/{id}/members"},
    {"method": "GET", "path": "v2/accounts/{id}/settings"},
    {"method": "GET", "path": "v2/accounts/{id}/settings/registration"},
    {"method": "GET", "path": "v2/accounts/{id}/sip_phones/phones"},
    {"method": "GET", "path": "v2/accounts/{id}/sip_trunk/callout_countries"},
    {"method": "GET", "path": "v2/accounts/{id}/sip_trunk/internal_numbers"},
    {"method": "GET", "path": "v2/accounts/{id}/sip_trunk/settings"},
    {"method": "GET", "path": "v2/accounts/{id}/sip_trunk/trunks"},
    {"method": "GET", "path": "v2/accounts/{id}/surveys"},
    {"method": "GET", "path": "v2/accounts/{id}/surveys/channels/{id}/instances"},
    {"method": "GET", "path": "v2/accounts/{id}/surveys/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/surveys/{id}/answers"},
    {"method": "GET", "path": "v2/accounts/{id}/surveys/{id}/instances"},
    {"method": "GET", "path": "v2/accounts/{id}/tracking_fields"},
    {"method": "GET", "path": "v2/accounts/{id}/tracking_fields/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/trusted_domains"},
    {"method": "GET", "path": "v2/accounts/{id}/tsp"},
    {"method": "GET", "path": "v2/accounts/{id}/users"},
    {"method": "GET", "path": "v2/accounts/{id}/users/summary"},
    {"method": "GET", "path": "v2/accounts/{id}/users/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/users/{id}/assistants"},
    {"method": "GET", "path": "v2/accounts/{id}/users/{id}/meeting_summaries"},
    {"method": "GET", "path": "v2/accounts/{id}/users/{id}/meeting_templates"},
    {"method": "GET", "path": "v2/accounts/{id}/users/{id}/meetings"},
    {"method": "GET", "path": "v2/accounts/{id}/users/{id}/pac"},
    {"method": "GET", "path": "v2/accounts/{id}/users/{id}/permissions"},
    {"method": "GET", "path": "v2/accounts/{id}/users/{id}/schedulers"},
    {"method": "GET", "path": "v2/accounts/{id}/users/{id}/settings"},
    {"method": "GET", "path": "v2/accounts/{id}/users/{id}/tsp"},
    {"method": "GET", "path": "v2/accounts/{id}/users/{id}/tsp/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/users/{id}/webinar_templates"},
    {"method": "GET", "path": "v2/accounts/{id}/users/{id}/webinars"},
    {"method": "GET", "path": "v2/accounts/{id}/webinars/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/webinars/{id}/branding"},
    {"method": "GET", "path": "v2/accounts/{id}/webinars/{id}/livestream"},
    {"method": "GET", "path": "v2/accounts/{id}/webinars/{id}/panelists"},
    {"method": "GET", "path": "v2/accounts/{id}/webinars/{id}/polls"},
    {"method": "GET", "path": "v2/accounts/{id}/webinars/{id}/polls/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/webinars/{id}/registrants"},
    {"method": "GET", "path": "v2/accounts/{id}/webinars/{id}/registrants/questions"},
    {"method": "GET", "path": "v2/accounts/{id}/webinars/{id}/registrants/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/webinars/{id}/survey"},
    {"method": "GET", "path": "v2/accounts/{id}/webinars/{id}/tracking_sources"},
    {"method": "GET", "path": "v2/data_requests/requests"},
    {"method": "GET", "path": "v2/data_requests/requests/{id}"},
    {"method": "GET", "path": "v2/information_barriers/policies"},
    {"method": "GET", "path": "v2/information_barriers/policies/{id}"},
    {"method": "GET", "path": "v2/contacts/groups"},
    {"method": "GET", "path": "v2/contacts/groups/{id}"},
    {"method": "GET", "path": "v2/contacts/groups/{id}/members"},
    {"method": "GET", "path": "v2/devices"},
    {"method": "GET", "path": "v2/devices/groups"},
    {"method": "GET", "path": "v2/devices/zpa/settings"},
    {"method": "GET", "path": "v2/devices/zpa/zdm_groups/{id}/versions"},
    {"method": "GET", "path": "v2/devices/{id}"},
    {"method": "GET", "path": "v2/h323/devices"},
    {"method": "GET", "path": "v2/sip_phones/phones"},
    {"method": "GET", "path": "v2/sip_trunk/numbers"},
    {"method": "GET", "path": "v2/divisions"},
    {"method": "GET", "path": "v2/divisions/{id}"},
    {"method": "GET", "path": "v2/divisions/{id}/users"},
    {"method": "GET", "path": "v2/groups"},
    {"method": "GET", "path": "v2/groups/{id}"},
    {"method": "GET", "path": "v2/groups/{id}/admins"},
    {"method": "GET", "path": "v2/groups/{id}/channels"},
    {"method": "GET", "path": "v2/groups/{id}/lock_settings"},
    {"method": "GET", "path": "v2/groups/{id}/members"},
    {"method": "GET", "path": "v2/groups/{id}/settings"},
    {"method": "GET", "path": "v2/groups/{id}/settings/registration"},
    {"method": "GET", "path": "v2/archive_files"},
    {"method": "GET", "path": "v2/archive_files/download_audit"},
    {"method": "GET", "path": "v2/archive_files/statistics"},
    {"method": "GET", "path": "v2/meetings/meeting_summaries"},
    {"method": "GET", "path": "v2/meetings/{id}"},
    {"method": "GET", "path": "v2/meetings/{id}/invitation"},
    {"method": "GET", "path": "v2/meetings/{id}/livestream"},
    {"method": "GET", "path": "v2/meetings/{id}/meeting_summary"},
    {"method": "GET", "path": "v2/meetings/{id}/polls"},
    {"method": "GET", "path": "v2/meetings/{id}/polls/{id}"},
    {"method": "GET", "path": "v2/meetings/{id}/registrants"},
    {"method": "GET", "path": "v2/meetings/{id}/registrants/questions"},
    {"method": "GET", "path": "v2/meetings/{id}/registrants/{id}"},
    {"method": "GET", "path": "v2/meetings/{id}/survey"},
    {"method": "GET", "path": "v2/meetings/{id}/transcript"},
    {"method": "GET", "path": "v2/past_meetings/{id}"},
    {"method": "GET", "path": "v2/past_meetings/{id}/archive_files"},
    {"method": "GET", "path": "v2/past_meetings/{id}/instances"},
    {"method": "GET", "path": "v2/past_meetings/{id}/participants"},
    {"method": "GET", "path": "v2/past_meetings/{id}/polls"},
    {"method": "GET", "path": "v2/past_meetings/{id}/qa"},
    {"method": "GET", "path": "v2/metrics/ai/adoption"},
    {"method": "GET", "path": "v2/metrics/ai/kpis"},
    {"method": "GET", "path": "v2/metrics/ai/usage/details"},
    {"method": "GET", "path": "v2/metrics/ai/usage/trend"},
    {"method": "GET", "path": "v2/metrics/aic/roi/kpis"},
    {"method": "GET", "path": "v2/metrics/aic/roi/meeting_summary_usage"},
    {"method": "GET", "path": "v2/metrics/chat"},
    {"method": "GET", "path": "v2/metrics/client/feedback"},
    {"method": "GET", "path": "v2/metrics/client/feedback/{id}"},
    {"method": "GET", "path": "v2/metrics/client/satisfaction"},
    {"method": "GET", "path": "v2/metrics/client_versions"},
    {"method": "GET", "path": "v2/metrics/crc"},
    {"method": "GET", "path": "v2/metrics/issues/zoomrooms"},
    {"method": "GET", "path": "v2/metrics/issues/zoomrooms/{id}"},
    {"method": "GET", "path": "v2/metrics/meetings"},
    {"method": "GET", "path": "v2/metrics/meetings/{id}"},
    {"method": "GET", "path": "v2/metrics/meetings/{id}/participants"},
    {"method": "GET", "path": "v2/metrics/meetings/{id}/participants/qos"},
    {"method": "GET", "path": "v2/metrics/meetings/{id}/participants/satisfaction"},
    {"method": "GET", "path": "v2/metrics/meetings/{id}/participants/sharing"},
    {"method": "GET", "path": "v2/metrics/meetings/{id}/participants/{id}/qos"},
    {"method": "GET", "path": "v2/metrics/quality"},
    {"method": "GET", "path": "v2/metrics/webinars"},
    {"method": "GET", "path": "v2/metrics/webinars/{id}"},
    {"method": "GET", "path": "v2/metrics/webinars/{id}/participants"},
    {"method": "GET", "path": "v2/metrics/webinars/{id}/participants/qos"},
    {"method": "GET", "path": "v2/metrics/webinars/{id}/participants/satisfaction"},
    {"method": "GET", "path": "v2/metrics/webinars/{id}/participants/sharing"},
    {"method": "GET", "path": "v2/metrics/webinars/{id}/participants/{id}/qos"},
    {"method": "GET", "path": "v2/metrics/zoomrooms"},
    {"method": "GET", "path": "v2/metrics/zoomrooms/issues"},
    {"method": "GET", "path": "v2/metrics/zoomrooms/{id}"},
    {"method": "GET", "path": "v2/accounts/{id}/meetings/{id}/recordings"},
    {"method": "GET", "path": "v2/accounts/{id}/meetings/{id}/recordings/analytics_details"},
    {"method": "GET", "path": "v2/accounts/{id}/meetings/{id}/recordings/analytics_summary"},
    {"method": "GET", "path": "v2/accounts/{id}/meetings/{id}/recordings/registrants"},
    {"method": "GET", "path": "v2/accounts/{id}/meetings/{id}/recordings/registrants/questions"},
    {"method": "GET", "path": "v2/accounts/{id}/meetings/{id}/recordings/settings"},
    {"method": "GET", "path": "v2/accounts/{id}/recordings"},
    {"method": "GET", "path": "v2/accounts/{id}/users/{id}/recordings"},
    {"method": "GET", "path": "v2/meetings/{id}/recordings"},
    {"method": "GET", "path": "v2/meetings/{id}/recordings/analytics_details"},
    {"method": "GET", "path": "v2/meetings/{id}/recordings/analytics_summary"},
    {"method": "GET", "path": "v2/meetings/{id}/recordings/registrants"},
    {"method": "GET", "path": "v2/meetings/{id}/recordings/registrants/questions"},
    {"method": "GET", "path": "v2/meetings/{id}/recordings/settings"},
    {"method": "GET", "path": "v2/users/{id}/recordings"},
    {"method": "GET", "path": "v2/report/activities"},
    {"method": "GET", "path": "v2/report/billing"},
    {"method": "GET", "path": "v2/report/billing/invoices"},
    {"method": "GET", "path": "v2/report/cloud_recording"},
    {"method": "GET", "path": "v2/report/daily"},
    {"method": "GET", "path": "v2/report/disclaimer"},
    {"method": "GET", "path": "v2/report/history_meetings"},
    {"method": "GET", "path": "v2/report/meeting_activities"},
    {"method": "GET", "path": "v2/report/meetings/{id}"},
    {"method": "GET", "path": "v2/report/meetings/{id}/participants"},
    {"method": "GET", "path": "v2/report/meetings/{id}/polls"},
    {"method": "GET", "path": "v2/report/meetings/{id}/qa"},
    {"method": "GET", "path": "v2/report/meetings/{id}/survey"},
    {"method": "GET", "path": "v2/report/operationlogs"},
    {"method": "GET", "path": "v2/report/remote_support"},
    {"method": "GET", "path": "v2/report/telephone"},
    {"method": "GET", "path": "v2/report/upcoming_events"},
    {"method": "GET", "path": "v2/report/users"},
    {"method": "GET", "path": "v2/report/users/{id}/meetings"},
    {"method": "GET", "path": "v2/report/webinars/{id}"},
    {"method": "GET", "path": "v2/report/webinars/{id}/participants"},
    {"method": "GET", "path": "v2/report/webinars/{id}/polls"},
    {"method": "GET", "path": "v2/report/webinars/{id}/qa"},
    {"method": "GET", "path": "v2/report/webinars/{id}/survey"},
    {"method": "GET", "path": "v2/roles"},
    {"method": "GET", "path": "v2/roles/{id}"},
    {"method": "GET", "path": "v2/roles/{id}/members"},
    {"method": "GET", "path": "v2/sso/capabilities"},
    {"method": "GET", "path": "v2/sso/configurations"},
    {"method": "GET", "path": "v2/sso/configurations/{id}"},
    {"method": "GET", "path": "v2/sso/configurations/{id}/certificates"},
    {"method": "GET", "path": "v2/sso/configurations/{id}/mapping"},
    {"method": "GET", "path": "v2/sso/login_logs"},
    {"method": "GET", "path": "v2/sso/login_logs/{id}"},
    {"method": "GET", "path": "v2/sso/settings"},
    {"method": "GET", "path": "v2/sso/status"},
    {"method": "GET", "path": "v2/surveys"},
    {"method": "GET", "path": "v2/surveys/channels/{id}/instances"},
    {"method": "GET", "path": "v2/surveys/{id}"},
    {"method": "GET", "path": "v2/surveys/{id}/answers"},
    {"method": "GET", "path": "v2/surveys/{id}/instances"},
    {"method": "GET", "path": "v2/tracking_fields"},
    {"method": "GET", "path": "v2/tracking_fields/{id}"},
    {"method": "GET", "path": "v2/tsp"},
    {"method": "GET", "path": "v2/users"},
    {"method": "GET", "path": "v2/users/email"},
    {"method": "GET", "path": "v2/users/summary"},
    {"method": "GET", "path": "v2/users/vanity_name"},
    {"method": "GET", "path": "v2/users/{id}"},
    {"method": "GET", "path": "v2/users/{id}/assistants"},
    {"method": "GET", "path": "v2/users/{id}/collaboration_devices"},
    {"method": "GET", "path": "v2/users/{id}/collaboration_devices/{id}"},
    {"method": "GET", "path": "v2/users/{id}/meeting_summaries"},
    {"method": "GET", "path": "v2/users/{id}/meeting_summary_templates"},
    {"method": "GET", "path": "v2/users/{id}/meeting_templates"},
    {"method": "GET", "path": "v2/users/{id}/meeting_templates/{id}"},
    {"method": "GET", "path": "v2/users/{id}/meetings"},
    {"method": "GET", "path": "v2/users/{id}/pac"},
    {"method": "GET", "path": "v2/users/{id}/permissions"},
    {"method": "GET", "path": "v2/users/{id}/presence_status"},
    {"method": "GET", "path": "v2/users/{id}/schedulers"},
    {"method": "GET", "path": "v2/users/{id}/settings"},
    {"method": "GET", "path": "v2/users/{id}/settings/sensitive_label"},
    {"method": "GET", "path": "v2/users/{id}/tsp"},
    {"method": "GET", "path": "v2/users/{id}/tsp/{id}"},
    {"method": "GET", "path": "v2/users/{id}/upcoming_meetings"},
    {"method": "GET", "path": "v2/users/{id}/webinar_templates"},
    {"method": "GET", "path": "v2/users/{id}/webinars"},
    {"method": "GET", "path": "v2/past_webinars/{id}/absentees"},
    {"method": "GET", "path": "v2/past_webinars/{id}/instances"},
    {"method": "GET", "path": "v2/past_webinars/{id}/participants"},
    {"method": "GET", "path": "v2/past_webinars/{id}/polls"},
    {"method": "GET", "path": "v2/past_webinars/{id}/qa"},
    {"method": "GET", "path": "v2/webinars/{id}"},
    {"method": "GET", "path": "v2/webinars/{id}/branding"},
    {"method": "GET", "path": "v2/webinars/{id}/livestream"},
    {"method": "GET", "path": "v2/webinars/{id}/panelists"},
    {"method": "GET", "path": "v2/webinars/{id}/polls"},
    {"method": "GET", "path": "v2/webinars/{id}/polls/{id}"},
    {"method": "GET", "path": "v2/webinars/{id}/registrants"},
    {"method": "GET", "path": "v2/webinars/{id}/registrants/questions"},
    {"method": "GET", "path": "v2/webinars/{id}/registrants/{id}"},
    {"method": "GET", "path": "v2/webinars/{id}/survey"},
    {"method": "GET", "path": "v2/webinars/{id}/tracking_sources"}
  ],
  "deny": []
}
```

## Endpoints

The Zoom Admin endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v2/accounts | read | accounts | List all subaccounts created by a master account. |
| POST | v2/accounts | write | accounts | Create a subaccount under a master account. |
| GET | v2/accounts/{id} | read | accounts | Retrieve information about a master account's sub account. |
| DELETE | v2/accounts/{id} | write | accounts | Disassociate a sub account from its master account. |
| GET | v2/accounts/{id}/archive_files | read | accounts | Get an account's archived meeting or webinar files. |
| GET | v2/accounts/{id}/groups | read | accounts | List groups under an account. |
| POST | v2/accounts/{id}/groups | write | accounts | Use this API to create a group. |
| GET | v2/accounts/{id}/groups/{id} | read | accounts | Get a group under an account. |
| PATCH | v2/accounts/{id}/groups/{id} | write | accounts | Update a group under your account. |
| DELETE | v2/accounts/{id}/groups/{id} | write | accounts | Delete an entire group. |
| GET | v2/accounts/{id}/groups/{id}/admins | read | accounts | Use this API to return a list of group administrators under your account. |
| POST | v2/accounts/{id}/groups/{id}/admins | write | accounts | Use this API to add administrators to a group under your account. |
| DELETE | v2/accounts/{id}/groups/{id}/admins/{id} | write | accounts | Use this API to remove a group administrator in a Zoom account. |
| GET | v2/accounts/{id}/groups/{id}/channels | read | accounts | Returns a list of channels for a group under your account. |
| GET | v2/accounts/{id}/groups/{id}/lock_settings | read | accounts | Retrieve a group's locked settings. |
| PATCH | v2/accounts/{id}/groups/{id}/lock_settings | write | accounts | Update a group's locked settings. |
| GET | v2/accounts/{id}/groups/{id}/members | read | accounts | List the members of a group under your account. |
| POST | v2/accounts/{id}/groups/{id}/members | write | accounts | Use this API to add users to a group in your account. |
| PATCH | v2/accounts/{id}/groups/{id}/members/{id} | write | accounts | Use this API to perform either of the following tasks. |
| DELETE | v2/accounts/{id}/groups/{id}/members/{id} | write | accounts | Use this API to remove a user from a group in an account. |
| GET | v2/accounts/{id}/groups/{id}/settings | read | accounts | Get settings for a group. |
| PATCH | v2/accounts/{id}/groups/{id}/settings | write | accounts | Update settings for a group. |
| GET | v2/accounts/{id}/groups/{id}/settings/registration | read | accounts | Get webinar registration settings for a group. |
| PATCH | v2/accounts/{id}/groups/{id}/settings/registration | write | accounts | Update webinar registration settings for a group.&lt;p style=&quot;background-color:FEEFB3; color:9F6000&quot;&gt. |
| POST | v2/accounts/{id}/groups/{id}/settings/virtual_backgrounds | write | accounts | Use this API to upload Virtual Background files for all users in a group to use. |
| DELETE | v2/accounts/{id}/groups/{id}/settings/virtual_backgrounds | write | accounts | Use this API to delete a group's Virtual Background files. |
| POST | v2/accounts/{id}/groups/{id}/settings/webinar_waiting_room_branding | write | accounts | Sets the Webinar Waiting Room branding (logo, background image, video, welcome title/description, and layout) for the group. |
| GET | v2/accounts/{id}/h323/devices | read | accounts | A H.323 or SIP device can make a video call to a Room Connector to join a Zoom cloud meeting. |
| POST | v2/accounts/{id}/h323/devices | write | accounts | A H.323 or SIP device can make a video call to a Room Connector to join a Zoom cloud meeting. |
| PATCH | v2/accounts/{id}/h323/devices/{id} | write | accounts | Edit information for a H.323/SIP device from your Zoom account. |
| DELETE | v2/accounts/{id}/h323/devices/{id} | write | accounts | A H.323 or SIP device can make a video call to a Room Connector to join a Zoom cloud meeting. |
| GET | v2/accounts/{id}/information_barriers/policies | read | accounts | Return a list of all Information Barriers policies and their information. |
| POST | v2/accounts/{id}/information_barriers/policies | write | accounts | Create a new Information Barrier policy. |
| GET | v2/accounts/{id}/information_barriers/policies/{id} | read | accounts | Return an Information Barriers policy by its ID. |
| PATCH | v2/accounts/{id}/information_barriers/policies/{id} | write | accounts | Update an Information Barriers policy. |
| DELETE | v2/accounts/{id}/information_barriers/policies/{id} | write | accounts | Remove an Information Barrier policy. |
| PATCH | v2/accounts/{id}/live_meetings/{id}/events | write | accounts | In-meeting controls include starting, stopping, pausing, and resuming a recording; inviting participants; updating the waiting room with a custom message; and... |
| GET | v2/accounts/{id}/lock_settings | read | accounts | Retrieves an account's locked settings. |
| PATCH | v2/accounts/{id}/lock_settings | write | accounts | Updates an account's locked settings. |
| GET | v2/accounts/{id}/managed_domains | read | accounts | Retrieve a list of an account's managed domains. |
| GET | v2/accounts/{id}/meetings/meeting_summaries | read | accounts | Retrieve a list of all meeting or webinar summaries available for an account. |
| GET | v2/accounts/{id}/meetings/{id} | read | accounts | Retrieve the given meeting's details. |
| PATCH | v2/accounts/{id}/meetings/{id} | write | accounts | Updates meeting details. |
| DELETE | v2/accounts/{id}/meetings/{id} | write | accounts | Delete a meeting. |
| POST | v2/accounts/{id}/meetings/{id}/batch_polls | write | accounts | Polls allow the meeting host to survey attendees. |
| POST | v2/accounts/{id}/meetings/{id}/batch_registrants | write | accounts | Register up to 30 registrants at once for a meeting that requires registration. |
| GET | v2/accounts/{id}/meetings/{id}/invitation | read | accounts | Retrieve the meeting invitation note for a specific meeting. |
| POST | v2/accounts/{id}/meetings/{id}/invite_links | write | accounts | Create a batch of invitation links for a meeting. |
| GET | v2/accounts/{id}/meetings/{id}/livestream | read | accounts | Zoom allows users to livestream a meeting to a custom platform. |
| PATCH | v2/accounts/{id}/meetings/{id}/livestream | write | accounts | Update a meeting's livestream information. |
| PATCH | v2/accounts/{id}/meetings/{id}/livestream/status | write | accounts | Zoom allows users to livestream a meeting to a custom platform. |
| GET | v2/accounts/{id}/meetings/{id}/meeting_summary | read | accounts | Retrieve the summary of a meeting or webinar. |
| DELETE | v2/accounts/{id}/meetings/{id}/meeting_summary | write | accounts | Delete the summary of a meeting or webinar. |
| GET | v2/accounts/{id}/meetings/{id}/polls | read | accounts | Polls allow the meeting host to survey attendees. |
| POST | v2/accounts/{id}/meetings/{id}/polls | write | accounts | Polls allow the meeting host to survey attendees. |
| GET | v2/accounts/{id}/meetings/{id}/polls/{id} | read | accounts | Retrieves information about a specific meeting poll. |
| PUT | v2/accounts/{id}/meetings/{id}/polls/{id} | write | accounts | Polls allow the meeting host to survey attendees. |
| DELETE | v2/accounts/{id}/meetings/{id}/polls/{id} | write | accounts | Polls allow the meeting host to survey attendees. |
| GET | v2/accounts/{id}/meetings/{id}/registrants | read | accounts | List users that have registered for a meeting. |
| POST | v2/accounts/{id}/meetings/{id}/registrants | write | accounts | Create and submit a user's registration to a meeting. |
| GET | v2/accounts/{id}/meetings/{id}/registrants/questions | read | accounts | List registration questions that will be displayed to users while registering for a meeting. |
| PATCH | v2/accounts/{id}/meetings/{id}/registrants/questions | write | accounts | Update registration questions that will be displayed to users while registering for a meeting. |
| PUT | v2/accounts/{id}/meetings/{id}/registrants/status | write | accounts | Update a meeting registrant's status by either approving, cancelling or denying a registrant from joining the meeting. |
| GET | v2/accounts/{id}/meetings/{id}/registrants/{id} | read | accounts | Retrieve details on a specific user who has registered for the meeting. |
| DELETE | v2/accounts/{id}/meetings/{id}/registrants/{id} | write | accounts | Delete a meeting registrant. |
| PUT | v2/accounts/{id}/meetings/{id}/status | write | accounts | Update the status of a meeting. |
| GET | v2/accounts/{id}/meetings/{id}/survey | read | accounts | Display information about a meeting survey. |
| PATCH | v2/accounts/{id}/meetings/{id}/survey | write | accounts | Update a meeting survey. |
| DELETE | v2/accounts/{id}/meetings/{id}/survey | write | accounts | Delete a meeting survey. |
| GET | v2/accounts/{id}/meetings/{id}/token | write | accounts | Get a meeting's closed caption token (caption URL). Kept out of read: it returns a token. |
| GET | v2/accounts/{id}/metrics/ai/adoption | read | accounts | Get the AI adoption summary — active user count vs licensed user count for each AI feature across ZoomMate and AI in Workplace plans. |
| GET | v2/accounts/{id}/metrics/ai/kpis | read | accounts | Get the overall AI KPI snapshot — metrics with period-over-period change for AI feature usage across  ZoomMate and AI in Workplace plans. |
| GET | v2/accounts/{id}/metrics/ai/usage/details | read | accounts | Get AI usage and engagement details. |
| GET | v2/accounts/{id}/metrics/ai/usage/trend | read | accounts | Get the AI usage and engagement trend. |
| GET | v2/accounts/{id}/metrics/aic/roi/kpis | read | accounts | Get AIC ROI KPI data. |
| GET | v2/accounts/{id}/metrics/aic/roi/meeting_summary_usage | read | accounts | Get AIC ROI meeting summary usage data. |
| GET | v2/accounts/{id}/metrics/chat | read | accounts | Get metrics for how users are utilizing Zoom Chat to send messages. |
| GET | v2/accounts/{id}/metrics/client/feedback | read | accounts | Use this API to return Zoom meetings client feedback survey results. |
| GET | v2/accounts/{id}/metrics/client/feedback/{id} | read | accounts | Retrieve detailed information on a Zoom meetings client feedback. |
| GET | v2/accounts/{id}/metrics/client/satisfaction | read | accounts | If the End of Meeting Feedback Survey option is enabled, attendees will be prompted with a survey window where they can tap either the Thumbs Up or Thumbs Down button... |
| GET | v2/accounts/{id}/metrics/client_versions | read | accounts | Use this API to list all the client versions and its count. |
| GET | v2/accounts/{id}/metrics/crc | read | accounts | A Cloud Room Connector allows H.323/SIP endpoints to connect to a Zoom meeting. |
| GET | v2/accounts/{id}/metrics/issues/zoomrooms | read | accounts | Get information on top 25 Zoom Rooms with issues in a month. |
| GET | v2/accounts/{id}/metrics/issues/zoomrooms/{id} | read | accounts | Use this API to return information about the Zoom Rooms in an account with issues, such as disconnected hardware or bandwidth issues. |
| GET | v2/accounts/{id}/metrics/meetings | read | accounts | Lists the total live or past meetings that occurred during a specified period of time. |
| GET | v2/accounts/{id}/metrics/meetings/{id} | read | accounts | Get details on live or past meetings. |
| GET | v2/accounts/{id}/metrics/meetings/{id}/participants | read | accounts | Return a list of participants from live or past meetings. |
| GET | v2/accounts/{id}/metrics/meetings/{id}/participants/qos | read | accounts | Show a list of meeting participants from live or past meetings, and their quality of service received during the meeting. |
| GET | v2/accounts/{id}/metrics/meetings/{id}/participants/satisfaction | read | accounts | When a meeting ends, each attendee will be prompted to share their meeting experience by clicking either thumbs up or thumbs down. |
| GET | v2/accounts/{id}/metrics/meetings/{id}/participants/sharing | read | accounts | Retrieve the sharing and recording details of participants from live or past meetings. |
| GET | v2/accounts/{id}/metrics/meetings/{id}/participants/{id}/qos | read | accounts | Return the quality of service (QoS) report for participants from live or past meetings. |
| GET | v2/accounts/{id}/metrics/quality | read | accounts | Use this API to return meeting quality score information. |
| GET | v2/accounts/{id}/metrics/webinars | read | accounts | Lists all the live or past webinars from a specified period of time. |
| GET | v2/accounts/{id}/metrics/webinars/{id} | read | accounts | Retrieve details from live or past webinars. |
| GET | v2/accounts/{id}/metrics/webinars/{id}/participants | read | accounts | Get information about participants from live or past webinars. |
| GET | v2/accounts/{id}/metrics/webinars/{id}/participants/qos | read | accounts | Show a list of webinar participants from live or past webinars and the quality of service they received during the webinar. |
| GET | v2/accounts/{id}/metrics/webinars/{id}/participants/satisfaction | read | accounts | When a Webinar ends, each attendee will be prompted to share their Webinar experience by clicking either thumbs up or thumbs down. |
| GET | v2/accounts/{id}/metrics/webinars/{id}/participants/sharing | read | accounts | Retrieve the sharing and recording details of participants from live or past webinars. |
| GET | v2/accounts/{id}/metrics/webinars/{id}/participants/{id}/qos | read | accounts | Returns the quality of service (QoS) for participants during live or past webinars. |
| GET | v2/accounts/{id}/metrics/zoomrooms | read | accounts | List information on all Zoom Rooms in an account. |
| GET | v2/accounts/{id}/metrics/zoomrooms/issues | read | accounts | Get top 25 issues of Zoom Rooms. |
| GET | v2/accounts/{id}/metrics/zoomrooms/{id} | read | accounts | The Zoom Rooms dashboard metrics lets you know the type of configuration a Zoom room has and details on the meetings held in that room. |
| PATCH | v2/accounts/{id}/options | write | accounts | Update a sub account's options under the master account. |
| PUT | v2/accounts/{id}/owner | write | accounts | Changes an account's owner. |
| GET | v2/accounts/{id}/past_meetings/{id}/instances | read | accounts | Return a list of past meeting instances. |
| GET | v2/accounts/{id}/past_webinars/{id}/absentees | read | accounts | List absentees of a webinar. |
| GET | v2/accounts/{id}/past_webinars/{id}/instances | read | accounts | List past webinar instances. |
| GET | v2/accounts/{id}/report/activities | read | accounts | Retrieve a list of sign in / sign out activity logs report of users under a Zoom account. |
| GET | v2/accounts/{id}/report/billing | read | accounts | Get department billing reports of a Zoom account. |
| GET | v2/accounts/{id}/report/billing/invoices | read | accounts | Get department billing invoices reports for a specific billing period. |
| GET | v2/accounts/{id}/report/cloud_recording | read | accounts | Retrieve cloud recording usage report for a specified period. |
| GET | v2/accounts/{id}/report/daily | read | accounts | Retrieve daily report to access the account-wide usage of Zoom services for each day in a given month. |
| GET | v2/accounts/{id}/report/disclaimer | read | accounts | Retrieve a list of disclaimer records. |
| GET | v2/accounts/{id}/report/history_meetings | read | accounts | Retrieve a list of history meetings and webinars. |
| GET | v2/accounts/{id}/report/meeting_activities | read | accounts | Retrieve a list of a meeting activity logs. |
| GET | v2/accounts/{id}/report/meetings/{id} | read | accounts | Get a detailed report for a past meeting. |
| GET | v2/accounts/{id}/report/meetings/{id}/participants | read | accounts | Return a report of a past meeting with two or more participants, including the host. |
| GET | v2/accounts/{id}/report/meetings/{id}/polls | read | accounts | Use this API to get a report of poll results for a past meeting. |
| GET | v2/accounts/{id}/report/meetings/{id}/qa | read | accounts | Retrieve a report on questions asked and answered by participants from past meetings. |
| GET | v2/accounts/{id}/report/meetings/{id}/survey | read | accounts | Retrieve a report on past meeting survey. |
| GET | v2/accounts/{id}/report/operationlogs | read | accounts | The Operations Logs report allows you to audit admin and user activity, such as adding a new user, changing account settings, and deleting recordings. |
| GET | v2/accounts/{id}/report/remote_support | read | accounts | Retrieve a list of remote support records. |
| GET | v2/accounts/{id}/report/telephone | read | accounts | The telephone report allows you to view who dialed into meetings via phone (Audio Conferencing or SIP Connected Audio) and which number they dialed into and other... |
| GET | v2/accounts/{id}/report/upcoming_events | read | accounts | Use this API to list upcoming meeting and/or webinar events within a specified period of time. |
| GET | v2/accounts/{id}/report/users | read | accounts | Retrieve a host report for a specified period of time within the last six months. |
| GET | v2/accounts/{id}/report/users/{id}/meetings | read | accounts | Retrieve report on past meetings and webinars for a specified time period. |
| GET | v2/accounts/{id}/report/webinars/{id} | read | accounts | Retrieve a report containing past webinar details. |
| GET | v2/accounts/{id}/report/webinars/{id}/participants | read | accounts | Get a detailed report on each webinar attendee. |
| GET | v2/accounts/{id}/report/webinars/{id}/polls | read | accounts | Retrieve a report on past webinar polls. |
| GET | v2/accounts/{id}/report/webinars/{id}/qa | read | accounts | Retrieve a report on questions asked by participants and answered by panelists, co-hosts and hosts from past webinars. |
| GET | v2/accounts/{id}/report/webinars/{id}/survey | read | accounts | Retrieve a report on past webinar survey. |
| GET | v2/accounts/{id}/roles | read | accounts | List roles on your account. |
| POST | v2/accounts/{id}/roles | write | accounts | Each Zoom user automatically has a role which can either be owner, administrator, or member. |
| GET | v2/accounts/{id}/roles/{id} | read | accounts | Each Zoom user automatically has a role which can either be owner, administrator, or member. |
| PATCH | v2/accounts/{id}/roles/{id} | write | accounts | Each Zoom user automatically has a role which can either be owner, administrator, or a member. |
| DELETE | v2/accounts/{id}/roles/{id} | write | accounts | Each Zoom user automatically has a role which can either be owner, administrator, or a member. |
| GET | v2/accounts/{id}/roles/{id}/members | read | accounts | User roles can have a set of permissions that allows access only to the pages a user needs to view or edit. |
| POST | v2/accounts/{id}/roles/{id}/members | write | accounts | User roles can have a set of permissions that allows access only to the pages a user needs to view or edit. |
| DELETE | v2/accounts/{id}/roles/{id}/members/{id} | write | accounts | User roles can have a set of permissions that allows access only to the pages a user needs to view or edit. |
| GET | v2/accounts/{id}/settings | read | accounts | Returns an account's settings. |
| PATCH | v2/accounts/{id}/settings | write | accounts | Update an account's settings. |
| POST | v2/accounts/{id}/settings/meeting_waiting_room_branding | write | accounts | Sets the meeting Waiting Room branding (logo, background image, video, welcome title/description, and layout) for the account. |
| GET | v2/accounts/{id}/settings/registration | read | accounts | Get an account's webinar registration settings. |
| PATCH | v2/accounts/{id}/settings/registration | write | accounts | Update an account's webinar registration settings. |
| POST | v2/accounts/{id}/settings/virtual_backgrounds | write | accounts | Uploads virtual background files for all users on the account to use. |
| DELETE | v2/accounts/{id}/settings/virtual_backgrounds | write | accounts | Deletes an account's existing virtual background files. |
| POST | v2/accounts/{id}/settings/webinar_waiting_room_branding | write | accounts | Sets webinar Waiting Room branding (logo, background image, video, welcome title/description, and layout) for the account. |
| GET | v2/accounts/{id}/sip_phones/phones | read | accounts | List SIP phones on an account. |
| POST | v2/accounts/{id}/sip_phones/phones | write | accounts | Enable a user to use a SIP phone. |
| PATCH | v2/accounts/{id}/sip_phones/phones/{id} | write | accounts | Update the information of a specific SIP phone on a Zoom account. |
| DELETE | v2/accounts/{id}/sip_phones/phones/{id} | write | accounts | Delete a Zoom account's SIP phone. |
| GET | v2/accounts/{id}/sip_trunk/callout_countries | read | accounts | Retrieve the list of internal call-out countries of a master account or a sub account. |
| POST | v2/accounts/{id}/sip_trunk/callout_countries | write | accounts | Specify the list of call-out countries for a master account or a subaccount. |
| DELETE | v2/accounts/{id}/sip_trunk/callout_countries/{id} | write | accounts | Delete a previously assigned call-out country from a master account or a subaccount. |
| GET | v2/accounts/{id}/sip_trunk/internal_numbers | read | accounts | Let a master account with the SIP Connected Audio plan list internal phone numbers - numbers that are not provided by Zoom but are owned by the organization consuming... |
| POST | v2/accounts/{id}/sip_trunk/internal_numbers | write | accounts | Let a master account with a SIP Connected Audio plan to assign internal phone numbers - numbers that are not provided by Zoom but are owned by the organization... |
| PATCH | v2/accounts/{id}/sip_trunk/internal_numbers/{id} | write | accounts | Use this API to update a previously-assigned internal phone number. |
| DELETE | v2/accounts/{id}/sip_trunk/internal_numbers/{id} | write | accounts | Let a master account with SIP Connected Audio plan delete a previously assigned internal phone number from a master account or a subaccount. |
| POST | v2/accounts/{id}/sip_trunk/numbers | write | accounts | Assign internal numbers to a subaccount. |
| DELETE | v2/accounts/{id}/sip_trunk/numbers | write | accounts | Delete all internal numbers assigned to a subaccount. |
| GET | v2/accounts/{id}/sip_trunk/settings | read | accounts | Get a SIP (Session Initiation Protocol) trunk configuration. |
| PATCH | v2/accounts/{id}/sip_trunk/settings | write | accounts | Use this API to copy the Session Initiation Protocol (SIP) Connected Audio configurations applied on the master account and enable or disable those configurations on... |
| GET | v2/accounts/{id}/sip_trunk/trunks | read | accounts | List all the SIP trunks assigned to a master account or a sub account of the master account. |
| POST | v2/accounts/{id}/sip_trunk/trunks | write | accounts | Assign SIP trunks that are available on a master account to a subaccount. |
| DELETE | v2/accounts/{id}/sip_trunk/trunks/{id} | write | accounts | Remove a subaccount's existing SIP trunk. |
| GET | v2/accounts/{id}/surveys | read | accounts | Queries all surveys in the current account. |
| GET | v2/accounts/{id}/surveys/channels/{id}/instances | read | accounts | Query the channel survey instances based on channelId. |
| GET | v2/accounts/{id}/surveys/{id} | read | accounts | Queries the latest version of survey information from surveyId. |
| GET | v2/accounts/{id}/surveys/{id}/answers | read | accounts | Queries the answers of survey from surveyId. |
| GET | v2/accounts/{id}/surveys/{id}/instances | read | accounts | Query the instances which used the survey, based on surveyId. |
| GET | v2/accounts/{id}/tracking_fields | read | accounts | List all the tracking fields on your Zoom account. |
| POST | v2/accounts/{id}/tracking_fields | write | accounts | Use this API to create a new tracking field. |
| GET | v2/accounts/{id}/tracking_fields/{id} | read | accounts | Use this API to return information about a tracking field. |
| PATCH | v2/accounts/{id}/tracking_fields/{id} | write | accounts | Update a tracking field. |
| DELETE | v2/accounts/{id}/tracking_fields/{id} | write | accounts | Delete a tracking field. |
| GET | v2/accounts/{id}/trusted_domains | read | accounts | Retrieve an account's trusted domains. |
| GET | v2/accounts/{id}/tsp | read | accounts | Get information on Telephony Service Provider (TSP) on an account level. |
| PATCH | v2/accounts/{id}/tsp | write | accounts | Update information of the Telephony Service Provider (TSP) set up on an account. |
| GET | v2/accounts/{id}/users | read | accounts | Retrieve a list of your account's users. |
| POST | v2/accounts/{id}/users | write | accounts | Add a new user to your Zoom account. |
| POST | v2/accounts/{id}/users/features | write | accounts | Update multiple features for a user. |
| GET | v2/accounts/{id}/users/summary | read | accounts | Gets a summary of users, including the number and types of users in the account. |
| GET | v2/accounts/{id}/users/{id} | read | accounts | View a user's account information. |
| PATCH | v2/accounts/{id}/users/{id} | write | accounts | Updates a user's Zoom profile information. |
| DELETE | v2/accounts/{id}/users/{id} | write | accounts | Disassociate (unlink) a user or permanently delete a user. |
| PUT | v2/accounts/{id}/users/{id}/account | write | accounts | Disassociate a user from one Account and move the user to another Account under the same master account. |
| GET | v2/accounts/{id}/users/{id}/assistants | read | accounts | List a user's assistants. |
| POST | v2/accounts/{id}/users/{id}/assistants | write | accounts | Assign assistants to a user. |
| DELETE | v2/accounts/{id}/users/{id}/assistants | write | accounts | Delete all of the current user's assistants. |
| DELETE | v2/accounts/{id}/users/{id}/assistants/{id} | write | accounts | Delete a specific assistant of a user. |
| PUT | v2/accounts/{id}/users/{id}/email | write | accounts | Change a user's email address on a Zoom account that has managed domain set up. |
| GET | v2/accounts/{id}/users/{id}/meeting_summaries | read | accounts | Retrieve a list of meeting or webinar summaries hosted by the specified user. |
| GET | v2/accounts/{id}/users/{id}/meeting_templates | read | accounts | List available meeting templates for a user. |
| POST | v2/accounts/{id}/users/{id}/meeting_templates | write | accounts | Create a meeting template from an existing meeting. |
| GET | v2/accounts/{id}/users/{id}/meetings | read | accounts | List a meeting host user's scheduled meetings. |
| POST | v2/accounts/{id}/users/{id}/meetings | write | accounts | Creates a meeting for a user. |
| GET | v2/accounts/{id}/users/{id}/pac | read | accounts | Retrieve a list of a user's personal audio conference (PAC) accounts. |
| PUT | v2/accounts/{id}/users/{id}/password | write | accounts | Update the password of a user using which the user can login to Zoom. |
| GET | v2/accounts/{id}/users/{id}/permissions | read | accounts | Get permissions that have been granted to the user. |
| POST | v2/accounts/{id}/users/{id}/picture | write | accounts | Upload a user's profile picture. |
| DELETE | v2/accounts/{id}/users/{id}/picture | write | accounts | Delete a user's profile picture. |
| GET | v2/accounts/{id}/users/{id}/schedulers | read | accounts | List all of a user's schedulers. |
| DELETE | v2/accounts/{id}/users/{id}/schedulers | write | accounts | Delete all of a user's schedulers. |
| DELETE | v2/accounts/{id}/users/{id}/schedulers/{id} | write | accounts | Delete a scheduler. |
| GET | v2/accounts/{id}/users/{id}/settings | read | accounts | Retrieve a user's settings. |
| PATCH | v2/accounts/{id}/users/{id}/settings | write | accounts | Update a user's settings. |
| POST | v2/accounts/{id}/users/{id}/settings/virtual_backgrounds | write | accounts | Use this API to upload a Virtual Background files to a user's profile. |
| DELETE | v2/accounts/{id}/users/{id}/settings/virtual_backgrounds | write | accounts | Use this API to delete a user's Virtual Background files. |
| POST | v2/accounts/{id}/users/{id}/settings/webinar_waiting_room_branding | write | accounts | Sets the webinar Waiting Room branding (logo, background image, video, welcome title/description, and layout) for the user. |
| PUT | v2/accounts/{id}/users/{id}/status | write | accounts | Deactivate an active user or to reactivate a deactivated user. |
| GET | v2/accounts/{id}/users/{id}/token | write | accounts | Gets a user's Zoom token or Zoom Access Key (ZAK). Kept out of read: it returns a token. |
| DELETE | v2/accounts/{id}/users/{id}/token | write | accounts | Revokes a user's SSO token. |
| GET | v2/accounts/{id}/users/{id}/tsp | read | accounts | List all of a user's TSP accounts. |
| POST | v2/accounts/{id}/users/{id}/tsp | write | accounts | Add a user's TSP account. |
| PATCH | v2/accounts/{id}/users/{id}/tsp/settings | write | accounts | Set the URL for a global dial-in page of a user whose Zoom account has TSP and special TSP with third-party audio conferencing options enabled. |
| GET | v2/accounts/{id}/users/{id}/tsp/{id} | read | accounts | Retrieve details of a specific TSP account enabled for a specific user. |
| PATCH | v2/accounts/{id}/users/{id}/tsp/{id} | write | accounts | Update a user's Telephony Service Provider (TSP) account. |
| DELETE | v2/accounts/{id}/users/{id}/tsp/{id} | write | accounts | Delete a user's TSP account. |
| GET | v2/accounts/{id}/users/{id}/webinar_templates | read | accounts | Display a list of a user's webinar templates. |
| POST | v2/accounts/{id}/users/{id}/webinar_templates | write | accounts | Create a webinar template from an existing webinar. |
| GET | v2/accounts/{id}/users/{id}/webinars | read | accounts | List all the webinars scheduled by or on behalf a webinar host. |
| POST | v2/accounts/{id}/users/{id}/webinars | write | accounts | Schedule a webinar for a user who is a webinar host. |
| GET | v2/accounts/{id}/webinars/{id} | read | accounts | Get details for a scheduled Zoom webinar. |
| PATCH | v2/accounts/{id}/webinars/{id} | write | accounts | Make updates to a scheduled webinar. |
| DELETE | v2/accounts/{id}/webinars/{id} | write | accounts | Delete a webinar. |
| POST | v2/accounts/{id}/webinars/{id}/batch_registrants | write | accounts | Register up to 30 registrants at once for a scheduled webinar that requires registration. |
| GET | v2/accounts/{id}/webinars/{id}/branding | read | accounts | Get the webinar's session branding information. |
| POST | v2/accounts/{id}/webinars/{id}/branding/name_tags | write | accounts | Create a webinar's session branding name tag. |
| DELETE | v2/accounts/{id}/webinars/{id}/branding/name_tags | write | accounts | Delete a webinar's session branding name tag. |
| PATCH | v2/accounts/{id}/webinars/{id}/branding/name_tags/{id} | write | accounts | Update a webinar's session branding name tag. |
| POST | v2/accounts/{id}/webinars/{id}/branding/virtual_backgrounds | write | accounts | Upload a webinar's session branding virtual background. |
| PATCH | v2/accounts/{id}/webinars/{id}/branding/virtual_backgrounds | write | accounts | Set a webinar's default session branding virtual background. |
| DELETE | v2/accounts/{id}/webinars/{id}/branding/virtual_backgrounds | write | accounts | Delete a webinar's session branding virtual background. |
| POST | v2/accounts/{id}/webinars/{id}/branding/wallpaper | write | accounts | Upload a webinar's session branding wallpaper file. |
| DELETE | v2/accounts/{id}/webinars/{id}/branding/wallpaper | write | accounts | Delete a webinar's session branding wallpaper file. |
| POST | v2/accounts/{id}/webinars/{id}/invite_links | write | accounts | Create a batch of invitation links for a webinar. |
| GET | v2/accounts/{id}/webinars/{id}/livestream | read | accounts | Get a webinar's live stream configuration details, such as Stream URL, Stream Key and Page URL. |
| PATCH | v2/accounts/{id}/webinars/{id}/livestream | write | accounts | Update a webinar's live stream information. |
| PATCH | v2/accounts/{id}/webinars/{id}/livestream/status | write | accounts | Lets users live stream a webinar to a custom platform. |
| GET | v2/accounts/{id}/webinars/{id}/panelists | read | accounts | List all of a webinar's panelists. |
| POST | v2/accounts/{id}/webinars/{id}/panelists | write | accounts | Panelists in a webinar can view and send video, screen share, annotate, and do much more compared to attendees in a webinar. |
| DELETE | v2/accounts/{id}/webinars/{id}/panelists | write | accounts | Remove all the panelists from a webinar. |
| DELETE | v2/accounts/{id}/webinars/{id}/panelists/{id} | write | accounts | Remove a single panelist from a webinar. |
| GET | v2/accounts/{id}/webinars/{id}/polls | read | accounts | Lists all the polls of a webinar. |
| POST | v2/accounts/{id}/webinars/{id}/polls | write | accounts | Creates a poll for a webinar. |
| GET | v2/accounts/{id}/webinars/{id}/polls/{id} | read | accounts | Returns a webinar's poll details. |
| PUT | v2/accounts/{id}/webinars/{id}/polls/{id} | write | accounts | Updates a webinar's poll. |
| DELETE | v2/accounts/{id}/webinars/{id}/polls/{id} | write | accounts | Delete a webinar's poll. |
| GET | v2/accounts/{id}/webinars/{id}/registrants | read | accounts | List all users that have registered for a given webinar. |
| POST | v2/accounts/{id}/webinars/{id}/registrants | write | accounts | Create and submit a user's registration for a webinar. |
| GET | v2/accounts/{id}/webinars/{id}/registrants/questions | read | accounts | List registration questions and fields that are to be answered by users while registering for a webinar. |
| PATCH | v2/accounts/{id}/webinars/{id}/registrants/questions | write | accounts | Update registration questions and fields of a scheduled webinar for users to answer during webinar registration. |
| PUT | v2/accounts/{id}/webinars/{id}/registrants/status | write | accounts | Update webinar registrants' registration status. |
| GET | v2/accounts/{id}/webinars/{id}/registrants/{id} | read | accounts | Zoom users with a webinar plan have access to creating and managing webinars. |
| DELETE | v2/accounts/{id}/webinars/{id}/registrants/{id} | write | accounts | Delete a webinar registrant. |
| PUT | v2/accounts/{id}/webinars/{id}/status | write | accounts | Update a webinar's status. |
| GET | v2/accounts/{id}/webinars/{id}/survey | read | accounts | Return information about a webinar survey. |
| PATCH | v2/accounts/{id}/webinars/{id}/survey | write | accounts | Update a webinar survey. |
| DELETE | v2/accounts/{id}/webinars/{id}/survey | write | accounts | Delete a webinar survey. |
| GET | v2/accounts/{id}/webinars/{id}/token | write | accounts | Use this API to get a webinar's closed caption token (caption URL). Kept out of read: it returns a token. |
| GET | v2/accounts/{id}/webinars/{id}/tracking_sources | read | accounts | Webinar Registration Tracking Sources allow you to see where your registrants are coming from if you share the webinar registration page in multiple platforms. |
| GET | v2/data_requests/files/{id}/url | write | accounts | Returns download link for given fileId. Kept out of read: it returns a pre-signed download URL. |
| GET | v2/data_requests/requests | read | accounts | Lists all data requests for account. |
| POST | v2/data_requests/requests | write | accounts | Submit a request to. |
| GET | v2/data_requests/requests/{id} | read | accounts | Fetches downloadable file information from an individual data request. |
| DELETE | v2/data_requests/requests/{id} | write | accounts | Cancel a pending data request with ID requestId. |
| GET | v2/information_barriers/policies | read | accounts | Return a list of all Information Barriers policies and their information. |
| POST | v2/information_barriers/policies | write | accounts | Create a new Information Barrier policy. |
| GET | v2/information_barriers/policies/{id} | read | accounts | Return an Information Barriers policy by its ID. |
| PATCH | v2/information_barriers/policies/{id} | write | accounts | Update an Information Barriers policy. |
| DELETE | v2/information_barriers/policies/{id} | write | accounts | Remove an Information Barrier policy. |
| GET | v2/contacts/groups | read | contacts | List contact groups under an account. |
| POST | v2/contacts/groups | write | contacts | Use this API to create a contact group. |
| GET | v2/contacts/groups/{id} | read | contacts | Get a contact group under an account. |
| PATCH | v2/contacts/groups/{id} | write | contacts | Update a contact group under your account. |
| DELETE | v2/contacts/groups/{id} | write | contacts | Use this API to delete a contact group. |
| GET | v2/contacts/groups/{id}/members | read | contacts | List members in contact groups under an account. |
| POST | v2/contacts/groups/{id}/members | write | contacts | Use this API to add members to a contact group. |
| DELETE | v2/contacts/groups/{id}/members | write | contacts | Removes members in a contact group. |
| GET | v2/devices | read | devices | This API lets you list devices. |
| POST | v2/devices | write | devices | Add a new device to Zoom account. |
| GET | v2/devices/groups | read | devices | Get Zoom Device Manager (ZDM) group information for an account. |
| POST | v2/devices/zpa/assignment | write | devices | Assign a device to a user or common area, or move a device to another user or common area, or remove a device. |
| GET | v2/devices/zpa/settings | read | devices | Get a user's Zoom Phone Appliance (ZPA) device profile settings. |
| POST | v2/devices/zpa/upgrade | write | devices | Upgrade ZPA firmware or app by Zoom Device Manager (ZDM) group ID. |
| DELETE | v2/devices/zpa/vendors/{id}/mac_addresses/{id} | write | devices | Remove a ZPA device from the device manager, by vendor and mac address. |
| GET | v2/devices/zpa/zdm_groups/{id}/versions | read | devices | Get ZPA firmware and app version information that can be upgraded for devices. |
| GET | v2/devices/{id} | read | devices | Retrieve a device's details. |
| PATCH | v2/devices/{id} | write | devices | Change device name. |
| DELETE | v2/devices/{id} | write | devices | Delete a device from a Zoom account. |
| PATCH | v2/devices/{id}/assign_group | write | devices | Assign a device to a new group. |
| PATCH | v2/devices/{id}/assignment | write | devices | Change a device's association from one Zoom Room to another. |
| GET | v2/h323/devices | read | devices | A H.323 or SIP device can make a video call to a Room Connector to join a Zoom cloud meeting. |
| POST | v2/h323/devices | write | devices | A H.323 or SIP device can make a video call to a Room Connector to join a Zoom cloud meeting. |
| PATCH | v2/h323/devices/{id} | write | devices | Edit information for a H.323/SIP device from your Zoom account. |
| DELETE | v2/h323/devices/{id} | write | devices | A H.323 or SIP device can make a video call to a Room Connector to join a Zoom cloud meeting. |
| GET | v2/sip_phones/phones | read | devices | List SIP phones on an account. |
| POST | v2/sip_phones/phones | write | devices | Enable a user to use a SIP phone. |
| PATCH | v2/sip_phones/phones/{id} | write | devices | Update the information of a specific SIP phone on a Zoom account. |
| DELETE | v2/sip_phones/phones/{id} | write | devices | Delete a Zoom account's SIP phone. |
| GET | v2/sip_trunk/numbers | read | devices | List all the numbers that are configured for SIP Connected Audio in a Zoom Account. |
| GET | v2/divisions | read | divisions | List divisions under an account. |
| POST | v2/divisions | write | divisions | Create a division. |
| GET | v2/divisions/{id} | read | divisions | Get a division under an account. |
| PATCH | v2/divisions/{id} | write | divisions | Update a group under your account. |
| DELETE | v2/divisions/{id} | write | divisions | Delete an entire division. |
| GET | v2/divisions/{id}/users | read | divisions | List the users of a division under your account. |
| POST | v2/divisions/{id}/users | write | divisions | Assign a division to members. |
| GET | v2/groups | read | groups | List groups under an account. |
| POST | v2/groups | write | groups | Use this API to create a group. |
| GET | v2/groups/{id} | read | groups | Get a group under an account. |
| PATCH | v2/groups/{id} | write | groups | Update a group under your account. |
| DELETE | v2/groups/{id} | write | groups | Delete an entire group. |
| GET | v2/groups/{id}/admins | read | groups | Use this API to return a list of group administrators under your account. |
| POST | v2/groups/{id}/admins | write | groups | Use this API to add administrators to a group under your account. |
| DELETE | v2/groups/{id}/admins/{id} | write | groups | Use this API to remove a group administrator in a Zoom account. |
| GET | v2/groups/{id}/channels | read | groups | Returns a list of channels for a group under your account. |
| GET | v2/groups/{id}/lock_settings | read | groups | Retrieve a group's locked settings. |
| PATCH | v2/groups/{id}/lock_settings | write | groups | Update a group's locked settings. |
| GET | v2/groups/{id}/members | read | groups | List the members of a group under your account. |
| POST | v2/groups/{id}/members | write | groups | Use this API to add users to a group in your account. |
| PATCH | v2/groups/{id}/members/{id} | write | groups | Use this API to perform either of the following tasks. |
| DELETE | v2/groups/{id}/members/{id} | write | groups | Use this API to remove a user from a group in an account. |
| GET | v2/groups/{id}/settings | read | groups | Get settings for a group. |
| PATCH | v2/groups/{id}/settings | write | groups | Update settings for a group. |
| POST | v2/groups/{id}/settings/meeting_waiting_room_branding | write | groups | Sets the meeting Waiting Room branding (logo, background image, video, welcome title/description, and layout) for the group. |
| GET | v2/groups/{id}/settings/registration | read | groups | Get webinar registration settings for a group. |
| PATCH | v2/groups/{id}/settings/registration | write | groups | Update webinar registration settings for a group.&lt;p style=&quot;background-color:FEEFB3; color:9F6000&quot;&gt. |
| POST | v2/groups/{id}/settings/virtual_backgrounds | write | groups | Use this API to upload Virtual Background files for all users in a group to use. |
| DELETE | v2/groups/{id}/settings/virtual_backgrounds | write | groups | Use this API to delete a group's Virtual Background files. |
| POST | v2/groups/{id}/settings/webinar_waiting_room_branding | write | groups | Sets the Webinar Waiting Room branding (logo, background image, video, welcome title/description, and layout) for the group. |
| GET | v2/archive_files | read | meetings | Get an account's archived meeting or webinar files. |
| GET | v2/archive_files/download_audit | read | meetings | Get an account's archived meeting or webinar file download audit logs. |
| GET | v2/archive_files/statistics | read | meetings | Get statistics about an account's archived meeting or webinar files. |
| PATCH | v2/archive_files/{id} | write | meetings | Update an archived file's auto-delete status. |
| PATCH | v2/live_meetings/{id}/chat/messages/{id} | write | meetings | Update a message in a live meeting, based on ID. |
| DELETE | v2/live_meetings/{id}/chat/messages/{id} | write | meetings | Delete a message in a live meeting, based on ID. |
| PATCH | v2/live_meetings/{id}/events | write | meetings | In-meeting controls include starting, stopping, pausing, and resuming a recording; inviting participants; updating the waiting room with a custom message; and... |
| PATCH | v2/live_meetings/{id}/rtms_app/status | write | meetings | Update the Real-Time Media Streams (RTMS) status for a specific participant in an ongoing meeting. |
| GET | v2/meetings/meeting_summaries | read | meetings | Retrieve a list of all meeting or webinar summaries available for an account. |
| GET | v2/meetings/{id} | read | meetings | Retrieve the given meeting's details. |
| PATCH | v2/meetings/{id} | write | meetings | Updates meeting details. |
| DELETE | v2/meetings/{id} | write | meetings | Delete a meeting. |
| POST | v2/meetings/{id}/batch_polls | write | meetings | Polls allow the meeting host to survey attendees. |
| POST | v2/meetings/{id}/batch_registrants | write | meetings | Register up to 30 registrants at once for a meeting that requires registration. |
| GET | v2/meetings/{id}/invitation | read | meetings | Retrieve the meeting invitation note for a specific meeting. |
| POST | v2/meetings/{id}/invite_links | write | meetings | Create a batch of invitation links for a meeting. |
| GET | v2/meetings/{id}/jointoken/live_streaming | write | meetings | Get a meeting's join token to allow live streaming. Kept out of read: it returns a token. |
| GET | v2/meetings/{id}/jointoken/local_archiving | write | meetings | Get a meeting's archive token to allow local archiving. Kept out of read: it returns a token. |
| GET | v2/meetings/{id}/jointoken/local_recording | write | meetings | Get a meeting's join token to allow for local recording. Kept out of read: it returns a token. |
| GET | v2/meetings/{id}/livestream | read | meetings | Zoom allows users to livestream a meeting to a custom platform. |
| PATCH | v2/meetings/{id}/livestream | write | meetings | Update a meeting's livestream information. |
| PATCH | v2/meetings/{id}/livestream/status | write | meetings | Zoom allows users to livestream a meeting to a custom platform. |
| GET | v2/meetings/{id}/meeting_summary | read | meetings | Retrieve the summary of a meeting or webinar. |
| DELETE | v2/meetings/{id}/meeting_summary | write | meetings | Delete the summary of a meeting or webinar. |
| POST | v2/meetings/{id}/open_apps | write | meetings | Add an auto-open app in a meeting. |
| DELETE | v2/meetings/{id}/open_apps | write | meetings | Delete a meeting auto-open app. |
| GET | v2/meetings/{id}/polls | read | meetings | Polls allow the meeting host to survey attendees. |
| POST | v2/meetings/{id}/polls | write | meetings | Polls allow the meeting host to survey attendees. |
| GET | v2/meetings/{id}/polls/{id} | read | meetings | Retrieves information about a specific meeting poll. |
| PUT | v2/meetings/{id}/polls/{id} | write | meetings | Polls allow the meeting host to survey attendees. |
| DELETE | v2/meetings/{id}/polls/{id} | write | meetings | Polls allow the meeting host to survey attendees. |
| GET | v2/meetings/{id}/registrants | read | meetings | List users that have registered for a meeting. |
| POST | v2/meetings/{id}/registrants | write | meetings | Create and submit a user's registration to a meeting. |
| GET | v2/meetings/{id}/registrants/questions | read | meetings | List registration questions that will be displayed to users while registering for a meeting. |
| PATCH | v2/meetings/{id}/registrants/questions | write | meetings | Update registration questions that will be displayed to users while registering for a meeting. |
| PUT | v2/meetings/{id}/registrants/status | write | meetings | Update a meeting registrant's status by either approving, cancelling or denying a registrant from joining the meeting. |
| GET | v2/meetings/{id}/registrants/{id} | read | meetings | Retrieve details on a specific user who has registered for the meeting. |
| DELETE | v2/meetings/{id}/registrants/{id} | write | meetings | Delete a meeting registrant. |
| POST | v2/meetings/{id}/sip_dialing | write | meetings | Get a meeting's SIP URI. |
| PUT | v2/meetings/{id}/status | write | meetings | Update the status of a meeting. |
| GET | v2/meetings/{id}/survey | read | meetings | Display information about a meeting survey. |
| PATCH | v2/meetings/{id}/survey | write | meetings | Update a meeting survey. |
| DELETE | v2/meetings/{id}/survey | write | meetings | Delete a meeting survey. |
| GET | v2/meetings/{id}/token | write | meetings | Get a meeting's closed caption token (caption URL). Kept out of read: it returns a token. |
| GET | v2/meetings/{id}/transcript | read | meetings | Return a meeting's transcript information. |
| DELETE | v2/meetings/{id}/transcript | write | meetings | Delete a transcript for a meeting or webinar. |
| GET | v2/past_meetings/{id} | read | meetings | Get information about a past meeting. |
| GET | v2/past_meetings/{id}/archive_files | read | meetings | Return a specific meeting instance's archived files. |
| DELETE | v2/past_meetings/{id}/archive_files | write | meetings | Delete all of a meeting's archived files. |
| GET | v2/past_meetings/{id}/instances | read | meetings | Return a list of past meeting instances. |
| GET | v2/past_meetings/{id}/participants | read | meetings | Retrieve participant information for a past meeting. |
| GET | v2/past_meetings/{id}/polls | read | meetings | Polls allow the meeting host to survey attendees. |
| GET | v2/past_meetings/{id}/qa | read | meetings | List Q&amp;A of a specific meeting. |
| GET | v2/metrics/ai/adoption | read | metrics | Get the AI adoption summary — active user count vs licensed user count for each AI feature across ZoomMate and AI in Workplace plans. |
| GET | v2/metrics/ai/kpis | read | metrics | Get the overall AI KPI snapshot — metrics with period-over-period change for AI feature usage across  ZoomMate and AI in Workplace plans. |
| GET | v2/metrics/ai/usage/details | read | metrics | Get AI usage and engagement details. |
| GET | v2/metrics/ai/usage/trend | read | metrics | Get the AI usage and engagement trend. |
| GET | v2/metrics/aic/roi/kpis | read | metrics | Get AIC ROI KPI data. |
| GET | v2/metrics/aic/roi/meeting_summary_usage | read | metrics | Get AIC ROI meeting summary usage data. |
| GET | v2/metrics/chat | read | metrics | Get metrics for how users are utilizing Zoom Chat to send messages. |
| GET | v2/metrics/client/feedback | read | metrics | Use this API to return Zoom meetings client feedback survey results. |
| GET | v2/metrics/client/feedback/{id} | read | metrics | Retrieve detailed information on a Zoom meetings client feedback. |
| GET | v2/metrics/client/satisfaction | read | metrics | If the End of Meeting Feedback Survey option is enabled, attendees will be prompted with a survey window where they can tap either the Thumbs Up or Thumbs Down button... |
| GET | v2/metrics/client_versions | read | metrics | Use this API to list all the client versions and its count. |
| GET | v2/metrics/crc | read | metrics | A Cloud Room Connector allows H.323/SIP endpoints to connect to a Zoom meeting. |
| GET | v2/metrics/issues/zoomrooms | read | metrics | Get information on top 25 Zoom Rooms with issues in a month. |
| GET | v2/metrics/issues/zoomrooms/{id} | read | metrics | Use this API to return information about the Zoom Rooms in an account with issues, such as disconnected hardware or bandwidth issues. |
| GET | v2/metrics/meetings | read | metrics | Lists the total live or past meetings that occurred during a specified period of time. |
| GET | v2/metrics/meetings/{id} | read | metrics | Get details on live or past meetings. |
| GET | v2/metrics/meetings/{id}/participants | read | metrics | Return a list of participants from live or past meetings. |
| GET | v2/metrics/meetings/{id}/participants/qos | read | metrics | Show a list of meeting participants from live or past meetings, and their quality of service received during the meeting. |
| GET | v2/metrics/meetings/{id}/participants/satisfaction | read | metrics | When a meeting ends, each attendee will be prompted to share their meeting experience by clicking either thumbs up or thumbs down. |
| GET | v2/metrics/meetings/{id}/participants/sharing | read | metrics | Retrieve the sharing and recording details of participants from live or past meetings. |
| GET | v2/metrics/meetings/{id}/participants/{id}/qos | read | metrics | Return the quality of service (QoS) report for participants from live or past meetings. |
| GET | v2/metrics/quality | read | metrics | Use this API to return meeting quality score information. |
| GET | v2/metrics/webinars | read | metrics | Lists all the live or past webinars from a specified period of time. |
| GET | v2/metrics/webinars/{id} | read | metrics | Retrieve details from live or past webinars. |
| GET | v2/metrics/webinars/{id}/participants | read | metrics | Get information about participants from live or past webinars. |
| GET | v2/metrics/webinars/{id}/participants/qos | read | metrics | Show a list of webinar participants from live or past webinars and the quality of service they received during the webinar. |
| GET | v2/metrics/webinars/{id}/participants/satisfaction | read | metrics | When a Webinar ends, each attendee will be prompted to share their Webinar experience by clicking either thumbs up or thumbs down. |
| GET | v2/metrics/webinars/{id}/participants/sharing | read | metrics | Retrieve the sharing and recording details of participants from live or past webinars. |
| GET | v2/metrics/webinars/{id}/participants/{id}/qos | read | metrics | Returns the quality of service (QoS) for participants during live or past webinars. |
| GET | v2/metrics/zoomrooms | read | metrics | List information on all Zoom Rooms in an account. |
| GET | v2/metrics/zoomrooms/issues | read | metrics | Get top 25 issues of Zoom Rooms. |
| GET | v2/metrics/zoomrooms/{id} | read | metrics | The Zoom Rooms dashboard metrics lets you know the type of configuration a Zoom room has and details on the meetings held in that room. |
| GET | v2/accounts/{id}/meetings/{id}/recordings | read | recordings | Returns all of a meeting's recordings. |
| DELETE | v2/accounts/{id}/meetings/{id}/recordings | write | recordings | Delete all of a meeting's or webinar's recording files. |
| GET | v2/accounts/{id}/meetings/{id}/recordings/analytics_details | read | recordings | Retrieve a meeting or webinar recording's analytics details. |
| GET | v2/accounts/{id}/meetings/{id}/recordings/analytics_summary | read | recordings | Retrieve meeting recording's analytics summary. |
| GET | v2/accounts/{id}/meetings/{id}/recordings/registrants | read | recordings | Get a list of registrants of a past meeting's on-demand cloud recordings. |
| POST | v2/accounts/{id}/meetings/{id}/recordings/registrants | write | recordings | Register a user to gain access to On-demand cloud recordings of a previous meeting. |
| GET | v2/accounts/{id}/meetings/{id}/recordings/registrants/questions | read | recordings | Retrieve a list of questions that are displayed for users to complete when registering to view the recording of a specific meeting. |
| PATCH | v2/accounts/{id}/meetings/{id}/recordings/registrants/questions | write | recordings | Update registration questions for users to answer while registering to view a recording. |
| PUT | v2/accounts/{id}/meetings/{id}/recordings/registrants/status | write | recordings | Update a registrant's status. |
| GET | v2/accounts/{id}/meetings/{id}/recordings/settings | read | recordings | Retrieve settings applied to a meeting's cloud recording. |
| PATCH | v2/accounts/{id}/meetings/{id}/recordings/settings | write | recordings | Update settings applied to a meeting's cloud recording. |
| PUT | v2/accounts/{id}/meetings/{id}/recordings/status | write | recordings | Recover all deleted cloud recordings of a specific meeting. |
| DELETE | v2/accounts/{id}/meetings/{id}/recordings/{id} | write | recordings | Delete a specific recording file from a meeting or webinar. |
| PUT | v2/accounts/{id}/meetings/{id}/recordings/{id}/status | write | recordings | Recover a single recording file from the meeting. |
| GET | v2/accounts/{id}/recordings | read | recordings | Lists the cloud recordings available on an account. |
| GET | v2/accounts/{id}/users/{id}/recordings | read | recordings | Lists all cloud recordings for a user. |
| GET | v2/meetings/{id}/recordings | read | recordings | Returns all of a meeting's recordings. |
| DELETE | v2/meetings/{id}/recordings | write | recordings | Delete all of a meeting's or webinar's recording files. |
| GET | v2/meetings/{id}/recordings/analytics_details | read | recordings | Retrieve a meeting or webinar recording's analytics details. |
| GET | v2/meetings/{id}/recordings/analytics_summary | read | recordings | Retrieve meeting recording's analytics summary. |
| GET | v2/meetings/{id}/recordings/registrants | read | recordings | Get a list of registrants of a past meeting's on-demand cloud recordings. |
| POST | v2/meetings/{id}/recordings/registrants | write | recordings | Register a user to gain access to On-demand cloud recordings of a previous meeting. |
| GET | v2/meetings/{id}/recordings/registrants/questions | read | recordings | Retrieve a list of questions that are displayed for users to complete when registering to view the recording of a specific meeting. |
| PATCH | v2/meetings/{id}/recordings/registrants/questions | write | recordings | Update registration questions for users to answer while registering to view a recording. |
| PUT | v2/meetings/{id}/recordings/registrants/status | write | recordings | Update a registrant's status. |
| GET | v2/meetings/{id}/recordings/settings | read | recordings | Retrieve settings applied to a meeting's cloud recording. |
| PATCH | v2/meetings/{id}/recordings/settings | write | recordings | Update settings applied to a meeting's cloud recording. |
| PUT | v2/meetings/{id}/recordings/status | write | recordings | Recover all deleted cloud recordings of a specific meeting. |
| DELETE | v2/meetings/{id}/recordings/{id} | write | recordings | Delete a specific recording file from a meeting or webinar. |
| PUT | v2/meetings/{id}/recordings/{id}/status | write | recordings | Recover a single recording file from the meeting. |
| GET | v2/users/{id}/recordings | read | recordings | Lists all cloud recordings for a user. |
| GET | v2/report/activities | read | report | Retrieve a list of sign in / sign out activity logs report of users under a Zoom account. |
| GET | v2/report/billing | read | report | Get department billing reports of a Zoom account. |
| GET | v2/report/billing/invoices | read | report | Get department billing invoices reports for a specific billing period. |
| GET | v2/report/cloud_recording | read | report | Retrieve cloud recording usage report for a specified period. |
| GET | v2/report/daily | read | report | Retrieve daily report to access the account-wide usage of Zoom services for each day in a given month. |
| GET | v2/report/disclaimer | read | report | Retrieve a list of disclaimer records. |
| GET | v2/report/history_meetings | read | report | Retrieve a list of history meetings and webinars. |
| GET | v2/report/meeting_activities | read | report | Retrieve a list of a meeting activity logs. |
| GET | v2/report/meetings/{id} | read | report | Get a detailed report for a past meeting. |
| GET | v2/report/meetings/{id}/participants | read | report | Return a report of a past meeting with two or more participants, including the host. |
| GET | v2/report/meetings/{id}/polls | read | report | Use this API to get a report of poll results for a past meeting. |
| GET | v2/report/meetings/{id}/qa | read | report | Retrieve a report on questions asked and answered by participants from past meetings. |
| GET | v2/report/meetings/{id}/survey | read | report | Retrieve a report on past meeting survey. |
| GET | v2/report/operationlogs | read | report | The Operations Logs report allows you to audit admin and user activity, such as adding a new user, changing account settings, and deleting recordings. |
| GET | v2/report/remote_support | read | report | Retrieve a list of remote support records. |
| GET | v2/report/telephone | read | report | The telephone report allows you to view who dialed into meetings via phone (Audio Conferencing or SIP Connected Audio) and which number they dialed into and other... |
| GET | v2/report/upcoming_events | read | report | Use this API to list upcoming meeting and/or webinar events within a specified period of time. |
| GET | v2/report/users | read | report | Retrieve a host report for a specified period of time within the last six months. |
| GET | v2/report/users/{id}/meetings | read | report | Retrieve report on past meetings and webinars for a specified time period. |
| GET | v2/report/webinars/{id} | read | report | Retrieve a report containing past webinar details. |
| GET | v2/report/webinars/{id}/participants | read | report | Get a detailed report on each webinar attendee. |
| GET | v2/report/webinars/{id}/polls | read | report | Retrieve a report on past webinar polls. |
| GET | v2/report/webinars/{id}/qa | read | report | Retrieve a report on questions asked by participants and answered by panelists, co-hosts and hosts from past webinars. |
| GET | v2/report/webinars/{id}/survey | read | report | Retrieve a report on past webinar survey. |
| GET | v2/roles | read | roles | List roles on your account. |
| POST | v2/roles | write | roles | Each Zoom user automatically has a role which can either be owner, administrator, or member. |
| GET | v2/roles/{id} | read | roles | Each Zoom user automatically has a role which can either be owner, administrator, or member. |
| PATCH | v2/roles/{id} | write | roles | Each Zoom user automatically has a role which can either be owner, administrator, or a member. |
| DELETE | v2/roles/{id} | write | roles | Each Zoom user automatically has a role which can either be owner, administrator, or a member. |
| GET | v2/roles/{id}/members | read | roles | User roles can have a set of permissions that allows access only to the pages a user needs to view or edit. |
| POST | v2/roles/{id}/members | write | roles | User roles can have a set of permissions that allows access only to the pages a user needs to view or edit. |
| DELETE | v2/roles/{id}/members/{id} | write | roles | User roles can have a set of permissions that allows access only to the pages a user needs to view or edit. |
| GET | v2/sso/capabilities | read | sso | Return the account's SSO capabilities so clients can shape requests. |
| GET | v2/sso/configurations | read | sso | List the account's full filtered SSO configuration set. |
| POST | v2/sso/configurations | write | sso | Create a SAML, InCommon, or OIDC SSO configuration. |
| GET | v2/sso/configurations/{id} | read | sso | Retrieve a single SSO configuration by ID. |
| PATCH | v2/sso/configurations/{id} | write | sso | Partially update an SSO configuration. |
| DELETE | v2/sso/configurations/{id} | write | sso | Delete a single SSO configuration (multiple-configuration accounts only). |
| GET | v2/sso/configurations/{id}/certificates | read | sso | List the account's SP certificates (CA and self-signed). |
| POST | v2/sso/configurations/{id}/certificates | write | sso | Create a self-signed SP certificate. |
| PATCH | v2/sso/configurations/{id}/certificates/{id} | write | sso | Update the self-signed SP certificate name. |
| DELETE | v2/sso/configurations/{id}/certificates/{id} | write | sso | Delete a self-signed SP certificate. |
| GET | v2/sso/configurations/{id}/mapping | read | sso | Retrieve the SAML or OIDC attribute mapping configuration of a single SSO configuration. |
| PATCH | v2/sso/configurations/{id}/mapping | write | sso | Partially update the SAML or OIDC attribute mapping configuration of a single SSO configuration. |
| PATCH | v2/sso/configurations/{id}/status | write | sso | Enable or disable a single SSO configuration (multiple-configuration accounts only). |
| GET | v2/sso/login_logs | read | sso | Returns SSO sign-in log summaries for the requesting account. |
| GET | v2/sso/login_logs/{id} | read | sso | Returns the full detail of the SSO sign-in log recorded under a specific tracking ID, including the decoded SAML response or the OIDC login documents. |
| GET | v2/sso/settings | read | sso | Return account-level SSO settings (user_provisioning). |
| PATCH | v2/sso/settings | write | sso | Update account-level SSO settings (user_provisioning). |
| GET | v2/sso/status | read | sso | Return whether account SSO is enabled. |
| PATCH | v2/sso/status | write | sso | Update the account-level SSO status. |
| GET | v2/surveys | read | surveys | Queries all surveys in the current account. |
| GET | v2/surveys/channels/{id}/instances | read | surveys | Query the channel survey instances based on channelId. |
| GET | v2/surveys/{id} | read | surveys | Queries the latest version of survey information from surveyId. |
| GET | v2/surveys/{id}/answers | read | surveys | Queries the answers of survey from surveyId. |
| GET | v2/surveys/{id}/instances | read | surveys | Query the instances which used the survey, based on surveyId. |
| GET | v2/tracking_fields | read | tracking_fields | List all the tracking fields on your Zoom account. |
| POST | v2/tracking_fields | write | tracking_fields | Use this API to create a new tracking field. |
| GET | v2/tracking_fields/{id} | read | tracking_fields | Use this API to return information about a tracking field. |
| PATCH | v2/tracking_fields/{id} | write | tracking_fields | Update a tracking field. |
| DELETE | v2/tracking_fields/{id} | write | tracking_fields | Delete a tracking field. |
| GET | v2/tsp | read | tsp | Get information on Telephony Service Provider (TSP) on an account level. |
| PATCH | v2/tsp | write | tsp | Update information of the Telephony Service Provider (TSP) set up on an account. |
| GET | v2/users | read | users | Retrieve a list of your account's users. |
| POST | v2/users | write | users | Add a new user to your Zoom account. |
| GET | v2/users/email | read | users | Verify if a user's email is registered with Zoom. |
| POST | v2/users/features | write | users | Update multiple features for a user. |
| GET | v2/users/me/zak | write | users | Get the Zoom Access Key (ZAK) for the authenticated user associated with the access token in the API request. Kept out of read: it returns a token. |
| GET | v2/users/summary | read | users | Gets a summary of users, including the number and types of users in the account. |
| GET | v2/users/vanity_name | read | users | A personal meeting room is a virtual meeting room that can be permanently assigned to a user. |
| GET | v2/users/{id} | read | users | View a user's account information. |
| PATCH | v2/users/{id} | write | users | Updates a user's Zoom profile information. |
| DELETE | v2/users/{id} | write | users | Disassociate (unlink) a user or permanently delete a user. |
| GET | v2/users/{id}/assistants | read | users | List a user's assistants. |
| POST | v2/users/{id}/assistants | write | users | Assign assistants to a user. |
| DELETE | v2/users/{id}/assistants | write | users | Delete all of the current user's assistants. |
| DELETE | v2/users/{id}/assistants/{id} | write | users | Delete a specific assistant of a user. |
| GET | v2/users/{id}/collaboration_devices | read | users | List a user's collaboration devices. |
| GET | v2/users/{id}/collaboration_devices/{id} | read | users | Get collaboration device detail. |
| PUT | v2/users/{id}/email | write | users | Change a user's email address on a Zoom account that has managed domain set up. |
| GET | v2/users/{id}/meeting_summaries | read | users | Retrieve a list of meeting or webinar summaries hosted by the specified user. |
| GET | v2/users/{id}/meeting_summary_templates | read | users | List meeting summary templates. |
| GET | v2/users/{id}/meeting_templates | read | users | List available meeting templates for a user. |
| POST | v2/users/{id}/meeting_templates | write | users | Create a meeting template from an existing meeting. |
| GET | v2/users/{id}/meeting_templates/{id} | read | users | Retrieve a user's meeting template. |
| GET | v2/users/{id}/meetings | read | users | List a meeting host user's scheduled meetings. |
| POST | v2/users/{id}/meetings | write | users | Creates a meeting for a user. |
| GET | v2/users/{id}/pac | read | users | Retrieve a list of a user's personal audio conference (PAC) accounts. |
| PUT | v2/users/{id}/password | write | users | Update the password of a user using which the user can login to Zoom. |
| GET | v2/users/{id}/permissions | read | users | Get permissions that have been granted to the user. |
| POST | v2/users/{id}/picture | write | users | Upload a user's profile picture. |
| DELETE | v2/users/{id}/picture | write | users | Delete a user's profile picture. |
| GET | v2/users/{id}/presence_status | read | users | Returns a user's current status. |
| PUT | v2/users/{id}/presence_status | write | users | Update a user's presence status. |
| GET | v2/users/{id}/schedulers | read | users | List all of a user's schedulers. |
| DELETE | v2/users/{id}/schedulers | write | users | Delete all of a user's schedulers. |
| DELETE | v2/users/{id}/schedulers/{id} | write | users | Delete a scheduler. |
| GET | v2/users/{id}/settings | read | users | Retrieve a user's settings. |
| PATCH | v2/users/{id}/settings | write | users | Update a user's settings. |
| POST | v2/users/{id}/settings/meeting_waiting_room_branding | write | users | Sets Meeting Waiting Room branding (logo, background image, video, welcome title/description, and layout) for the user. |
| GET | v2/users/{id}/settings/sensitive_label | read | users | Get user sensitive label settings. |
| POST | v2/users/{id}/settings/virtual_backgrounds | write | users | Use this API to upload a Virtual Background files to a user's profile. |
| DELETE | v2/users/{id}/settings/virtual_backgrounds | write | users | Use this API to delete a user's Virtual Background files. |
| POST | v2/users/{id}/settings/webinar_waiting_room_branding | write | users | Sets the webinar Waiting Room branding (logo, background image, video, welcome title/description, and layout) for the user. |
| PUT | v2/users/{id}/status | write | users | Deactivate an active user or to reactivate a deactivated user. |
| GET | v2/users/{id}/token | write | users | Gets a user's Zoom token or Zoom Access Key (ZAK). Kept out of read: it returns a token. |
| DELETE | v2/users/{id}/token | write | users | Revokes a user's SSO token. |
| GET | v2/users/{id}/tsp | read | users | List all of a user's TSP accounts. |
| POST | v2/users/{id}/tsp | write | users | Add a user's TSP account. |
| PATCH | v2/users/{id}/tsp/settings | write | users | Set the URL for a global dial-in page of a user whose Zoom account has TSP and special TSP with third-party audio conferencing options enabled. |
| GET | v2/users/{id}/tsp/{id} | read | users | Retrieve details of a specific TSP account enabled for a specific user. |
| PATCH | v2/users/{id}/tsp/{id} | write | users | Update a user's Telephony Service Provider (TSP) account. |
| DELETE | v2/users/{id}/tsp/{id} | write | users | Delete a user's TSP account. |
| GET | v2/users/{id}/upcoming_meetings | read | users | List a Zoom user's upcoming meetings. |
| GET | v2/users/{id}/webinar_templates | read | users | Display a list of a user's webinar templates. |
| POST | v2/users/{id}/webinar_templates | write | users | Create a webinar template from an existing webinar. |
| GET | v2/users/{id}/webinars | read | users | List all the webinars scheduled by or on behalf a webinar host. |
| POST | v2/users/{id}/webinars | write | users | Schedule a webinar for a user who is a webinar host. |
| DELETE | v2/live_webinars/{id}/chat/messages/{id} | write | webinars | Deletes a message in a live webinar based on ID. |
| GET | v2/past_webinars/{id}/absentees | read | webinars | List absentees of a webinar. |
| GET | v2/past_webinars/{id}/instances | read | webinars | List past webinar instances. |
| GET | v2/past_webinars/{id}/participants | read | webinars | Retrieve a list of all the participants who attended a webinar hosted in the past. |
| GET | v2/past_webinars/{id}/polls | read | webinars | The polling feature for webinar lets you create single-choice or multiple-choice polling questions for your webinars. |
| GET | v2/past_webinars/{id}/qa | read | webinars | List the Q&amp;A of a specific past webinar. |
| GET | v2/webinars/{id} | read | webinars | Get details for a scheduled Zoom webinar. |
| PATCH | v2/webinars/{id} | write | webinars | Make updates to a scheduled webinar. |
| DELETE | v2/webinars/{id} | write | webinars | Delete a webinar. |
| POST | v2/webinars/{id}/batch_registrants | write | webinars | Register up to 30 registrants at once for a scheduled webinar that requires registration. |
| GET | v2/webinars/{id}/branding | read | webinars | Get the webinar's session branding information. |
| POST | v2/webinars/{id}/branding/name_tags | write | webinars | Create a webinar's session branding name tag. |
| DELETE | v2/webinars/{id}/branding/name_tags | write | webinars | Delete a webinar's session branding name tag. |
| PATCH | v2/webinars/{id}/branding/name_tags/{id} | write | webinars | Update a webinar's session branding name tag. |
| POST | v2/webinars/{id}/branding/virtual_backgrounds | write | webinars | Upload a webinar's session branding virtual background. |
| PATCH | v2/webinars/{id}/branding/virtual_backgrounds | write | webinars | Set a webinar's default session branding virtual background. |
| DELETE | v2/webinars/{id}/branding/virtual_backgrounds | write | webinars | Delete a webinar's session branding virtual background. |
| POST | v2/webinars/{id}/branding/wallpaper | write | webinars | Upload a webinar's session branding wallpaper file. |
| DELETE | v2/webinars/{id}/branding/wallpaper | write | webinars | Delete a webinar's session branding wallpaper file. |
| POST | v2/webinars/{id}/invite_links | write | webinars | Create a batch of invitation links for a webinar. |
| GET | v2/webinars/{id}/jointoken/live_streaming | write | webinars | Retrieve a webinar's archive token to allow live streaming. Kept out of read: it returns a token. |
| GET | v2/webinars/{id}/jointoken/local_archiving | write | webinars | Use this API to get a webinar's archive token to allow local archiving. Kept out of read: it returns a token. |
| GET | v2/webinars/{id}/jointoken/local_recording | write | webinars | Retrieve a webinar's join token to allow for local recording. Kept out of read: it returns a token. |
| GET | v2/webinars/{id}/livestream | read | webinars | Get a webinar's live stream configuration details, such as Stream URL, Stream Key and Page URL. |
| PATCH | v2/webinars/{id}/livestream | write | webinars | Update a webinar's live stream information. |
| PATCH | v2/webinars/{id}/livestream/status | write | webinars | Lets users live stream a webinar to a custom platform. |
| GET | v2/webinars/{id}/panelists | read | webinars | List all of a webinar's panelists. |
| POST | v2/webinars/{id}/panelists | write | webinars | Panelists in a webinar can view and send video, screen share, annotate, and do much more compared to attendees in a webinar. |
| DELETE | v2/webinars/{id}/panelists | write | webinars | Remove all the panelists from a webinar. |
| DELETE | v2/webinars/{id}/panelists/{id} | write | webinars | Remove a single panelist from a webinar. |
| GET | v2/webinars/{id}/polls | read | webinars | Lists all the polls of a webinar. |
| POST | v2/webinars/{id}/polls | write | webinars | Creates a poll for a webinar. |
| GET | v2/webinars/{id}/polls/{id} | read | webinars | Returns a webinar's poll details. |
| PUT | v2/webinars/{id}/polls/{id} | write | webinars | Updates a webinar's poll. |
| DELETE | v2/webinars/{id}/polls/{id} | write | webinars | Delete a webinar's poll. |
| GET | v2/webinars/{id}/registrants | read | webinars | List all users that have registered for a given webinar. |
| POST | v2/webinars/{id}/registrants | write | webinars | Create and submit a user's registration for a webinar. |
| GET | v2/webinars/{id}/registrants/questions | read | webinars | List registration questions and fields that are to be answered by users while registering for a webinar. |
| PATCH | v2/webinars/{id}/registrants/questions | write | webinars | Update registration questions and fields of a scheduled webinar for users to answer during webinar registration. |
| PUT | v2/webinars/{id}/registrants/status | write | webinars | Update webinar registrants' registration status. |
| GET | v2/webinars/{id}/registrants/{id} | read | webinars | Zoom users with a webinar plan have access to creating and managing webinars. |
| DELETE | v2/webinars/{id}/registrants/{id} | write | webinars | Delete a webinar registrant. |
| POST | v2/webinars/{id}/sip_dialing | write | webinars | Get a webinar's SIP URI. |
| PUT | v2/webinars/{id}/status | write | webinars | Update a webinar's status. |
| GET | v2/webinars/{id}/survey | read | webinars | Return information about a webinar survey. |
| PATCH | v2/webinars/{id}/survey | write | webinars | Update a webinar survey. |
| DELETE | v2/webinars/{id}/survey | write | webinars | Delete a webinar survey. |
| GET | v2/webinars/{id}/token | write | webinars | Use this API to get a webinar's closed caption token (caption URL). Kept out of read: it returns a token. |
| GET | v2/webinars/{id}/tracking_sources | read | webinars | Webinar Registration Tracking Sources allow you to see where your registrants are coming from if you share the webinar registration page in multiple platforms. |
