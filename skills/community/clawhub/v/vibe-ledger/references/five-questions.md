# The five questions

Every promise sits under exactly one question. If a promise fits none of them, it does not belong in the ledger.

| Key | Question | Belongs here | Does not belong here |
|---|---|---|---|
| `where_data` | Where does the data live? | "save notes in Supabase", "keep photos in S3", "don't store card numbers" | "use a blue theme" |
| `what_costs` | What costs money? | "don't let strangers run up my OpenAI bill", "only call the AI when I press the button", "stay on the free tier" | "make it fast" |
| `who_can_see` | Who can see it? | "only I can see my notes", "teammates can read but not edit", "the admin page is password-protected" | "add a dark mode" |
| `what_breaks` | Where is it most likely to break? | "it must not crash when the list is empty", promises about backups, error handling around payments | general code style |
| `open_debts` | What was put off "for later"? | "for now the key is in the frontend", "test mode until launch", "hardcode the admin password for now" | ideas never agreed on |

Put a `deferred` promise under `open_debts` unless it is clearly about another question (a key "for now in the frontend" is `open_debts`; its consequence for `what_costs` goes in the verdict).

Subjects in the access matrix:

- `anonymous` — anyone on the internet who is not signed in;
- `signed_in` — another signed-in user who does not own the data;
- `owner` — the person the data belongs to.
