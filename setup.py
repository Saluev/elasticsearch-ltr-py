import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="elasticsearch_ltr",
    version="1.0.0",
    author="Tigran Saluev",
    author_email="tigran@saluev.com",
    description="Python interface for Elasticsearch LTR extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Saluev/elasticsearch-ltr-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "elasticsearch>=7.0.0,<8.0.0",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
