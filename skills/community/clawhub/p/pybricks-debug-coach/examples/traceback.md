# Traceback

## Input

The hub reports `OSError: [Errno 19] ENODEV` at `main.py` line 12 when constructing a motor on Port.C. The robot reference says the attachment motor is on Port.D.

## Expected coaching behavior

- Cite the exception line and port mismatch.
- Identify the port mapping as the likely cause.
- Change only Port.C to Port.D.
- Rerun the same minimal program.
- Pass means the program starts without the same traceback.
- Fail means the same exception remains.
