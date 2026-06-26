# Taint Profiles

This file defines source/sink/sanitizer typing used by `run_pure_llm.py` in local Web App mode.

## Java Web Profile

### Source types
- `spring_mapping`: Spring mapping annotations (`@RequestMapping`, `@GetMapping`, ...)
- `request_binding`: request-bound parameters (`@RequestParam`, `@PathVariable`, `@RequestBody`, ...)
- `servlet_request`: direct servlet request access (`HttpServletRequest`, `getParameter`, ...)
- `multipart_upload`: upload/file-input points (`MultipartFile`, `getPart`, ...)

### Sink types
- `jdbc_execution`: SQL execution APIs (`JdbcTemplate.*`, `createStatement`, ...)
- `mybatis_dollar`: MyBatis `${}` interpolation
- `command_exec`: command execution (`Runtime.exec`, `ProcessBuilder`)
- `file_access`: file/path operations (`File`, `Paths.get`, `Files.*`)
- `ssrf_network`: outbound HTTP/network clients (`URL`, `RestTemplate`, `WebClient`, ...)
- `unsafe_deser`: deserialization (`ObjectInputStream`, `readObject`)
- `template_eval`: expression/template execution (`SpEL`, `TemplateEngine`, ...)

### Sanitizer types
- `bean_validation`: Bean Validation annotations (`@Valid`, `@NotNull`, ...)
- `prepared_stmt_usage`: prepared-statement parameter binding
- `path_canonicalization`: canonicalization (`getCanonicalPath`, `normalize`, ...)
- `escaping_utils`: escaping utilities (`StringEscapeUtils`, `ESAPI`, ...)
- `allowlist_checks`: allowlist/whitelist checks

## Python Web Profile

### Source types
- `flask_request`: Flask request inputs (`request.args`, `request.form`, `get_json`, ...)
- `django_request`: Django request inputs (`request.GET`, `request.POST`, `request.body`, ...)
- `fastapi_params`: FastAPI parameter declarations (`Query`, `Body`, `Path`, ...)
- `url_params`: route/query parameter extraction helpers

### Sink types
- `sql_execution`: SQL execution calls (`cursor.execute`, `raw`, `extra`, ...)
- `command_exec`: command execution (`os.system`, `subprocess.*`)
- `file_access`: file/path operations (`open`, `Path`, `send_file`, ...)
- `ssrf_network`: outbound HTTP/network (`requests.*`, `httpx.*`, `urlopen`)
- `unsafe_deser`: unsafe deserialization (`pickle.loads`, `yaml.load`)
- `template_eval`: template render/eval (`render_template_string`, `eval`, `exec`, ...)

### Sanitizer types
- `pydantic_validation`: Pydantic schema validation (`BaseModel`, `Field`, ...)
- `django_forms_validation`: Django/serializer validation (`is_valid`, `cleaned_data`, ...)
- `parameterized_sql`: parameterized SQL invocation patterns
- `escaping_utils`: escaping/filtering (`bleach.clean`, `markupsafe.escape`, ...)
- `path_canonicalization`: path normalization (`resolve`, `realpath`, `normpath`)

## Notes

- These profiles provide candidate taint-flow anchors and are intentionally high recall.
- Treat hits as triage signals; confirm reachability and exploitability with manual tracing.
- Java `mybatis_dollar` sink typing is narrowed to mapper XML SQL contexts to reduce placeholder noise from build/config files.
