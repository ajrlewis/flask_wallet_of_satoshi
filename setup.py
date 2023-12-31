from setuptools import setup, find_packages

setup(
    name="flask_wallet_of_satoshi",
    version="0.2",
    packages=["flask_wallet_of_satoshi"],
    install_requires=[
        "Flask",
        "wallet_of_satoshi @ git+https://github.com/ajrlewis/wallet_of_satoshi.git",
    ],
    url="https://github.com/ajrlewis/flask_wallet_of_satoshi",
    author="ajrlewis",
    author_email="hello@ajrlewis.com",
    description="Flask extension for Wallet of Satoshi",
)
