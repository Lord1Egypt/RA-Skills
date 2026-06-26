---
name: tidepool
description: "Build and deploy any kind of web app without leaving the command line. This project is built for autonomous AI agents. Handles auth, Stripe payments, admin panels, email, database, file storage, custom domains, markdown, secrets, and real-time SSE (chat apps/online games) out of the box. Minimalist approach. Use when: the user wants to create a website, deploy a Python web app, add subscriptions or paywalls, set up user login, or build anything with a URL. Provides the tidepool CLI and tp.* runtime API. Deploys in seconds, scales to 10+ replicas. NOT for: non-web tasks, general Python scripting."
metadata:
  openclaw:
    emoji: "🌀"
    homepage: "https://tidepool.sh"
    requires:
      bins:
        - tidepool
    install:
      - id: uv
        kind: uv
        package: tidepool
        bins:
          - tidepool
        label: "Install Tidepool CLI (pip/uv)"
---

# Tidepool

Build and deploy any kind of web app without leaving the command line. Build for autonomous AI agents. Handles auth, Stripe payments, admin panels, email, database, file storage, custom domains, markdown, secrets, and real-time SSE (chat apps/online games) out of the box. Minimalist approach.

Use when: the user wants to create a website, deploy a Python web app, add subscriptions or paywalls, set up user login, or build anything with a URL. Provides the tidepool CLI and tp.* runtime API. Deploys in seconds, scales to 10+ replicas. NOT for: non-web tasks, general Python scripting.

## Learn the API

Before building anything, fetch the full API reference:

```bash
curl -s https://tidepool.sh/api | python3 -m json.tool
```

This returns every endpoint, every `tp.*` runtime tool, and usage examples. Read it first.

## Workflow

Zero to live Substack clone in one command:
```bash
pip install tidepool && tidepool quickstart
```

Or build from scratch:
```bash
tidepool init my-app && cd my-app
# edit main.py
tidepool dev                    # local dev server at http://localhost:8000
tidepool register --email you@example.com
tidepool deploy                 # live at https://my-app.tidepool.sh
```

Iterate on a live pod:
```bash
tidepool pull <hash>            # pull pod code + data to work locally
tidepool dev                    # test changes locally
tidepool push                   # push code, db, secrets, files back to prod
tidepool push --secret STRIPE_KEY=sk_xxx   # override a secret
tidepool push --replace-db                 # replace all db keys instead of merging
tidepool push --sync            # also delete remote files not present locally
tidepool push -y                # skip confirmation prompt
```

## Runtime (`import tp`)

`main.py` runs once at startup to register routes and configure the app. The server dispatches requests to handlers.

```python
import tp

tp.auth = 'standard'                          # email/password auth
tp.payments = {'products': [{'id': 'pro', 'name': 'Pro', 'price': 500, 'recurring': 'month'}]}
tp.admin = {'users': ['admin@example.com']}

@tp.route('/')
def home(req):
    posts = tp.db.prefix('post:', reverse=True, limit=10)
    return render_posts(posts, req.user)

@tp.route('/post/:slug', methods=['GET', 'POST'])
def post(req, slug):
    if req.method == 'POST':
        tp.db.set(f'post:{slug}', req.body)
        return None  # 303 redirect
    return tp.db.get(f'post:{slug}')
```

**Handler returns:** `str` → HTML, `dict` → JSON, `int` → status, `None` → redirect, `tuple` → (body, status), generator → SSE.

**Request object:** `req.path`, `req.method`, `req.query`, `req.user`, `req.body`, `req.files`.

## Key tools

| Tool | Usage |
|------|-------|
| `tp.route(path)` | `@tp.route('/api/:id', methods=['GET','POST'])` |
| `tp.page(path, html)` | `tp.page('/about', '<h1>About</h1>')` |
| `tp.auth` | `'standard'`, `'paywall'`, or config dict |
| `tp.payments` | `{products: [{id, name, price, recurring}]}` |
| `tp.admin` | `{users: ['admin@x.com'], models: {...}}` |
| `tp.db` | `.get(k)`, `.set(k,v)`, `.delete(k)`, `.prefix(p)`, `.keys()`, `.count()` |
| `tp.files` | `.read(name)`, `.write(name, data)`, `.list()`, `.delete(name)` |
| `tp.email()` | `tp.email('to@x.com', 'Subject', 'body', html='<p>hi</p>')` |
| `tp.http` | `tp.http.get(url)`, `.post(url, json={})` |
| `tp.secrets` | Read-only dict from `tp_data/secrets.json` |
| `tp.state` | Public JSON state, readable at `?format=json` |
| `tp.background()` | `@tp.background(seconds=3600)` for recurring tasks |
| `tp.markdown()` | Convert markdown string to HTML |
| `tp.create_user()` | `tp.create_user('email', 'pass', subscriptions={})` |
| `tp.users()` | Returns all users (password hashes excluded) |
| `tp.publish()` | `tp.publish({'messages': msgs})` — update public JSON state (ETag polling) |

## Notes

- Local dev stores data in `tp_data/` (db.json, secrets.json, files/).
- Secrets go in `tp_data/secrets.json` — they are read-only at runtime.
- Static files in `static/` are served at `/static/`.
- Jinja2 is pre-installed for templating.
- `tidepool eject` copies runtime files into your project for full control.
