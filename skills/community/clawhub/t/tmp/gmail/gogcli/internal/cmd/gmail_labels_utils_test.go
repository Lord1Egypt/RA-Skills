package cmd

import (
	"errors"
	"net/http"
	"testing"

	"google.golang.org/api/googleapi"
)

func TestMapLabelCreateError(t *testing.T) {
	if err := mapLabelCreateError(nil, "foo"); err != nil {
		t.Fatalf("expected nil error")
	}

	dup := &googleapi.Error{
		Code:    http.StatusConflict,
		Message: "Label name exists",
	}
	if err := mapLabelCreateError(dup, "foo"); err == nil {
		t.Fatalf("expected mapped error")
	}

	other := errors.New("nope")
	if err := mapLabelCreateError(other, "foo"); !errors.Is(err, other) {
		t.Fatalf("expected original error")
	}
}

func TestIsDuplicateLabelError(t *testing.T) {
	err := &googleapi.Error{
		Code:    http.StatusConflict,
		Message: "label already exists",
		Errors: []googleapi.ErrorItem{
			{Reason: "duplicate"},
		},
	}
	if !isDuplicateLabelError(err) {
		t.Fatalf("expected duplicate label error")
	}

	err = &googleapi.Error{
		Code:   http.StatusBadRequest,
		Errors: []googleapi.ErrorItem{{Message: "label name exists"}},
	}
	if !isDuplicateLabelError(err) {
		t.Fatalf("expected message-based duplicate")
	}

	err = &googleapi.Error{
		Code:    http.StatusConflict,
		Message: "conflict",
		Errors:  []googleapi.ErrorItem{{Reason: "duplicate"}},
	}
	if !isDuplicateLabelError(err) {
		t.Fatalf("expected reason-based duplicate")
	}

	if !labelDuplicateReason(" alreadyExists ") {
		t.Fatalf("expected duplicate reason match")
	}

	if !isDuplicateLabelError(errors.New("label name exists")) {
		t.Fatalf("expected string duplicate")
	}

	if isDuplicateLabelError(errors.New("nope")) {
		t.Fatalf("expected non-duplicate")
	}
}
