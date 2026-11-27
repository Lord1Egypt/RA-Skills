# Zoho CRM access policy

An access policy limits which endpoints Zoho CRM connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/zoho-crm#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Zoho CRM: its 169 read-only endpoints, plus deny rules for the 1 write endpoint a read rule would otherwise match. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create zoho-crm --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "crm/v8/__apis"},
    {"method": "GET", "path": "crm/v8/settings/appointment_preferences"},
    {"method": "GET", "path": "crm/v8/settings/automation/assignment_rules"},
    {"method": "GET", "path": "crm/v8/settings/automation/assignment_rules/{id}"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/Attachments"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/Attachments/{id}"},
    {"method": "GET", "path": "crm/v8/settings/audit_log_export"},
    {"method": "GET", "path": "crm/v8/settings/audit_log_export/{id}"},
    {"method": "GET", "path": "crm/v8/org/currencies/actions/available_currencies"},
    {"method": "GET", "path": "crm/bulk/v8/backup"},
    {"method": "GET", "path": "crm/bulk/v8/backup/history"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/actions/blueprint"},
    {"method": "GET", "path": "crm/bulk/v8/read/{id}"},
    {"method": "GET", "path": "crm/bulk/v8/read/{id}/result"},
    {"method": "GET", "path": "crm/bulk/v8/write/{id}"},
    {"method": "GET", "path": "crm/v8/settings/business_hours"},
    {"method": "GET", "path": "crm/v8/settings/automation/cadences"},
    {"method": "GET", "path": "crm/v8/settings/call_preferences"},
    {"method": "GET", "path": "crm/v8/Contacts/roles"},
    {"method": "GET", "path": "crm/v8/Contacts/roles/{id}"},
    {"method": "GET", "path": "crm/v8/Leads/{id}/__conversion_options"},
    {"method": "POST", "path": "crm/v8/coql"},
    {"method": "GET", "path": "crm/v8/org/currencies"},
    {"method": "GET", "path": "crm/v8/org/currencies/{id}"},
    {"method": "GET", "path": "crm/v8/settings/custom_views"},
    {"method": "GET", "path": "crm/v8/settings/custom_views/{id}"},
    {"method": "GET", "path": "crm/v8/settings/data_sharing"},
    {"method": "GET", "path": "crm/v8/Deals/{id}/Contact_Roles"},
    {"method": "GET", "path": "crm/v8/Deals/{id}/Contact_Roles/{id}"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/Emails/actions/download_attachments"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/Emails/actions/download_inline_images"},
    {"method": "GET", "path": "crm/v8/settings/duplicate_check_preference"},
    {"method": "GET", "path": "crm/email/v8/settings/compose"},
    {"method": "GET", "path": "crm/email/v8/settings/compose/configuration_options"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/Emails"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/Emails/{id}"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/__emails_sharing_details"},
    {"method": "GET", "path": "crm/email/v8/settings/compose/email_signatures"},
    {"method": "GET", "path": "crm/email/v8/settings/compose/email_signatures/{id}"},
    {"method": "GET", "path": "crm/v8/settings/email_templates"},
    {"method": "GET", "path": "crm/v8/settings/email_templates/{id}"},
    {"method": "GET", "path": "crm/v8/Entity_Scores__s"},
    {"method": "GET", "path": "crm/v8/Entity_Scores__s/{id}"},
    {"method": "GET", "path": "crm/v8/__features"},
    {"method": "GET", "path": "crm/v8/__features/data_enrichment"},
    {"method": "GET", "path": "crm/v8/__features/user_licenses"},
    {"method": "GET", "path": "crm/v8/__features/{id}"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/actions/download_fields_attachment"},
    {"method": "GET", "path": "crm/v8/settings/layouts/{id}/map_dependency"},
    {"method": "GET", "path": "crm/v8/settings/layouts/{id}/map_dependency/{id}"},
    {"method": "GET", "path": "crm/v8/settings/fields"},
    {"method": "GET", "path": "crm/v8/settings/fields/{id}"},
    {"method": "GET", "path": "crm/v8/files"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/actions/merge"},
    {"method": "GET", "path": "crm/v8/settings/fiscal_year"},
    {"method": "GET", "path": "crm/v8/settings/emails/actions/from_addresses"},
    {"method": "POST", "path": "crm/v8/{id}/{id}/actions/get_related_records_count"},
    {"method": "GET", "path": "crm/v8/settings/global_picklists"},
    {"method": "GET", "path": "crm/v8/settings/global_picklists/{id}"},
    {"method": "GET", "path": "crm/v8/settings/global_picklists/{id}/actions/associations"},
    {"method": "GET", "path": "crm/v8/settings/global_picklists/{id}/actions/pick_list_values_associations"},
    {"method": "GET", "path": "crm/v8/settings/global_picklists/{id}/actions/replaced_values"},
    {"method": "GET", "path": "crm/v8/settings/holidays"},
    {"method": "GET", "path": "crm/v8/settings/holidays/{id}"},
    {"method": "GET", "path": "crm/v8/{id}/actions/mass_convert"},
    {"method": "GET", "path": "crm/v8/settings/inventory_templates"},
    {"method": "GET", "path": "crm/v8/settings/inventory_templates/{id}"},
    {"method": "GET", "path": "crm/v8/settings/layouts"},
    {"method": "GET", "path": "crm/v8/settings/layouts/{id}"},
    {"method": "GET", "path": "crm/v8/{id}/actions/mass_change_owner"},
    {"method": "GET", "path": "crm/v8/Leads/actions/mass_convert"},
    {"method": "GET", "path": "crm/v8/{id}/actions/mass_delete"},
    {"method": "GET", "path": "crm/v8/settings/tags/actions/mass_delete"},
    {"method": "GET", "path": "crm/v8/settings/modules"},
    {"method": "GET", "path": "crm/v8/settings/modules/{id}"},
    {"method": "GET", "path": "crm/v8/Notes"},
    {"method": "GET", "path": "crm/v8/Notes/{id}"},
    {"method": "GET", "path": "crm/v8/actions/watch"},
    {"method": "GET", "path": "crm/v8/org"},
    {"method": "GET", "path": "crm/v8/org/photo"},
    {"method": "GET", "path": "crm/v8/settings/fields/{id}/pick_list_values"},
    {"method": "GET", "path": "crm/v8/settings/pipeline"},
    {"method": "GET", "path": "crm/v8/settings/pipeline/{id}"},
    {"method": "GET", "path": "crm/v8/settings/portals/{id}/user_type"},
    {"method": "GET", "path": "crm/v8/settings/portals/{id}/user_type/{id}"},
    {"method": "GET", "path": "crm/v8/settings/portals"},
    {"method": "GET", "path": "crm/v8/settings/portals/{id}"},
    {"method": "GET", "path": "crm/v8/settings/profiles"},
    {"method": "GET", "path": "crm/v8/settings/profiles/{id}"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/Locking_Information__s"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/Locking_Information__s/{id}"},
    {"method": "GET", "path": "crm/v8/settings/record_locking_configurations"},
    {"method": "GET", "path": "crm/v8/{id}"},
    {"method": "GET", "path": "crm/v8/{id}/actions/count"},
    {"method": "GET", "path": "crm/v8/{id}/actions/fetch_full_data"},
    {"method": "GET", "path": "crm/v8/{id}/actions/mass_update"},
    {"method": "GET", "path": "crm/v8/{id}/deleted"},
    {"method": "GET", "path": "crm/v8/{id}/search"},
    {"method": "GET", "path": "crm/v8/{id}/{id}"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/actions/fetch_full_data"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/photo"},
    {"method": "GET", "path": "crm/v8/settings/recycle_bin"},
    {"method": "GET", "path": "crm/v8/settings/recycle_bin/{id}"},
    {"method": "GET", "path": "crm/v8/settings/related_lists"},
    {"method": "GET", "path": "crm/v8/settings/related_lists/{id}"},
    {"method": "GET", "path": "crm/v8/{id}/deleted/{id}/{id}"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/{id}"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/{id}/{id}"},
    {"method": "GET", "path": "crm/v8/Appointments_Rescheduled_History__s"},
    {"method": "GET", "path": "crm/v8/Appointments_Rescheduled_History__s/{id}"},
    {"method": "GET", "path": "crm/v8/settings/roles"},
    {"method": "GET", "path": "crm/v8/settings/roles/{id}"},
    {"method": "GET", "path": "crm/v8/settings/automation/scoring_rules"},
    {"method": "GET", "path": "crm/v8/settings/automation/scoring_rules/{id}"},
    {"method": "GET", "path": "crm/v8/settings/service_preferences"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/actions/share"},
    {"method": "GET", "path": "crm/v8/settings/data_sharing/rules"},
    {"method": "GET", "path": "crm/v8/settings/data_sharing/rules/actions/summary"},
    {"method": "POST", "path": "crm/v8/settings/data_sharing/rules/actions/summary"},
    {"method": "POST", "path": "crm/v8/settings/data_sharing/rules/search"},
    {"method": "GET", "path": "crm/v8/settings/data_sharing/rules/{id}"},
    {"method": "GET", "path": "crm/v8/settings/business_hours/shift_hours"},
    {"method": "GET", "path": "crm/v8/settings/business_hours/shift_hours/{id}"},
    {"method": "GET", "path": "crm/v8/settings/signals"},
    {"method": "GET", "path": "crm/v8/settings/tags"},
    {"method": "GET", "path": "crm/v8/settings/tags/{id}/actions/records_count"},
    {"method": "GET", "path": "crm/v8/org/taxes"},
    {"method": "GET", "path": "crm/v8/org/taxes/{id}"},
    {"method": "GET", "path": "crm/v8/settings/territories"},
    {"method": "GET", "path": "crm/v8/settings/territories/actions/associated_users_count"},
    {"method": "GET", "path": "crm/v8/settings/territories/{id}"},
    {"method": "GET", "path": "crm/v8/settings/territories/{id}/__child_territories"},
    {"method": "GET", "path": "crm/v8/settings/territories/{id}/users"},
    {"method": "GET", "path": "crm/v8/settings/territories/{id}/users/{id}"},
    {"method": "GET", "path": "crm/v8/{id}/{id}/__timeline"},
    {"method": "GET", "path": "crm/v8/settings/unsubscribe_link/actions/associations"},
    {"method": "GET", "path": "crm/v8/settings/unsubscribe_links"},
    {"method": "GET", "path": "crm/v8/settings/unsubscribe_links/{id}"},
    {"method": "GET", "path": "crm/v8/settings/user_groups"},
    {"method": "GET", "path": "crm/v8/settings/user_groups/actions/associated_users_count"},
    {"method": "GET", "path": "crm/v8/settings/user_groups/{id}"},
    {"method": "GET", "path": "crm/v8/settings/user_groups/{id}/actions/associations"},
    {"method": "GET", "path": "crm/v8/settings/user_groups/{id}/actions/sources_count"},
    {"method": "GET", "path": "crm/v8/settings/user_groups/{id}/associated_users/actions/grouped_counts"},
    {"method": "GET", "path": "crm/v8/settings/user_groups/{id}/sources"},
    {"method": "GET", "path": "crm/v8/users/{id}/actions/associated_groups"},
    {"method": "GET", "path": "crm/v8/settings/portals/{id}/user_type/{id}/users"},
    {"method": "GET", "path": "crm/v8/users"},
    {"method": "GET", "path": "crm/v8/users/actions/count"},
    {"method": "GET", "path": "crm/v8/users/{id}"},
    {"method": "GET", "path": "crm/v8/users/{id}/territories"},
    {"method": "GET", "path": "crm/v8/users/{id}/territories/{id}"},
    {"method": "GET", "path": "crm/v8/users/actions/transfer_and_delete"},
    {"method": "GET", "path": "crm/v8/settings/users_unavailability"},
    {"method": "GET", "path": "crm/v8/settings/users_unavailability/{id}"},
    {"method": "GET", "path": "crm/v8/settings/variable_groups"},
    {"method": "GET", "path": "crm/v8/settings/variable_groups/{id}"},
    {"method": "GET", "path": "crm/v8/settings/variables"},
    {"method": "GET", "path": "crm/v8/settings/variables/{id}"},
    {"method": "GET", "path": "crm/v8/settings/webforms"},
    {"method": "GET", "path": "crm/v8/settings/webforms/{id}"},
    {"method": "GET", "path": "crm/v8/settings/webforms/{id}/actions/preview"},
    {"method": "GET", "path": "crm/v8/settings/wizards"},
    {"method": "GET", "path": "crm/v8/settings/wizards/{id}"},
    {"method": "GET", "path": "crm/v8/settings/zia/data_enrichment"},
    {"method": "GET", "path": "crm/v8/__zia_org_enrichment"},
    {"method": "GET", "path": "crm/v8/__zia_org_enrichment/{id}"},
    {"method": "GET", "path": "crm/v8/__zia_people_enrichment"},
    {"method": "GET", "path": "crm/v8/__zia_people_enrichment/{id}"}
  ],
  "deny": [
    {"method": "GET", "path": "crm/v8/functions/{id}/actions/execute"}
  ]
}
```

## Endpoints

The Zoho CRM endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | crm/v8/__apis | read | apis | Get supported api. |
| GET | crm/v8/settings/appointment_preferences | read | appointment-preference | Get appointment preference. |
| PUT | crm/v8/settings/appointment_preferences | write | appointment-preference | Update appointment preference. |
| GET | crm/v8/settings/automation/assignment_rules | read | assignment-rules | Get assignment rules. |
| GET | crm/v8/settings/automation/assignment_rules/{id} | read | assignment-rules | Get assignment rule. |
| POST | crm/v8/{id}/{id}/actions/associate_email | write | associate-email | Associate. |
| GET | crm/v8/{id}/{id}/Attachments | read | attachments | Get attachments. |
| POST | crm/v8/{id}/{id}/Attachments | write | attachments | Upload attachments. |
| DELETE | crm/v8/{id}/{id}/Attachments | write | attachments | Delete attachments. |
| GET | crm/v8/{id}/{id}/Attachments/{id} | read | attachments | Get attachment. |
| DELETE | crm/v8/{id}/{id}/Attachments/{id} | write | attachments | Delete attachment. |
| GET | crm/v8/settings/audit_log_export | read | audit-log-export | Get exported auditlogs. |
| POST | crm/v8/settings/audit_log_export | write | audit-log-export | Create auditlog export. |
| GET | crm/v8/settings/audit_log_export/{id} | read | audit-log-export | Get exported auditlog. |
| GET | crm/v8/org/currencies/actions/available_currencies | read | available-currencies | Get available currencies. |
| GET | crm/bulk/v8/backup | read | backup | Get details. |
| POST | crm/bulk/v8/backup | write | backup | Schedule. |
| GET | crm/bulk/v8/backup/history | read | backup | History. |
| GET | crm/bulk/v8/backup/urls | write | backup | Get urls. Kept out of read: returns signed download links to data backups. |
| PUT | crm/bulk/v8/backup/{id}/actions/cancel | write | backup | Cancel. |
| GET | crm/v8/{id}/{id}/actions/blueprint | read | blueprint | Get blueprint. |
| PUT | crm/v8/{id}/{id}/actions/blueprint | write | blueprint | Update blueprint. |
| POST | crm/bulk/v8/read | write | bulk-read | Create bulk read job. Kept out of read: creates a bulk export job. |
| GET | crm/bulk/v8/read/{id} | read | bulk-read | Get bulk read job details. |
| GET | crm/bulk/v8/read/{id}/result | read | bulk-read | Download result. |
| POST | crm/bulk/v8/write | write | bulk-write | Create bulk write job. |
| GET | crm/bulk/v8/write/{id} | read | bulk-write | Get bulk write job details. |
| GET | crm/v8/settings/business_hours | read | business-hours | Get business hours. |
| POST | crm/v8/settings/business_hours | write | business-hours | Create business hours. |
| PUT | crm/v8/settings/business_hours | write | business-hours | Update business hours. |
| GET | crm/v8/settings/automation/cadences | read | cadences | Get cadences. |
| POST | crm/v8/{id}/actions/enrol_in_cadences | write | cadences-execution | Enroll cadences. |
| POST | crm/v8/{id}/actions/unenrol_from_cadences | write | cadences-execution | Unenroll cadences. |
| GET | crm/v8/settings/call_preferences | read | call-preferences | Get call preference. |
| PUT | crm/v8/settings/call_preferences | write | call-preferences | Update call preference. |
| POST | crm/v8/Events/{id}/actions/cancel | write | cancel-meetings | Cancel meetings. |
| POST | crm/v8/{id}/actions/change_owner | write | change-owner | Change the owner of multiple records. |
| POST | crm/v8/{id}/{id}/actions/change_owner | write | change-owner | Change the owner of a record. |
| GET | crm/v8/Contacts/roles | read | contact-roles | Get roles. |
| POST | crm/v8/Contacts/roles | write | contact-roles | Create roles. |
| PUT | crm/v8/Contacts/roles | write | contact-roles | Update roles. |
| DELETE | crm/v8/Contacts/roles | write | contact-roles | Delete contact roles. |
| GET | crm/v8/Contacts/roles/{id} | read | contact-roles | Get role. |
| PUT | crm/v8/Contacts/roles/{id} | write | contact-roles | Update contact role. |
| DELETE | crm/v8/Contacts/roles/{id} | write | contact-roles | Delete contact role. |
| GET | crm/v8/Leads/{id}/__conversion_options | read | conversion-option | Lead conversion options. |
| POST | crm/v8/Leads/{id}/actions/convert | write | convert-lead | Convert lead. |
| POST | crm/v8/coql | read | coql | Query records with a COQL SELECT statement. |
| GET | crm/v8/org/currencies | read | currencies | Get currencies. |
| POST | crm/v8/org/currencies | write | currencies | Add currencies. |
| PUT | crm/v8/org/currencies | write | currencies | Update currencies. |
| POST | crm/v8/org/currencies/actions/enable | write | currencies | Enable base currency. |
| PUT | crm/v8/org/currencies/actions/enable | write | currencies | Update base currency. |
| GET | crm/v8/org/currencies/{id} | read | currencies | Get currency. |
| PUT | crm/v8/org/currencies/{id} | write | currencies | Update currency. |
| GET | crm/v8/settings/custom_views | read | custom-views | Get custom views. |
| PUT | crm/v8/settings/custom_views/actions/change_sort | write | custom-views | Change sort order of custom views. |
| GET | crm/v8/settings/custom_views/{id} | read | custom-views | Get custom view. |
| PUT | crm/v8/settings/custom_views/{id}/actions/change_sort | write | custom-views | Change sort order of custom view. |
| GET | crm/v8/settings/data_sharing | read | data-sharing | Get data sharing. |
| PUT | crm/v8/settings/data_sharing | write | data-sharing | Update data sharing. |
| GET | crm/v8/Deals/{id}/Contact_Roles | read | deal-contact-roles | Get associated contact roles. |
| DELETE | crm/v8/Deals/{id}/Contact_Roles | write | deal-contact-roles | Delete associated contact roles. |
| GET | crm/v8/Deals/{id}/Contact_Roles/{id} | read | deal-contact-roles | Get associated contact roles specific to contact. |
| PUT | crm/v8/Deals/{id}/Contact_Roles/{id} | write | deal-contact-roles | Associate contact role to deal. |
| DELETE | crm/v8/Deals/{id}/Contact_Roles/{id} | write | deal-contact-roles | Delete contact role relation. |
| POST | crm/v8/__digest | write | digest | Create digest. |
| GET | crm/v8/{id}/{id}/Emails/actions/download_attachments | read | download-attachments | Get download attachments details. |
| GET | crm/v8/{id}/{id}/Emails/actions/download_inline_images | read | download-inline-images | Get download inline images. |
| GET | crm/v8/settings/duplicate_check_preference | read | duplicate-check-preference | Get duplicate check preference. |
| POST | crm/v8/settings/duplicate_check_preference | write | duplicate-check-preference | Create duplicate check preference. |
| PUT | crm/v8/settings/duplicate_check_preference | write | duplicate-check-preference | Update duplicate check preference. |
| DELETE | crm/v8/settings/duplicate_check_preference | write | duplicate-check-preference | Delete duplicate check preference. |
| GET | crm/email/v8/settings/compose | read | email-compose | Get email composer default settings. |
| PUT | crm/email/v8/settings/compose | write | email-compose | Update email composer default settings. |
| GET | crm/email/v8/settings/compose/configuration_options | read | email-configuration-options | Get email configuration options. |
| PUT | crm/email/v8/settings/compose/configuration_options | write | email-configuration-options | Update email configuration options. |
| GET | crm/v8/{id}/{id}/Emails | read | email-related-records | Get emails related records. |
| GET | crm/v8/{id}/{id}/Emails/{id} | read | email-related-records | Get emails related record. |
| GET | crm/v8/{id}/{id}/__emails_sharing_details | read | email-sharing-details | Get email sharing details. |
| GET | crm/email/v8/settings/compose/email_signatures | read | email-signatures | Get all email signatures. |
| POST | crm/email/v8/settings/compose/email_signatures | write | email-signatures | Create email signatures. |
| PUT | crm/email/v8/settings/compose/email_signatures | write | email-signatures | Update email signatures. |
| DELETE | crm/email/v8/settings/compose/email_signatures | write | email-signatures | Delete email signatures. |
| GET | crm/email/v8/settings/compose/email_signatures/{id} | read | email-signatures | Get email signature. |
| PUT | crm/email/v8/settings/compose/email_signatures/{id} | write | email-signatures | Update email signature. |
| DELETE | crm/email/v8/settings/compose/email_signatures/{id} | write | email-signatures | Delete email signature. |
| GET | crm/v8/settings/email_templates | read | email-templates | Get email templates. |
| GET | crm/v8/settings/email_templates/{id} | read | email-templates | Get email template. |
| GET | crm/v8/Entity_Scores__s | read | entity-scores | Get entity scores. |
| GET | crm/v8/Entity_Scores__s/{id} | read | entity-scores | Get entity score. |
| GET | crm/v8/__features | read | features | Get feature details. |
| GET | crm/v8/__features/data_enrichment | read | features | Get data enrichment. |
| GET | crm/v8/__features/user_licenses | read | features | Get user licences count. |
| GET | crm/v8/__features/{id} | read | features | Get feature detail. |
| GET | crm/v8/{id}/{id}/actions/download_fields_attachment | read | field-attachments | Get field attachments. |
| GET | crm/v8/settings/layouts/{id}/map_dependency | read | field-map-dependency | Get map dependencies. |
| POST | crm/v8/settings/layouts/{id}/map_dependency | write | field-map-dependency | Create map dependency. |
| GET | crm/v8/settings/layouts/{id}/map_dependency/{id} | read | field-map-dependency | Get map dependency. |
| PUT | crm/v8/settings/layouts/{id}/map_dependency/{id} | write | field-map-dependency | Update map dependency. |
| DELETE | crm/v8/settings/layouts/{id}/map_dependency/{id} | write | field-map-dependency | Delete map dependency. |
| GET | crm/v8/settings/fields | read | fields | Get fields. |
| POST | crm/v8/settings/fields | write | fields | Create field. |
| PATCH | crm/v8/settings/fields | write | fields | Update fields. |
| GET | crm/v8/settings/fields/{id} | read | fields | Get field. |
| PATCH | crm/v8/settings/fields/{id} | write | fields | Update field. |
| DELETE | crm/v8/settings/fields/{id} | write | fields | Delete field. |
| GET | crm/v8/files | read | files | Get file. |
| POST | crm/v8/files | write | files | Upload files. |
| GET | crm/v8/{id}/{id}/actions/merge | read | find-and-merge | Get record merge. |
| POST | crm/v8/{id}/{id}/actions/merge | write | find-and-merge | Merge records. |
| GET | crm/v8/settings/fiscal_year | read | fiscal-year | Get fiscal year. |
| PUT | crm/v8/settings/fiscal_year | write | fiscal-year | Update fiscal year. |
| GET | crm/v8/settings/emails/actions/from_addresses | read | from-addresses | Get from addresses. |
| GET | crm/v8/functions/{id}/actions/execute | write | functions | Execute function using parameters. Kept out of read: executes a Deluge function. |
| POST | crm/v8/functions/{id}/actions/execute | write | functions | Execute function using request body. |
| POST | crm/v8/{id}/{id}/actions/get_related_records_count | read | get-related-records-count | Get related records count. |
| GET | crm/v8/settings/global_picklists | read | global-picklists | Get global picklists. |
| POST | crm/v8/settings/global_picklists | write | global-picklists | Create global picklist. |
| PATCH | crm/v8/settings/global_picklists | write | global-picklists | Update global picklists. |
| DELETE | crm/v8/settings/global_picklists | write | global-picklists | Delete global picklists. |
| GET | crm/v8/settings/global_picklists/{id} | read | global-picklists | Get global picklist. |
| PATCH | crm/v8/settings/global_picklists/{id} | write | global-picklists | Update global picklist. |
| DELETE | crm/v8/settings/global_picklists/{id} | write | global-picklists | Delete global picklist. |
| GET | crm/v8/settings/global_picklists/{id}/actions/associations | read | global-picklists | Get associations. |
| GET | crm/v8/settings/global_picklists/{id}/actions/pick_list_values_associations | read | global-picklists | Get pick list value associations. |
| POST | crm/v8/settings/global_picklists/{id}/actions/replace_picklist_values | write | global-picklists | Replace picklist values. |
| GET | crm/v8/settings/global_picklists/{id}/actions/replaced_values | read | global-picklists | Get replace values. |
| GET | crm/v8/settings/holidays | read | holidays | Get holidays. |
| POST | crm/v8/settings/holidays | write | holidays | Create holidays. |
| PUT | crm/v8/settings/holidays | write | holidays | Update holidays. |
| GET | crm/v8/settings/holidays/{id} | read | holidays | Get holiday. |
| PUT | crm/v8/settings/holidays/{id} | write | holidays | Update holiday. |
| DELETE | crm/v8/settings/holidays/{id} | write | holidays | Delete holiday. |
| POST | crm/v8/{id}/{id}/actions/convert | write | inventory-convert | Convert inventory. |
| GET | crm/v8/{id}/actions/mass_convert | read | inventory-mass-convert | Get scheduled jobs details. |
| POST | crm/v8/{id}/actions/mass_convert | write | inventory-mass-convert | Mass inventory convert. |
| GET | crm/v8/settings/inventory_templates | read | inventory-templates | Get inventory templates. |
| GET | crm/v8/settings/inventory_templates/{id} | read | inventory-templates | Get inventory template. |
| GET | crm/v8/settings/layouts | read | layouts | Get layouts. |
| GET | crm/v8/settings/layouts/{id} | read | layouts | Get layout. |
| PATCH | crm/v8/settings/layouts/{id} | write | layouts | Update custom layout. |
| DELETE | crm/v8/settings/layouts/{id} | write | layouts | Delete custom layout. |
| POST | crm/v8/settings/layouts/{id}/actions/activate | write | layouts | Activate custom layout. |
| DELETE | crm/v8/settings/layouts/{id}/actions/activate | write | layouts | Deactivate custom layout. |
| POST | crm/v8/{id}/{id}/actions/download_mail_merge | write | mail-merge | Download mail merge. |
| POST | crm/v8/{id}/{id}/actions/send_mail_merge | write | mail-merge | Send mail merge. |
| POST | crm/v8/{id}/{id}/actions/sign_mail_merge | write | mail-merge | Sign mail merge. |
| GET | crm/v8/{id}/actions/mass_change_owner | read | mass-change-owner | Check status. |
| POST | crm/v8/{id}/actions/mass_change_owner | write | mass-change-owner | Change owner. |
| GET | crm/v8/Leads/actions/mass_convert | read | mass-convert | Get job status. |
| POST | crm/v8/Leads/actions/mass_convert | write | mass-convert | Mass convert. |
| GET | crm/v8/{id}/actions/mass_delete | read | mass-delete-cvid | Get mass delete status. |
| POST | crm/v8/{id}/actions/mass_delete | write | mass-delete-cvid | Mass delete records. |
| GET | crm/v8/settings/tags/actions/mass_delete | read | mass-delete-tags | Get status. |
| POST | crm/v8/settings/tags/actions/mass_delete | write | mass-delete-tags | Mass delete tags. |
| GET | crm/v8/settings/modules | read | modules | Get modules. |
| POST | crm/v8/settings/modules | write | modules | Create custom modules. |
| GET | crm/v8/settings/modules/{id} | read | modules | Get module by api name. |
| PUT | crm/v8/settings/modules/{id} | write | modules | Update module by api name. |
| GET | crm/v8/Notes | read | notes | Get notes. |
| POST | crm/v8/Notes | write | notes | Create notes. |
| PUT | crm/v8/Notes | write | notes | Update notes. |
| DELETE | crm/v8/Notes | write | notes | Delete notes. |
| GET | crm/v8/Notes/{id} | read | notes | Get note. |
| PUT | crm/v8/Notes/{id} | write | notes | Update note. |
| DELETE | crm/v8/Notes/{id} | write | notes | Delete note. |
| GET | crm/v8/actions/watch | read | notifications | Get notifications. |
| POST | crm/v8/actions/watch | write | notifications | Enable notifications. |
| PUT | crm/v8/actions/watch | write | notifications | Update notifications. |
| PATCH | crm/v8/actions/watch | write | notifications | Update notification. |
| DELETE | crm/v8/actions/watch | write | notifications | Delete notification. |
| GET | crm/v8/org | read | org | Get organization. |
| GET | crm/v8/org/photo | read | org | Get org photo. |
| POST | crm/v8/org/photo | write | org | Upload organization photo. |
| DELETE | crm/v8/org/photo | write | org | Delete organization photo. |
| GET | crm/v8/settings/fields/{id}/pick_list_values | read | pick-list-values | Get pick list values. |
| GET | crm/v8/settings/pipeline | read | pipeline | Get pipelines. |
| POST | crm/v8/settings/pipeline | write | pipeline | Create pipeline. |
| PUT | crm/v8/settings/pipeline | write | pipeline | Update pipelines. |
| POST | crm/v8/settings/pipeline/actions/transfer | write | pipeline | Transfer pipelines. |
| GET | crm/v8/settings/pipeline/{id} | read | pipeline | Get pipeline. |
| PUT | crm/v8/settings/pipeline/{id} | write | pipeline | Update pipeline. |
| PATCH | crm/v8/settings/pipeline/{id} | write | pipeline | Delete pipeline. |
| POST | crm/v8/{id}/{id}/actions/portal_invite | write | portal-invite | Invite users. |
| GET | crm/v8/settings/portals/{id}/user_type | read | portal-user-type | Get user types. |
| POST | crm/v8/settings/portals/{id}/user_type | write | portal-user-type | Create user type. |
| GET | crm/v8/settings/portals/{id}/user_type/{id} | read | portal-user-type | Get user type. |
| PUT | crm/v8/settings/portals/{id}/user_type/{id} | write | portal-user-type | Update user type. |
| DELETE | crm/v8/settings/portals/{id}/user_type/{id} | write | portal-user-type | Delete user type. |
| GET | crm/v8/settings/portals | read | portals | Get portals. |
| POST | crm/v8/settings/portals | write | portals | Create portal. |
| GET | crm/v8/settings/portals/{id} | read | portals | Get portal. |
| PUT | crm/v8/settings/portals/{id} | write | portals | Update portal. |
| GET | crm/v8/settings/profiles | read | profiles | Get profiles. |
| GET | crm/v8/settings/profiles/{id} | read | profiles | Get profile. |
| PUT | crm/v8/settings/profiles/{id} | write | profiles | Update profile. |
| DELETE | crm/v8/settings/profiles/{id} | write | profiles | Delete profile. |
| POST | crm/v8/settings/profiles/{id}/actions/clone | write | profiles | Clone profiles. |
| GET | crm/v8/{id}/{id}/Locking_Information__s | read | record-locking | Get record locking informations. |
| POST | crm/v8/{id}/{id}/Locking_Information__s | write | record-locking | Lock records. |
| GET | crm/v8/{id}/{id}/Locking_Information__s/{id} | read | record-locking | Get record locking information. |
| PUT | crm/v8/{id}/{id}/Locking_Information__s/{id} | write | record-locking | Update record locking information. |
| DELETE | crm/v8/{id}/{id}/Locking_Information__s/{id} | write | record-locking | Unlock record. |
| GET | crm/v8/settings/record_locking_configurations | read | record-locking-configuration | Get record locking configurations. |
| POST | crm/v8/settings/record_locking_configurations | write | record-locking-configuration | Add record locking configuration. |
| PUT | crm/v8/settings/record_locking_configurations | write | record-locking-configuration | Update record locking configurations. |
| PUT | crm/v8/settings/record_locking_configurations/{id} | write | record-locking-configuration | Update record locking configuration. |
| DELETE | crm/v8/settings/record_locking_configurations/{id} | write | record-locking-configuration | Delete record locking configuration. |
| POST | crm/v8/{id}/actions/share_emails | write | record-share-email | Share bulk emails. |
| POST | crm/v8/{id}/actions/unshare_emails | write | record-share-email | Unshare bulk emails. |
| POST | crm/v8/{id}/{id}/actions/share_emails | write | record-share-email | Share emails. |
| POST | crm/v8/{id}/{id}/actions/unshare_emails | write | record-share-email | Unshare emails. |
| GET | crm/v8/{id} | read | records | Get records of a module. |
| POST | crm/v8/{id} | write | records | Create records in a module. |
| PUT | crm/v8/{id} | write | records | Update records in a module. |
| DELETE | crm/v8/{id} | write | records | Delete records from a module. |
| POST | crm/v8/{id}/actions/assign_territories | write | records | Assign territories to multiple records. |
| GET | crm/v8/{id}/actions/count | read | records | Record count. |
| GET | crm/v8/{id}/actions/fetch_full_data | read | records | Get rich text records. |
| GET | crm/v8/{id}/actions/mass_update | read | records | Get mass update status. |
| POST | crm/v8/{id}/actions/mass_update | write | records | Mass update records. |
| POST | crm/v8/{id}/actions/remove_territories | write | records | Remove territories from multiple records. |
| GET | crm/v8/{id}/deleted | read | records | Get deleted records. |
| GET | crm/v8/{id}/search | read | records | Search records of a module. |
| POST | crm/v8/{id}/upsert | write | records | Insert or update records by duplicate-check fields. |
| GET | crm/v8/{id}/{id} | read | records | Get a record by ID. |
| PUT | crm/v8/{id}/{id} | write | records | Update a record by ID. |
| DELETE | crm/v8/{id}/{id} | write | records | Delete a record by ID. |
| POST | crm/v8/{id}/{id}/actions/assign_territories | write | records | Assign territory to record. |
| POST | crm/v8/{id}/{id}/actions/clone | write | records | Clone record. |
| GET | crm/v8/{id}/{id}/actions/fetch_full_data | read | records | Get full data for rich text. |
| POST | crm/v8/{id}/{id}/actions/remove_territories | write | records | Remove territories from record. |
| GET | crm/v8/{id}/{id}/photo | read | records | Get photo. |
| POST | crm/v8/{id}/{id}/photo | write | records | Upload photo. |
| DELETE | crm/v8/{id}/{id}/photo | write | records | Delete photo. |
| GET | crm/v8/settings/recycle_bin | read | recycle-bin | Get recyclebin records. |
| DELETE | crm/v8/settings/recycle_bin | write | recycle-bin | Delete recyclebin records. |
| GET | crm/v8/settings/recycle_bin/{id} | read | recycle-bin | Get recyclebin record. |
| DELETE | crm/v8/settings/recycle_bin/{id} | write | recycle-bin | Delete recyclebin record. |
| GET | crm/v8/settings/related_lists | read | related-lists | Get related lists. |
| GET | crm/v8/settings/related_lists/{id} | read | related-lists | Get related list. |
| GET | crm/v8/{id}/deleted/{id}/{id} | read | related-records | Get deleted parent records related record. |
| GET | crm/v8/{id}/{id}/{id} | read | related-records | Get the records in a related list of a record. |
| PUT | crm/v8/{id}/{id}/{id} | write | related-records | Update the records in a related list of a record. |
| DELETE | crm/v8/{id}/{id}/{id} | write | related-records | Delink related records from a record. |
| GET | crm/v8/{id}/{id}/{id}/{id} | read | related-records | Get a related record. |
| PUT | crm/v8/{id}/{id}/{id}/{id} | write | related-records | Update a related record. |
| DELETE | crm/v8/{id}/{id}/{id}/{id} | write | related-records | Delink a related record. |
| GET | crm/v8/Appointments_Rescheduled_History__s | read | reschedule-history | Get appointments rescheduled history. |
| POST | crm/v8/Appointments_Rescheduled_History__s | write | reschedule-history | Add appointments rescheduled history. |
| PUT | crm/v8/Appointments_Rescheduled_History__s | write | reschedule-history | Update appointments rescheduled history. |
| GET | crm/v8/Appointments_Rescheduled_History__s/{id} | read | reschedule-history | Get appointment rescheduled history. |
| PUT | crm/v8/Appointments_Rescheduled_History__s/{id} | write | reschedule-history | Update appointment rescheduled history. |
| DELETE | crm/v8/Appointments_Rescheduled_History__s/{id} | write | reschedule-history | Delete appointments rescheduled history. |
| GET | crm/v8/settings/roles | read | roles | Get roles. |
| POST | crm/v8/settings/roles | write | roles | Create roles. |
| PUT | crm/v8/settings/roles | write | roles | Update roles. |
| GET | crm/v8/settings/roles/{id} | read | roles | Get role. |
| PUT | crm/v8/settings/roles/{id} | write | roles | Update role. |
| DELETE | crm/v8/settings/roles/{id} | write | roles | Delete role. |
| GET | crm/v8/settings/automation/scoring_rules | read | scoring-rules | Get scoring rules. |
| POST | crm/v8/settings/automation/scoring_rules | write | scoring-rules | Create scoring rules. |
| PUT | crm/v8/settings/automation/scoring_rules | write | scoring-rules | Update scoring rules. |
| DELETE | crm/v8/settings/automation/scoring_rules | write | scoring-rules | Delete scoring rules. |
| GET | crm/v8/settings/automation/scoring_rules/{id} | read | scoring-rules | Get scoring rule. |
| PUT | crm/v8/settings/automation/scoring_rules/{id} | write | scoring-rules | Update scoring rule. |
| DELETE | crm/v8/settings/automation/scoring_rules/{id} | write | scoring-rules | Delete scoring rule. |
| PUT | crm/v8/settings/automation/scoring_rules/{id}/actions/activate | write | scoring-rules | Activate scoring rule. |
| DELETE | crm/v8/settings/automation/scoring_rules/{id}/actions/activate | write | scoring-rules | Deactivate scoring rule. |
| POST | crm/v8/settings/automation/scoring_rules/{id}/actions/clone | write | scoring-rules | Clone scoring rule. |
| PUT | crm/v8/{id}/actions/run_scoring_rules | write | scoring-rules | Scoring rule execution using layout id. |
| POST | crm/v8/{id}/{id}/actions/send_mail | write | send-mail | Send mail. |
| GET | crm/v8/settings/service_preferences | read | service-preference | Get service preference. |
| PUT | crm/v8/settings/service_preferences | write | service-preference | Update service preference. |
| GET | crm/v8/{id}/{id}/actions/share | read | share-records | Get shared record details. |
| POST | crm/v8/{id}/{id}/actions/share | write | share-records | Share record. |
| PUT | crm/v8/{id}/{id}/actions/share | write | share-records | Update share permissions. |
| DELETE | crm/v8/{id}/{id}/actions/share | write | share-records | Revoke shared record. |
| GET | crm/v8/settings/data_sharing/rules | read | sharing-rules | Get sharing rules. |
| POST | crm/v8/settings/data_sharing/rules | write | sharing-rules | Create sharing rules. |
| PUT | crm/v8/settings/data_sharing/rules | write | sharing-rules | Update sharing rules. |
| POST | crm/v8/settings/data_sharing/rules/actions/run | write | sharing-rules | Rerun sharing rules. |
| GET | crm/v8/settings/data_sharing/rules/actions/summary | read | sharing-rules | Get sharing rule summary. |
| POST | crm/v8/settings/data_sharing/rules/actions/summary | read | sharing-rules | Search sharing rules summary. |
| POST | crm/v8/settings/data_sharing/rules/search | read | sharing-rules | Search sharing rules. |
| GET | crm/v8/settings/data_sharing/rules/{id} | read | sharing-rules | Get sharing rule. |
| PUT | crm/v8/settings/data_sharing/rules/{id} | write | sharing-rules | Update sharing rule. |
| DELETE | crm/v8/settings/data_sharing/rules/{id} | write | sharing-rules | Delete sharing rule. |
| PUT | crm/v8/settings/data_sharing/rules/{id}/actions/activate | write | sharing-rules | Activate sharing rule. |
| DELETE | crm/v8/settings/data_sharing/rules/{id}/actions/activate | write | sharing-rules | Deactivate sharing rule. |
| GET | crm/v8/settings/business_hours/shift_hours | read | shift-hours | Get shift hours. |
| POST | crm/v8/settings/business_hours/shift_hours | write | shift-hours | Create shifts hours. |
| PUT | crm/v8/settings/business_hours/shift_hours | write | shift-hours | Update shift hours. |
| GET | crm/v8/settings/business_hours/shift_hours/{id} | read | shift-hours | Get shift hour. |
| PUT | crm/v8/settings/business_hours/shift_hours/{id} | write | shift-hours | Update shift hour. |
| DELETE | crm/v8/settings/business_hours/shift_hours/{id} | write | shift-hours | Delete shift hour. |
| GET | crm/v8/settings/signals | read | signals | Get signals. |
| POST | crm/v8/signals/notifications | write | signals-notifications | Create signals. |
| GET | crm/v8/settings/tags | read | tags | Get tags. |
| POST | crm/v8/settings/tags | write | tags | Create tags. |
| PUT | crm/v8/settings/tags | write | tags | Update tags. |
| PUT | crm/v8/settings/tags/{id} | write | tags | Update tag. |
| DELETE | crm/v8/settings/tags/{id} | write | tags | Delete tag. |
| POST | crm/v8/settings/tags/{id}/actions/merge | write | tags | Merge tags. |
| GET | crm/v8/settings/tags/{id}/actions/records_count | read | tags | Get record count for tag. |
| POST | crm/v8/{id}/actions/add_tags | write | tags | Add tags to multiple records. |
| POST | crm/v8/{id}/actions/remove_tags | write | tags | Remove tags from multiple records. |
| POST | crm/v8/{id}/{id}/actions/add_tags | write | tags | Add tags. |
| POST | crm/v8/{id}/{id}/actions/remove_tags | write | tags | Remove tags. |
| GET | crm/v8/org/taxes | read | taxes | Get taxes. |
| PUT | crm/v8/org/taxes | write | taxes | Update taxes. |
| GET | crm/v8/org/taxes/{id} | read | taxes | Get tax. |
| GET | crm/v8/settings/territories | read | territories | Get territories. |
| POST | crm/v8/settings/territories | write | territories | Create territories. |
| PUT | crm/v8/settings/territories | write | territories | Update territories. |
| DELETE | crm/v8/settings/territories | write | territories | Delete territories. |
| GET | crm/v8/settings/territories/actions/associated_users_count | read | territories | Get associated user count. |
| POST | crm/v8/settings/territories/actions/transfer_and_delete | write | territories | Transfer and delete territories. |
| GET | crm/v8/settings/territories/{id} | read | territories | Get territory. |
| PUT | crm/v8/settings/territories/{id} | write | territories | Update territory. |
| DELETE | crm/v8/settings/territories/{id} | write | territories | Delete territory. |
| GET | crm/v8/settings/territories/{id}/__child_territories | read | territories | Get child territory. |
| POST | crm/v8/settings/territories/{id}/actions/transfer_and_delete | write | territories | Transfer and delete territory. |
| GET | crm/v8/settings/territories/{id}/users | read | territory-users | Get territory users. |
| PUT | crm/v8/settings/territories/{id}/users | write | territory-users | Update territory users. |
| DELETE | crm/v8/settings/territories/{id}/users | write | territory-users | Deassociate territory users. |
| GET | crm/v8/settings/territories/{id}/users/{id} | read | territory-users | Get territory user. |
| PUT | crm/v8/settings/territories/{id}/users/{id} | write | territory-users | Update territory user. |
| DELETE | crm/v8/settings/territories/{id}/users/{id} | write | territory-users | Deassociate territory user. |
| GET | crm/v8/{id}/{id}/__timeline | read | timelines | Get timelines. |
| POST | crm/v8/{id}/actions/unblock_email | write | unblock-email | Unblock emails. |
| POST | crm/v8/{id}/{id}/actions/unblock_email | write | unblock-email | Unblock email. |
| GET | crm/v8/settings/unsubscribe_link/actions/associations | read | unsubscribe-links | Get associated unsubscribe links. |
| GET | crm/v8/settings/unsubscribe_links | read | unsubscribe-links | Get unsubscribe links. |
| POST | crm/v8/settings/unsubscribe_links | write | unsubscribe-links | Create unsubscribe link. |
| PUT | crm/v8/settings/unsubscribe_links | write | unsubscribe-links | Update unsubscribe links. |
| GET | crm/v8/settings/unsubscribe_links/{id} | read | unsubscribe-links | Get unsubscribe link. |
| PUT | crm/v8/settings/unsubscribe_links/{id} | write | unsubscribe-links | Update unsubscribe link. |
| DELETE | crm/v8/settings/unsubscribe_links/{id} | write | unsubscribe-links | Delete unsubscribe link. |
| GET | crm/v8/settings/user_groups | read | user-groups | Get groups. |
| POST | crm/v8/settings/user_groups | write | user-groups | Create groups. |
| PUT | crm/v8/settings/user_groups | write | user-groups | Update groups. |
| GET | crm/v8/settings/user_groups/actions/associated_users_count | read | user-groups | Get associated users count. |
| GET | crm/v8/settings/user_groups/{id} | read | user-groups | Get group. |
| PUT | crm/v8/settings/user_groups/{id} | write | user-groups | Update group. |
| DELETE | crm/v8/settings/user_groups/{id} | write | user-groups | Delete group. |
| GET | crm/v8/settings/user_groups/{id}/actions/associations | read | user-groups | Get associations. |
| GET | crm/v8/settings/user_groups/{id}/actions/sources_count | read | user-groups | Get sources count. |
| GET | crm/v8/settings/user_groups/{id}/associated_users/actions/grouped_counts | read | user-groups | Get grouped counts. |
| GET | crm/v8/settings/user_groups/{id}/sources | read | user-groups | Get sources. |
| GET | crm/v8/users/{id}/actions/associated_groups | read | user-groups | Get associate groups of user. |
| GET | crm/v8/settings/portals/{id}/user_type/{id}/users | read | user-type-users | Get users of user type. |
| DELETE | crm/v8/settings/portals/{id}/user_type/{id}/users | write | user-type-users | Delete user from the portal. |
| POST | crm/v8/settings/portals/{id}/user_type/{id}/users/action/transfer | write | user-type-users | Transfer users of a user type. |
| PUT | crm/v8/settings/portals/{id}/user_type/{id}/users/{id}/actions/change_status | write | user-type-users | Change users status. |
| GET | crm/v8/users | read | users | Get users. |
| POST | crm/v8/users | write | users | Create users. |
| PUT | crm/v8/users | write | users | Update users. |
| GET | crm/v8/users/actions/count | read | users | Users count. |
| GET | crm/v8/users/{id} | read | users | Get user. |
| PUT | crm/v8/users/{id} | write | users | Update user. |
| DELETE | crm/v8/users/{id} | write | users | Delete user. |
| GET | crm/v8/users/{id}/territories | read | users-territories | Get territories of user. |
| PUT | crm/v8/users/{id}/territories | write | users-territories | Associate territories to user. |
| DELETE | crm/v8/users/{id}/territories | write | users-territories | Remove territories from user. |
| GET | crm/v8/users/{id}/territories/{id} | read | users-territories | Get territory of user. |
| DELETE | crm/v8/users/{id}/territories/{id} | write | users-territories | Remove territory from user. |
| GET | crm/v8/users/actions/transfer_and_delete | read | users-transfer-delete | Get status. |
| POST | crm/v8/users/actions/transfer_and_delete | write | users-transfer-delete | Users transfer and delete. |
| POST | crm/v8/users/{id}/actions/transfer_and_delete | write | users-transfer-delete | User transfer and delete. |
| GET | crm/v8/settings/users_unavailability | read | users-unavailability | Get users unavailability. |
| POST | crm/v8/settings/users_unavailability | write | users-unavailability | Create users unavailability. |
| PUT | crm/v8/settings/users_unavailability | write | users-unavailability | Update users unavailability. |
| GET | crm/v8/settings/users_unavailability/{id} | read | users-unavailability | Get user unavailability. |
| PUT | crm/v8/settings/users_unavailability/{id} | write | users-unavailability | Update user unavailability. |
| DELETE | crm/v8/settings/users_unavailability/{id} | write | users-unavailability | Delete user unavailability. |
| GET | crm/v8/settings/variable_groups | read | variable-groups | Get variable groups. |
| GET | crm/v8/settings/variable_groups/{id} | read | variable-groups | Get variable group by id. |
| GET | crm/v8/settings/variables | read | variables | Get variables. |
| POST | crm/v8/settings/variables | write | variables | Create variables. |
| PUT | crm/v8/settings/variables | write | variables | Update variables. |
| DELETE | crm/v8/settings/variables | write | variables | Delete variables. |
| GET | crm/v8/settings/variables/{id} | read | variables | Get variable by id. |
| PUT | crm/v8/settings/variables/{id} | write | variables | Update variable by id. |
| DELETE | crm/v8/settings/variables/{id} | write | variables | Delete variable. |
| GET | crm/v8/settings/webforms | read | webforms | Get web forms. |
| POST | crm/v8/settings/webforms | write | webforms | Create web forms. |
| GET | crm/v8/settings/webforms/{id} | read | webforms | Get web form. |
| PUT | crm/v8/settings/webforms/{id} | write | webforms | Update web form. |
| DELETE | crm/v8/settings/webforms/{id} | write | webforms | Delete web forms. |
| GET | crm/v8/settings/webforms/{id}/actions/preview | read | webforms | Get webforms preview. |
| GET | crm/v8/settings/wizards | read | wizards | Get wizards. |
| GET | crm/v8/settings/wizards/{id} | read | wizards | Get wizard by id. |
| GET | crm/v8/settings/zia/data_enrichment | read | zia-enrichment | Get zia enrichment. |
| GET | crm/v8/__zia_org_enrichment | read | zia-org-enrichment | Get zia org enrichments. |
| POST | crm/v8/__zia_org_enrichment | write | zia-org-enrichment | Create zia org enrichment. |
| GET | crm/v8/__zia_org_enrichment/{id} | read | zia-org-enrichment | Get zia org enrichment. |
| GET | crm/v8/__zia_people_enrichment | read | zia-people-enrichment | Get zia people enrichments. |
| POST | crm/v8/__zia_people_enrichment | write | zia-people-enrichment | Create zia people enrichment. |
| GET | crm/v8/__zia_people_enrichment/{id} | read | zia-people-enrichment | Get zia people enrichment. |
