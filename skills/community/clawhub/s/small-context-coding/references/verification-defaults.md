# Verification Defaults

Use the smallest meaningful verification step for the stack in front of you.
Do not run the whole world if one focused command is enough.

## Python

### Small change
- targeted pytest test
- direct script execution for the affected path
- focused lint on touched files when configured

### Good defaults
```bash
pytest path/to/test_file.py -q
pytest -k "login_timeout" -q
python path/to/script.py
ruff check path/to/file.py
```

## TypeScript / JavaScript

### Small change
- targeted test file
- package-level test for affected area
- typecheck for the package if types are central to the change
- focused lint on touched files when available

### Good defaults
```bash
pnpm test -- --runInBand path/to/test.spec.ts
pnpm vitest run path/to/test.spec.ts
pnpm exec tsc --noEmit
pnpm eslint path/to/file.ts
npm test -- path/to/test.spec.ts
```

## React / Frontend

### Small change
- component test or page-level test
- typecheck if props or API contracts changed
- build only if the change crosses bundling or config boundaries

### Good defaults
```bash
pnpm vitest run src/components/Button.test.tsx
pnpm exec tsc --noEmit
pnpm build
```

## Node backend

### Small change
- targeted route/service test
- typecheck if TS backend
- focused integration test if request/response behavior changed

### Good defaults
```bash
pnpm vitest run src/api/auth.test.ts
pnpm exec tsc --noEmit
npm test -- auth
```

## Go

### Small change
- targeted package test
- build the affected package or binary if behavior is compile-sensitive

### Good defaults
```bash
go test ./path/to/package -run TestLoginTimeout -v
go test ./path/to/package
go build ./cmd/service
```

## Rust

### Small change
- targeted cargo test
- cargo check for affected crate

### Good defaults
```bash
cargo test login_timeout
cargo test -p my_crate
cargo check -p my_crate
```

## Java / Kotlin

### Small change
- targeted gradle/maven test
- compile or package module if signature changes are involved

### Good defaults
```bash
./gradlew test --tests "*LoginTimeout*"
./gradlew :app:test
./gradlew :app:compileJava
mvn -Dtest=LoginTimeoutTest test
```

## C# / .NET

### Small change
- targeted test project or filter
- build affected solution/project when signatures or DI wiring changed

### Good defaults
```bash
dotnet test --filter LoginTimeout
dotnet test path/to/Tests.csproj
dotnet build path/to/App.csproj
```

## Ruby

### Small change
- targeted rspec/minitest file
- focused lint when configured

### Good defaults
```bash
bundle exec rspec spec/services/login_timeout_spec.rb
bundle exec rubocop path/to/file.rb
```

## PHP

### Small change
- targeted phpunit/pest test
- focused static analysis if configured

### Good defaults
```bash
php artisan test --filter=LoginTimeout
vendor/bin/phpunit tests/Feature/LoginTimeoutTest.php
vendor/bin/phpstan analyse path/to/file.php
```

## Shell / Infra / Config

### Small change
- syntax validation
- targeted dry run
- linter or formatter when available

### Good defaults
```bash
bash -n script.sh
shellcheck script.sh
terraform validate
terraform plan
ansible-playbook site.yml --check
```

## Selection rules

Prefer this order when choosing verification:
1. test closest to changed behavior
2. compile/typecheck closest to changed module
3. broader package or service build
4. full project verification only when local checks are insufficient

## Reporting

When reporting completion, mention:
- what command was run
- whether it passed
- what was not verified, if anything
