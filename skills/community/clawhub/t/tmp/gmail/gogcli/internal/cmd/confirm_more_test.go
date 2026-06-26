package cmd

import (
	"context"
	"strings"
	"testing"
)

func TestConfirmDestructive_Force(t *testing.T) {
	if err := confirmDestructive(context.Background(), &RootFlags{Force: true}, "do thing"); err != nil {
		t.Fatalf("expected nil, got %v", err)
	}
}

func TestConfirmDestructive_NoInput(t *testing.T) {
	err := confirmDestructive(context.Background(), &RootFlags{NoInput: true}, "nuke things")
	if err == nil {
		t.Fatalf("expected error")
	}
	if !strings.Contains(err.Error(), "refusing to nuke things") {
		t.Fatalf("unexpected error: %v", err)
	}
}
