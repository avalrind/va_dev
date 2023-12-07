import setuptools

setuptools.setup(
    name = 'va_dev' ,
    version = '0.0.1' , 
    author = "Ayush Singhal",
    description = 'Loads different functions form different non-python files' ,
    long_description = 'Sample Description' ,
    long_description_content_type = 'text/markdown' ,
    packages=setuptools.find_packages() ,
    classifiers = [
        'Programming Language :: Python :: 3' ,
        'License :: OSI Approved :: MIT License' ,
        'Operating System :: OS Independent' ,
    ] ,
    python_requires = '>=3.6' , 
    py_modules = ['va_dev'] , 
    package_dir = {'':'va_dev/src'} ,
    install_requires = []
)
