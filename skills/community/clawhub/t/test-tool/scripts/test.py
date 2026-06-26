#!/usr/bin/env python3
import os, sys
if len(sys.argv)<2: sys.exit(1)
tests={'-e':os.path.exists,'-f':os.path.isfile,'-d':os.path.isdir}
op=sys.argv[1]; path=sys.argv[2] if len(sys.argv)>2 else ''
sys.exit(0 if tests.get(op,lambda x:False)(path) else 1)
