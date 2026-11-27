# Trello access policy

An access policy limits which endpoints Trello connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/trello#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Trello: its 125 read-only endpoints, plus deny rules for the 1 write endpoint a read rule would otherwise match. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create trello --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "1/actions/{id}"},
    {"method": "GET", "path": "1/actions/{id}/board"},
    {"method": "GET", "path": "1/actions/{id}/card"},
    {"method": "GET", "path": "1/actions/{id}/list"},
    {"method": "GET", "path": "1/actions/{id}/member"},
    {"method": "GET", "path": "1/actions/{id}/memberCreator"},
    {"method": "GET", "path": "1/actions/{id}/organization"},
    {"method": "GET", "path": "1/actions/{id}/reactions"},
    {"method": "GET", "path": "1/actions/{id}/reactions/{id}"},
    {"method": "GET", "path": "1/actions/{id}/reactionsSummary"},
    {"method": "GET", "path": "1/actions/{id}/{id}"},
    {"method": "GET", "path": "1/applications/{id}/compliance"},
    {"method": "GET", "path": "1/batch"},
    {"method": "GET", "path": "1/boards/{id}"},
    {"method": "GET", "path": "1/boards/{id}/actions"},
    {"method": "GET", "path": "1/boards/{id}/boardPlugins"},
    {"method": "GET", "path": "1/boards/{id}/boardStars"},
    {"method": "GET", "path": "1/boards/{id}/cards"},
    {"method": "GET", "path": "1/boards/{id}/cards/{id}"},
    {"method": "GET", "path": "1/boards/{id}/checklists"},
    {"method": "GET", "path": "1/boards/{id}/customFields"},
    {"method": "GET", "path": "1/boards/{id}/exports/mostRecent"},
    {"method": "GET", "path": "1/boards/{id}/exports/{id}"},
    {"method": "GET", "path": "1/boards/{id}/exports/{id}/download"},
    {"method": "GET", "path": "1/boards/{id}/labels"},
    {"method": "GET", "path": "1/boards/{id}/lists"},
    {"method": "GET", "path": "1/boards/{id}/lists/{id}"},
    {"method": "GET", "path": "1/boards/{id}/members"},
    {"method": "GET", "path": "1/boards/{id}/memberships"},
    {"method": "GET", "path": "1/boards/{id}/plugins"},
    {"method": "GET", "path": "1/boards/{id}/{id}"},
    {"method": "GET", "path": "1/cards/{id}"},
    {"method": "GET", "path": "1/cards/{id}/actions"},
    {"method": "GET", "path": "1/cards/{id}/attachments"},
    {"method": "GET", "path": "1/cards/{id}/attachments/{id}"},
    {"method": "GET", "path": "1/cards/{id}/board"},
    {"method": "GET", "path": "1/cards/{id}/checkItem/{id}"},
    {"method": "GET", "path": "1/cards/{id}/checkItemStates"},
    {"method": "GET", "path": "1/cards/{id}/checklists"},
    {"method": "GET", "path": "1/cards/{id}/customFieldItems"},
    {"method": "GET", "path": "1/cards/{id}/list"},
    {"method": "GET", "path": "1/cards/{id}/members"},
    {"method": "GET", "path": "1/cards/{id}/membersVoted"},
    {"method": "GET", "path": "1/cards/{id}/pluginData"},
    {"method": "GET", "path": "1/cards/{id}/stickers"},
    {"method": "GET", "path": "1/cards/{id}/stickers/{id}"},
    {"method": "GET", "path": "1/cards/{id}/{id}"},
    {"method": "GET", "path": "1/checklists/{id}"},
    {"method": "GET", "path": "1/checklists/{id}/board"},
    {"method": "GET", "path": "1/checklists/{id}/cards"},
    {"method": "GET", "path": "1/checklists/{id}/checkItems"},
    {"method": "GET", "path": "1/checklists/{id}/checkItems/{id}"},
    {"method": "GET", "path": "1/checklists/{id}/{id}"},
    {"method": "GET", "path": "1/customFields/{id}"},
    {"method": "GET", "path": "1/customFields/{id}/options"},
    {"method": "GET", "path": "1/customFields/{id}/options/{id}"},
    {"method": "GET", "path": "1/emoji"},
    {"method": "GET", "path": "1/enterprises/{id}"},
    {"method": "GET", "path": "1/enterprises/{id}/admins"},
    {"method": "GET", "path": "1/enterprises/{id}/auditlog"},
    {"method": "GET", "path": "1/enterprises/{id}/claimableOrganizations"},
    {"method": "GET", "path": "1/enterprises/{id}/members"},
    {"method": "GET", "path": "1/enterprises/{id}/members/query"},
    {"method": "GET", "path": "1/enterprises/{id}/members/{id}"},
    {"method": "GET", "path": "1/enterprises/{id}/organizations"},
    {"method": "GET", "path": "1/enterprises/{id}/pendingOrganizations"},
    {"method": "GET", "path": "1/enterprises/{id}/signupUrl"},
    {"method": "GET", "path": "1/enterprises/{id}/transferrable/bulk/{id}"},
    {"method": "GET", "path": "1/enterprises/{id}/transferrable/organization/{id}"},
    {"method": "GET", "path": "1/labels/{id}"},
    {"method": "GET", "path": "1/lists/{id}"},
    {"method": "GET", "path": "1/lists/{id}/actions"},
    {"method": "GET", "path": "1/lists/{id}/board"},
    {"method": "GET", "path": "1/lists/{id}/cards"},
    {"method": "GET", "path": "1/members/{id}"},
    {"method": "GET", "path": "1/members/{id}/actions"},
    {"method": "GET", "path": "1/members/{id}/boardBackgrounds"},
    {"method": "GET", "path": "1/members/{id}/boardBackgrounds/{id}"},
    {"method": "GET", "path": "1/members/{id}/boardStars"},
    {"method": "GET", "path": "1/members/{id}/boardStars/{id}"},
    {"method": "GET", "path": "1/members/{id}/boards"},
    {"method": "GET", "path": "1/members/{id}/boardsInvited"},
    {"method": "GET", "path": "1/members/{id}/cards"},
    {"method": "GET", "path": "1/members/{id}/customBoardBackgrounds"},
    {"method": "GET", "path": "1/members/{id}/customBoardBackgrounds/{id}"},
    {"method": "GET", "path": "1/members/{id}/customEmoji"},
    {"method": "GET", "path": "1/members/{id}/customEmoji/{id}"},
    {"method": "GET", "path": "1/members/{id}/customStickers"},
    {"method": "GET", "path": "1/members/{id}/customStickers/{id}"},
    {"method": "GET", "path": "1/members/{id}/notificationChannelSettings"},
    {"method": "GET", "path": "1/members/{id}/notificationChannelSettings/{id}"},
    {"method": "GET", "path": "1/members/{id}/notifications"},
    {"method": "GET", "path": "1/members/{id}/organizations"},
    {"method": "GET", "path": "1/members/{id}/organizationsInvited"},
    {"method": "GET", "path": "1/members/{id}/savedSearches"},
    {"method": "GET", "path": "1/members/{id}/savedSearches/{id}"},
    {"method": "GET", "path": "1/members/{id}/{id}"},
    {"method": "GET", "path": "1/notifications/{id}"},
    {"method": "GET", "path": "1/notifications/{id}/board"},
    {"method": "GET", "path": "1/notifications/{id}/card"},
    {"method": "GET", "path": "1/notifications/{id}/list"},
    {"method": "GET", "path": "1/notifications/{id}/member"},
    {"method": "GET", "path": "1/notifications/{id}/memberCreator"},
    {"method": "GET", "path": "1/notifications/{id}/organization"},
    {"method": "GET", "path": "1/notifications/{id}/{id}"},
    {"method": "GET", "path": "1/organizations/{id}"},
    {"method": "GET", "path": "1/organizations/{id}/actions"},
    {"method": "GET", "path": "1/organizations/{id}/boards"},
    {"method": "GET", "path": "1/organizations/{id}/exports"},
    {"method": "GET", "path": "1/organizations/{id}/members"},
    {"method": "GET", "path": "1/organizations/{id}/memberships"},
    {"method": "GET", "path": "1/organizations/{id}/memberships/{id}"},
    {"method": "GET", "path": "1/organizations/{id}/newBillableGuests/{id}"},
    {"method": "GET", "path": "1/organizations/{id}/pluginData"},
    {"method": "GET", "path": "1/organizations/{id}/tags"},
    {"method": "GET", "path": "1/organizations/{id}/{id}"},
    {"method": "GET", "path": "1/plugins/{id}"},
    {"method": "GET", "path": "1/plugins/{id}/compliance/memberPrivacy"},
    {"method": "GET", "path": "1/search"},
    {"method": "GET", "path": "1/search/members"},
    {"method": "GET", "path": "1/tokens/{id}/member"},
    {"method": "GET", "path": "1/tokens/{id}/webhooks"},
    {"method": "GET", "path": "1/tokens/{id}/webhooks/{id}"},
    {"method": "GET", "path": "1/webhooks/{id}"},
    {"method": "GET", "path": "1/webhooks/{id}/{id}"}
  ],
  "deny": [
    {"method": "GET", "path": "1/members/{id}/tokens"}
  ]
}
```

## Endpoints

The Trello endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | 1/actions/{id} | read | actions | Get an Action. |
| PUT | 1/actions/{id} | write | actions | Update an Action. |
| DELETE | 1/actions/{id} | write | actions | Delete an Action. |
| GET | 1/actions/{id}/board | read | actions | Get the Board for an Action. |
| GET | 1/actions/{id}/card | read | actions | Get the Card for an Action. |
| GET | 1/actions/{id}/list | read | actions | Get the List for an Action. |
| GET | 1/actions/{id}/member | read | actions | Get the Member of an Action. |
| GET | 1/actions/{id}/memberCreator | read | actions | Get the Member Creator of an Action. |
| GET | 1/actions/{id}/organization | read | actions | Get the Organization of an Action. |
| GET | 1/actions/{id}/reactions | read | actions | Get Action's Reactions. |
| POST | 1/actions/{id}/reactions | write | actions | Create Reaction for Action. |
| GET | 1/actions/{id}/reactions/{id} | read | actions | Get Action's Reaction. |
| DELETE | 1/actions/{id}/reactions/{id} | write | actions | Delete Action's Reaction. |
| GET | 1/actions/{id}/reactionsSummary | read | actions | List Action's summary of Reactions. |
| PUT | 1/actions/{id}/text | write | actions | Update a Comment Action. |
| GET | 1/actions/{id}/{id} | read | actions | Get a specific field on an Action. |
| GET | 1/applications/{id}/compliance | read | applications | Get Application's compliance data. |
| GET | 1/batch | read | batch | Batch Requests. |
| POST | 1/boards | write | boards | Create a Board. |
| GET | 1/boards/{id} | read | boards | Get a Board. |
| PUT | 1/boards/{id} | write | boards | Update a Board. |
| DELETE | 1/boards/{id} | write | boards | Delete a Board. |
| GET | 1/boards/{id}/actions | read | boards | Get Actions of a Board. |
| GET | 1/boards/{id}/boardPlugins | read | boards | Get Enabled Power-Ups on Board. |
| POST | 1/boards/{id}/boardPlugins | write | boards | Enable a Power-Up on a Board. |
| DELETE | 1/boards/{id}/boardPlugins/{id} | write | boards | Disable a Power-Up on a Board. |
| GET | 1/boards/{id}/boardStars | read | boards | Get boardStars on a Board. |
| POST | 1/boards/{id}/calendarKey/generate | write | boards | Create a calendarKey for a Board. |
| GET | 1/boards/{id}/cards | read | boards | Get Cards on a Board. |
| GET | 1/boards/{id}/cards/{id} | read | boards | Get filtered Cards on a Board. |
| GET | 1/boards/{id}/checklists | read | boards | Get Checklists on a Board. |
| GET | 1/boards/{id}/customFields | read | boards | Get Custom Fields for Board. |
| POST | 1/boards/{id}/emailKey/generate | write | boards | Create a emailKey for a Board. |
| POST | 1/boards/{id}/exports | write | boards | Create an Export for a Board. |
| GET | 1/boards/{id}/exports/mostRecent | read | boards | Get a Board's Most Recent Export. |
| GET | 1/boards/{id}/exports/{id} | read | boards | Get an Export for a Board. |
| DELETE | 1/boards/{id}/exports/{id} | write | boards | Delete an Export for a Board. |
| GET | 1/boards/{id}/exports/{id}/download | read | boards | Download an Export for a Board. |
| POST | 1/boards/{id}/idTags | write | boards | Create a Tag for a Board. |
| GET | 1/boards/{id}/labels | read | boards | Get Labels on a Board. |
| POST | 1/boards/{id}/labels | write | boards | Create a Label on a Board. |
| GET | 1/boards/{id}/lists | read | boards | Get Lists on a Board. |
| POST | 1/boards/{id}/lists | write | boards | Create a List on a Board. |
| GET | 1/boards/{id}/lists/{id} | read | boards | Get filtered Lists on a Board. |
| POST | 1/boards/{id}/markAsViewed | write | boards | Mark Board as viewed. |
| GET | 1/boards/{id}/members | read | boards | Get the Members of a Board. |
| PUT | 1/boards/{id}/members | write | boards | Invite Member to Board via email. |
| PUT | 1/boards/{id}/members/{id} | write | boards | Add a Member to a Board. |
| DELETE | 1/boards/{id}/members/{id} | write | boards | Remove Member from Board. |
| GET | 1/boards/{id}/memberships | read | boards | Get Memberships of a Board. |
| PUT | 1/boards/{id}/memberships/{id} | write | boards | Update Membership of Member on a Board. |
| PUT | 1/boards/{id}/myPrefs/emailPosition | write | boards | Update emailPosition Pref on a Board. |
| PUT | 1/boards/{id}/myPrefs/idEmailList | write | boards | Update idEmailList Pref on a Board. |
| PUT | 1/boards/{id}/myPrefs/showSidebar | write | boards | Update showSidebar Pref on a Board. |
| PUT | 1/boards/{id}/myPrefs/showSidebarActivity | write | boards | Update showSidebarActivity Pref on a Board. |
| PUT | 1/boards/{id}/myPrefs/showSidebarBoardActions | write | boards | Update showSidebarBoardActions Pref on a Board. |
| PUT | 1/boards/{id}/myPrefs/showSidebarMembers | write | boards | Update showSidebarMembers Pref on a Board. |
| GET | 1/boards/{id}/plugins | read | boards | Get Power-Ups on a Board. |
| GET | 1/boards/{id}/{id} | read | boards | Get a field on a Board. |
| POST | 1/cards | write | cards | Create a new Card. |
| GET | 1/cards/{id} | read | cards | Get a Card. |
| PUT | 1/cards/{id} | write | cards | Update a Card. |
| DELETE | 1/cards/{id} | write | cards | Delete a Card. |
| GET | 1/cards/{id}/actions | read | cards | Get Actions on a Card. |
| POST | 1/cards/{id}/actions/comments | write | cards | Add a new comment to a Card. |
| PUT | 1/cards/{id}/actions/{id}/comments | write | cards | Update Comment Action on a Card. |
| DELETE | 1/cards/{id}/actions/{id}/comments | write | cards | Delete a comment on a Card. |
| GET | 1/cards/{id}/attachments | read | cards | Get Attachments on a Card. |
| POST | 1/cards/{id}/attachments | write | cards | Create Attachment On Card. |
| GET | 1/cards/{id}/attachments/{id} | read | cards | Get an Attachment on a Card. |
| DELETE | 1/cards/{id}/attachments/{id} | write | cards | Delete an Attachment on a Card. |
| GET | 1/cards/{id}/board | read | cards | Get the Board the Card is on. |
| GET | 1/cards/{id}/checkItem/{id} | read | cards | Get checkItem on a Card. |
| PUT | 1/cards/{id}/checkItem/{id} | write | cards | Update a checkItem on a Card. |
| DELETE | 1/cards/{id}/checkItem/{id} | write | cards | Delete checkItem on a Card. |
| GET | 1/cards/{id}/checkItemStates | read | cards | Get checkItems on a Card. |
| PUT | 1/cards/{id}/checklist/{id}/checkItem/{id} | write | cards | Update Checkitem on Checklist on Card. |
| GET | 1/cards/{id}/checklists | read | cards | Get Checklists on a Card. |
| POST | 1/cards/{id}/checklists | write | cards | Create Checklist on a Card. |
| DELETE | 1/cards/{id}/checklists/{id} | write | cards | Delete a Checklist on a Card. |
| PUT | 1/cards/{id}/customField/{id}/item | write | cards | Update Custom Field item on Card. |
| GET | 1/cards/{id}/customFieldItems | read | cards | Get Custom Field Items for a Card. |
| PUT | 1/cards/{id}/customFields | write | cards | Update Multiple Custom Field items on Card. |
| POST | 1/cards/{id}/idLabels | write | cards | Add a Label to a Card. |
| DELETE | 1/cards/{id}/idLabels/{id} | write | cards | Remove a Label from a Card. |
| POST | 1/cards/{id}/idMembers | write | cards | Add a Member to a Card. |
| DELETE | 1/cards/{id}/idMembers/{id} | write | cards | Remove a Member from a Card. |
| POST | 1/cards/{id}/labels | write | cards | Create a new Label on a Card. |
| GET | 1/cards/{id}/list | read | cards | Get the List of a Card. |
| POST | 1/cards/{id}/markAssociatedNotificationsRead | write | cards | Mark a Card's Notifications as read. |
| GET | 1/cards/{id}/members | read | cards | Get the Members of a Card. |
| GET | 1/cards/{id}/membersVoted | read | cards | Get Members who have voted on a Card. |
| POST | 1/cards/{id}/membersVoted | write | cards | Add Member vote to Card. |
| DELETE | 1/cards/{id}/membersVoted/{id} | write | cards | Remove a Member's Vote on a Card. |
| GET | 1/cards/{id}/pluginData | read | cards | Get pluginData on a Card. |
| GET | 1/cards/{id}/stickers | read | cards | Get Stickers on a Card. |
| POST | 1/cards/{id}/stickers | write | cards | Add a Sticker to a Card. |
| GET | 1/cards/{id}/stickers/{id} | read | cards | Get a Sticker on a Card. |
| PUT | 1/cards/{id}/stickers/{id} | write | cards | Update a Sticker on a Card. |
| DELETE | 1/cards/{id}/stickers/{id} | write | cards | Delete a Sticker on a Card. |
| GET | 1/cards/{id}/{id} | read | cards | Get a field on a Card. |
| POST | 1/checklists | write | checklists | Create a Checklist. |
| GET | 1/checklists/{id} | read | checklists | Get a Checklist. |
| PUT | 1/checklists/{id} | write | checklists | Update a Checklist. |
| DELETE | 1/checklists/{id} | write | checklists | Delete a Checklist. |
| GET | 1/checklists/{id}/board | read | checklists | Get the Board the Checklist is on. |
| GET | 1/checklists/{id}/cards | read | checklists | Get the Card a Checklist is on. |
| GET | 1/checklists/{id}/checkItems | read | checklists | Get Checkitems on a Checklist. |
| POST | 1/checklists/{id}/checkItems | write | checklists | Create Checkitem on Checklist. |
| GET | 1/checklists/{id}/checkItems/{id} | read | checklists | Get a Checkitem on a Checklist. |
| DELETE | 1/checklists/{id}/checkItems/{id} | write | checklists | Delete Checkitem from Checklist. |
| GET | 1/checklists/{id}/{id} | read | checklists | Get field on a Checklist. |
| PUT | 1/checklists/{id}/{id} | write | checklists | Update field on a Checklist. |
| POST | 1/customFields | write | custom-fields | Create a new Custom Field on a Board. |
| GET | 1/customFields/{id} | read | custom-fields | Get a Custom Field. |
| PUT | 1/customFields/{id} | write | custom-fields | Update a Custom Field definition. |
| DELETE | 1/customFields/{id} | write | custom-fields | Delete a Custom Field definition. |
| GET | 1/customFields/{id}/options | read | custom-fields | Get Options of Custom Field drop down. |
| POST | 1/customFields/{id}/options | write | custom-fields | Add Option to Custom Field dropdown. |
| GET | 1/customFields/{id}/options/{id} | read | custom-fields | Get Option of Custom Field dropdown. |
| DELETE | 1/customFields/{id}/options/{id} | write | custom-fields | Delete Option of Custom Field dropdown. |
| GET | 1/emoji | read | emoji | List available Emoji. |
| GET | 1/enterprises/{id} | read | enterprises | Get an Enterprise. |
| GET | 1/enterprises/{id}/admins | read | enterprises | Get Enterprise admin Members. |
| PUT | 1/enterprises/{id}/admins/{id} | write | enterprises | Update Member to be admin of Enterprise. |
| DELETE | 1/enterprises/{id}/admins/{id} | write | enterprises | Remove a Member as admin from Enterprise. |
| GET | 1/enterprises/{id}/auditlog | read | enterprises | Get auditlog data for an Enterprise. |
| GET | 1/enterprises/{id}/claimableOrganizations | read | enterprises | Get ClaimableOrganizations of an Enterprise. |
| PUT | 1/enterprises/{id}/enterpriseJoinRequest/bulk | write | enterprises | Decline enterpriseJoinRequests from one organization or a bulk list of organizations. |
| GET | 1/enterprises/{id}/members | read | enterprises | Get Members of Enterprise. |
| GET | 1/enterprises/{id}/members/query | read | enterprises | Get Users of an Enterprise. |
| GET | 1/enterprises/{id}/members/{id} | read | enterprises | Get a Member of Enterprise. |
| PUT | 1/enterprises/{id}/members/{id}/deactivated | write | enterprises | Deactivate a Member of an Enterprise. |
| PUT | 1/enterprises/{id}/members/{id}/licensed | write | enterprises | Update a Member's licensed status. |
| GET | 1/enterprises/{id}/organizations | read | enterprises | Get Organizations of an Enterprise. |
| PUT | 1/enterprises/{id}/organizations | write | enterprises | Transfer an Organization to an Enterprise. |
| GET | 1/enterprises/{id}/organizations/bulk/{id} | write | enterprises | Bulk accept a set of organizations to an Enterprise. Kept out of read: despite GET, it accepts organizations into the enterprise. |
| DELETE | 1/enterprises/{id}/organizations/{id} | write | enterprises | Delete an Organization from an Enterprise. |
| GET | 1/enterprises/{id}/pendingOrganizations | read | enterprises | Get PendingOrganizations of an Enterprise. |
| GET | 1/enterprises/{id}/signupUrl | read | enterprises | Get signupUrl for Enterprise. |
| POST | 1/enterprises/{id}/tokens | write | enterprises | Create an auth Token for an Enterprise. |
| GET | 1/enterprises/{id}/transferrable/bulk/{id} | read | enterprises | Get a bulk list of organizations that can be transferred to an enterprise. |
| GET | 1/enterprises/{id}/transferrable/organization/{id} | read | enterprises | Get whether an organization can be transferred to an enterprise. |
| POST | 1/labels | write | labels | Create a Label. |
| GET | 1/labels/{id} | read | labels | Get a Label. |
| PUT | 1/labels/{id} | write | labels | Update a Label. |
| DELETE | 1/labels/{id} | write | labels | Delete a Label. |
| PUT | 1/labels/{id}/{id} | write | labels | Update a field on a label. |
| POST | 1/lists | write | lists | Create a new List. |
| GET | 1/lists/{id} | read | lists | Get a List. |
| PUT | 1/lists/{id} | write | lists | Update a List. |
| GET | 1/lists/{id}/actions | read | lists | Get Actions for a List. |
| POST | 1/lists/{id}/archiveAllCards | write | lists | Archive all Cards in List. |
| GET | 1/lists/{id}/board | read | lists | Get the Board a List is on. |
| GET | 1/lists/{id}/cards | read | lists | Get Cards in a List. |
| PUT | 1/lists/{id}/closed | write | lists | Archive or unarchive a list. |
| PUT | 1/lists/{id}/idBoard | write | lists | Move List to Board. |
| POST | 1/lists/{id}/moveAllCards | write | lists | Move all Cards in List. |
| PUT | 1/lists/{id}/{id} | write | lists | Update a field on a List. |
| GET | 1/members/{id} | read | members | Get a Member. |
| PUT | 1/members/{id} | write | members | Update a Member. |
| GET | 1/members/{id}/actions | read | members | Get a Member's Actions. |
| POST | 1/members/{id}/avatar | write | members | Create Avatar for Member. |
| GET | 1/members/{id}/boardBackgrounds | read | members | Get Member's custom Board backgrounds. |
| POST | 1/members/{id}/boardBackgrounds | write | members | Upload new boardBackground for Member. |
| GET | 1/members/{id}/boardBackgrounds/{id} | read | members | Get a boardBackground of a Member. |
| PUT | 1/members/{id}/boardBackgrounds/{id} | write | members | Update a Member's custom Board background. |
| DELETE | 1/members/{id}/boardBackgrounds/{id} | write | members | Delete a Member's custom Board background. |
| GET | 1/members/{id}/boardStars | read | members | Get a Member's boardStars. |
| POST | 1/members/{id}/boardStars | write | members | Create Star for Board. |
| GET | 1/members/{id}/boardStars/{id} | read | members | Get a boardStar of Member. |
| PUT | 1/members/{id}/boardStars/{id} | write | members | Update the position of a boardStar of Member. |
| DELETE | 1/members/{id}/boardStars/{id} | write | members | Delete Star for Board. |
| GET | 1/members/{id}/boards | read | members | Get Boards that Member belongs to. |
| GET | 1/members/{id}/boardsInvited | read | members | Get Boards the Member has been invited to. |
| GET | 1/members/{id}/cards | read | members | Get Cards the Member is on. |
| GET | 1/members/{id}/customBoardBackgrounds | read | members | Get a Member's custom Board Backgrounds. |
| POST | 1/members/{id}/customBoardBackgrounds | write | members | Create a new custom Board Background. |
| GET | 1/members/{id}/customBoardBackgrounds/{id} | read | members | Get custom Board Background of Member. |
| PUT | 1/members/{id}/customBoardBackgrounds/{id} | write | members | Update custom Board Background of Member. |
| DELETE | 1/members/{id}/customBoardBackgrounds/{id} | write | members | Delete custom Board Background of Member. |
| GET | 1/members/{id}/customEmoji | read | members | Get a Member's customEmojis. |
| POST | 1/members/{id}/customEmoji | write | members | Create custom Emoji for Member. |
| GET | 1/members/{id}/customEmoji/{id} | read | members | Get a Member's custom Emoji. |
| GET | 1/members/{id}/customStickers | read | members | Get Member's custom Stickers. |
| POST | 1/members/{id}/customStickers | write | members | Create custom Sticker for Member. |
| GET | 1/members/{id}/customStickers/{id} | read | members | Get a Member's custom Sticker. |
| DELETE | 1/members/{id}/customStickers/{id} | write | members | Delete a Member's custom Sticker. |
| GET | 1/members/{id}/notificationChannelSettings | read | members | Get a Member's notification channel settings. |
| PUT | 1/members/{id}/notificationChannelSettings | write | members | Update blocked notification keys of Member on a channel. |
| GET | 1/members/{id}/notificationChannelSettings/{id} | read | members | Get blocked notification keys of Member on this channel. |
| PUT | 1/members/{id}/notificationChannelSettings/{id} | write | members | Update blocked notification keys of Member on a channel. |
| PUT | 1/members/{id}/notificationChannelSettings/{id}/{id} | write | members | Update blocked notification keys of Member on a channel. |
| GET | 1/members/{id}/notifications | read | members | Get Member's Notifications. |
| POST | 1/members/{id}/oneTimeMessagesDismissed | write | members | Dismiss a message for Member. |
| GET | 1/members/{id}/organizations | read | members | Get Member's Organizations. |
| GET | 1/members/{id}/organizationsInvited | read | members | Get Organizations a Member has been invited to. |
| GET | 1/members/{id}/savedSearches | read | members | Get Member's saved searched. |
| POST | 1/members/{id}/savedSearches | write | members | Create saved Search for Member. |
| GET | 1/members/{id}/savedSearches/{id} | read | members | Get a saved search. |
| PUT | 1/members/{id}/savedSearches/{id} | write | members | Update a saved search. |
| DELETE | 1/members/{id}/savedSearches/{id} | write | members | Delete a saved search. |
| GET | 1/members/{id}/tokens | write | members | Get Member's Tokens. Kept out of read: returns the member's API tokens. |
| GET | 1/members/{id}/{id} | read | members | Get a field on a Member. |
| POST | 1/notifications/all/read | write | notifications | Mark all Notifications as read. |
| GET | 1/notifications/{id} | read | notifications | Get a Notification. |
| PUT | 1/notifications/{id} | write | notifications | Update a Notification's read status. |
| GET | 1/notifications/{id}/board | read | notifications | Get the Board a Notification is on. |
| GET | 1/notifications/{id}/card | read | notifications | Get the Card a Notification is on. |
| GET | 1/notifications/{id}/list | read | notifications | Get the List a Notification is on. |
| GET | 1/notifications/{id}/member | read | notifications | Get the Member a Notification is about (not the creator). |
| GET | 1/notifications/{id}/memberCreator | read | notifications | Get the Member who created the Notification. |
| GET | 1/notifications/{id}/organization | read | notifications | Get a Notification's associated Organization. |
| PUT | 1/notifications/{id}/unread | write | notifications | Update Notification's read status. |
| GET | 1/notifications/{id}/{id} | read | notifications | Get a field of a Notification. |
| POST | 1/organizations | write | organizations | Create a new Organization. |
| GET | 1/organizations/{id} | read | organizations | Get an Organization. |
| PUT | 1/organizations/{id} | write | organizations | Update an Organization. |
| DELETE | 1/organizations/{id} | write | organizations | Delete an Organization. |
| GET | 1/organizations/{id}/actions | read | organizations | Get Actions for Organization. |
| GET | 1/organizations/{id}/boards | read | organizations | Get Boards in an Organization. |
| GET | 1/organizations/{id}/exports | read | organizations | Retrieve Organization's Exports. |
| POST | 1/organizations/{id}/exports | write | organizations | Create Export for Organizations. |
| POST | 1/organizations/{id}/logo | write | organizations | Update logo for an Organization. |
| DELETE | 1/organizations/{id}/logo | write | organizations | Delete Logo for Organization. |
| GET | 1/organizations/{id}/members | read | organizations | Get the Members of an Organization. |
| PUT | 1/organizations/{id}/members | write | organizations | Update an Organization's Members. |
| PUT | 1/organizations/{id}/members/{id} | write | organizations | Update a Member of an Organization. |
| DELETE | 1/organizations/{id}/members/{id} | write | organizations | Remove a Member from an Organization. |
| DELETE | 1/organizations/{id}/members/{id}/all | write | organizations | Remove a Member from an Organization and all Organization Boards. |
| PUT | 1/organizations/{id}/members/{id}/deactivated | write | organizations | Deactivate or reactivate a member of an Organization. |
| GET | 1/organizations/{id}/memberships | read | organizations | Get Memberships of an Organization. |
| GET | 1/organizations/{id}/memberships/{id} | read | organizations | Get a Membership of an Organization. |
| GET | 1/organizations/{id}/newBillableGuests/{id} | read | organizations | Get Organizations new billable guests. |
| GET | 1/organizations/{id}/pluginData | read | organizations | Get the pluginData Scoped to Organization. |
| DELETE | 1/organizations/{id}/prefs/associatedDomain | write | organizations | Remove the associated Google Apps domain from a Workspace. |
| DELETE | 1/organizations/{id}/prefs/orgInviteRestrict | write | organizations | Delete the email domain restriction on who can be invited to the Workspace. |
| GET | 1/organizations/{id}/tags | read | organizations | Get Tags of an Organization. |
| POST | 1/organizations/{id}/tags | write | organizations | Create a Tag in Organization. |
| DELETE | 1/organizations/{id}/tags/{id} | write | organizations | Delete an Organization's Tag. |
| GET | 1/organizations/{id}/{id} | read | organizations | Get field on Organization. |
| GET | 1/plugins/{id} | read | plugins | Get a Plugin. |
| PUT | 1/plugins/{id} | write | plugins | Update a Plugin. |
| GET | 1/plugins/{id}/compliance/memberPrivacy | read | plugins | Get Plugin's Member privacy compliance. |
| POST | 1/plugins/{id}/listings | write | plugins | Create a Listing for Plugin. |
| PUT | 1/plugins/{id}/listings/{id} | write | plugins | Updating Plugin's Listing. |
| GET | 1/search | read | search | Search Trello. |
| GET | 1/search/members | read | search | Search for Members. |
| GET | 1/tokens/{id} | write | tokens | Get a Token. Kept out of read: returns token records. |
| DELETE | 1/tokens/{id} | write | tokens | Delete a Token. |
| GET | 1/tokens/{id}/member | read | tokens | Get Token's Member. |
| GET | 1/tokens/{id}/webhooks | read | tokens | Get Webhooks for Token. |
| POST | 1/tokens/{id}/webhooks | write | tokens | Create Webhooks for Token. |
| GET | 1/tokens/{id}/webhooks/{id} | read | tokens | Get a Webhook belonging to a Token. |
| PUT | 1/tokens/{id}/webhooks/{id} | write | tokens | Update a Webhook created by Token. |
| DELETE | 1/tokens/{id}/webhooks/{id} | write | tokens | Delete a Webhook created by Token. |
| POST | 1/webhooks | write | webhooks | Create a Webhook. |
| GET | 1/webhooks/{id} | read | webhooks | Get a Webhook. |
| PUT | 1/webhooks/{id} | write | webhooks | Update a Webhook. |
| DELETE | 1/webhooks/{id} | write | webhooks | Delete a Webhook. |
| GET | 1/webhooks/{id}/{id} | read | webhooks | Get a field on a Webhook. |
