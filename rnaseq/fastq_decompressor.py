import logging
import os
import subprocess

from bz2 import BZ2File 


class FastQDecompressor(object):
    def __init__(self, compressed_fastq_file_path, decompression_dir=".", keep_original= True):
        self.compressed_fastq_file_path = compressed_fastq_file_path
        fastq_base= os.path.basename(self.compressed_fastq_file_path.rstrip(".bz2"))
        self.fastq_file_path= os.path.join(decompression_dir, fastq_base)
        self.decompression_dir= decompression_dir
    
        self.keep_original = keep_original
        
        self.set_logger()
        ### log
        self.logger.debug("Decompressing %s" % os.path.basename(compressed_fastq_file_path))
        self.decompress_alt()
        self.logger.debug("Decompression finished!")
    
    def set_logger(self):
        self.logger= logging.getLogger("rnaseq.fastq_decompressor.FastQDecomompressor")
        self.logger.setLevel(logging.DEBUG)


    def decompress_alt(self):
        
        command_line= "sbatch decompress.sh %s %s" %(self.compressed_fastq_file_path, self.fastq_file_path)
        p = subprocess.Popen(command_line, shell= True, stderr=subprocess.STDOUT)
        out, err = p.communicate()
        ### log
        self.logger.debug(out)


    
    def decompress(self):
        compressed_fastq_file = BZ2File(self.compressed_fastq_file_path)
        fastq_file= open(self.fastq_file_path, mode= "w")
            
        fastq_file.writelines(compressed_fastq_file.read())
    
        if not self.keep_original:
            os.remove(self.compressed_fastq_file_path)
    
        return self.fastq_file_path


