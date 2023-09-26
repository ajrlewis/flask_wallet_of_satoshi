# FlaskWalletOfSatoshi

![My Project Logo](images/logo.png)

A Flask wrapper for the WalletOfSatoshi package (https://github.com/ajrlewis/wallet_of_satoshi.git).

## Installation

Install via pip:

```bash
pip install git+https://github.com/ajrlewis/flask_wallet_of_satoshi.git
```

## Usage

Create and load the following environment variables:

```.env
WOS_USERNAME="your-wallet-of-satoshi-username"
WOS_USERNAME_ALIAS="username-alias"
```

Use in the application as follows:

```app.py
from flask_wallet_of_satoshi import WalletOfSatoshi
from config import Config

wos = WalletOfSatoshi()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    wos.init_app(app=app)
    ...
```

It adds two routes:

    1. example.com/.well-known/lnurl/<username-alias>
    2. example.com/lightning/lnurl/pay

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

