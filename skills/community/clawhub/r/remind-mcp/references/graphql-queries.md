# Remind GraphQL — ready-to-run documents

Every query below was executed against the live API. Field selections come from introspection;
Remind reports an unknown field as `Internal service error` / `GRAPHQL_VALIDATION_FAILED`, so
edit them only alongside a re-run.

All examples assume the `rq` helper from `SKILL.md`.

---

## Start here — what's in the account

`navigationList` is the sidebar, and the source of every uuid you need.

```bash
rq '{ navigationList { cursor items { __typename
  ... on TextHeader { text }
  ... on NavigationListEntityItem { type uuid title subtitle isRostered unreadsCount } } } }'
```

Just the classes and chats, one per line:

```bash
rq '{ navigationList { items { __typename
  ... on NavigationListEntityItem { type uuid title unreadsCount } } } }' \
| jq -r '.data.navigationList.items[]
         | select(.__typename=="NavigationListEntityItem")
         | "\(.type)\t\(.unreadsCount // 0)\t\(.uuid)\t\(.title)"'
```

Page with `cursor`: pass it back as `lastCursor`.

```bash
rq 'query($c:String){ navigationList(lastCursor:$c){ cursor items { __typename } } }' '{"c":"<cursor>"}'
```

## Account

```bash
rq '{ me { uuid id first_name last_name display_name email locale is_admin is_child created_at sign_in_count } }' \
| jq .data.me
```

## Classes

```bash
rq 'query($u:[String!]){ classes(uuids:$u){
  uuid id code name displayName type
  messagesCount unreadMessagesCount subscribersCount membershipsCount ownersCount
  createdAt archivedAt messageHistoryEnabled isMember joinUrl
  subscriberInitiatedChats canEditInfo canAddOwners } }' \
  '{"u":["<class-uuid>"]}' | jq '.data.classes[]'
```

Class members (paginate with `page`/`perPage`):

```bash
rq 'query($u:[String!]){ classes(uuids:$u){ members(perPage:50){ __typename } } }' '{"u":["<class-uuid>"]}'
```

> Introspect `ClassMembership` before selecting fields:
> `rq '{ __type(name:"ClassMembership"){ fields { name } } }' | jq -r '.data.__type.fields[].name'`

## Chats

List every conversation, with the permission that decides whether you can reply:

```bash
rq '{ chatStreams { uuid title properTitle streamType type state hidden
  unreadMessagesCount membershipsCount updatedAt
  permissions { canSend canAdd canClose canLeave canPhone } } }' \
| jq -r '.data.chatStreams[] | "\(.updatedAt)\t\(.unreadMessagesCount)\t\(.uuid)\t\(.title)"'
```

Filter to one class (numeric `id` from `classes`, not the uuid) or search by name:

```bash
rq 'query($g:Int,$q:String){ chatStreams(groupId:$g, chatQuery:$q){ uuid title } }' '{"g":47615786,"q":null}'
```

## Messages

```bash
rq 'query($u:[String!],$n:Int){ chatStreams(chatUuids:$u){
  uuid title unreadMessagesCount
  sequenceItems(nonGapMessagesLimit:$n){ seq key item { __typename
    ... on MessageItem { uuid body type createdAt sentAt urgent publicUrl
                         sender { uuid name } files { __typename } }
    ... on SystemMessageItem { uuid body createdAt }
    ... on GapItem { uuid size } } } } }' \
  '{"u":["<chat-uuid>"],"n":25}'
```

Readable transcript, oldest first:

```bash
… | jq -r '.data.chatStreams[].sequenceItems[]
           | select(.item.__typename=="MessageItem")
           | "\(.item.createdAt)  \(.item.sender.name): \(.item.body)"'
```

Item types: **MessageItem** (a real message), **SystemMessageItem** (joins, stream creation),
**GapItem** (`size` unloaded messages — raise `nonGapMessagesLimit` or page with
`gapItemNextPageParams`).

## Notification settings

```bash
rq '{ accountNotificationsScreen {
  canManageReplies repliesEnabled
  canManageAnnouncementCopies announcementCopiesEnabled
  canManageCalls allowsIncomingCalls
  devices { id type title deliveryDescription isEnabled isPendingConfirmation isPreferredVoiceCallsDevice } } }' \
| jq '.data.accountNotificationsScreen'
```

The `canManage*` flags say what this account may change. On a subscriber (parent) account they
are typically all `false` — the *device* toggles below still work.

## Schema discovery

```bash
# root fields
rq '{ __type(name:"Query"){ fields { name } } }'    | jq -r '.data.__type.fields[].name'
rq '{ __type(name:"Mutation"){ fields { name } } }' | jq -r '.data.__type.fields[].name'
# one type's fields, with types
rq '{ __type(name:"MessageItem"){ fields { name type { name kind ofType { name } } } } }'
# union / interface members — needed to write an inline fragment
rq '{ __type(name:"StreamItem"){ possibleTypes { name } } }' | jq -r '.data.__type.possibleTypes[].name'
```

---

## Mutations — read this first

Writes hit real people and **cannot be unsent**. Nothing here is needed for reading Remind.

**Verified live:** toggling notification devices, which affects only your own account.

```bash
# disable, then re-enable, a delivery device (id from accountNotificationsScreen)
rq 'mutation($i:UpdateAccountNotificationsScreenInput!){ updateAccountNotificationsScreen(input:$i){ __typename } }' \
   '{"i":{"devicesToDisable":[<device-id>]}}'
rq 'mutation($i:UpdateAccountNotificationsScreenInput!){ updateAccountNotificationsScreen(input:$i){ __typename } }' \
   '{"i":{"devicesToEnable":[<device-id>]}}'
```

A 200 is not proof — re-read `accountNotificationsScreen` and check `devices[].isEnabled` actually moved.

**Shape only, NOT executed here** — sending a message. Check `permissions.canSend` first.

```bash
rq 'mutation($i:PutMessageInput!){ putMessage(input:$i){ error { __typename } messages { __typename } } }' \
   '{"i":{"recipients":[{"type":"chat","uuid":"<chat-uuid>"}],"message":{"body":"…","urgent":false}}}'
```

`recipients[].type` is `chat` for a conversation or `group` for a whole class.

**Owner/teacher only:** `scheduleMessage`, `api_scheduledMessages` and `api_deleteScheduledMessage`
return `Unauthorized` on a subscriber account even with a valid session.
