---
name: Ruby on Rails
detect:
  files: ["Gemfile", "config/routes.rb", "config/application.rb"]
  dependencies: ["rails", "actionpack", "activerecord", "actioncable"]
  keywords: ["Rails", "Ruby on Rails"]
---

## recon-agent

**Rails Discovery:**
1. Read `config/routes.rb` — maps all HTTP endpoints with their controller actions
2. Glob for `config/initializers/*.rb` — security-relevant initializers (CORS, session, auth)
3. Check `config/environments/production.rb` vs `config/environments/development.rb` for security differences
4. Glob for `app/models/*.rb` and check for `has_secure_password`, custom validations

## attack-surface-http

**Controller Vulnerabilities:**
1. Grep for `params.permit` and `params.require` — these define strong parameters
   - Are there controllers using `params.permit!` (permit ALL parameters)? This is mass assignment
   - Are there actions that use `params[:key]` directly without going through strong parameters?
   - Can an attacker add `admin`, `role`, or `id` to permitted parameters?
2. **Unsafe Rendering:**
   - Grep for `render inline:`, `render text:`, `render html:` with user input — SSTI/XSS risk
   - Grep for `raw`, `html_safe`, `sanitize` in views — these bypass HTML escaping
   - Are there ERB templates using `<%= raw ... %>` or `<%== ... %>` (unescaped output)?
3. **Open Redirects:**
   - Grep for `redirect_to params[` — user-controlled redirect destination
   - Is `redirect_to` used with `allow_other_host: true`? (allows external redirects)
4. **File Sending:**
   - Grep for `send_file`, `send_data` — are paths user-controlled?
   - Is `ActiveStorage` configured with proper access controls?

## attack-surface-authz

**Authorization Patterns:**
1. Check which authorization library is used (Pundit, CanCanCan, custom):
   - Pundit: Are there controllers missing `authorize` or `policy_scope` calls?
   - CanCanCan: Is `load_and_authorize_resource` used consistently? Are there `skip_authorization` calls?
2. **`before_action` Filters:**
   - Are auth filters applied via `before_action` in `ApplicationController`?
   - Are there controllers with `skip_before_action :authenticate_user!` that shouldn't have it?
   - Can filter ordering be exploited? (filters run in definition order)
3. **IDOR via ActiveRecord:**
   - Are there `Model.find(params[:id])` calls without scoping to the current user?
   - Should it be `current_user.models.find(params[:id])` instead?

## config-infrastructure

**Rails Security Configuration:**
1. **Secret Management:**
   - Is `Rails.application.credentials` or `Rails.application.secrets` used?
   - Is `config/master.key` or `config/credentials.yml.enc` committed? (master.key should NOT be committed)
   - Is `SECRET_KEY_BASE` set in production? (missing = session forgery)
2. **CSRF Protection:**
   - Is `protect_from_forgery with: :exception` enabled in `ApplicationController`?
   - Are there controllers with `skip_forgery_protection` or `protect_from_forgery with: :null_session` that serve HTML forms?
3. **Content Security Policy:**
   - Check `config/initializers/content_security_policy.rb`
   - Is CSP configured? Are there `unsafe-inline` or `unsafe-eval` directives?
4. **Cookie Configuration:**
   - Check `config/initializers/session_store.rb`
   - Is `secure: true` set for production cookies?
   - Is `httponly: true` set? Is `same_site: :lax` or `:strict` set?
5. **ActionCable:**
   - If ActionCable is used: check `config/environments/production.rb` for `allowed_request_origins`
   - Is the WebSocket origin check restrictive? (setting it to `[/http:\/\/*/]` allows any origin)
   - Are channel subscriptions authenticated?

## dependency-audit

**Rails-Specific Dependency Concerns:**
1. Check Rails version for known CVEs (deserialization, SQL injection, path traversal)
2. Is `rack` updated? (frequent header parsing and DoS vulnerabilities)
3. Are `nokogiri` and `loofah` updated? (HTML/XML parsing vulnerabilities)
4. Is `devise` (if used) updated? (authentication bypass vulnerabilities)
5. Is `brakeman` configured as a development dependency? Review any existing Brakeman output
