#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: run.py
#          Desc:
#        Author: Chu Yanshuo
#         Email: chu@yanshuo.name
#      HomePage: http://yanshuo.name
#       Version: 0.0.1
#    LastChange: 2018-03-13 14:38:10
#       History:
# =============================================================================
'''

import argparse

from phySCNAClonal.preprocess.run_preprocess import run_preprocess
from phySCNAClonal.model.evolve import process

parser = argparse.ArgumentParser(
    description=
        'Run phySCNAClonal to infer subclonal composition from SCNA stripes',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

subparsers = parser.add_subparsers()

################
#  preprocess  #
################

parserPreprocess = subparsers.add_parser('preprocess',
                                        help='''Out put preprocess format''')

parserPreprocess.add_argument('--nBamName',
                             help='''BAM file for normal sample.''')

parserPreprocess.add_argument('--tBamNameL', nargs='+',
                             help='''BAM files for tumor samples sorted in \
                               chronological order.''')

parserPreprocess.add_argument('--refFaName',
                             help='''FASTA file for reference genome.''')

parserPreprocess.add_argument( '--pathPreFix',
                             help='''Base name of the preprocessed input
                             file to be created.''')

parserPreprocess.add_argument('--bedNameL', nargs='+',
                             help='''BED files for segments of each sample in\
                               chronological order.''')

parserPreprocess.add_argument('--bedCorrectedPath',
                          help='''The name of corrected BICseq result file''')

parserPreprocess.add_argument('--pklPath',
                          help='''Load the pkl path''')


parserPreprocess.add_argument('--maxCopyNumber', default=6, type=int,
                          help='''Set the maximum copy number''')

parserPreprocess.add_argument('--subcloneNumL', args='+', type=int,
                          help='''Set the subclone numbers''')

parserPreprocess.add_argument('--baselineThredLOH', default=0.16, type=float,
                          help='''The threshold of LOH sites fraction
                              within each segment to
                              define the segment is LOH, the range is
                             [baseline_thred_LOH, 1]. Default is
                              0.16.''')

parserPreprocess.add_argument('--baselineThredAPM',
                          default=0.2, type=float,
                          help='''The threshold of average P and M SNP sites
                              fraction within each segment to
                              define the segment as baseline, the range is
                             [baseline_thred_APM, 1]. Default is
                              0.2.''')

parserPreprocess.add_argument( '--minDepth', default=20, type=int,
                             help='''Minimum reads depth required for both
                             normal and tumor samples.  Default is 20.''')

parserPreprocess.add_argument( '--minBqual', default=10, type=int,
                             help='''Minimum base quality required.
                             Default is 10.''')

parserPreprocess.add_argument( '--minMqual', default=10, type=int,
                             help='''Minimum mapping quality required.
                             Default is 10.''')

parserPreprocess.add_argument( '--processNum', default=1, type=int,
                             help='''Number of processes to launch for
                             preprocessing. Default is 1.''')

parserPreprocess.add_argument('--gcCorrectionMethod', default="auto",
                             help='''The gc correction method, one of auto and
                             visual''')

parserPreprocess.add_argument('--pklFlag', default=False, type=bool,
                               help='''The pkl flag''')

parserPreprocess.set_defaults(func=run_preprocess)

###################
#  model process  #
###################

parserModel = subparsers.add_parser('model',
                                    help='''Output model parameters format''')

parserModel.add_argument( '-b', '--write-backups-every',
                         dest='writeBackupsEvery', default=100, type=int,
                         help='Number of iterations to go between writing\
                         backups of program state')

parserModel.add_argument( '-S', '--write-state-every', dest='writeStateEvery',
                         default=10, type=int, help= 'Number of iterations\
                         between writing program state to disk. Higher values\
                         reduce IO burden at the cost of losing progress made\
                         if program is interrupted.')

parserModel.add_argument('-k', '--top-k-trees', dest='topKTrees',
                         default='topKTrees', help='Output file to save top-k\
                         trees in text format')

parserModel.add_argument('-f', '--clonal-freqs', dest='clonalFreqs',
                         default='clonalFrequencies', help='Output file to save\
                         clonal frequencies')

parserModel.add_argument('-B', '--burnin-samples',
                         dest='burninSampleNum', default=1000, type=int,
                         help='Number of burnin samples')

parserModel.add_argument('-s', '--mcmc-samples', dest='mcmcSampleNum',
                         default=2500, type=int, help='Number of MCMC samples')

parserModel.add_argument('-i', '--mh-iterations', dest='mhIterations',
                         default=5000, type=int, help='Number of\
                         Metropolis-Hastings iterations')

parserModel.add_argument('-r', '--random-seed', dest='randomSeed',
                         type=int, help='Random seed for initializing MCMC\
                         sampler')

parserModel.add_argument('-t', '--tmp-dir', dest='tmpDir', help='Path to\
                         directory for temporary files')

parserModel.add_argument('-p', '--params', dest='paramsFile', help='JSON\
                         file listing run parameters, generated by the parser')

parserModel.add_argument('stripesFile', help= 'File listing stripes(SCNA\
                         stripes). For proper format, see README.md.')

parserModel.set_defaults(func=process)


#################
#  postprocess  #
#################


parserPostprocess = subparsers.add_parser('postprocess',
                                help='''Output postprocess parameters format''')

parserPostprocess.add_argument( '--include-stripe-names',
                               dest='includeStripeNames', action='store_true',
                               help='Include stripe names in output \(which may\
                               be sensitive data\)')

parserPostprocess.add_argument('datasetName', help='Name identifying dataset')

parserPostprocess.add_argument('treeFile', help='File containing sampled trees')

parserPostprocess.add_argument('segPoolFile', help='File containing segment\
                               pool')

parserPostprocess.add_argument('treeSummaryOutput', help='Output file for\
                               JSON-formatted tree summaries')

parserPostprocess.add_argument('mutlistOutput', help='Output file for\
                               JSON-formatted list of mutations')

parserPostprocess.add_argument('mutassOutput', help= 'Output file for\
                               JSON-formatted list of SSMs and CNVs assigned to\
                               each subclone')

args = parser.parse_args()
args.func(args)