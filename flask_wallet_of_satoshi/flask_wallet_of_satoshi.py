from flask import jsonify
from wallet_of_satoshi import WalletOfSatoshi as _WalletOfSatoshi


class WalletOfSatoshi:
    def __init__(self, app=None):
        self.app = app
        self.wallet = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.route("/.well-known/lnurl/pay")(self.lnurl_pay)

        @app.errorhandler(500)
        def handle_error(error):
            return jsonify({"error": "Wallet of Satoshi username not configured."}), 500

    def lnurl_pay(self):
        username = self.app.config.get("WOS_USERNAME")
        if not username:
            return "", 500

        if not self.wallet:
            self.wallet = _WalletOfSatoshi(username)

        lnurlp = self.wallet.well_known()
        return jsonify(lnurlp)
