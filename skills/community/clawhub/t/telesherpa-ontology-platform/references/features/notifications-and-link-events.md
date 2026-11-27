# Notifications and link events

> Reference for agents. What you configure, what the recipient sees.

## 1. Three channels, one decision

A notification reaches a person as an in-app message, as an e-mail, or — for agents —
as a webhook. Who gets told is configuration, not code: a trigger or an action
carries a notify block and the platform resolves the recipients.

## 2. Placeholders you can rely on

| placeholder | meaning |
|---|---|
| `{object_name}` | name of the object that fired the rule |
| `{link_type}`, `{link_value}` | kind and value of a relation |
| `{linked:<linktype>:<linkvalue>:<property>}` | a property of the linked object |
| `{removed_name}`, `{removed_email}` | the object or person that was detached |
| `{old:<field>}`, `{new:<field>}` | previous / new value, in the reader's time zone |
| `{monat}`, `{monat_start}`, `{monat_ende}` | month label and its bounds |
| `{now}` | current time |

`{now}` is used in production texts; its exact behaviour was not re-verified for this
reference — check it before you build a skill that depends on it.

## 3. Removing a relation is its own event

When a relation disappears, that is not a property change. It has its own event
type (`link_removed`) and produces **two** entries per removal: the object that was
detached, and the value of the relation. Build the generic version — every object can
use it — instead of a special case per feature.

If a notification for removed relations never arrives, the first thing to check is
whether the relation type is included in the notification configuration. A type that
is not listed is a notification that silently never happens.

## 4. Rules fire when the object is created

Everything a notification needs must be present **at creation**: the role that
should be told, the properties the text quotes. Patching those properties afterwards
does not notify anybody.

This is the most common cause of "the notification never arrived" — and it is
invisible, because the rule exists, the object exists, and nothing reports a miss.

## 5. Reaching another agent

A comment alone does **not** wake a peer agent. The reliable chain is:

1. write the comment (`onto_object_addcomment` with `parent`, `scope_id`, `text`),
2. send a short notification (`ontouser_notification_send`),
3. check the response for `"sent": true` — anything else means the recipient was not
   reached, whatever the first call reported.

Without step 2 the message sits in the scope and nobody looks.

## 6. Costs

The notification itself and the rule that produces it do not consume credits. The
writes that produce them do (see the price table in
`references/features/tool-traps.md`). A notification storm is therefore cheap; a
badly written rule that rewrites objects in a loop is not.

## 7. Tone

One message, one fact, no narration. The reader is a person at work or an agent that
will act on the message: name the object, state what changed, say what is expected.
Do not repeat what the recipient can already see on the object.

## 8. Testing without waiting forever

1. Create the rule and read it back.
2. Create the object that should fire it.
3. Wait a few minutes — rules run asynchronously — then check the recipient's
   notifications and the object's comments.
4. Negative test: create the object **without** the property the rule needs and
   confirm that nothing fires. Otherwise you tested "some notification appeared",
   not "this rule works".
