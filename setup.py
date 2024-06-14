from setuptools import find_packages, setup
from typing import List

Hypen_e = '-e .'
def get_requirements(file_path:str)->List[str]:

    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", " ") for req in requirements]

        if Hypen_e in requirements:
            requirements.remove(Hypen_e)

    return requirements






setup(
    name = "real estate project",
    version='0.0.1',
    author="Pranav",
    author_email='pranav261001@gmail.com',
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt')
)

''' whenever setup.py runs find packages it will chcek in every folder 
where you have__init__.py, So it will directly consider that folder as a package

so we can import it as a package wherever we want'''