package cmd

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"google.golang.org/api/drive/v3"
	"google.golang.org/api/option"
)

func TestDriveCommentsList_Empty(t *testing.T) {
	origNew := newDriveService
	t.Cleanup(func() { newDriveService = origNew })

	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		path := strings.TrimPrefix(r.URL.Path, "/drive/v3")
		if r.Method == http.MethodGet && path == "/files/empty/comments" {
			w.Header().Set("Content-Type", "application/json")
			_ = json.NewEncoder(w).Encode(map[string]any{
				"comments": []any{},
			})
			return
		}
		http.NotFound(w, r)
	}))
	defer srv.Close()

	svc, err := drive.NewService(context.Background(),
		option.WithoutAuthentication(),
		option.WithHTTPClient(srv.Client()),
		option.WithEndpoint(srv.URL+"/"),
	)
	if err != nil {
		t.Fatalf("NewService: %v", err)
	}
	newDriveService = func(context.Context, string) (*drive.Service, error) { return svc, nil }

	errOut := captureStderr(t, func() {
		if err := Execute([]string{"--account", "a@b.com", "drive", "comments", "list", "empty"}); err != nil {
			t.Fatalf("Execute: %v", err)
		}
	})
	if !strings.Contains(errOut, "No comments") {
		t.Fatalf("unexpected stderr: %q", errOut)
	}
}
