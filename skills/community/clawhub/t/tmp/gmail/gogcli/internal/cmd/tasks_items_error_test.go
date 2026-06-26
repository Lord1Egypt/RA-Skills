package cmd

import (
	"context"
	"strings"
	"testing"
)

func TestTasksUpdate_ValidationErrors(t *testing.T) {
	flags := &RootFlags{Account: "a@b.com"}

	if err := runKong(t, &TasksUpdateCmd{}, []string{"l1", "t1"}, context.Background(), flags); err == nil || !strings.Contains(err.Error(), "no fields to update") {
		t.Fatalf("expected no fields error, got %v", err)
	}

	if err := runKong(t, &TasksUpdateCmd{}, []string{"l1", "t1", "--status", "nope"}, context.Background(), flags); err == nil || !strings.Contains(err.Error(), "invalid --status") {
		t.Fatalf("expected status error, got %v", err)
	}
}
