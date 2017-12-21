#!/usr/bin/env python

#filter reads based on kraken analysis
#author: Shaokang Zhang
#contact: zskzsk@uga.edu

from argparse import ArgumentParser
import os, sys, time


def parse_args():
    "Parse the input arguments, use '-h' for help."
    parser = ArgumentParser(
        description='run kraken and filter reads based on kraken analysis')
    parser.add_argument(
        '-i',
        type=str,
        nargs="+",
        required=True,
        help='fastq or fastq.gz format')
    parser.add_argument(
        '-d',
        type=str,
        required=True,
        metavar='database path of kraken',
        help='e.g. /home/programs/kraken-XXX/std_db')
    parser.add_argument(
        '-t',
        type=str,
        required=False,
        default='fastq.gz',
        help='Type of data: "fastq.gz" (default), "fastq"')
    parser.add_argument(
        '-s',
        type=str,
        default="1",
        required=True,
        help='how manny threads, e.g. 16')
    parser.add_argument(
        '-k',
        type=str,
        required=False,
        help=
        'The unique characters of the genus name you want to extract; for example, Salmonella, or Escherichia_coli, or Listeria_mono'
    )
    parser.add_argument(
        '-o',
        type=str,
        required=True,
        metavar='output prefix',
        help=
        'e.g. if "Salmonella_reads", then the output will be Salmonella_reads_1.fastq and Salmonella_reads_2.fastq'
    )
    parser.add_argument(
        '-c',
        type=str,
        default="True",
        metavar='clean mode',
        help='if clean mode is True, the temp files will be removed')
    return parser.parse_args()


def main():
    args = parse_args()
    input_file = args.i
    data_type = args.t
    keystring = args.k
    database = args.d
    threads = args.s
    prefix = args.o
    clean = args.c
    temp_kraken = "kraken_" + time.strftime("%m_%d_%Y_%H_%M_%S",
                                            time.localtime()) + ".txt"
    temp_kraken_translate = "kraken_" + time.strftime(
        "%m_%d_%Y_%H_%M_%S", time.localtime()) + "_translate.txt"
    if len(input_file) == 2 and isinstance(input_file, list):
        if data_type == "fastq":
            os.system("kraken --db " + database + " --threads " + threads +
                      " --fastq-input --paired " + input_file[0] + " " +
                      input_file[1] + " > " + temp_kraken)
        elif data_type == "fastq.gz":
            os.system(
                "kraken --db " + database + " --threads " + threads +
                " --fastq-input --gzip-compressed --paired " + input_file[0] +
                " " + input_file[1] + " > " + temp_kraken)
    else:
        if data_type == "fastq":
            os.system("kraken --db " + database + " --threads " + threads +
                      " --fastq-input " + input_file + " > " + temp_kraken)
        elif data_type == "fastq.gz":
            os.system("kraken --db " + database + " --threads " + threads +
                      " --fastq-input --gzip-compressed " + input_file +
                      " > " + temp_kraken)
    os.system("kraken-translate --db " + database + " " + temp_kraken + " > " +
              temp_kraken_translate)
    key_word_transsum = temp_kraken_translate.replace(
        ".txt", "_" + keystring + "_translate.txt")
    os.system("cat " + temp_kraken_translate + "|grep " + keystring + " > " +
              key_word_transsum)
    key_word_transsum_title = key_word_transsum.replace(
        ".txt", "_reads_title.txt")
    os.system("cat " + key_word_transsum + " | awk '{print $1}' > " +
              key_word_transsum_title)
    if len(input_file) == 2 and isinstance(input_file, list):
        os.system('sed -i "s/\/1/\ 1/g" '+input_file[0])
        os.system('sed -i "s/\/2/\ 2/g" '+input_file[1])
        output_for = prefix + "_1.fastq"
        output_rev = prefix + "_2.fastq"
        os.system("seqtk subseq " + input_file[0] + " " +
                  key_word_transsum_title + " > " + output_for)
        os.system("seqtk subseq " + input_file[1] + " " +
                  key_word_transsum_title + " > " + output_rev)
    else:
        output_reads = prefix + ".fastq"
        os.system('sed -i "s/\/1/\ 1/g" '+input_file)
        os.system("seqtk subseq " + input_file + " " + key_word_transsum_title +
                  " > " + output_reads)
    if clean == "True":
        os.system("rm " + temp_kraken + " " + temp_kraken_translate + " " +
                  key_word_transsum + " " + key_word_transsum_title)


if __name__ == '__main__':
    main()
