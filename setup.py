from distutils.core import setup

#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.
files = ["okexV3Turkey/*"]

setup(name = "okexV3Turkey",
    version = "0.1",
    description = "OKEX V3 unified RESTful API by Turkey Sui",
    author = "Turkey Sui",
    author_email = "whatever",
    url = "",
    #packages = ['package'],
    #'package' package must contain files (see list above)
    #I called the package 'package' thus cleverly confusing the whole issue...
    #This dict maps the package name =to=> directories
    #It says, package *needs* these files.
    package_data = {'package':files },
    #'runner' is in the root.
    scripts = ["runner"],
    long_description = """Really long text here.""" 
) 