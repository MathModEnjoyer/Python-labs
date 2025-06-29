from setuptools import setup

setup(
    name='analyzerdf',
    version='0.1',
    description='A package of DataFrame analyzer',
    author='Lev Shimchenko',
    author_email='lev.shimchlev@gmail.com',
    packages=['analyzerdf'],
    install_requires=[
        'matplotlib',
        'statsmodels',
        'pandas',
        'openpyxl',
        'numpy'
    ],
)