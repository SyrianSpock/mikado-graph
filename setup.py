import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mikado_graph",
    version="0.1.0",
    author="Salah Missri",
    author_email="syrianspock@gmail.com",
    description="Python tool to draw graphs for Mikado refactoring",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/syrianspock/mikado-graph",
    packages=setuptools.find_packages(),
    install_requires=[
        "graphviz",
        "watchdog",
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
