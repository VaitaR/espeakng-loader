"""Verification-only (Windows): does the UCRT narrow stat() espeak-ng uses accept a path of N chars?"""

import ctypes
import os
import sys
import tempfile

ucrt = ctypes.CDLL("ucrtbase")
ucrt._errno.restype = ctypes.POINTER(ctypes.c_int)
for n in map(int, sys.argv[1:]):
    base = tempfile.mkdtemp(prefix="esd")
    target = os.path.join(base, "x" * (n - len(base) - 1))
    os.makedirs(target)
    buf = ctypes.create_string_buffer(256)
    rc = ucrt._stat64(target.encode(), buf)
    print(f"stat len={n} rc={rc} errno={ucrt._errno().contents.value if rc else 0} base={base}")
