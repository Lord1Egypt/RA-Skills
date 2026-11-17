# Reusable digital human creation

This route applies when the user explicitly wants a new reusable avatar or clone. Ordinary tryouts and talking-head generation should use existing resources.

There is no confirmed public create, approval, or creation-status contract for reusable digital humans. Generating an avatar video does not create a new avatar ID. For creation, preserve adopted copy, inputs, and the next step using [account continuation](../../runtime/account-continuation.md). Run `account_links`, open the returned `create_avatar` link, and ask the user to complete the website flow and reply “continue”. They supply the materials requested by the website directly; do not require training media to be uploaded to the agent first.

On return, query the avatar list again in the same account and region and compare real records with the earlier list. Adopt a uniquely matched requested name, or a single new candidate whose identity matches the user's intent. If several candidates or ambiguous identities remain, show names/covers for one selection. Bind `id + name + cover` from that record; do not ask the user to copy IDs or infer IDs from display positions.

If no new avatar is available yet, say it has not appeared in the available list and provide the returned `avatars` management link to check creation/review progress. Absence does not prove failure or a specific waiting time. Website completion and OpenAPI availability require separate checks. Avoid indefinite polling; preserve progress and refresh after the user confirms availability. Continue independent script/storyboard work without substituting a public avatar for paid generation.

Do not invent IDs, claim creation succeeded, call private web endpoints, or collect additional training material based on guessed duration/format requirements. Follow the requirements actually shown by the platform. See [digital human resources](../../resources/digital-humans.md).
