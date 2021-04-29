from setuptools import setup, find_packages

install_requires = [
    "selenium>=3.141.1",
    "setuptools>=41.0.0"]

try:
    import selenium

    se_version = selenium.__version__
except ImportError:
    install_requires.append(f"selenium=={se_version}")
    pass

setup(
    name="knu_lab_auto",
    version="0.0.1",
    description="Auto check about lab safety",
    url="https://github.com/keiohta/tf2rl",
    author="Kei Ohta",
    author_email="dev.ohtakei@gmail.com",
    license="MIT",
    packages=find_packages("."),
    install_requires=install_requires,
    extras_require=extras_require)
