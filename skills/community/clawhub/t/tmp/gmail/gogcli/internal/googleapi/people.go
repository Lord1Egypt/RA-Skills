package googleapi

import (
	"context"
	"fmt"

	"google.golang.org/api/people/v1"
)

const (
	scopeContactsWrite   = "https://www.googleapis.com/auth/contacts"
	scopeContactsOtherRO = "https://www.googleapis.com/auth/contacts.other.readonly"
	scopeDirectoryRO     = "https://www.googleapis.com/auth/directory.readonly"
)

func NewPeopleContacts(ctx context.Context, email string) (*people.Service, error) {
	if opts, err := optionsForAccountScopes(ctx, "contacts", email, []string{scopeContactsWrite}); err != nil {
		return nil, fmt.Errorf("contacts options: %w", err)
	} else if svc, err := people.NewService(ctx, opts...); err != nil {
		return nil, fmt.Errorf("create contacts service: %w", err)
	} else {
		return svc, nil
	}
}

func NewPeopleOtherContacts(ctx context.Context, email string) (*people.Service, error) {
	if opts, err := optionsForAccountScopes(ctx, "contacts", email, []string{scopeContactsOtherRO}); err != nil {
		return nil, fmt.Errorf("contacts options: %w", err)
	} else if svc, err := people.NewService(ctx, opts...); err != nil {
		return nil, fmt.Errorf("create contacts service: %w", err)
	} else {
		return svc, nil
	}
}

func NewPeopleDirectory(ctx context.Context, email string) (*people.Service, error) {
	if opts, err := optionsForAccountScopes(ctx, "contacts", email, []string{scopeDirectoryRO}); err != nil {
		return nil, fmt.Errorf("contacts options: %w", err)
	} else if svc, err := people.NewService(ctx, opts...); err != nil {
		return nil, fmt.Errorf("create contacts service: %w", err)
	} else {
		return svc, nil
	}
}
