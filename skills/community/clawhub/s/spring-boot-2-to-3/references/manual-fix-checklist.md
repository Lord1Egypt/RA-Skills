# Manual Fix Checklist (After OpenRewrite)

## When to load this file

Load this file after running rewrite recipes and when compile/test failures remain.

## Stage output requirement

For each fix stage, always record:

1. Commands executed
2. Files/modules changed
3. Blocking issues
4. Validation result

## 1) Java and Runtime Baseline

- Ensure JDK 17+ is configured in **build** (e.g. `java.version` in pom, `sourceCompatibility` in Gradle) and in **CI** (e.g. GitHub Actions `java: '17'`, Jenkins JDK 17, GitLab CI image). Update CI config if it still uses Java 11 or 8.
- Ensure container/runtime images use Java 17+ (see **Dockerfile / container image** below).

## 2) Dockerfile / container image

- Align the **Java base image** in `Dockerfile` (or equivalent) with the target JDK (17 or 21). Boot 3 requires Java 17+.
- If the Dockerfile runs the app with **`java -jar`** (or `java -cp`), the **image** that runs that command must be Java 17+ (e.g. `eclipse-temurin:21-jdk` or `eclipse-temurin:21-jre`). The `java -jar` command itself does not need to change; only the runtime (base image) does. In multi-stage builds, upgrade the **final stage** image as well.
- **OpenRewrite**: Use the [rewrite-docker](https://github.com/openrewrite/rewrite-docker) module. Add dependency `org.openrewrite:rewrite-docker` and run the **Change Docker FROM** recipe to update the base image (e.g. `eclipse-temurin:11-jdk` → `eclipse-temurin:21-jdk`). See [OpenRewrite Docker recipes](https://docs.openrewrite.org/recipes/docker) and [references/openrewrite-recipes.md](openrewrite-recipes.md#dockerfile-upgrade).
- **Alternative**: Use a text-based recipe (e.g. `org.openrewrite.text.FindAndReplace`) with `filePattern: "**/Dockerfile"` to replace the image name/version if you only need a simple bump.
- Rebuild the image and run a quick container smoke test (e.g. start app, hit health endpoint).

## 3) `javax` -> `jakarta`

- Replace imports such as:
  - `javax.servlet.*` -> `jakarta.servlet.*`
  - `javax.validation.*` -> `jakarta.validation.*`
  - `javax.persistence.*` -> `jakarta.persistence.*`
- Verify all related dependencies are Jakarta-compatible.

## 4) Spring Security Migration

- Replace `WebSecurityConfigurerAdapter` style config with `SecurityFilterChain` bean config.
- Re-check URL matchers and method security annotations for behavior drift.
- Re-test authentication and authorization flows.

## 5) Web and Serialization

- Check Spring MVC/WebFlux exception handling and binding behavior.
- Replace `WebMvcConfigurerAdapter` usage that might remain after recipe runs.
- Replace `HandlerInterceptorAdapter` usage that might remain after recipe runs.
- Re-check Jackson and date/time serialization compatibility.
- Re-validate custom converters, interceptors, and filters.

## 6) Data and Persistence

- Verify Hibernate/JPA version compatibility with Boot 3.
- Re-check generated SQL and schema management behavior.
- Test transaction boundaries and lazy-loading sensitive paths.

## 7) API Documentation and Observability

- If using Springfox, migrate to **springdoc-openapi 2.8.x** for Spring Boot 3.5 (use the 2.8.x release that matches your Boot 3.5.x). Do not use springdoc-openapi 3.0.0 with Boot 3.5—3.0.0 targets Spring Boot 4.
- Verify Micrometer/Actuator endpoint exposure and metric naming changes.
- Validate health/readiness/liveness endpoints used by deployment platform.

## 8) Dependency and HTTP stack

- Check HttpClient5/HttpCore5 version alignment to avoid runtime `NoSuchMethodError`.
- Validate `RestTemplate`/HTTP client bean construction and timeout settings.
- If `setReadTimeout` style code no longer works with target HTTP client APIs, migrate to `RequestConfig` + explicit timeout types.
- If the project uses **Spring Cloud**, align the Spring Cloud BOM version with Boot 3.5 (e.g. 2024.0.x). Check [Spring Cloud release train compatibility](https://spring.io/projects/spring-cloud) with the chosen Boot version.
- If the project uses **GraalVM native image** build, re-run the native build after migration and fix any new reflection or resource hints if needed.

## 9) Test and Framework API migration

- Confirm JUnit 4 remnants are fully migrated to JUnit 5 annotations and assertions.
- Re-check exception handlers that changed from `HttpStatus` parameters/return usage to `HttpStatusCode` patterns.
- Replace `APPLICATION_JSON_UTF8_VALUE` and similar removed constants.

## 10) Custom Recipe opportunity (repeatable fixes)

- For repeated internal API migration tasks, create custom OpenRewrite recipes instead of repeating manual edits.
- Typical candidates:
  - Internal shared library package/class migration
  - Cross-service annotation rename
  - Repeated dependency version alignment

## 11) Test and Release Gate

- Run full test suite.
- Run smoke tests for startup, login, critical APIs, and data writes.
- Compare key logs/metrics before and after migration.
- Document known gaps and rollback plan before production rollout.
- Keep migration stage reports so later rollback or audit can trace each change set.

## 12) Common error triage

- `NoSuchMethodError` in HttpComponents:
  - Verify `httpclient5` and `httpcore5` are compatible versions in dependency tree.
- `Failed to load ApplicationContext`:
  - Check final `caused by` chain; common roots are `@Bean` signature issues, security config mismatch, and dependency conflicts.
- `BeanCreationException` around `RestTemplate`:
  - Re-check HTTP client wiring and aligned dependency versions.
