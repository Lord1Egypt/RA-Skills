# OpenRewrite Recipe-First Migration

**Version policy:** Do not hardcode plugin or recipe versions. Look up current versions from [OpenRewrite Maven plugin](https://docs.openrewrite.org/reference/rewrite-maven-plugin), [rewrite-spring](https://github.com/openrewrite/rewrite-spring/releases), and [rewrite-migrate-java](https://github.com/openrewrite/rewrite-migrate-java/releases) (or Gradle plugin docs) and substitute in the snippets below.

## When to load this file

Load this file when you need concrete OpenRewrite setup and run commands for Spring Boot 2.7.x → 3.x (the spring-boot-2-to-3 skill assumes a 2.7.x baseline).

## Stage-oriented execution (toolkit-style)

Use this order to keep migration controllable:

1. Run baseline checks and save outputs.
2. Run rewrite recipes in small batches.
3. Build and test after each batch.
4. Save diff and failure logs before moving to manual fixes.

## Maven setup

Add plugin (replace `REWRITE_MAVEN_PLUGIN_VERSION`, `REWRITE_SPRING_VERSION`, and `REWRITE_MIGRATE_JAVA_VERSION` with current versions from the links above):

```xml
<plugin>
  <groupId>org.openrewrite.maven</groupId>
  <artifactId>rewrite-maven-plugin</artifactId>
  <version>REWRITE_MAVEN_PLUGIN_VERSION</version>
  <configuration>
    <activeRecipes>
      <recipe>org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_5</recipe>
      <recipe>org.openrewrite.java.migrate.UpgradeToJava21</recipe>
    </activeRecipes>
  </configuration>
  <dependencies>
    <dependency>
      <groupId>org.openrewrite.recipe</groupId>
      <artifactId>rewrite-spring</artifactId>
      <version>REWRITE_SPRING_VERSION</version>
    </dependency>
    <dependency>
      <groupId>org.openrewrite.recipe</groupId>
      <artifactId>rewrite-migrate-java</artifactId>
      <version>REWRITE_MIGRATE_JAVA_VERSION</version>
    </dependency>
  </dependencies>
</plugin>
```

Run:

```bash
./mvnw -U org.openrewrite.maven:rewrite-maven-plugin:run
```

Default target is **Spring Boot 3.5.x** (current stable line). One-shot command without editing pom:

```bash
./mvnw -U org.openrewrite.maven:rewrite-maven-plugin:run \
  -Drewrite.recipeArtifactCoordinates=org.openrewrite.recipe:rewrite-spring:LATEST \
  -Drewrite.activeRecipes=org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_5
```

Multi-module (single module run):

```bash
./mvnw -U org.openrewrite.maven:rewrite-maven-plugin:run \
  -Drewrite.recipeArtifactCoordinates=org.openrewrite.recipe:rewrite-spring:LATEST \
  -Drewrite.activeRecipes=org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_5 \
  -pl <module-name>
```

## Gradle setup

Add plugin, **dependencies** (rewrite-spring, rewrite-migrate-java), and recipes (replace version placeholders from OpenRewrite Gradle plugin docs and recipe releases; align target with Maven strategy):

```groovy
plugins {
  id("org.openrewrite.rewrite") version "REWRITE_GRADLE_PLUGIN_VERSION"
}

dependencies {
  rewrite("org.openrewrite.recipe:rewrite-spring:REWRITE_SPRING_VERSION")
  rewrite("org.openrewrite.recipe:rewrite-migrate-java:REWRITE_MIGRATE_JAVA_VERSION")
}

rewrite {
  activeRecipe(
    "org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_5",
    "org.openrewrite.java.migrate.UpgradeToJava21",
    "org.openrewrite.java.migrate.jakarta.JavaxToJakarta"
  )
}
```

Run:

```bash
./gradlew rewriteRun
```

## Recommended recipe sequence

Use targeted sequence when needed instead of one large jump:

1. Choose Java target recipe:
   - `org.openrewrite.java.migrate.UpgradeToJava17` (if runtime baseline remains Java 17)
   - `org.openrewrite.java.migrate.UpgradeToJava21` (if target baseline is Java 21)
2. `org.openrewrite.java.spring.boot2.UpgradeSpringBoot_2_7`
3. `org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_0`
4. `org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_1` (optional if target is 3.1+)
5. `org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_2` (optional if target is 3.2+)
6. `org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_5` (prefer this—3.5.x is the target line; 3.0–3.4 are transition)
7. `org.openrewrite.java.migrate.jakarta.JavaxToJakarta` (if not already included by selected recipe set)

For newer target versions, continue with corresponding `UpgradeSpringBoot_3_x` recipes.

## Auto-migrated scenarios to expect

When running an `UpgradeSpringBoot_3_x` recipe (e.g. 3_5), the recipe chain typically covers the following. Exact set depends on target version—see [OpenRewrite recipe reference](https://docs.openrewrite.org/recipes/java/spring/boot3) for the chosen recipe.

**Build and dependencies**

- Maven/Gradle: Boot parent and plugin versions, `java.version`, Spring BOM and related dependency versions (Spring Framework, SpringDoc, Hibernate, Flyway, Micrometer, GraalVM native plugin, etc.).
- Cassandra: `com.datastax.oss` → `org.apache.cassandra` groupId where applicable.

**Code and annotations**

- `javax.*` imports to `jakarta.*`
- Remove redundant `@Autowired` on single constructor.
- `@RequestMapping(method = GET/POST/...)` to `@GetMapping` / `@PostMapping` / etc.; `@PathVariable("id")` to `@PathVariable` (optional name).
- `WebSecurityConfigurerAdapter` to `SecurityFilterChain` bean style.
- `WebMvcConfigurerAdapter` to `WebMvcConfigurer`; `HandlerInterceptorAdapter` to `HandlerInterceptor`; `AsyncConfigurerSupport` to `AsyncConfigurer`.
- JUnit 4 → JUnit 5: `@RunWith(SpringRunner.class)` removed, `@Before`/`@After` to `@BeforeEach`/`@AfterEach`, `public` test methods to package-private where applicable.
- Apache HttpClient 4 package/API usage toward HttpClient 5.
- `HttpStatus` parameters/returns toward `HttpStatusCode` where applicable.
- `MediaType.APPLICATION_JSON_UTF8_VALUE` to `APPLICATION_JSON_VALUE`.

**Configuration properties**

- `spring.datasource.schema` / `spring.datasource.data` → `spring.sql.init.schema-locations` / `spring.sql.init.data-locations`.
- `spring.datasource.initialization-mode` → `spring.sql.init.mode`.
- `management.contextPath` → `management.server.base-path`.
- Other version-specific keys via chained `SpringBootProperties_3_x` recipes.

**Chained framework migrations (version-dependent)**

- Spring Security 6.x API and config.
- Hibernate 6.x, Flyway 10, Micrometer 1.13+. For API docs: with **Boot 3.5** use **springdoc-openapi 2.8.x** (springdoc 3.0.0 is for Spring Boot 4).

Treat this as "usually covered, still verify by compile/test". For the authoritative list for a given recipe, see its definition and recipeList on the OpenRewrite docs.

## Practical run strategy

1. Run recipes on a clean branch.
2. Commit generated changes immediately after each major recipe group.
3. Build and run tests between groups.
4. Only then start manual edits.
5. Keep one migration log per stage (commands, output, blockers).

Quick verification helpers:

```bash
git diff --stat
./mvnw -q -DskipTests compile
./mvnw -q test
./mvnw dependency:tree | rg "spring-boot|httpclient5|httpcore5"
```

## Dockerfile upgrade

OpenRewrite supports Dockerfile changes via [rewrite-docker](https://github.com/openrewrite/rewrite-docker). Use it to align the **Java base image** with the target JDK (17 or 21) for Boot 3. If the container runs the app with `java -jar`, the image used in that step (or the final stage of a multi-stage build) must be 17+; the `java -jar` command itself stays the same.

**Recipe**: `org.openrewrite.docker.ChangeFrom` — change the base image in a Dockerfile `FROM` instruction. It requires configuration (e.g. `oldImageName`, `newImageName`, `newTag`). See [Change Docker FROM](https://docs.openrewrite.org/recipes/docker/changefrom).

**Maven**: add the plugin dependency (replace `REWRITE_DOCKER_VERSION` with current version from [Maven Central](https://central.sonatype.com/artifact/org.openrewrite/rewrite-docker)):

```xml
<dependency>
  <groupId>org.openrewrite</groupId>
  <artifactId>rewrite-docker</artifactId>
  <version>REWRITE_DOCKER_VERSION</version>
</dependency>
```

Because `ChangeFrom` has required parameters, define a named recipe in `rewrite.yml` (project root) that sets them, then activate that recipe. Example for upgrading Eclipse Temurin 11 → 21:

```yaml
---
type: specs.openrewrite.org/v1beta/recipe
name: com.yourorg.UpgradeDockerfileJava21
displayName: Upgrade Dockerfile Java base to 21
recipeList:
  - org.openrewrite.docker.ChangeFrom:
      oldImageName: eclipse-temurin
      newImageName: eclipse-temurin
      newTag: "21-jdk-jammy"
```

Activate `com.yourorg.UpgradeDockerfileJava21` in the plugin and run `./mvnw -U org.openrewrite.maven:rewrite-maven-plugin:run`. Run Docker recipes in a separate pass or with the Boot upgrade; commit as e.g. `chore(rewrite): Boot 3.5 + Dockerfile Java 21 base image`.

**Alternative (text-based)**: For a simple image tag bump, use `org.openrewrite.text.FindAndReplace` with `filePattern: "**/Dockerfile"`, `find: "eclipse-temurin:11-jdk"`, `replace: "eclipse-temurin:21-jdk"`. See [Running text based recipes](https://docs.openrewrite.org/running-recipes/running-text-based-recipes).

**Docs**: [OpenRewrite Docker recipes](https://docs.openrewrite.org/recipes/docker).

## Common follow-up after rewrite

- Fix dependencies not managed by Spring Boot BOM.
- Resolve `javax.*` imports still left from third-party APIs.
- Replace removed/deprecated APIs that recipes do not touch.
- Upgrade Dockerfile Java base image to 17+ or 21 (see **Dockerfile upgrade** above).
