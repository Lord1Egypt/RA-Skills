package googleapi

import (
	"context"
	"fmt"

	"google.golang.org/api/cloudidentity/v1"
)

const (
	scopeCloudIdentityGroupsRO = "https://www.googleapis.com/auth/cloud-identity.groups.readonly"
)

// NewCloudIdentityGroups creates a Cloud Identity service for reading groups.
// This API allows non-admin users to list groups they belong to and view group members.
func NewCloudIdentityGroups(ctx context.Context, email string) (*cloudidentity.Service, error) {
	if opts, err := optionsForAccountScopes(ctx, "cloudidentity", email, []string{scopeCloudIdentityGroupsRO}); err != nil {
		return nil, fmt.Errorf("cloudidentity options: %w", err)
	} else if svc, err := cloudidentity.NewService(ctx, opts...); err != nil {
		return nil, fmt.Errorf("create cloudidentity service: %w", err)
	} else {
		return svc, nil
	}
}
