package input

import (
	"bufio"
	"errors"
	"fmt"
	"io"
	"strings"
)

// ReadLine reads a single line from r.
//
// It supports Unix (\n) and Windows (\r\n) line endings, and treats a bare \r as
// end-of-line as well.
//
// If the input ends with EOF before a newline and there is buffered content, the
// accumulated content is returned with a nil error.
//
// If EOF is encountered without any buffered content, ReadLine returns io.EOF.
func ReadLine(r io.Reader) (string, error) {
	br := bufio.NewReader(r)

	var sb strings.Builder

	for {
		b, err := br.ReadByte()
		if err != nil {
			if errors.Is(err, io.EOF) {
				if sb.Len() > 0 {
					return sb.String(), nil
				}

				return "", io.EOF
			}

			return "", fmt.Errorf("read line: %w", err)
		}

		if b == '\n' || b == '\r' {
			if b == '\r' {
				if next, _ := br.Peek(1); len(next) == 1 && next[0] == '\n' {
					_, _ = br.ReadByte()
				}
			}

			return sb.String(), nil
		}

		sb.WriteByte(b)
	}
}
