---
name: Spring Boot (Java)
detect:
  files: ["pom.xml", "build.gradle", "build.gradle.kts"]
  dependencies: ["spring-boot-starter-web", "spring-boot-starter-security", "spring-framework"]
  keywords: ["Spring Boot", "Spring", "Java"]
---

## recon-agent

**Spring Boot Discovery:**
1. Glob for `**/application.yml`, `**/application.properties`, `**/application-*.yml`, `**/application-*.properties` — these contain runtime configuration per profile
2. Glob for `**/SecurityConfig.java`, `**/WebSecurityConfig*`, `**/*SecurityConfiguration*` — security filter chain definitions
3. Check for `management.endpoints.web.exposure.include` in properties — this controls which Actuator endpoints are exposed
4. Check for `@Profile` annotations that conditionally enable/disable security

## attack-surface-http

**Spring MVC / WebFlux Entry Points:**
1. Grep for `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`, `@PatchMapping`, `@RequestMapping` — these define all HTTP endpoints
   - For each: is `@PreAuthorize`, `@Secured`, or `@RolesAllowed` present?
   - Are there endpoints missing security annotations that should have them?
2. **SpEL Injection:**
   - Grep for `@Value("${...}")` and `@PreAuthorize("...")` with user-controlled expressions
   - If `SpelExpressionParser` is used directly: is the input sanitized before evaluation?
   - Can an attacker inject SpEL via `@PathVariable`, `@RequestParam`, or `@RequestBody` values that are used in expression evaluation?
3. **Mass Assignment / Autobinding:**
   - Are `@ModelAttribute` or `@RequestBody` used to directly bind JSON/form data to JPA entities?
   - Is `@JsonIgnore` or `@JsonProperty(access = READ_ONLY)` used on sensitive fields (id, role, isAdmin)?
   - Can an attacker send extra fields that get bound to the entity and persisted?
4. **Path Traversal via `@PathVariable`:**
   - Are path variables used in file operations without sanitization?
   - Does `ResourceHttpRequestHandler` serve static files from configurable paths?
5. **Deserialization:**
   - Is `ObjectMapper` configured to restrict polymorphic deserialization? (`activateDefaultTyping` is dangerous)
   - Are there endpoints accepting `application/xml` that use JAXB or Jackson XML? (XXE risk)
   - Grep for `@RequestBody Object` or `@RequestBody Map` — loose typing enables injection

## attack-surface-authz

**Spring Security Filter Chain:**
1. Read the SecurityFilterChain / WebSecurityConfigurerAdapter configuration
   - Is `.permitAll()` applied too broadly? (e.g., `/**` patterns before specific restrictions)
   - Is `.authenticated()` or `.hasRole()` applied to all sensitive endpoints?
   - Does the filter chain order matter? Are custom filters inserted at the right position?
2. **Method-Level Security:**
   - Is `@EnableMethodSecurity` (or `@EnableGlobalMethodSecurity`) active?
   - Are there service methods missing `@PreAuthorize` that modify sensitive data?
   - Can SpEL expressions in `@PreAuthorize` be bypassed? (e.g., `#id == principal.id` — does it handle null safely?)
3. **CSRF Configuration:**
   - Is CSRF protection disabled? (`http.csrf().disable()` or `http.csrf(csrf -> csrf.disable())`)
   - If disabled, is the app stateless JWT only? (CSRF not needed for purely token-based auth)
   - If enabled, are there endpoints excluded from CSRF that shouldn't be?

## config-infrastructure

**Actuator Exposure:**
1. Check if Spring Boot Actuator is on the classpath (Grep for `spring-boot-starter-actuator` in pom.xml/build.gradle)
2. If present:
   - Is `management.endpoints.web.exposure.include=*`? (exposes ALL actuator endpoints including `/env`, `/heapdump`, `/beans`)
   - Is `/actuator/env` exposed? It reveals all environment variables including secrets
   - Is `/actuator/heapdump` exposed? It contains a JVM heap dump with in-memory secrets
   - Is `/actuator/shutdown` exposed? It can remotely stop the application
   - Is the management port different from the application port? (`management.server.port`)
   - Are actuator endpoints behind authentication?
3. **Thymeleaf Server-Side Template Injection (SSTI):**
   - If Thymeleaf is used: are there templates that include user-controlled content via `th:utext` (unescaped)?
   - Can an attacker inject Thymeleaf expressions via `__${...}__` preprocessing?
   - Is fragment injection possible via URL path manipulation?
4. **Spring Profiles:**
   - Is `spring.profiles.active` configurable via environment? Can an attacker switch to a dev/debug profile?
   - Does the `dev` or `test` profile disable security features that are enabled in `prod`?
   - Are there profile-specific properties that weaken security (e.g., `debug=true`, `logging.level.root=DEBUG`)?
5. **H2 Console:**
   - Is the H2 database console enabled? (`spring.h2.console.enabled=true`)
   - Is it accessible in production? (provides direct SQL access to the database)

## dependency-audit

**Spring-Specific Dependency Concerns:**
1. Check Spring Boot version against known CVEs (Spring4Shell CVE-2022-22965, Spring Cloud Function SpEL injection CVE-2022-22963)
2. Is `jackson-databind` updated? (frequent CVEs in polymorphic deserialization)
3. Is `log4j-core` present? Check version for Log4Shell (CVE-2021-44228)
4. Is `snakeyaml` updated? (deserialization vulnerabilities in older versions)
5. Are `spring-boot-devtools` excluded from production builds?
