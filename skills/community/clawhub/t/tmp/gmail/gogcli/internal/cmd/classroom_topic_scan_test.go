package cmd

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"google.golang.org/api/classroom/v1"
	"google.golang.org/api/option"
)

func withClassroomTestService(t *testing.T, handler http.HandlerFunc, fn func()) {
	t.Helper()

	origNew := newClassroomService
	t.Cleanup(func() { newClassroomService = origNew })

	srv := httptest.NewServer(http.HandlerFunc(handler))
	t.Cleanup(srv.Close)

	svc, err := classroom.NewService(context.Background(),
		option.WithoutAuthentication(),
		option.WithHTTPClient(srv.Client()),
		option.WithEndpoint(srv.URL+"/"),
	)
	if err != nil {
		t.Fatalf("NewService: %v", err)
	}

	newClassroomService = func(context.Context, string) (*classroom.Service, error) { return svc, nil }
	fn()
}

func TestClassroomCourseworkList_TopicScanPages(t *testing.T) {
	var calls int
	withClassroomTestService(t, func(w http.ResponseWriter, r *http.Request) {
		if !strings.Contains(r.URL.Path, "/courseWork") {
			http.NotFound(w, r)
			return
		}
		calls++
		w.Header().Set("Content-Type", "application/json")
		switch calls {
		case 1:
			_ = json.NewEncoder(w).Encode(map[string]any{
				"courseWork":    []map[string]any{{"id": "w1", "topicId": "other"}},
				"nextPageToken": "p2",
			})
		case 2:
			_ = json.NewEncoder(w).Encode(map[string]any{
				"courseWork":    []map[string]any{{"id": "w2", "topicId": "target"}},
				"nextPageToken": "",
			})
		default:
			t.Fatalf("unexpected coursework calls: %d", calls)
		}
	}, func() {
		var payload struct {
			Coursework []struct {
				ID string `json:"id"`
			} `json:"coursework"`
			NextPageToken string `json:"nextPageToken"`
		}

		out := captureStdout(t, func() {
			_ = captureStderr(t, func() {
				if err := Execute([]string{"--json", "--account", "a@b.com", "classroom", "coursework", "c1", "--topic", "target", "--scan-pages", "2"}); err != nil {
					t.Fatalf("execute: %v", err)
				}
			})
		})

		if err := json.Unmarshal([]byte(out), &payload); err != nil {
			t.Fatalf("unmarshal: %v", err)
		}
		if len(payload.Coursework) != 1 || payload.Coursework[0].ID != "w2" {
			t.Fatalf("expected coursework w2, got %#v", payload.Coursework)
		}
		if calls != 2 {
			t.Fatalf("expected 2 calls, got %d", calls)
		}
	})
}

func TestClassroomMaterialsList_TopicScanPages(t *testing.T) {
	var calls int
	withClassroomTestService(t, func(w http.ResponseWriter, r *http.Request) {
		if !strings.Contains(r.URL.Path, "/courseWorkMaterials") {
			http.NotFound(w, r)
			return
		}
		calls++
		w.Header().Set("Content-Type", "application/json")
		switch calls {
		case 1:
			_ = json.NewEncoder(w).Encode(map[string]any{
				"courseWorkMaterial": []map[string]any{{"id": "m1", "topicId": "other"}},
				"nextPageToken":      "p2",
			})
		case 2:
			_ = json.NewEncoder(w).Encode(map[string]any{
				"courseWorkMaterial": []map[string]any{{"id": "m2", "topicId": "target"}},
				"nextPageToken":      "",
			})
		default:
			t.Fatalf("unexpected materials calls: %d", calls)
		}
	}, func() {
		var payload struct {
			Materials []struct {
				ID string `json:"id"`
			} `json:"materials"`
			NextPageToken string `json:"nextPageToken"`
		}

		out := captureStdout(t, func() {
			_ = captureStderr(t, func() {
				if err := Execute([]string{"--json", "--account", "a@b.com", "classroom", "materials", "c1", "--topic", "target", "--scan-pages", "2"}); err != nil {
					t.Fatalf("execute: %v", err)
				}
			})
		})

		if err := json.Unmarshal([]byte(out), &payload); err != nil {
			t.Fatalf("unmarshal: %v", err)
		}
		if len(payload.Materials) != 1 || payload.Materials[0].ID != "m2" {
			t.Fatalf("expected material m2, got %#v", payload.Materials)
		}
		if calls != 2 {
			t.Fatalf("expected 2 calls, got %d", calls)
		}
	})
}
