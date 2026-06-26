# SEO Actions for Managing Placements (Serpzilla)

The table below lists all available actions for the `serpzilla.perform_placement_action` tool.

| Action name                    | Description	                                                                                                | From status(es)	                                                                                | To status	                       | Notes                                                                                                                       |
|--------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| `approve_seo`                  | Approve a placement after you have reviewed the live page. Marks the placement as successfully completed.   | `STATUS_PLACEMENT_CHECK`                                                                        | `STATUS_APPROVED`                | 	Only possible when the placement is in the final check stage.                                                              | 
| `approve_content_seo`          | Accept the content provided by the webmaster (for formats where content approval is required).              | `STATUS_ON_CONTENT_APPROVAL`, `STATUS_PLACEMENT_ARBITRATION`                                    | `STATUS_ON_PLACEMENT_GUARANTEED` | After approval the placement moves to a guaranteed state. Usually used for `review`, `link`, or `archive` formats.          | 
| `approve_from_arbitration_seo` | Approve a placement that was sent to arbitration, resolving the dispute in your favour.                     | `STATUS_PLACEMENT_ARBITRATION`                                                                  | `STATUS_APPROVED`                | Use this when the moderator or system decides in your favour.                                                               |
| `cancel_from_on_placement_seo` | Cancel a placement that is currently in the “on placement” state (before the webmaster has published).      | `STATUS_ON_PLACEMENT`                                                                           | `STATUS_REJECTED`                | Available only 1‑72 hours after the placement entered `STATUS_ON_PLACEMENT`. After 72 hours the action becomes unavailable. |
| `cancel_from_improve_seo`      | Cancel a placement that is in the “improvement needed” state (webmaster is reworking the content).          | `STATUS_PLACEMENT_IMPROVE`                                                                      | `STATUS_REJECTED`                | Allowed only if the placement has been in `STATUS_PLACEMENT_IMPROVE` for more than 15 days.                                 |
| `cancel_seo`                   | Generic cancellation for placements in various states where the process has stalled or you are unsatisfied. | `STATUS_MODER`, `STATUS_CLARIFICATION`, `STATUS_ON_PLACEMENT_GUARANTEED`, `STATUS_NEED_APPROVE` | `STATUS_REJECTED`                | Requires the placement to be guaranteed and a timeout condition.                                                            |
| `terminate_seo`                | Request permanent removal (teardown) of an already approved backlink.                                       | `STATUS_APPROVED`                                                                               | `STATUS_TO_TERMINATE`            | The link will be removed after the webmaster acts on the request.                                                           |

## Workflow Notes

- **Guaranteed placements** (`STATUS_ON_PLACEMENT_GUARANTEED`) are those where the webmaster has confirmed they will complete the work. Most actions on guaranteed placements have stricter timeouts.
- **Arbitration** (`STATUS_PLACEMENT_ARBITRATION`) is a special state for disputes. You should first try to resolve with the webmaster; if unresolved, use `approve_from_arbitration_seo` or let the moderator decide.

## Example: Cancelling a placement that is stuck in “on placement”

```bash
npx mcporter call serpzilla.perform_placement_action placements_id=12345 action=cancel_from_on_placement_seo
```

## Common Statuses You Will Encounter

| Status                          | Meaning                                    |
|---------------------------------|--------------------------------------------|
| STATUS_PHANTOM	                 | Initial ghost state before any processing. |
| STATUS_CREATING	                | Placement is being created in subsystems.  |
| STATUS_NEED_APPROVE	            | Awaiting your approval (auto‑buyer mode).  |
| STATUS_ON_PLACEMENT	            | Webmaster is expected to place the link.   |
| STATUS_ON_PLACEMENT_GUARANTEED	 | Webmaster guaranteed the placement.        |
| STATUS_ON_CONTENT_APPROVAL	     | Content is ready for your review.          |
| STATUS_PLACEMENT_CHECK	         | Live page is being checked by the system.  |
| STATUS_PLACEMENT_IMPROVE	       | Webmaster must improve the placement.      |
| STATUS_PLACEMENT_ARBITRATION	   | Dispute resolution in progress.            |
| STATUS_APPROVED	                | Placement successfully completed.          |
| STATUS_TO_TERMINATE	            | Link removal requested.                    |
| STATUS_TERMINATED	              | Link removed.                              |
| STATUS_CHANGE_REQUESTED	        | Link change requested.                     |
| STATUS_BUY_FAIL	                | Purchase attempt failed.                   |
| STATUS_WAIT_WITHDRAWAL	         | Draft waiting for payment.                 |
| STATUS_DELETED	                 | Permanently deleted.                       |