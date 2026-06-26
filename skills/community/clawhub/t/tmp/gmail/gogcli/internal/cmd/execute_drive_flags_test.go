package cmd

import "testing"

func TestExecute_DriveLs_PositionalFolderRejected(t *testing.T) {
	_ = captureStderr(t, func() {
		err := Execute([]string{"--account", "a@b.com", "drive", "ls", "root"})
		if err == nil {
			t.Fatalf("expected error")
		}
		if ExitCode(err) != 2 {
			t.Fatalf("expected exit code 2, got %d (err=%v)", ExitCode(err), err)
		}
	})
}

func TestExecute_DriveMove_MissingParentFlag(t *testing.T) {
	_ = captureStderr(t, func() {
		err := Execute([]string{"--account", "a@b.com", "drive", "move", "id1"})
		if err == nil {
			t.Fatalf("expected error")
		}
		if ExitCode(err) != 2 {
			t.Fatalf("expected exit code 2, got %d (err=%v)", ExitCode(err), err)
		}
	})
}

func TestExecute_DriveMove_PositionalParentRejected(t *testing.T) {
	_ = captureStderr(t, func() {
		err := Execute([]string{"--account", "a@b.com", "drive", "move", "id1", "np"})
		if err == nil {
			t.Fatalf("expected error")
		}
		if ExitCode(err) != 2 {
			t.Fatalf("expected exit code 2, got %d (err=%v)", ExitCode(err), err)
		}
	})
}
