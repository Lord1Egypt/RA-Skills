#!/usr/bin/env python3
import os, sys
print(os.readlink(sys.argv[1] if sys.argv[1:] else '.'))
