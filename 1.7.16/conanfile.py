from conans import ConanFile, CMake, tools
import os

class AlembicConan(ConanFile):
    name = "alembic"
    version = "1.7.16"
    license = "BSD-3-Clause"
    author = "Christopher Horvath blackencino@gmail.com"
    homepage = "http://www.alembic.io/"
    url = "https://github.com/blackencino/conan-alembic.git"
    description = "Alembic is an open computer graphics interchange framework. "\
        "Alembic distills complex, animated scenes into a non-procedural, "\
        "application-independent set of baked geometric results."\
        "Alembic was developed by Industrial Light & Magic and Sony Pictures Imagworks"
    topics = ("conan", "alembic", "geometry", "pointcloud", "mesh", "vfx")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False]
        }
    default_options = {
        "shared": False
        }
    generators = "cmake", "cmake_find_package"
    exports_sources = ["CMakeLists.txt", "patches/*"]

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        pass

    def configure(self):
        pass

    def requirements(self):
        self.requires("hdf5/[>=1.12.0]")
        self.requires("openexr/[>=2.5.3 <3]")
        self.requires("zlib/[>=1.2.11]")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        tools.patch(patch_file="patches/alembic-1.7.16.patch",
                    base_path="alembic-{}".format(self.version))
        os.rename("alembic-{}".format(self.version), self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["USE_ARNOLD"] = False
        self._cmake.definitions["USE_BINARIES"] = False
        self._cmake.definitions["USE_EXAMPLES"] = False
        self._cmake.definitions["USE_HDF5"] = True
        self._cmake.definitions["USE_MAYA"] = False
        self._cmake.definitions["USE_PRMAN"] = False
        self._cmake.definitions["USE_PYALEMBIC"] = False
        self._cmake.definitions["USE_STATIC_BOOST"] = False
        self._cmake.definitions["USE_STATIC_HDF5"] = True
        self._cmake.definitions["USE_TESTS"] = False
        self._cmake.definitions["ALEMBIC_BUILD_LIBS"] = True
        self._cmake.definitions["ALEMBIC_ILMBASE_LINK_STATIC"] = True
        self._cmake.definitions["ALEMBIC_SHARED_LIBS"] = self.options.shared
        self._cmake.definitions["ALEMBIC_LIB_USES_BOOST"] = False
        self._cmake.definitions["ALEMBIC_LIB_USES_TR1"] = False
        self._cmake.definitions["DOCS_PATH"] = False
        #self._cmake.definitions["CONAN_CXX_FLAGS"] = "-Wno-deprecated-copy"
        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE.txt", src=self._source_subfolder, dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "share"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "Alembic"
        self.cpp_info.names["cmake_find_package_multi"] = "Alembic"
        self.cpp_info.names["pkg_config"] = "Alembic"

        compiler = self.settings.compiler
        if str(compiler) in ("gcc", "clang", "apple-clang"):
            self.cpp_info.cxxflags.append("-Wno-error-deprecated-copy")

        self.cpp_info.libs = tools.collect_libs(self)
        #self.cpp_info.includedirs = ["lib"]
        if self.options.shared:
            self.cpp_info.defines.append("ALEMBIC_DLL")




