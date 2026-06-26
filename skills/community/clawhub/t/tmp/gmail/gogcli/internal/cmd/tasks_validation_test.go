package cmd

import (
	"context"
	"errors"
	"strings"
	"testing"

	"google.golang.org/api/tasks/v1"
)

func TestExecute_TasksAdd_RequiresTitle(t *testing.T) {
	origNew := newTasksService
	t.Cleanup(func() { newTasksService = origNew })
	newTasksService = func(context.Context, string) (*tasks.Service, error) {
		t.Fatalf("expected validation to fail before creating service")
		return nil, errors.New("unexpected tasks service call")
	}

	_ = captureStderr(t, func() {
		err := Execute([]string{"--account", "a@b.com", "tasks", "add", "l1"})
		if err == nil || !strings.Contains(err.Error(), "required: --title") {
			t.Fatalf("unexpected err: %v", err)
		}
	})
}

func TestExecute_TasksUpdate_RequiresFields(t *testing.T) {
	origNew := newTasksService
	t.Cleanup(func() { newTasksService = origNew })
	newTasksService = func(context.Context, string) (*tasks.Service, error) {
		t.Fatalf("expected validation to fail before creating service")
		return nil, errors.New("unexpected tasks service call")
	}

	_ = captureStderr(t, func() {
		err := Execute([]string{"--account", "a@b.com", "tasks", "update", "l1", "t1"})
		if err == nil || !strings.Contains(err.Error(), "no fields to update") {
			t.Fatalf("unexpected err: %v", err)
		}
	})
}

func TestExecute_TasksUpdate_RejectsInvalidStatus(t *testing.T) {
	origNew := newTasksService
	t.Cleanup(func() { newTasksService = origNew })
	newTasksService = func(context.Context, string) (*tasks.Service, error) {
		t.Fatalf("expected validation to fail before creating service")
		return nil, errors.New("unexpected tasks service call")
	}

	_ = captureStderr(t, func() {
		err := Execute([]string{"--account", "a@b.com", "tasks", "update", "l1", "t1", "--status", "nope"})
		if err == nil || !strings.Contains(err.Error(), "invalid --status") {
			t.Fatalf("unexpected err: %v", err)
		}
	})
}
