"""Verification-only: espeak_Initialize with a data path longer than the stock N_PATH_HOME.

usage: python ci_path_test.py LIB LENGTH
Copies the espeak-ng-data of the installed espeakng-loader wheel to a path of exactly LENGTH
chars, then initializes LIB from it. espeak-ng calls exit(1) when it cannot load its data.
"""

import ctypes
import os
import shutil
import sys
import tempfile

import espeakng_loader

lib_path, n = sys.argv[1], int(sys.argv[2])
base = tempfile.mkdtemp(prefix="esd")
target = base
while len(target) < n:  # components of <= 100 chars stay under NAME_MAX
    target = os.path.join(target, "x" * min(100, n - len(target) - 1))
assert len(target) == n, len(target)
shutil.copytree(espeakng_loader.get_data_path(), target)
lib = ctypes.cdll.LoadLibrary(lib_path)
rate = lib.espeak_Initialize(0x02, 0, target.encode(), 0)
print(f"lib={lib_path} len={n}: espeak_Initialize ok, sample rate {rate}", flush=True)
