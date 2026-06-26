package cmd

import (
	"errors"
	"testing"
)

func TestExitErrorErrorAndUnwrap(t *testing.T) {
	var nilErr *ExitError
	if got := nilErr.Error(); got != "" {
		t.Fatalf("expected empty error for nil receiver, got %q", got)
	}

	if got := nilErr.Unwrap(); got != nil {
		t.Fatalf("expected nil unwrap for nil receiver, got %v", got)
	}

	err := &ExitError{}
	if got := err.Error(); got != "" {
		t.Fatalf("expected empty error for nil Err, got %q", got)
	}

	baseErr := errors.New("boom")
	err.Err = baseErr
	if got := err.Error(); got != "boom" {
		t.Fatalf("expected boom, got %q", got)
	}

	if got := err.Unwrap(); !errors.Is(got, baseErr) {
		t.Fatalf("expected base err, got %v", got)
	}
}

func TestExitCodeMore(t *testing.T) {
	if got := ExitCode(nil); got != 0 {
		t.Fatalf("expected 0, got %d", got)
	}

	if got := ExitCode(errors.New("nope")); got != 1 {
		t.Fatalf("expected 1, got %d", got)
	}

	if got := ExitCode(&ExitError{Code: -1, Err: errors.New("nope")}); got != 1 {
		t.Fatalf("expected 1 for negative code, got %d", got)
	}

	if got := ExitCode(&ExitError{Code: 3, Err: errors.New("nope")}); got != 3 {
		t.Fatalf("expected 3, got %d", got)
	}
}
