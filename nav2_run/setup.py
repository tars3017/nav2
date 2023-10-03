import os
from glob import glob
from setuptools import setup

package_name = 'nav2_run'

setup(
    data_files=[
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.launch.py'))),
        (os.path.join('share', package_name, 'config'),
            glob(os.path.join('config', '*.yaml'))),
        (os.path.join('share', package_name, 'rviz'),
            glob(os.path.join('rviz', '*.rviz'))),
        (os.path.join('share', package_name, 'maps'),
            glob(os.path.join('maps', '*.yaml'))) 
        (os.path.join('share', package_name, 'maps'),
            glob(os.path.join('maps', '*.pgm'))) 
    ]
)