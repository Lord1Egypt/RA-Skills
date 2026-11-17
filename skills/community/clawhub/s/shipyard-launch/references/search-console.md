# Google Search Console: verify once, cover every subdomain

Use after the app is public (no `noindex`, see `seo-performance.md`). Placeholders: `<your-domain>` (e.g. `example.com`), `<dns-provider>` (where the domain's DNS records live: the registrar, Cloudflare, Vercel DNS, Route 53...).

## Agent rule: try first, ask last

Before asking the student to do anything, try it yourself in the browser session you already have (Search Console, the DNS provider's dashboard). Often the student is already signed in there. Ask only for the one step you really cannot do (a sign-in with a password or a second factor), say exactly which page and button, and never ask for a password in chat: let them type it into the page.

## 0. Find every app's real address before deciding what to submit

Never conclude an app "has no custom domain" from one signal. Repo names, project names and hostnames often differ (repo `psycscope` -> `psyc.<your-domain>`, Vercel project `landing` -> `hydrascrape.<your-domain>`), and a list of projects is paginated. Check all of these, and treat an app as having a custom domain if any of them shows one:

1. **Every Vercel project, every page.** `GET /v9/projects?teamId=<team>&limit=100`, then follow `pagination.next` (pass it as `from=`) until it is null. The default page is only 20 projects, so an unpaged call silently misses the rest. Pass `teamId` (or `--scope`) so a token that defaults to another scope still lists the team's projects.
2. **Each project's domain list.** `GET /v9/projects/<id-or-name>/domains?teamId=<team>` lists every attached domain, including ones whose latest production deploy failed. `targets.production.alias` only reflects the latest production deploy, so it can be empty or stale.
3. **Map by linked repo, not by name.** Use `project.link.repo` to join repos to projects; one repo can feed several projects and the names rarely match.
4. **Confirm with DNS and HTTP.** `dig +short <host>` (or `getent hosts <host>`) must resolve, and `curl -sI https://<host>/` must answer from the app. A domain that is attached but returns Vercel's `NOT_FOUND` page has no production deployment yet: redeploy it, don't call it "no domain".
5. Write the result as a table (repo, project, hosts, resolves, HTTP status) and use it for the sitemap list below.

## 1. Prefer a Domain property

In Search Console > Add property, choose **Domain** (not URL prefix) and enter `<your-domain>` with no `https://` and no `www`. One Domain property covers `https`, `http`, `www` and every subdomain (`app1.<your-domain>`, `app2.<your-domain>`...), so new apps on the domain are covered with no new verification. Use a URL-prefix property only when you cannot edit DNS (then verify with the HTML file or meta tag, and make sure the proxy does not redirect that file to sign-in).

## 2. Add the TXT record at `<dns-provider>`

Search Console shows a value like `google-site-verification=...`. Copy it exactly.

1. Find where the DNS records live: check the domain's nameservers (`dig NS <your-domain> +short`). That company is `<dns-provider>`, even if you bought the domain elsewhere.
2. In its dashboard the records are usually under *DNS*, *DNS management*, *DNS zone*, *Advanced DNS* or *Records* for the domain.
3. Add a **new** record: type `TXT`, host/name `@` (some providers want it blank, or the full `<your-domain>.`; all three mean the root), value = the Google string, TTL default.
4. **Never edit or delete existing records.** Other TXT records (SPF `v=spf1`, DKIM, other verifications) stay as they are; a domain can have many TXT records. Do not touch A, CNAME or MX records.
5. Check it is live: `dig TXT <your-domain> +short` shows the Google string (can take minutes, rarely hours). Then press **Verify** in Search Console.
6. **Keep the record after verifying.** Google re-checks it; deleting it unverifies the property.

## 3. Submit sitemaps and request indexing

- Sitemaps (left menu): submit the full URL of each app's sitemap, e.g. `https://<your-domain>/sitemap.xml` and `https://app1.<your-domain>/sitemap.xml`. Status should become "Success"; "Couldn't fetch" usually means the proxy or an auth wall blocks it.
- URL Inspection: paste each app's home page, then **Request indexing**. Do it for the landing page of each app, not every page (the sitemap handles the rest).
- Check back after a few days: Pages report > "Why pages aren't indexed". "Excluded by noindex" on a public app means a `noindex` was left on.
