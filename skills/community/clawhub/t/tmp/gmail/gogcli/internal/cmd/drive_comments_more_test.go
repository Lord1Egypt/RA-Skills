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

func TestDriveCommentsGetUpdateDeleteReply(t *testing.T) {
	origNew := newDriveService
	t.Cleanup(func() { newDriveService = origNew })

	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		path := strings.TrimPrefix(r.URL.Path, "/drive/v3")
		switch {
		case r.Method == http.MethodGet && path == "/files/file1/comments":
			w.Header().Set("Content-Type", "application/json")
			_ = json.NewEncoder(w).Encode(map[string]any{
				"comments": []map[string]any{
					{
						"id":          "c-list",
						"content":     "list",
						"createdTime": "2025-01-01T00:00:00Z",
						"resolved":    false,
						"quotedFileContent": map[string]any{
							"value": "quoted",
						},
					},
				},
			})
			return
		case r.Method == http.MethodGet && path == "/files/file1/comments/c1":
			w.Header().Set("Content-Type", "application/json")
			_ = json.NewEncoder(w).Encode(map[string]any{
				"id":          "c1",
				"content":     "hello",
				"createdTime": "2025-01-01T00:00:00Z",
			})
			return
		case r.Method == http.MethodPatch && path == "/files/file1/comments/c1":
			w.Header().Set("Content-Type", "application/json")
			_ = json.NewEncoder(w).Encode(map[string]any{
				"id":           "c1",
				"content":      "updated",
				"modifiedTime": "2025-01-01T01:00:00Z",
			})
			return
		case r.Method == http.MethodPost && path == "/files/file1/comments":
			var body struct {
				Content           string `json:"content"`
				QuotedFileContent struct {
					Value string `json:"value"`
				} `json:"quotedFileContent"`
			}
			_ = json.NewDecoder(r.Body).Decode(&body)
			if body.Content == "" {
				http.Error(w, "missing content", http.StatusBadRequest)
				return
			}
			w.Header().Set("Content-Type", "application/json")
			_ = json.NewEncoder(w).Encode(map[string]any{
				"id":          "c2",
				"content":     body.Content,
				"createdTime": "2025-01-01T03:00:00Z",
				"quotedFileContent": map[string]any{
					"value": body.QuotedFileContent.Value,
				},
			})
			return
		case r.Method == http.MethodDelete && path == "/files/file1/comments/c1":
			w.WriteHeader(http.StatusNoContent)
			return
		case r.Method == http.MethodPost && path == "/files/file1/comments/c1/replies":
			w.Header().Set("Content-Type", "application/json")
			_ = json.NewEncoder(w).Encode(map[string]any{
				"id":          "r1",
				"content":     "reply",
				"createdTime": "2025-01-01T02:00:00Z",
			})
			return
		default:
			http.NotFound(w, r)
			return
		}
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

	getOut := captureStdout(t, func() {
		_ = captureStderr(t, func() {
			if err := Execute([]string{"--json", "--account", "a@b.com", "drive", "comments", "get", "file1", "c1"}); err != nil {
				t.Fatalf("Execute get: %v", err)
			}
		})
	})
	if !strings.Contains(getOut, "\"content\":") {
		t.Fatalf("unexpected get output: %q", getOut)
	}

	plainGetOut := captureStdout(t, func() {
		_ = captureStderr(t, func() {
			if err := Execute([]string{"--account", "a@b.com", "drive", "comments", "get", "file1", "c1"}); err != nil {
				t.Fatalf("Execute get plain: %v", err)
			}
		})
	})
	if !strings.Contains(plainGetOut, "content") {
		t.Fatalf("unexpected get plain output: %q", plainGetOut)
	}

	listOut := captureStdout(t, func() {
		_ = captureStderr(t, func() {
			if err := Execute([]string{"--json", "--account", "a@b.com", "drive", "comments", "list", "file1"}); err != nil {
				t.Fatalf("Execute list: %v", err)
			}
		})
	})
	if !strings.Contains(listOut, "\"comments\"") {
		t.Fatalf("unexpected list output: %q", listOut)
	}

	plainListOut := captureStdout(t, func() {
		_ = captureStderr(t, func() {
			if err := Execute([]string{"--account", "a@b.com", "drive", "comments", "list", "file1", "--include-quoted"}); err != nil {
				t.Fatalf("Execute list plain: %v", err)
			}
		})
	})
	if !strings.Contains(plainListOut, "quoted") {
		t.Fatalf("unexpected plain list output: %q", plainListOut)
	}

	createOut := captureStdout(t, func() {
		_ = captureStderr(t, func() {
			if err := Execute([]string{"--json", "--account", "a@b.com", "drive", "comments", "create", "file1", "new comment", "--quoted", "quote"}); err != nil {
				t.Fatalf("Execute create: %v", err)
			}
		})
	})
	if !strings.Contains(createOut, "new comment") {
		t.Fatalf("unexpected create output: %q", createOut)
	}

	plainCreateOut := captureStdout(t, func() {
		_ = captureStderr(t, func() {
			if err := Execute([]string{"--account", "a@b.com", "drive", "comments", "create", "file1", "plain comment"}); err != nil {
				t.Fatalf("Execute create plain: %v", err)
			}
		})
	})
	if !strings.Contains(plainCreateOut, "content") {
		t.Fatalf("unexpected create plain output: %q", plainCreateOut)
	}

	updateOut := captureStdout(t, func() {
		_ = captureStderr(t, func() {
			if err := Execute([]string{"--json", "--account", "a@b.com", "drive", "comments", "update", "file1", "c1", "updated"}); err != nil {
				t.Fatalf("Execute update: %v", err)
			}
		})
	})
	if !strings.Contains(updateOut, "updated") {
		t.Fatalf("unexpected update output: %q", updateOut)
	}

	plainUpdateOut := captureStdout(t, func() {
		_ = captureStderr(t, func() {
			if err := Execute([]string{"--account", "a@b.com", "drive", "comments", "update", "file1", "c1", "updated"}); err != nil {
				t.Fatalf("Execute update plain: %v", err)
			}
		})
	})
	if !strings.Contains(plainUpdateOut, "updated") {
		t.Fatalf("unexpected update plain output: %q", plainUpdateOut)
	}

	deleteOut := captureStdout(t, func() {
		_ = captureStderr(t, func() {
			if err := Execute([]string{"--json", "--force", "--account", "a@b.com", "drive", "comments", "delete", "file1", "c1"}); err != nil {
				t.Fatalf("Execute delete: %v", err)
			}
		})
	})
	var deleted struct {
		Deleted   bool   `json:"deleted"`
		FileID    string `json:"fileId"`
		CommentID string `json:"commentId"`
	}
	if err := json.Unmarshal([]byte(deleteOut), &deleted); err != nil {
		t.Fatalf("delete json parse: %v", err)
	}
	if !deleted.Deleted || deleted.FileID != "file1" || deleted.CommentID != "c1" {
		t.Fatalf("unexpected delete output: %#v", deleted)
	}

	plainDeleteOut := captureStdout(t, func() {
		_ = captureStderr(t, func() {
			if err := Execute([]string{"--force", "--account", "a@b.com", "drive", "comments", "delete", "file1", "c1"}); err != nil {
				t.Fatalf("Execute delete plain: %v", err)
			}
		})
	})
	if !strings.Contains(plainDeleteOut, "deleted") {
		t.Fatalf("unexpected delete plain output: %q", plainDeleteOut)
	}

	replyOut := captureStdout(t, func() {
		_ = captureStderr(t, func() {
			if err := Execute([]string{"--json", "--account", "a@b.com", "drive", "comments", "reply", "file1", "c1", "reply"}); err != nil {
				t.Fatalf("Execute reply: %v", err)
			}
		})
	})
	if !strings.Contains(replyOut, "reply") {
		t.Fatalf("unexpected reply output: %q", replyOut)
	}

	plainReplyOut := captureStdout(t, func() {
		_ = captureStderr(t, func() {
			if err := Execute([]string{"--account", "a@b.com", "drive", "comments", "reply", "file1", "c1", "reply"}); err != nil {
				t.Fatalf("Execute reply plain: %v", err)
			}
		})
	})
	if !strings.Contains(plainReplyOut, "reply") {
		t.Fatalf("unexpected reply plain output: %q", plainReplyOut)
	}
}
