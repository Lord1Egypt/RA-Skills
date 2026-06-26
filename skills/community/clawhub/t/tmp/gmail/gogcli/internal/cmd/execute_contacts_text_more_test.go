package cmd

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"google.golang.org/api/option"
	"google.golang.org/api/people/v1"
)

func TestExecute_ContactsMoreCommands_Text(t *testing.T) {
	origContacts := newPeopleContactsService
	origOther := newPeopleOtherContactsService
	origDir := newPeopleDirectoryService
	t.Cleanup(func() {
		newPeopleContactsService = origContacts
		newPeopleOtherContactsService = origOther
		newPeopleDirectoryService = origDir
	})

	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		path := r.URL.Path
		switch {
		case strings.Contains(path, "people/c1") && r.Method == http.MethodGet && !strings.Contains(path, ":"):
			w.Header().Set("Content-Type", "application/json")
			_ = json.NewEncoder(w).Encode(map[string]any{
				"resourceName": "people/c1",
				"names":        []map[string]any{{"displayName": "Ada Lovelace"}},
				"emailAddresses": []map[string]any{
					{"value": "ada@example.com"},
				},
				"phoneNumbers": []map[string]any{{"value": "+1"}},
			})
			return
		case strings.Contains(path, "people:searchContacts") && r.Method == http.MethodGet:
			w.Header().Set("Content-Type", "application/json")
			_ = json.NewEncoder(w).Encode(map[string]any{
				"results": []map[string]any{
					{
						"person": map[string]any{
							"resourceName": "people/c1",
							"names":        []map[string]any{{"displayName": "Ada"}},
							"emailAddresses": []map[string]any{
								{"value": "ada@example.com"},
							},
							"phoneNumbers": []map[string]any{{"value": "+1"}},
						},
					},
				},
			})
			return
		case strings.Contains(path, "people/me/connections") && r.Method == http.MethodGet:
			w.Header().Set("Content-Type", "application/json")
			_ = json.NewEncoder(w).Encode(map[string]any{
				"connections": []map[string]any{
					{
						"resourceName": "people/c1",
						"names":        []map[string]any{{"displayName": "Ada"}},
						"emailAddresses": []map[string]any{
							{"value": "ada@example.com"},
						},
					},
				},
			})
			return
		case strings.Contains(path, "people:createContact") && r.Method == http.MethodPost:
			w.Header().Set("Content-Type", "application/json")
			_ = json.NewEncoder(w).Encode(map[string]any{
				"resourceName": "people/c2",
				"names":        []map[string]any{{"displayName": "Grace"}},
			})
			return
		case strings.Contains(path, "people/c1") && strings.Contains(path, ":updateContact") && (r.Method == http.MethodPatch || r.Method == http.MethodPost):
			w.Header().Set("Content-Type", "application/json")
			_ = json.NewEncoder(w).Encode(map[string]any{
				"resourceName": "people/c1",
				"names":        []map[string]any{{"displayName": "Ada Updated"}},
			})
			return
		case strings.Contains(path, "people/c1:deleteContact") && r.Method == http.MethodDelete:
			w.WriteHeader(http.StatusNoContent)
			return
		case strings.Contains(path, "people:searchDirectoryPeople") && r.Method == http.MethodGet:
			w.Header().Set("Content-Type", "application/json")
			_ = json.NewEncoder(w).Encode(map[string]any{
				"people": []map[string]any{{
					"resourceName": "people/d1",
					"names":        []map[string]any{{"displayName": "Dir"}},
					"emailAddresses": []map[string]any{
						{"value": "dir@example.com"},
					},
				}},
			})
			return
		case strings.Contains(path, "otherContacts:search") && r.Method == http.MethodGet:
			w.Header().Set("Content-Type", "application/json")
			_ = json.NewEncoder(w).Encode(map[string]any{
				"results": []map[string]any{
					{
						"person": map[string]any{
							"resourceName": "people/o1",
							"names":        []map[string]any{{"displayName": "Other"}},
							"emailAddresses": []map[string]any{
								{"value": "other@example.com"},
							},
						},
					},
				},
			})
			return
		case strings.Contains(path, "/otherContacts") && r.Method == http.MethodGet:
			w.Header().Set("Content-Type", "application/json")
			_ = json.NewEncoder(w).Encode(map[string]any{
				"otherContacts": []map[string]any{{
					"resourceName": "people/o1",
					"names":        []map[string]any{{"displayName": "Other"}},
					"emailAddresses": []map[string]any{
						{"value": "other@example.com"},
					},
				}},
			})
			return
		default:
			http.NotFound(w, r)
			return
		}
	}))
	defer srv.Close()

	svc, err := people.NewService(context.Background(),
		option.WithoutAuthentication(),
		option.WithHTTPClient(srv.Client()),
		option.WithEndpoint(srv.URL+"/"),
	)
	if err != nil {
		t.Fatalf("NewService: %v", err)
	}
	newPeopleContactsService = func(context.Context, string) (*people.Service, error) { return svc, nil }
	newPeopleOtherContactsService = func(context.Context, string) (*people.Service, error) { return svc, nil }
	newPeopleDirectoryService = func(context.Context, string) (*people.Service, error) { return svc, nil }

	out := captureStdout(t, func() {
		_ = captureStderr(t, func() {
			if err := Execute([]string{"--account", "a@b.com", "contacts", "search", "Ada"}); err != nil {
				t.Fatalf("search: %v", err)
			}
			if err := Execute([]string{"--account", "a@b.com", "contacts", "list", "--max", "1"}); err != nil {
				t.Fatalf("list: %v", err)
			}
			if err := Execute([]string{"--account", "a@b.com", "contacts", "get", "people/c1"}); err != nil {
				t.Fatalf("get: %v", err)
			}
			if err := Execute([]string{"--account", "a@b.com", "contacts", "create", "--given", "Grace"}); err != nil {
				t.Fatalf("create: %v", err)
			}
			if err := Execute([]string{"--account", "a@b.com", "contacts", "update", "people/c1", "--given", "Ada"}); err != nil {
				t.Fatalf("update: %v", err)
			}
			if err := Execute([]string{"--force", "--account", "a@b.com", "contacts", "delete", "people/c1"}); err != nil {
				t.Fatalf("delete: %v", err)
			}
			if err := Execute([]string{"--account", "a@b.com", "contacts", "directory", "search", "Dir"}); err != nil {
				t.Fatalf("dir search: %v", err)
			}
			if err := Execute([]string{"--account", "a@b.com", "contacts", "other", "list"}); err != nil {
				t.Fatalf("other list: %v", err)
			}
			if err := Execute([]string{"--account", "a@b.com", "contacts", "other", "search", "Other"}); err != nil {
				t.Fatalf("other search: %v", err)
			}
		})
	})
	if !strings.Contains(out, "RESOURCE") || !strings.Contains(out, "people/c1") || !strings.Contains(out, "people/d1") {
		t.Fatalf("unexpected output: %q", out)
	}
}
