package cmd

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"google.golang.org/api/cloudidentity/v1"
	"google.golang.org/api/option"
)

func TestCollectGroupMemberEmails_RecursiveAndPaging(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch {
		case strings.Contains(r.URL.Path, "groups:lookup"):
			id := r.URL.Query().Get("groupKey.id")
			switch id {
			case "group-a@example.com":
				w.Header().Set("Content-Type", "application/json")
				_ = json.NewEncoder(w).Encode(map[string]any{"name": "groups/ga"})
				return
			case "group-b@example.com":
				w.Header().Set("Content-Type", "application/json")
				_ = json.NewEncoder(w).Encode(map[string]any{"name": "groups/gb"})
				return
			default:
				http.NotFound(w, r)
				return
			}
		case strings.Contains(r.URL.Path, "groups/ga/memberships"):
			w.Header().Set("Content-Type", "application/json")
			switch r.URL.Query().Get("pageToken") {
			case "":
				_ = json.NewEncoder(w).Encode(map[string]any{
					"memberships": []any{
						nil,
						map[string]any{"preferredMemberKey": map[string]any{"id": "group-b@example.com"}, "type": "GROUP"},
						map[string]any{"preferredMemberKey": map[string]any{"id": "user1@example.com"}, "type": "USER"},
						map[string]any{"preferredMemberKey": map[string]any{"id": "notanemail"}, "type": "USER"},
						map[string]any{"preferredMemberKey": map[string]any{"id": ""}, "type": "USER"},
					},
					"nextPageToken": "next",
				})
				return
			case "next":
				_ = json.NewEncoder(w).Encode(map[string]any{
					"memberships": []any{
						map[string]any{"preferredMemberKey": map[string]any{"id": "user2@example.com"}, "type": ""},
					},
				})
				return
			default:
				http.NotFound(w, r)
				return
			}
		case strings.Contains(r.URL.Path, "groups/gb/memberships"):
			w.Header().Set("Content-Type", "application/json")
			_ = json.NewEncoder(w).Encode(map[string]any{
				"memberships": []any{
					map[string]any{"preferredMemberKey": map[string]any{"id": "group-a@example.com"}, "type": "GROUP"},
					map[string]any{"preferredMemberKey": map[string]any{"id": "user3@example.com"}, "type": "USER"},
				},
			})
			return
		}
		http.NotFound(w, r)
	}))
	defer srv.Close()

	svc, err := cloudidentity.NewService(context.Background(),
		option.WithoutAuthentication(),
		option.WithHTTPClient(srv.Client()),
		option.WithEndpoint(srv.URL+"/"),
	)
	if err != nil {
		t.Fatalf("NewService: %v", err)
	}

	emails, err := collectGroupMemberEmails(context.Background(), svc, "group-a@example.com")
	if err != nil {
		t.Fatalf("collectGroupMemberEmails: %v", err)
	}
	want := []string{"user1@example.com", "user2@example.com", "user3@example.com"}
	if strings.Join(emails, ",") != strings.Join(want, ",") {
		t.Fatalf("emails=%v want %v", emails, want)
	}
}

func TestCollectGroupMemberEmails_LookupError(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.NotFound(w, r)
	}))
	defer srv.Close()

	svc, err := cloudidentity.NewService(context.Background(),
		option.WithoutAuthentication(),
		option.WithHTTPClient(srv.Client()),
		option.WithEndpoint(srv.URL+"/"),
	)
	if err != nil {
		t.Fatalf("NewService: %v", err)
	}

	if _, err := collectGroupMemberEmails(context.Background(), svc, "missing@example.com"); err == nil {
		t.Fatalf("expected error")
	}
}
