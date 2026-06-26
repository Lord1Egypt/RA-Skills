package config

import (
	"encoding/base64"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestDerivedPaths(t *testing.T) {
	home := t.TempDir()
	t.Setenv("HOME", home)
	t.Setenv("XDG_CONFIG_HOME", filepath.Join(home, "xdg-config"))

	base, err := Dir()
	if err != nil {
		t.Fatalf("Dir: %v", err)
	}

	keyringDir, err := KeyringDir()
	if err != nil {
		t.Fatalf("KeyringDir: %v", err)
	}

	if !strings.HasPrefix(keyringDir, base) {
		t.Fatalf("expected keyring under %q, got %q", base, keyringDir)
	}

	watchDir, err := GmailWatchDir()
	if err != nil {
		t.Fatalf("GmailWatchDir: %v", err)
	}

	if !strings.HasPrefix(watchDir, base) {
		t.Fatalf("expected watch dir under %q, got %q", base, watchDir)
	}

	attachmentsDir, err := GmailAttachmentsDir()
	if err != nil {
		t.Fatalf("GmailAttachmentsDir: %v", err)
	}

	if !strings.HasPrefix(attachmentsDir, base) {
		t.Fatalf("expected attachments dir under %q, got %q", base, attachmentsDir)
	}

	downloadsDir, err := DriveDownloadsDir()
	if err != nil {
		t.Fatalf("DriveDownloadsDir: %v", err)
	}

	if !strings.HasPrefix(downloadsDir, base) {
		t.Fatalf("expected downloads dir under %q, got %q", base, downloadsDir)
	}
}

func TestKeepServiceAccountLegacyPathMore(t *testing.T) {
	home := t.TempDir()
	t.Setenv("HOME", home)
	t.Setenv("XDG_CONFIG_HOME", filepath.Join(home, "xdg-config"))

	path, err := KeepServiceAccountLegacyPath("A@B.com")
	if err != nil {
		t.Fatalf("KeepServiceAccountLegacyPath: %v", err)
	}

	if !strings.Contains(filepath.Base(path), "keep-sa-A@B.com") {
		t.Fatalf("unexpected legacy filename: %q", filepath.Base(path))
	}
}

func TestKeepServiceAccountPath(t *testing.T) {
	home := t.TempDir()
	t.Setenv("HOME", home)
	t.Setenv("XDG_CONFIG_HOME", filepath.Join(home, "xdg-config"))

	path, err := KeepServiceAccountPath("A@B.com")
	if err != nil {
		t.Fatalf("KeepServiceAccountPath: %v", err)
	}

	expected := base64.RawURLEncoding.EncodeToString([]byte("a@b.com"))
	if !strings.Contains(filepath.Base(path), "keep-sa-"+expected) {
		t.Fatalf("unexpected service account path: %q", filepath.Base(path))
	}
}

func TestServiceAccountPath(t *testing.T) {
	home := t.TempDir()
	t.Setenv("HOME", home)
	t.Setenv("XDG_CONFIG_HOME", filepath.Join(home, "xdg-config"))

	path, err := ServiceAccountPath("A@B.com")
	if err != nil {
		t.Fatalf("ServiceAccountPath: %v", err)
	}

	expected := base64.RawURLEncoding.EncodeToString([]byte("a@b.com"))
	if !strings.Contains(filepath.Base(path), "sa-"+expected) {
		t.Fatalf("unexpected service account path: %q", filepath.Base(path))
	}
}

func TestListServiceAccountEmails(t *testing.T) {
	home := t.TempDir()
	t.Setenv("HOME", home)
	t.Setenv("XDG_CONFIG_HOME", filepath.Join(home, "xdg-config"))

	dir, err := EnsureDir()
	if err != nil {
		t.Fatalf("EnsureDir: %v", err)
	}

	enc := base64.RawURLEncoding.EncodeToString([]byte("user@example.com"))
	if writeErr := os.WriteFile(filepath.Join(dir, "sa-"+enc+".json"), []byte(`{"type":"service_account"}`), 0o600); writeErr != nil {
		t.Fatalf("write sa file: %v", writeErr)
	}

	if writeErr := os.WriteFile(filepath.Join(dir, "keep-sa-"+enc+".json"), []byte(`{"type":"service_account"}`), 0o600); writeErr != nil {
		t.Fatalf("write keep-sa file: %v", writeErr)
	}

	if writeErr := os.WriteFile(filepath.Join(dir, "keep-sa-Other@Example.com.json"), []byte(`{"type":"service_account"}`), 0o600); writeErr != nil {
		t.Fatalf("write legacy keep-sa file: %v", writeErr)
	}

	emails, err := ListServiceAccountEmails()
	if err != nil {
		t.Fatalf("ListServiceAccountEmails: %v", err)
	}

	if !strings.Contains(strings.Join(emails, ","), "user@example.com") || !strings.Contains(strings.Join(emails, ","), "other@example.com") {
		t.Fatalf("unexpected emails: %#v", emails)
	}
}
