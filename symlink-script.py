import os
import sys
import pandas as pd

ATAC_seq_dict = {
    'P013':['A4','WD','1'], 'P014':['A4','WD','2'], 'P015':['A4','WD','4'],
    'P004':['A4','ED','2'], 'P005':['A4','ED','3'], 'P006':['A4','ED','4'],
    'P028':['A5','WD','1'], 'P029':['A5','WD','2'], 'P030':['A5','WD','3'],
    'P019':['A5','ED','1'], 'P020':['A5','ED','2'], 'P021':['A5','ED','3'],
    'P043':['A6','WD','1'], 'P044':['A6','WD','2'], 'P045':['A6','WD','3'],
    'P034':['A6','ED','1'], 'P035':['A6','ED','2'], 'P036':['A6','ED','3'],
    'P058':['A7','WD','1'], 'P059':['A7','WD','2'], 'P060':['A7','WD','3'],
    'P049':['A7','ED','1'], 'P050':['A7','ED','2'], 'P051':['A7','ED','3']
}

DNA_seq_dict = {
    'ADL06': 'A4', 'ADL09': 'A5', 'ADL10': 'A6', 'ADL14': 'A7'
}

#function for moving up a directory
def par_dir():
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)
    return

#function for creating a directory in the existing directory
def create_dir(f_name):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'' + str(f_name))
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    return final_directory

#Create the name of your top level directory with command line argument
create_dir(sys.argv[1])


ATAC_path = '/data/class/ecoevo283/public/RAWDATA/ATACseq/'
DNA_path = '/data/class/ecoevo283/public/RAWDATA/DNAseq/'
RNA_path = '/data/class/ecoevo283/public/RAWDATA/RNAseq/'

os.chdir(str(sys.argv[1]))

create_dir('ATACseq')
os.chdir('ATACseq')

#Create symlinks for all the ATACseq fastq gz files
for filename in os.listdir(ATAC_path):
    if filename.endswith('.gz'):
        barcode = ''
        sym = ATAC_path + filename
        for i in range(33,37):
            barcode = barcode + str(filename[i])
        if filename[38:40] == 'R1':
            new_name = ATAC_seq_dict[barcode][0] + '_' + ATAC_seq_dict[barcode][1] + '_' + ATAC_seq_dict[barcode][2] + '_' + 'R1' + '.fq.gz'
        else:
            new_name = ATAC_seq_dict[barcode][0] + '_' + ATAC_seq_dict[barcode][1] + '_' + ATAC_seq_dict[barcode][2] + '_' + 'R2' + '.fq.gz'
        os.symlink(sym, new_name)
os.symlink(ATAC_path + 'README.ATACseq.txt', 'README.ATACseq.txt')
print('ATACseq symlinks created')

par_dir()
create_dir('DNAseq')
os.chdir('DNAseq')

#Create symlinks for all the DNAseq fastq gz files
for f in os.listdir(DNA_path):
    if f.endswith('.gz'):
        barcode1 = ''
        sym1 = DNA_path + f
        for i in range(0,5):
            barcode1 = barcode1 + f[i]
        new_name = DNA_seq_dict[barcode1]
        os.symlink(sym1, f.replace(barcode1, new_name))
os.symlink(DNA_path + 'README.DNA_samples.txt', 'README.DNA_samples.txt')
print('DNAseq symlinks created')

par_dir()
create_dir('RNAseq')
os.chdir('RNAseq')

readme = pd.read_excel(RNA_path + 'RNAseq384_SampleCoding.xlsx')

#Create symlinks for all the RNAseq fastq gz files
i=0
for subdir, dirs, files in os.walk(RNA_path):
    if 'Undetermined_indices' in dirs:
        dirs.remove('Undetermined_indices')
    for file in files:
        if file.endswith('.gz'):
            samp_num = str(file.split('_')[0])
            full_num = readme.loc[readme['SampleNumber'] == int(samp_num), 'FullSampleName'].item()
            path_name = str(os.path.join(subdir,file))
            if 'R1' in str(file):
                read_num = 'R1'
            elif 'R2' in str(file):
                read_num = 'R2'
            os.symlink(path_name, full_num + '_' + read_num + ".fq.gz")
            i += 1
print("RNAseq symlinks created")            
print("this is the total number of fastq files in the RNA-seq experiment: " + str(i))

par_dir()
par_dir()