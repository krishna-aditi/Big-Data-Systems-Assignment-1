from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description='Processing Storm data from SEVIR dataset in Google Big Query and visualizing insights from it using Google Data Studio. Used csv files as the data source for this project.',
    author='Aditi Krishna',
    license='MIT',
)
