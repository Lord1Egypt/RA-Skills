---
title: Test Hooks and Routes with tests.NewTestApp and ApiScenario
instead of Curl
impact: HIGH
impactDescription: Without the tests package you cannot exercise hooks, middleware, and transactions in isolation
tags: testing, tests, NewTestApp, ApiScenario, go, extending
---

## Test Hooks and Routes with tests.NewTestApp and ApiScenario

PocketBase ships a `tests` package specifically for integration-testing Go extensions. `tests.NewTestApp(testDataDir)` builds a fully-wired `core.App` over a **temp copy** of your test data directory, so you can register hooks, fire requests through the real router, and assert on the resulting DB state without spinning up a real HTTP server or touching `pb_data/`. The `tests.ApiScenario` struct drives the router the same way a real HTTP client would, including middleware and transactions. Curl-based shell tests cannot do either of these things.

**Incorrect (hand-rolled HTTP client, shared dev DB, no hook reset):**

```go
// ❌ Hits the actual dev server - depends on side-effects from a previous run
func TestCreatePost(t *testing.T) {
    resp, _ := http.Post("http://localhost:8090/api/collections/posts/records",
        "application/json",
        strings.NewReader(`{"title":"hi"}`))
    if resp.StatusCode != 200 {
        t.Fatal("bad status")
    }
    // ❌ No DB assertion, no cleanup, no hook verification
}
```

**Correct (NewTestApp + ApiScenario + AfterTestFunc assertions):**

```go
// internal/app/posts_test.go
package app_test

import (
    "net/http"
    "strings"
    "testing"

    "github.com/pocketbase/pocketbase/core"
    "github.com/pocketbase/pocketbase/tests"

    "myapp/internal/hooks" // your hook registration
)

// testDataDir is a checked-in pb_data snapshot with your collections.
// Create it once with `./pocketbase --dir ./test_pb_data migrate up`
// and commit it to your test fixtures.
const testDataDir = "../../test_pb_data"

func TestCreatePostFiresAudit(t *testing.T) {
    // Each test gets its own copy of testDataDir - parallel-safe
    app, err := tests.NewTestApp(testDataDir)
    if err != nil {
        t.Fatal(err)
    }
    defer app.Cleanup() // REQUIRED - removes the temp copy

    // Register the hook under test against this isolated app
    hooks.RegisterPostHooks(app)

    scenario := tests.ApiScenario{
        Name:   "POST /api/collections/posts/records as verified user",
        Method: http.MethodPost,
        URL:    "/api/collections/posts/records",
        Body:   strings.NewReader(`{"title":"hello","slug":"hello"}`),
        Headers: map[string]string{
            "Authorization": testAuthHeader(app, "users", "alice@example.com"),
            "Content-Type":  "application/json",
        },
        ExpectedStatus: 200,
        ExpectedContent: []string{
            `"title":"hello"`,
            `"slug":"hello"`,
        },
        NotExpectedContent: []string{
            `"internalNotes"`, // the enrich hook should hide this
        },
        ExpectedEvents: map[string]int{
            "OnRecordCreateRequest":       1,
            "OnRecordAfterCreateSuccess":  1,
            "OnRecordEnrich":              1,
        },
        AfterTestFunc: func(t testing.TB, app *tests.TestApp, res *http.Response) {
            // Assert side-effects in the DB using the SAME app instance
            audits, err := app.FindRecordsByFilter(
                "audit",
                "action = 'post.create'",
                "-created", 10, 0,
            )
            if err != nil {
                t.Fatal(err)
            }
            if len(audits) != 1 {
                t.Fatalf("expected 1 audit record, got %d", len(audits))
            }
        },
        TestAppFactory: func(t testing.TB) *tests.TestApp { return app },
    }

    scenario.Test(t)
}
```

**Table-driven variant (authz matrix):**

```go
func TestPostsListAuthz(t *testing.T) {
    for _, tc := range []struct {
        name   string
        auth   string  // "", "users:alice", "users:bob", "_superusers:root"
        expect int
    }{
        {"guest gets public posts",       "",                200},
        {"authed gets own + public",      "users:alice",     200},
        {"superuser sees everything",     "_superusers:root",200},
    } {
        t.Run(tc.name, func(t *testing.T) {
            app, _ := tests.NewTestApp(testDataDir)
            defer app.Cleanup()
            hooks.RegisterPostHooks(app)

            tests.ApiScenario{
                Method:         http.MethodGet,
                URL:            "/api/collections/posts/records",
                Headers:        authHeaderFor(app, tc.auth),
                ExpectedStatus: tc.expect,
                TestAppFactory: func(t testing.TB) *tests.TestApp { return app },
            }.Test(t)
        })
    }
}
```

**Unit-testing a hook in isolation (no HTTP layer):**

```go
func TestAuditHookRollsBackOnAuditFailure(t *testing.T) {
    app, _ := tests.NewTestApp(testDataDir)
    defer app.Cleanup()
    hooks.RegisterPostHooks(app)

    // Delete the audit collection so the hook's Save fails
    audit, _ := app.FindCollectionByNameOrId("audit")
    _ = app.Delete(audit)

    col, _ := app.FindCollectionByNameOrId("posts")
    post := core.NewRecord(col)
    post.Set("title", "should rollback")
    post.Set("slug", "rollback")

    if err := app.Save(post); err == nil {
        t.Fatal("expected Save to fail because audit hook errored")
    }

    // Assert the post was NOT persisted (tx rolled back)
    _, err := app.FindFirstRecordByFilter("posts", "slug = 'rollback'", nil)
    if err == nil {
        t.Fatal("post should not exist after rollback")
    }
}
```

**Rules:**
- **Always `defer app.Cleanup()`** - otherwise temp directories leak under `/tmp`.
- **Use a checked-in `test_pb_data/` fixture** with the collections you need. Do not depend on the dev `pb_data/` - tests must be hermetic.
- **Register hooks against the test app**, not against a package-level `app` singleton. The test app is a fresh instance each time.
- **`ExpectedEvents`** asserts that specific hooks fired the expected number of times - use it to catch "hook silently skipped because someone forgot `e.Next()`" regressions.
- **`AfterTestFunc`** runs with the same app instance the scenario used, so you can query the DB to verify side-effects.
- **Parallelize with `t.Parallel()`** - `NewTestApp` gives each goroutine its own copy, so there's no shared state.
- **Tests run pure-Go SQLite** (`modernc.org/sqlite`) - no CGO, no extra setup, works on `go test ./...` out of the box.
- **For JSVM**, there is no equivalent test harness yet - test pb_hooks by booting `tests.NewTestApp` with the `pb_hooks/` directory populated and exercising the router from Go. Pure-JS unit testing of hook bodies requires extracting the logic into a `require()`able module.

Reference: [Testing](https://pocketbase.io/docs/go-testing/) · [tests package GoDoc](https://pkg.go.dev/github.com/pocketbase/pocketbase/tests)
