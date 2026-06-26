#!/usr/bin/env python3
import os, sys
print(os.path.realpath(sys.argv[1] if sys.argv[1:] else '.'))
