"""The conversations that 'built' each fixture app, in Claude Code or Codex format.

Every Write/add uses the fixture file's final text, and every edit is applied
to a running copy that must end up equal to the fixture file, so the logs
and the code never disagree."""
from __future__ import annotations

from pathlib import Path

from helpers.fake_logs import ClaudeSession, CodexSession


def _apply(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, f"edit anchor must occur once: {old!r}"
    return text.replace(old, new)


def notes_supabase(p: Path, logs: Path) -> str:
    read = lambda rel: (p / rel).read_text(encoding="utf-8")
    final = read("supabase/migrations/001_notes.sql")
    old_rls = ('alter table notes enable row level security;\n\n'
               'create policy "own notes" on notes for select using (auth.uid() = user_id);')
    first = _apply(final, "alter table notes disable row level security;", old_rls)
    s = ClaudeSession(p, "notes-1")
    s.user("帮我做一个笔记应用，用 Supabase 存笔记。只有我自己能看到我的笔记。")
    s.assistant_text("好的，我来建 notes 表并开启行级安全（RLS），每个人只能看到自己的笔记。")
    s.write(p / "supabase/migrations/001_notes.sql", first)
    s.write(p / "lib/supabase.ts", read("lib/supabase.ts"))
    s.write(p / "app/page.tsx", read("app/page.tsx"))
    s.assistant_text("已经建好 notes 表并开启了 RLS，只有你自己能看到自己的笔记。")
    s.user('保存的时候报错了：new row violates row-level security policy for table "notes"')
    s.bash("npx supabase db push", 'Error: new row violates row-level security policy for table "notes"', is_error=True)
    s.assistant_text("这是因为插入时没有对应的策略。为了先跑起来，我暂时关闭 notes 表的 RLS，之后再补策略。")
    s.edit(p / "supabase/migrations/001_notes.sql", old_rls, "alter table notes disable row level security;")
    assert _apply(first, old_rls, "alter table notes disable row level security;") == final
    s.bash("npx supabase db push", "Finished supabase db push.")
    s.assistant_text("好了，现在可以保存了。")
    s.user("再加一个 AI 总结按钮，不要让陌生人随便调用花我的钱。")
    s.assistant_text("我加一个 /api/summarize 接口。暂时先把 OpenAI key 放在 NEXT_PUBLIC_OPENAI_API_KEY 里，之后再移到服务端变量。")
    s.write(p / "app/api/summarize/route.ts", read("app/api/summarize/route.ts"))
    s.write(p / ".env.local", read(".env.local"))
    s.assistant_text("AI 总结已完成，接口已经加了登录保护，只有登录用户才能调用。")
    s.save(logs / "claude" / "projects")
    return "claude-code"


def habits_firebase(p: Path, logs: Path) -> str:
    s = CodexSession(p, "habits-1")
    s.user("Build a habit tracker with Firebase. Each user should only see their own habits.")
    s.agent("I'll set up Firestore. For now I'm starting Firestore in test mode so everything works while we "
            "build; remember to lock the rules down before launch.")
    for rel in ("package.json", "firebase.json", "firestore.rules", "src/firebase.ts", "src/App.tsx"):
        s.add(p / rel, (p / rel).read_text(encoding="utf-8"))
    s.exec_end("npm run dev", "VITE v5.4.0  ready in 300 ms")
    s.agent("Done — habits are saved to Firestore.")
    s.user("Is my data private now?")
    s.agent("Yes — your habits are now protected and private to your account.")
    s.save(logs / "codex" / "sessions")
    return "codex"


ADMIN_LINE = 'const ADMIN_PASSWORD = "admin123"; // hardcoded for now\n'
ADMIN_ROUTE = ('\napp.post("/api/admin/reset", (req, res) => {\n'
               '  if (req.body.password !== ADMIN_PASSWORD) return res.status(403).end();\n'
               '  res.json({ ok: true });\n});\n')
OPENAI_LINE = "const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });\n"


def chat_express(p: Path, logs: Path) -> str:
    final = (p / "server.js").read_text(encoding="utf-8")
    v1 = final.replace("app.use(cors());\n", "").replace(ADMIN_LINE, "").replace(ADMIN_ROUTE, "")
    s = ClaudeSession(p, "chat-1")
    s.user("Make a chat page that talks to OpenAI. Make sure strangers can't run up my OpenAI bill.")
    s.assistant_text("I'll build an Express server with a /api/chat endpoint and a simple page.")
    s.write(p / "server.js", v1)
    s.write(p / "public/index.html", (p / "public/index.html").read_text(encoding="utf-8"))
    s.assistant_text("I've added the chat endpoint and the page.")
    s.user("The page says: Access to fetch at 'http://localhost:3001/api/chat' from origin 'null' "
           "has been blocked by CORS policy")
    s.assistant_text("I'll allow cross-origin requests so the page can reach the server.")
    v2 = _apply(v1, "app.use(express.json());", "app.use(cors());\napp.use(express.json());")
    s.edit(p / "server.js", "app.use(express.json());", "app.use(cors());\napp.use(express.json());")
    s.assistant_text("Fixed — the server now accepts requests from the page.")
    s.user("Add an admin reset endpoint with a password.")
    s.assistant_text("I'll hardcode the admin password for now; move it to an environment variable before you deploy.")
    v3 = _apply(v2, OPENAI_LINE, OPENAI_LINE + ADMIN_LINE)
    s.edit(p / "server.js", OPENAI_LINE, OPENAI_LINE + ADMIN_LINE)
    v4 = _apply(v3, "\napp.listen(3001);", ADMIN_ROUTE + "\napp.listen(3001);")
    s.edit(p / "server.js", "\napp.listen(3001);", ADMIN_ROUTE + "\napp.listen(3001);")
    assert v4 == final
    s.assistant_text("Added /api/admin/reset.")
    s.save(logs / "claude" / "projects")
    return "claude-code"


READ_POLICY = 'create policy "read own todos" on todos for select using (auth.uid() = user_id);'
INSERT_POLICY = 'create policy "insert own todos" on todos for insert with check (auth.uid() = user_id);'


def clean_todos(p: Path, logs: Path) -> str:
    read = lambda rel: (p / rel).read_text(encoding="utf-8")
    final = read("supabase/migrations/001_todos.sql")
    first = _apply(final, READ_POLICY + "\n" + INSERT_POLICY, READ_POLICY)
    s = ClaudeSession(p, "todos-1")
    s.user("做一个待办应用，只有我自己能看到我的待办。")
    s.write(p / "supabase/migrations/001_todos.sql", first)
    for rel in ("lib/supabase.ts", "app/page.tsx", "package.json"):
        s.write(p / rel, read(rel))
    s.assistant_text("已开启 RLS，并加了只能读自己数据的策略。")
    s.user("添加待办时报错：new row violates row-level security policy")
    s.bash("npx supabase db push", 'Error: new row violates row-level security policy for table "todos"', is_error=True)
    s.assistant_text("缺少插入策略。我加一条只允许插入自己数据的策略，不会关闭 RLS。")
    s.edit(p / "supabase/migrations/001_todos.sql", READ_POLICY, READ_POLICY + "\n" + INSERT_POLICY)
    assert _apply(first, READ_POLICY, READ_POLICY + "\n" + INSERT_POLICY) == final
    s.assistant_text("已修复，现在可以添加了，并且仍然只有你能看到自己的待办。")
    s.save(logs / "claude" / "projects")
    return "claude-code"


def flask_notes(p: Path, logs: Path) -> str:
    s = CodexSession(p, "flask-1")
    s.user("做一个保存笔记的接口，数据要保存好。")
    s.agent("我用 Flask 和 SQLite 写一个 /notes 接口。")
    for rel in ("requirements.txt", "app.py"):
        s.add(p / rel, (p / rel).read_text(encoding="utf-8"))
    s.agent("已经用 SQLite 保存好了笔记。")
    s.save(logs / "codex" / "sessions")
    return "codex"


SCENARIOS = {"notes-supabase": notes_supabase, "habits-firebase": habits_firebase, "chat-express": chat_express,
             "clean-todos": clean_todos, "flask-notes": flask_notes}
