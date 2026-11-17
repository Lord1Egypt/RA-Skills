# Legacy recovery record compatibility

The old record-only guard classified failures with names such as CORE_APPLIED_WITH_POST_FAILURE, MIGRATION_LOCKED and SERVICE_DEFINITION_DRIFT. Preserve those records when diagnosing an interrupted historical operation.

For current recovery decisions use [the current skill](../SKILL.md), [native semantics](native-updater.md) and [verification/retention](verification-and-retention.md). Do not mix old manual budgets with an active official transaction.

Legacy classifications or a proposed rename are not authorization to act. A migration source, a case alias and a database-registry row are distinct. Inspect physical identity, constrain any requested repair, preserve evidence and honor the user's specific authority.

No lock removal, database overwrite, credential reset, plugin disable or broad cleanup is an automatic recovery shortcut. A package rollback cannot reverse a newer schema.
