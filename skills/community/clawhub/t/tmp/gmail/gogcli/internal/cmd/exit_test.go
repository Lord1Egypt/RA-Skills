package cmd

import (
	"errors"
	"testing"
)

func TestExitError(t *testing.T) {
	err := &ExitError{Code: 2, Err: errors.New("boom")}
	if err.Error() != "boom" {
		t.Fatalf("unexpected error: %q", err.Error())
	}
	if !errors.Is(err, err.Err) {
		t.Fatalf("expected unwrap")
	}
}

func TestExitCode(t *testing.T) {
	if ExitCode(nil) != 0 {
		t.Fatalf("expected 0")
	}
	if ExitCode(errors.New("x")) != 1 {
		t.Fatalf("expected 1")
	}
	if ExitCode(&ExitError{Code: -1, Err: errors.New("x")}) != 1 {
		t.Fatalf("expected 1 for negative code")
	}
	if ExitCode(&ExitError{Code: 5, Err: errors.New("x")}) != 5 {
		t.Fatalf("expected 5")
	}
}
