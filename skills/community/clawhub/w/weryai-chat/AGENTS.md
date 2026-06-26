# WeryAI Chat

Use this package when the user wants general assistant chat or direct chat-completions access rather than one of the specialized writing skills.

Preferred entry points:

- `node {baseDir}/scripts/write.js`
- `node {baseDir}/scripts/models.js`

Route intents this way:

- general chat or prompt-response -> `write.js`
- explicit `messages` array -> `write.js`
- model list or pricing lookup -> `models.js`

Read `SKILL.md` first for scope boundaries and default model behavior.
Read `references/chat-api.md` when you need the exact message or model-list contract.
