#!/usr/bin/env python

#filter reads based with the help of mapping to a reference genome
#author: Shaokang Zhang
#contact: zskzsk@uga.edu

import os, sys, subprocess
from distutils.version import LooseVersion

from argparse import ArgumentParser
import os, sys, time


def parse_args():
    "Parse the input arguments, use '-h' for help."
    parser = ArgumentParser(description='run BWA, and get mapped paired fastq')
    parser.add_argument(
        '-i',
        type=str,
        nargs="+",
        required=True,
        help='raw reads files, fastq or fastq.gz format')
    parser.add_argument(
        '-r',
        type=str,
        required=True,
        help='reference genome of mapping',
    )
    parser.add_argument(
        '-s',
        type=str,
        default="1",
        required=True,
        help='how manny threads, e.g. 16')
    parser.add_argument(
        '-c',
        type=str,
        default="True",
        help=
        'True or Falsse, if clean mode is "True", the temp files will be removed'
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_file = args.i
    if len(input_file) == 2 and isinstance(input_file, list):
        for_fq = input_file[0]
        rev_fq = input_file[-1]
    database = args.r
    threads = args.s
    clean = args.c
    temp_id = time.strftime("%m_%d_%Y_%H_%M_%S", time.localtime())
    os.system("bwa index " + database)
    file1 = for_fq.strip()
    core_id = file1.split(".")[0].strip()
    sam = core_id + temp_id + ".sam"
    bam = core_id + temp_id + ".bam"
    sorted_bam = core_id + temp_id + "_sorted.bam"
    mapped_fq1 = for_fq + "_mapped.fq"
    mapped_fq2 = rev_fq + "_mapped.fq"
    os.system("bwa mem -t " + threads + " " + database + " " + for_fq + " " +
              rev_fq + " > " + sam)
    os.system(
        "samtools view -@ " + threads + " -F 4 -Sbh " + sam + " > " + bam)
    ### check the version of samtools then use differnt commands
    samtools_version = subprocess.Popen(
        ["samtools"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = samtools_version.communicate()
    version = err.split("ersion:")[1].strip().split(" ")[0].strip()
    print "check samtools version:", version
    if LooseVersion(version) <= LooseVersion("1.2"):
        os.system("samtools sort -@ " + threads + " -n " + bam + " " + core_id + temp_id +
                  "_sorted")
    else:
        os.system("samtools sort -@ " + threads + " -n " + bam + " >" + sorted_bam)
    ### end of samtools version check and its analysis
    os.system("bamToFastq -i " + sorted_bam + " -fq " + mapped_fq1 + " -fq2 " +
              mapped_fq2 + " 2>> data_log_" + temp_id + ".txt")  #2> /dev/null if want no output
    if clean == "True":
        os.system("rm " + sam + " " + bam + " " + sorted_bam)


if __name__ == '__main__':
    main()
