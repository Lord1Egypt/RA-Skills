# Systeme.io access policy

An access policy limits which endpoints Systeme.io connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/systeme#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Systeme.io: its 80 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create systeme --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/mailing/automation-emails"},
    {"method": "GET", "path": "api/mailing/automation-emails/{id}"},
    {"method": "GET", "path": "api/mailing/automation-emails/{id}/statistics"},
    {"method": "GET", "path": "api/mailing/automation-emails/{id}/statistics/recipients"},
    {"method": "GET", "path": "api/mailing/automation-emails-to-specific-address"},
    {"method": "GET", "path": "api/mailing/automation-emails-to-specific-address/{id}"},
    {"method": "GET", "path": "api/booking-calendar/bookings"},
    {"method": "GET", "path": "api/mailing/campaign-steps/{id}"},
    {"method": "GET", "path": "api/mailing/campaign-steps/{id}/statistics"},
    {"method": "GET", "path": "api/mailing/campaign-steps/{id}/statistics/recipients"},
    {"method": "GET", "path": "api/mailing/campaigns"},
    {"method": "GET", "path": "api/mailing/campaigns/{id}"},
    {"method": "GET", "path": "api/mailing/campaigns/{id}/steps"},
    {"method": "GET", "path": "api/community/communities"},
    {"method": "GET", "path": "api/community/communities/{id}"},
    {"method": "GET", "path": "api/community/communities/{id}/posts"},
    {"method": "GET", "path": "api/community/communities/{id}/topics"},
    {"method": "GET", "path": "api/contact_fields"},
    {"method": "GET", "path": "api/contacts"},
    {"method": "GET", "path": "api/contacts/{id}"},
    {"method": "GET", "path": "api/payment/coupons"},
    {"method": "GET", "path": "api/payment/coupons/{id}"},
    {"method": "GET", "path": "api/school/course-modules"},
    {"method": "GET", "path": "api/school/course-modules/{id}"},
    {"method": "GET", "path": "api/school/course-themes"},
    {"method": "GET", "path": "api/school/courses"},
    {"method": "GET", "path": "api/school/courses/{id}"},
    {"method": "GET", "path": "api/school/courses/{id}/modules-with-lectures"},
    {"method": "GET", "path": "api/payment/digital-products"},
    {"method": "GET", "path": "api/payment/digital-products/{id}"},
    {"method": "GET", "path": "api/domains"},
    {"method": "GET", "path": "api/school/enrollments"},
    {"method": "GET", "path": "api/booking-calendar/events"},
    {"method": "GET", "path": "api/booking-calendar/events/{id}"},
    {"method": "GET", "path": "api/files"},
    {"method": "GET", "path": "api/funnel-steps/{id}"},
    {"method": "GET", "path": "api/funnels"},
    {"method": "GET", "path": "api/funnels/steps"},
    {"method": "GET", "path": "api/funnels/{id}"},
    {"method": "GET", "path": "api/funnels/{id}/steps"},
    {"method": "GET", "path": "api/school/lectures/{id}"},
    {"method": "GET", "path": "api/community/memberships"},
    {"method": "GET", "path": "api/sms/message-services"},
    {"method": "GET", "path": "api/mailing/newsletters"},
    {"method": "GET", "path": "api/mailing/newsletters/{id}"},
    {"method": "GET", "path": "api/mailing/newsletters/{id}/excluded-tags"},
    {"method": "GET", "path": "api/mailing/newsletters/{id}/included-tags"},
    {"method": "GET", "path": "api/mailing/newsletters/{id}/schedule"},
    {"method": "GET", "path": "api/mailing/newsletters/{id}/statistics"},
    {"method": "GET", "path": "api/mailing/newsletters/{id}/statistics/recipients"},
    {"method": "GET", "path": "api/payment/offers/{id}"},
    {"method": "POST", "path": "api/page-editor/page-schema"},
    {"method": "POST", "path": "api/page-editor/page-template"},
    {"method": "GET", "path": "api/sms/phone-numbers"},
    {"method": "GET", "path": "api/payment/physical-products"},
    {"method": "GET", "path": "api/payment/physical-products/{id}"},
    {"method": "GET", "path": "api/community/posts/{id}"},
    {"method": "GET", "path": "api/payment/price-plans"},
    {"method": "GET", "path": "api/payment/price-plans/{id}"},
    {"method": "GET", "path": "api/automation/rules"},
    {"method": "GET", "path": "api/automation/rules/{id}"},
    {"method": "GET", "path": "api/payment/sale-settings/payment-methods/{id}"},
    {"method": "GET", "path": "api/payment/sale-settings/{id}"},
    {"method": "GET", "path": "api/mailing/statistics/automation-emails"},
    {"method": "GET", "path": "api/mailing/statistics/automation-emails/summary"},
    {"method": "GET", "path": "api/mailing/statistics/campaign-steps"},
    {"method": "GET", "path": "api/mailing/statistics/campaign-steps/summary"},
    {"method": "GET", "path": "api/mailing/statistics/newsletters"},
    {"method": "GET", "path": "api/mailing/statistics/newsletters/summary"},
    {"method": "GET", "path": "api/payment/subscriptions"},
    {"method": "GET", "path": "api/tags"},
    {"method": "GET", "path": "api/tags/{id}"},
    {"method": "GET", "path": "api/sms/templates"},
    {"method": "GET", "path": "api/sms/templates/{id}"},
    {"method": "GET", "path": "api/community/topics/{id}"},
    {"method": "GET", "path": "api/booking-calendar/user-availability"},
    {"method": "GET", "path": "api/webhooks"},
    {"method": "GET", "path": "api/webhooks/{id}"},
    {"method": "GET", "path": "api/workflows/{id}/steps"},
    {"method": "GET", "path": "api/workspace/members"}
  ],
  "deny": []
}
```

## Endpoints

The Systeme.io endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/mailing/automation-emails | read | automation_emails | Retrieves the collection of AutomationEmail resources. |
| POST | api/mailing/automation-emails | write | automation_emails | Creates a AutomationEmail resource. |
| GET | api/mailing/automation-emails/{id} | read | automation_emails | Retrieves a AutomationEmail resource. |
| PATCH | api/mailing/automation-emails/{id} | write | automation_emails | Updates the AutomationEmail resource. |
| GET | api/mailing/automation-emails/{id}/statistics | read | automation_emails | [Beta] Retrieves a AutomationEmail resource. |
| GET | api/mailing/automation-emails/{id}/statistics/recipients | read | automation_emails | List automation email recipient statistics. |
| GET | api/mailing/automation-emails-to-specific-address | read | automation_emails_to_specific_address | Retrieves the collection of AutomationEmailToSpecificAddress resources. |
| POST | api/mailing/automation-emails-to-specific-address | write | automation_emails_to_specific_address | Creates a AutomationEmailToSpecificAddress resource. |
| GET | api/mailing/automation-emails-to-specific-address/{id} | read | automation_emails_to_specific_address | Retrieves a AutomationEmailToSpecificAddress resource. |
| PATCH | api/mailing/automation-emails-to-specific-address/{id} | write | automation_emails_to_specific_address | Updates the AutomationEmailToSpecificAddress resource. |
| GET | api/booking-calendar/bookings | read | bookings | Retrieves the collection of Booking resources. |
| GET | api/mailing/campaign-steps/{id} | read | campaign_steps | Retrieves a CampaignStep resource. |
| PATCH | api/mailing/campaign-steps/{id} | write | campaign_steps | Updates the CampaignStep resource. |
| DELETE | api/mailing/campaign-steps/{id} | write | campaign_steps | Removes the CampaignStep resource. |
| POST | api/mailing/campaign-steps/{id}/send-test | write | campaign_steps | Sends a test email of a campaign step. |
| GET | api/mailing/campaign-steps/{id}/statistics | read | campaign_steps | [Beta] Retrieves a CampaignStep resource. |
| GET | api/mailing/campaign-steps/{id}/statistics/recipients | read | campaign_steps | List campaign step recipient statistics. |
| GET | api/mailing/campaigns | read | campaigns | Retrieves the collection of Campaign resources. |
| POST | api/mailing/campaigns | write | campaigns | Creates a Campaign resource. |
| GET | api/mailing/campaigns/{id} | read | campaigns | Retrieves a Campaign resource. |
| PATCH | api/mailing/campaigns/{id} | write | campaigns | Updates the Campaign resource. |
| DELETE | api/mailing/campaigns/{id} | write | campaigns | Removes the Campaign resource. |
| GET | api/mailing/campaigns/{id}/steps | read | campaigns | Retrieves the collection of CampaignStep resources. |
| POST | api/mailing/campaigns/{id}/steps | write | campaigns | Creates a CampaignStep resource. |
| GET | api/community/communities | read | communities | Retrieves the collection of Community resources. |
| POST | api/community/communities | write | communities | Creates a Community resource. |
| GET | api/community/communities/{id} | read | communities | Retrieves a Community resource. |
| PATCH | api/community/communities/{id} | write | communities | Updates the Community resource. |
| DELETE | api/community/communities/{id} | write | communities | Removes the Community resource. |
| POST | api/community/communities/{id}/memberships | write | communities | Creates a Membership resource. |
| GET | api/community/communities/{id}/posts | read | communities | [Beta] Returns the posts of a community. |
| GET | api/community/communities/{id}/topics | read | communities | Retrieves the collection of Topic resources. |
| POST | api/community/communities/{id}/topics | write | communities | Creates a Topic resource. |
| GET | api/contact_fields | read | contact_fields | Retrieves the collection of ContactField resources. |
| POST | api/contact_fields | write | contact_fields | Creates a ContactField resource. |
| PATCH | api/contact_fields/{id} | write | contact_fields | Updates the ContactField resource. |
| DELETE | api/contact_fields/{id} | write | contact_fields | Removes the ContactField resource. |
| GET | api/contacts | read | contacts | Retrieves the collection of Contact resources. |
| POST | api/contacts | write | contacts | Creates a Contact resource. |
| GET | api/contacts/{id} | read | contacts | Retrieves a Contact resource. |
| PATCH | api/contacts/{id} | write | contacts | Updates the Contact resource. |
| DELETE | api/contacts/{id} | write | contacts | Removes the Contact resource. |
| POST | api/contacts/{id}/tags | write | contacts | Assigns a Tag to a Contact. |
| DELETE | api/contacts/{id}/tags/{id} | write | contacts | Removes a Tag from a Contact. |
| GET | api/payment/coupons | read | coupons | Retrieves the collection of Coupon resources. |
| POST | api/payment/coupons | write | coupons | Creates a Coupon resource. |
| GET | api/payment/coupons/{id} | read | coupons | Retrieves a Coupon resource. |
| PUT | api/payment/coupons/{id} | write | coupons | This endpoint is deprecated. Use PATCH instead. |
| PATCH | api/payment/coupons/{id} | write | coupons | Updates the Coupon resource. |
| DELETE | api/payment/coupons/{id} | write | coupons | Removes the Coupon resource. |
| GET | api/school/course-modules | read | course_modules | Retrieves the collection of Module resources. |
| GET | api/school/course-modules/{id} | read | course_modules | Retrieves a Module resource. |
| PATCH | api/school/course-modules/{id} | write | course_modules | Updates the Module resource. |
| DELETE | api/school/course-modules/{id} | write | course_modules | Removes the Module resource. |
| GET | api/school/course-themes | read | course_themes | Retrieves the collection of CourseTheme resources. |
| GET | api/school/courses | read | courses | Retrieves the collection of Course resources. |
| POST | api/school/courses/classic | write | courses | Creates a Course resource. |
| GET | api/school/courses/{id} | read | courses | Retrieves a Course resource. |
| PATCH | api/school/courses/{id} | write | courses | Updates the Course resource. |
| DELETE | api/school/courses/{id} | write | courses | Removes the Course resource. |
| POST | api/school/courses/{id}/activate | write | courses | Activates a course. |
| POST | api/school/courses/{id}/deactivate | write | courses | Deactivates a course. |
| POST | api/school/courses/{id}/enrollments | write | courses | Creates an enrollment in a course. |
| POST | api/school/courses/{id}/modules | write | courses | Creates a Module resource. |
| GET | api/school/courses/{id}/modules-with-lectures | read | courses | Retrieves the collection of CourseModulesWithLectures resources. |
| GET | api/payment/digital-products | read | digital_products | Retrieves the collection of DigitalProduct resources. |
| POST | api/payment/digital-products | write | digital_products | Creates a DigitalProduct resource. |
| GET | api/payment/digital-products/{id} | read | digital_products | Retrieves a DigitalProduct resource. |
| PATCH | api/payment/digital-products/{id} | write | digital_products | Updates the DigitalProduct resource. |
| DELETE | api/payment/digital-products/{id} | write | digital_products | Removes the DigitalProduct resource. |
| GET | api/domains | read | domains | Retrieves the collection of Domain resources. |
| GET | api/school/enrollments | read | enrollments | Retrieves the collection of Enrollment resources. |
| DELETE | api/school/enrollments/{id} | write | enrollments | Removes the Enrollment resource. |
| GET | api/booking-calendar/events | read | events | Retrieves the collection of Event resources. |
| POST | api/booking-calendar/events | write | events | Creates a CalendarEvent resource. |
| GET | api/booking-calendar/events/{id} | read | events | Retrieves a CalendarEvent resource. |
| PATCH | api/booking-calendar/events/{id} | write | events | Updates the CalendarEvent resource. |
| DELETE | api/booking-calendar/events/{id} | write | events | Removes the CalendarEvent resource. |
| POST | api/automation/feature-flag-field-pilot | write | feature_flag_field_pilot | Creates a feature flag field pilot. |
| POST | api/automation/feature-flag-field-pilot/control | write | feature_flag_field_pilot | Creates a feature flag field pilot control. |
| GET | api/files | read | files | Retrieves the collection of File resources. |
| GET | api/funnel-steps/{id} | read | funnel-steps | Retrieves a FunnelStep resource. |
| POST | api/funnel-steps/{id}/change-position | write | funnel-steps | [Beta] Moves a funnel step to a new position. |
| GET | api/funnels | read | funnels | Retrieves the collection of Funnel resources. |
| POST | api/funnels | write | funnels | Creates a Funnel resource. |
| GET | api/funnels/steps | read | funnels | Retrieves the collection of FunnelStepSearchResult resources. |
| GET | api/funnels/{id} | read | funnels | Retrieves a Funnel resource. |
| GET | api/funnels/{id}/steps | read | funnels | Retrieves the collection of FunnelStep resources. |
| POST | api/funnels/{id}/steps | write | funnels | Creates a FunnelStep resource. |
| GET | api/school/lectures/{id} | read | lectures | Retrieves a Lecture resource. |
| PATCH | api/school/lectures/{id} | write | lectures | Updates the Lecture resource. |
| DELETE | api/school/lectures/{id} | write | lectures | Removes the Lecture resource. |
| POST | api/school/lectures/{id}/activate | write | lectures | Activates a lecture. |
| POST | api/school/lectures/{id}/deactivate | write | lectures | Deactivates a lecture. |
| GET | api/community/memberships | read | memberships | Retrieves the collection of Membership resources. |
| DELETE | api/community/memberships/{id} | write | memberships | Removes the Membership resource. |
| GET | api/sms/message-services | read | message_services | Retrieves the collection of SmsMessageService resources. |
| POST | api/school/modules/{id}/classic-lectures | write | modules | Creates a Lecture resource. |
| GET | api/mailing/newsletters | read | newsletters | Retrieves the collection of Newsletter resources. |
| POST | api/mailing/newsletters | write | newsletters | Creates a Newsletter resource. |
| GET | api/mailing/newsletters/{id} | read | newsletters | Retrieves a Newsletter resource. |
| PUT | api/mailing/newsletters/{id} | write | newsletters | This endpoint is deprecated. Use PATCH instead. |
| PATCH | api/mailing/newsletters/{id} | write | newsletters | Updates the Newsletter resource. |
| DELETE | api/mailing/newsletters/{id} | write | newsletters | Removes the Newsletter resource. |
| GET | api/mailing/newsletters/{id}/excluded-tags | read | newsletters | Retrieves the collection of MailingTag resources. |
| PUT | api/mailing/newsletters/{id}/excluded-tags | write | newsletters | Replaces the MailingTag resource. |
| GET | api/mailing/newsletters/{id}/included-tags | read | newsletters | Retrieves the collection of MailingTag resources. |
| PUT | api/mailing/newsletters/{id}/included-tags | write | newsletters | Replaces the MailingTag resource. |
| GET | api/mailing/newsletters/{id}/schedule | read | newsletters | Retrieves a NewsletterSchedule resource. |
| PUT | api/mailing/newsletters/{id}/schedule | write | newsletters | Replaces the NewsletterSchedule resource. |
| POST | api/mailing/newsletters/{id}/send | write | newsletters | Sends a newsletter. |
| POST | api/mailing/newsletters/{id}/send-test | write | newsletters | Sends a test email of a newsletter. |
| GET | api/mailing/newsletters/{id}/statistics | read | newsletters | [Beta] Retrieves a Newsletter resource. |
| GET | api/mailing/newsletters/{id}/statistics/recipients | read | newsletters | List newsletter recipient statistics. |
| POST | api/payment/offers | write | offers | Creates a Offer resource. |
| GET | api/payment/offers/{id} | read | offers | Retrieves a Offer resource. |
| PATCH | api/payment/offers/{id} | write | offers | Updates the Offer resource. |
| POST | api/page-editor/page-schema | read | page_schema | Returns a Page JSON Schema. |
| POST | api/page-editor/page-template | read | page_template | [Beta] Returns a page template description. |
| PUT | api/page-editor/pages/{id}/save | write | pages | Replaces the PageContentSave resource. |
| PUT | api/pages/{id}/content/from-template | write | pages | [Beta] Replaces page content from a template. |
| GET | api/sms/phone-numbers | read | phone_numbers | Retrieves a SmsPhoneNumbers resource. |
| GET | api/payment/physical-products | read | physical_products | Retrieves the collection of PhysicalProduct resources. |
| POST | api/payment/physical-products | write | physical_products | Creates a PhysicalProduct resource. |
| GET | api/payment/physical-products/{id} | read | physical_products | Retrieves a PhysicalProduct resource. |
| PATCH | api/payment/physical-products/{id} | write | physical_products | Updates the PhysicalProduct resource. |
| DELETE | api/payment/physical-products/{id} | write | physical_products | Removes the PhysicalProduct resource. |
| GET | api/community/posts/{id} | read | posts | [Beta] Returns a community post. |
| GET | api/payment/price-plans | read | price_plans | Retrieves the collection of PricePlan resources. |
| POST | api/payment/price-plans | write | price_plans | Creates a PricePlan resource. |
| GET | api/payment/price-plans/{id} | read | price_plans | Retrieves a PricePlan resource. |
| PATCH | api/payment/price-plans/{id} | write | price_plans | Updates the PricePlan resource. |
| DELETE | api/payment/price-plans/{id} | write | price_plans | Removes the PricePlan resource. |
| GET | api/automation/rules | read | rules | Retrieves the collection of AutomationRule resources. |
| POST | api/automation/rules | write | rules | Creates a AutomationRule resource. |
| GET | api/automation/rules/{id} | read | rules | Retrieves a AutomationRule resource. |
| PATCH | api/automation/rules/{id} | write | rules | Updates the AutomationRule resource. |
| DELETE | api/automation/rules/{id} | write | rules | Removes the AutomationRule resource. |
| GET | api/payment/sale-settings/payment-methods/{id} | read | sale_settings | Retrieves a AvailablePaymentMethods resource. |
| GET | api/payment/sale-settings/{id} | read | sale_settings | Retrieves a SaleSettings resource. |
| PATCH | api/payment/sale-settings/{id} | write | sale_settings | Updates the SaleSettings resource. |
| GET | api/mailing/statistics/automation-emails | read | statistics | [Beta] Retrieves the collection of AutomationEmailStatisticsListItem resources. |
| GET | api/mailing/statistics/automation-emails/summary | read | statistics | [Beta] Retrieve automation email statistics overview. |
| GET | api/mailing/statistics/campaign-steps | read | statistics | [Beta] Retrieves the collection of CampaignStepStatisticsListItem resources. |
| GET | api/mailing/statistics/campaign-steps/summary | read | statistics | [Beta] Retrieve campaign step statistics overview. |
| GET | api/mailing/statistics/newsletters | read | statistics | [Beta] Retrieves the collection of NewsletterStatisticsListItem resources. |
| GET | api/mailing/statistics/newsletters/summary | read | statistics | [Beta] Retrieve newsletter statistics overview. |
| GET | api/payment/subscriptions | read | subscriptions | Retrieves the collection of Subscription resources. |
| POST | api/payment/subscriptions/{id}/cancel | write | subscriptions | Cancels a subscription. |
| GET | api/tags | read | tags | Retrieves the collection of Tag resources. |
| POST | api/tags | write | tags | Creates a Tag resource. |
| GET | api/tags/{id} | read | tags | Retrieves a Tag resource. |
| PUT | api/tags/{id} | write | tags | Replaces the Tag resource. |
| DELETE | api/tags/{id} | write | tags | Removes the Tag resource. |
| GET | api/sms/templates | read | templates | Retrieves the collection of SmsTemplate resources. |
| POST | api/sms/templates | write | templates | Creates a SmsTemplate resource. |
| GET | api/sms/templates/{id} | read | templates | Retrieves a SmsTemplate resource. |
| PATCH | api/sms/templates/{id} | write | templates | Updates the SmsTemplate resource. |
| DELETE | api/sms/templates/{id} | write | templates | Removes the SmsTemplate resource. |
| GET | api/community/topics/{id} | read | topics | Retrieves a Topic resource. |
| PATCH | api/community/topics/{id} | write | topics | Updates the Topic resource. |
| DELETE | api/community/topics/{id} | write | topics | Removes the Topic resource. |
| GET | api/sms/twilio-account | write | twilio_account | Retrieves a SmsTwilioAccount resource. Kept out of read: may return Twilio credentials. |
| GET | api/booking-calendar/user-availability | read | user_availability | Retrieves a UserAvailability resource. |
| POST | api/booking-calendar/user-availability | write | user_availability | Creates a UserAvailability resource. |
| PATCH | api/booking-calendar/user-availability | write | user_availability | Updates the UserAvailability resource. |
| GET | api/webhooks | read | webhooks | Retrieves the collection of Webhook resources. |
| POST | api/webhooks | write | webhooks | Creates a Webhook resource. |
| GET | api/webhooks/{id} | read | webhooks | Retrieves a Webhook resource. |
| PATCH | api/webhooks/{id} | write | webhooks | Updates the Webhook resource. |
| DELETE | api/webhooks/{id} | write | webhooks | Removes the Webhook resource. |
| PUT | api/workflow-steps/{id} | write | workflow-steps | [Beta] Replaces a workflow step configuration. |
| DELETE | api/workflow-steps/{id} | write | workflow-steps | [Beta] Deletes a workflow step. |
| GET | api/workflows/{id}/steps | read | workflows | [Beta] Retrieves workflow steps. |
| POST | api/workflows/{id}/steps | write | workflows | [Beta] Creates a workflow step. |
| GET | api/workspace/members | read | workspace | Retrieves the collection of WorkspaceMember resources. |
