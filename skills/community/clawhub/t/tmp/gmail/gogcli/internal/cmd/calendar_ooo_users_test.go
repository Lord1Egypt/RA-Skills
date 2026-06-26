package cmd

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"google.golang.org/api/calendar/v3"
	"google.golang.org/api/option"
	"google.golang.org/api/people/v1"
)

func TestCalendarOOOCmd_JSON(t *testing.T) {
	origCal := newCalendarService
	t.Cleanup(func() { newCalendarService = origCal })

	srv := httptest.NewServer(withPrimaryCalendar(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodPost && strings.Contains(r.URL.Path, "/events") {
			var body map[string]any
			_ = json.NewDecoder(r.Body).Decode(&body)
			if body["eventType"] != "outOfOffice" {
				t.Fatalf("expected outOfOffice eventType, got %#v", body["eventType"])
			}
			w.Header().Set("Content-Type", "application/json")
			_ = json.NewEncoder(w).Encode(map[string]any{
				"id":      "evt1",
				"summary": "Out of office",
			})
			return
		}
		http.NotFound(w, r)
	})))
	defer srv.Close()

	svc, err := calendar.NewService(context.Background(),
		option.WithoutAuthentication(),
		option.WithHTTPClient(srv.Client()),
		option.WithEndpoint(srv.URL+"/"),
	)
	if err != nil {
		t.Fatalf("NewService: %v", err)
	}
	newCalendarService = func(context.Context, string) (*calendar.Service, error) { return svc, nil }

	out := captureStdout(t, func() {
		_ = captureStderr(t, func() {
			if err := Execute([]string{"--json", "--account", "a@b.com", "calendar", "ooo", "--from", "2025-01-01", "--to", "2025-01-02"}); err != nil {
				t.Fatalf("Execute: %v", err)
			}
		})
	})
	if !strings.Contains(out, "event") {
		t.Fatalf("unexpected output: %q", out)
	}
}

func TestCalendarUsersCmd_TextAndJSON(t *testing.T) {
	origPeople := newPeopleDirectoryService
	t.Cleanup(func() { newPeopleDirectoryService = origPeople })

	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if !strings.Contains(r.URL.Path, "people:listDirectoryPeople") {
			http.NotFound(w, r)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(map[string]any{
			"people": []map[string]any{
				{
					"names":          []map[string]any{{"displayName": "User One"}},
					"emailAddresses": []map[string]any{{"value": "user@example.com"}},
				},
			},
			"nextPageToken": "npt",
		})
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
	newPeopleDirectoryService = func(context.Context, string) (*people.Service, error) { return svc, nil }

	textOut := captureStdout(t, func() {
		errOut := captureStderr(t, func() {
			if err := Execute([]string{"--account", "a@b.com", "calendar", "users", "--max", "1"}); err != nil {
				t.Fatalf("Execute: %v", err)
			}
		})
		if !strings.Contains(errOut, "Tip: Use any email") {
			t.Fatalf("unexpected stderr: %q", errOut)
		}
	})
	if !strings.Contains(textOut, "user@example.com") {
		t.Fatalf("unexpected text output: %q", textOut)
	}

	jsonOut := captureStdout(t, func() {
		_ = captureStderr(t, func() {
			if err := Execute([]string{"--json", "--account", "a@b.com", "calendar", "users", "--max", "1"}); err != nil {
				t.Fatalf("Execute: %v", err)
			}
		})
	})
	if !strings.Contains(jsonOut, "users") {
		t.Fatalf("unexpected json output: %q", jsonOut)
	}
}
