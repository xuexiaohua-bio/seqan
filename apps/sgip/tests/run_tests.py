#!/usr/bin/env python
"""Execute the tests for sgip.

The golden test outputs are generated by the script generate_outputs.sh.

You have to give the root paths to the source and the binaries as arguments to
the program.  These are the paths to the directory that contains the 'projects'
directory.

Usage:  run_tests.py SOURCE_ROOT_PATH BINARY_ROOT_PATH
"""
import logging
import os.path
import sys

# Automagically add util/py_lib to PYTHONPATH environment variable.
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                    '..', '..', 'util', 'py_lib'))
sys.path.insert(0, path)

import seqan.app_tests as app_tests

def main(source_base, binary_base):
    """Main entry point of the script."""

    print 'Executing test for sgip'
    print '========================='
    print

    ph = app_tests.TestPathHelper(
        source_base, binary_base,
        'apps/sgip/tests')  # tests dir

    # ============================================================
    # Auto-detect the binary path.
    # ============================================================

    path_to_program = app_tests.autolocateBinary(
      binary_base, 'apps/sgip', 'sgip')

    # ============================================================
    # Built TestConf list.
    # ============================================================

    # Build list with TestConf objects, analoguely to how the output
    # was generated in generate_outputs.sh.
    conf_list = []

    # ============================================================
    # First Section.
    # ============================================================

    # App TestConf objects to conf_list, just like this for each
    # test you want to run.

    # Example 1
    conf = app_tests.TestConf(
        program=path_to_program,
        redir_stdout=ph.outFile('iso_r01_m200.A00_B00.stdout'),
        args=['-o', ph.inFile('../example/r01/iso_r01_m200.A00'), '-c',
              ph.inFile('../example/r01/iso_r01_m200.B00'), '-v', '2', '-i'],
        to_diff=[(ph.inFile('iso_r01_m200.A00_B00.stdout'),
                  ph.outFile('iso_r01_m200.A00_B00.stdout'))])
    conf_list.append(conf)

    # Example 2
    conf = app_tests.TestConf(
        program=path_to_program,
        redir_stdout=ph.outFile('iso_r01_m200.A01_B01.stdout'),
        args=['-o', ph.inFile('../example/r01/iso_r01_m200.A01'), '-c',
              ph.inFile('../example/r01/iso_r01_m200.B01'), '-v', '2', '-i'],
        to_diff=[(ph.inFile('iso_r01_m200.A01_B01.stdout'),
                  ph.outFile('iso_r01_m200.A01_B01.stdout'))])
    conf_list.append(conf)
    # Example 3
    conf = app_tests.TestConf(
        program=path_to_program,
        redir_stdout=ph.outFile('iso_r01_m200.A00_B01.stdout'),
        args=['-o', ph.inFile('../example/r01/iso_r01_m200.A00'), '-c',
              ph.inFile('../example/r01/iso_r01_m200.B01'), '-v', '2','-i'],
        to_diff=[(ph.inFile('iso_r01_m200.A00_B01.stdout'),
                  ph.outFile('iso_r01_m200.A00_B01.stdout'))])
    conf_list.append(conf)
	# Example 4
    conf = app_tests.TestConf(
        program=path_to_program,
        redir_stdout=ph.outFile('iso_r01_m200.A00.stdout'),
        args=['-o', ph.inFile('../example/r01/iso_r01_m200.A00'), '-v', '2'],
        to_diff=[(ph.inFile('iso_r01_m200.A00.stdout'),
                  ph.outFile('iso_r01_m200.A00.stdout'))])
    conf_list.append(conf)
	# Example 5

	#Example 6
    conf = app_tests.TestConf(
        program=path_to_program,
        redir_stdout=ph.outFile('srg_latin-4.stdout'),
        args=['-o', ph.inFile('../example/srg/latin-4'), '-v', '2'],
        to_diff=[(ph.inFile('srg_latin-4.stdout'),
                  ph.outFile('srg_latin-4.stdout'))])
    conf_list.append(conf)
    # Example 7
    conf = app_tests.TestConf(
        program=path_to_program,
        redir_stdout=ph.outFile('srg_lattice-4.stdout'),
        args=['-o', ph.inFile('../example/srg/lattice-4'), '-v', '2'],
        to_diff=[(ph.inFile('srg_lattice-4.stdout'),
                  ph.outFile('srg_lattice-4.stdout'))])
    conf_list.append(conf)
    # Example 8
    conf = app_tests.TestConf(
        program=path_to_program,
        redir_stdout=ph.outFile('srg_paley-5.stdout'),
        args=['-o', ph.inFile('../example/srg/paley-5'), '-v', '2'],
        to_diff=[(ph.inFile('srg_paley-5.stdout'),
                  ph.outFile('srg_paley-5.stdout'))])
    conf_list.append(conf)
    # Example 9
    conf = app_tests.TestConf(
        program=path_to_program,
        redir_stdout=ph.outFile('srg_sts7.stdout'),
        args=['-o', ph.inFile('../example/srg/sts-7'), '-v', '2'],
        to_diff=[(ph.inFile('srg_sts7.stdout'),
                  ph.outFile('srg_sts7.stdout'))])
    conf_list.append(conf)
    # Example 10
    conf = app_tests.TestConf(
        program=path_to_program,
        redir_stdout=ph.outFile('srg_triang-5.stdout'),
        args=['-o', ph.inFile('../example/srg/triang-5'), '-v', '2'],
        to_diff=[(ph.inFile('srg_triang-5.stdout'),
                  ph.outFile('srg_triang-5.stdout'))])
    conf_list.append(conf)

    # ============================================================
    # Execute the tests.
    # ============================================================
    failures = 0
    for conf in conf_list:
        res = app_tests.runTest(conf)
        # Output to the user.
        print ' '.join(['sgip'] + conf.args),
        if res:
             print 'OK'
        else:
            failures += 1
            print 'FAILED'

    # Cleanup.
    ph.deleteTempDir()

    print '=============================='
    print '     total tests: %d' % len(conf_list)
    print '    failed tests: %d' % failures
    print 'successful tests: %d' % (len(conf_list) - failures)
    print '=============================='
    # Compute and return return code.
    return failures != 0


if __name__ == '__main__':
    sys.exit(app_tests.main(main))
