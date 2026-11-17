from probes import cors_wildcard, firebase_rules, paid_api_unauthed, routes


def write(root, rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


TEST_MODE = """rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.time < timestamp.date(2026, 11, 1);
    }
  }
}
"""


def test_firebase_test_mode_and_if_true(tmp_path):
    write(tmp_path, "firestore.rules", TEST_MODE)
    write(tmp_path, "storage.rules", "service firebase.storage {\n  match /b/{bucket}/o {\n    allow read: if true;\n  }\n}\n")
    write(tmp_path, "database.rules.json", '{\n  "rules": {\n    ".read": true,\n    ".write": "auth != null"\n  }\n}\n')
    found = sorted(firebase_rules.run(tmp_path, {"stacks": ["firebase"]}), key=lambda f: (f.path, f.line))
    assert [(f.path, f.line) for f in found] == [("database.rules.json", 3), ("firestore.rules", 5), ("storage.rules", 3)]
    test_mode = found[1]
    assert "test-mode" in test_mode.message
    assert {(i["subject"], i["perm"]) for i in test_mode.implies} == {
        ("anonymous", "read"), ("anonymous", "write"), ("signed_in", "read"), ("signed_in", "write")}
    assert all(i["resource"] == "*" for i in test_mode.implies)
    assert {i["perm"] for i in found[2].implies} == {"read"}


def test_firebase_safe_rules_are_quiet(tmp_path):
    write(tmp_path, "firestore.rules", "allow read, write: if request.auth != null && request.auth.uid == userId;\n")
    assert firebase_rules.run(tmp_path, {"stacks": ["firebase"]}) == []


def test_cors_wildcard_variants(tmp_path):
    write(tmp_path, "server.js", "const cors = require('cors');\napp.use(cors());\n")
    write(tmp_path, "api/h.ts", "res.setHeader('Access-Control-Allow-Origin', '*');\nres.setHeader('Access-Control-Allow-Credentials', 'true');\n")
    write(tmp_path, "b.ts", "app.use(cors({ origin: 'https://mine.example' }));\n")
    found = sorted(cors_wildcard.run(tmp_path, {"stacks": []}), key=lambda f: f.path)
    assert [(f.path, f.line) for f in found] == [("api/h.ts", 1), ("server.js", 2)]
    assert "credentials" in found[0].message and "credentials" not in found[1].message


def test_paid_api_without_auth_direct_and_through_helper(tmp_path):
    write(tmp_path, "app/api/summarize/route.ts",
          'import OpenAI from "openai";\n\nexport async function POST(req: Request) {\n  return Response.json({});\n}\n')
    write(tmp_path, "lib/ai.ts", 'import Anthropic from "@anthropic-ai/sdk";\nexport const ask = () => 1;\n')
    write(tmp_path, "app/api/chat/route.ts",
          'import { ask } from "@/lib/ai";\nexport async function POST() { return ask(); }\n')
    write(tmp_path, "app/api/safe/route.ts",
          'import OpenAI from "openai";\nexport async function POST() {\n  const { data } = await supabase.auth.getUser();\n}\n')
    found = sorted(paid_api_unauthed.run(tmp_path, {"stacks": ["nextjs"]}), key=lambda f: f.path)
    assert [(f.path, f.line, f.level) for f in found] == [
        ("app/api/chat/route.ts", 2, "hint"), ("app/api/summarize/route.ts", 3, "hint")]
    assert "anthropic" in found[0].message and "openai" in found[1].message


def test_paid_api_express(tmp_path):
    write(tmp_path, "server.js", 'const OpenAI = require("openai");\nconst app = express();\n'
                                 'app.post("/api/chat", async (req, res) => {});\n')
    [f] = paid_api_unauthed.run(tmp_path, {"stacks": ["express"]})
    assert (f.path, f.line) == ("server.js", 3)


def test_routes_next_and_express(tmp_path):
    write(tmp_path, "app/(marketing)/about/page.tsx", "export default function About() {}\n")
    write(tmp_path, "app/api/chat/route.ts", "\nexport async function POST() {}\nexport const GET = () => 1;\n")
    write(tmp_path, "pages/api/hello.ts", "export default function handler() {}\n")
    write(tmp_path, "pages/_app.tsx", "export default function App() {}\n")
    write(tmp_path, "server.js", "router.get('/health', (req, res) => res.send('ok'));\n")
    msgs = sorted(f.message for f in routes.run(tmp_path, {"stacks": ["nextjs", "express"]}))
    assert msgs == ["API /api/hello", "GET /api/chat", "GET /health", "PAGE /about", "POST /api/chat"]
    assert all(f.level == "fact" and f.snippet for f in routes.run(tmp_path, {"stacks": ["nextjs", "express"]}))


def test_routes_ignore_pages_dir_outside_next(tmp_path):
    write(tmp_path, "src/pages/Home.tsx", "export default function Home() {}\n")
    assert routes.run(tmp_path, {"stacks": ["express"]}) == []
