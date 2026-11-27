# Scope bridges: writing into a scope where you have no write right

> Reference for agents building a workspace. Describes the contract you configure
> and what you can observe — not the platform internals.

## 1. The problem

A staff member must be able to clock in, request a swap or hand in a wish — and the
result belongs in the planning scope, where that person has no write access (and,
in the reference layout, no read access either).

Granting write access to planning would hand over the whole plan. So the platform
gives no right; it opens a **door for one write operation**: the action declares the
scope its result belongs to.

```json
"action": {
  "type": "update",
  "result_scope_id": 80,
  "props": ["actual_start", "actual_end"]
}
```

## 2. What that door allows

The door is narrow by construction. A write is accepted without a write grant only
if all of these hold:

1. the call is the execution of that action definition — the door exists during the
   call and is closed again afterwards,
2. the target is exactly the object the action works on (one object, not its links),
3. the property is listed in `action.props`,
4. the property belongs to the same scope as the result scope.

Nothing survives the call. It is not a temporary grant and not a session state: the
next request has to open its own door.

## 3. Rules the platform enforces when you save the definition

An agent that gets these wrong builds a definition that looks fine and fails on the
first click, in front of the customer:

- `result_scope_id` belongs **inside** `action`. A value at the top level of the body
  is rejected with an explicit error rather than ignored silently.
- The definition must **bind the acting person**: one of `{current_user_email}`,
  `{current_profile_id}`, `{current_user_id}`, `{user_email}`, `{user_person}`.
  Exception: `type: "form_answer"` binds the person itself, so the declaration is not
  required there.
- `type: "update"` with a `result_scope_id` **requires** a non-empty `action.props`.
  Without the list the door would allow "everything on this object", which is exactly
  what it must not do.

## 4. When the bridge is the wrong tool

| Situation | Better approach |
|---|---|
| staff must **read** data from another scope | a dedicated view that shows only what they need, or a copy written by a trigger — never a read grant on planning |
| a whole object has to move between scopes | an action that creates or updates it in the target scope |
| several objects change at once | one action per object; the door is bound to one object |
| notifications afterwards | a notify block on the action, or a trigger on the property |

## 5. Worked example — swap request

Team scope; the member approves a swap for their own shift:

```json
{
  "action": {
    "type": "update",
    "target": "{linked:worksShift:...:udid}",
    "result_scope_id": 80,
    "props": ["swap_status", "swap_partner"]
  },
  "guards": [
    { "type": "linked_to_user", "linktype": "worksShift",
      "message": "Only your own shift can be changed." }
  ]
}
```

What happens: the member clicks in the team scope; the guard proves the object is
theirs; the write lands in the planning scope for exactly these two properties; the
door closes; the member still has no write grant there.

## 6. Pitfalls

1. **UDID case.** Hex ids are lower case. An id written in mixed case silently never
   matches.
2. **Detaching a link is not a property write.** It has its own path and its own
   event; check it separately when the action is supposed to remove a relation.
3. **`type: "create"`** needs the person binding in the body — no link to the person
   is created automatically.
4. **Guards first.** A guard of type `linked_to_user` with the `linktype` proves
   "only my own row". Without it the door writes into a foreign object as soon as
   somebody manipulates an id.
5. **Costs.** An action costs 20 credits, paid by the executing account. The bridge
   does not change who pays; a member without credits gets HTTP 402 before anything
   happens.

## 7. Test recipe, no browser needed

1. As manager: save the definition, then read it back — the saved body is the truth.
2. As the member: execute the action once.
3. As manager: read the target object and confirm the property changed in the
   planning scope.
4. As the member: confirm the planning scope is still invisible.
5. Negative test: the same call against a foreign object must fail on the guard, not
   "succeed" quietly.
