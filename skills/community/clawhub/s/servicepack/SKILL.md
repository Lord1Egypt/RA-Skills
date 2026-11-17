---
name: servicepack
description: Build a Go service on psyb0t/servicepack — clone-and-own framework (not a `go get` library) providing a Service interface (Name/Run/Stop), a singleton ServiceManager that runs services concurrently with dependency-ordered topological start, automatic retry (Retryable), non-fatal failures (AllowedFailure), readiness gating (ReadyNotifier), per-service CLI subcommands (Commander), an App singleton with OnPreRun/OnPostStop lifecycle hooks, gofindimpl-based service auto-discovery codegen, ctxscope/slogging structured logging, and a graceful-shutdown Runner. Import path github.com/psyb0t/servicepack. Use when the user wants related Go services debugged together locally, then deployed as one binary or split into separate microservices, with retry/dependency/readiness semantics.
homepage: https://github.com/psyb0t/servicepack
user-invocable: true
permissions:
  filesystem:
    read:
      - "**/*.go"
      - "go.mod"
      - "go.sum"
      - "Makefile*"
      - "README.md"
    write:
      - "internal/pkg/services/**"
      - "cmd/init.go"
      - "cmd/commands.go"
  shell:
    - "make dev-image"
    - "make service NAME=*"
    - "make service-registration"
    - "make build"
    - "make test"
    - "make test-integration"
    - "make test-coverage"
    - "make lint"
    - "make format"
metadata:
  openclaw:
    emoji: "📦"
    requires:
      bins:
        - docker
---

# servicepack — build a Go service on the framework

`servicepack` runs your Go services concurrently without you hand-rolling a supervisor loop. It is NOT a package you `go get` into an existing project — it's a **template repo you clone and make your own**, then you add services under `internal/pkg/services/`. This skill teaches you to build a service with it, not to run it as a standalone server (there's nothing to run until you write a service).

## Security & safety

servicepack is source code you compile into your own binary — it has no runtime surface of its own, no network listener, no daemon to secure. Once cloned it's just Go files in your repo; whatever surface your SERVICE exposes (HTTP, gRPC, DB connections) is on you, same as any Go code you'd write by hand. The only things worth flagging:

- `make own MODNAME=...` rewrites `go.mod`, nukes `.git`, and re-inits — irreversible on the clone, run it once at the start.
- `internal/app/`, `internal/pkg/service-manager/`, `pkg/runner/`, and `cmd/main.go` are framework-owned files that `make servicepack-update` overwrites — never hand-edit them (see "Framework boundaries" below).
- No secrets, tokens, or credentials live in the framework itself. Your services' env vars are your own to manage (`gonfiguration`, not `os.Getenv`).

## When to use

- Starting a new Go service/daemon that needs to run one or more long-lived workers concurrently, with clean shutdown on SIGINT/SIGTERM.
- You need retry-on-failure, non-fatal ("allowed failure") services, dependency-ordered startup, or readiness gating between services in the same process.
- You want per-service CLI subcommands (`./app <service> migrate`) alongside the long-running `./app run`.
- You're adding a new service to a repo that already has `servicepack.version`, `Makefile.servicepack`, or `internal/pkg/service-manager/` present.

## When NOT to use

- You need a single, simple `main()` with no concurrent workers — plain Go is less ceremony.
- You're building an HTTP API only, no background workers — reach for `aichteeteapee` directly in a plain `main.go`; servicepack's value is the multi-service supervisor, not routing.
- You want a library to import into an EXISTING app without restructuring around `cmd/`, `internal/app/`, `internal/pkg/services/`. servicepack expects to own your project's top-level shape.

## Quick start

```bash
git clone https://github.com/psyb0t/servicepack
cd servicepack
make own MODNAME=github.com/yourname/yourproject
make service NAME=my-worker
```

`make service` scaffolds `internal/pkg/services/my-worker/my-worker.go`:

```go
package myworker

import (
	"context"

	"github.com/psyb0t/ctxerrors"
	"github.com/psyb0t/ctxscope"
	"github.com/psyb0t/gonfiguration"
)

const ServiceName = "my-worker"

type Config struct {
	Value string `env:"MYWORKER_VALUE" default:"default-value"`
}

type MyWorker struct {
	config Config
}

func New() (*MyWorker, error) {
	cfg := Config{}

	if err := gonfiguration.Parse(&cfg); err != nil {
		return nil, ctxerrors.Wrap(err, "parse my-worker config")
	}

	return &MyWorker{config: cfg}, nil
}

func (s *MyWorker) Name() string {
	return ServiceName
}

func (s *MyWorker) Run(ctx context.Context) error {
	ctx = ctxscope.Set(ctx, ctxscope.Attr("service", ServiceName))
	logger := ctxscope.GetLogger(ctx)
	logger.Info("starting service")

	<-ctx.Done()
	logger.Info("service context cancelled")

	return nil
}

func (s *MyWorker) Stop(ctx context.Context) error {
	serviceCtx := ctxscope.Set(ctx, ctxscope.Attr("service", ServiceName))
	ctxscope.GetLogger(serviceCtx).Info("stopping service")

	return nil
}
```

Edit the `Run()` body, then `make service-registration` regenerates `internal/pkg/services/services.gen.go` (auto-discovers every `Service` implementation via `gofindimpl`). Build and run:

```bash
make build
./build/yourproject run
```

## The Service interface

Every service implements:

```go
type Service interface {
	Name() string
	Run(ctx context.Context) error
	Stop(ctx context.Context) error
}
```

`Run()` listens for `ctx.Done()` and returns cleanly on cancellation; a non-nil return from `Run()` stops all services (unless the service is an `AllowedFailure`, see below). `Stop()` runs during shutdown for cleanup.

## Optional interfaces — opt into extra behavior

A service can implement any combination of these on top of `Service`:

```go
// Retryable — service gets restarted on failure, up to MaxRetries times,
// waiting RetryDelay between attempts.
type Retryable interface {
	MaxRetries() int
	RetryDelay() time.Duration
}

// AllowedFailure — service can die (even after exhausting retries)
// without killing the rest of the process.
type AllowedFailure interface {
	IsAllowedFailure() bool
}

// Dependent — service manager topologically sorts start order;
// services with no deps start first.
type Dependent interface {
	Dependencies() []string // names of other services in this process
}

// ReadyNotifier — service manager waits for this channel to close
// before starting anything that depends on this service.
type ReadyNotifier interface {
	Ready() <-chan struct{}
}

// Commander — exposes CLI subcommands under the service's own
// namespace: ./app <servicename> <subcommand>. Only that service
// gets instantiated when its command runs.
type Commander interface {
	Commands() []*cobra.Command
}
```

Dependencies on services not present in the current process (e.g. another microservice) are skipped with a debug log, not an error — cyclic dependencies within the process ARE rejected at startup.

**`Dependent` alone orders the LAUNCH, not the readiness.** A service that does not implement `ReadyNotifier` is treated as ready the moment its goroutine is launched, so its dependents are started right after — possibly before its `Run` body has executed a single line. If a dependent genuinely must not start until the dependency is accepting work (a DB accepting connections, a listener bound), the dependency has to implement `ReadyNotifier` and close its channel when it is actually up. Combining `Dependent` with `ReadyNotifier` is what turns "started in the right order" into "started only once the dependency works".

## Lifecycle hooks — customize without touching framework files

`cmd/init.go` is yours; it's never overwritten by `make servicepack-update`. Register hooks on the `App` singleton:

```go
// cmd/init.go
package main

import (
	"context"

	"github.com/yourname/yourproject/internal/app"
)

func init() {
	app.GetInstance().OnPreRun(func(ctx context.Context) {
		// runs before any service starts
	})

	app.GetInstance().OnPostStop(func(ctx context.Context) {
		// runs after all services have stopped
	})
}
```

Hooks run sequentially in registration order; multiple hooks are allowed.

## Custom CLI commands

`cmd/commands.go` is also yours — add standalone cobra commands separate from per-service `Commander` commands:

```go
// cmd/commands.go
package main

import "github.com/spf13/cobra"

func commands() []*cobra.Command {
	return []*cobra.Command{
		{
			Use:   "seed",
			Short: "Seed the database",
			Run: func(_ *cobra.Command, _ []string) {
				// your logic
			},
		},
	}
}
```

## Logging and config

- Logging is `ctxscope` over `log/slog`, with `github.com/psyb0t/slogging/slogconf` wiring the default handler. Add extra `slog.Handler`s (Loki, Datadog, etc.) in `cmd/init.go`; set durable identity fields with `ctxscope.Set(ctx, ...)`, then log through `ctxscope.GetLogger(ctx)`.
- Config is `github.com/psyb0t/gonfiguration` — struct tags (`env:"MYWORKER_VALUE"`), `gonfiguration.Parse(&cfg)`, `gonfiguration.SetDefaults(map[string]any{...})`. Never `os.Getenv` directly.
- Errors are wrapped with `github.com/psyb0t/ctxerrors` (`ctxerrors.Wrap(err, "doing X")`) for file/line/function context.

## Framework boundaries — never hand-edit these

`internal/app/`, `internal/pkg/service-manager/`, `pkg/runner/`, `cmd/main.go`, `Makefile.servicepack`, `scripts/make/servicepack/`, `Dockerfile.servicepack*`, `servicepack.version` are all overwritten by `make servicepack-update`. Customize behavior through the lifecycle hooks above, not by patching these files. Everything under `internal/pkg/services/`, `docs/`, and `tests/`, plus `Makefile`, `Dockerfile`, `Dockerfile.dev`, `cmd/init.go`, `cmd/commands.go`, is yours and never touched by updates.

## Filtering which services run

```bash
export SERVICES_ENABLED="my-worker,another-service"   # comma-separated; unset/empty = all
./build/yourproject run
```

## Further reading

`references/setup.md` has the install/module details, Docker/toolchain requirements, and a fuller worked example with `Retryable` + `Dependent` + `ReadyNotifier` combined.
