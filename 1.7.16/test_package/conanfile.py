import os

from conans import ConanFile, CMake, tools


class AlembicTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package"
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self):
            bin_path = os.path.join("bin", "example")
            abcfile = os.path.join(self.source_folder, "example.abc")
            self.run("{} {}".format(bin_path, abcfile), run_environment=True)
