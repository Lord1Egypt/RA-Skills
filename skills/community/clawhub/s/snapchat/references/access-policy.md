# Snapchat access policy

An access policy limits which endpoints Snapchat connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/snapchat#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Snapchat: its 142 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create snapchat --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1/adaccounts/{id}"},
    {"method": "GET", "path": "v1/organizations/{id}/adaccounts"},
    {"method": "POST", "path": "v1/adaccounts/{id}/ad_squad_outcome_estimates_v2"},
    {"method": "GET", "path": "v1/adaccounts/{id}/ad_squad_ui_render_data"},
    {"method": "GET", "path": "v1/adaccounts/{id}/adsquads"},
    {"method": "POST", "path": "v1/adaccounts/{id}/bid_estimate"},
    {"method": "POST", "path": "v1/adaccounts/{id}/get_adsquads_by_ids"},
    {"method": "POST", "path": "v1/adaccounts/{id}/reserved_forecasting"},
    {"method": "GET", "path": "v1/adaccounts/{id}/spend_guidance"},
    {"method": "GET", "path": "v1/adsquads/{id}"},
    {"method": "GET", "path": "v1/adsquads/{id}/ad_squad_ad_restrictions"},
    {"method": "GET", "path": "v1/adsquads/{id}/ad_squad_ui_render_data"},
    {"method": "GET", "path": "v1/adsquads/{id}/bid_estimate"},
    {"method": "GET", "path": "v1/adsquads/{id}/external_changelogs"},
    {"method": "GET", "path": "v1/campaigns/{id}/adsquads"},
    {"method": "GET", "path": "v1/adaccounts/{id}/ads"},
    {"method": "POST", "path": "v1/adaccounts/{id}/get_ads_by_ids"},
    {"method": "GET", "path": "v1/ads/{id}"},
    {"method": "GET", "path": "v1/ads/{id}/external_changelogs"},
    {"method": "GET", "path": "v1/adsquads/{id}/ads"},
    {"method": "GET", "path": "v1/campaigns/{id}/ads"},
    {"method": "POST", "path": "v1/adaccounts/{id}/audience_size"},
    {"method": "POST", "path": "v1/adaccounts/{id}/audience_size_v2"},
    {"method": "GET", "path": "v1/adaccounts/{id}/segments"},
    {"method": "POST", "path": "v1/adaccounts/{id}/targeting_insights"},
    {"method": "GET", "path": "v1/adsquads/{id}/audience_size_v2"},
    {"method": "GET", "path": "v1/segments/{id}"},
    {"method": "GET", "path": "v1/adaccounts/{id}/smart-rules"},
    {"method": "GET", "path": "v1/adaccounts/{id}/smart-rules/executions"},
    {"method": "GET", "path": "v1/adaccounts/{id}/smart-rules/{id}"},
    {"method": "GET", "path": "v1/billingcenters/{id}"},
    {"method": "GET", "path": "v1/organizations/{id}/billingcenters"},
    {"method": "GET", "path": "v1/adaccounts/{id}/campaigns"},
    {"method": "POST", "path": "v1/adaccounts/{id}/get_campaigns_by_ids"},
    {"method": "GET", "path": "v1/adaccounts/{id}/sbo_tcpa_eligibility"},
    {"method": "GET", "path": "v1/campaigns/{id}"},
    {"method": "GET", "path": "v1/campaigns/{id}/external_changelogs"},
    {"method": "GET", "path": "v1/catalogs/{id}"},
    {"method": "POST", "path": "v1/catalogs/{id}/facets"},
    {"method": "POST", "path": "v1/catalogs/{id}/flights/search"},
    {"method": "POST", "path": "v1/catalogs/{id}/hotels/search"},
    {"method": "GET", "path": "v1/catalogs/{id}/product_feeds"},
    {"method": "POST", "path": "v1/catalogs/{id}/product_search"},
    {"method": "GET", "path": "v1/catalogs/{id}/product_sets"},
    {"method": "POST", "path": "v1/catalogs/{id}/products/search"},
    {"method": "GET", "path": "v1/organizations/{id}/catalogs"},
    {"method": "GET", "path": "v1/product_feeds/{id}"},
    {"method": "GET", "path": "v1/product_feeds/{id}/feed_uploads"},
    {"method": "GET", "path": "v1/adaccounts/{id}/creatives"},
    {"method": "POST", "path": "v1/adaccounts/{id}/get_creatives_by_ids"},
    {"method": "GET", "path": "v1/adaccounts/{id}/phone_numbers"},
    {"method": "GET", "path": "v1/creatives/{id}"},
    {"method": "GET", "path": "v1/creatives/{id}/creative_preview"},
    {"method": "GET", "path": "v1/creatives/{id}/external_changelogs"},
    {"method": "GET", "path": "v1/creatives/{id}/snapcode"},
    {"method": "GET", "path": "v1/tools/extract_snap_id"},
    {"method": "GET", "path": "v1/custom_conversions/{id}"},
    {"method": "GET", "path": "v1/adaccounts/{id}/dynamic_templates"},
    {"method": "GET", "path": "v1/dynamic_templates/{id}"},
    {"method": "GET", "path": "v1/dynamic_templates/{id}/external_changelogs"},
    {"method": "GET", "path": "v1/adaccounts/{id}/event_details"},
    {"method": "GET", "path": "v1/event_details/{id}"},
    {"method": "GET", "path": "v1/fundingsources/{id}"},
    {"method": "GET", "path": "v1/organizations/{id}/fundingsources"},
    {"method": "GET", "path": "v1/adaccounts/{id}/interaction_zones"},
    {"method": "GET", "path": "v1/interaction_zones/{id}"},
    {"method": "GET", "path": "v1/adaccounts/{id}/invoices"},
    {"method": "GET", "path": "v1/adaccounts/{id}/invoices/{id}"},
    {"method": "GET", "path": "v1/adaccounts/{id}/lead_generation_forms"},
    {"method": "GET", "path": "v1/lead_gen/forms/{id}/integrations"},
    {"method": "GET", "path": "v1/lead_generation_forms/{id}"},
    {"method": "POST", "path": "v1/adaccounts/{id}/get_media_by_ids"},
    {"method": "GET", "path": "v1/adaccounts/{id}/media"},
    {"method": "GET", "path": "v1/media/{id}"},
    {"method": "GET", "path": "v1/media/{id}/lens_preview"},
    {"method": "GET", "path": "v1/media/{id}/preview"},
    {"method": "GET", "path": "v1/media/{id}/thumbnail"},
    {"method": "GET", "path": "v1/members/{id}"},
    {"method": "GET", "path": "v1/organizations/{id}/members"},
    {"method": "GET", "path": "v1/mmm/reports/{id}"},
    {"method": "GET", "path": "v1/adaccounts/{id}/mobile_apps"},
    {"method": "GET", "path": "v1/mobile_apps/{id}"},
    {"method": "GET", "path": "v1/mobile_apps/{id}/campaign_eligibilities"},
    {"method": "GET", "path": "v1/mobile_apps/{id}/custom_conversions"},
    {"method": "GET", "path": "v1/mobile_apps/{id}/ecid_status"},
    {"method": "GET", "path": "v1/mobile_apps/{id}/event_quality_scores"},
    {"method": "GET", "path": "v1/mobile_apps/{id}/skadnetwork_adsquads"},
    {"method": "GET", "path": "v1/organizations/{id}/mobile_apps"},
    {"method": "GET", "path": "v1/adaccounts/{id}/offer_disclaimers"},
    {"method": "GET", "path": "v1/adaccounts/{id}/offer_disclaimers/{id}"},
    {"method": "GET", "path": "v1/organizations/{id}"},
    {"method": "GET", "path": "v1/adaccounts/{id}/pixels"},
    {"method": "GET", "path": "v1/organizations/{id}/pixels"},
    {"method": "GET", "path": "v1/pixels/{id}"},
    {"method": "GET", "path": "v1/pixels/{id}/campaign_eligibilities"},
    {"method": "GET", "path": "v1/pixels/{id}/custom_conversions"},
    {"method": "GET", "path": "v1/pixels/{id}/domains/stats"},
    {"method": "GET", "path": "v1/pixels/{id}/event_quality_scores"},
    {"method": "GET", "path": "v1/pixels/{id}/stats"},
    {"method": "GET", "path": "v1/adaccounts/{id}/roles"},
    {"method": "GET", "path": "v1/catalogs/{id}/roles"},
    {"method": "GET", "path": "v1/members/{id}/roles"},
    {"method": "GET", "path": "v1/organizations/{id}/roles"},
    {"method": "GET", "path": "v1/adaccounts/{id}/leads_report"},
    {"method": "GET", "path": "v1/adaccounts/{id}/stats"},
    {"method": "GET", "path": "v1/adaccounts/{id}/stats_report"},
    {"method": "GET", "path": "v1/ads/{id}/stats"},
    {"method": "GET", "path": "v1/ads/{id}/stats_report"},
    {"method": "GET", "path": "v1/adsquads/{id}/stats"},
    {"method": "GET", "path": "v1/adsquads/{id}/stats_report"},
    {"method": "GET", "path": "v1/campaigns/{id}/stats"},
    {"method": "GET", "path": "v1/campaigns/{id}/stats_report"},
    {"method": "GET", "path": "v1/creatives/{id}/stats"},
    {"method": "GET", "path": "v1/media/{id}/stats"},
    {"method": "GET", "path": "v1/adsquads/{id}/targeting_specs"},
    {"method": "GET", "path": "v1/targeting/demographics/advanced_demographics"},
    {"method": "GET", "path": "v1/targeting/demographics/age_group"},
    {"method": "GET", "path": "v1/targeting/demographics/gender"},
    {"method": "GET", "path": "v1/targeting/demographics/languages"},
    {"method": "GET", "path": "v1/targeting/device/carrier"},
    {"method": "GET", "path": "v1/targeting/device/connection_type"},
    {"method": "GET", "path": "v1/targeting/device/marketing_name"},
    {"method": "GET", "path": "v1/targeting/device/os_type"},
    {"method": "GET", "path": "v1/targeting/device/{id}/os_version"},
    {"method": "GET", "path": "v1/targeting/geo/country"},
    {"method": "GET", "path": "v1/targeting/geo/{id}/metro"},
    {"method": "GET", "path": "v1/targeting/geo/{id}/postal_code"},
    {"method": "GET", "path": "v1/targeting/geo/{id}/region"},
    {"method": "GET", "path": "v1/targeting/interests/dlxc"},
    {"method": "GET", "path": "v1/targeting/interests/dlxp"},
    {"method": "GET", "path": "v1/targeting/interests/dlxs"},
    {"method": "GET", "path": "v1/targeting/interests/nln"},
    {"method": "GET", "path": "v1/targeting/location/categories_loi"},
    {"method": "GET", "path": "v1/targeting/v1/interests/scls"},
    {"method": "GET", "path": "v1/targeting/v1/interests/shp"},
    {"method": "GET", "path": "v1/targeting/v1/interests/vac"},
    {"method": "GET", "path": "v1/targeting/v1/options"},
    {"method": "GET", "path": "v1/targeting_specs/{id}"},
    {"method": "GET", "path": "v1/organizations/{id}/transactions"},
    {"method": "GET", "path": "v1/me"},
    {"method": "GET", "path": "v1/me/organizations"},
    {"method": "GET", "path": "v1/me/source_organizations"}
  ],
  "deny": []
}
```

## Endpoints

The Snapchat endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v1/adaccounts/{id} | read | ad accounts | Get an ad account. |
| GET | v1/organizations/{id}/adaccounts | read | ad accounts | List ad accounts of an organization. |
| POST | v1/organizations/{id}/adaccounts | write | ad accounts | Create an ad account. |
| PUT | v1/organizations/{id}/adaccounts | write | ad accounts | Update an ad account. |
| POST | v1/adaccounts/{id}/ad_squad_outcome_estimates_v2 | read | ad squads | Estimate outcomes for an ad squad configuration. |
| GET | v1/adaccounts/{id}/ad_squad_ui_render_data | read | ad squads | Get ad squad UI render data for an ad account. |
| GET | v1/adaccounts/{id}/adsquads | read | ad squads | List ad squads of an ad account. |
| POST | v1/adaccounts/{id}/bid_estimate | read | ad squads | Get a bid estimate for a targeting spec. |
| POST | v1/adaccounts/{id}/get_adsquads_by_ids | read | ad squads | Get ad squads by a list of IDs. |
| POST | v1/adaccounts/{id}/reserved_forecasting | read | ad squads | Forecast reach for a reserved campaign. |
| GET | v1/adaccounts/{id}/spend_guidance | read | ad squads | Get spend guidance for an ad account. |
| GET | v1/adsquads/{id} | read | ad squads | Get an ad squad. |
| DELETE | v1/adsquads/{id} | write | ad squads | Delete an ad squad. |
| GET | v1/adsquads/{id}/ad_squad_ad_restrictions | read | ad squads | Get ad restrictions of an ad squad. |
| GET | v1/adsquads/{id}/ad_squad_ui_render_data | read | ad squads | Get UI render data for an ad squad. |
| GET | v1/adsquads/{id}/bid_estimate | read | ad squads | Get a bid estimate for an ad squad. |
| GET | v1/adsquads/{id}/external_changelogs | read | ad squads | List the change log of an ad squad. |
| GET | v1/campaigns/{id}/adsquads | read | ad squads | List ad squads of a campaign. |
| POST | v1/campaigns/{id}/adsquads | write | ad squads | Create ad squads. |
| PUT | v1/campaigns/{id}/adsquads | write | ad squads | Update ad squads. |
| PATCH | v1/campaigns/{id}/adsquads/{id} | write | ad squads | Partially update an ad squad. |
| GET | v1/adaccounts/{id}/ads | read | ads | List ads of an ad account. |
| POST | v1/adaccounts/{id}/get_ads_by_ids | read | ads | Get ads by a list of IDs. |
| GET | v1/ads/{id} | read | ads | Get an ad. |
| DELETE | v1/ads/{id} | write | ads | Delete an ad. |
| GET | v1/ads/{id}/external_changelogs | read | ads | List the change log of an ad. |
| GET | v1/adsquads/{id}/ads | read | ads | List ads of an ad squad. |
| POST | v1/adsquads/{id}/ads | write | ads | Create ads. |
| PUT | v1/adsquads/{id}/ads | write | ads | Update ads. |
| PATCH | v1/adsquads/{id}/ads/{id} | write | ads | Partially update an ad. |
| GET | v1/campaigns/{id}/ads | read | ads | List ads of a campaign. |
| POST | v1/adaccounts/{id}/audience_size | read | audience segments | Estimate audience size. |
| POST | v1/adaccounts/{id}/audience_size_v2 | read | audience segments | Estimate audience size (v2). |
| GET | v1/adaccounts/{id}/segments | read | audience segments | List audience segments of an ad account. |
| POST | v1/adaccounts/{id}/segments | write | audience segments | Create audience segments. |
| PUT | v1/adaccounts/{id}/segments | write | audience segments | Update audience segments. |
| POST | v1/adaccounts/{id}/targeting_insights | read | audience segments | Get audience insights for a targeting spec. |
| GET | v1/adsquads/{id}/audience_size_v2 | read | audience segments | Get the audience size of an ad squad. |
| GET | v1/segments/{id} | read | audience segments | Get an audience segment. |
| DELETE | v1/segments/{id} | write | audience segments | Delete an audience segment. |
| DELETE | v1/segments/{id}/all_users | write | audience segments | Remove all users from a customer list segment. |
| POST | v1/segments/{id}/users | write | audience segments | Add users to a customer list segment. |
| DELETE | v1/segments/{id}/users | write | audience segments | Remove users from a customer list segment. |
| GET | v1/adaccounts/{id}/smart-rules | read | automated rules | List automated rules of an ad account. |
| POST | v1/adaccounts/{id}/smart-rules | write | automated rules | Create an automated rule. |
| GET | v1/adaccounts/{id}/smart-rules/executions | read | automated rules | List automated rule executions. |
| GET | v1/adaccounts/{id}/smart-rules/{id} | read | automated rules | Get an automated rule. |
| PATCH | v1/adaccounts/{id}/smart-rules/{id} | write | automated rules | Update an automated rule. |
| DELETE | v1/adaccounts/{id}/smart-rules/{id} | write | automated rules | Delete an automated rule. |
| GET | v1/billingcenters/{id} | read | billing centers | Get a billing center. |
| GET | v1/organizations/{id}/billingcenters | read | billing centers | List billing centers of an organization. |
| POST | v1/organizations/{id}/billingcenters | write | billing centers | Create a billing center. |
| PUT | v1/organizations/{id}/billingcenters | write | billing centers | Update a billing center. |
| GET | v1/adaccounts/{id}/campaigns | read | campaigns | List campaigns of an ad account. |
| POST | v1/adaccounts/{id}/campaigns | write | campaigns | Create campaigns. |
| PUT | v1/adaccounts/{id}/campaigns | write | campaigns | Update campaigns. |
| PATCH | v1/adaccounts/{id}/campaigns/{id} | write | campaigns | Partially update a campaign. |
| POST | v1/adaccounts/{id}/get_campaigns_by_ids | read | campaigns | Get campaigns by a list of IDs. |
| GET | v1/adaccounts/{id}/sbo_tcpa_eligibility | read | campaigns | Check ad account eligibility for target CPA bidding. |
| GET | v1/campaigns/{id} | read | campaigns | Get a campaign. |
| DELETE | v1/campaigns/{id} | write | campaigns | Delete a campaign. |
| GET | v1/campaigns/{id}/external_changelogs | read | campaigns | List the change log of a campaign. |
| GET | v1/catalogs/{id} | read | catalogs | Get a catalog. |
| DELETE | v1/catalogs/{id} | write | catalogs | Delete a catalog. |
| POST | v1/catalogs/{id}/facets | read | catalogs | Get product facets of a catalog. |
| POST | v1/catalogs/{id}/flights/search | read | catalogs | Search flights in a catalog. |
| POST | v1/catalogs/{id}/hotels/search | read | catalogs | Search hotels in a catalog. |
| GET | v1/catalogs/{id}/product_feeds | read | catalogs | List product feeds of a catalog. |
| POST | v1/catalogs/{id}/product_feeds | write | catalogs | Create a product feed. |
| PUT | v1/catalogs/{id}/product_feeds | write | catalogs | Update a product feed. |
| POST | v1/catalogs/{id}/product_search | read | catalogs | Search products in a catalog for dynamic ads. |
| GET | v1/catalogs/{id}/product_sets | read | catalogs | List product sets of a catalog. |
| POST | v1/catalogs/{id}/product_sets | write | catalogs | Create a product set. |
| PUT | v1/catalogs/{id}/product_sets | write | catalogs | Update product sets. |
| POST | v1/catalogs/{id}/products/search | read | catalogs | Search products in a catalog. |
| GET | v1/organizations/{id}/catalogs | read | catalogs | List catalogs of an organization. |
| POST | v1/organizations/{id}/catalogs | write | catalogs | Create a catalog. |
| PUT | v1/organizations/{id}/catalogs | write | catalogs | Update a catalog. |
| GET | v1/product_feeds/{id} | read | catalogs | Get a product feed. |
| DELETE | v1/product_feeds/{id} | write | catalogs | Delete a product feed. |
| GET | v1/product_feeds/{id}/feed_uploads | read | catalogs | List feed uploads of a product feed. |
| POST | v1/product_feeds/{id}/feed_uploads | write | catalogs | Create a feed upload. |
| PUT | v1/product_sets/{id} | write | catalogs | Update a product set. |
| POST | v1/adaccounts/{id}/creative_elements | write | creative elements | Create creative elements. |
| POST | v1/adaccounts/{id}/claim_media_by_ad_code | write | creatives | Claim media by ad code. |
| POST | v1/adaccounts/{id}/claim_media_by_snap_reference | write | creatives | Claim media by Snap reference. |
| POST | v1/adaccounts/{id}/combine_snaps | write | creatives | Combine snaps into media. |
| GET | v1/adaccounts/{id}/creatives | read | creatives | List creatives of an ad account. |
| POST | v1/adaccounts/{id}/creatives | write | creatives | Create creatives. |
| PUT | v1/adaccounts/{id}/creatives | write | creatives | Update creatives. |
| PUT | v1/adaccounts/{id}/creatives/{id} | write | creatives | Update a creative. |
| PATCH | v1/adaccounts/{id}/creatives/{id} | write | creatives | Partially update a creative. |
| POST | v1/adaccounts/{id}/get_creatives_by_ids | read | creatives | Get creatives by a list of IDs. |
| GET | v1/adaccounts/{id}/phone_numbers | read | creatives | List phone numbers usable in creatives. |
| GET | v1/creatives/{id} | read | creatives | Get a creative. |
| GET | v1/creatives/{id}/creative_preview | read | creatives | Get a preview link for a creative. |
| GET | v1/creatives/{id}/external_changelogs | read | creatives | List the change log of a creative. |
| GET | v1/creatives/{id}/snapcode | read | creatives | Get the Snapcode of a creative. |
| GET | v1/tools/extract_snap_id | read | creatives | Extract a Snap ID from a Snap link. |
| GET | v1/custom_conversions/{id} | read | custom conversions | Get a custom conversion. |
| GET | v1/adaccounts/{id}/dynamic_templates | read | dynamic templates | List dynamic templates of an ad account. |
| POST | v1/adaccounts/{id}/dynamic_templates | write | dynamic templates | Create a dynamic template. |
| PUT | v1/adaccounts/{id}/dynamic_templates | write | dynamic templates | Update a dynamic template. |
| GET | v1/dynamic_templates/{id} | read | dynamic templates | Get a dynamic template. |
| GET | v1/dynamic_templates/{id}/external_changelogs | read | dynamic templates | List the change log of a dynamic template. |
| GET | v1/adaccounts/{id}/event_details | read | event details | List event details of an ad account. |
| POST | v1/adaccounts/{id}/event_details | write | event details | Create event details. |
| GET | v1/event_details/{id} | read | event details | Get event details. |
| DELETE | v1/event_details/{id} | write | event details | Delete event details. |
| GET | v1/fundingsources/{id} | read | funding sources | Get a funding source. |
| GET | v1/organizations/{id}/fundingsources | read | funding sources | List funding sources of an organization. |
| GET | v1/adaccounts/{id}/interaction_zones | read | interaction zones | List interaction zones of an ad account. |
| POST | v1/adaccounts/{id}/interaction_zones | write | interaction zones | Create interaction zones. |
| GET | v1/interaction_zones/{id} | read | interaction zones | Get an interaction zone. |
| GET | v1/adaccounts/{id}/invoices | read | invoices | List invoices of an ad account. |
| GET | v1/adaccounts/{id}/invoices/{id} | read | invoices | Get an invoice. |
| GET | v1/adaccounts/{id}/lead_generation_forms | read | lead generation | List lead generation forms of an ad account. |
| GET | v1/lead_gen/forms/{id}/integrations | read | lead generation | List integrations of a lead generation form. |
| POST | v1/lead_gen/integrations/public_webhook | write | lead generation | Create a public webhook lead integration. |
| DELETE | v1/lead_gen/integrations/{id} | write | lead generation | Delete a lead generation integration. |
| GET | v1/lead_gen/integrations/{id}/test | write | lead generation | Test a lead generation integration. Kept out of read: it sends a test lead to the integration endpoint. |
| GET | v1/lead_generation_forms/{id} | read | lead generation | Get a lead generation form. |
| POST | v1/adaccounts/{id}/get_media_by_ids | read | media | Get media by a list of IDs. |
| GET | v1/adaccounts/{id}/media | read | media | List media of an ad account. |
| POST | v1/adaccounts/{id}/media | write | media | Create media. |
| POST | v1/adaccounts/{id}/media_copy | write | media | Copy media to another ad account. |
| PATCH | v1/media/ai_content_source | write | media | Update the AI content source of media. |
| GET | v1/media/{id} | read | media | Get media. |
| GET | v1/media/{id}/lens_preview | read | media | Get a lens preview of media. |
| POST | v1/media/{id}/multipart-upload-v2 | write | media | Upload a media file in parts. |
| GET | v1/media/{id}/preview | read | media | Get a preview of media. |
| GET | v1/media/{id}/thumbnail | read | media | Get the thumbnail of media. |
| POST | v1/media/{id}/upload | write | media | Upload a media file. |
| GET | v1/members/{id} | read | members | Get a member. |
| DELETE | v1/members/{id} | write | members | Remove a member. |
| GET | v1/organizations/{id}/members | read | members | List members of an organization. |
| POST | v1/organizations/{id}/members | write | members | Add a member to an organization. |
| POST | v1/mmm/reports | write | mmm reports | Request a marketing mix modeling report. |
| GET | v1/mmm/reports/{id} | read | mmm reports | Get the status of a marketing mix modeling report. |
| GET | v1/adaccounts/{id}/mobile_apps | read | mobile apps | List mobile apps of an ad account. |
| GET | v1/mobile_apps/{id} | read | mobile apps | Get a mobile app. |
| GET | v1/mobile_apps/{id}/campaign_eligibilities | read | mobile apps | Get campaign eligibilities of a mobile app. |
| GET | v1/mobile_apps/{id}/custom_conversions | read | mobile apps | List custom conversions of a mobile app. |
| GET | v1/mobile_apps/{id}/ecid_status | read | mobile apps | Get the ECID status of a mobile app. |
| GET | v1/mobile_apps/{id}/event_quality_scores | read | mobile apps | Get event quality scores of a mobile app. |
| GET | v1/mobile_apps/{id}/skadnetwork_adsquads | read | mobile apps | List SKAdNetwork ad squads of a mobile app. |
| GET | v1/organizations/{id}/mobile_apps | read | mobile apps | List mobile apps of an organization. |
| GET | v1/adaccounts/{id}/offer_disclaimers | read | offer disclaimers | List offer disclaimers of an ad account. |
| POST | v1/adaccounts/{id}/offer_disclaimers | write | offer disclaimers | Create an offer disclaimer. |
| GET | v1/adaccounts/{id}/offer_disclaimers/{id} | read | offer disclaimers | Get an offer disclaimer. |
| DELETE | v1/adaccounts/{id}/offer_disclaimers/{id} | write | offer disclaimers | Delete an offer disclaimer. |
| GET | v1/organizations/{id} | read | organizations | Get an organization. |
| GET | v1/adaccounts/{id}/pixels | read | pixels | List pixels of an ad account. |
| PUT | v1/adaccounts/{id}/pixels | write | pixels | Update a pixel. |
| GET | v1/organizations/{id}/pixels | read | pixels | List pixels of an organization. |
| PUT | v1/organizations/{id}/pixels | write | pixels | Create or update a pixel. |
| GET | v1/pixels/{id} | read | pixels | Get a pixel. |
| GET | v1/pixels/{id}/campaign_eligibilities | read | pixels | Get campaign eligibilities of a pixel. |
| GET | v1/pixels/{id}/custom_conversions | read | pixels | List custom conversions of a pixel. |
| GET | v1/pixels/{id}/domains/stats | read | pixels | Get domain stats of a pixel. |
| GET | v1/pixels/{id}/event_quality_scores | read | pixels | Get event quality scores of a pixel. |
| GET | v1/pixels/{id}/stats | read | pixels | Get stats of a pixel. |
| GET | v1/adaccounts/{id}/roles | read | roles | List roles of an ad account. |
| POST | v1/adaccounts/{id}/roles | write | roles | Create an ad account role. |
| PUT | v1/adaccounts/{id}/roles | write | roles | Update an ad account role. |
| GET | v1/catalogs/{id}/roles | read | roles | List roles of a catalog. |
| POST | v1/catalogs/{id}/roles | write | roles | Create a catalog role. |
| GET | v1/members/{id}/roles | read | roles | List roles of a member. |
| GET | v1/organizations/{id}/roles | read | roles | List roles of an organization. |
| POST | v1/organizations/{id}/roles | write | roles | Create an organization role. |
| DELETE | v1/roles/{id} | write | roles | Delete a role. |
| GET | v1/adaccounts/{id}/leads_report | read | stats | Fetch the status of an asynchronous lead generation report. |
| POST | v1/adaccounts/{id}/leads_report | write | stats | Start an asynchronous lead generation report. |
| GET | v1/adaccounts/{id}/stats | read | stats | Get stats for an ad account. |
| GET | v1/adaccounts/{id}/stats_report | read | stats | Fetch the status of an asynchronous ad account stats report. |
| GET | v1/ads/{id}/stats | read | stats | Get stats for an ad. |
| GET | v1/ads/{id}/stats_report | read | stats | Fetch the status of an asynchronous ad stats report. |
| GET | v1/adsquads/{id}/stats | read | stats | Get stats for an ad squad. |
| GET | v1/adsquads/{id}/stats_report | read | stats | Fetch the status of an asynchronous ad squad stats report. |
| GET | v1/campaigns/{id}/stats | read | stats | Get stats for a campaign. |
| GET | v1/campaigns/{id}/stats_report | read | stats | Fetch the status of an asynchronous campaign stats report. |
| GET | v1/creatives/{id}/stats | read | stats | Get stats for a creative. |
| GET | v1/media/{id}/stats | read | stats | Get stats for media. |
| GET | v1/adsquads/{id}/targeting_specs | read | targeting | Get the targeting spec of an ad squad. |
| PUT | v1/adsquads/{id}/targeting_specs | write | targeting | Update the targeting spec of an ad squad. |
| GET | v1/targeting/demographics/advanced_demographics | read | targeting | List advanced demographic targeting options. |
| GET | v1/targeting/demographics/age_group | read | targeting | List age group targeting options. |
| GET | v1/targeting/demographics/gender | read | targeting | List gender targeting options. |
| GET | v1/targeting/demographics/languages | read | targeting | List language targeting options. |
| GET | v1/targeting/device/carrier | read | targeting | List carrier targeting options. |
| GET | v1/targeting/device/connection_type | read | targeting | List connection type targeting options. |
| GET | v1/targeting/device/marketing_name | read | targeting | List device marketing name targeting options. |
| GET | v1/targeting/device/os_type | read | targeting | List OS type targeting options. |
| GET | v1/targeting/device/{id}/os_version | read | targeting | List OS version targeting options. |
| GET | v1/targeting/geo/country | read | targeting | List country targeting options. |
| GET | v1/targeting/geo/{id}/metro | read | targeting | List metro targeting options for a country. |
| GET | v1/targeting/geo/{id}/postal_code | read | targeting | List postal code targeting options for a country. |
| GET | v1/targeting/geo/{id}/region | read | targeting | List region targeting options for a country. |
| GET | v1/targeting/interests/dlxc | read | targeting | List DLX consumer interest targeting options. |
| GET | v1/targeting/interests/dlxp | read | targeting | List DLX purchase interest targeting options. |
| GET | v1/targeting/interests/dlxs | read | targeting | List DLX shopper interest targeting options. |
| GET | v1/targeting/interests/nln | read | targeting | List Nielsen interest targeting options. |
| GET | v1/targeting/location/categories_loi | read | targeting | List location category targeting options. |
| GET | v1/targeting/v1/interests/scls | read | targeting | List Snap lifestyle category targeting options. |
| GET | v1/targeting/v1/interests/shp | read | targeting | List shopping interest targeting options. |
| GET | v1/targeting/v1/interests/vac | read | targeting | List visitor audience category targeting options. |
| GET | v1/targeting/v1/options | read | targeting | List targeting options. |
| GET | v1/targeting_specs/{id} | read | targeting | Get a targeting spec. |
| GET | v1/organizations/{id}/transactions | read | transactions | List billing transactions of an organization. |
| GET | v1/me | read | user | Get the current user. |
| GET | v1/me/organizations | read | user | List organizations the user belongs to. |
| GET | v1/me/source_organizations | read | user | List organizations that shared entities with the user. |
