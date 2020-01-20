import os
import sys
import pytest



try:
    sys.path.append(os.environ["LOCAL_PYTHONPATH"])
    print(os.environ["LOCAL_PYTHONPATH"])
    print(sys.path)
    from addon_helper import zip_addon, change_addon_dir, cleanup
except Exception as e:
    print(e)
    sys.exit(1)


class SetupPlugin(object):
    def __init__(self, addon):
        self.addon = addon
        self.addon_dir = "local_addon"

    def pytest_configure(self, config):
        (self.bpy_module, self.zfile) = zip_addon(self.addon, self.addon_dir)
        change_addon_dir(self.bpy_module, self.zfile, self.addon_dir)
        config.cache.set("bpy_module", self.bpy_module)

    def pytest_unconfigure(self):
        cleanup(self.addon, self.bpy_module, self.addon_dir)
        print("*** test run reporting finished")


addon = "fake_addon"
try:
    exit_val = pytest.main(["tests"], plugins=[SetupPlugin(addon)])
except Exception as e:
    print(e)
    exit_val = 1
sys.exit(exit_val)
