#!/usr/bin/env python
"""Execute the tests for program gustaf.

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

    print 'Executing test for gustaf'
    print '==============================='
    print

    ph = app_tests.TestPathHelper(
         source_base, binary_base,
         'apps/gustaf/tests')  # tests dir

    # ============================================================
    # Auto-detect the binary path.
    # ============================================================

    path_to_program = app_tests.autolocateBinary(
      binary_base, 'bin', 'gustaf')

    path_to_snd_program = app_tests.autolocateBinary(
      binary_base, 'bin', 'gustaf_mate_joining')


    # ============================================================
    # Built TestConf list.
    # ============================================================

    # Build list with TestConf objects, analoguely to how the output
    # was generated in generate_outputs.sh.
    conf_list = []

    # We prepare a list of transforms to apply to the output files.  This is
    # used to strip the input/output paths from the programs' output to
    # make it more canonical and host independent.
    ph.outFile('-')  # To ensure that the out path is set.
    transforms = [
        app_tests.ReplaceTransform(
            os.path.join(ph.source_base_path,
                         'apps/gustaf/tests') + os.sep,
            '', right=True),
        app_tests.ReplaceTransform(ph.temp_dir + os.sep, '', right=True),
        app_tests.NormalizeScientificExponentsTransform(),
        ]

    # ============================================================
    # Gustaf_mate_joining Tests
    # ============================================================

    # ============================================================
    # Simple gustaf_mate_joining app test
    # ============================================================

    conf = app_tests.TestConf(
        program=path_to_snd_program,
        redir_stdout=ph.outFile('gustaf_mate_joining.stdout'),
        redir_stderr=ph.outFile('gustaf_mate_joining.stderr'),
        args=[ph.inFile('adeno_modified_reads_mates1.fa'),
              ph.inFile('adeno_modified_reads_mates2.fa'),
              '-o', ph.outFile('adeno_modified_reads_joinedMates.fa'),
              '-rc',
              ],
        to_diff=[#(ph.inFile('st2_l100.vcf'),
                  #ph.outFile('st2_l100.vcf'),
                  #transforms),
                 (ph.inFile('adeno_modified_reads_joinedMates.fa'),
                  ph.outFile('adeno_modified_reads_joinedMates.fa'))])
    conf_list.append(conf)

    # ${JOINMATES} adeno_modified_reads_mates1.fa adeno_modified_reads_mates2.fa \
    # -o adeno_modified_reads_joinedMates.fa -rc 1 \
    # > gustaf_mate_joining.stdout 2> gustaf_mate_joining.stderr


    # ============================================================
    # Read joining, reverse complement
    # ============================================================

    conf = app_tests.TestConf(
        program=path_to_snd_program,
        redir_stdout=ph.outFile('gustaf_mate_joining.stdout'),
        redir_stderr=ph.outFile('gustaf_mate_joining.stderr'),
        args=[ph.inFile('reads_simulated_mates1_gold.fa'),
              ph.inFile('reads_simulated_mates2_gold.fa'),
              '-o', ph.outFile('reads_simulated_joined_rc.fa'),
              '-rc',
              ],
        to_diff=[#(ph.inFile('st2_l100.vcf'),
                  #ph.outFile('st2_l100.vcf'),
                  #transforms),
                 (ph.inFile('reads_simulated_joined_rc.fa'),
                  ph.outFile('reads_simulated_joined_rc.fa'))])
    conf_list.append(conf)

    # ${JOINMATES} reads_simulated_mates1_gold.fa reads_simulated_mates2_gold.fa \
    # -o reads_simulated_joined_rc.fa -rc 1 \
    # > gustaf_mate_joining.stdout 2> gustaf_mate_joining.stderr

    # ============================================================
    # Read joining, no reverse complement
    # ============================================================

    conf = app_tests.TestConf(
        program=path_to_snd_program,
        redir_stdout=ph.outFile('gustaf_mate_joining.stdout'),
        redir_stderr=ph.outFile('gustaf_mate_joining.stderr'),
        args=[ph.inFile('reads_simulated_mates1_gold.fa'),
              ph.inFile('reads_simulated_mates2_gold.fa'),
              '-o', ph.outFile('reads_simulated_joined.fa'),
              ],
        to_diff=[#(ph.inFile('st2_l100.vcf'),
                  #ph.outFile('st2_l100.vcf'),
                  #transforms),
                 (ph.inFile('reads_simulated_joined.fa'),
                  ph.outFile('reads_simulated_joined.fa'))])
    conf_list.append(conf)

    # ${JOINMATES} reads_simulated_mates1_gold.fa reads_simulated_mates2_gold.fa \
    # -o reads_simulated_joined.fa \
    # > gustaf_mate_joining.stdout 2> gustaf_mate_joining.stderr

    # ============================================================
    # Read splitting, reverse complement
    # ============================================================

    conf = app_tests.TestConf(
        program=path_to_snd_program,
        redir_stdout=ph.outFile('gustaf_mate_joining.stdout'),
        redir_stderr=ph.outFile('gustaf_mate_joining.stderr'),
        args=[ph.inFile('reads_simulated_joined_gold.fa'),
              '-o', ph.outFile('reads_simulated_mates1_rc.fa'),
              '-o', ph.outFile('reads_simulated_mates2_rc.fa'),
              '-rc',
              ],
        to_diff=[(ph.inFile('reads_simulated_mates1_rc.fa'),
                  ph.outFile('reads_simulated_mates1_rc.fa'),
                  transforms),
                 (ph.inFile('reads_simulated_mates2_rc.fa'),
                  ph.outFile('reads_simulated_mates2_rc.fa'))])
    conf_list.append(conf)

    # ${JOINMATES} reads_simulated_joined_gold.fa \
    # -o reads_simulated_mates1_rc.fa -o reads_simulated_mates2_rc.fa -rc 1 \
    # > gustaf_mate_joining.stdout 2> gustaf_mate_joining.stderr

    # ============================================================
    # Read splitting, no reverse complement
    # ============================================================

    conf = app_tests.TestConf(
        program=path_to_snd_program,
        redir_stdout=ph.outFile('gustaf_mate_joining.stdout'),
        redir_stderr=ph.outFile('gustaf_mate_joining.stderr'),
        args=[ph.inFile('reads_simulated_joined_gold.fa'),
              '-o', ph.outFile('reads_simulated_mates1.fa'),
              '-o', ph.outFile('reads_simulated_mates2.fa'),
              ],
        to_diff=[(ph.inFile('reads_simulated_mates1.fa'),
                  ph.outFile('reads_simulated_mates1.fa'),
                  transforms),
                 (ph.inFile('reads_simulated_mates2.fa'),
                  ph.outFile('reads_simulated_mates2.fa'))])
    conf_list.append(conf)

    # ${JOINMATES} reads_simulated_joined_gold.fa \
    # -o reads_simulated_mates1.fa -o reads_simulated_mates2.fa \
    # > gustaf_mate_joining.stdout 2> gustaf_mate_joining.stderr

    # ============================================================
    # Gustaf Tests
    # ============================================================

    # ============================================================
    # Sanity check with default values and empty output file
    # ============================================================


    conf = app_tests.TestConf(
        program=path_to_program,
        redir_stdout=ph.outFile('st2_l100.stdout'),
        redir_stderr=ph.outFile('st2_l100.stderr'),
        args=[ph.inFile('adeno.fa'),
              ph.inFile('adeno_modified_reads.fa'),
              '-gff', ph.outFile('st2_l100.gff'),
              '-vcf', ph.outFile('st2_l100.vcf'),
              ],
        to_diff=[])#(ph.inFile('st2_l100.vcf'),
                 # ph.outFile('st2_l100.vcf'),
                 # transforms),
                 #(ph.inFile('st2_l100.gff'),
                 # ph.outFile('st2_l100.gff'))])
    conf_list.append(conf)

    #out="st2_l100"
    #${GUSTAF} adeno.fa adeno_modified_reads.fa -gff ${out}.gff -vcf ${out}.vcf > ${out}.stdout 2> ${out}.stderr

    # ============================================================
    # -st 1 -l 30
    # ============================================================


    conf = app_tests.TestConf(
        program=path_to_program,
        redir_stdout=ph.outFile('st1_l30.stdout'),
        redir_stderr=ph.outFile('st1_l30.stderr'),
        args=[ph.inFile('adeno.fa'),
              ph.inFile('adeno_modified_reads.fa'),
              '-gff', ph.outFile('st1_l30.gff'),
              '-vcf', ph.outFile('st1_l30.vcf'),
              '-st', str(1),
              '-l', str(30),
              ],
        to_diff=[(ph.inFile('st1_l30.vcf'),
                  ph.outFile('st1_l30.vcf'),
                  transforms),
                 (ph.inFile('st1_l30.gff'),
                  ph.outFile('st1_l30.gff'))])
    conf_list.append(conf)

    #out="st1_l30"
    #${GUSTAF} adeno.fa adeno_modified_reads.fa -st 1 -l 30 -gff ${out}.gff -vcf ${out}.vcf > ${out}.stdout 2> ${out}.stderr

    # ============================================================
    # -st 1 -m stellar.gff
    # ============================================================

    conf = app_tests.TestConf(
        program=path_to_program,
        redir_stdout=ph.outFile('st1_l30_m.stdout'),
        redir_stderr=ph.outFile('st1_l30_m.stderr'),
        args=[ph.inFile('adeno.fa'),
              ph.inFile('adeno_modified_reads.fa'),
              '-m', ph.inFile('stellar.gff'),
              '-gff', ph.outFile('st1_l30_m.gff'),
              '-vcf', ph.outFile('st1_l30_m.vcf'),
              '-st', str(1),
              ],
        to_diff=[(ph.inFile('st1_l30_m.vcf'),
                  ph.outFile('st1_l30_m.vcf'),
                  transforms),
                 (ph.inFile('st1_l30_m.gff'),
                  ph.outFile('st1_l30_m.gff'))])
    conf_list.append(conf)

    #out="st1_l30_m"
    #${GUSTAF} adeno.fa adeno_modified_reads.fa -st 1 -m stellar.gff -gff ${out}.gff -vcf ${out}.vcf > ${out}.stdout 2> ${out}.stderr

    # ============================================================
    # -st 1 -l 30 -ith 5
    # ============================================================

    conf = app_tests.TestConf(
        program=path_to_program,
        redir_stdout=ph.outFile('st1_l30_ith5.stdout'),
        redir_stderr=ph.outFile('st1_l30_ith5.stderr'),
        args=[ph.inFile('adeno.fa'),
              ph.inFile('adeno_modified_reads.fa'),
              '-gff', ph.outFile('st1_l30_ith5.gff'),
              '-vcf', ph.outFile('st1_l30_ith5.vcf'),
              '-st', str(1),
              '-l', str(30),
              '-ith', str(5),
              '-bth', str(5),
              ],
        to_diff=[(ph.inFile('st1_l30_m.vcf'),
                  ph.outFile('st1_l30_m.vcf'),
                  transforms),
                 (ph.inFile('st1_l30_ith5.gff'),
                  ph.outFile('st1_l30_ith5.gff'))])
    conf_list.append(conf)

    #out="st1_l30_ith5"
    #${GUSTAF} adeno.fa adeno_modified_reads.fa -st 1 -l 30 -ith 5 -bth 5 -gff ${out}.gff -vcf ${out}.vcf > ${out}.stdout 2> ${out}.stderr

    # ============================================================
    # -st 1 -l 30 -gth 3
    # ============================================================

    conf = app_tests.TestConf(
        program=path_to_program,
        redir_stdout=ph.outFile('st1_l30_gth3.stdout'),
        redir_stderr=ph.outFile('st1_l30_gth3.stderr'),
        args=[ph.inFile('adeno.fa'),
              ph.inFile('adeno_modified_reads.fa'),
              '-gff', ph.outFile('st1_l30_gth3.gff'),
              '-vcf', ph.outFile('st1_l30_gth3.vcf'),
              '-st', str(1),
              '-l', str(30),
              '-gth', str(3),
              ],
        to_diff=[(ph.inFile('st1_l30_m.vcf'),
                  ph.outFile('st1_l30_m.vcf'),
                  transforms),
                 (ph.inFile('st1_l30_gth3.gff'),
                  ph.outFile('st1_l30_gth3.gff'))])
    conf_list.append(conf)

    #out="st1_l30_gth3"
    #${GUSTAF} adeno.fa adeno_modified_reads.fa -st 1 -l 30 -gth 3 -gff ${out}.gff -vcf ${out}.vcf > ${out}.stdout 2> ${out}.stderr

    # ============================================================
    # paired-end
    # -st 1 -m stellar_joinedMates_l30.gff
    # ============================================================

    conf = app_tests.TestConf(
        program=path_to_program,
        redir_stdout=ph.outFile('pairedEnd_st1_l30.stdout'),
        redir_stderr=ph.outFile('pairedEnd_st1_l30.stderr'),
        args=[ph.inFile('adeno.fa'),
              ph.inFile('adeno_modified_reads_mates1.fa'),
              ph.inFile('adeno_modified_reads_mates2.fa'),
              '-m', ph.inFile('stellar_joinedMates_l30.gff'),
              '-gff', ph.outFile('pairedEnd_st1_l30.gff'),
              '-vcf', ph.outFile('pairedEnd_st1_l30.vcf'),
              '-st', str(1),
              '-mst', str(1),
              '-ll', str(1000),
              '-le', str(100),
              '-rc',
              ],
        to_diff=[(ph.inFile('pairedEnd_st1_l30.vcf'),
                  ph.outFile('pairedEnd_st1_l30.vcf'),
                  transforms),
                 (ph.inFile('pairedEnd_st1_l30.gff'),
                  ph.outFile('pairedEnd_st1_l30.gff'))])
    conf_list.append(conf)

    #out="pairedEnd_st1_l30"
    #${GUSTAF} adeno.fa adeno_modified_reads_mates1.fa adeno_modified_reads_mates2.fa -m stellar_joinedMates_l30.gff -st 1
    #-mst 1 -ll 1000 -le 30 -rc -gff ${out}.gff -vcf ${out}.vcf > ${out}.stdout 2> ${out}.stderr

    # ============================================================
    # Sanity check multiple references
    # -st 1 -l 30
    # ============================================================

    conf = app_tests.TestConf(
        program=path_to_program,
        redir_stdout=ph.outFile('reference2_st1_l30.stdout'),
        redir_stderr=ph.outFile('reference2_st1_l30.stderr'),
        args=[ph.inFile('adeno.fa'),
              ph.inFile('read_reference2.fa'),
              '-gff', ph.outFile('reference2_st1_l30.gff'),
              '-vcf', ph.outFile('reference2_st1_l30.vcf'),
              '-st', str(1),
              '-l', str(30),
              ],
        to_diff=[(ph.inFile('reference2_st1_l30.vcf'),
                  ph.outFile('reference2_st1_l30.vcf'),
                  transforms),
                 (ph.inFile('reference2_st1_l30.gff'),
                  ph.outFile('reference2_st1_l30.gff'))])
    conf_list.append(conf)

    #out="reference2_st1_l30"
    #${GUSTAF} adeno.fa read_reference2.fa -st 1 \
    #-l 30 -gff ${out}.gff -vcf ${out}.vcf > ${out}.stdout 2> ${out}.stderr
    # ============================================================
    # Execute the tests.
    # ============================================================
    failures = 0
    for conf in conf_list:
        res = app_tests.runTest(conf)
        # Output to the user.
        print ' '.join(['gustaf'] + conf.args),
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
