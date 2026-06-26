---
title: Use RunInTransaction with the Scoped txApp, Never the Outer App
impact: CRITICAL
impactDescription: Mixing scoped and outer app inside a transaction silently deadlocks or writes outside the tx
tags: transactions, extending, deadlock, runInTransaction, atomicity
---

## Use RunInTransaction with the Scoped txApp, Never the Outer App

`app.RunInTransaction` (Go) and `$app.runInTransaction` (JS) wrap a block of work in a SQLite write transaction. The callback receives a **transaction-scoped app instance** (`txApp` / `txApp`). Every database call inside the block must go through that scoped instance - reusing the outer `app` / `$app` bypasses the transaction (silent partial writes) or deadlocks (SQLite allows only one writer).

**Incorrect (outer `app` used inside the tx block):**

```go
// ❌ Uses the outer app for the second Save - deadlocks on the writer lock
err := app.RunInTransaction(func(txApp core.App) error {
    user := core.NewRecord(usersCol)
    user.Set("email", "a@b.co")
    if err := txApp.Save(user); err != nil {
        return err
    }

    audit := core.NewRecord(auditCol)
    audit.Set("user", user.Id)
    return app.Save(audit) // ❌ NOT txApp - blocks forever
})
```

**Correct (always `txApp` inside the block, return errors to roll back):**

```go
err := app.RunInTransaction(func(txApp core.App) error {
    user := core.NewRecord(usersCol)
    user.Set("email", "a@b.co")
    if err := txApp.Save(user); err != nil {
        return err // rollback
    }

    audit := core.NewRecord(auditCol)
    audit.Set("user", user.Id)
    if err := txApp.Save(audit); err != nil {
        return err // rollback
    }
    return nil // commit
})
if err != nil {
    return err
}
```

```javascript
// JSVM - the callback receives the transactional app
$app.runInTransaction((txApp) => {
    const user = new Record(txApp.findCollectionByNameOrId("users"));
    user.set("email", "a@b.co");
    txApp.save(user);

    const audit = new Record(txApp.findCollectionByNameOrId("audit"));
    audit.set("user", user.id);
    txApp.save(audit);

    // throw anywhere in this block to roll back the whole tx
});
```

**Rules of the transaction:**
- **Use only `txApp` / the callback's scoped app** inside the block. Capturing the outer `app` defeats the purpose and can deadlock.
- Inside event hooks, `e.App` is already the transactional app when the hook fires inside a tx - prefer it over a captured parent-scope `app` for the same reason.
- Return an error (Go) or `throw` (JS) to roll back. A successful return commits.
- SQLite serializes writers - keep transactions **short**. Do not make HTTP calls, send emails, or wait on external systems inside the block.
- Do not start a transaction inside another transaction on the same app - nested `RunInTransaction` on `txApp` is supported and reuses the existing transaction, but nested calls on the outer `app` will deadlock.
- Hooks (`OnRecordAfterCreateSuccess`, etc.) fired from a `Save` inside a tx run **inside that tx**. Anything they do through `e.App` participates in the rollback; anything they do through a captured outer `app` does not.

Reference: [Go database](https://pocketbase.io/docs/go-database/#transaction) · [JS database](https://pocketbase.io/docs/js-database/#transaction)
