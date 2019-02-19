import click
from .batch_manager import BatchManager,Job
from .config_json_parser import ConfigParser
import os
from pkg_resources import resource_stream, resource_filename

@click.command()
@click.option('-config_file', type=click.Path(exists=True, dir_okay=False, file_okay=True), default = None)
@click.option('-subject', required=True, default=None)
@click.option('-session', default=None)
@click.option('-dicom_directory', required = True)
@click.option('-output_file', default = "dicom_info.tsv")
@click.option('-submit', is_flag = True, default=False)
def dicom_to_nifti_to_bids_converter_setup(subject = None, session = None, dicom_directory=None, output_file=None, config_file = None,  submit=False):

    #TODO: This function should run heudiconv with a default heuristic file
    # on one subject, pull the scan info file out of the directory and put it
    # in the output file, and then delete the test directory that was generated by heudiconv.
    # The key difficulty will be in copying the scaninfo file after heudiconv is done.
    # this potentially could be done with a dependency statement in a batch command.
    # To submit batch commmands, use the BatchManager class

    #Do I need to update config file with date ran for just this? Or validate after? It doesn't seem any of this is going in
    config = ConfigParser()
    config.config_updater(config_file)

    heuristic_file = resource_filename(__name__, 'data/setup_heuristic.py')

    if session:
        heudiconv_string = '''module add heudiconv \n heudiconv -d {dicomdirectory} -s {subject} '''\
        ''' -ss {sess} -f {heuristic} -o ./test/ -b --minmeta \n cp ./test/ '''\
        '''.heudiconv/{subject}/ses-{sess}/info/dicominfo_ses-{sess}.tsv {outputfile} \n rm -rf ./test/'''
    else:
        heudiconv_string = '''module add heudiconv \n heudiconv -d {dicomdirectory} -s {subject} ''' \
                           ''' -f {heuristic} -o ./test/ -b --minmeta \n cp ./test/ ''' \
                           '''.heudiconv/{subject}/info/dicominfo.tsv {outputfile} \n rm -rf ./test/'''
    #Turns out -c is the type of converter to use. It doesn't say anywhere what the default is, but I assume it's dcm2niix.
    #I have seen other examples of people using other converters, but for now I think we can get rid of it


    batch_manager = BatchManager(config.config['BatchConfig'], None)
    if session:
        job1 = Job("heudiconv_setup", heudiconv_string.format(
            dicomdirectory=os.path.abspath(dicom_directory),
            subject=subject,
            sess=session,
            heuristic = heuristic_file,
            outputfile = os.path.abspath(output_file),
        ))
    else:
        job1 = Job("heudiconv_setup", heudiconv_string.format(
            dicomdirectory=os.path.abspath(dicom_directory),
            subject=subject,
            heuristic = heuristic_file,
            outputfile = os.path.abspath(output_file),
        ))
        
    batch_manager.addjob(job1)
    batch_manager.compilejobstrings()
    if submit:
        batch_manager.submit_jobs()
    else:
        batch_manager.print_jobs()