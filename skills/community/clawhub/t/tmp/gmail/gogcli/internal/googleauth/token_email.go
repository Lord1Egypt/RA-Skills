package googleauth

import (
	"context"
	"fmt"
	"net/http"
	"strings"
	"time"

	"golang.org/x/oauth2"
)

// EmailForRefreshToken exchanges a refresh token and returns the authorized email address.
func EmailForRefreshToken(ctx context.Context, client string, refreshToken string, scopes []string, timeout time.Duration) (string, error) {
	if strings.TrimSpace(refreshToken) == "" {
		return "", errMissingToken
	}

	if timeout <= 0 {
		timeout = 15 * time.Second
	}

	creds, err := readClientCredentials(client)
	if err != nil {
		return "", fmt.Errorf("read credentials: %w", err)
	}

	cfg := oauth2.Config{
		ClientID:     creds.ClientID,
		ClientSecret: creds.ClientSecret,
		Endpoint:     oauthEndpoint,
		Scopes:       scopes,
	}

	ctx, cancel := context.WithTimeout(ctx, timeout)
	defer cancel()

	ctx = context.WithValue(ctx, oauth2.HTTPClient, &http.Client{Timeout: timeout})

	ts := cfg.TokenSource(ctx, &oauth2.Token{RefreshToken: refreshToken})

	tok, err := ts.Token()
	if err != nil {
		return "", fmt.Errorf("refresh access token: %w", err)
	}

	if raw, ok := tok.Extra("id_token").(string); ok {
		if email, err := emailFromIDToken(raw); err == nil {
			return email, nil
		}
	}

	if strings.TrimSpace(tok.AccessToken) == "" {
		return "", errMissingAccessToken
	}

	return fetchUserEmailWithURL(ctx, tok.AccessToken, userinfoURL)
}
