package config

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestConfigExists(t *testing.T) {
	home := t.TempDir()
	t.Setenv("HOME", home)
	t.Setenv("XDG_CONFIG_HOME", filepath.Join(home, "xdg"))

	exists, err := ConfigExists()
	if err != nil {
		t.Fatalf("ConfigExists: %v", err)
	}

	if exists {
		t.Fatalf("expected config to be missing")
	}

	path, err := ConfigPath()
	if err != nil {
		t.Fatalf("ConfigPath: %v", err)
	}

	err = os.MkdirAll(filepath.Dir(path), 0o700)
	if err != nil {
		t.Fatalf("mkdir: %v", err)
	}

	err = os.WriteFile(path, []byte(`{}`), 0o600)
	if err != nil {
		t.Fatalf("write config: %v", err)
	}

	exists, err = ConfigExists()
	if err != nil {
		t.Fatalf("ConfigExists (after write): %v", err)
	}

	if !exists {
		t.Fatalf("expected config to exist")
	}
}

func TestKeepServiceAccountLegacyPath(t *testing.T) {
	home := t.TempDir()
	t.Setenv("HOME", home)
	t.Setenv("XDG_CONFIG_HOME", filepath.Join(home, "xdg"))

	path, err := KeepServiceAccountLegacyPath("User@Example.com")
	if err != nil {
		t.Fatalf("KeepServiceAccountLegacyPath: %v", err)
	}

	if !strings.Contains(path, "keep-sa-User@Example.com.json") {
		t.Fatalf("unexpected path: %q", path)
	}
}
