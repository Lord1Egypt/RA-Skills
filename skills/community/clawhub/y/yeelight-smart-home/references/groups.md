# Groups

Use this reference for device groups and lighting groups.

- Use `entity.list` or `entity.get` for group discovery.
- Use `group.structure.list` when the user asks for group membership, grouping structure, or group organization under a home.
- Use `group.detail.get` when the user asks for one group's detailed configuration or when a group write plan needs stronger preflight evidence.
- Use `group.create` for creating a persistent group; Runtime must create a pending plan first.
- Use `group.update` when the user changes a group's name, description, icon, or room assignment. Runtime must return a pending plan and verify the group with `entity.list`.
- Do not claim group membership changes are executable from `group.update`; member `details` compatibility remains owner-reviewed.
- Use `group.delete` only when the user explicitly asks to delete one group. Runtime must return a pending plan, re-check the group, and verify removal after commit.
- Use `group.batch_delete` only when the user explicitly asks to delete multiple groups. Runtime caps one plan at 20 groups, resolves each target by id or unique name, and verifies every group disappeared from `entity.list`.
- Do not assume devices can be grouped together. Runtime must validate device membership and capability rules.
- If the user says "this room's lights" and a group is not named, pass natural target text to Runtime rather than inventing a group.
