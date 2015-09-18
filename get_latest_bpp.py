"""
Script to clone and install latest bpp version.
Originally by Jesse Bloom, slight modifications by Erick Matsen.

http://biopp.univ-montp2.fr/wiki/index.php/Installation#Development_version
"""

from collections import OrderedDict
import os
import subprocess


def main():
    """Main body of script."""

    # parameters describing what to download and where to put it
    branches = OrderedDict([
            ('bpp-core','master'),
            ('bpp-seq','master'),
            ('bpp-popgen','master'),
            ('bpp-phyl','newlik'),
            ('bppsuite','newlik')])
    rundoxygen = {
            'bpp-core':True,
            'bpp-seq':True,
            'bpp-popgen':True,
            'bpp-phyl':True,
            'bppsuite':False}
    giturl = 'http://biopp.univ-montp2.fr/git'
    doxygenfile = 'Doxyfile'
    installdir = '/usr/local/'
    basedir = os.getcwd()

    # clone or pull library
    for lib in branches.keys():
        if os.path.isdir(lib):
            os.chdir(lib)
            returncode = subprocess.call(['git', 'pull'])
            assert not returncode, "nonzero return code when pulling %s" % lib
            os.chdir(basedir)
        else:
            returncode = subprocess.call(['git', 'clone', '-b', branches[lib], '%s/%s.git' % (giturl, lib)])
            assert not returncode, "nonzero return code when cloning %s" % lib
            assert os.path.isdir(lib), "Failed to clone %s" % lib

    # build library
    for lib in branches.keys():
        os.chdir(lib)
        returncode = subprocess.call(['cmake', '-DCMAKE_INSTALL_PREFIX=%s' % installdir, '-DBUILD_TESTING=OFF'])
        assert not returncode, "nonzero return code when running cmake on %s" % lib
        returncode = subprocess.call(['make', '-j4', 'install'])
        assert not returncode, "nonzero return code when running make install on %s" % lib
        os.chdir(basedir)

    # run doxygen
    for lib in branches.keys():
        if rundoxygen[lib]:
            os.chdir(lib)
            assert os.path.isfile(doxygenfile), "Failed to find %s for %s" % (doxygenfile, lib)
            returncode = subprocess.call(['doxygen', doxygenfile])
            assert not returncode, "nonzero return code when running doxygen on %s" % lib
            os.chdir(basedir)



if __name__ == '__main__':
    main() # run the program
