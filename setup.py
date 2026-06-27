from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='streamlit-sp-cookies',
    version='0.1.1',
    author='AlesandrovSP',
    description='Persistent cookie manager for Streamlit',
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=["streamlit>=1.30.0"],
)
