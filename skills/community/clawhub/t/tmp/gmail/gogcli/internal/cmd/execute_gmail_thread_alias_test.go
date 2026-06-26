package cmd

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"google.golang.org/api/gmail/v1"
	"google.golang.org/api/option"
)

func TestExecute_GmailThreadAliases(t *testing.T) {
	origNew := newGmailService
	t.Cleanup(func() { newGmailService = origNew })

	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		path := strings.TrimPrefix(r.URL.Path, "/gmail/v1")
		switch {
		case r.Method == http.MethodGet && path == "/users/me/threads/t1":
			w.Header().Set("Content-Type", "application/json")
			_ = json.NewEncoder(w).Encode(map[string]any{
				"id": "t1",
				"messages": []map[string]any{
					{
						"id": "m1",
						"payload": map[string]any{
							"headers": []map[string]any{
								{"name": "From", "value": "me@example.com"},
								{"name": "To", "value": "you@example.com"},
								{"name": "Subject", "value": "Hello"},
								{"name": "Date", "value": "Wed, 21 Jan 2026 12:00:00 +0000"},
							},
						},
					},
				},
			})
			return
		default:
			http.NotFound(w, r)
			return
		}
	}))
	defer srv.Close()

	svc, err := gmail.NewService(context.Background(),
		option.WithoutAuthentication(),
		option.WithHTTPClient(srv.Client()),
		option.WithEndpoint(srv.URL+"/"),
	)
	if err != nil {
		t.Fatalf("NewService: %v", err)
	}
	newGmailService = func(context.Context, string) (*gmail.Service, error) { return svc, nil }

	cases := [][]string{
		{"--plain", "--account", "a@b.com", "gmail", "read", "t1"},
		{"--plain", "--account", "a@b.com", "gmail", "thread", "t1"},
	}
	for _, args := range cases {
		out := captureStdout(t, func() {
			_ = captureStderr(t, func() {
				if execErr := Execute(args); execErr != nil {
					t.Fatalf("Execute %v: %v", args, execErr)
				}
			})
		})
		if !strings.Contains(out, "Thread contains 1 message(s)") {
			t.Fatalf("unexpected output for %v: %q", args, out)
		}
	}
}
