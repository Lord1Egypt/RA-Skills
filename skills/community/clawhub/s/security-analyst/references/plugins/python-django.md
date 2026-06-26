---
name: Python + Django
detect:
  files: ["manage.py", "settings.py"]
  dependencies: ["django", "djangorestframework", "django-rest-framework"]
  keywords: ["Django", "Django REST Framework", "DRF"]
---

## attack-surface-http

**CSRF Exemptions:**
1. Grep for `@csrf_exempt` across the entire codebase
   - For EACH exempt view: why is CSRF disabled? Is it a legitimate API endpoint using token auth, or a mistake?
   - Are there views that use `@csrf_exempt` but also accept cookie-based authentication? (this is a CSRF vulnerability)
   - Check DRF views: DRF disables CSRF for `SessionAuthentication` unless explicitly configured — is this understood?

2. **ModelForm Field Exposure:**
   - Grep for `class Meta:` inside Form/ModelForm classes
   - Are forms using `fields = '__all__'`? This exposes ALL model fields to user input (including admin-only fields)
   - Is `exclude` used instead of `fields`? (dangerous — new model fields are auto-included unless explicitly excluded)
   - Best practice: always use explicit `fields = [...]` whitelist

3. **Raw SQL and QuerySet Injection:**
   - Grep for `.raw(`, `.extra(`, `RawSQL`, `cursor.execute`, `connection.cursor`
   - Are user inputs interpolated into raw SQL? (f-strings, `.format()`, `%` formatting)
   - Does `.extra()` use user-controlled `where`, `select`, or `tables` arguments?
   - Are there ORM filter calls with user-controlled field names? (e.g., `Model.objects.filter(**user_dict)` — allows filtering on any field including relationships)

4. **URL Resolver ReDoS:**
   - Are URL patterns using complex regex? (in `urlpatterns`)
   - Can crafted URLs cause catastrophic backtracking in URL resolution?
   - Are URL patterns using `re_path()` with user-influenced patterns?

5. **File Upload Handling:**
   - Are file uploads using Django's `FileField`/`ImageField`?
   - Is `MEDIA_ROOT` in a safe location? (not inside the static files directory or a web-accessible path)
   - Are uploaded file names sanitized? (Django sanitizes by default, but custom `upload_to` callables might not)
   - Is `FILE_UPLOAD_MAX_MEMORY_SIZE` configured to prevent large uploads from consuming memory?

6. **DRF-Specific (if Django REST Framework is used):**
   - Are serializers using `fields = '__all__'`? (same risk as ModelForm)
   - Is the default permission class restrictive? (check `DEFAULT_PERMISSION_CLASSES` in settings — `AllowAny` is dangerous as default)
   - Are viewset actions individually permission-checked? (`@action` decorators with `permission_classes`)
   - Is the browsable API enabled in production? (exposes API structure and allows unauthenticated browsing)
   - Are throttle rates configured? (`DEFAULT_THROTTLE_RATES`)

## attack-surface-authz

**Django Permissions Framework:**
1. How is authorization enforced?
   - `@login_required` only checks authentication, NOT authorization — is it used where `@permission_required` should be?
   - `@permission_required` checks model-level permissions — but does the app need object-level permissions?
   - Are there views that check `request.user.is_staff` or `request.user.is_superuser` inline? (fragile — easy to forget)

2. **Object-Level Permissions:**
   - Does the app use a library like `django-guardian` or `django-rules` for object-level permissions?
   - If not, are object-level checks done manually in each view? (error-prone — easy to miss a view)
   - For DRF: are `get_queryset()` and `get_object()` properly filtering by user? (the default `get_object()` only does a pk lookup without ownership checks)

3. **Admin Site Security:**
   - Is the Django admin accessible? (check `admin/` in `urlpatterns`)
   - Is the admin URL path customized from the default `/admin/`? (obscurity alone isn't security, but default path is actively probed)
   - Are admin actions audited? (Grep for `LogEntry`, `django.contrib.admin.models`)
   - Is two-factor auth enabled for admin? (Grep for `django-otp`, `django-two-factor-auth`)

4. **Group and Permission Assignments:**
   - Are permissions assigned via groups or directly to users? (group-based is more maintainable)
   - Can users be assigned to groups via API endpoints? (privilege escalation if an endpoint allows group modification)
   - Are custom permissions defined in models? (`class Meta: permissions = [...]`) — are they actually checked?

## config-infrastructure

**Django Settings Security:**
1. Read `settings.py` (and any environment-specific settings files) and check:
   - **`DEBUG`**: Is it `False` in production? (Grep for `DEBUG = True` and conditional logic)
   - **`SECRET_KEY`**: Is it hardcoded in settings or loaded from environment? Is it strong (50+ random chars)?
   - **`ALLOWED_HOSTS`**: Is it set? Is it restrictive? (`['*']` allows host header injection)
   - **`SECURE_SSL_REDIRECT`**: Is HTTPS enforced?
   - **`SECURE_HSTS_SECONDS`**: Is HSTS enabled with a reasonable duration?
   - **`SECURE_HSTS_INCLUDE_SUBDOMAINS`**: Are subdomains included in HSTS?
   - **`SECURE_CONTENT_TYPE_NOSNIFF`**: Is `X-Content-Type-Options: nosniff` set?
   - **`SECURE_BROWSER_XSS_FILTER`**: Is the XSS filter enabled?

2. **Cookie Security:**
   - **`SESSION_COOKIE_SECURE`**: Is it `True`? (cookie only sent over HTTPS)
   - **`SESSION_COOKIE_HTTPONLY`**: Is it `True`? (prevents JavaScript access)
   - **`SESSION_COOKIE_SAMESITE`**: Is it set to `'Lax'` or `'Strict'`?
   - **`CSRF_COOKIE_SECURE`**: Is it `True`?
   - **`SESSION_COOKIE_AGE`**: Is it reasonable? (default is 2 weeks — may be too long)

3. **Database Security:**
   - Are database credentials hardcoded in settings or loaded from environment/secrets?
   - Is the database using SSL for connections?
   - Are there multiple database configurations? Are read replicas properly restricted?

4. **Middleware Order:**
   - Django middleware order matters — check `MIDDLEWARE` list:
     - `SecurityMiddleware` should be first (handles SSL redirect, HSTS)
     - `SessionMiddleware` before `AuthenticationMiddleware`
     - `CsrfViewMiddleware` before any view-processing middleware
   - Are there custom middleware that could interfere with Django's security middleware?

5. **Static and Media Files:**
   - Is Django serving static files in production? (`django.contrib.staticfiles` with `DEBUG=True` serves files — this should be handled by nginx/CDN in production)
   - Is `MEDIA_URL` pointing to a path that could conflict with URL patterns?
   - Are uploaded files served through Django views with access control, or directly by the web server? (direct serving bypasses auth)
