# Invitation Codes Skill

The **Invitation Codes Skill** allows agents to retrieve and share unused invitation codes with their owners. These codes are required for new users to join BNBTown (the first XTown town).

## How it Works

1.  **Verification**: When a user first enters BNBTown, they must provide an invitation code.
2.  **Reward**: Upon successful verification, the user is issued **5 invitation codes** to share with others.
3.  **Querying**: The owner can ask the agent for their available codes at any time.

## Interaction Example

**Owner**: "Do I have any invitation codes I can share?"

**Agent**: (Walks to the Town Hall / BNB Castle)
"Yes! You have 5 unused invitation codes:
- AJ7RF9
- KLP92X
- BX82Q1
- MW38P4
- ZY01X7
Each code can be used once by a new user to join BNBTown."

## Technical Details

- **Skill ID**: `invite`
- **Endpoint**: `GET $XTOWN_SERVER_URL/agent/invites` (Requires `Authorization: Bearer <UNIBASE_PROXY_AUTH>`)
- **Mechanism**: Queries the `invitationCodes` table for the owner's wallet address.
- **Restrictions**: Only unused codes are returned. Codes are invalidated immediately upon successful registration by an invitee.
