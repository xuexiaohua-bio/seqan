#!/usr/bin/env python
"""Execute the tests for splazers.

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

    print 'Executing test for splazers'
    print '========================='
    print

    ph = app_tests.TestPathHelper(
        source_base, binary_base,
        'apps/splazers/tests')  # tests dir

    # ============================================================
    # Auto-detect the binary path.
    # ============================================================

    path_to_program = app_tests.autolocateBinary(
      binary_base, 'apps/splazers', 'splazers')

    # ============================================================
    # Built TestConf list.
    # ============================================================

    # Build list with TestConf objects, analoguely to how the output
    # was generated in generate_outputs.sh.
    conf_list = []

    # ============================================================
    # First Section.
    # ============================================================


    # We run the following for all read lengths we have reads for.
    for rl in [100]:
        # Run with default options.
        conf = app_tests.TestConf(
            program=path_to_program,
            redir_stdout=ph.outFile('se-adeno-reads%d_1_default.stdout' % rl),
            args=[ph.inFile('adeno-genome.fa'),
                  ph.inFile('adeno-reads%d_1.fa' % rl),
                  '-o', ph.outFile('se-adeno-reads%d_1_default.out' % rl)],
            to_diff=[(ph.inFile('se-adeno-reads%d_1_default.out' % rl),
                      ph.outFile('se-adeno-reads%d_1_default.out' % rl)),
                     (ph.inFile('se-adeno-reads%d_1_default.stdout' % rl),
                      ph.outFile('se-adeno-reads%d_1_default.stdout' % rl))])
        conf_list.append(conf)

        # test different min. match lengths
        for mml in range(16,26):
            # test different numbers of prefix errors
            for ep in range(0,2):
                # test different numbers of suffix errors
                for es in range(0,3):

                    conf = app_tests.TestConf(
                        program=path_to_program,
                        redir_stdout=ph.outFile('se-adeno-reads%d_1_mml%d_ep%d_es%d.stdout' % (rl, mml, ep, es)),
                        args=['-sm', str(mml), '-ep', str(ep), '-es', str(es),
                              ph.inFile('adeno-genome.fa'),
                              ph.inFile('adeno-reads%d_1.fa' % rl),
                              '-o', ph.outFile('se-adeno-reads%d_1_mml%d_ep%d_es%d.out' % (rl, mml, ep, es))],
                        to_diff=[(ph.inFile('se-adeno-reads%d_1_mml%d_ep%d_es%d.out' % (rl, mml, ep, es)),
                                  ph.outFile('se-adeno-reads%d_1_mml%d_ep%d_es%d.out' % (rl, mml, ep, es))),
                                 (ph.inFile('se-adeno-reads%d_1_mml%d_ep%d_es%d.stdout' % (rl, mml, ep, es)),
                                  ph.outFile('se-adeno-reads%d_1_mml%d_ep%d_es%d.stdout' % (rl, mml, ep, es)))])
                    conf_list.append(conf)

#                    # Allow indels.
#                    conf = app_tests.TestConf(
#                        program=path_to_program,
#                        redir_stdout=ph.outFile('se-adeno-reads%d_1_mml%d-id_ep%d_es%d.stdout' % (rl, mml, ep, es)),
#                        args=['-id', '-sm', str(mml), '-ep', str(ep), '-es', str(es),
#                              ph.inFile('adeno-genome.fa'),
#                              ph.inFile('adeno-reads%d_1.fa' % rl),
#                              '-o', ph.outFile('se-adeno-reads%d_1_mml%d-id_ep%d_es%d.out' % (rl, mml, ep, es))],
#                        to_diff=[(ph.inFile('se-adeno-reads%d_1_mml%d-id_ep%d_es%d.out' % (rl, mml, ep, es)),
#                                  ph.outFile('se-adeno-reads%d_1_mml%d-id_ep%d_es%d.out' % (rl, mml, ep, es))),
#                                 (ph.inFile('se-adeno-reads%d_1_mml%d-id_ep%d_es%d.stdout' % (rl, mml, ep, es)),
#                                  ph.outFile('se-adeno-reads%d_1_mml%d-id_ep%d_es%d.stdout' % (rl, mml, ep, es)))])
#                    conf_list.append(conf)

        # Compute forward/reverse matches only.
        for o in ['-r', '-f']:
            conf = app_tests.TestConf(
                program=path_to_program,
                redir_stdout=ph.outFile('se-adeno-reads%d_1_mml20%s_ep1_es1.stdout' % (rl, o)),
                args=[ o, '-id', '-sm', str(20), '-ep', str(1), '-es', str(1),
                      ph.inFile('adeno-genome.fa'),
                      ph.inFile('adeno-reads%d_1.fa' % rl),
                      '-o', ph.outFile('se-adeno-reads%d_1_mml20%s_ep1_es1.out' % (rl, o))],
                to_diff=[(ph.inFile('se-adeno-reads%d_1_mml20%s_ep1_es1.out' % (rl, o)),
                          ph.outFile('se-adeno-reads%d_1_mml20%s_ep1_es1.out' % (rl, o))),
                         (ph.inFile('se-adeno-reads%d_1_mml20%s_ep1_es1.stdout' % (rl, o)),
                          ph.outFile('se-adeno-reads%d_1_mml20%s_ep1_es1.stdout' % (rl, o)))])
            conf_list.append(conf)


        # Compute with different identity rates.
        for i in range(90, 100):
            conf = app_tests.TestConf(
                program=path_to_program,
                redir_stdout=ph.outFile('se-adeno-reads%d_1_mml20-i%d_ep1_es1.stdout' % (rl, i)),
                args=['-i', str(i), '-sm', str(20), '-ep', str(1), '-es', str(1),
                      ph.inFile('adeno-genome.fa'),
                      ph.inFile('adeno-reads%d_1.fa' % rl),
                      '-o', ph.outFile('se-adeno-reads%d_1_mml20-i%d_ep1_es1.out' % (rl, i))],
                to_diff=[(ph.inFile('se-adeno-reads%d_1_mml20-i%d_ep1_es1.out' % (rl, i)),
                          ph.outFile('se-adeno-reads%d_1_mml20-i%d_ep1_es1.out' % (rl, i))),
                         (ph.inFile('se-adeno-reads%d_1_mml20-i%d_ep1_es1.stdout' % (rl, i)),
                          ph.outFile('se-adeno-reads%d_1_mml20-i%d_ep1_es1.stdout' % (rl, i)))])
            conf_list.append(conf)

        # Compute with different output formats.
        for of in [3, 4]:
            conf = app_tests.TestConf(
                program=path_to_program,
                redir_stdout=ph.outFile('se-adeno-reads%d_1_mml20-of%d_ep1_es1.stdout' % (rl, of)),
                args=['-of', str(of),  '-sm', str(20), '-ep', str(1), '-es', str(1),
                      ph.inFile('adeno-genome.fa'),
                      ph.inFile('adeno-reads%d_1.fa' % rl),
                      '-o', ph.outFile('se-adeno-reads%d_1_mml20-of%d_ep1_es1.out' % (rl, of))],
                to_diff=[(ph.inFile('se-adeno-reads%d_1_mml20-of%d_ep1_es1.out' % (rl, of)),
                          ph.outFile('se-adeno-reads%d_1_mml20-of%d_ep1_es1.out' % (rl, of))),
                         (ph.inFile('se-adeno-reads%d_1_mml20-of%d_ep1_es1.stdout' % (rl, of)),
                          ph.outFile('se-adeno-reads%d_1_mml20-of%d_ep1_es1.stdout' % (rl, of)))])
            conf_list.append(conf)

        # Compute with different sort orders.
        for so in [0, 1]:
            conf = app_tests.TestConf(
                program=path_to_program,
                redir_stdout=ph.outFile('se-adeno-reads%d_1_mml20-so%d_ep1_es1.stdout' % (rl, so)),
                args=[ '-so', str(so),  '-sm', str(20), '-ep', str(1), '-es', str(1),
                      ph.inFile('adeno-genome.fa'),
                      ph.inFile('adeno-reads%d_1.fa' % rl),
                      '-o', ph.outFile('se-adeno-reads%d_1_mml20-so%d_ep1_es1.out' % (rl, so))],
                to_diff=[(ph.inFile('se-adeno-reads%d_1_mml20-so%d_ep1_es1.out' % (rl, so)),
                          ph.outFile('se-adeno-reads%d_1_mml20-so%d_ep1_es1.out' % (rl, so))),
                         (ph.inFile('se-adeno-reads%d_1_mml20-so%d_ep1_es1.stdout' % (rl, so)),
                          ph.outFile('se-adeno-reads%d_1_mml20-so%d_ep1_es1.stdout' % (rl, so)))])
            conf_list.append(conf)

        # Run in default anchored mode
        conf = app_tests.TestConf(
            program=path_to_program,
            redir_stdout=ph.outFile('anchored_adeno_example%d.stdout' % rl),
            args=['-an',
                  ph.inFile('adeno-genome.fa'),
                  ph.inFile('adeno-reads-pe.sam'), # % rl),
                  '-o', ph.outFile('anchored_adeno_example%d.out' % rl),
                  '-ll', '300', '-le', '90'],
            to_diff=[(ph.inFile('anchored_adeno_example%d.out' % rl),
                      ph.outFile('anchored_adeno_example%d.out' % rl)),
                     (ph.inFile('anchored_adeno_example%d.stdout' % rl),
                      ph.outFile('anchored_adeno_example%d.stdout' % rl))])
        conf_list.append(conf)

    # ============================================================
    # Execute the tests.
    # ============================================================
    failures = 0
    for conf in conf_list:
        res = app_tests.runTest(conf)
        # Output to the user.
        print ' '.join(['splazers'] + conf.args),
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
