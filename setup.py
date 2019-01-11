from setuptools import setup, find_packages


setup(name='clpipe',
      version='0.1',
      description='Cohen Lab MRI processing pipeline',
      url = 'blank',
      author = 'Cohen Lab',
      author_email='cohenlab@email.unc.edu',
      license='MIT',
      include_package_data=True,
      packages=find_packages(),
      entry_points='''
      [console_scripts]
      fmriprep_process=clpipe.fmriprep_process:fmriprep_process
      ''',
      zip_safe=False
      )