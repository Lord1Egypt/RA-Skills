package config

import (
	"errors"
	"testing"
)

var errNope = errors.New("nope")

func TestCredentialsMissingError(t *testing.T) {
	cause := errNope
	err := &CredentialsMissingError{Path: "/tmp/credentials.json", Cause: cause}

	if err.Error() == "" {
		t.Fatalf("expected message")
	}

	if !errors.Is(err, cause) {
		t.Fatalf("expected unwrap")
	}
}
